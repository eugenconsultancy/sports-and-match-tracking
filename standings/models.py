"""
Standings-related models: standings tables, team standings, ranking rules.
"""
import uuid
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class Standing(models.Model):
    """Table container for a competition stage or group."""
    
    class StandingType(models.TextChoices):
        TOTAL = 'total', _('Total')
        HOME = 'home', _('Home')
        AWAY = 'away', _('Away')
        FORM = 'form', _('Form')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competition_season = models.ForeignKey(
        'competitions.Season', on_delete=models.CASCADE, related_name='standings'
    )
    stage = models.ForeignKey(
        'competitions.Stage', on_delete=models.CASCADE, related_name='standings'
    )
    group = models.ForeignKey(
        'competitions.Group', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='standings'
    )
    standing_type = models.CharField(
        max_length=20, choices=StandingType.choices, default=StandingType.TOTAL
    )
    is_live = models.BooleanField(default=False)
    last_calculated = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'standings'
        verbose_name = _('standing')
        verbose_name_plural = _('standings')
        unique_together = [['competition_season', 'stage', 'group', 'standing_type']]
        indexes = [
            models.Index(fields=['competition_season', 'stage']),
            models.Index(fields=['is_live']),
        ]
    
    def __str__(self):
        base = f"{self.competition_season} - {self.stage}"
        if self.group:
            base += f" - {self.group.name}"
        return f"{base} ({self.get_standing_type_display()})"


class TeamStanding(models.Model):
    """Team position in a standings table."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    standing = models.ForeignKey(
        Standing, on_delete=models.CASCADE, related_name='team_standings'
    )
    group = models.ForeignKey(
        'competitions.Group', on_delete=models.CASCADE, related_name='team_standings',
        null=True, blank=True
    )
    team = models.ForeignKey(
        'teams.Team', on_delete=models.CASCADE, related_name='standings_entries'
    )
    position = models.IntegerField(validators=[MinValueValidator(1)])
    played = models.IntegerField(default=0)
    wins = models.IntegerField(default=0)
    draws = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)
    goals_for = models.IntegerField(default=0)
    goals_against = models.IntegerField(default=0)
    goal_difference = models.IntegerField(default=0)
    points = models.IntegerField(default=0)
    
    # Home/Away specific
    home_played = models.IntegerField(default=0)
    home_wins = models.IntegerField(default=0)
    home_draws = models.IntegerField(default=0)
    home_losses = models.IntegerField(default=0)
    home_goals_for = models.IntegerField(default=0)
    home_goals_against = models.IntegerField(default=0)
    
    away_played = models.IntegerField(default=0)
    away_wins = models.IntegerField(default=0)
    away_draws = models.IntegerField(default=0)
    away_losses = models.IntegerField(default=0)
    away_goals_for = models.IntegerField(default=0)
    away_goals_against = models.IntegerField(default=0)
    
    # Form (last 5 matches)
    form = models.CharField(max_length=5, blank=True, help_text='e.g., WWDLW')
    
    # Additional metrics
    clean_sheets = models.IntegerField(default=0)
    failed_to_score = models.IntegerField(default=0)
    points_deduction = models.IntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'team_standings'
        verbose_name = _('team standing')
        verbose_name_plural = _('team standings')
        unique_together = [['standing', 'team']]
        ordering = ['standing', 'position']
        indexes = [
            models.Index(fields=['standing', 'position']),
            models.Index(fields=['team']),
        ]
    
    def __str__(self):
        return f"{self.team.name} - {self.position}th ({self.points} pts)"


class StandingRule(models.Model):
    """Defines ranking/tie-breaker logic."""
    
    class RuleType(models.TextChoices):
        POINTS = 'points', _('Points')
        GOAL_DIFFERENCE = 'goal_difference', _('Goal Difference')
        GOALS_FOR = 'goals_for', _('Goals For')
        HEAD_TO_HEAD = 'head_to_head', _('Head to Head')
        AWAY_GOALS = 'away_goals', _('Away Goals')
        FAIR_PLAY = 'fair_play', _('Fair Play')
        DRAWING_LOTS = 'drawing_lots', _('Drawing of Lots')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competition = models.ForeignKey(
        'competitions.Competition', on_delete=models.CASCADE, related_name='standing_rules'
    )
    rule_type = models.CharField(
        max_length=20, choices=RuleType.choices
    )
    priority = models.IntegerField(validators=[MinValueValidator(1)])
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'standing_rules'
        verbose_name = _('standing rule')
        verbose_name_plural = _('standing rules')
        ordering = ['competition', 'priority']
        unique_together = [['competition', 'priority']]
    
    def __str__(self):
        return f"{self.competition.name}: {self.get_rule_type_display()} (Priority {self.priority})"