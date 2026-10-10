"""
URL configuration for competitions app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CompetitionViewSet, SeasonViewSet, StageViewSet, GroupViewSet

router = DefaultRouter()
router.register(r'competitions', CompetitionViewSet, basename='competition')
router.register(r'seasons', SeasonViewSet, basename='season')
router.register(r'stages', StageViewSet, basename='stage')
router.register(r'groups', GroupViewSet, basename='group')

urlpatterns = [
    path('', include(router.urls)),
]