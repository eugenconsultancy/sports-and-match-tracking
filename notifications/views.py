"""
Views for notifications app.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone

from .models import Notification, UserNotification, Subscription
from .serializers import (
    NotificationSerializer, UserNotificationSerializer, SubscriptionSerializer
)


class UserNotificationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for user notifications."""
    
    permission_classes = [IsAuthenticated]
    serializer_class = UserNotificationSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['delivery_status']
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    def get_queryset(self):
        return UserNotification.objects.filter(
            user=self.request.user
        ).select_related('notification').all()
    
    @action(detail=False, methods=['post'])
    def mark_all_read(self, request):
        """Mark all notifications as read."""
        updated = UserNotification.objects.filter(
            user=request.user,
            delivery_status__in=['sent', 'delivered']
        ).update(
            delivery_status='read',
            read_at=timezone.now()
        )
        
        return Response({'marked_read': updated})
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        """Mark a single notification as read."""
        notification = self.get_object()
        notification.delivery_status = 'read'
        notification.read_at = timezone.now()
        notification.save()
        
        return Response(UserNotificationSerializer(notification).data)
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        """Get count of unread notifications."""
        count = UserNotification.objects.filter(
            user=request.user,
            delivery_status__in=['sent', 'delivered']
        ).count()
        
        return Response({'unread_count': count})


class SubscriptionViewSet(viewsets.ModelViewSet):
    """ViewSet for notification subscriptions."""
    
    permission_classes = [IsAuthenticated]
    serializer_class = SubscriptionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['is_active', 'team', 'match', 'competition']
    
    def get_queryset(self):
        return Subscription.objects.filter(
            user=self.request.user
        ).select_related('team', 'match', 'competition', 'player').all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def subscribe(self, request):
        """Create a new subscription."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['delete'])
    def unsubscribe(self, request):
        """Remove a subscription."""
        subscription_id = request.data.get('subscription_id')
        if not subscription_id:
            return Response(
                {'error': 'subscription_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        deleted, _ = Subscription.objects.filter(
            user=request.user, id=subscription_id
        ).delete()
        
        if deleted:
            return Response({'message': 'Unsubscribed successfully'})
        return Response(
            {'error': 'Subscription not found'},
            status=status.HTTP_404_NOT_FOUND
        )