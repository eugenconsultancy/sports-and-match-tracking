"""
Poll-related models: polls, options, votes, cached results.
"""
import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Poll(models.Model):
    """Who Will Win poll widget."""
    
    class Status(models.TextChoices):
        ACTIVE = 'active', _('Active')
        CLOSED = 'closed', _('Closed')
        ARCHIVED = 'archived', _('Archived')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    match = models.OneToOneField(
        'matches.Match', on_delete=models.CASCADE, related_name='poll'
    )
    question = models.CharField(max_length=255, default="Who will win?")
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.ACTIVE, db_index=True
    )
    total_votes = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        'users_app.User', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='created_polls'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'polls'
        verbose_name = _('poll')
        verbose_name_plural = _('polls')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['match', 'status']),
            models.Index(fields=['status', '-total_votes']),
        ]
    
    def __str__(self):
        return f"Poll: {self.match}"


class PollOption(models.Model):
    """Available choices in a poll (Home win / Draw / Away win)."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name='options'
    )
    label = models.CharField(max_length=100)
    team = models.ForeignKey(
        'teams.Team', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='poll_options',
        help_text='Associated team (null for Draw option)'
    )
    option_type = models.CharField(
        max_length=20, choices=[
            ('home', 'Home Win'),
            ('draw', 'Draw'),
            ('away', 'Away Win'),
        ]
    )
    sort_order = models.IntegerField(default=0)
    vote_count = models.IntegerField(default=0)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'poll_options'
        verbose_name = _('poll option')
        verbose_name_plural = _('poll options')
        ordering = ['poll', 'sort_order']
    
    def __str__(self):
        return f"{self.label} ({self.vote_count} votes)"


class Vote(models.Model):
    """Individual user vote."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll = models.ForeignKey(
        Poll, on_delete=models.CASCADE, related_name='votes'
    )
    option = models.ForeignKey(
        PollOption, on_delete=models.CASCADE, related_name='votes'
    )
    user = models.ForeignKey(
        'users_app.User', on_delete=models.CASCADE, related_name='poll_votes'
    )
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    voted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'votes'
        verbose_name = _('vote')
        verbose_name_plural = _('votes')
        unique_together = ['poll', 'user']
        indexes = [
            models.Index(fields=['poll', 'voted_at']),
            models.Index(fields=['user', 'poll']),
        ]
    
    def __str__(self):
        return f"Vote by {self.user.email} for {self.option.label}"


class PollResultCache(models.Model):
    """Cached aggregated poll results for fast reads."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    poll = models.OneToOneField(
        Poll, on_delete=models.CASCADE, related_name='result_cache'
    )
    results_json = models.JSONField()
    total_votes = models.IntegerField(default=0)
    last_calculated = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'poll_result_caches'
        verbose_name = _('poll result cache')
        verbose_name_plural = _('poll result caches')
    
    def __str__(self):
        return f"Cache for {self.poll}"