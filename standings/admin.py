"""
Django admin configuration for standings app.
"""
from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Standing, TeamStanding, StandingRule


class TeamStandingInline(admin.TabularInline):
    """Inline team standings within standing admin."""
    
    model = TeamStanding
    extra = 0
    fields = [
        'team', 'position', 'played', 'wins', 'draws', 'losses',
        'goals_for', 'goals_against', 'goal_difference', 'points'
    ]
    raw_id_fields = ['team']
    ordering = ['position']


@admin.register(Standing)
class StandingAdmin(admin.ModelAdmin):
    """Admin view for Standing model."""
    
    list_display = [
        'standing_name', 'competition_season', 'stage',
        'group', 'standing_type', 'is_live', 'last_calculated'
    ]
    list_filter = [
        'standing_type', 'is_live',
        'competition_season__competition'
    ]
    search_fields = [
        'competition_season__name',
        'stage__name', 'group__name'
    ]
    readonly_fields = ['created_at', 'updated_at', 'last_calculated']
    inlines = [TeamStandingInline]
    autocomplete_fields = ['competition_season', 'stage', 'group']
    
    fieldsets = (
        ('Context', {
            'fields': ('competition_season', 'stage', 'group', 'standing_type')
        }),
        ('Status', {
            'fields': ('is_live', 'last_calculated')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def standing_name(self, obj):
        base = f'{obj.competition_season}'
        if obj.group:
            base += f' - {obj.group.name}'
        return f'{base} ({obj.get_standing_type_display()})'
    standing_name.short_description = 'Standing'


@admin.register(TeamStanding)
class TeamStandingAdmin(admin.ModelAdmin):
    """Admin view for TeamStanding model."""
    
    list_display = [
        'position', 'team', 'standing_link', 'played',
        'wins', 'draws', 'losses', 'goals_for', 'goals_against',
        'goal_difference', 'points', 'form_display'
    ]
    list_filter = ['standing__competition_season__competition']
    search_fields = ['team__name', 'standing__competition_season__name']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['standing', 'team']
    
    fieldsets = (
        ('Position', {
            'fields': ('standing', 'team', 'position')
        }),
        ('Overall Record', {
            'fields': (
                'played', 'wins', 'draws', 'losses',
                'goals_for', 'goals_against', 'goal_difference', 'points'
            )
        }),
        ('Home Record', {
            'fields': (
                'home_played', 'home_wins', 'home_draws', 'home_losses',
                'home_goals_for', 'home_goals_against'
            )
        }),
        ('Away Record', {
            'fields': (
                'away_played', 'away_wins', 'away_draws', 'away_losses',
                'away_goals_for', 'away_goals_against'
            )
        }),
        ('Additional', {
            'fields': (
                'form', 'clean_sheets', 'failed_to_score',
                'points_deduction', 'metadata'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def standing_link(self, obj):
        url = reverse('admin:standings_standing_change', args=[obj.standing_id])
        return format_html('<a href="{}">{}</a>', url, obj.standing)
    standing_link.short_description = 'Standing'
    
    def form_display(self, obj):
        if obj.form:
            html = ''
            for char in obj.form:
                colors = {'W': '#22c55e', 'D': '#eab308', 'L': '#ef4444'}
                color = colors.get(char, '#6b7280')
                html += f'<span style="display:inline-block;width:20px;height:20px;border-radius:50%;background:{color};color:white;text-align:center;line-height:20px;font-size:10px;margin:1px;font-weight:bold;">{char}</span>'
            return format_html(html)
        return '-'
    form_display.short_description = 'Form'


@admin.register(StandingRule)
class StandingRuleAdmin(admin.ModelAdmin):
    """Admin view for StandingRule model."""
    
    list_display = [
        'competition', 'rule_type', 'priority',
        'description', 'is_active'
    ]
    list_filter = ['competition', 'rule_type', 'is_active']
    search_fields = ['competition__name', 'description']
    readonly_fields = ['created_at']
    autocomplete_fields = ['competition']
    
    fieldsets = (
        ('Rule Definition', {
            'fields': ('competition', 'rule_type', 'priority', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )