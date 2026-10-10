"""
Views for matches app.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.utils import timezone
from datetime import timedelta
from django.db import models as db_models
from django.core.cache import cache

from .models import Match, MatchEvent, Lineup, MatchStats, MatchLiveState
from .serializers import (
    MatchListSerializer, MatchDetailSerializer,
    MatchEventSerializer, LineupSerializer,
    MatchStatsSerializer, MatchLiveStateSerializer
)
from .services.espn_api import espn_api


class MatchViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for matches."""
    
    queryset = Match.objects.select_related(
        'home_team', 'away_team', 'competition_season__competition'
    ).prefetch_related('events').all()
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'status', 'competition_season', 'home_team', 'away_team',
        'stage', 'group', 'is_featured'
    ]
    search_fields = ['home_team__name', 'away_team__name']
    ordering_fields = ['kickoff_time', 'home_score', 'away_score']
    ordering = ['-kickoff_time']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MatchListSerializer
        return MatchDetailSerializer
    
    @method_decorator(cache_page(30))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    # ============ DATABASE ENDPOINTS ============
    
    @action(detail=False, methods=['get'])
    def live(self, request):
        """Get all currently live matches from database."""
        matches = Match.objects.filter(
            status__in=[Match.Status.LIVE, Match.Status.HALF_TIME]
        ).select_related(
            'home_team', 'away_team', 'competition_season__competition'
        ).order_by('kickoff_time')
        
        serializer = MatchListSerializer(matches, many=True)
        return Response({
            'count': matches.count(),
            'matches': serializer.data,
        })
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """Get all matches scheduled for today."""
        today = timezone.now().date()
        matches = Match.objects.filter(
            kickoff_time__date=today
        ).select_related(
            'home_team', 'away_team', 'competition_season__competition'
        ).order_by('kickoff_time')
        
        serializer = MatchListSerializer(matches, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        """Get upcoming matches (next 7 days)."""
        now = timezone.now()
        end_date = now + timedelta(days=7)
        
        matches = Match.objects.filter(
            kickoff_time__gte=now,
            kickoff_time__lte=end_date,
            status=Match.Status.SCHEDULED
        ).select_related(
            'home_team', 'away_team', 'competition_season__competition'
        ).order_by('kickoff_time')
        
        page = self.paginate_queryset(matches)
        if page is not None:
            serializer = MatchListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = MatchListSerializer(matches, many=True)
        return Response(serializer.data)
    
    # ============ ESPN FREE API ENDPOINTS (WORKING) ============
    
    @action(detail=False, methods=['get'])
    def live_external(self, request):
        """Get live matches from ESPN Free API (no key required)."""
        cached_matches = cache.get('espn_live_matches')
        if cached_matches:
            return Response({
                'count': len(cached_matches),
                'matches': cached_matches,
                'source': 'cache'
            })
        
        sport = request.query_params.get('sport', 'soccer')
        live_matches = espn_api.get_live_scores(sport)
        cache.set('espn_live_matches', live_matches, 30)
        
        return Response({
            'count': len(live_matches),
            'matches': live_matches,
            'source': 'ESPN Free API',
            'sport': sport
        })
    
    @action(detail=False, methods=['get'])
    def refresh_live(self, request):
        """Force refresh live matches from ESPN Free API."""
        sport = request.query_params.get('sport', 'soccer')
        live_matches = espn_api.get_live_scores(sport)
        cache.set('espn_live_matches', live_matches, 30)
        
        return Response({
            'count': len(live_matches),
            'matches': live_matches,
            'refreshed_at': timezone.now().isoformat(),
            'sport': sport,
            'source': 'ESPN Free API'
        })
    
    @action(detail=False, methods=['get'])
    def search_teams(self, request):
        """Search for teams by name via ESPN API."""
        query = request.query_params.get('q', '')
        sport = request.query_params.get('sport', 'soccer')
        
        if not query:
            return Response({'error': 'q parameter required'}, status=400)
        
        teams = espn_api.search_teams(query, sport)
        
        return Response({
            'count': len(teams),
            'teams': teams,
            'query': query,
            'sport': sport,
            'source': 'ESPN Free API'
        })
    
    # ============ FLASHSCORE API ENDPOINTS (Return helpful message) ============
    
    @action(detail=False, methods=['get'])
    def flashscore_search(self, request):
        """FlashScore API - Please use /live_external/ endpoint instead."""
        return Response({
            'error': 'FlashScore API is not currently available. Please use the ESPN API endpoint.',
            'alternative': '/api/v1/matches/matches/live_external/',
            'message': 'The FlashScore API requires a separate subscription on RapidAPI.'
        }, status=503)
    
    @action(detail=False, methods=['get'])
    def flashscore_live(self, request):
        """FlashScore API - Please use /live_external/ endpoint instead."""
        return Response({
            'error': 'FlashScore API is not currently available. Please use the ESPN API endpoint.',
            'alternative': '/api/v1/matches/matches/live_external/',
            'message': 'The FlashScore API requires a separate subscription on RapidAPI.'
        }, status=503)
    
    @action(detail=False, methods=['get'])
    def flashscore_fixtures(self, request):
        """FlashScore API - Please use /upcoming/ endpoint instead."""
        return Response({
            'error': 'FlashScore API is not currently available.',
            'alternative': '/api/v1/matches/matches/upcoming/',
            'message': 'Use the upcoming endpoint for fixture data from your database.'
        }, status=503)
    
    @action(detail=True, methods=['get'])
    def flashscore_match(self, request, pk=None):
        """FlashScore API - Please use regular match endpoint."""
        return Response({
            'error': 'FlashScore API is not currently available.',
            'alternative': f'/api/v1/matches/matches/{pk}/',
            'message': 'Use the regular match detail endpoint.'
        }, status=503)
    
    @action(detail=False, methods=['get'])
    def flashscore_standings(self, request):
        """FlashScore API - Please use standings endpoint."""
        return Response({
            'error': 'FlashScore API is not currently available.',
            'alternative': '/api/v1/standings/standings/',
            'message': 'Use the standings endpoint for league tables.'
        }, status=503)
    
    @action(detail=False, methods=['get'])
    def flashscore_team(self, request):
        """FlashScore API - Please use teams endpoint."""
        return Response({
            'error': 'FlashScore API is not currently available.',
            'alternative': '/api/v1/teams/teams/',
            'message': 'Use the teams endpoint for team information.'
        }, status=503)
    
    # ============ MATCH DETAIL ENDPOINTS ============
    
    @action(detail=True, methods=['get'])
    def events(self, request, pk=None):
        """Get all events for a match."""
        match = self.get_object()
        events = match.events.all().order_by('minute', 'injury_minute')
        serializer = MatchEventSerializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def lineups(self, request, pk=None):
        """Get lineups for a match."""
        match = self.get_object()
        lineups = match.lineups.select_related('player', 'team').all()
        serializer = LineupSerializer(lineups, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get statistics for a match."""
        match = self.get_object()
        stats = match.stats.all()
        serializer = MatchStatsSerializer(stats, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def live_state(self, request, pk=None):
        """Get live match state."""
        match = self.get_object()
        if hasattr(match, 'live_state') and match.live_state:
            serializer = MatchLiveStateSerializer(match.live_state)
            return Response(serializer.data)
        return Response({'error': 'No live state available'}, status=404)


class MatchEventViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for match events."""
    
    queryset = MatchEvent.objects.select_related(
        'match', 'player', 'related_player', 'team'
    ).all()
    serializer_class = MatchEventSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['match', 'event_type', 'player', 'team']
    ordering = ['match', 'minute']


class LineupViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for lineups."""
    
    queryset = Lineup.objects.select_related('match', 'team', 'player').all()
    serializer_class = LineupSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['match', 'team', 'role']


class MatchStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for match statistics."""
    
    queryset = MatchStats.objects.select_related('match', 'team').all()
    serializer_class = MatchStatsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['match', 'team']