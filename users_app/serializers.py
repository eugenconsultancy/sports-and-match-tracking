"""
Serializers for users app.
"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from .models import UserProfile, UserPreference, SessionDevice

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration."""
    
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'first_name', 'last_name']
    
    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match'})
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            username=validated_data['email'],  # Use email as username
        )
        
        # Create profile and preferences
        UserProfile.objects.create(user=user)
        UserPreference.objects.create(user=user)
        
        return user


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""
    
    profile = serializers.SerializerMethodField()
    preferences = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name',
            'date_of_birth', 'phone_number', 'is_verified',
            'date_joined', 'profile', 'preferences'
        ]
        read_only_fields = ['email', 'is_verified', 'date_joined']
    
    def get_profile(self, obj):
        if hasattr(obj, 'profile'):
            return UserProfileSerializer(obj.profile).data
        return None
    
    def get_preferences(self, obj):
        if hasattr(obj, 'preferences'):
            return UserPreferenceSerializer(obj.preferences).data
        return None


class UserProfileSerializer(serializers.ModelSerializer):
    """User profile serializer."""
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'avatar', 'bio', 'language', 'timezone',
            'country', 'favorite_sport', 'social_links'
        ]


class UserPreferenceSerializer(serializers.ModelSerializer):
    """User preferences serializer."""
    
    class Meta:
        model = UserPreference
        fields = [
            'id', 'notification_match_start', 'notification_goal',
            'notification_red_card', 'notification_half_time',
            'notification_full_time', 'notification_news',
            'email_notifications', 'push_notifications', 'odds_format'
        ]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom JWT serializer that includes user data."""
    
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        
        data['user'] = {
            'id': str(user.id),
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        
        return data


class ChangePasswordSerializer(serializers.Serializer):
    """Serializer for password change."""
    
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Old password is incorrect')
        return value


class DeviceTokenSerializer(serializers.ModelSerializer):
    """Serializer for device token registration."""
    
    class Meta:
        model = SessionDevice
        fields = ['id', 'device_token', 'platform', 'user_agent', 'is_active']
        read_only_fields = ['id']