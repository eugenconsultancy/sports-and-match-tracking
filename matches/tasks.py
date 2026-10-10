"""
Celery tasks for matches app.
"""
import json
import logging
from celery import shared_task
from django.utils import timezone
from django.db import transaction
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def fetch_live_matches(self):
    """
    Fetch live match data from external APIs and update database.
    This is a scheduled task running every 30 seconds.
    """
    from matches.models import Match, MatchLiveState, MatchEvent
    from matches.serializers import MatchDetailSerializer
    
    channel_layer = get_channel_layer()
    
    # Get all live matches
    live_matches = Match.objects.filter(
        status__in=[Match.Status.LIVE, Match.Status.HALF_TIME]
    ).select_related('home_team', 'away_team')
    
    updated_matches = []
    
    for match in live_matches:
        try:
            # In production, this would call external API
            # For now, simulate a data refresh
            match_data = _simulate_match_update(match)
            
            with transaction.atomic():
                # Update live state
                live_state, created = MatchLiveState.objects.get_or_create(
                    match=match,
                    defaults=match_data['live_state']
                )
                if not created:
                    for key, value in match_data['live_state'].items():
                        setattr(live_state, key, value)
                    live_state.save()
                
                # Update match scores
                if match_data.get('home_score') is not None:
                    match.home_score = match_data['home_score']
                if match_data.get('away_score') is not None:
                    match.away_score = match_data['away_score']
                if match_data.get('minute') is not None:
                    match.minute = match_data['minute']
                match.save()
                
                # Create new events if any
                for event_data in match_data.get('new_events', []):
                    MatchEvent.objects.create(
                        match=match,
                        **event_data
                    )
            
            # Publish update to Redis/WebSocket
            serialized = MatchDetailSerializer(match).data
            
            # Send to specific match channel
            async_to_sync(channel_layer.group_send)(
                f'match_{match.id}',
                {
                    'type': 'match_update',
                    'data': serialized
                }
            )
            
            # Send live state update
            async_to_sync(channel_layer.group_send)(
                f'match_{match.id}',
                {
                    'type': 'live_state_update',
                    'data': match_data['live_state']
                }
            )
            
            updated_matches.append(str(match.id))
            
        except Exception as exc:
            logger.error(f"Error updating match {match.id}: {exc}")
            continue
    
    # Broadcast live matches summary
    if updated_matches:
        from matches.serializers import MatchListSerializer
        all_live = Match.objects.filter(
            status__in=[Match.Status.LIVE, Match.Status.HALF_TIME]
        ).select_related('home_team', 'away_team', 'competition_season__competition')
        
        live_list = MatchListSerializer(all_live, many=True).data
        
        async_to_sync(channel_layer.group_send)(
            'live_matches',
            {
                'type': 'live_matches_update',
                'data': live_list
            }
        )
    
    return f"Updated {len(updated_matches)} live matches"


@shared_task(bind=True, max_retries=3)
def sync_external_fixtures(self, competition_id=None):
    """
    Sync fixtures from external APIs.
    Runs hourly or on-demand.
    """
    from competitions.models import Competition, Season
    from matches.models import Match, MatchStats
    from teams.models import Team
    
    # In production, this would call external APIs like:
    # - Sportradar
    # - Opta
    # - API-Football
    
    competitions = Competition.objects.filter(is_active=True)
    if competition_id:
        competitions = competitions.filter(id=competition_id)
    
    synced_count = 0
    
    for competition in competitions:
        try:
            current_season = competition.seasons.filter(is_current=True).first()
            if not current_season:
                continue
            
            # Fetch fixtures from external API (simulated)
            # api_client = ExternalAPIClient()
            # fixtures = api_client.get_fixtures(competition.external_api_id, current_season.external_api_id)
            
            # Process fixtures
            # for fixture in fixtures:
            #     home_team = Team.objects.get(external_api_id=fixture['home_team_id'])
            #     away_team = Team.objects.get(external_api_id=fixture['away_team_id'])
            #     Match.objects.update_or_create(
            #         external_api_id=fixture['id'],
            #         defaults={...}
            #     )
            #     synced_count += 1
            
        except Exception as exc:
            logger.error(f"Error syncing fixtures for {competition.name}: {exc}")
            continue
    
    return f"Synced {synced_count} fixtures"


def _simulate_match_update(match):
    """
    Simulate live match data updates.
    In production, this would be replaced with real API data.
    """
    from matches.models import MatchLiveState
    import random
    
    # Get or create live state
    live_state, _ = MatchLiveState.objects.get_or_create(
        match=match,
        defaults={
            'current_minute': 0,
            'home_score': match.home_score or 0,
            'away_score': match.away_score or 0,
            'attacks': [],
            'dangerous_attacks': [],
            'momentum': 'balanced',
            'last_events': [],
            'possession': {'home': 50, 'away': 50},
            'match_status': match.status,
        }
    )
    
    # Randomly update possession
    home_possession = random.randint(35, 65)
    away_possession = 100 - home_possession
    live_state.possession = {'home': home_possession, 'away': away_possession}
    
    # Randomly add attacks
    if random.random() < 0.3:
        attacks = live_state.attacks or []
        attacks.append({
            'team': random.choice(['home', 'away']),
            'minute': live_state.current_minute,
            'description': f"Attack at {live_state.current_minute}'"
        })
        live_state.attacks = attacks[-5:]  # Keep last 5
    
    # Update momentum
    if home_possession > 55:
        live_state.momentum = 'home'
    elif away_possession > 55:
        live_state.momentum = 'away'
    else:
        live_state.momentum = 'balanced'
    
    live_state.current_minute += 1
    live_state.save()
    
    return {
        'live_state': {
            'current_minute': live_state.current_minute,
            'home_score': match.home_score,
            'away_score': match.away_score,
            'attacks': live_state.attacks,
            'dangerous_attacks': live_state.dangerous_attacks,
            'momentum': live_state.momentum,
            'last_events': live_state.last_events,
            'possession': live_state.possession,
            'match_status': match.status,
        },
        'home_score': match.home_score,
        'away_score': match.away_score,
        'minute': live_state.current_minute,
        'new_events': [],
    }