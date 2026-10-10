"""
Serializers for competitions app.
"""
from rest_framework import serializers
from .models import Competition, Season, Stage, Group
from django.db import models


class CompetitionListSerializer(serializers.ModelSerializer):
    """Compact serializer for list views."""
    
    current_season = serializers.SerializerMethodField()
    
    class Meta:
        model = Competition
        fields = [
            'id', 'name', 'short_name', 'slug', 'competition_type',
            'tier', 'country', 'country_flag', 'logo_url',
            'primary_color', 'secondary_color', 'is_active', 'current_season'
        ]
    
    def get_current_season(self, obj):
        current_season = obj.seasons.filter(is_current=True).first()
        if current_season:
            return {
                'id': current_season.id,
                'name': current_season.name,
                'status': current_season.status,
            }
        return None


class CompetitionDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single competition."""
    
    seasons = serializers.SerializerMethodField()
    total_teams = serializers.SerializerMethodField()
    
    class Meta:
        model = Competition
        fields = [
            'id', 'name', 'short_name', 'slug', 'competition_type',
            'tier', 'country', 'country_flag', 'logo_url',
            'primary_color', 'secondary_color', 'is_active',
            'external_api_id', 'external_api_source', 'metadata',
            'created_at', 'updated_at', 'seasons', 'total_teams'
        ]
    
    def get_seasons(self, obj):
        seasons = obj.seasons.all().order_by('-start_date')[:10]
        return SeasonListSerializer(seasons, many=True).data
    
    def get_total_teams(self, obj):
        return obj.seasons.aggregate(total=models.Sum('total_teams'))['total'] or 0


class SeasonListSerializer(serializers.ModelSerializer):
    """Season serializer for lists."""
    
    competition_name = serializers.CharField(source='competition.name', read_only=True)
    
    class Meta:
        model = Season
        fields = [
            'id', 'competition', 'competition_name', 'name', 'slug',
            'start_date', 'end_date', 'status', 'is_current',
            'winner_team', 'total_teams', 'total_matches'
        ]


class SeasonDetailSerializer(serializers.ModelSerializer):
    """Detailed season serializer."""
    
    competition = CompetitionListSerializer(read_only=True)
    stages = serializers.SerializerMethodField()
    
    class Meta:
        model = Season
        fields = [
            'id', 'competition', 'name', 'slug', 'start_date', 'end_date',
            'status', 'is_current', 'winner_team', 'total_teams',
            'total_matches', 'external_api_id', 'metadata',
            'created_at', 'updated_at', 'stages'
        ]
    
    def get_stages(self, obj):
        stages = obj.stages.all().order_by('order')
        return StageListSerializer(stages, many=True).data


class StageListSerializer(serializers.ModelSerializer):
    """Stage serializer."""
    
    groups = serializers.SerializerMethodField()
    
    class Meta:
        model = Stage
        fields = [
            'id', 'name', 'stage_type', 'order', 'start_date', 'end_date',
            'is_active', 'groups'
        ]
    
    def get_groups(self, obj):
        if obj.stage_type == 'group':
            groups = obj.groups.all().order_by('sort_order')
            return GroupListSerializer(groups, many=True).data
        return []


class GroupListSerializer(serializers.ModelSerializer):
    """Group serializer."""
    
    teams_count = serializers.IntegerField(source='teams.count', read_only=True)
    
    class Meta:
        model = Group
        fields = [
            'id', 'name', 'label', 'sort_order', 'teams_count'
        ]