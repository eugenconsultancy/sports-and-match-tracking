"""
Competition-related models: tournaments, seasons, stages, groups.
"""
import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Competition(models.Model):
    """Represents a tournament or league (e.g., FIFA World Cup, Premier League)."""
    
    class CompetitionType(models.TextChoices):
        LEAGUE = 'league', _('League')
        CUP = 'cup', _('Cup')
        INTERNATIONAL = 'international', _('International')
        FRIENDLY = 'friendly', _('Friendly')
    
    class Tier(models.IntegerChoices):
        TIER_1 = 1, _('Tier 1')
        TIER_2 = 2, _('Tier 2')
        TIER_3 = 3, _('Tier 3')
        TIER_4 = 4, _('Tier 4')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, db_index=True)
    short_name = models.CharField(max_length=50, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    competition_type = models.CharField(
        max_length=20, choices=CompetitionType.choices, default=CompetitionType.LEAGUE
    )
    tier = models.IntegerField(choices=Tier.choices, default=Tier.TIER_1)
    country = models.CharField(max_length=100, db_index=True)
    country_flag = models.URLField(blank=True)
    logo_url = models.URLField(blank=True)
    primary_color = models.CharField(max_length=7, default='#1a1a1a')
    secondary_color = models.CharField(max_length=7, default='#ffffff')
    is_active = models.BooleanField(default=True, db_index=True)
    external_api_id = models.CharField(max_length=100, blank=True, db_index=True)
    external_api_source = models.CharField(max_length=50, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'competitions'
        verbose_name = _('competition')
        verbose_name_plural = _('competitions')
        ordering = ['tier', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['competition_type', 'is_active']),
            models.Index(fields=['country']),
        ]
    
    def __str__(self):
        return self.name


class Season(models.Model):
    """Specific edition of a competition (e.g., 2025-2026 season)."""
    
    class Status(models.TextChoices):
        UPCOMING = 'upcoming', _('Upcoming')
        LIVE = 'live', _('Live')
        FINISHED = 'finished', _('Finished')
        CANCELLED = 'cancelled', _('Cancelled')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    competition = models.ForeignKey(
        Competition, on_delete=models.CASCADE, related_name='seasons'
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.UPCOMING, db_index=True
    )
    is_current = models.BooleanField(default=False, db_index=True)
    winner_team = models.ForeignKey(
        'teams.Team', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='won_seasons'
    )
    total_teams = models.IntegerField(default=0)
    total_matches = models.IntegerField(default=0)
    external_api_id = models.CharField(max_length=100, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'seasons'
        verbose_name = _('season')
        verbose_name_plural = _('seasons')
        ordering = ['-start_date']
        unique_together = ['competition', 'slug']
        indexes = [
            models.Index(fields=['competition', 'status']),
            models.Index(fields=['is_current']),
        ]
    
    def __str__(self):
        return f"{self.competition.name} - {self.name}"


class Stage(models.Model):
    """Logical phase of a competition (Group Stage, Knockout, Final)."""
    
    class StageType(models.TextChoices):
        GROUP = 'group', _('Group Stage')
        KNOCKOUT = 'knockout', _('Knockout Stage')
        QUALIFICATION = 'qualification', _('Qualification')
        PLAYOFF = 'playoff', _('Playoff')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    season = models.ForeignKey(
        Season, on_delete=models.CASCADE, related_name='stages'
    )
    name = models.CharField(max_length=255)
    stage_type = models.CharField(
        max_length=20, choices=StageType.choices, default=StageType.GROUP, db_index=True
    )
    order = models.IntegerField(default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'stages'
        verbose_name = _('stage')
        verbose_name_plural = _('stages')
        ordering = ['season', 'order']
        indexes = [
            models.Index(fields=['season', 'stage_type']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.season} - {self.name}"


class Group(models.Model):
    """Subdivision inside a stage (e.g., Group A, Group B)."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    stage = models.ForeignKey(
        Stage, on_delete=models.CASCADE, related_name='groups'
    )
    name = models.CharField(max_length=50)
    label = models.CharField(max_length=10, blank=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'groups'
        verbose_name = _('group')
        verbose_name_plural = _('groups')
        ordering = ['stage', 'sort_order']
        indexes = [
            models.Index(fields=['stage', 'sort_order']),
        ]
    
    def __str__(self):
        return f"{self.stage} - {self.name}"