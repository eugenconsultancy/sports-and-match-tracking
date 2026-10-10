"""
Team-related models: teams, venues, coaches, team-season participation.
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class Team(models.Model):
    """Core entity representing a club or national team."""
    
    class TeamType(models.TextChoices):
        CLUB = 'club', _('Club')
        NATIONAL = 'national', _('National Team')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True)
    short_name = models.CharField(max_length=10, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    team_type = models.CharField(
        max_length=20, choices=TeamType.choices, default=TeamType.CLUB
    )
    country = models.CharField(max_length=100, db_index=True)
    logo_url = models.URLField(blank=True)
    founded_year = models.IntegerField(null=True, blank=True)
    primary_color = models.CharField(max_length=7, default='#000000')
    secondary_color = models.CharField(max_length=7, default='#ffffff')
    external_api_id = models.CharField(max_length=100, blank=True, db_index=True)
    external_api_source = models.CharField(max_length=50, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'teams'
        verbose_name = _('team')
        verbose_name_plural = _('teams')
        ordering = ['name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['team_type', 'country']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.name


class Venue(models.Model):
    """Stadium or venue information."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    capacity = models.IntegerField(default=0)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    image_url = models.URLField(blank=True)
    external_api_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'venues'
        verbose_name = _('venue')
        verbose_name_plural = _('venues')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Coach(models.Model):
    """Team manager/coach."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True)
    nationality = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    image_url = models.URLField(blank=True)
    current_team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='current_coaches'
    )
    contract_start = models.DateField(null=True, blank=True)
    contract_end = models.DateField(null=True, blank=True)
    external_api_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'coaches'
        verbose_name = _('coach')
        verbose_name_plural = _('coaches')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class TeamSeason(models.Model):
    """Team participation in a specific season."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    team = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='season_participations'
    )
    season = models.ForeignKey(
        'competitions.Season', on_delete=models.CASCADE, related_name='team_participations'
    )
    coach = models.ForeignKey(
        Coach, on_delete=models.SET_NULL, null=True, blank=True, related_name='season_teams'
    )
    squad_size = models.IntegerField(default=0)
    average_age = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    foreign_players_count = models.IntegerField(default=0)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'team_seasons'
        verbose_name = _('team season')
        verbose_name_plural = _('team seasons')
        unique_together = ['team', 'season']
        indexes = [
            models.Index(fields=['team', 'season']),
        ]
    
    def __str__(self):
        return f"{self.team.name} - {self.season.name}"