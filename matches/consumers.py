"""
WebSocket consumers for real-time match updates.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.core.serializers.json import DjangoJSONEncoder   # <-- new import


class MatchConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for a single match."""

    async def connect(self):
        self.match_id = self.scope['url_route']['kwargs']['match_id']
        self.room_group_name = f'match_{self.match_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        match_data = await self.get_match_data(self.match_id)
        if match_data:
            await self.send(text_data=json.dumps(
                {'type': 'match_state', 'data': match_data},
                cls=DjangoJSONEncoder          # <-- fix
            ))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data.get('type') == 'ping':
            await self.send(text_data=json.dumps(
                {'type': 'pong'},
                cls=DjangoJSONEncoder
            ))

    async def match_update(self, event):
        await self.send(text_data=json.dumps(
            {'type': event['type'], 'data': event['data']},
            cls=DjangoJSONEncoder
        ))

    async def match_event(self, event):
        await self.send(text_data=json.dumps(
            {'type': 'match_event', 'data': event['data']},
            cls=DjangoJSONEncoder
        ))

    async def live_state_update(self, event):
        await self.send(text_data=json.dumps(
            {'type': 'live_state_update', 'data': event['data']},
            cls=DjangoJSONEncoder
        ))

    @database_sync_to_async
    def get_match_data(self, match_id):
        from .models import Match
        from .serializers import MatchDetailSerializer

        try:
            match = Match.objects.select_related(
                'home_team', 'away_team', 'competition_season__competition'
            ).prefetch_related('events').get(id=match_id)
            return MatchDetailSerializer(match).data
        except Match.DoesNotExist:
            return None


class LiveMatchesConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for all live matches summary."""

    async def connect(self):
        self.room_group_name = 'live_matches'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        live_data = await self.get_live_matches()
        await self.send(text_data=json.dumps(
            {'type': 'live_matches_list', 'data': live_data},
            cls=DjangoJSONEncoder            # <-- fix
        ))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def live_matches_update(self, event):
        await self.send(text_data=json.dumps(
            {'type': 'live_matches_update', 'data': event['data']},
            cls=DjangoJSONEncoder
        ))

    @database_sync_to_async
    def get_live_matches(self):
        from .models import Match
        from .serializers import MatchListSerializer

        matches = Match.objects.filter(
            status__in=['live', 'half_time']
        ).select_related(
            'home_team', 'away_team', 'competition_season__competition'
        ).order_by('kickoff_time')

        return MatchListSerializer(matches, many=True).data