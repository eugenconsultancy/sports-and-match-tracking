"""
Service layer for matches app.
Contains business logic for match operations.
"""
import logging
from django.db import transaction
from django.db.models import Q, F
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)


class MatchService:
    """Service class for match-related business logic."""
    
    @staticmethod
    def get_live_matches():
        """Get all currently live matches."""
        from .models import Match
        
        return Match.objects.filter(
            status__in=['live', 'half_time']
        ).select_related(
            'home_team', 'away_team', 'competition_season__competition'
        ).order_by('kickoff_time')
    
    @staticmethod
    def get_today_matches():
        """Get all matches scheduled for today."""
        from .models import Match
        
        today = timezone.now().date()
        
        return Match.objects.filter(
            kickoff_time__date=today
        ).select_related(
            'home_team', 'away_team', 'competition_season__competition'
        ).order_by('kickoff_time')
    
    @staticmethod
    def get_upcoming_matches(days=7, limit=50):
        """Get upcoming matches within the next N days."""
        from .models import Match
        
        now = timezone.now()
        end_date = now + timedelta(days=days)
        
        return Match.objects.filter(
            kickoff_time__gte=now,
            kickoff_time__lte=end_date,
            status='scheduled'
        ).select_related(
            'home_team', 'away_team', 'competition_season__competition'
        ).order_by('kickoff_time')[:limit]
    
    @staticmethod
    def get_team_matches(team_id, last=10, upcoming=10):
        """Get recent and upcoming matches for a team."""
        from .models import Match
        
        recent = Match.objects.filter(
            Q(home_team_id=team_id) | Q(away_team_id=team_id),
            status='finished'
        ).select_related(
            'home_team', 'away_team', 'competition_season__competition'
        ).order_by('-kickoff_time')[:last]
        
        upcoming = Match.objects.filter(
            Q(home_team_id=team_id) | Q(away_team_id=team_id),
            status='scheduled'
        ).select_related(
            'home_team', 'away_team', 'competition_season__competition'
        ).order_by('kickoff_time')[:upcoming]
        
        return {
            'recent': list(recent),
            'upcoming': list(upcoming),
        }
    
    @staticmethod
    @transaction.atomic
    def update_match_score(match_id, home_score, away_score, minute=None):
        """Update match score and related data."""
        from .models import Match, MatchLiveState
        
        match = Match.objects.select_for_update().get(id=match_id)
        
        match.home_score = home_score
        match.away_score = away_score
        
        if minute is not None:
            match.minute = minute
        
        if home_score > 0 or away_score > 0:
            if match.status == 'scheduled':
                match.status = 'live'
        
        match.save()
        
        # Update live state
        live_state, _ = MatchLiveState.objects.get_or_create(match=match)
        live_state.home_score = home_score
        live_state.away_score = away_score
        if minute:
            live_state.current_minute = minute
        live_state.match_status = match.status
        live_state.save()
        
        logger.info(f"Updated match {match_id} score: {home_score}-{away_score}")
        return match
    
    @staticmethod
    @transaction.atomic
    def add_match_event(match_id, event_type, minute, player_id, team_id, **kwargs):
        """Add an event to a match."""
        from .models import Match, MatchEvent
        
        match = Match.objects.get(id=match_id)
        
        event = MatchEvent.objects.create(
            match=match,
            event_type=event_type,
            minute=minute,
            player_id=player_id,
            team_id=team_id,
            **kwargs
        )
        
        # Update score for goals
        if event_type in ['goal', 'penalty_goal', 'own_goal']:
            if team_id == match.home_team_id:
                match.home_score += 1
            else:
                match.away_score += 1
            match.save()
        
        return event
    
    @staticmethod
    @transaction.atomic
    def finish_match(match_id, home_score=None, away_score=None):
        """Mark a match as finished."""
        from .models import Match
        
        match = Match.objects.select_for_update().get(id=match_id)
        
        match.status = 'finished'
        match.minute = 90
        
        if home_score is not None:
            match.home_score = home_score
        if away_score is not None:
            match.away_score = away_score
        
        match.save()
        
        # Trigger standings update
        from standings.tasks import update_standing_for_match
        update_standing_for_match.delay(match_id)
        
        logger.info(f"Finished match {match_id}")
        return match
    
    @staticmethod
    def get_match_timeline(match_id):
        """Get full match timeline with events sorted chronologically."""
        from .models import MatchEvent
        
        return MatchEvent.objects.filter(
            match_id=match_id
        ).select_related(
            'player', 'related_player', 'team'
        ).order_by('minute', 'injury_minute')