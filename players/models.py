"""
Player-related models: players, stats, transfers.
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Player(models.Model):
    """Individual athlete."""
    
    class Position(models.TextChoices):
        GOALKEEPER = 'GK', _('Goalkeeper')
        CENTER_BACK = 'CB', _('Center Back')
        LEFT_BACK = 'LB', _('Left Back')
        RIGHT_BACK = 'RB', _('Right Back')
        DEFENSIVE_MIDFIELDER = 'DM', _('Defensive Midfielder')
        CENTRAL_MIDFIELDER = 'CM', _('Central Midfielder')
        ATTACKING_MIDFIELDER = 'AM', _('Attacking Midfielder')
        LEFT_WINGER = 'LW', _('Left Winger')
        RIGHT_WINGER = 'RW', _('Right Winger')
        CENTER_FORWARD = 'CF', _('Center Forward')
        STRIKER = 'ST', _('Striker')
    
    class Foot(models.TextChoices):
        LEFT = 'left', _('Left')
        RIGHT = 'right', _('Right')
        BOTH = 'both', _('Both')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, db_index=True)
    full_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    nationality = models.CharField(max_length=100, db_index=True)
    position = models.CharField(
        max_length=5, choices=Position.choices, db_index=True
    )
    preferred_foot = models.CharField(
        max_length=5, choices=Foot.choices, default=Foot.RIGHT
    )
    height_cm = models.IntegerField(null=True, blank=True)
    weight_kg = models.IntegerField(null=True, blank=True)
    jersey_number = models.IntegerField(null=True, blank=True)
    current_team = models.ForeignKey(
        'teams.Team', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='current_players'
    )
    image_url = models.URLField(blank=True)
    market_value = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    market_value_currency = models.CharField(max_length=3, default='EUR')
    external_api_id = models.CharField(max_length=100, blank=True, db_index=True)
    external_api_source = models.CharField(max_length=50, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'players'
        verbose_name = _('player')
        verbose_name_plural = _('players')
        ordering = ['last_name', 'first_name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['position', 'nationality']),
            models.Index(fields=['current_team']),
            models.Index(fields=['external_api_id', 'external_api_source']),
        ]
    
    def __str__(self):
        return self.full_name


class PlayerStats(models.Model):
    """Aggregated player statistics per season."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='season_stats'
    )
    season = models.ForeignKey(
        'competitions.Season', on_delete=models.CASCADE, related_name='player_stats'
    )
    team = models.ForeignKey(
        'teams.Team', on_delete=models.CASCADE, related_name='player_stats'
    )
    appearances = models.IntegerField(default=0)
    minutes_played = models.IntegerField(default=0)
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    yellow_cards = models.IntegerField(default=0)
    red_cards = models.IntegerField(default=0)
    shots_total = models.IntegerField(default=0)
    shots_on_target = models.IntegerField(default=0)
    pass_accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    duels_won = models.IntegerField(default=0)
    dribbles_successful = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'player_stats'
        verbose_name = _('player stats')
        verbose_name_plural = _('player stats')
        unique_together = ['player', 'season', 'team']
        indexes = [
            models.Index(fields=['player', 'season']),
            models.Index(fields=['goals', 'assists']),
        ]
    
    def __str__(self):
        return f"{self.player.full_name} stats - {self.season.name}"


class PlayerMatchStats(models.Model):
    """Performance of a player in a specific match."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='match_stats'
    )
    match = models.ForeignKey(
        'matches.Match', on_delete=models.CASCADE, related_name='player_stats'
    )
    team = models.ForeignKey(
        'teams.Team', on_delete=models.CASCADE, related_name='player_match_stats'
    )
    goals = models.IntegerField(default=0)
    assists = models.IntegerField(default=0)
    minutes_played = models.IntegerField(default=0)
    yellow_card = models.BooleanField(default=False)
    red_card = models.BooleanField(default=False)
    shots_on_target = models.IntegerField(default=0)
    shots_off_target = models.IntegerField(default=0)
    passes_completed = models.IntegerField(default=0)
    passes_total = models.IntegerField(default=0)
    tackles = models.IntegerField(default=0)
    interceptions = models.IntegerField(default=0)
    fouls_committed = models.IntegerField(default=0)
    fouls_drawn = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    is_mvp = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'player_match_stats'
        verbose_name = _('player match stats')
        verbose_name_plural = _('player match stats')
        unique_together = ['player', 'match']
        indexes = [
            models.Index(fields=['match', 'rating']),
            models.Index(fields=['player', 'goals']),
        ]
    
    def __str__(self):
        return f"{self.player.full_name} vs match {self.match_id}"


class TransferHistory(models.Model):
    """Track player transfers between teams."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='transfers'
    )
    from_team = models.ForeignKey(
        'teams.Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='transfers_out'
    )
    to_team = models.ForeignKey(
        'teams.Team', on_delete=models.CASCADE, related_name='transfers_in'
    )
    transfer_date = models.DateField()
    transfer_fee = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    transfer_fee_currency = models.CharField(max_length=3, default='EUR')
    contract_until = models.DateField(null=True, blank=True)
    is_loan = models.BooleanField(default=False)
    additional_info = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'transfer_history'
        verbose_name = _('transfer history')
        verbose_name_plural = _('transfer histories')
        ordering = ['-transfer_date']
        indexes = [
            models.Index(fields=['player', '-transfer_date']),
            models.Index(fields=['to_team', '-transfer_date']),
        ]
    
    def __str__(self):
        return f"{self.player.full_name}: {self.from_team} → {self.to_team}"