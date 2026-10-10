"""
Serializers for teams app.
"""
from rest_framework import serializers
from .models import Team, Venue, Coach, TeamSeason


class VenueSerializer(serializers.ModelSerializer):
    """Venue/stadium serializer."""
    
    class Meta:
        model = Venue
        fields = [
            'id', 'name', 'slug', 'city', 'country', 'capacity',
            'latitude', 'longitude', 'image_url'
        ]


class CoachSerializer(serializers.ModelSerializer):
    """Coach serializer."""
    
    current_team_name = serializers.CharField(source='current_team.name', read_only=True)
    
    class Meta:
        model = Coach
        fields = [
            'id', 'name', 'nationality', 'date_of_birth', 'image_url',
            'current_team', 'current_team_name', 'contract_start', 'contract_end'
        ]


class TeamListSerializer(serializers.ModelSerializer):
    """Compact team serializer for lists."""
    
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'short_name', 'slug', 'team_type',
            'country', 'logo_url', 'primary_color', 'secondary_color',
            'founded_year', 'is_active'
        ]


class TeamDetailSerializer(serializers.ModelSerializer):
    """Detailed team serializer."""
    
    current_coaches = CoachSerializer(many=True, read_only=True)
    current_competitions = serializers.SerializerMethodField()
    squad_size = serializers.SerializerMethodField()
    venue = serializers.SerializerMethodField()
    
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'short_name', 'slug', 'team_type',
            'country', 'logo_url', 'founded_year',
            'primary_color', 'secondary_color',
            'external_api_id', 'external_api_source', 'metadata',
            'is_active', 'created_at', 'updated_at',
            'current_coaches', 'current_competitions', 'squad_size', 'venue'
        ]
    
    def get_current_competitions(self, obj):
        from competitions.models import Competition
        from competitions.serializers import CompetitionListSerializer
        
        current_season_ids = obj.season_participations.filter(
            season__is_current=True
        ).values_list('season__competition_id', flat=True)
        
        competitions = Competition.objects.filter(
            id__in=current_season_ids
        ).distinct()
        return CompetitionListSerializer(competitions, many=True).data
    
    def get_squad_size(self, obj):
        return obj.current_players.count()
    
    def get_venue(self, obj):
        home_matches = obj.home_matches.first()
        if home_matches and home_matches.venue:
            return VenueSerializer(home_matches.venue).data
        return None


class TeamSeasonSerializer(serializers.ModelSerializer):
    """Team participation in a season."""
    
    team_name = serializers.CharField(source='team.name', read_only=True)
    season_name = serializers.CharField(source='season.name', read_only=True)
    coach_name = serializers.CharField(source='coach.name', read_only=True, allow_null=True)
    
    class Meta:
        model = TeamSeason
        fields = [
            'id', 'team', 'team_name', 'season', 'season_name',
            'coach', 'coach_name', 'squad_size', 'average_age',
            'foreign_players_count', 'metadata'
        ]