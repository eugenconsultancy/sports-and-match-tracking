"""
Redis pub/sub listener for the FastAPI real-time service.
Listens for events published by Django/Celery and forwards them to WebSocket clients.
"""
import asyncio
import json
import logging
from typing import Optional
import redis.asyncio as aioredis

logger = logging.getLogger(__name__)


class RedisListener:
    """
    Listens to Redis pub/sub channels and processes messages
    for real-time WebSocket delivery.
    """
    
    def __init__(self, redis_url: str = "redis://127.0.0.1:6379/2"):
        self.redis_url = redis_url
        self.redis_client: Optional[aioredis.Redis] = None
        self.pubsub: Optional[aioredis.client.PubSub] = None
        self.is_running = False
        self.handlers = {}
        self.connection_manager = None
    
    def set_connection_manager(self, manager):
        """Set the WebSocket connection manager for broadcasting."""
        self.connection_manager = manager
    
    def register_handler(self, channel_pattern: str, handler):
        """Register a handler for a specific channel pattern."""
        self.handlers[channel_pattern] = handler
    
    async def connect(self):
        """Connect to Redis and start listening."""
        try:
            self.redis_client = aioredis.from_url(
                self.redis_url,
                encoding="utf-8",
                decode_responses=True
            )
            
            # Test connection
            await self.redis_client.ping()
            
            self.pubsub = self.redis_client.pubsub()
            self.is_running = True
            
            logger.info(f"Connected to Redis at {self.redis_url}")
            
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    async def subscribe(self, *channels):
        """Subscribe to Redis channels."""
        if not self.pubsub:
            raise RuntimeError("Not connected to Redis")
        
        await self.pubsub.subscribe(*channels)
        logger.info(f"Subscribed to channels: {channels}")
    
    async def psubscribe(self, *patterns):
        """Subscribe to Redis channel patterns."""
        if not self.pubsub:
            raise RuntimeError("Not connected to Redis")
        
        await self.pubsub.psubscribe(*patterns)
        logger.info(f"Subscribed to patterns: {patterns}")
    
    async def listen(self):
        """
        Main listening loop.
        Processes messages and routes them to appropriate handlers.
        """
        if not self.pubsub:
            raise RuntimeError("Not connected to Redis")
        
        logger.info("Starting Redis listener loop...")
        
        async for message in self.pubsub.listen():
            if not self.is_running:
                break
            
            try:
                await self._process_message(message)
            except Exception as e:
                logger.error(f"Error processing message: {e}")
    
    async def _process_message(self, message: dict):
        """Process a single Redis message."""
        # Skip subscription confirmations
        if message["type"] not in ("message", "pmessage"):
            return
        
        channel = message.get("channel", "")
        
        # Try to parse data as JSON
        try:
            data = json.loads(message["data"])
        except (json.JSONDecodeError, TypeError):
            data = message["data"]
        
        # Route to specific handlers based on channel
        if channel.startswith("match_") and self.connection_manager:
            await self._handle_match_update(channel, data)
        
        elif channel == "live_matches" and self.connection_manager:
            await self._handle_live_matches_update(data)
        
        elif channel.startswith("poll_") and self.connection_manager:
            await self._handle_poll_update(channel, data)
        
        elif channel.startswith("competition_") and self.connection_manager:
            await self._handle_competition_update(channel, data)
        
        elif channel.startswith("notification_") and self.connection_manager:
            await self._handle_notification(channel, data)
        
        # Call custom handlers if registered
        for pattern, handler in self.handlers.items():
            if self._channel_matches_pattern(channel, pattern):
                await handler(channel, data)
    
    async def _handle_match_update(self, channel: str, data: dict):
        """Forward match updates to WebSocket clients."""
        match_id = channel.replace("match_", "")
        
        await self.connection_manager.broadcast(
            f"match_{match_id}",
            data
        )
    
    async def _handle_live_matches_update(self, data):
        """Forward live matches summary to WebSocket clients."""
        await self.connection_manager.broadcast(
            "live_matches",
            {
                "type": "live_matches_update",
                "data": data if isinstance(data, dict) else {"matches": data}
            }
        )
    
    async def _handle_poll_update(self, channel: str, data: dict):
        """Forward poll updates to WebSocket clients."""
        await self.connection_manager.broadcast(channel, data)
    
    async def _handle_competition_update(self, channel: str, data: dict):
        """Forward competition updates (standings, etc.) to WebSocket clients."""
        await self.connection_manager.broadcast(channel, data)
    
    async def _handle_notification(self, channel: str, data: dict):
        """Forward notifications to specific user channels."""
        user_id = data.get("user_id")
        if user_id:
            await self.connection_manager.broadcast(
                f"user_{user_id}",
                {
                    "type": "notification",
                    "data": data
                }
            )
    
    @staticmethod
    def _channel_matches_pattern(channel: str, pattern: str) -> bool:
        """Check if a channel matches a pattern."""
        import fnmatch
        return fnmatch.fnmatch(channel, pattern)
    
    async def stop(self):
        """Stop the listener and cleanup."""
        self.is_running = False
        
        if self.pubsub:
            await self.pubsub.unsubscribe()
            await self.pubsub.punsubscribe()
        
        if self.redis_client:
            await self.redis_client.close()
        
        logger.info("Redis listener stopped")
    
    async def reconnect(self):
        """Attempt to reconnect to Redis."""
        retry_count = 0
        max_retries = 10
        
        while retry_count < max_retries and self.is_running:
            try:
                await self.connect()
                
                # Re-subscribe to patterns
                await self.psubscribe(
                    "match_*",
                    "live_matches",
                    "poll_*",
                    "competition_*",
                    "notification_*"
                )
                
                logger.info("Reconnected to Redis")
                return True
                
            except Exception as e:
                retry_count += 1
                wait_time = min(2 ** retry_count, 60)
                logger.warning(
                    f"Reconnection attempt {retry_count}/{max_retries} failed: {e}. "
                    f"Retrying in {wait_time}s..."
                )
                await asyncio.sleep(wait_time)
        
        logger.error("Failed to reconnect to Redis after maximum retries")
        return False


