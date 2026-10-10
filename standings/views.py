"""
Views for standings app.
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Standing, TeamStanding, StandingRule
from .serializers import (
    StandingSerializer, TeamStandingSerializer, StandingRuleSerializer
)


class StandingViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for standings tables."""
    
    queryset = Standing.objects.select_related(
        'competition_season__competition', 'stage', 'group'
    ).prefetch_related('team_standings__team').all()
    
    serializer_class = StandingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['competition_season', 'stage', 'group', 'standing_type', 'is_live']
    
    @method_decorator(cache_page(60 * 5))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def live(self, request):
        """Get all live standings (currently active competitions)."""
        standings = Standing.objects.filter(
            is_live=True
        ).select_related(
            'competition_season__competition', 'stage', 'group'
        ).prefetch_related('team_standings__team').all()
        
        serializer = self.get_serializer(standings, many=True)
        return Response(serializer.data)


class TeamStandingViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for individual team standings entries."""
    
    queryset = TeamStanding.objects.select_related(
        'standing', 'team'
    ).all()
    serializer_class = TeamStandingSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['standing', 'team']
    ordering_fields = ['position', 'points', 'goals_for']
    ordering = ['standing', 'position']


class StandingRuleViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for standing rules."""
    
    queryset = StandingRule.objects.select_related('competition').all()
    serializer_class = StandingRuleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['competition', 'is_active']
    ordering = ['competition', 'priority']