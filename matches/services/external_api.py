"""
External API integration for Free Live Football Data API.
Working version with proper error handling.
"""
import requests
import logging
from typing import Dict, List, Optional
from django.core.cache import cache
import time

logger = logging.getLogger(__name__)


class FreeFootballAPIService:
    """Service for interacting with Free Live Football Data API."""
    
    def __init__(self):
        self.base_url = 'https://free-api-live-football-data.p.rapidapi.com'
        self.api_key = '7c4dcee121mshc65a1468dbddbb0p1ecfe4jsn518676c350d8'
        self.host = 'free-api-live-football-data.p.rapidapi.com'
        self.timeout = 30
        self.max_retries = 3
        
    def _make_request(self, endpoint: str, params: Dict = None, retry_count: int = 0) -> Optional[Dict]:
        """Make API request with retry logic."""
        headers = {
            'X-RapidAPI-Key': self.api_key,
            'X-RapidAPI-Host': self.host,
            'Content-Type': 'application/json'
        }
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = requests.get(
                url, 
                headers=headers, 
                params=params, 
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            if retry_count < self.max_retries:
                time.sleep(2 ** retry_count)
                return self._make_request(endpoint, params, retry_count + 1)
            return None
    
    def search_players(self, search_term: str) -> List[Dict]:
        """Search for football players by name."""
        cache_key = f'api:players_search:{search_term}'
        cached = cache.get(cache_key)
        
        if cached:
            return cached
        
        params = {'search': search_term}
        data = self._make_request('/football-players-search', params)
        
        players = []
        if data and isinstance(data, list):
            for player in data:
                players.append({
                    'id': player.get('player_id'),
                    'name': player.get('player_name'),
                    'team': player.get('team_name'),
                    'team_id': player.get('team_id'),
                    'nationality': player.get('nationality'),
                    'position': player.get('position'),
                    'age': player.get('age'),
                    'jersey_number': player.get('jersey_number'),
                    'image_url': player.get('image_url'),
                })
            
            cache.set(cache_key, players, 3600)  # Cache for 1 hour
            logger.info(f"Found {len(players)} players matching '{search_term}'")
        
        return players
    
    def get_player_by_name(self, name: str) -> Optional[Dict]:
        """Get player details by searching for exact name."""
        players = self.search_players(name)
        
        # Try to find exact match
        for player in players:
            if player.get('name', '').lower() == name.lower():
                return player
        
        # Return first result if available
        return players[0] if players else None


# Singleton instance
free_football_api = FreeFootballAPIService()