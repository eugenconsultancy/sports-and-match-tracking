"""
Django admin configuration for polls app.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Poll, PollOption, Vote, PollResultCache


class PollOptionInline(admin.TabularInline):
    """Inline options within poll admin."""
    
    model = PollOption
    extra = 1
    fields = ['label', 'team', 'option_type', 'sort_order', 'vote_count', 'percentage']
    raw_id_fields = ['team']


class PollResultCacheInline(admin.StackedInline):
    """Inline result cache within poll admin."""
    
    model = PollResultCache
    extra = 0
    readonly_fields = ['total_votes', 'last_calculated']
    fields = ['results_json', 'total_votes', 'last_calculated']
    can_delete = False
    max_num = 1


@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):
    """Admin view for Poll model."""
    
    list_display = [
        'question', 'match_link', 'status', 'total_votes',
        'start_time', 'end_time', 'is_featured'
    ]
    list_filter = ['status', 'is_featured']
    search_fields = ['question', 'match__home_team__name', 'match__away_team__name']
    readonly_fields = ['total_votes', 'created_at', 'updated_at']
    inlines = [PollOptionInline, PollResultCacheInline]
    autocomplete_fields = ['match', 'created_by']
    
    fieldsets = (
        ('Poll Details', {
            'fields': ('match', 'question', 'status', 'is_featured')
        }),
        ('Timing', {
            'fields': ('start_time', 'end_time')
        }),
        ('Statistics', {
            'fields': ('total_votes',)
        }),
        ('Creator', {
            'fields': ('created_by',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def match_link(self, obj):
        url = reverse('admin:matches_match_change', args=[obj.match_id])
        return format_html('<a href="{}">{}</a>', url, obj.match)
    match_link.short_description = 'Match'


@admin.register(PollOption)
class PollOptionAdmin(admin.ModelAdmin):
    """Admin view for PollOption model."""
    
    list_display = ['label', 'poll_link', 'option_type', 'team', 'vote_count', 'percentage']
    list_filter = ['option_type']
    search_fields = ['label', 'team__name', 'poll__question']
    readonly_fields = ['vote_count', 'percentage', 'created_at']
    autocomplete_fields = ['poll', 'team']
    
    fieldsets = (
        ('Option Details', {
            'fields': ('poll', 'label', 'team', 'option_type', 'sort_order')
        }),
        ('Statistics', {
            'fields': ('vote_count', 'percentage')
        }),
    )
    
    def poll_link(self, obj):
        url = reverse('admin:polls_poll_change', args=[obj.poll_id])
        return format_html('<a href="{}">{}</a>', url, obj.poll)
    poll_link.short_description = 'Poll'


@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    """Admin view for Vote model."""
    
    list_display = ['user', 'poll_link', 'option_link', 'ip_address', 'voted_at']
    list_filter = ['voted_at']
    search_fields = [
        'user__email', 'poll__question',
        'option__label', 'ip_address'
    ]
    readonly_fields = ['voted_at']
    autocomplete_fields = ['poll', 'option', 'user']
    date_hierarchy = 'voted_at'
    
    fieldsets = (
        ('Vote Details', {
            'fields': ('poll', 'option', 'user')
        }),
        ('Client Info', {
            'fields': ('ip_address', 'user_agent')
        }),
    )
    
    def poll_link(self, obj):
        url = reverse('admin:polls_poll_change', args=[obj.poll_id])
        return format_html('<a href="{}">View Poll</a>', url)
    poll_link.short_description = 'Poll'
    
    def option_link(self, obj):
        url = reverse('admin:polls_polloption_change', args=[obj.option_id])
        return format_html('<a href="{}">{}</a>', url, obj.option.label)
    option_link.short_description = 'Option'


@admin.register(PollResultCache)
class PollResultCacheAdmin(admin.ModelAdmin):
    """Admin view for PollResultCache model."""
    
    list_display = ['poll_link', 'total_votes', 'last_calculated']
    readonly_fields = ['total_votes', 'last_calculated']
    autocomplete_fields = ['poll']
    
    fieldsets = (
        ('Cache Data', {
            'fields': ('poll', 'results_json', 'total_votes', 'last_calculated')
        }),
    )
    
    def poll_link(self, obj):
        url = reverse('admin:polls_poll_change', args=[obj.poll_id])
        return format_html('<a href="{}">View Poll</a>', url)
    poll_link.short_description = 'Poll'