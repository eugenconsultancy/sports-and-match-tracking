"""
URL configuration for notifications app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserNotificationViewSet, SubscriptionViewSet

router = DefaultRouter()
router.register(r'notifications', UserNotificationViewSet, basename='notification')
router.register(r'subscriptions', SubscriptionViewSet, basename='subscription')

urlpatterns = [
    path('', include(router.urls)),
]