"""
Django admin configuration for notifications app.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Notification, UserNotification, Subscription


class UserNotificationInline(admin.TabularInline):
    """Inline user notifications within notification admin."""
    
    model = UserNotification
    extra = 0
    fields = ['user', 'delivery_status', 'read_at']
    readonly_fields = ['delivery_status', 'read_at']
    can_delete = False


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin view for Notification model."""
    
    list_display = [
        'title', 'notification_type', 'is_system',
        'created_at', 'delivery_count'
    ]
    list_filter = ['notification_type', 'is_system']
    search_fields = ['title', 'body']
    readonly_fields = ['created_at']
    inlines = [UserNotificationInline]
    
    fieldsets = (
        ('Notification Content', {
            'fields': ('notification_type', 'title', 'body')
        }),
        ('Data', {
            'fields': ('data_payload',)
        }),
        ('System', {
            'fields': ('is_system',)
        }),
    )
    
    def delivery_count(self, obj):
        return obj.user_notifications.count()
    delivery_count.short_description = 'Delivered To'


@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    """Admin view for UserNotification model."""
    
    list_display = [
        'user', 'notification_link', 'delivery_status_badge',
        'read_at', 'created_at'
    ]
    list_filter = ['delivery_status', 'clicked']
    search_fields = [
        'user__email', 'notification__title',
        'notification__body'
    ]
    readonly_fields = ['created_at', 'delivered_at']
    autocomplete_fields = ['user', 'notification']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Notification', {
            'fields': ('user', 'notification', 'delivery_status')
        }),
        ('Delivery Info', {
            'fields': ('device_token', 'delivered_at', 'read_at', 'clicked')
        }),
    )
    
    def notification_link(self, obj):
        from django.urls import reverse
        url = reverse('admin:notifications_notification_change', args=[obj.notification_id])
        return format_html('<a href="{}">{}</a>', url, obj.notification.title[:50])
    notification_link.short_description = 'Notification'
    
    def delivery_status_badge(self, obj):
        colors = {
            'pending': '#f59e0b',
            'sent': '#3b82f6',
            'delivered': '#10b981',
            'read': '#6366f1',
            'failed': '#ef4444',
        }
        color = colors.get(obj.delivery_status, '#6b7280')
        return format_html(
            '<span style="background:{};color:white;padding:2px 8px;border-radius:12px;font-size:12px;">{}</span>',
            color, obj.get_delivery_status_display()
        )
    delivery_status_badge.short_description = 'Status'
    
    actions = ['mark_as_read']
    
    @admin.action(description='Mark selected as read')
    def mark_as_read(self, request, queryset):
        from django.utils import timezone
        queryset.update(delivery_status='read', read_at=timezone.now())


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Admin view for Subscription model."""
    
    list_display = [
        'user', 'subscription_target', 'notification_types_list',
        'is_active', 'created_at'
    ]
    list_filter = ['is_active']
    search_fields = [
        'user__email', 'team__name', 'competition__name',
        'player__full_name'
    ]
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['user', 'team', 'match', 'competition', 'player']
    
    fieldsets = (
        ('Subscription', {
            'fields': ('user', 'is_active')
        }),
        ('Target', {
            'fields': ('team', 'match', 'competition', 'player'),
            'description': 'Select at least one target for the subscription'
        }),
        ('Notification Types', {
            'fields': ('notification_types',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def subscription_target(self, obj):
        targets = []
        if obj.team:
            targets.append(f'Team: {obj.team.name}')
        if obj.match:
            targets.append(f'Match: {obj.match}')
        if obj.competition:
            targets.append(f'Comp: {obj.competition.name}')
        if obj.player:
            targets.append(f'Player: {obj.player.full_name}')
        return ' | '.join(targets) if targets else 'No target'
    subscription_target.short_description = 'Target'
    
    def notification_types_list(self, obj):
        if obj.notification_types:
            return ', '.join(obj.notification_types)
        return 'All'
    notification_types_list.short_description = 'Types'