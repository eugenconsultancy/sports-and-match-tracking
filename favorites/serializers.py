"""
Serializers for favorites app.
"""
from rest_framework import serializers
from .models import UserFavoriteTeam, UserFavoriteMatch, UserFavoriteCompetition


class UserFavoriteTeamSerializer(serializers.ModelSerializer):
    """User favorite team serializer."""
    
    team_name = serializers.CharField(source='team.name', read_only=True)
    team_logo = serializers.CharField(source='team.logo_url', read_only=True)
    team_slug = serializers.CharField(source='team.slug', read_only=True)
    
    class Meta:
        model = UserFavoriteTeam
        fields = [
            'id', 'team', 'team_name', 'team_logo', 'team_slug',
            'priority', 'notify_matches', 'notify_goals', 'notify_transfers',
            'created_at'
        ]
        read_only_fields = ['user', 'created_at']


class UserFavoriteMatchSerializer(serializers.ModelSerializer):
    """User favorite match serializer."""
    
    home_team = serializers.CharField(source='match.home_team.name', read_only=True)
    away_team = serializers.CharField(source='match.away_team.name', read_only=True)
    match_status = serializers.CharField(source='match.status', read_only=True)
    score = serializers.SerializerMethodField()
    
    class Meta:
        model = UserFavoriteMatch
        fields = [
            'id', 'match', 'home_team', 'away_team', 'match_status',
            'score', 'notify_goals', 'notify_half_time', 'notify_full_time',
            'created_at'
        ]
        read_only_fields = ['user', 'created_at']
    
    def get_score(self, obj):
        return f"{obj.match.home_score} - {obj.match.away_score}"


class UserFavoriteCompetitionSerializer(serializers.ModelSerializer):
    """User favorite competition serializer."""
    
    competition_name = serializers.CharField(source='competition.name', read_only=True)
    competition_logo = serializers.CharField(source='competition.logo_url', read_only=True)
    
    class Meta:
        model = UserFavoriteCompetition
        fields = [
            'id', 'competition', 'competition_name', 'competition_logo',
            'priority', 'created_at'
        ]
        read_only_fields = ['user', 'created_at']


class AddFavoriteSerializer(serializers.Serializer):
    """Serializer for adding a favorite."""
    
    entity_type = serializers.ChoiceField(choices=['team', 'match', 'competition'])
    entity_id = serializers.UUIDField()
    
    def validate(self, data):
        """Validate that the entity exists."""
        entity_type = data['entity_type']
        entity_id = data['entity_id']
        
        if entity_type == 'team':
            from teams.models import Team
            if not Team.objects.filter(id=entity_id).exists():
                raise serializers.ValidationError("Team not found")
        elif entity_type == 'match':
            from matches.models import Match
            if not Match.objects.filter(id=entity_id).exists():
                raise serializers.ValidationError("Match not found")
        elif entity_type == 'competition':
            from competitions.models import Competition
            if not Competition.objects.filter(id=entity_id).exists():
                raise serializers.ValidationError("Competition not found")
        
        return data