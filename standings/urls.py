"""
URL configuration for standings app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StandingViewSet, TeamStandingViewSet, StandingRuleViewSet

router = DefaultRouter()
router.register(r'standings', StandingViewSet, basename='standing')
router.register(r'team-standings', TeamStandingViewSet, basename='teamstanding')
router.register(r'rules', StandingRuleViewSet, basename='standingrule')

urlpatterns = [
    path('', include(router.urls)),
]