"""
Django admin configuration for teams app.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Team, Venue, Coach, TeamSeason


class CoachInline(admin.TabularInline):
    """Inline coaches within team admin."""
    
    model = Coach
    fk_name = 'current_team'
    extra = 0
    fields = ['name', 'nationality', 'contract_start', 'contract_end']
    show_change_link = True


class TeamSeasonInline(admin.TabularInline):
    """Inline season participations within team admin."""
    
    model = TeamSeason
    extra = 0
    fields = ['season', 'coach', 'squad_size', 'average_age']
    raw_id_fields = ['season', 'coach']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin view for Team model."""
    
    list_display = [
        'name', 'short_name', 'team_type', 'country',
        'founded_year', 'is_active', 'logo_preview', 'players_count'
    ]
    list_filter = ['team_type', 'country', 'is_active']
    search_fields = ['name', 'short_name', 'country', 'external_api_id']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    inlines = [CoachInline, TeamSeasonInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name', 'short_name', 'slug', 'team_type',
                'country', 'founded_year'
            )
        }),
        ('Branding', {
            'fields': ('logo_url', 'primary_color', 'secondary_color')
        }),
        ('Status & External', {
            'fields': (
                'is_active', 'external_api_id', 'external_api_source',
                'metadata'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def logo_preview(self, obj):
        if obj.logo_url:
            return format_html(
                '<img src="{}" style="max-height: 30px;" />',
                obj.logo_url
            )
        return '-'
    logo_preview.short_description = 'Logo'
    
    def players_count(self, obj):
        return obj.current_players.count()
    players_count.short_description = 'Players'


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    """Admin view for Venue model."""
    
    list_display = [
        'name', 'city', 'country', 'capacity',
        'latitude', 'longitude', 'image_preview'
    ]
    list_filter = ['country', 'city']
    search_fields = ['name', 'city', 'country']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'city', 'country', 'capacity')
        }),
        ('Location', {
            'fields': ('latitude', 'longitude')
        }),
        ('Media', {
            'fields': ('image_url',)
        }),
        ('External', {
            'fields': ('external_api_id',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" style="max-height: 30px;" />',
                obj.image_url
            )
        return '-'
    image_preview.short_description = 'Image'


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    """Admin view for Coach model."""
    
    list_display = [
        'name', 'nationality', 'current_team', 'date_of_birth',
        'contract_start', 'contract_end'
    ]
    list_filter = ['nationality', 'current_team__country']
    search_fields = ['name', 'nationality', 'current_team__name']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['current_team']
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'nationality', 'date_of_birth', 'image_url')
        }),
        ('Current Team', {
            'fields': ('current_team', 'contract_start', 'contract_end')
        }),
        ('External', {
            'fields': ('external_api_id',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(TeamSeason)
class TeamSeasonAdmin(admin.ModelAdmin):
    """Admin view for TeamSeason model."""
    
    list_display = [
        'team', 'season', 'coach', 'squad_size',
        'average_age', 'foreign_players_count'
    ]
    list_filter = ['season__competition', 'season']
    search_fields = ['team__name', 'season__name', 'coach__name']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['team', 'season', 'coach']
    
    fieldsets = (
        ('Participation', {
            'fields': ('team', 'season', 'coach')
        }),
        ('Squad Info', {
            'fields': ('squad_size', 'average_age', 'foreign_players_count')
        }),
        ('Additional', {
            'fields': ('metadata',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )