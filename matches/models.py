"""
Match-related models: matches, events, lineups, stats, live state.
"""
import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Match(models.Model):
    """Central entity representing a fixture/match."""
    
    class Status(models.TextChoices):
        SCHEDULED = 'scheduled', _('Scheduled')
        LIVE = 'live', _('Live')
        HALF_TIME = 'half_time', _('Half Time')
        FINISHED = 'finished', _('Finished')
        POSTPONED = 'postponed', _('Postponed')
        CANCELLED = 'cancelled', _('Cancelled')
        SUSPENDED = 'suspended', _('Suspended')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    home_team = models.ForeignKey(
        'teams.Team', on_delete=models.CASCADE, related_name='home_matches'
    )
    away_team = models.ForeignKey(
        'teams.Team', on_delete=models.CASCADE, related_name='away_matches'
    )
    competition_season = models.ForeignKey(
        'competitions.Season', on_delete=models.CASCADE, related_name='matches'
    )
    stage = models.ForeignKey(
        'competitions.Stage', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='matches'
    )
    group = models.ForeignKey(
        'competitions.Group', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='matches'
    )
    venue = models.ForeignKey(
        'teams.Venue', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='matches'
    )
    round_number = models.IntegerField(null=True, blank=True)
    matchday = models.CharField(max_length=50, blank=True)
    kickoff_time = models.DateTimeField(db_index=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.SCHEDULED, db_index=True
    )
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    home_score_halftime = models.IntegerField(null=True, blank=True)
    away_score_halftime = models.IntegerField(null=True, blank=True)
    minute = models.IntegerField(null=True, blank=True, help_text='Current minute of play')
    injury_time = models.IntegerField(null=True, blank=True)
    attendance = models.IntegerField(null=True, blank=True)
    referee_name = models.CharField(max_length=255, blank=True)
    is_featured = models.BooleanField(default=False)
    external_api_id = models.CharField(max_length=100, blank=True, db_index=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'matches'
        verbose_name = _('match')
        verbose_name_plural = _('matches')
        ordering = ['-kickoff_time']
        indexes = [
            models.Index(fields=['status', 'kickoff_time']),
            models.Index(fields=['competition_season', 'status']),
            models.Index(fields=['home_team', 'status']),
            models.Index(fields=['away_team', 'status']),
            models.Index(fields=['external_api_id']),
        ]
        constraints = [
            models.CheckConstraint(
                check=~models.Q(home_team=models.F('away_team')),
                name='no_same_team_match'
            )
        ]
    
    def __str__(self):
        return f"{self.home_team} {self.home_score} - {self.away_score} {self.away_team}"
    
    @property
    def is_live(self):
        return self.status == self.Status.LIVE


class MatchEvent(models.Model):
    """Timeline events in a match (goals, cards, substitutions)."""
    
    class EventType(models.TextChoices):
        GOAL = 'goal', _('Goal')
        OWN_GOAL = 'own_goal', _('Own Goal')
        PENALTY_GOAL = 'penalty_goal', _('Penalty Goal')
        PENALTY_MISS = 'penalty_miss', _('Penalty Miss')
        YELLOW_CARD = 'yellow_card', _('Yellow Card')
        SECOND_YELLOW = 'second_yellow', _('Second Yellow Card')
        RED_CARD = 'red_card', _('Red Card')
        SUBSTITUTION_IN = 'substitution_in', _('Substitution In')
        SUBSTITUTION_OUT = 'substitution_out', _('Substitution Out')
        ASSIST = 'assist', _('Assist')
        HALF_TIME = 'half_time', _('Half Time')
        FULL_TIME = 'full_time', _('Full Time')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(
        Match, on_delete=models.CASCADE, related_name='events'
    )
    event_type = models.CharField(
        max_length=30, choices=EventType.choices, db_index=True
    )
    minute = models.IntegerField()
    injury_minute = models.IntegerField(null=True, blank=True)
    player = models.ForeignKey(
        'players.Player', on_delete=models.CASCADE, related_name='match_events'
    )
    related_player = models.ForeignKey(
        'players.Player', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='related_match_events',
        help_text='Assist provider, substituted player, etc.'
    )
    team = models.ForeignKey(
        'teams.Team', on_delete=models.CASCADE, related_name='match_events'
    )
    description = models.TextField(blank=True)
    score_home = models.IntegerField(null=True, blank=True)
    score_away = models.IntegerField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'match_events'
        verbose_name = _('match event')
        verbose_name_plural = _('match events')
        ordering = ['match', 'minute', 'injury_minute']
        indexes = [
            models.Index(fields=['match', 'event_type']),
            models.Index(fields=['player', 'event_type']),
        ]
    
    def __str__(self):
        return f"{self.get_event_type_display()}: {self.player} at {self.minute}'"


class Lineup(models.Model):
    """Starting lineup and bench for a match."""
    
    class PlayerRole(models.TextChoices):
        STARTER = 'starter', _('Starter')
        BENCH = 'bench', _('Bench')
        NOT_IN_SQUAD = 'not_in_squad', _('Not in Squad')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(
        Match, on_delete=models.CASCADE, related_name='lineups'
    )
    team = models.ForeignKey(
        'teams.Team', on_delete=models.CASCADE, related_name='lineups'
    )
    player = models.ForeignKey(
        'players.Player', on_delete=models.CASCADE, related_name='lineups'
    )
    role = models.CharField(
        max_length=20, choices=PlayerRole.choices, default=PlayerRole.STARTER
    )
    position = models.CharField(max_length=5)
    jersey_number = models.IntegerField()
    is_captain = models.BooleanField(default=False)
    sort_order = models.IntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'lineups'
        verbose_name = _('lineup')
        verbose_name_plural = _('lineups')
        unique_together = ['match', 'player']
        ordering = ['team', 'sort_order']
        indexes = [
            models.Index(fields=['match', 'team', 'role']),
        ]
    
    def __str__(self):
        return f"{self.player} ({self.team}) - {self.role}"


class MatchStats(models.Model):
    """Aggregated match statistics per team."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.ForeignKey(
        Match, on_delete=models.CASCADE, related_name='stats'
    )
    team = models.ForeignKey(
        'teams.Team', on_delete=models.CASCADE, related_name='match_stats'
    )
    possession_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    shots_total = models.IntegerField(default=0)
    shots_on_target = models.IntegerField(default=0)
    shots_off_target = models.IntegerField(default=0)
    blocked_shots = models.IntegerField(default=0)
    corner_kicks = models.IntegerField(default=0)
    offsides = models.IntegerField(default=0)
    fouls = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    passes_total = models.IntegerField(default=0)
    passes_accurate = models.IntegerField(default=0)
    pass_accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    crosses_total = models.IntegerField(default=0)
    crosses_accurate = models.IntegerField(default=0)
    tackles_total = models.IntegerField(default=0)
    tackles_accurate = models.IntegerField(default=0)
    interceptions = models.IntegerField(default=0)
    clearances = models.IntegerField(default=0)
    goalkeeper_saves = models.IntegerField(default=0)
    expected_goals_xg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'match_stats'
        verbose_name = _('match stats')
        verbose_name_plural = _('match stats')
        unique_together = ['match', 'team']
        indexes = [
            models.Index(fields=['match']),
        ]
    
    def __str__(self):
        return f"Stats: {self.team} in match {self.match_id}"


class MatchLiveState(models.Model):
    """Real-time snapshot for fast API delivery (cached/denormalized)."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.OneToOneField(
        Match, on_delete=models.CASCADE, related_name='live_state'
    )
    current_minute = models.IntegerField(default=0)
    injury_minute = models.IntegerField(null=True, blank=True)
    home_score = models.IntegerField(default=0)
    away_score = models.IntegerField(default=0)
    attacks = models.JSONField(default=list, help_text='Recent attack sequences')
    dangerous_attacks = models.JSONField(default=list)
    momentum = models.CharField(
        max_length=20, choices=[
            ('home', 'Home Dominant'),
            ('away', 'Away Dominant'),
            ('balanced', 'Balanced'),
        ], default='balanced'
    )
    last_events = models.JSONField(default=list, help_text='Last 5 events')
    possession = models.JSONField(default=dict, help_text='{home: 55, away: 45}')
    match_status = models.CharField(max_length=20, default='scheduled')
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'match_live_states'
        verbose_name = _('match live state')
        verbose_name_plural = _('match live states')
    
    def __str__(self):
        return f"Live state: {self.match}"