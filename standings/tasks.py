"""
Celery tasks for standings app.
"""
import logging
from celery import shared_task
from django.db import transaction
from django.db.models import Sum, Count, Q, F
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def update_all_standings(self):
    """
    Update all standings tables.
    Runs every 5 minutes.
    """
    from competitions.models import Season
    from standings.models import Standing
    
    # Get all live standings
    standings = Standing.objects.filter(is_live=True)
    
    updated_count = 0
    for standing in standings:
        try:
            _update_standing_table(standing)
            updated_count += 1
        except Exception as exc:
            logger.error(f"Error updating standing {standing.id}: {exc}")
            continue
    
    return f"Updated {updated_count} standings tables"


@shared_task(bind=True, max_retries=3)
def update_standing_for_match(self, match_id):
    """
    Update standings affected by a specific match result.
    """
    from matches.models import Match
    from standings.models import Standing, TeamStanding
    
    try:
        match = Match.objects.select_related(
            'competition_season', 'stage', 'group', 'home_team', 'away_team'
        ).get(id=match_id)
        
        # Find relevant standings
        standings = Standing.objects.filter(
            competition_season=match.competition_season,
            stage=match.stage,
            group=match.group,
        )
        
        for standing in standings:
            _update_standing_table(standing)
        
        return f"Updated standings for match {match_id}"
        
    except Match.DoesNotExist:
        logger.error(f"Match {match_id} not found")
        return f"Match {match_id} not found"
    except Exception as exc:
        logger.error(f"Error updating standings for match {match_id}: {exc}")
        raise


def _update_standing_table(standing):
    """
    Core logic to calculate standings from match results.
    """
    from matches.models import Match
    from standings.models import TeamStanding
    from teams.models import Team
    
    # Get all matches for this standing's scope
    matches_query = Match.objects.filter(
        competition_season=standing.competition_season,
        stage=standing.stage,
        status=Match.Status.FINISHED,
    )
    
    if standing.group:
        matches_query = matches_query.filter(group=standing.group)
    
    # Get teams in this standing
    if standing.group:
        teams = standing.group.teams.all()
    else:
        # For league stages, get all participating teams
        teams = Team.objects.filter(
            Q(home_matches__in=matches_query) | Q(away_matches__in=matches_query)
        ).distinct()
    
    with transaction.atomic():
        # Remove existing entries
        TeamStanding.objects.filter(standing=standing).delete()
        
        for team in teams:
            # Calculate stats
            home_matches = matches_query.filter(home_team=team)
            away_matches = matches_query.filter(away_team=team)
            
            # Home record
            home_played = home_matches.count()
            home_wins = home_matches.filter(home_score__gt=F('away_score')).count()
            home_draws = home_matches.filter(home_score=F('away_score')).count()
            home_losses = home_matches.filter(home_score__lt=F('away_score')).count()
            home_goals_for = home_matches.aggregate(total=Sum('home_score'))['total'] or 0
            home_goals_against = home_matches.aggregate(total=Sum('away_score'))['total'] or 0
            
            # Away record
            away_played = away_matches.count()
            away_wins = away_matches.filter(away_score__gt=F('home_score')).count()
            away_draws = away_matches.filter(away_score=F('home_score')).count()
            away_losses = away_matches.filter(away_score__lt=F('home_score')).count()
            away_goals_for = away_matches.aggregate(total=Sum('away_score'))['total'] or 0
            away_goals_against = away_matches.aggregate(total=Sum('home_score'))['total'] or 0
            
            # Totals
            played = home_played + away_played
            wins = home_wins + away_wins
            draws = home_draws + away_draws
            losses = home_losses + away_losses
            goals_for = home_goals_for + away_goals_for
            goals_against = home_goals_against + away_goals_against
            goal_difference = goals_for - goals_against
            points = (wins * 3) + draws
            
            # Form (last 5 matches)
            all_team_matches = matches_query.filter(
                Q(home_team=team) | Q(away_team=team)
            ).order_by('-kickoff_time')[:5]
            
            form = ''
            for m in all_team_matches:
                if m.home_team == team:
                    if m.home_score > m.away_score:
                        form += 'W'
                    elif m.home_score == m.away_score:
                        form += 'D'
                    else:
                        form += 'L'
                else:
                    if m.away_score > m.home_score:
                        form += 'W'
                    elif m.away_score == m.home_score:
                        form += 'D'
                    else:
                        form += 'L'
            
            TeamStanding.objects.create(
                standing=standing,
                team=team,
                position=0,  # Will be calculated after sorting
                played=played,
                wins=wins,
                draws=draws,
                losses=losses,
                goals_for=goals_for,
                goals_against=goals_against,
                goal_difference=goal_difference,
                points=points,
                home_played=home_played,
                home_wins=home_wins,
                home_draws=home_draws,
                home_losses=home_losses,
                home_goals_for=home_goals_for,
                home_goals_against=home_goals_against,
                away_played=away_played,
                away_wins=away_wins,
                away_draws=away_draws,
                away_losses=away_losses,
                away_goals_for=away_goals_for,
                away_goals_against=away_goals_against,
                form=form,
            )
        
        # Recalculate positions (sort by points, goal difference, goals for)
        entries = TeamStanding.objects.filter(standing=standing).order_by(
            '-points', '-goal_difference', '-goals_for'
        )
        for idx, entry in enumerate(entries, 1):
            entry.position = idx
            entry.save(update_fields=['position'])
        
        # Update last_calculated timestamp
        standing.last_calculated = timezone.now()
        standing.save(update_fields=['last_calculated'])