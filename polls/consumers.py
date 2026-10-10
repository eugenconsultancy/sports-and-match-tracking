"""
WebSocket consumer for real-time poll updates.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class PollConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for live poll updates."""
    
    async def connect(self):
        self.poll_id = self.scope['url_route']['kwargs']['poll_id']
        self.room_group_name = f'poll_{self.poll_id}'
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        # Send initial poll data
        poll_data = await self.get_poll_data(self.poll_id)
        if poll_data:
            await self.send(text_data=json.dumps({
                'type': 'poll_state',
                'data': poll_data
            }))
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('type') == 'ping':
            await self.send(text_data=json.dumps({'type': 'pong'}))
    
    async def poll_update(self, event):
        """Send poll updates to WebSocket."""
        await self.send(text_data=json.dumps({
            'type': 'poll_update',
            'data': event['data']
        }))
    
    async def new_vote(self, event):
        """Send new vote notification."""
        await self.send(text_data=json.dumps({
            'type': 'new_vote',
            'data': event['data']
        }))
    
    @database_sync_to_async
    def get_poll_data(self, poll_id):
        """Get initial poll data from database."""
        from .models import Poll
        from .serializers import PollDetailSerializer
        
        try:
            poll = Poll.objects.select_related(
                'match__home_team', 'match__away_team'
            ).prefetch_related('options', 'result_cache').get(id=poll_id)
            return PollDetailSerializer(poll).data
        except Poll.DoesNotExist:
            return None