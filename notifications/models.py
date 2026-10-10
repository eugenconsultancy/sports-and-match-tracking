"""
Notification-related models: notifications, user notifications, subscriptions.
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Notification(models.Model):
    """System notification template/definition."""
    
    class NotificationType(models.TextChoices):
        MATCH_START = 'match_start', _('Match Starting')
        GOAL = 'goal', _('Goal Scored')
        RED_CARD = 'red_card', _('Red Card')
        HALF_TIME = 'half_time', _('Half Time')
        FULL_TIME = 'full_time', _('Full Time')
        BREAKING_NEWS = 'breaking_news', _('Breaking News')
        TRANSFER = 'transfer', _('Transfer Update')
        LINEUP = 'lineup', _('Lineup Announced')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    notification_type = models.CharField(
        max_length=30, choices=NotificationType.choices, db_index=True
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    data_payload = models.JSONField(default=dict, blank=True)
    is_system = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['notification_type', '-created_at']),
        ]
    
    def __str__(self):
        return self.title


class UserNotification(models.Model):
    """User-specific notification delivery."""
    
    class DeliveryStatus(models.TextChoices):
        PENDING = 'pending', _('Pending')
        SENT = 'sent', _('Sent')
        DELIVERED = 'delivered', _('Delivered')
        READ = 'read', _('Read')
        FAILED = 'failed', _('Failed')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'users_app.User', on_delete=models.CASCADE, related_name='notifications'
    )
    notification = models.ForeignKey(
        Notification, on_delete=models.CASCADE, related_name='user_notifications'
    )
    delivery_status = models.CharField(
        max_length=20, choices=DeliveryStatus.choices, default=DeliveryStatus.PENDING,
        db_index=True
    )
    read_at = models.DateTimeField(null=True, blank=True)
    clicked = models.BooleanField(default=False)
    device_token = models.CharField(max_length=255, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_notifications'
        verbose_name = _('user notification')
        verbose_name_plural = _('user notifications')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'delivery_status']),
            models.Index(fields=['delivery_status']),
        ]
    
    def __str__(self):
        return f"Notif for {self.user.email}: {self.notification.title}"


class Subscription(models.Model):
    """User subscription to specific notification triggers."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'users_app.User', on_delete=models.CASCADE, related_name='subscriptions'
    )
    team = models.ForeignKey(
        'teams.Team', on_delete=models.CASCADE, null=True, blank=True,
        related_name='subscriptions'
    )
    match = models.ForeignKey(
        'matches.Match', on_delete=models.CASCADE, null=True, blank=True,
        related_name='subscriptions'
    )
    competition = models.ForeignKey(
        'competitions.Competition', on_delete=models.CASCADE, null=True, blank=True,
        related_name='subscriptions'
    )
    player = models.ForeignKey(
        'players.Player', on_delete=models.CASCADE, null=True, blank=True,
        related_name='subscriptions'
    )
    notification_types = models.JSONField(
        help_text='List of notification types subscribed to'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'subscriptions'
        verbose_name = _('subscription')
        verbose_name_plural = _('subscriptions')
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['match']),
            models.Index(fields=['team']),
        ]
    
    def __str__(self):
        targets = []
        if self.team:
            targets.append(f"team:{self.team.name}")
        if self.match:
            targets.append(f"match:{self.match_id}")
        if self.competition:
            targets.append(f"comp:{self.competition.name}")
        return f"Sub for {self.user.email}: {', '.join(targets)}"