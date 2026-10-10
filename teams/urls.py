"""
URL configuration for teams app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeamViewSet, VenueViewSet, CoachViewSet, TeamSeasonViewSet

router = DefaultRouter()
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'venues', VenueViewSet, basename='venue')
router.register(r'coaches', CoachViewSet, basename='coach')
router.register(r'team-seasons', TeamSeasonViewSet, basename='teamseason')

urlpatterns = [
    path('', include(router.urls)),
]