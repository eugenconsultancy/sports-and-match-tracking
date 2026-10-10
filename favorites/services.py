"""
Service layer for favorites app.
Contains business logic for managing user favorites.
"""
import logging
from django.db import transaction
from django.db.models import Q
from django.core.cache import cache

logger = logging.getLogger(__name__)


class FavoritesService:
    """Service class for favorites-related business logic."""
    
    @staticmethod
    def get_user_favorite_teams(user_id):
        """Get user's favorite teams with live match info."""
        from .models import UserFavoriteTeam
        
        favorites = UserFavoriteTeam.objects.filter(
            user_id=user_id
        ).select_related(
            'team'
        ).prefetch_related(
            'team__home_matches',
            'team__away_matches'
        ).order_by('priority')
        
        result = []
        for fav in favorites:
            team_data = {
                'id': str(fav.id),
                'team_id': str(fav.team_id),
                'team_name': fav.team.name,
                'team_logo': fav.team.logo_url,
                'team_slug': fav.team.slug,
                'priority': fav.priority,
                'notify_matches': fav.notify_matches,
                'notify_goals': fav.notify_goals,
                'notify_transfers': fav.notify_transfers,
                'next_match': FavoritesService._get_team_next_match(fav.team),
                'live_match': FavoritesService._get_team_live_match(fav.team),
            }
            result.append(team_data)
        
        return result
    
    @staticmethod
    def get_user_favorite_matches(user_id):
        """Get user's favorite matches."""
        from .models import UserFavoriteMatch
        
        favorites = UserFavoriteMatch.objects.filter(
            user_id=user_id
        ).select_related(
            'match__home_team',
            'match__away_team',
            'match__competition_season__competition'
        ).order_by('-created_at')
        
        result = []
        for fav in favorites:
            match_data = {
                'id': str(fav.id),
                'match_id': str(fav.match_id),
                'home_team': fav.match.home_team.name if fav.match.home_team else None,
                'away_team': fav.match.away_team.name if fav.match.away_team else None,
                'home_score': fav.match.home_score,
                'away_score': fav.match.away_score,
                'status': fav.match.status,
                'kickoff_time': fav.match.kickoff_time.isoformat() if fav.match.kickoff_time else None,
                'notify_goals': fav.notify_goals,
                'notify_half_time': fav.notify_half_time,
                'notify_full_time': fav.notify_full_time,
            }
            result.append(match_data)
        
        return result
    
    @staticmethod
    def get_user_favorite_competitions(user_id):
        """Get user's favorite competitions."""
        from .models import UserFavoriteCompetition
        
        favorites = UserFavoriteCompetition.objects.filter(
            user_id=user_id
        ).select_related(
            'competition'
        ).order_by('priority')
        
        result = []
        for fav in favorites:
            comp_data = {
                'id': str(fav.id),
                'competition_id': str(fav.competition_id),
                'competition_name': fav.competition.name,
                'competition_logo': fav.competition.logo_url,
                'competition_slug': fav.competition.slug,
                'priority': fav.priority,
                'current_season': FavoritesService._get_current_season_info(fav.competition),
            }
            result.append(comp_data)
        
        return result
    
    @staticmethod
    def get_all_user_favorites(user_id):
        """Get all user favorites in a single call."""
        return {
            'teams': FavoritesService.get_user_favorite_teams(user_id),
            'matches': FavoritesService.get_user_favorite_matches(user_id),
            'competitions': FavoritesService.get_user_favorite_competitions(user_id),
        }
    
    @staticmethod
    @transaction.atomic
    def add_favorite_team(user_id, team_id, **kwargs):
        """Add a team to user favorites."""
        from .models import UserFavoriteTeam
        from teams.models import Team
        
        team = Team.objects.get(id=team_id)
        
        favorite, created = UserFavoriteTeam.objects.get_or_create(
            user_id=user_id,
            team_id=team_id,
            defaults={
                'priority': kwargs.get('priority', 0),
                'notify_matches': kwargs.get('notify_matches', True),
                'notify_goals': kwargs.get('notify_goals', True),
                'notify_transfers': kwargs.get('notify_transfers', False),
            }
        )
        
        if created:
            logger.info(f"User {user_id} favorited team {team.name}")
            cache.delete(f'user_favorites:{user_id}')
        
        return favorite, created
    
    @staticmethod
    @transaction.atomic
    def add_favorite_match(user_id, match_id, **kwargs):
        """Add a match to user favorites."""
        from .models import UserFavoriteMatch
        from matches.models import Match
        
        match = Match.objects.get(id=match_id)
        
        favorite, created = UserFavoriteMatch.objects.get_or_create(
            user_id=user_id,
            match_id=match_id,
            defaults={
                'notify_goals': kwargs.get('notify_goals', True),
                'notify_half_time': kwargs.get('notify_half_time', False),
                'notify_full_time': kwargs.get('notify_full_time', True),
            }
        )
        
        if created:
            logger.info(f"User {user_id} favorited match {match_id}")
            cache.delete(f'user_favorites:{user_id}')
        
        return favorite, created
    
    @staticmethod
    @transaction.atomic
    def add_favorite_competition(user_id, competition_id, **kwargs):
        """Add a competition to user favorites."""
        from .models import UserFavoriteCompetition
        from competitions.models import Competition
        
        competition = Competition.objects.get(id=competition_id)
        
        favorite, created = UserFavoriteCompetition.objects.get_or_create(
            user_id=user_id,
            competition_id=competition_id,
            defaults={
                'priority': kwargs.get('priority', 0),
            }
        )
        
        if created:
            logger.info(f"User {user_id} favorited competition {competition.name}")
            cache.delete(f'user_favorites:{user_id}')
        
        return favorite, created
    
    @staticmethod
    @transaction.atomic
    def remove_favorite_team(user_id, team_id):
        """Remove a team from user favorites."""
        from .models import UserFavoriteTeam
        
        deleted, _ = UserFavoriteTeam.objects.filter(
            user_id=user_id, team_id=team_id
        ).delete()
        
        if deleted:
            cache.delete(f'user_favorites:{user_id}')
            logger.info(f"User {user_id} unfavorited team {team_id}")
        
        return deleted > 0
    
    @staticmethod
    @transaction.atomic
    def remove_favorite_match(user_id, match_id):
        """Remove a match from user favorites."""
        from .models import UserFavoriteMatch
        
        deleted, _ = UserFavoriteMatch.objects.filter(
            user_id=user_id, match_id=match_id
        ).delete()
        
        if deleted:
            cache.delete(f'user_favorites:{user_id}')
        
        return deleted > 0
    
    @staticmethod
    @transaction.atomic
    def remove_favorite_competition(user_id, competition_id):
        """Remove a competition from user favorites."""
        from .models import UserFavoriteCompetition
        
        deleted, _ = UserFavoriteCompetition.objects.filter(
            user_id=user_id, competition_id=competition_id
        ).delete()
        
        if deleted:
            cache.delete(f'user_favorites:{user_id}')
        
        return deleted > 0
    
    @staticmethod
    def is_team_favorited(user_id, team_id):
        """Check if a team is in user's favorites."""
        from .models import UserFavoriteTeam
        
        return UserFavoriteTeam.objects.filter(
            user_id=user_id, team_id=team_id
        ).exists()
    
    @staticmethod
    def is_match_favorited(user_id, match_id):
        """Check if a match is in user's favorites."""
        from .models import UserFavoriteMatch
        
        return UserFavoriteMatch.objects.filter(
            user_id=user_id, match_id=match_id
        ).exists()
    
    @staticmethod
    def get_favorite_count(user_id):
        """Get total count of user's favorites."""
        from .models import UserFavoriteTeam, UserFavoriteMatch, UserFavoriteCompetition
        
        return {
            'teams': UserFavoriteTeam.objects.filter(user_id=user_id).count(),
            'matches': UserFavoriteMatch.objects.filter(user_id=user_id).count(),
            'competitions': UserFavoriteCompetition.objects.filter(user_id=user_id).count(),
        }
    
    @staticmethod
    def get_users_who_favorited_team(team_id):
        """Get users who favorited a specific team (for notifications)."""
        from .models import UserFavoriteTeam
        
        return list(
            UserFavoriteTeam.objects.filter(
                team_id=team_id,
                notify_matches=True
            ).values_list('user_id', flat=True)
        )
    
    @staticmethod
    def get_users_who_favorited_match(match_id):
        """Get users who favorited a specific match (for notifications)."""
        from .models import UserFavoriteMatch
        
        return list(
            UserFavoriteMatch.objects.filter(
                match_id=match_id
            ).values_list('user_id', flat=True)
        )
    
    # -- Private helper methods --
    
    @staticmethod
    def _get_team_next_match(team):
        """Get the next upcoming match for a team."""
        from matches.models import Match
        from django.utils import timezone
        
        next_match = Match.objects.filter(
            Q(home_team=team) | Q(away_team=team),
            status='scheduled',
            kickoff_time__gte=timezone.now()
        ).order_by('kickoff_time').first()
        
        if next_match:
            return {
                'match_id': str(next_match.id),
                'opponent': next_match.away_team.name if next_match.home_team == team else next_match.home_team.name,
                'kickoff_time': next_match.kickoff_time.isoformat(),
                'is_home': next_match.home_team == team,
            }
        return None
    
    @staticmethod
    def _get_team_live_match(team):
        """Get current live match for a team."""
        from matches.models import Match
        
        live_match = Match.objects.filter(
            Q(home_team=team) | Q(away_team=team),
            status__in=['live', 'half_time']
        ).first()
        
        if live_match:
            return {
                'match_id': str(live_match.id),
                'home_team': live_match.home_team.name,
                'away_team': live_match.away_team.name,
                'home_score': live_match.home_score,
                'away_score': live_match.away_score,
                'minute': live_match.minute,
            }
        return None
    
    @staticmethod
    def _get_current_season_info(competition):
        """Get current season info for a competition."""
        current = competition.seasons.filter(is_current=True).first()
        
        if current:
            return {
                'season_id': str(current.id),
                'name': current.name,
                'status': current.status,
            }
        return None