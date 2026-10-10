"""
Service layer for standings app.
Contains business logic for standings calculation.
"""
import logging
from django.db import transaction
from django.db.models import Q, Sum, Count, F, Case, When, IntegerField
from django.utils import timezone
from collections import defaultdict

logger = logging.getLogger(__name__)


class StandingsService:
    """Service class for standings-related business logic."""
    
    @staticmethod
    @transaction.atomic
    def calculate_standings(standing_id):
        """
        Calculate standings table from match results.
        This is the core algorithm used by the Celery task.
        """
        from .models import Standing, TeamStanding
        from matches.models import Match
        
        standing = Standing.objects.select_related(
            'competition_season', 'stage', 'group'
        ).get(id=standing_id)
        
        # Get all finished matches for this scope
        matches = Match.objects.filter(
            competition_season=standing.competition_season,
            stage=standing.stage,
            status='finished'
        )
        
        if standing.group:
            matches = matches.filter(group=standing.group)
        
        # Get unique teams
        team_ids = set()
        for match in matches:
            team_ids.add(match.home_team_id)
            team_ids.add(match.away_team_id)
        
        # Clear existing standings
        TeamStanding.objects.filter(standing=standing).delete()
        
        # Calculate per team
        team_stats = defaultdict(lambda: {
            'played': 0, 'wins': 0, 'draws': 0, 'losses': 0,
            'goals_for': 0, 'goals_against': 0,
            'home_played': 0, 'home_wins': 0, 'home_draws': 0, 'home_losses': 0,
            'home_goals_for': 0, 'home_goals_against': 0,
            'away_played': 0, 'away_wins': 0, 'away_draws': 0, 'away_losses': 0,
            'away_goals_for': 0, 'away_goals_against': 0,
            'clean_sheets': 0, 'failed_to_score': 0,
            'results': [],
        })
        
        for match in matches:
            # Home team stats
            home = team_stats[match.home_team_id]
            home['played'] += 1
            home['home_played'] += 1
            home['goals_for'] += match.home_score
            home['goals_against'] += match.away_score
            home['home_goals_for'] += match.home_score
            home['home_goals_against'] += match.away_score
            
            # Away team stats
            away = team_stats[match.away_team_id]
            away['played'] += 1
            away['away_played'] += 1
            away['goals_for'] += match.away_score
            away['goals_against'] += match.home_score
            away['away_goals_for'] += match.away_score
            away['away_goals_against'] += match.home_score
            
            # Determine result
            if match.home_score > match.away_score:
                home['wins'] += 1
                home['home_wins'] += 1
                away['losses'] += 1
                away['away_losses'] += 1
                home['results'].append('W')
                away['results'].append('L')
            elif match.home_score == match.away_score:
                home['draws'] += 1
                home['home_draws'] += 1
                away['draws'] += 1
                away['away_draws'] += 1
                home['results'].append('D')
                away['results'].append('D')
            else:
                home['losses'] += 1
                home['home_losses'] += 1
                away['wins'] += 1
                away['away_wins'] += 1
                home['results'].append('L')
                away['results'].append('W')
            
            # Clean sheets
            if match.away_score == 0:
                home['clean_sheets'] += 1
            if match.home_score == 0:
                away['clean_sheets'] += 1
            
            # Failed to score
            if match.home_score == 0:
                home['failed_to_score'] += 1
            if match.away_score == 0:
                away['failed_to_score'] += 1
        
        # Create team standing entries
        entries = []
        for team_id, stats in team_stats.items():
            points = (stats['wins'] * 3) + stats['draws']
            goal_diff = stats['goals_for'] - stats['goals_against']
            
            # Get form from last 5 results
            form = ''.join(stats['results'][-5:]) if stats['results'] else ''
            
            entries.append(TeamStanding(
                standing=standing,
                team_id=team_id,
                position=0,
                played=stats['played'],
                wins=stats['wins'],
                draws=stats['draws'],
                losses=stats['losses'],
                goals_for=stats['goals_for'],
                goals_against=stats['goals_against'],
                goal_difference=goal_diff,
                points=points,
                home_played=stats['home_played'],
                home_wins=stats['home_wins'],
                home_draws=stats['home_draws'],
                home_losses=stats['home_losses'],
                home_goals_for=stats['home_goals_for'],
                home_goals_against=stats['home_goals_against'],
                away_played=stats['away_played'],
                away_wins=stats['away_wins'],
                away_draws=stats['away_draws'],
                away_losses=stats['away_losses'],
                away_goals_for=stats['away_goals_for'],
                away_goals_against=stats['away_goals_against'],
                form=form,
                clean_sheets=stats['clean_sheets'],
                failed_to_score=stats['failed_to_score'],
            ))
        
        # Bulk create
        TeamStanding.objects.bulk_create(entries)
        
        # Calculate & assign positions
        all_entries = TeamStanding.objects.filter(standing=standing).order_by(
            '-points', '-goal_difference', '-goals_for', '-wins'
        )
        
        position = 1
        for entry in all_entries:
            entry.position = position
            entry.save(update_fields=['position'])
            position += 1
        
        # Update standing timestamp
        standing.last_calculated = timezone.now()
        standing.save(update_fields=['last_calculated'])
        
        logger.info(f"Calculated standings for {standing}")
        return standing
    
    @staticmethod
    def get_promotion_relegation_zones(standing_id):
        """Get promotion and relegation zone markers."""
        from .models import Standing
        
        standing = Standing.objects.get(id=standing_id)
        competition = standing.competition_season.competition
        
        # Get competition rules
        rules = competition.standing_rules.filter(is_active=True)
        
        zones = {
            'promotion_zone': 0,
            'promotion_playoff_zone': 0,
            'relegation_playoff_zone': 0,
            'relegation_zone': 0,
        }
        
        # Default zone sizes (could be configurable)
        total_teams = standing.team_standings.count()
        
        if standing.standing_type == 'total':
            zones['promotion_zone'] = min(2, total_teams)
            zones['relegation_zone'] = max(total_teams - 2, 0)
        
        return zones