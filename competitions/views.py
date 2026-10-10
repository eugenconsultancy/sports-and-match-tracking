"""
Views for competitions app.
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Competition, Season, Stage, Group
from .serializers import (
    CompetitionListSerializer, CompetitionDetailSerializer,
    SeasonListSerializer, SeasonDetailSerializer,
    StageListSerializer, GroupListSerializer
)


class CompetitionViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for competitions."""
    
    queryset = Competition.objects.prefetch_related('seasons').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['competition_type', 'tier', 'country', 'is_active']
    search_fields = ['name', 'short_name', 'country']
    ordering_fields = ['name', 'tier', 'created_at']
    ordering = ['tier', 'name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CompetitionListSerializer
        return CompetitionDetailSerializer
    
    @method_decorator(cache_page(60 * 5))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def seasons(self, request, pk=None):
        """Get all seasons for a competition."""
        competition = self.get_object()
        seasons = competition.seasons.all().order_by('-start_date')
        page = self.paginate_queryset(seasons)
        if page is not None:
            serializer = SeasonListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = SeasonListSerializer(seasons, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def standings(self, request, pk=None):
        """Get current standings for competition."""
        competition = self.get_object()
        current_season = competition.seasons.filter(is_current=True).first()
        if not current_season:
            return Response({'error': 'No current season'}, status=404)
        
        from standings.models import Standing, TeamStanding
        from standings.serializers import StandingSerializer
        
        standings = Standing.objects.filter(
            competition_season=current_season
        ).prefetch_related('team_standings__team')
        
        serializer = StandingSerializer(standings, many=True)
        return Response(serializer.data)


class SeasonViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for seasons."""
    
    queryset = Season.objects.select_related('competition').all()
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['competition', 'status', 'is_current']
    ordering_fields = ['start_date', 'name']
    ordering = ['-start_date']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return SeasonListSerializer
        return SeasonDetailSerializer
    
    @action(detail=True, methods=['get'])
    def stages(self, request, pk=None):
        """Get all stages for a season."""
        season = self.get_object()
        stages = season.stages.all().order_by('order')
        serializer = StageListSerializer(stages, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def matches(self, request, pk=None):
        """Get all matches for a season."""
        from matches.models import Match
        from matches.serializers import MatchListSerializer
        
        season = self.get_object()
        matches = Match.objects.filter(
            competition_season=season
        ).select_related('home_team', 'away_team').order_by('-kickoff_time')
        
        page = self.paginate_queryset(matches)
        if page is not None:
            serializer = MatchListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = MatchListSerializer(matches, many=True)
        return Response(serializer.data)


class StageViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for stages."""
    
    queryset = Stage.objects.select_related('season').prefetch_related('groups').all()
    serializer_class = StageListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['season', 'stage_type', 'is_active']
    
    
class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for groups."""
    
    queryset = Group.objects.select_related('stage').prefetch_related('teams').all()
    serializer_class = GroupListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['stage']