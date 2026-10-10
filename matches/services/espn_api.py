"""
ESPN API Integration - Free, No API Key Required
Using ESPNs public endpoints.
"""
import requests
import logging
from typing import Dict, List, Optional
from django.core.cache import cache
from datetime import datetime

logger = logging.getLogger(__name__)


class ESPNAPiService:
    """Service for ESPN Public API - Free, no authentication needed."""
    
    def __init__(self):
        self.base_url = 'https://site.api.espn.com/apis/site/v2/sports'
        self.timeout = 30
        
    def _make_request(self, url: str) -> Optional[Dict]:
        """Make API request to ESPN."""
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"API request failed: {e}")
            return None
    
    def get_live_scores(self, sport: str = 'soccer') -> List[Dict]:
        """Get live football/soccer scores from ESPN."""
        cache_key = f'espn:live:{sport}'
        cached = cache.get(cache_key)
        
        if cached:
            return cached
        
        # ESPN Soccer scoreboard endpoint (public, no key needed)
        url = f"{self.base_url}/soccer/scoreboard"
        data = self._make_request(url)
        
        matches = []
        if data:
            events = data.get('events', [])
            for event in events:
                match = self._parse_match(event)
                if match:
                    matches.append(match)
            
            cache.set(cache_key, matches, 30)  # Cache for 30 seconds
            logger.info(f"Fetched {len(matches)} live {sport} matches from ESPN")
        
        return matches
    
    def search_teams(self, query: str, sport: str = 'soccer') -> List[Dict]:
        """Search for teams by name."""
        # ESPN doesn't have a direct search endpoint, return empty for now
        logger.info(f"Team search for '{query}' not available in ESPN free API")
        return []
    
    def _parse_match(self, event: Dict) -> Optional[Dict]:
        """Parse match data from ESPN response."""
        try:
            competitions = event.get('competitions', [])
            if not competitions:
                return None
            
            comp = competitions[0]
            competitors = comp.get('competitors', [])
            
            if len(competitors) < 2:
                return None
            
            # Find home and away teams
            home_team = None
            away_team = None
            
            for team in competitors:
                if team.get('homeaway') == 'home':
                    home_team = team
                elif team.get('homeaway') == 'away':
                    away_team = team
            
            # If not found by homeaway, take first as home, second as away
            if not home_team:
                home_team = competitors[0]
            if not away_team and len(competitors) > 1:
                away_team = competitors[1]
            
            # Get status
            status = comp.get('status', {})
            status_type = status.get('type', {}).get('name', 'STATUS_SCHEDULED')
            
            # Map status
            if status_type in ['STATUS_IN_PROGRESS', 'STATUS_HALFTIME']:
                match_status = 'live'
            elif status_type == 'STATUS_FINAL':
                match_status = 'finished'
            else:
                match_status = 'scheduled'
            
            # Get minute/clock
            display_clock = status.get('displayClock', '0')
            minute = 0
            if display_clock and str(display_clock).isdigit():
                minute = int(display_clock)
            
            return {
                'id': event.get('id'),
                'home_team': home_team.get('team', {}).get('displayName', 'Home') if home_team else 'Home',
                'away_team': away_team.get('team', {}).get('displayName', 'Away') if away_team else 'Away',
                'home_score': int(home_team.get('score', 0)) if home_team else 0,
                'away_score': int(away_team.get('score', 0)) if away_team else 0,
                'status': match_status,
                'minute': minute,
                'competition': event.get('league', {}).get('name', 'Unknown'),
                'venue': comp.get('venue', {}).get('fullName'),
                'kickoff_time': event.get('date'),
            }
        except Exception as e:
            logger.error(f"Error parsing match: {e}")
            return None


# Create singleton instance
espn_api = ESPNAPiService()