class MatchDataProcessor:
    """Processes and enriches match data from Redis messages."""
    
    @staticmethod
    def process_match_event(event_data: dict) -> dict:
        """Process and validate a match event."""
        event_types = {
            'goal': 'Goal',
            'penalty_goal': 'Penalty Goal',
            'own_goal': 'Own Goal',
            'penalty_miss': 'Penalty Miss',
            'yellow_card': 'Yellow Card',
            'second_yellow': 'Second Yellow',
            'red_card': 'Red Card',
            'substitution_in': 'Substitution In',
            'substitution_out': 'Substitution Out',
            'assist': 'Assist',
            'half_time': 'Half Time',
            'full_time': 'Full Time',
        }
        
        return {
            'id': event_data.get('id'),
            'event_type': event_data.get('event_type'),
            'event_type_display': event_types.get(event_data.get('event_type'), 'Event'),
            'minute': event_data.get('minute', 0),
            'injury_minute': event_data.get('injury_minute'),
            'player_name': event_data.get('player_name', ''),
            'team_name': event_data.get('team_name', ''),
            'description': event_data.get('description', ''),
            'score': f"{event_data.get('score_home', 0)} - {event_data.get('score_away', 0)}",
        }
    
    @staticmethod
    def process_live_state(state_data: dict) -> dict:
        """Process and validate live match state."""
        return {
            'current_minute': state_data.get('current_minute', 0),
            'injury_minute': state_data.get('injury_minute'),
            'home_score': state_data.get('home_score', 0),
            'away_score': state_data.get('away_score', 0),
            'possession': state_data.get('possession', {'home': 50, 'away': 50}),
            'momentum': state_data.get('momentum', 'balanced'),
            'attacks': state_data.get('attacks', [])[-5:],  # Keep last 5
            'dangerous_attacks': state_data.get('dangerous_attacks', [])[-5:],
            'last_events': [
                MatchDataProcessor.process_match_event(e)
                for e in state_data.get('last_events', [])
            ],
            'match_status': state_data.get('match_status', 'scheduled'),
        }


class PollDataProcessor:
    """Processes poll data from Redis messages."""
    
    @staticmethod
    def process_poll_update(data: dict) -> dict:
        """Process poll update data for WebSocket delivery."""
        return {
            'poll_id': data.get('poll_id'),
            'match_id': data.get('match_id'),
            'total_votes': data.get('total_votes', 0),
            'results': data.get('results', []),
            'timestamp': data.get('timestamp'),
        }
    
    @staticmethod
    def process_new_vote(data: dict) -> dict:
        """Process a single new vote for real-time update."""
        return {
            'poll_id': data.get('poll_id'),
            'option_id': data.get('option_id'),
            'user_id': data.get('user_id'),
            'timestamp': data.get('timestamp'),
        }