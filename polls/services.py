"""
Service layer for polls app.
Contains business logic for poll operations.
"""
import logging
from django.db import transaction
from django.db.models import F
from django.utils import timezone

logger = logging.getLogger(__name__)


class PollService:
    """Service class for poll-related business logic."""
    
    @staticmethod
    @transaction.atomic
    def cast_vote(poll_id, option_id, user, ip_address=None, user_agent=None):
        """
        Cast or update a vote for a poll.
        Returns the updated poll data.
        """
        from .models import Poll, PollOption, Vote, PollResultCache
        
        poll = Poll.objects.select_for_update().get(id=poll_id)
        
        # Validate poll is active
        if poll.status != 'active':
            raise ValueError("Poll is not active")
        
        if poll.end_time and poll.end_time < timezone.now():
            raise ValueError("Poll has ended")
        
        # Find existing vote or create new
        vote, created = Vote.objects.update_or_create(
            poll=poll,
            user=user,
            defaults={
                'option_id': option_id,
                'ip_address': ip_address,
                'user_agent': user_agent or '',
            }
        )
        
        # Recalculate option counts
        PollService._recalculate_poll_results(poll)
        
        return poll
    
    @staticmethod
    def _recalculate_poll_results(poll):
        """Recalculate vote counts and percentages for a poll."""
        from .models import PollOption, PollResultCache
        
        total_votes = poll.votes.count()
        
        results = []
        for option in poll.options.all():
            votes = option.votes.count()
            percentage = round((votes / total_votes * 100), 2) if total_votes > 0 else 0
            
            option.vote_count = votes
            option.percentage = percentage
            option.save(update_fields=['vote_count', 'percentage'])
            
            results.append({
                'option_id': str(option.id),
                'label': option.label,
                'option_type': option.option_type,
                'team_id': str(option.team_id) if option.team_id else None,
                'votes': votes,
                'percentage': percentage,
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
        
        return results
    
    @staticmethod
    def get_poll_results(poll_id):
        """Get cached poll results."""
        from .models import PollResultCache
        
        cache_obj = PollResultCache.objects.filter(poll_id=poll_id).first()
        
        if cache_obj:
            return {
                'poll_id': str(poll_id),
                'total_votes': cache_obj.total_votes,
                'results': cache_obj.results_json,
                'last_calculated': cache_obj.last_calculated.isoformat(),
            }
        return None
    
    @staticmethod
    @transaction.atomic
    def close_poll(poll_id):
        """Close a poll and finalize results."""
        from .models import Poll
        
        poll = Poll.objects.select_for_update().get(id=poll_id)
        poll.status = 'closed'
        poll.end_time = timezone.now()
        poll.save()
        
        logger.info(f"Closed poll {poll_id}")
        return poll
    
    @staticmethod
    def has_user_voted(poll_id, user_id):
        """Check if a user has voted in a poll."""
        from .models import Vote
        
        return Vote.objects.filter(poll_id=poll_id, user_id=user_id).exists()