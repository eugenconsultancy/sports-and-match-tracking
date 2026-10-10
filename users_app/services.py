"""
Service layer for users app.
Contains business logic for user management, authentication helpers, and profile operations.
"""
import logging
import uuid
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from django.core.cache import cache
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

User = get_user_model()


class UserService:
    """Service class for user-related business logic."""
    
    @staticmethod
    @transaction.atomic
    def create_user(email, password, first_name='', last_name='', **extra_fields):
        """Create a new user with profile and preferences."""
        from .models import UserProfile, UserPreference
        
        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            username=email,  # Use email as username
            **extra_fields
        )
        
        # Create default profile
        UserProfile.objects.create(
            user=user,
            language=extra_fields.get('language', 'en'),
            timezone=extra_fields.get('timezone', 'UTC'),
        )
        
        # Create default preferences
        UserPreference.objects.create(user=user)
        
        logger.info(f"Created user: {email}")
        return user
    
    @staticmethod
    def get_user_by_email(email):
        """Get user by email address."""
        return User.objects.filter(email=email).first()
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID with related data."""
        return User.objects.filter(id=user_id).select_related(
            'profile', 'preferences'
        ).first()
    
    @staticmethod
    @transaction.atomic
    def update_user_profile(user_id, profile_data):
        """Update user profile information."""
        from .models import UserProfile
        
        profile = UserProfile.objects.get(user_id=user_id)
        
        updatable_fields = [
            'avatar', 'bio', 'language', 'timezone',
            'country', 'favorite_sport', 'social_links'
        ]
        
        for field in updatable_fields:
            if field in profile_data:
                setattr(profile, field, profile_data[field])
        
        profile.save()
        
        # Invalidate cache
        cache.delete(f'user_profile:{user_id}')
        
        return profile
    
    @staticmethod
    @transaction.atomic
    def update_user_preferences(user_id, preferences_data):
        """Update user notification and display preferences."""
        from .models import UserPreference
        
        preferences = UserPreference.objects.get(user_id=user_id)
        
        updatable_fields = [
            'notification_match_start', 'notification_goal',
            'notification_red_card', 'notification_half_time',
            'notification_full_time', 'notification_news',
            'email_notifications', 'push_notifications', 'odds_format'
        ]
        
        for field in updatable_fields:
            if field in preferences_data:
                setattr(preferences, field, preferences_data[field])
        
        preferences.save()
        return preferences
    
    @staticmethod
    @transaction.atomic
    def change_password(user_id, old_password, new_password):
        """Change user password with validation."""
        user = User.objects.get(id=user_id)
        
        if not user.check_password(old_password):
            raise ValueError("Old password is incorrect")
        
        user.set_password(new_password)
        user.save()
        
        # Invalidate all user sessions (optional)
        # Could implement token blacklisting here
        
        logger.info(f"Password changed for user {user.email}")
        return True
    
    @staticmethod
    @transaction.atomic
    def verify_user_email(user_id):
        """Mark user email as verified."""
        user = User.objects.select_for_update().get(id=user_id)
        user.is_verified = True
        user.save(update_fields=['is_verified'])
        
        logger.info(f"Email verified for user {user.email}")
        return user
    
    @staticmethod
    @transaction.atomic
    def deactivate_user(user_id):
        """Deactivate a user account."""
        user = User.objects.select_for_update().get(id=user_id)
        user.is_active = False
        user.save(update_fields=['is_active'])
        
        # Deactivate all devices
        from .models import SessionDevice
        SessionDevice.objects.filter(user_id=user_id).update(is_active=False)
        
        logger.info(f"Deactivated user {user.email}")
        return user
    
    @staticmethod
    @transaction.atomic
    def reactivate_user(user_id):
        """Reactivate a deactivated user account."""
        user = User.objects.select_for_update().get(id=user_id)
        user.is_active = True
        user.save(update_fields=['is_active'])
        
        logger.info(f"Reactivated user {user.email}")
        return user
    
    @staticmethod
    @transaction.atomic
    def register_device(user_id, device_token, platform='web', user_agent=''):
        """Register a device for push notifications."""
        from .models import SessionDevice
        
        device, created = SessionDevice.objects.update_or_create(
            device_token=device_token,
            defaults={
                'user_id': user_id,
                'platform': platform,
                'user_agent': user_agent,
                'is_active': True,
                'last_used': timezone.now(),
            }
        )
        
        return device, created
    
    @staticmethod
    @transaction.atomic
    def unregister_device(user_id, device_token):
        """Unregister a device from push notifications."""
        from .models import SessionDevice
        
        SessionDevice.objects.filter(
            user_id=user_id,
            device_token=device_token
        ).update(is_active=False)
        
        return True
    
    @staticmethod
    def get_user_devices(user_id):
        """Get active devices for a user."""
        from .models import SessionDevice
        
        return SessionDevice.objects.filter(
            user_id=user_id,
            is_active=True
        ).order_by('-last_used')
    
    @staticmethod
    def search_users(query, limit=20):
        """Search users by email or name (admin only)."""
        return User.objects.filter(
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).filter(is_active=True)[:limit]
    
    @staticmethod
    def get_user_statistics(user_id):
        """Get user activity statistics."""
        from favorites.models import UserFavoriteTeam, UserFavoriteMatch, UserFavoriteCompetition
        from notifications.models import UserNotification
        from polls.models import Vote
        
        stats = {
            'favorite_teams': UserFavoriteTeam.objects.filter(user_id=user_id).count(),
            'favorite_matches': UserFavoriteMatch.objects.filter(user_id=user_id).count(),
            'favorite_competitions': UserFavoriteCompetition.objects.filter(user_id=user_id).count(),
            'total_votes': Vote.objects.filter(user_id=user_id).count(),
            'unread_notifications': UserNotification.objects.filter(
                user_id=user_id,
                delivery_status__in=['sent', 'delivered']
            ).count(),
            'total_notifications': UserNotification.objects.filter(user_id=user_id).count(),
            'member_since': None,
        }
        
        user = User.objects.get(id=user_id)
        stats['member_since'] = user.date_joined
        
        return stats
    
    @staticmethod
    def get_or_create_social_user(email, first_name='', last_name='', provider='google'):
        """Get existing user or create a new one for social login."""
        user = User.objects.filter(email=email).first()
        
        if not user:
            # Generate random password for social users
            random_password = str(uuid.uuid4())
            
            user = UserService.create_user(
                email=email,
                password=random_password,
                first_name=first_name,
                last_name=last_name,
                is_verified=True,  # Social accounts are pre-verified
            )
            
            logger.info(f"Created social user ({provider}): {email}")
        
        return user
    
    @staticmethod
    def get_user_personalized_feed(user_id, limit=20):
        """Generate a personalized feed based on user favorites."""
        from matches.models import Match
        from news.models import Article
        from django.utils import timezone
        
        # Get user's favorite teams
        favorite_team_ids = list(
            User.objects.get(id=user_id).favorite_teams.values_list('team_id', flat=True)
        )
        
        # Get matches for favorite teams
        team_matches = Match.objects.filter(
            Q(home_team_id__in=favorite_team_ids) | Q(away_team_id__in=favorite_team_ids),
            status__in=['scheduled', 'live', 'half_time', 'finished']
        ).select_related(
            'home_team', 'away_team', 'competition_season__competition'
        ).order_by('-kickoff_time')[:limit]
        
        # Get news related to favorite teams
        from news.models import ArticleRelation
        
        article_ids = ArticleRelation.objects.filter(
            content_type='team',
            team_id__in=favorite_team_ids
        ).values_list('article_id', flat=True)
        
        related_articles = Article.objects.filter(
            id__in=article_ids,
            status='published'
        ).select_related('category', 'author').order_by('-published_at')[:limit]
        
        return {
            'matches': list(team_matches),
            'articles': list(related_articles),
        }
    
    @staticmethod
    def invalidate_user_cache(user_id):
        """Invalidate all cached data for a user."""
        cache.delete(f'user_profile:{user_id}')
        cache.delete(f'user_preferences:{user_id}')
        cache.delete(f'user_favorites:{user_id}')
        cache.delete(f'user_stats:{user_id}')
        cache.delete_pattern(f'user_notifications:{user_id}:*')