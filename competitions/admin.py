"""
Django admin configuration for competitions app.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Competition, Season, Stage, Group


class SeasonInline(admin.TabularInline):
    """Inline seasons within competition admin."""
    
    model = Season
    extra = 0
    fields = ['name', 'start_date', 'end_date', 'status', 'is_current', 'total_teams']
    show_change_link = True


class StageInline(admin.TabularInline):
    """Inline stages within season admin."""
    
    model = Stage
    extra = 0
    fields = ['name', 'stage_type', 'order', 'start_date', 'end_date', 'is_active']
    show_change_link = True


class GroupInline(admin.TabularInline):
    """Inline groups within stage admin."""
    
    model = Group
    extra = 0
    fields = ['name', 'label', 'sort_order']


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    """Admin view for Competition model."""
    
    list_display = [
        'name', 'short_name', 'competition_type', 'tier',
        'country', 'is_active', 'logo_preview', 'created_at'
    ]
    list_filter = [
        'competition_type', 'tier', 'country', 'is_active'
    ]
    search_fields = ['name', 'short_name', 'country', 'external_api_id']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    inlines = [SeasonInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': (
                'name', 'short_name', 'slug', 'competition_type',
                'tier', 'country', 'country_flag'
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


@admin.register(Season)
class SeasonAdmin(admin.ModelAdmin):
    """Admin view for Season model."""
    
    list_display = [
        'name', 'competition', 'start_date', 'end_date',
        'status', 'is_current', 'total_teams', 'total_matches'
    ]
    list_filter = ['status', 'is_current', 'competition']
    search_fields = ['name', 'competition__name', 'external_api_id']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    inlines = [StageInline]
    autocomplete_fields = ['competition', 'winner_team']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('competition', 'name', 'slug', 'status', 'is_current')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('Statistics', {
            'fields': ('winner_team', 'total_teams', 'total_matches')
        }),
        ('External', {
            'fields': ('external_api_id', 'metadata')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    """Admin view for Stage model."""
    
    list_display = [
        'name', 'season', 'stage_type', 'order',
        'start_date', 'end_date', 'is_active'
    ]
    list_filter = ['stage_type', 'is_active', 'season__competition']
    search_fields = ['name', 'season__name', 'season__competition__name']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [GroupInline]
    autocomplete_fields = ['season']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('season', 'name', 'stage_type', 'order', 'is_active')
        }),
        ('Dates', {
            'fields': ('start_date', 'end_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Admin view for Group model."""
    
    list_display = ['name', 'label', 'stage', 'sort_order', 'teams_count']
    list_filter = ['stage__season__competition', 'stage']
    search_fields = ['name', 'label', 'stage__name']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['stage']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('stage', 'name', 'label', 'sort_order')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def teams_count(self, obj):
        return obj.teams.count()
    teams_count.short_description = 'Teams'