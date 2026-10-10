"""
Django admin configuration for matches app.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Match, MatchEvent, Lineup, MatchStats, MatchLiveState


class MatchEventInline(admin.TabularInline):
    """Inline events within match admin."""
    
    model = MatchEvent
    extra = 0
    fields = [
        'event_type', 'minute', 'player', 'team',
        'score_home', 'score_away', 'description'
    ]
    raw_id_fields = ['player', 'related_player', 'team']


class MatchStatsInline(admin.TabularInline):
    """Inline stats within match admin."""
    
    model = MatchStats
    extra = 0
    fields = [
        'team', 'possession_percentage', 'shots_total',
        'shots_on_target', 'expected_goals_xg'
    ]
    raw_id_fields = ['team']


class LineupInline(admin.TabularInline):
    """Inline lineup within match admin."""
    
    model = Lineup
    extra = 0
    fields = [
        'team', 'player', 'role', 'position', 'jersey_number', 'is_captain'
    ]
    raw_id_fields = ['player', 'team']


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    """Admin view for Match model."""
    
    list_display = [
        'match_display', 'competition_season', 'kickoff_time',
        'status', 'score', 'minute', 'venue', 'is_featured'
    ]
    list_filter = [
        'status', 'is_featured', 'competition_season__competition',
        'competition_season', 'stage'
    ]
    search_fields = [
        'home_team__name', 'away_team__name',
        'referee_name', 'external_api_id'
    ]
    date_hierarchy = 'kickoff_time'
    readonly_fields = ['created_at', 'updated_at']
    inlines = [MatchEventInline, MatchStatsInline, LineupInline]
    autocomplete_fields = [
        'home_team', 'away_team', 'competition_season',
        'stage', 'group', 'venue'
    ]
    
    fieldsets = (
        ('Teams', {
            'fields': ('home_team', 'away_team')
        }),
        ('Competition Details', {
            'fields': ('competition_season', 'stage', 'group', 'round_number', 'matchday')
        }),
        ('Schedule', {
            'fields': ('kickoff_time', 'venue')
        }),
        ('Score & Status', {
            'fields': (
                'status', 'home_score', 'away_score',
                'home_score_halftime', 'away_score_halftime',
                'minute', 'injury_time'
            )
        }),
        ('Additional Info', {
            'fields': (
                'attendance', 'referee_name', 'is_featured',
                'external_api_id', 'metadata'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def match_display(self, obj):
        return f'{obj.home_team} vs {obj.away_team}'
    match_display.short_description = 'Match'
    match_display.admin_order_field = 'kickoff_time'
    
    def score(self, obj):
        if obj.status == 'scheduled' and obj.home_score == 0 and obj.away_score == 0:
            return 'vs'
        return f'{obj.home_score} - {obj.away_score}'
    score.short_description = 'Score'


@admin.register(MatchEvent)
class MatchEventAdmin(admin.ModelAdmin):
    """Admin view for MatchEvent model."""
    
    list_display = [
        'match_link', 'event_type', 'minute_display',
        'player', 'team', 'score_display'
    ]
    list_filter = ['event_type', 'team']
    search_fields = [
        'player__full_name', 'related_player__full_name',
        'team__name', 'description'
    ]
    readonly_fields = ['created_at']
    autocomplete_fields = ['match', 'player', 'related_player', 'team']
    
    fieldsets = (
        ('Event Details', {
            'fields': (
                'match', 'event_type', 'minute', 'injury_minute',
                'player', 'related_player', 'team'
            )
        }),
        ('Score at Event', {
            'fields': ('score_home', 'score_away')
        }),
        ('Description', {
            'fields': ('description', 'metadata')
        }),
    )
    
    def match_link(self, obj):
        url = reverse('admin:matches_match_change', args=[obj.match_id])
        return format_html(
            '<a href="{}">{}</a>',
            url, obj.match
        )
    match_link.short_description = 'Match'
    
    def minute_display(self, obj):
        if obj.injury_minute:
            return f"{obj.minute}'+{obj.injury_minute}'"
        return f"{obj.minute}'"
    minute_display.short_description = 'Minute'
    
    def score_display(self, obj):
        if obj.score_home is not None:
            return f'{obj.score_home} - {obj.score_away}'
        return '-'
    score_display.short_description = 'Score'


@admin.register(Lineup)
class LineupAdmin(admin.ModelAdmin):
    """Admin view for Lineup model."""
    
    list_display = [
        'player', 'team', 'role', 'position',
        'jersey_number', 'is_captain', 'match_link'
    ]
    list_filter = ['role', 'is_captain', 'position', 'team']
    search_fields = ['player__full_name', 'team__name']
    readonly_fields = ['created_at']
    autocomplete_fields = ['match', 'player', 'team']
    
    fieldsets = (
        ('Lineup Entry', {
            'fields': (
                'match', 'team', 'player', 'role',
                'position', 'jersey_number', 'is_captain',
                'sort_order'
            )
        }),
        ('Additional', {
            'fields': ('metadata',)
        }),
    )
    
    def match_link(self, obj):
        url = reverse('admin:matches_match_change', args=[obj.match_id])
        return format_html('<a href="{}">View Match</a>', url)
    match_link.short_description = 'Match'


@admin.register(MatchStats)
class MatchStatsAdmin(admin.ModelAdmin):
    """Admin view for MatchStats model."""
    
    list_display = [
        'match_link', 'team', 'possession_percentage',
        'shots_total', 'shots_on_target', 'expected_goals_xg'
    ]
    list_filter = ['team']
    search_fields = ['team__name']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['match', 'team']
    
    fieldsets = (
        ('References', {
            'fields': ('match', 'team')
        }),
        ('Possession & Shots', {
            'fields': (
                'possession_percentage', 'shots_total',
                'shots_on_target', 'shots_off_target',
                'blocked_shots', 'expected_goals_xg'
            )
        }),
        ('Passing', {
            'fields': (
                'passes_total', 'passes_accurate', 'pass_accuracy',
                'crosses_total', 'crosses_accurate'
            )
        }),
        ('Defensive', {
            'fields': (
                'tackles_total', 'tackles_accurate',
                'interceptions', 'clearances',
                'goalkeeper_saves'
            )
        }),
        ('Discipline', {
            'fields': ('fouls', 'yellow_cards', 'red_cards', 'offsides', 'corner_kicks')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def match_link(self, obj):
        url = reverse('admin:matches_match_change', args=[obj.match_id])
        return format_html('<a href="{}">View Match</a>', url)
    match_link.short_description = 'Match'


@admin.register(MatchLiveState)
class MatchLiveStateAdmin(admin.ModelAdmin):
    """Admin view for MatchLiveState model."""
    
    list_display = [
        'match_link', 'current_minute', 'home_score',
        'away_score', 'momentum', 'match_status', 'updated_at'
    ]
    list_filter = ['momentum', 'match_status']
    readonly_fields = ['updated_at']
    autocomplete_fields = ['match']
    
    fieldsets = (
        ('Match Reference', {
            'fields': ('match', 'match_status')
        }),
        ('Current State', {
            'fields': (
                'current_minute', 'injury_minute',
                'home_score', 'away_score', 'momentum'
            )
        }),
        ('Possession', {
            'fields': ('possession',)
        }),
        ('Attacks', {
            'fields': ('attacks', 'dangerous_attacks')
        }),
        ('Recent Events', {
            'fields': ('last_events',)
        }),
        ('Timestamp', {
            'fields': ('updated_at',)
        }),
    )
    
    def match_link(self, obj):
        url = reverse('admin:matches_match_change', args=[obj.match_id])
        return format_html('<a href="{}">View Match</a>', url)
    match_link.short_description = 'Match'