"""
Favorites-related models: user favorite teams, matches, competitions.
"""
import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserFavoriteTeam(models.Model):
    """User's favorite teams."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'users_app.User', on_delete=models.CASCADE, related_name='favorite_teams'
    )
    team = models.ForeignKey(
        'teams.Team', on_delete=models.CASCADE, related_name='favorited_by'
    )
    priority = models.IntegerField(default=0)
    notify_matches = models.BooleanField(default=True)
    notify_goals = models.BooleanField(default=True)
    notify_transfers = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_favorite_teams'
        verbose_name = _('user favorite team')
        verbose_name_plural = _('user favorite teams')
        unique_together = ['user', 'team']
        ordering = ['user', 'priority']
    
    def __str__(self):
        return f"{self.user.email} → {self.team.name}"


class UserFavoriteMatch(models.Model):
    """User's followed matches."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'users_app.User', on_delete=models.CASCADE, related_name='favorite_matches'
    )
    match = models.ForeignKey(
        'matches.Match', on_delete=models.CASCADE, related_name='favorited_by'
    )
    notify_goals = models.BooleanField(default=True)
    notify_half_time = models.BooleanField(default=False)
    notify_full_time = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_favorite_matches'
        verbose_name = _('user favorite match')
        verbose_name_plural = _('user favorite matches')
        unique_together = ['user', 'match']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.email} → match {self.match_id}"


class UserFavoriteCompetition(models.Model):
    """User's favorite competitions."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        'users_app.User', on_delete=models.CASCADE, related_name='favorite_competitions'
    )
    competition = models.ForeignKey(
        'competitions.Competition', on_delete=models.CASCADE,
        related_name='favorited_by'
    )
    priority = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'user_favorite_competitions'
        verbose_name = _('user favorite competition')
        verbose_name_plural = _('user favorite competitions')
        unique_together = ['user', 'competition']
        ordering = ['user', 'priority']
    
    def __str__(self):
        return f"{self.user.email} → {self.competition.name}"