"""
Views for teams app.
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Team, Venue, Coach, TeamSeason
from .serializers import (
    TeamListSerializer, TeamDetailSerializer,
    VenueSerializer, CoachSerializer, TeamSeasonSerializer
)


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for teams."""
    
    queryset = Team.objects.prefetch_related(
        'current_coaches', 'current_players'
    ).all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['team_type', 'country', 'is_active']
    search_fields = ['name', 'short_name', 'country']
    ordering_fields = ['name', 'founded_year', 'created_at']
    ordering = ['name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TeamListSerializer
        return TeamDetailSerializer
    
    @method_decorator(cache_page(60 * 15))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def players(self, request, pk=None):
        """Get all current players for a team."""
        from players.models import Player
        from players.serializers import PlayerListSerializer
        
        team = self.get_object()
        players = team.current_players.all().order_by('position', 'last_name')
        page = self.paginate_queryset(players)
        if page is not None:
            serializer = PlayerListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = PlayerListSerializer(players, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def matches(self, request, pk=None):
        """Get recent and upcoming matches for a team."""
        from matches.models import Match
        from matches.serializers import MatchListSerializer
        
        team = self.get_object()
        matches = Match.objects.filter(
            models.Q(home_team=team) | models.Q(away_team=team)
        ).select_related('home_team', 'away_team', 'competition_season').order_by('-kickoff_time')
        
        # Get last 10 and next 10
        upcoming = matches.filter(status='scheduled').order_by('kickoff_time')[:10]
        recent = matches.filter(status='finished').order_by('-kickoff_time')[:10]
        
        return Response({
            'upcoming': MatchListSerializer(upcoming, many=True).data,
            'recent': MatchListSerializer(recent, many=True).data,
        })
    
    @action(detail=True, methods=['get'])
    def transfers(self, request, pk=None):
        """Get transfer history for a team."""
        from players.models import TransferHistory
        from players.serializers import TransferHistorySerializer
        
        team = self.get_object()
        transfers = TransferHistory.objects.filter(
            models.Q(from_team=team) | models.Q(to_team=team)
        ).select_related('player', 'from_team', 'to_team').order_by('-transfer_date')[:50]
        
        page = self.paginate_queryset(transfers)
        if page is not None:
            serializer = TransferHistorySerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = TransferHistorySerializer(transfers, many=True)
        return Response(serializer.data)


class VenueViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for venues."""
    
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['country', 'city']
    search_fields = ['name', 'city', 'country']


class CoachViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for coaches."""
    
    queryset = Coach.objects.select_related('current_team').all()
    serializer_class = CoachSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['nationality', 'current_team']
    search_fields = ['name', 'nationality']


class TeamSeasonViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for team season participations."""
    
    queryset = TeamSeason.objects.select_related(
        'team', 'season__competition', 'coach'
    ).all()
    serializer_class = TeamSeasonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['team', 'season']


# Import models for Q queries
from django.db import models