"""
Celery tasks for syncing football data from Free API.
"""
import logging
from celery import shared_task
from django.utils import timezone

# Django models
from players.models import Player
from teams.models import Team
from matches.models import Match
from competitions.models import Competition

# API service
from matches.services.external_api import free_football_api

# Setup logger
logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def sync_players_from_api(self, search_term: str = 'a'):
    """
    Sync players from Free Football API.
    Searches for players by initial letter.
    """
    logger.info(f"Syncing players matching '{search_term}' from API...")
    
    try:
        players_data = free_football_api.search_players(search_term)
        
        if not players_data:
            logger.info("No players found")
            return "No players found"
        
        created_count = 0
        updated_count = 0
        
        for player_data in players_data:
            try:
                # Get player data safely
                player_id = player_data.get('id')
                player_name = player_data.get('name', 'Unknown')
                player_nationality = player_data.get('nationality', '')
                player_position = player_data.get('position', '')
                player_jersey = player_data.get('jersey_number')
                team_name = player_data.get('team', '')
                
                if not player_id:
                    logger.warning(f"Skipping player without ID: {player_name}")
                    continue
                
                # Find or create team for the player (optional)
                team = None
                if team_name:
                    team, _ = Team.objects.get_or_create(
                        name=team_name,
                        defaults={
                            'team_type': 'club',
                            'is_active': True,
                        }
                    )
                
                # Create or update player
                player, created = Player.objects.update_or_create(
                    external_api_id=str(player_id),
                    defaults={
                        'full_name': player_name,
                        'nationality': player_nationality,
                        'position': player_position,
                        'jersey_number': player_jersey,
                        'current_team': team,
                        'is_active': True,
                    }
                )
                
                if created:
                    created_count += 1
                    logger.debug(f"Created player: {player.full_name}")
                else:
                    updated_count += 1
                    logger.debug(f"Updated player: {player.full_name}")
                    
            except Exception as e:
                logger.error(f"Error processing player {player_data.get('name', 'Unknown')}: {e}")
                continue
        
        logger.info(f"Sync complete: {created_count} created, {updated_count} updated")
        return f"Created: {created_count}, Updated: {updated_count}"
        
    except Exception as exc:
        logger.error(f"Error syncing players: {exc}")
        raise self.retry(exc=exc)


@shared_task(bind=True)
def sync_all_players(self):
    """Sync players for all letters of the alphabet."""
    import string
    results = []
    
    for letter in string.ascii_lowercase:
        result = sync_players_from_api.delay(letter)
        results.append(result)
        logger.info(f"Queued sync for letter: {letter}")
    
    return f"Queued sync for letters: {', '.join(string.ascii_lowercase)}"


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def sync_specific_player(self, player_name: str):
    """
    Sync a specific player by name.
    """
    logger.info(f"Syncing player: {player_name}")
    
    try:
        player_data = free_football_api.get_player_by_name(player_name)
        
        if not player_data:
            logger.info(f"Player not found: {player_name}")
            return f"Player not found: {player_name}"
        
        # Get player data
        player_id = player_data.get('id')
        player_full_name = player_data.get('name', player_name)
        player_nationality = player_data.get('nationality', '')
        player_position = player_data.get('position', '')
        player_jersey = player_data.get('jersey_number')
        team_name = player_data.get('team', '')
        
        # Find or create team
        team = None
        if team_name:
            team, _ = Team.objects.get_or_create(
                name=team_name,
                defaults={
                    'team_type': 'club',
                    'is_active': True,
                }
            )
        
        # Create or update player
        player, created = Player.objects.update_or_create(
            external_api_id=str(player_id),
            defaults={
                'full_name': player_full_name,
                'nationality': player_nationality,
                'position': player_position,
                'jersey_number': player_jersey,
                'current_team': team,
                'is_active': True,
            }
        )
        
        logger.info(f"{'Created' if created else 'Updated'} player: {player.full_name}")
        return f"{'Created' if created else 'Updated'}: {player.full_name}"
        
    except Exception as exc:
        logger.error(f"Error syncing player {player_name}: {exc}")
        raise self.retry(exc=exc)