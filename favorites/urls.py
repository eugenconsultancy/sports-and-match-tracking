"""
URL configuration for favorites app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserFavoriteTeamViewSet, UserFavoriteMatchViewSet,
    UserFavoriteCompetitionViewSet
)

router = DefaultRouter()
router.register(r'teams', UserFavoriteTeamViewSet, basename='favorite-team')
router.register(r'matches', UserFavoriteMatchViewSet, basename='favorite-match')
router.register(r'competitions', UserFavoriteCompetitionViewSet, basename='favorite-competition')

urlpatterns = [
    path('', include(router.urls)),
]