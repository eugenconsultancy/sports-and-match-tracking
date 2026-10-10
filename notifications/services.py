"""
Service layer for notifications app.
Contains business logic for notification creation and delivery.
"""
import logging
from django.db import transaction
from django.db.models import Q

logger = logging.getLogger(__name__)


class NotificationService:
    """Service class for notification-related business logic."""
    
    @staticmethod
    @transaction.atomic
    def create_notification(notification_type, title, body, data_payload=None, is_system=False):
        """Create a new notification."""
        from .models import Notification
        
        notification = Notification.objects.create(
            notification_type=notification_type,
            title=title,
            body=body,
            data_payload=data_payload or {},
            is_system=is_system,
        )
        
        return notification
    
    @staticmethod
    @transaction.atomic
    def send_to_users(notification, user_ids=None, delivery_status='pending'):
        """Send a notification to specific users or subscribers."""
        from .models import UserNotification
        from users_app.models import User
        
        if user_ids:
            users = User.objects.filter(id__in=user_ids, is_active=True)
        else:
            users = User.objects.filter(is_active=True)
        
        notifications = [
            UserNotification(
                user=user,
                notification=notification,
                delivery_status=delivery_status,
            )
            for user in users
        ]
        
        UserNotification.objects.bulk_create(notifications, batch_size=500)
        
        logger.info(f"Sent notification '{notification.title}' to {len(notifications)} users")
        return len(notifications)
    
    @staticmethod
    def send_match_notification(match, notification_type):
        """Send a match-related notification to subscribed users."""
        from .models import Notification, UserNotification, Subscription
        
        # Create notification
        title = f"{match.home_team.name} vs {match.away_team.name}"
        
        type_messages = {
            'match_start': f"Kickoff! {title} is starting now.",
            'goal': f"GOAL! {title} - score update.",
            'red_card': f"RED CARD! {title} - player sent off.",
            'half_time': f"Half Time: {title} {match.home_score}-{match.away_score}",
            'full_time': f"Full Time: {title} {match.home_score}-{match.away_score}",
        }
        
        body = type_messages.get(notification_type, f"Update: {title}")
        
        notification = NotificationService.create_notification(
            notification_type=notification_type,
            title=title,
            body=body,
            data_payload={
                'match_id': str(match.id),
                'home_team': match.home_team.name,
                'away_team': match.away_team.name,
                'home_score': match.home_score,
                'away_score': match.away_score,
                'status': match.status,
            }
        )
        
        # Find subscribed users
        subscriptions = Subscription.objects.filter(
            Q(match=match) |
            Q(team__in=[match.home_team, match.away_team]) |
            Q(competition=match.competition_season.competition),
            is_active=True,
            notification_types__contains=[notification_type],
        ).select_related('user').distinct('user')
        
        user_ids = [sub.user_id for sub in subscriptions]
        
        count = NotificationService.send_to_users(notification, user_ids)
        logger.info(f"Sent {notification_type} notification for match {match.id} to {count} users")
        
        return notification
    
    @staticmethod
    def mark_all_read(user_id):
        """Mark all notifications as read for a user."""
        from .models import UserNotification
        from django.utils import timezone
        
        updated = UserNotification.objects.filter(
            user_id=user_id,
            delivery_status__in=['sent', 'delivered']
        ).update(
            delivery_status='read',
            read_at=timezone.now()
        )
        
        return updated
    
    @staticmethod
    def get_unread_count(user_id):
        """Get count of unread notifications for a user."""
        from .models import UserNotification
        
        return UserNotification.objects.filter(
            user_id=user_id,
            delivery_status__in=['sent', 'delivered']
        ).count()
    
    @staticmethod
    def cleanup_old_notifications(days=30):
        """Delete notifications older than specified days."""
        from .models import UserNotification
        from django.utils import timezone
        from datetime import timedelta
        
        cutoff = timezone.now() - timedelta(days=days)
        deleted, _ = UserNotification.objects.filter(
            created_at__lt=cutoff,
            delivery_status='read'
        ).delete()
        
        logger.info(f"Cleaned up {deleted} old notifications")
        return deleted