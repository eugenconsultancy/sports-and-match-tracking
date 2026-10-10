"""
Views for polls app.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db import transaction

from .models import Poll, PollOption, Vote, PollResultCache
from .serializers import (
    PollListSerializer, PollDetailSerializer,
    PollOptionSerializer, VoteSerializer, CreateVoteSerializer,
    PollResultCacheSerializer
)


class PollViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for polls."""
    
    queryset = Poll.objects.select_related(
        'match__home_team', 'match__away_team'
    ).prefetch_related('options', 'result_cache').all()
    
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['match', 'status', 'is_featured']
    ordering_fields = ['created_at', 'total_votes', 'start_time']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PollListSerializer
        return PollDetailSerializer
    
    @action(detail=False, methods=['get'])
    def active(self, request):
        """Get all active polls."""
        polls = Poll.objects.filter(
            status='active'
        ).select_related(
            'match__home_team', 'match__away_team'
        ).prefetch_related('options', 'result_cache').order_by('-total_votes')
        
        page = self.paginate_queryset(polls)
        if page is not None:
            serializer = PollListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = PollListSerializer(polls, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured polls."""
        polls = Poll.objects.filter(
            is_featured=True, status='active'
        ).select_related(
            'match__home_team', 'match__away_team'
        ).prefetch_related('options', 'result_cache').order_by('-total_votes')[:10]
        
        serializer = PollListSerializer(polls, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def vote(self, request, pk=None):
        """Cast a vote on a poll."""
        poll = self.get_object()
        
        # Validate poll is active
        if poll.status != 'active':
            return Response(
                {'error': 'Poll is not active'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if poll.end_time and poll.end_time < timezone.now():
            return Response(
                {'error': 'Poll has ended'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate input
        serializer = CreateVoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        option_id = serializer.validated_data['option_id']
        
        # Check if user already voted
        existing_vote = Vote.objects.filter(poll=poll, user=request.user).first()
        
        with transaction.atomic():
            if existing_vote:
                # Update existing vote
                existing_vote.option_id = option_id
                existing_vote.save()
                message = "Vote updated successfully"
            else:
                # Create new vote
                Vote.objects.create(
                    poll=poll,
                    option_id=option_id,
                    user=request.user,
                    ip_address=self._get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
                message = "Vote recorded successfully"
            
            # Trigger cache update (async via Celery)
            from polls.tasks import update_poll_caches
            update_poll_caches.delay()
        
        # Return updated poll
        poll.refresh_from_db()
        return Response({
            'message': message,
            'poll': PollDetailSerializer(poll, context={'request': request}).data
        })
    
    def _get_client_ip(self, request):
        """Get client IP address."""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class PollOptionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for poll options."""
    
    queryset = PollOption.objects.select_related('poll', 'team').all()
    serializer_class = PollOptionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['poll', 'option_type']


class PollResultCacheViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for poll result caches."""
    
    queryset = PollResultCache.objects.select_related('poll').all()
    serializer_class = PollResultCacheSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['poll']