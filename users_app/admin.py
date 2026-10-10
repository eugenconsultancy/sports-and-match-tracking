"""
Django admin configuration for users app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import User, UserProfile, UserPreference, SessionDevice


class UserProfileInline(admin.StackedInline):
    """Inline profile within user admin."""
    
    model = UserProfile
    extra = 0
    can_delete = False
    fields = ['avatar', 'bio', 'language', 'timezone', 'country', 'favorite_sport']


class UserPreferenceInline(admin.StackedInline):
    """Inline preferences within user admin."""
    
    model = UserPreference
    extra = 0
    can_delete = False
    fields = [
        'notification_match_start', 'notification_goal',
        'notification_red_card', 'notification_half_time',
        'notification_full_time', 'notification_news',
        'email_notifications', 'push_notifications', 'odds_format'
    ]


class SessionDeviceInline(admin.TabularInline):
    """Inline devices within user admin."""
    
    model = SessionDevice
    extra = 0
    fields = ['device_token', 'platform', 'is_active', 'last_used']
    readonly_fields = ['device_token', 'platform', 'last_used']
    can_delete = True


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin view for custom User model."""
    
    list_display = [
        'email', 'first_name', 'last_name', 'is_active',
        'is_verified', 'is_staff', 'date_joined', 'favorites_count'
    ]
    list_filter = ['is_active', 'is_verified', 'is_staff', 'is_superuser']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    readonly_fields = ['created_at', 'updated_at', 'date_joined', 'last_login']
    inlines = [UserProfileInline, UserPreferenceInline, SessionDeviceInline]
    
    fieldsets = (
        (_('Login Credentials'), {
            'fields': ('email', 'password')
        }),
        (_('Personal Information'), {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'phone_number')
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_verified', 'is_staff',
                'is_superuser', 'groups', 'user_permissions'
            )
        }),
        (_('Important Dates'), {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name'),
        }),
    )
    
    def favorites_count(self, obj):
        teams = obj.favorite_teams.count()
        matches = obj.favorite_matches.count()
        competitions = obj.favorite_competitions.count()
        return f'{teams} teams / {matches} matches / {competitions} comps'
    favorites_count.short_description = 'Favorites'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin view for UserProfile model."""
    
    list_display = ['user', 'language', 'timezone', 'country', 'avatar_preview']
    list_filter = ['language', 'timezone', 'country']
    search_fields = ['user__email', 'country', 'bio']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['user']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Profile Details', {
            'fields': ('avatar', 'bio', 'language', 'timezone', 'country', 'favorite_sport')
        }),
        ('Social', {
            'fields': ('social_links',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def avatar_preview(self, obj):
        if obj.avatar:
            return format_html(
                '<img src="{}" style="max-height: 30px; border-radius: 50%;" />',
                obj.avatar.url
            )
        return '-'
    avatar_preview.short_description = 'Avatar'


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    """Admin view for UserPreference model."""
    
    list_display = [
        'user', 'email_notifications', 'push_notifications',
        'odds_format'
    ]
    list_filter = [
        'email_notifications', 'push_notifications',
        'notification_match_start', 'notification_goal'
    ]
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['user']
    
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Match Notifications', {
            'fields': (
                'notification_match_start', 'notification_goal',
                'notification_red_card', 'notification_half_time',
                'notification_full_time'
            )
        }),
        ('Other Notifications', {
            'fields': ('notification_news',)
        }),
        ('Channels', {
            'fields': ('email_notifications', 'push_notifications')
        }),
        ('Display', {
            'fields': ('odds_format',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SessionDevice)
class SessionDeviceAdmin(admin.ModelAdmin):
    """Admin view for SessionDevice model."""
    
    list_display = ['user', 'platform', 'is_active', 'last_used', 'created_at']
    list_filter = ['platform', 'is_active']
    search_fields = ['user__email', 'device_token', 'user_agent']
    readonly_fields = ['created_at']
    autocomplete_fields = ['user']
    
    fieldsets = (
        ('Device', {
            'fields': ('user', 'device_token', 'platform', 'user_agent')
        }),
        ('Status', {
            'fields': ('is_active', 'last_used')
        }),
    )