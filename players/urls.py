"""
URL configuration for players app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PlayerViewSet, PlayerStatsViewSet,
    PlayerMatchStatsViewSet, TransferHistoryViewSet
)

router = DefaultRouter()
router.register(r'players', PlayerViewSet, basename='player')
router.register(r'player-stats', PlayerStatsViewSet, basename='playerstats')
router.register(r'player-match-stats', PlayerMatchStatsViewSet, basename='playermatchstats')
router.register(r'transfers', TransferHistoryViewSet, basename='transfer')

urlpatterns = [
    path('', include(router.urls)),
]