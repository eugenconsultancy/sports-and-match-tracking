"""
URL configuration for matches app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MatchViewSet, MatchEventViewSet,
    LineupViewSet, MatchStatsViewSet
)

router = DefaultRouter()
router.register(r'matches', MatchViewSet, basename='match')
router.register(r'events', MatchEventViewSet, basename='event')
router.register(r'lineups', LineupViewSet, basename='lineup')
router.register(r'match-stats', MatchStatsViewSet, basename='matchstats')

urlpatterns = [
    path('', include(router.urls)),
]