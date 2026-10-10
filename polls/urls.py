"""
URL configuration for polls app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PollViewSet, PollOptionViewSet, PollResultCacheViewSet

router = DefaultRouter()
router.register(r'polls', PollViewSet, basename='poll')
router.register(r'options', PollOptionViewSet, basename='polloption')
router.register(r'result-caches', PollResultCacheViewSet, basename='pollcache')

urlpatterns = [
    path('', include(router.urls)),
]