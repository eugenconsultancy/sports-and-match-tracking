"""
Serializers for matches app.
"""
from rest_framework import serializers
from .models import Match, MatchEvent, Lineup, MatchStats, MatchLiveState


class MatchListSerializer(serializers.ModelSerializer):
    """Compact match serializer for lists."""
    
    home_team_name = serializers.CharField(source='home_team.name', read_only=True)
    home_team_logo = serializers.CharField(source='home_team.logo_url', read_only=True)
    away_team_name = serializers.CharField(source='away_team.name', read_only=True)
    away_team_logo = serializers.CharField(source='away_team.logo_url', read_only=True)
    competition_name = serializers.CharField(source='competition_season.competition.name', read_only=True)
    venue_name = serializers.CharField(source='venue.name', read_only=True, allow_null=True)
    
    class Meta:
        model = Match
        fields = [
            'id', 'home_team', 'home_team_name', 'home_team_logo',
            'away_team', 'away_team_name', 'away_team_logo',
            'home_score', 'away_score', 'home_score_halftime', 'away_score_halftime',
            'kickoff_time', 'status', 'minute', 'competition_name', 'venue_name',
            'matchday', 'is_featured', 'competition_season', 'stage', 'group'
        ]


class MatchDetailSerializer(serializers.ModelSerializer):
    """Detailed match serializer with related data."""
    
    home_team = serializers.SerializerMethodField()
    away_team = serializers.SerializerMethodField()
    competition = serializers.SerializerMethodField()
    venue = serializers.SerializerMethodField()
    events = serializers.SerializerMethodField()
    lineups = serializers.SerializerMethodField()
    stats = serializers.SerializerMethodField()
    live_state = serializers.SerializerMethodField()
    has_poll = serializers.SerializerMethodField()
    
    class Meta:
        model = Match
        fields = [
            'id', 'home_team', 'away_team', 'home_score', 'away_score',
            'home_score_halftime', 'away_score_halftime',
            'kickoff_time', 'status', 'minute', 'injury_time',
            'attendance', 'referee_name', 'is_featured',
            'round_number', 'matchday', 'competition', 'venue',
            'external_api_id', 'metadata', 'created_at',
            'events', 'lineups', 'stats', 'live_state', 'has_poll'
        ]
    
    def get_home_team(self, obj):
        from teams.serializers import TeamListSerializer
        return TeamListSerializer(obj.home_team).data
    
    def get_away_team(self, obj):
        from teams.serializers import TeamListSerializer
        return TeamListSerializer(obj.away_team).data
    
    def get_competition(self, obj):
        from competitions.serializers import CompetitionListSerializer
        return CompetitionListSerializer(obj.competition_season.competition).data
    
    def get_venue(self, obj):
        if obj.venue:
            from teams.serializers import VenueSerializer
            return VenueSerializer(obj.venue).data
        return None
    
    def get_events(self, obj):
        events = obj.events.all().order_by('minute', 'injury_minute')
        return MatchEventSerializer(events, many=True).data
    
    def get_lineups(self, obj):
        lineups = obj.lineups.select_related('player', 'team').all()
        return LineupSerializer(lineups, many=True).data
    
    def get_stats(self, obj):
        stats = obj.stats.all()
        return MatchStatsSerializer(stats, many=True).data
    
    def get_live_state(self, obj):
        if hasattr(obj, 'live_state') and obj.live_state:
            return MatchLiveStateSerializer(obj.live_state).data
        return None
    
    def get_has_poll(self, obj):
        return hasattr(obj, 'poll') and obj.poll is not None


class MatchEventSerializer(serializers.ModelSerializer):
    """Match event (goal, card, etc.) serializer."""
    
    player_name = serializers.CharField(source='player.full_name', read_only=True)
    related_player_name = serializers.CharField(
        source='related_player.full_name', read_only=True, allow_null=True
    )
    team_name = serializers.CharField(source='team.name', read_only=True)
    
    class Meta:
        model = MatchEvent
        fields = [
            'id', 'match', 'event_type', 'minute', 'injury_minute',
            'player', 'player_name', 'related_player', 'related_player_name',
            'team', 'team_name', 'description', 'score_home', 'score_away',
            'metadata'
        ]


class LineupSerializer(serializers.ModelSerializer):
    """Player lineup entry serializer."""
    
    player_name = serializers.CharField(source='player.full_name', read_only=True)
    player_image = serializers.CharField(source='player.image_url', read_only=True)
    team_name = serializers.CharField(source='team.name', read_only=True)
    
    class Meta:
        model = Lineup
        fields = [
            'id', 'match', 'team', 'team_name', 'player', 'player_name',
            'player_image', 'role', 'position', 'jersey_number',
            'is_captain', 'sort_order'
        ]


class MatchStatsSerializer(serializers.ModelSerializer):
    """Match statistics per team serializer."""
    
    team_name = serializers.CharField(source='team.name', read_only=True)
    
    class Meta:
        model = MatchStats
        fields = [
            'id', 'match', 'team', 'team_name',
            'possession_percentage', 'shots_total', 'shots_on_target',
            'shots_off_target', 'blocked_shots', 'corner_kicks',
            'offsides', 'fouls', 'yellow_cards', 'red_cards',
            'passes_total', 'passes_accurate', 'pass_accuracy',
            'crosses_total', 'crosses_accurate', 'tackles_total',
            'tackles_accurate', 'interceptions', 'clearances',
            'goalkeeper_saves', 'expected_goals_xg'
        ]


class MatchLiveStateSerializer(serializers.ModelSerializer):
    """Real-time match state serializer."""
    
    class Meta:
        model = MatchLiveState
        fields = [
            'id', 'match', 'current_minute', 'injury_minute',
            'home_score', 'away_score', 'attacks', 'dangerous_attacks',
            'momentum', 'last_events', 'possession', 'match_status',
            'updated_at'
        ]