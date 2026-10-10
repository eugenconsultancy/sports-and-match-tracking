"""
Serializers for polls app.
"""
from rest_framework import serializers
from .models import Poll, PollOption, Vote, PollResultCache


class PollOptionSerializer(serializers.ModelSerializer):
    """Poll option serializer."""
    
    team_name = serializers.CharField(source='team.name', read_only=True, allow_null=True)
    team_logo = serializers.CharField(source='team.logo_url', read_only=True, allow_null=True)
    
    class Meta:
        model = PollOption
        fields = [
            'id', 'label', 'team', 'team_name', 'team_logo',
            'option_type', 'sort_order', 'vote_count', 'percentage'
        ]


class PollListSerializer(serializers.ModelSerializer):
    """Compact poll serializer for lists."""
    
    match_info = serializers.SerializerMethodField()
    options = PollOptionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Poll
        fields = [
            'id', 'match', 'match_info', 'question',
            'start_time', 'end_time', 'status', 'total_votes',
            'is_featured', 'options'
        ]
    
    def get_match_info(self, obj):
        return {
            'home_team': obj.match.home_team.name if obj.match.home_team else None,
            'away_team': obj.match.away_team.name if obj.match.away_team else None,
            'home_score': obj.match.home_score,
            'away_score': obj.match.away_score,
            'kickoff_time': obj.match.kickoff_time,
            'status': obj.match.status,
        }


class PollDetailSerializer(serializers.ModelSerializer):
    """Detailed poll serializer with full vote data."""
    
    match_info = serializers.SerializerMethodField()
    options = PollOptionSerializer(many=True, read_only=True)
    result_cache = serializers.SerializerMethodField()
    user_vote = serializers.SerializerMethodField()
    
    class Meta:
        model = Poll
        fields = [
            'id', 'match', 'match_info', 'question',
            'start_time', 'end_time', 'status', 'total_votes',
            'is_featured', 'created_at', 'options',
            'result_cache', 'user_vote'
        ]
    
    def get_match_info(self, obj):
        return {
            'id': str(obj.match.id),
            'home_team': obj.match.home_team.name if obj.match.home_team else None,
            'home_team_logo': obj.match.home_team.logo_url if obj.match.home_team else None,
            'away_team': obj.match.away_team.name if obj.match.away_team else None,
            'away_team_logo': obj.match.away_team.logo_url if obj.match.away_team else None,
            'home_score': obj.match.home_score,
            'away_score': obj.match.away_score,
            'kickoff_time': obj.match.kickoff_time.isoformat() if obj.match.kickoff_time else None,
            'status': obj.match.status,
        }
    
    def get_result_cache(self, obj):
        if hasattr(obj, 'result_cache') and obj.result_cache:
            return obj.result_cache.results_json
        return None
    
    def get_user_vote(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            vote = obj.votes.filter(user=request.user).first()
            if vote:
                return {
                    'option_id': str(vote.option_id),
                    'voted_at': vote.voted_at.isoformat()
                }
        return None


class VoteSerializer(serializers.ModelSerializer):
    """Vote serializer."""
    
    user_email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = Vote
        fields = [
            'id', 'poll', 'option', 'user', 'user_email',
            'ip_address', 'voted_at'
        ]
        read_only_fields = ['user', 'ip_address', 'voted_at']


class CreateVoteSerializer(serializers.Serializer):
    """Serializer for creating a vote."""
    
    option_id = serializers.UUIDField()
    
    def validate_option_id(self, value):
        from polls.models import PollOption
        try:
            option = PollOption.objects.select_related('poll').get(id=value)
        except PollOption.DoesNotExist:
            raise serializers.ValidationError("Invalid option")
        
        if option.poll.status != 'active':
            raise serializers.ValidationError("Poll is not active")
        
        if option.poll.end_time and option.poll.end_time < timezone.now():
            raise serializers.ValidationError("Poll has ended")
        
        return value


class PollResultCacheSerializer(serializers.ModelSerializer):
    """Cached poll results serializer."""
    
    class Meta:
        model = PollResultCache
        fields = ['id', 'poll', 'results_json', 'total_votes', 'last_calculated']


# Import timezone
from django.utils import timezone