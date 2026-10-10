"""
Service layer for competitions app.
Contains business logic for competition operations.
"""
import logging
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.db import models, transaction

logger = logging.getLogger(__name__)


class CompetitionService:
    """Service class for competition-related business logic."""
    
    @staticmethod
    def get_active_competitions():
        """Get all currently active competitions with live or upcoming seasons."""
        from .models import Competition, Season
        
        return Competition.objects.filter(
            is_active=True,
            seasons__status__in=['live', 'upcoming']
        ).distinct().order_by('tier', 'name')
    
    @staticmethod
    def get_current_season(competition):
        """Get the current season for a competition."""
        return competition.seasons.filter(is_current=True).first()
    
    @staticmethod
    def get_competition_by_slug(slug):
        """Get competition by slug with related data."""
        from .models import Competition
        
        return Competition.objects.filter(slug=slug).first()
    
    @staticmethod
    def search_competitions(query, limit=10):
        """Search competitions by name or country."""
        from .models import Competition
        
        return Competition.objects.filter(
            Q(name__icontains=query) |
            Q(short_name__icontains=query) |
            Q(country__icontains=query)
        ).filter(is_active=True)[:limit]
    
    @staticmethod
    @transaction.atomic
    def create_season(competition_id, name, start_date, end_date, **kwargs):
        """Create a new season for a competition."""
        from .models import Competition, Season
        
        competition = Competition.objects.get(id=competition_id)
        
        season = Season.objects.create(
            competition=competition,
            name=name,
            slug=name.lower().replace(' ', '-'),
            start_date=start_date,
            end_date=end_date,
            **kwargs
        )
        
        logger.info(f"Created season {season.name} for {competition.name}")
        return season
    
    @staticmethod
    def get_competition_statistics(competition_id):
        """Get statistics for a competition."""
        from .models import Competition
        from matches.models import Match
        
        competition = Competition.objects.get(id=competition_id)
        current_season = competition.seasons.filter(is_current=True).first()
        
        stats = {
            'total_seasons': competition.seasons.count(),
            'total_teams': 0,
            'total_matches': 0,
            'total_goals': 0,
            'avg_goals_per_match': 0,
        }
        
        if current_season:
            matches = Match.objects.filter(competition_season=current_season)
            finished = matches.filter(status='finished')
            
            stats['total_teams'] = current_season.total_teams
            stats['total_matches'] = matches.count()
            stats['total_goals'] = finished.aggregate(
                total=models.Sum(models.F('home_score') + models.F('away_score'))
            )['total'] or 0
            
            if finished.count() > 0:
                stats['avg_goals_per_match'] = round(
                    stats['total_goals'] / finished.count(), 2
                )
        
        return stats