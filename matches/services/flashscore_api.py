"""
FlashScore API Integration via RapidAPI
Using your existing API key for flashscore4.p.rapidapi.com
"""
import requests
import logging
from typing import Dict, List, Optional
from django.core.cache import cache
from datetime import datetime
import time

logger = logging.getLogger(__name__)


class FlashScoreAPIService:
    """Service for FlashScore API via RapidAPI."""
    
    def __init__(self):
        self.base_url = 'https://flashscore4.p.rapidapi.com'
        self.api_key = '7c4dcee121mshc65a1468dbddbb0p1ecfe4jsn518676c350d8'
        self.host = 'flashscore4.p.rapidapi.com'
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
    
    def search(self, query: str) -> List[Dict]:
        """Search for teams, players, or competitions."""
        cache_key = f'flashscore:search:{query}'
        cached = cache.get(cache_key)
        
        if cached:
            return cached
        
        params = {'q': query}
        data = self._make_request('/api/flashscore/v2/general/search', params)
        
        results = []
        if data:
            results = self._parse_search_results(data)
            cache.set(cache_key, results, 3600)
            logger.info(f"Search for '{query}' returned {len(results)} results")
        
        return results
    
    def get_live_scores(self) -> List[Dict]:
        """Get live football scores."""
        cache_key = 'flashscore:live'
        cached = cache.get(cache_key)
        
        if cached:
            return cached
        
        data = self._make_request('/api/flashscore/v2/scores/live')
        
        matches = []
        if data:
            matches = self._parse_matches(data)
            cache.set(cache_key, matches, 30)
            logger.info(f"Fetched {len(matches)} live matches")
        
        return matches
    
    def get_fixtures(self, date: str = None) -> List[Dict]:
        """Get fixtures for a specific date."""
        if not date:
            date = datetime.now().strftime('%Y-%m-%d')
        
        cache_key = f'flashscore:fixtures:{date}'
        cached = cache.get(cache_key)
        
        if cached:
            return cached
        
        params = {'date': date}
        data = self._make_request('/api/flashscore/v2/scores/fixtures', params)
        
        matches = []
        if data:
            matches = self._parse_matches(data)
            cache.set(cache_key, matches, 3600)
        
        return matches
    
    def get_match_details(self, match_id: str) -> Optional[Dict]:
        """Get detailed information for a specific match."""
        cache_key = f'flashscore:match:{match_id}'
        cached = cache.get(cache_key)
        
        if cached:
            return cached
        
        params = {'id': match_id}
        data = self._make_request('/api/flashscore/v2/match/details', params)
        
        if data:
            cache.set(cache_key, data, 300)
            return data
        
        return None
    
    def get_team_info(self, team_id: str) -> Optional[Dict]:
        """Get detailed information for a specific team."""
        cache_key = f'flashscore:team:{team_id}'
        cached = cache.get(cache_key)
        
        if cached:
            return cached
        
        params = {'id': team_id}
        data = self._make_request('/api/flashscore/v2/team/details', params)
        
        if data:
            cache.set(cache_key, data, 86400)
            return data
        
        return None
    
    def get_standings(self, tournament_id: str) -> List[Dict]:
        """Get league standings."""
        cache_key = f'flashscore:standings:{tournament_id}'
        cached = cache.get(cache_key)
        
        if cached:
            return cached
        
        params = {'id': tournament_id}
        data = self._make_request('/api/flashscore/v2/tournament/standings', params)
        
        standings = []
        if data:
            standings = self._parse_standings(data)
            cache.set(cache_key, standings, 7200)
        
        return standings
    
    def _parse_search_results(self, data: Dict) -> List[Dict]:
        """Parse search results from API response."""
        results = []
        
        teams = data.get('teams', []) or data.get('team', [])
        for team in teams:
            results.append({
                'type': 'team',
                'id': team.get('id'),
                'name': team.get('name'),
                'country': team.get('country'),
                'logo': team.get('logo'),
            })
        
        players = data.get('players', []) or data.get('player', [])
        for player in players:
            results.append({
                'type': 'player',
                'id': player.get('id'),
                'name': player.get('name'),
                'nationality': player.get('nationality'),
                'team': player.get('teamName'),
            })
        
        competitions = data.get('tournaments', []) or data.get('competitions', [])
        for comp in competitions:
            results.append({
                'type': 'competition',
                'id': comp.get('id'),
                'name': comp.get('name'),
                'country': comp.get('country'),
            })
        
        return results
    
    def _parse_matches(self, data: Dict) -> List[Dict]:
        """Parse matches from API response."""
        matches = []
        events = data.get('events', []) or data.get('matches', []) or data.get('data', [])
        
        for event in events:
            match = {
                'id': event.get('id') or event.get('eventId'),
                'home_team': self._get_team_name(event, 'home'),
                'away_team': self._get_team_name(event, 'away'),
                'home_score': self._get_score(event, 'home'),
                'away_score': self._get_score(event, 'away'),
                'status': event.get('status', 'scheduled'),
                'minute': event.get('minute', 0) or event.get('time', 0),
                'competition': event.get('tournamentName') or event.get('leagueName'),
                'venue': event.get('stadiumName'),
                'kickoff_time': event.get('startDate') or event.get('date'),
            }
            matches.append(match)
        
        return matches
    
    def _get_team_name(self, event: Dict, side: str) -> str:
        """Extract team name from event data."""
        if side == 'home':
            return event.get('homeTeamName') or event.get('homeTeam', {}).get('name', 'Home')
        else:
            return event.get('awayTeamName') or event.get('awayTeam', {}).get('name', 'Away')
    
    def _get_score(self, event: Dict, side: str) -> int:
        """Extract score from event data."""
        if side == 'home':
            return int(event.get('homeScore', 0))
        else:
            return int(event.get('awayScore', 0))
    
    def _parse_standings(self, data: Dict) -> List[Dict]:
        """Parse standings from API response."""
        standings = []
        table = data.get('table', []) or data.get('standings', [])
        
        for row in table:
            standings.append({
                'position': row.get('position') or row.get('rank'),
                'team_id': row.get('teamId'),
                'team_name': row.get('teamName'),
                'played': row.get('played') or row.get('matches'),
                'wins': row.get('wins'),
                'draws': row.get('draws'),
                'losses': row.get('losses'),
                'goals_for': row.get('goalsFor') or row.get('goals'),
                'goals_against': row.get('goalsAgainst'),
                'goal_difference': row.get('goalDifference'),
                'points': row.get('points'),
            })
        
        return standings


# Singleton instance
flashscore_api = FlashScoreAPIService()