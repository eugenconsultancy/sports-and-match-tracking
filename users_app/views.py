"""
Views for users app - authentication and user management.
"""
from rest_framework import viewsets, status, generics, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model

from .models import UserProfile, UserPreference, SessionDevice
from .serializers import (
    UserRegistrationSerializer, UserSerializer,
    UserProfileSerializer, UserPreferenceSerializer,
    CustomTokenObtainPairSerializer, ChangePasswordSerializer,
    DeviceTokenSerializer
)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """User registration endpoint."""
    
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'message': 'User registered successfully',
            'user': UserSerializer(user).data,
        }, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    """Custom JWT login with user data."""
    
    serializer_class = CustomTokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for user management."""
    
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user profile."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Update user profile."""
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_preferences(self, request):
        """Update user preferences."""
        preferences = request.user.preferences
        serializer = UserPreferenceSerializer(
            preferences, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        """Change user password."""
        serializer = ChangePasswordSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        
        return Response({'message': 'Password changed successfully'})
    
    @action(detail=False, methods=['delete'])
    def deactivate(self, request):
        """Deactivate user account."""
        user = request.user
        user.is_active = False
        user.save()
        
        return Response({'message': 'Account deactivated'})


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for user profiles."""
    
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    
    def get_object(self):
        return self.request.user.profile
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)


class UserPreferenceViewSet(viewsets.ModelViewSet):
    """ViewSet for user preferences."""
    
    permission_classes = [IsAuthenticated]
    serializer_class = UserPreferenceSerializer
    
    def get_object(self):
        return self.request.user.preferences


class DeviceTokenViewSet(viewsets.ModelViewSet):
    """ViewSet for device token registration (push notifications)."""
    
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceTokenSerializer
    
    def get_queryset(self):
        return SessionDevice.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        """Register a device token."""
        token = request.data.get('device_token')
        platform = request.data.get('platform', 'web')
        
        if not token:
            return Response(
                {'error': 'device_token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        device, created = SessionDevice.objects.update_or_create(
            device_token=token,
            defaults={
                'user': request.user,
                'platform': platform,
                'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                'is_active': True,
            }
        )
        
        return Response(
            DeviceTokenSerializer(device).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'])
    def unregister(self, request):
        """Unregister a device token."""
        token = request.data.get('device_token')
        
        if not token:
            return Response(
                {'error': 'device_token is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        SessionDevice.objects.filter(
            user=request.user, device_token=token
        ).update(is_active=False)
        
        return Response({'message': 'Device unregistered'})