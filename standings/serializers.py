"""
Serializers for standings app.
"""
from rest_framework import serializers
from .models import Standing, TeamStanding, StandingRule


class TeamStandingSerializer(serializers.ModelSerializer):
    """Individual team standings entry."""
    
    team_name = serializers.CharField(source='team.name', read_only=True)
    team_logo = serializers.CharField(source='team.logo_url', read_only=True)
    team_slug = serializers.CharField(source='team.slug', read_only=True)
    
    class Meta:
        model = TeamStanding
        fields = [
            'id', 'team', 'team_name', 'team_logo', 'team_slug',
            'position', 'played', 'wins', 'draws', 'losses',
            'goals_for', 'goals_against', 'goal_difference', 'points',
            'home_played', 'home_wins', 'home_draws', 'home_losses',
            'home_goals_for', 'home_goals_against',
            'away_played', 'away_wins', 'away_draws', 'away_losses',
            'away_goals_for', 'away_goals_against',
            'form', 'clean_sheets', 'failed_to_score', 'points_deduction'
        ]


class StandingSerializer(serializers.ModelSerializer):
    """Standings table with team entries."""
    
    team_standings = TeamStandingSerializer(many=True, read_only=True)
    competition_name = serializers.CharField(
        source='competition_season.competition.name', read_only=True
    )
    stage_name = serializers.CharField(source='stage.name', read_only=True)
    group_name = serializers.CharField(source='group.name', read_only=True, allow_null=True)
    
    class Meta:
        model = Standing
        fields = [
            'id', 'competition_season', 'competition_name',
            'stage', 'stage_name', 'group', 'group_name',
            'standing_type', 'is_live', 'last_calculated',
            'team_standings'
        ]


class StandingRuleSerializer(serializers.ModelSerializer):
    """Ranking rule serializer."""
    
    competition_name = serializers.CharField(source='competition.name', read_only=True)
    
    class Meta:
        model = StandingRule
        fields = [
            'id', 'competition', 'competition_name',
            'rule_type', 'priority', 'description', 'is_active'
        ]