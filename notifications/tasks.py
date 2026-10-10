"""
Celery tasks for notifications app.
"""
import logging
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.db import transaction
from django.db.models import Q


logger = logging.getLogger(__name__)


@shared_task(bind=True)
def cleanup_old_notifications(self, days=30):
    """
    Delete notifications older than specified days.
    Runs daily at 2 AM.
    """
    from notifications.models import UserNotification
    
    cutoff_date = timezone.now() - timedelta(days=days)
    deleted, _ = UserNotification.objects.filter(
        created_at__lt=cutoff_date
    ).delete()
    
    logger.info(f"Cleaned up {deleted} old notifications")
    return f"Deleted {deleted} old notifications"


@shared_task(bind=True, max_retries=3)
def send_match_start_notifications(self, match_id):
    """
    Send push notifications for match start.
    """
    from matches.models import Match
    from notifications.models import Notification, UserNotification, Subscription
    from users_app.models import User, SessionDevice
    
    try:
        match = Match.objects.select_related('home_team', 'away_team').get(id=match_id)
        
        # Create notification
        notification = Notification.objects.create(
            notification_type='match_start',
            title=f"{match.home_team.name} vs {match.away_team.name}",
            body=f"The match is about to start! Kickoff at {match.kickoff_time.strftime('%H:%M')}",
            data_payload={
                'match_id': str(match.id),
                'home_team': match.home_team.name,
                'away_team': match.away_team.name,
            }
        )
        
        # Find subscribed users
        subscriptions = Subscription.objects.filter(
            Q(match=match) | Q(team__in=[match.home_team, match.away_team])
        ).select_related('user')
        
        # Create user notifications
        user_notifications = []
        for sub in subscriptions:
            user_notifications.append(UserNotification(
                user=sub.user,
                notification=notification,
                delivery_status='pending',
            ))
        
        UserNotification.objects.bulk_create(user_notifications)
        
        # In production, trigger push notification service
        # (Firebase Cloud Messaging, APNs, etc.)
        
        return f"Sent {len(user_notifications)} match start notifications"
        
    except Match.DoesNotExist:
        logger.error(f"Match {match_id} not found")
        return f"Match {match_id} not found"