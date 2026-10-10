"""
Serializers for players app.
"""
from rest_framework import serializers
from .models import Player, PlayerStats, PlayerMatchStats, TransferHistory


class PlayerListSerializer(serializers.ModelSerializer):
    """Compact player serializer for lists."""
    
    current_team_name = serializers.CharField(source='current_team.name', read_only=True)
    current_team_logo = serializers.CharField(source='current_team.logo_url', read_only=True)
    
    class Meta:
        model = Player
        fields = [
            'id', 'full_name', 'slug', 'nationality', 'position',
            'preferred_foot', 'jersey_number', 'image_url',
            'market_value', 'market_value_currency',
            'current_team', 'current_team_name', 'current_team_logo'
        ]


class PlayerDetailSerializer(serializers.ModelSerializer):
    """Detailed player serializer."""
    
    current_team_name = serializers.CharField(source='current_team.name', read_only=True)
    current_team_logo = serializers.CharField(source='current_team.logo_url', read_only=True)
    season_stats = serializers.SerializerMethodField()
    recent_transfers = serializers.SerializerMethodField()
    
    class Meta:
        model = Player
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'slug',
            'date_of_birth', 'nationality', 'position', 'preferred_foot',
            'height_cm', 'weight_kg', 'jersey_number',
            'current_team', 'current_team_name', 'current_team_logo',
            'image_url', 'market_value', 'market_value_currency',
            'external_api_id', 'external_api_source', 'metadata',
            'is_active', 'created_at', 'season_stats', 'recent_transfers'
        ]
    
    def get_season_stats(self, obj):
        stats = obj.season_stats.select_related('season', 'team').all()[:5]
        return PlayerStatsSerializer(stats, many=True).data
    
    def get_recent_transfers(self, obj):
        transfers = obj.transfers.select_related('from_team', 'to_team').order_by('-transfer_date')[:5]
        return TransferHistorySerializer(transfers, many=True).data


class PlayerStatsSerializer(serializers.ModelSerializer):
    """Player season stats serializer."""
    
    season_name = serializers.CharField(source='season.name', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)
    
    class Meta:
        model = PlayerStats
        fields = [
            'id', 'player', 'season', 'season_name', 'team', 'team_name',
            'appearances', 'minutes_played', 'goals', 'assists',
            'yellow_cards', 'red_cards', 'shots_total', 'shots_on_target',
            'pass_accuracy', 'duels_won', 'dribbles_successful',
            'average_rating'
        ]


class PlayerMatchStatsSerializer(serializers.ModelSerializer):
    """Player match performance serializer."""
    
    player_name = serializers.CharField(source='player.full_name', read_only=True)
    match_info = serializers.SerializerMethodField()
    
    class Meta:
        model = PlayerMatchStats
        fields = [
            'id', 'player', 'player_name', 'match', 'match_info',
            'team', 'goals', 'assists', 'minutes_played',
            'yellow_card', 'red_card', 'shots_on_target', 'shots_off_target',
            'passes_completed', 'passes_total', 'tackles',
            'interceptions', 'fouls_committed', 'fouls_drawn',
            'rating', 'is_mvp'
        ]
    
    def get_match_info(self, obj):
        return {
            'home_team': obj.match.home_team.name if obj.match.home_team else None,
            'away_team': obj.match.away_team.name if obj.match.away_team else None,
            'kickoff_time': obj.match.kickoff_time,
            'status': obj.match.status,
        }


class TransferHistorySerializer(serializers.ModelSerializer):
    """Player transfer history serializer."""
    
    player_name = serializers.CharField(source='player.full_name', read_only=True)
    from_team_name = serializers.CharField(source='from_team.name', read_only=True, allow_null=True)
    to_team_name = serializers.CharField(source='to_team.name', read_only=True)
    
    class Meta:
        model = TransferHistory
        fields = [
            'id', 'player', 'player_name', 'from_team', 'from_team_name',
            'to_team', 'to_team_name', 'transfer_date', 'transfer_fee',
            'transfer_fee_currency', 'contract_until', 'is_loan',
            'additional_info'
        ]