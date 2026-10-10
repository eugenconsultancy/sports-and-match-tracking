"""
Django admin configuration for players app.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Player, PlayerStats, PlayerMatchStats, TransferHistory


class PlayerStatsInline(admin.TabularInline):
    """Inline stats within player admin."""
    
    model = PlayerStats
    extra = 0
    fields = ['season', 'team', 'appearances', 'goals', 'assists', 'average_rating']
    raw_id_fields = ['season', 'team']
    show_change_link = True


class TransferHistoryInline(admin.TabularInline):
    """Inline transfers within player admin."""
    
    model = TransferHistory
    extra = 0
    fields = ['from_team', 'to_team', 'transfer_date', 'transfer_fee', 'is_loan']
    raw_id_fields = ['from_team', 'to_team']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    """Admin view for Player model."""
    
    list_display = [
        'full_name', 'nationality', 'position', 'preferred_foot',
        'current_team', 'jersey_number', 'market_value_display',
        'is_active', 'image_preview'
    ]
    list_filter = [
        'position', 'nationality', 'preferred_foot',
        'current_team__country', 'is_active'
    ]
    search_fields = [
        'first_name', 'last_name', 'full_name',
        'nationality', 'external_api_id'
    ]
    prepopulated_fields = {'slug': ('full_name',)}
    readonly_fields = ['created_at', 'updated_at']
    inlines = [PlayerStatsInline, TransferHistoryInline]
    autocomplete_fields = ['current_team']
    
    fieldsets = (
        ('Personal Information', {
            'fields': (
                'first_name', 'last_name', 'full_name', 'slug',
                'date_of_birth', 'nationality', 'image_url'
            )
        }),
        ('Professional Details', {
            'fields': (
                'position', 'preferred_foot', 'height_cm', 'weight_kg',
                'jersey_number', 'current_team'
            )
        }),
        ('Market Value', {
            'fields': ('market_value', 'market_value_currency')
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
    
    def market_value_display(self, obj):
        if obj.market_value:
            return f'{obj.market_value_currency} {obj.market_value:,.0f}'
        return '-'
    market_value_display.short_description = 'Market Value'
    market_value_display.admin_order_field = 'market_value'
    
    def image_preview(self, obj):
        if obj.image_url:
            return format_html(
                '<img src="{}" style="max-height: 30px; border-radius: 50%;" />',
                obj.image_url
            )
        return '-'
    image_preview.short_description = 'Photo'


@admin.register(PlayerStats)
class PlayerStatsAdmin(admin.ModelAdmin):
    """Admin view for PlayerStats model."""
    
    list_display = [
        'player', 'season', 'team', 'appearances', 'goals',
        'assists', 'yellow_cards', 'red_cards', 'average_rating'
    ]
    list_filter = ['season__competition', 'season']
    search_fields = ['player__full_name', 'team__name', 'season__name']
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['player', 'season', 'team']
    
    fieldsets = (
        ('References', {
            'fields': ('player', 'season', 'team')
        }),
        ('Appearances', {
            'fields': ('appearances', 'minutes_played')
        }),
        ('Offensive', {
            'fields': ('goals', 'assists', 'shots_total', 'shots_on_target')
        }),
        ('Discipline', {
            'fields': ('yellow_cards', 'red_cards')
        }),
        ('Performance', {
            'fields': (
                'pass_accuracy', 'duels_won', 'dribbles_successful',
                'average_rating'
            )
        }),
        ('Additional', {
            'fields': ('metadata',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(PlayerMatchStats)
class PlayerMatchStatsAdmin(admin.ModelAdmin):
    """Admin view for PlayerMatchStats model."""
    
    list_display = [
        'player', 'match_link', 'team', 'goals', 'assists',
        'minutes_played', 'rating', 'is_mvp'
    ]
    list_filter = ['is_mvp', 'yellow_card', 'red_card']
    search_fields = [
        'player__full_name', 'team__name',
        'match__home_team__name', 'match__away_team__name'
    ]
    readonly_fields = ['created_at', 'updated_at']
    autocomplete_fields = ['player', 'match', 'team']
    
    fieldsets = (
        ('References', {
            'fields': ('player', 'match', 'team')
        }),
        ('Performance', {
            'fields': (
                'goals', 'assists', 'minutes_played', 'rating', 'is_mvp'
            )
        }),
        ('Discipline', {
            'fields': ('yellow_card', 'red_card')
        }),
        ('Detailed Stats', {
            'fields': (
                'shots_on_target', 'shots_off_target',
                'passes_completed', 'passes_total',
                'tackles', 'interceptions',
                'fouls_committed', 'fouls_drawn'
            )
        }),
        ('Additional', {
            'fields': ('metadata',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def match_link(self, obj):
        from django.urls import reverse
        url = reverse('admin:matches_match_change', args=[obj.match_id])
        return format_html(
            '<a href="{}">{} vs {}</a>',
            url, obj.match.home_team, obj.match.away_team
        )
    match_link.short_description = 'Match'


@admin.register(TransferHistory)
class TransferHistoryAdmin(admin.ModelAdmin):
    """Admin view for TransferHistory model."""
    
    list_display = [
        'player', 'from_team', 'to_team', 'transfer_date',
        'transfer_fee_display', 'is_loan', 'contract_until'
    ]
    list_filter = ['is_loan', 'transfer_date', 'to_team__country']
    search_fields = [
        'player__full_name', 'from_team__name',
        'to_team__name', 'additional_info'
    ]
    date_hierarchy = 'transfer_date'
    readonly_fields = ['created_at']
    autocomplete_fields = ['player', 'from_team', 'to_team']
    
    fieldsets = (
        ('Transfer Details', {
            'fields': (
                'player', 'from_team', 'to_team',
                'transfer_date', 'is_loan'
            )
        }),
        ('Financial', {
            'fields': ('transfer_fee', 'transfer_fee_currency')
        }),
        ('Contract', {
            'fields': ('contract_until', 'additional_info')
        }),
    )
    
    def transfer_fee_display(self, obj):
        if obj.transfer_fee:
            return f'{obj.transfer_fee_currency} {obj.transfer_fee:,.0f}'
        return 'Free / Unknown'
    transfer_fee_display.short_description = 'Fee'
    transfer_fee_display.admin_order_field = 'transfer_fee'