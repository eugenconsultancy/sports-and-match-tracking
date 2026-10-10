"""
Celery tasks for polls app.
"""
import logging
from celery import shared_task
from django.db.models import Count, F
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

logger = logging.getLogger(__name__)


@shared_task(bind=True)
def update_poll_caches(self):
    """
    Update cached poll results for active polls.
    Runs every 10 seconds for live polling experience.
    """
    from polls.models import Poll, PollOption, PollResultCache
    
    active_polls = Poll.objects.filter(status='active').select_related('match')
    
    updated = 0
    channel_layer = get_channel_layer()
    
    for poll in active_polls:
        try:
            options = poll.options.all()
            total_votes = poll.votes.count()
            
            results = []
            for option in options:
                votes = option.votes.count()
                percentage = (votes / total_votes * 100) if total_votes > 0 else 0
                
                option.vote_count = votes
                option.percentage = round(percentage, 2)
                option.save(update_fields=['vote_count', 'percentage'])
                
                results.append({
                    'option_id': str(option.id),
                    'label': option.label,
                    'option_type': option.option_type,
                    'team_id': str(option.team_id) if option.team_id else None,
                    'votes': votes,
                    'percentage': round(percentage, 2),
                })
            
            # Update poll total
            poll.total_votes = total_votes
            poll.save(update_fields=['total_votes'])
            
            # Update cache
            PollResultCache.objects.update_or_create(
                poll=poll,
                defaults={
                    'results_json': results,
                    'total_votes': total_votes,
                }
            )
            
            # Broadcast to WebSocket
            async_to_sync(channel_layer.group_send)(
                f'poll_{poll.id}',
                {
                    'type': 'poll_update',
                    'data': {
                        'poll_id': str(poll.id),
                        'match_id': str(poll.match_id),
                        'total_votes': total_votes,
                        'results': results,
                    }
                }
            )
            
            updated += 1
            
        except Exception as exc:
            logger.error(f"Error updating poll cache {poll.id}: {exc}")
            continue
    
    return f"Updated {updated} poll caches"