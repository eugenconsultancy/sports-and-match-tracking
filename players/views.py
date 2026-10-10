"""
Views for players app.
"""
from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from .models import Player, PlayerStats, PlayerMatchStats, TransferHistory
from .serializers import (
    PlayerListSerializer, PlayerDetailSerializer,
    PlayerStatsSerializer, PlayerMatchStatsSerializer,
    TransferHistorySerializer
)


class PlayerViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for players."""
    
    queryset = Player.objects.select_related('current_team').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nationality', 'position', 'current_team', 'is_active']
    search_fields = ['first_name', 'last_name', 'full_name', 'nationality']
    ordering_fields = ['full_name', 'market_value', 'date_of_birth']
    ordering = ['last_name', 'first_name']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PlayerListSerializer
        return PlayerDetailSerializer
    
    @method_decorator(cache_page(60 * 15))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get comprehensive stats for a player."""
        player = self.get_object()
        
        season_stats = player.season_stats.all()
        match_stats = player.match_stats.select_related('match').order_by('-match__kickoff_time')[:20]
        transfers = player.transfers.all().order_by('-transfer_date')
        
        return Response({
            'season_stats': PlayerStatsSerializer(season_stats, many=True).data,
            'recent_matches': PlayerMatchStatsSerializer(match_stats, many=True).data,
            'transfers': TransferHistorySerializer(transfers, many=True).data,
        })
    
    @action(detail=True, methods=['get'])
    def matches(self, request, pk=None):
        """Get match performances for a player."""
        player = self.get_object()
        match_stats = player.match_stats.select_related(
            'match__home_team', 'match__away_team'
        ).order_by('-match__kickoff_time')
        
        page = self.paginate_queryset(match_stats)
        if page is not None:
            serializer = PlayerMatchStatsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = PlayerMatchStatsSerializer(match_stats, many=True)
        return Response(serializer.data)


class PlayerStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for player season stats."""
    
    queryset = PlayerStats.objects.select_related('player', 'season', 'team').all()
    serializer_class = PlayerStatsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['player', 'season', 'team']
    ordering_fields = ['goals', 'assists', 'minutes_played', 'average_rating']
    ordering = ['-goals']


class PlayerMatchStatsViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for player match stats."""
    
    queryset = PlayerMatchStats.objects.select_related(
        'player', 'match', 'team'
    ).all()
    serializer_class = PlayerMatchStatsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['player', 'match', 'team', 'is_mvp']
    ordering_fields = ['rating', 'goals', 'assists']
    ordering = ['-rating']


class TransferHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for transfer history."""
    
    queryset = TransferHistory.objects.select_related(
        'player', 'from_team', 'to_team'
    ).all()
    serializer_class = TransferHistorySerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['player', 'from_team', 'to_team']
    ordering_fields = ['transfer_date', 'transfer_fee']
    ordering = ['-transfer_date']