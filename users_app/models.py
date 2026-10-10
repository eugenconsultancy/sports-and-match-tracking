"""
Custom User model and related models.
"""
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager for email-based authentication."""
    
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Custom User model with email as unique identifier."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    email = models.EmailField(_('email address'), unique=True, db_index=True)
    
    # Additional fields
    date_of_birth = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['is_active', 'is_verified']),
        ]
    
    def __str__(self):
        return self.email


class UserProfile(models.Model):
    """Extended user profile information."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile'
    )
    avatar = models.URLField('avatars/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    language = models.CharField(max_length=10, default='en')
    timezone = models.CharField(max_length=50, default='UTC')
    country = models.CharField(max_length=100, blank=True)
    favorite_sport = models.CharField(max_length=50, blank=True)
    social_links = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_profiles'
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
    
    def __str__(self):
        return f"Profile of {self.user.email}"


class UserPreference(models.Model):
    """User preferences for personalization."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='preferences'
    )
    notification_match_start = models.BooleanField(default=True)
    notification_goal = models.BooleanField(default=True)
    notification_red_card = models.BooleanField(default=True)
    notification_half_time = models.BooleanField(default=False)
    notification_full_time = models.BooleanField(default=True)
    notification_news = models.BooleanField(default=False)
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    odds_format = models.CharField(
        max_length=10, choices=[
            ('decimal', 'Decimal'),
            ('fractional', 'Fractional'),
            ('american', 'American'),
        ], default='decimal'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_preferences'
        verbose_name = _('user preference')
        verbose_name_plural = _('user preferences')
    
    def __str__(self):
        return f"Preferences of {self.user.email}"


class SessionDevice(models.Model):
    """Track user devices for push notifications."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='devices'
    )
    device_token = models.CharField(max_length=255, unique=True)
    platform = models.CharField(
        max_length=20, choices=[
            ('ios', 'iOS'),
            ('android', 'Android'),
            ('web', 'Web'),
        ]
    )
    user_agent = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    last_used = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'session_devices'
        verbose_name = _('session device')
        verbose_name_plural = _('session devices')
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['device_token']),
        ]
    
    def __str__(self):
        return f"{self.platform} device for {self.user.email}"