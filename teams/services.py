"""
Service layer for teams app.
Contains business logic for team operations.
"""
import logging
from django.db.models import Q, Sum, Count, F
from django.core.cache import cache

logger = logging.getLogger(__name__)


class TeamService:
    """Service class for team-related business logic."""
    
    @staticmethod
    def get_team_form(team, last_n=5):
        """Get the form of a team over the last N matches."""
        from matches.models import Match
        
        recent_matches = Match.objects.filter(
            Q(home_team=team) | Q(away_team=team),
            status='finished'
        ).order_by('-kickoff_time')[:last_n]
        
        form = []
        for match in recent_matches:
            if match.home_team == team:
                if match.home_score > match.away_score:
                    form.append('W')
                elif match.home_score == match.away_score:
                    form.append('D')
                else:
                    form.append('L')
            else:
                if match.away_score > match.home_score:
                    form.append('W')
                elif match.away_score == match.home_score:
                    form.append('D')
                else:
                    form.append('L')
        
        return ''.join(form)
    
    @staticmethod
    def get_head_to_head(team1_id, team2_id, limit=10):
        """Get head-to-head record between two teams."""
        from matches.models import Match
        
        matches = Match.objects.filter(
            (Q(home_team_id=team1_id) & Q(away_team_id=team2_id)) |
            (Q(home_team_id=team2_id) & Q(away_team_id=team1_id)),
            status='finished'
        ).order_by('-kickoff_time')[:limit]
        
        return list(matches)
    
    @staticmethod
    def get_team_season_stats(team_id, season_id):
        """Get comprehensive team statistics for a season."""
        from matches.models import Match, MatchStats
        
        stats = {
            'matches_played': 0,
            'wins': 0,
            'draws': 0,
            'losses': 0,
            'goals_scored': 0,
            'goals_conceded': 0,
            'clean_sheets': 0,
            'failed_to_score': 0,
            'avg_possession': 0,
            'home_record': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0},
            'away_record': {'played': 0, 'wins': 0, 'draws': 0, 'losses': 0},
        }
        
        matches = Match.objects.filter(
            Q(home_team_id=team_id) | Q(away_team_id=team_id),
            competition_season_id=season_id,
            status='finished'
        )
        
        for match in matches:
            stats['matches_played'] += 1
            is_home = match.home_team_id == team_id
            
            team_goals = match.home_score if is_home else match.away_score
            opponent_goals = match.away_score if is_home else match.home_score
            
            stats['goals_scored'] += team_goals
            stats['goals_conceded'] += opponent_goals
            
            if team_goals > opponent_goals:
                stats['wins'] += 1
                if is_home:
                    stats['home_record']['wins'] += 1
                else:
                    stats['away_record']['wins'] += 1
            elif team_goals == opponent_goals:
                stats['draws'] += 1
                if is_home:
                    stats['home_record']['draws'] += 1
                else:
                    stats['away_record']['draws'] += 1
            else:
                stats['losses'] += 1
                if is_home:
                    stats['home_record']['losses'] += 1
                else:
                    stats['away_record']['losses'] += 1
            
            if opponent_goals == 0:
                stats['clean_sheets'] += 1
            if team_goals == 0:
                stats['failed_to_score'] += 1
            
            if is_home:
                stats['home_record']['played'] += 1
            else:
                stats['away_record']['played'] += 1
        
        # Calculate average possession from match stats
        possessions = MatchStats.objects.filter(
            match__in=matches, team_id=team_id
        ).aggregate(avg=Avg('possession_percentage'))
        
        if possessions['avg']:
            stats['avg_possession'] = round(float(possessions['avg']), 1)
        
        return stats
    
    @staticmethod
    def search_teams(query, limit=10):
        """Search teams by name or country."""
        from .models import Team
        
        return Team.objects.filter(
            Q(name__icontains=query) |
            Q(short_name__icontains=query) |
            Q(country__icontains=query)
        ).filter(is_active=True)[:limit]
    
    @staticmethod
    def get_top_scorers(team_id, season_id=None, limit=5):
        """Get top goal scorers for a team."""
        from players.models import PlayerMatchStats
        
        filters = {'team_id': team_id}
        if season_id:
            filters['match__competition_season_id'] = season_id
        
        top_scorers = PlayerMatchStats.objects.filter(
            **filters
        ).values(
            'player_id', 'player__full_name'
        ).annotate(
            total_goals=Sum('goals')
        ).order_by('-total_goals')[:limit]
        
        return list(top_scorers)


from django.db.models import Avg