"""
Serializers for notifications app.
"""
from rest_framework import serializers
from .models import Notification, UserNotification, Subscription


class NotificationSerializer(serializers.ModelSerializer):
    """Notification serializer."""
    
    class Meta:
        model = Notification
        fields = [
            'id', 'notification_type', 'title', 'body',
            'data_payload', 'is_system', 'created_at'
        ]


class UserNotificationSerializer(serializers.ModelSerializer):
    """User notification serializer."""
    
    notification = NotificationSerializer(read_only=True)
    
    class Meta:
        model = UserNotification
        fields = [
            'id', 'notification', 'delivery_status',
            'read_at', 'clicked', 'created_at'
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    """Subscription serializer."""
    
    team_name = serializers.CharField(source='team.name', read_only=True, allow_null=True)
    match_info = serializers.SerializerMethodField()
    competition_name = serializers.CharField(
        source='competition.name', read_only=True, allow_null=True
    )
    player_name = serializers.CharField(
        source='player.full_name', read_only=True, allow_null=True
    )
    
    class Meta:
        model = Subscription
        fields = [
            'id', 'team', 'team_name', 'match', 'match_info',
            'competition', 'competition_name', 'player', 'player_name',
            'notification_types', 'is_active', 'created_at'
        ]
        read_only_fields = ['user', 'created_at', 'updated_at']
    
    def get_match_info(self, obj):
        if obj.match:
            return {
                'home_team': obj.match.home_team.name,
                'away_team': obj.match.away_team.name,
                'kickoff_time': obj.match.kickoff_time,
            }
        return None