"""
Enhanced vote service with analytics.
"""
import logging
from celery import shared_task
from django.db import transaction
from django.db.models import Count, Q
from django.utils import timezone
from django.core.cache import cache
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json

logger = logging.getLogger(__name__)


class VoteAnalyticsService:
    """Service for tracking and analyzing votes."""
    
    @staticmethod
    def get_match_poll_trends(poll_id: str, hours: int = 24):
        """Get vote trends over time for a poll."""
        from polls.models import Vote
        
        cutoff = timezone.now() - timezone.timedelta(hours=hours)
        
        votes = Vote.objects.filter(
            poll_id=poll_id,
            voted_at__gte=cutoff
        ).extra({
            'hour': "strftime('%%H', voted_at)"
        }).values('hour', 'option_id').annotate(
            count=Count('id')
        )
        
        return list(votes)
    
    @staticmethod
    def get_live_poll_stats():
        """Get statistics for all live polls."""
        from polls.models import Poll
        
        live_polls = Poll.objects.filter(
            status='active',
            match__status__in=['live', 'half_time']
        ).select_related('match')
        
        stats = []
        for poll in live_polls:
            total_votes = poll.votes.count()
            stats.append({
                'poll_id': str(poll.id),
                'match': f"{poll.match.home_team.name} vs {poll.match.away_team.name}",
                'total_votes': total_votes,
                'options': [
                    {
                        'label': opt.label,
                        'votes': opt.votes.count(),
                        'percentage': round(opt.votes.count() / total_votes * 100, 1) if total_votes > 0 else 0
                    }
                    for opt in poll.options.all()
                ],
                'vote_rate': VoteAnalyticsService._calculate_vote_rate(poll)
            })
        
        return stats
    
    @staticmethod
    def _calculate_vote_rate(poll):
        """Calculate votes per minute rate."""
        first_vote = poll.votes.order_by('voted_at').first()
        if not first_vote:
            return 0
        
        minutes_passed = (timezone.now() - first_vote.voted_at).total_seconds() / 60
        if minutes_passed < 1:
            minutes_passed = 1
        
        return round(poll.votes.count() / minutes_passed, 2)


@shared_task
def broadcast_poll_update(poll_id: str):
    """Broadcast poll update to all connected WebSocket clients."""
    from polls.serializers import PollDetailSerializer
    from polls.models import Poll
    
    try:
        poll = Poll.objects.get(id=poll_id)
        serializer = PollDetailSerializer(poll)
        
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'poll_{poll_id}',
            {
                'type': 'poll_update',
                'data': serializer.data
            }
        )
        logger.info(f"Broadcasted update for poll {poll_id}")
    except Poll.DoesNotExist:
        logger.error(f"Poll {poll_id} not found for broadcast")
    except Exception as e:
        logger.error(f"Error broadcasting poll update: {e}")