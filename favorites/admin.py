"""
Django admin configuration for favorites app.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import UserFavoriteTeam, UserFavoriteMatch, UserFavoriteCompetition


@admin.register(UserFavoriteTeam)
class UserFavoriteTeamAdmin(admin.ModelAdmin):
    """Admin view for UserFavoriteTeam model."""
    
    list_display = ['user', 'team_link', 'priority', 'notify_matches', 'notify_goals', 'created_at']
    list_filter = ['notify_matches', 'notify_goals', 'notify_transfers', 'team__country']
    search_fields = ['user__email', 'team__name']
    readonly_fields = ['created_at']
    autocomplete_fields = ['user', 'team']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Favorite', {
            'fields': ('user', 'team', 'priority')
        }),
        ('Notifications', {
            'fields': ('notify_matches', 'notify_goals', 'notify_transfers')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
    
    def team_link(self, obj):
        url = reverse('admin:teams_team_change', args=[obj.team_id])
        return format_html('<a href="{}">{}</a>', url, obj.team.name)
    team_link.short_description = 'Team'


@admin.register(UserFavoriteMatch)
class UserFavoriteMatchAdmin(admin.ModelAdmin):
    """Admin view for UserFavoriteMatch model."""
    
    list_display = [
        'user', 'match_link', 'notify_goals',
        'notify_half_time', 'notify_full_time', 'created_at'
    ]
    list_filter = ['notify_goals', 'notify_half_time', 'notify_full_time']
    search_fields = [
        'user__email', 'match__home_team__name', 'match__away_team__name'
    ]
    readonly_fields = ['created_at']
    autocomplete_fields = ['user', 'match']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Favorite', {
            'fields': ('user', 'match')
        }),
        ('Notifications', {
            'fields': ('notify_goals', 'notify_half_time', 'notify_full_time')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
    
    def match_link(self, obj):
        url = reverse('admin:matches_match_change', args=[obj.match_id])
        return format_html('<a href="{}">{}</a>', url, obj.match)
    match_link.short_description = 'Match'


@admin.register(UserFavoriteCompetition)
class UserFavoriteCompetitionAdmin(admin.ModelAdmin):
    """Admin view for UserFavoriteCompetition model."""
    
    list_display = ['user', 'competition_link', 'priority', 'created_at']
    search_fields = ['user__email', 'competition__name']
    readonly_fields = ['created_at']
    autocomplete_fields = ['user', 'competition']
    
    fieldsets = (
        ('Favorite', {
            'fields': ('user', 'competition', 'priority')
        }),
        ('Timestamp', {
            'fields': ('created_at',)
        }),
    )
    
    def competition_link(self, obj):
        url = reverse('admin:competitions_competition_change', args=[obj.competition_id])
        return format_html('<a href="{}">{}</a>', url, obj.competition.name)
    competition_link.short_description = 'Competition'