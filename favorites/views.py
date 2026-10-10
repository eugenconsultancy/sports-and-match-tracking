"""
Views for favorites app.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import UserFavoriteTeam, UserFavoriteMatch, UserFavoriteCompetition
from .serializers import (
    UserFavoriteTeamSerializer, UserFavoriteMatchSerializer,
    UserFavoriteCompetitionSerializer, AddFavoriteSerializer
)


class BaseFavoriteViewSet(viewsets.ModelViewSet):
    """Base viewset for favorites with common logic."""
    
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class UserFavoriteTeamViewSet(BaseFavoriteViewSet):
    """ViewSet for user favorite teams."""
    
    queryset = UserFavoriteTeam.objects.select_related('team').all()
    serializer_class = UserFavoriteTeamSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['priority', 'created_at']
    ordering = ['priority']
    
    @action(detail=False, methods=['post'])
    def add(self, request):
        """Add a team to favorites."""
        serializer = AddFavoriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if serializer.validated_data['entity_type'] != 'team':
            return Response(
                {'error': 'Use /api/v1/favorites/matches/add/ for matches'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        favorite, created = UserFavoriteTeam.objects.get_or_create(
            user=request.user,
            team_id=serializer.validated_data['entity_id']
        )
        
        if not created:
            return Response({'message': 'Team already in favorites'})
        
        return Response(
            UserFavoriteTeamSerializer(favorite).data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['delete'])
    def remove(self, request):
        """Remove a team from favorites."""
        team_id = request.data.get('entity_id')
        if not team_id:
            return Response(
                {'error': 'entity_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        deleted, _ = UserFavoriteTeam.objects.filter(
            user=request.user, team_id=team_id
        ).delete()
        
        if deleted:
            return Response({'message': 'Removed from favorites'})
        return Response(
            {'error': 'Favorite not found'},
            status=status.HTTP_404_NOT_FOUND
        )


class UserFavoriteMatchViewSet(BaseFavoriteViewSet):
    """ViewSet for user favorite matches."""
    
    queryset = UserFavoriteMatch.objects.select_related(
        'match__home_team', 'match__away_team'
    ).all()
    serializer_class = UserFavoriteMatchSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['post'])
    def add(self, request):
        """Add a match to favorites."""
        serializer = AddFavoriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if serializer.validated_data['entity_type'] != 'match':
            return Response(
                {'error': 'Use /api/v1/favorites/teams/add/ for teams'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        favorite, created = UserFavoriteMatch.objects.get_or_create(
            user=request.user,
            match_id=serializer.validated_data['entity_id']
        )
        
        if not created:
            return Response({'message': 'Match already in favorites'})
        
        return Response(
            UserFavoriteMatchSerializer(favorite).data,
            status=status.HTTP_201_CREATED
        )


class UserFavoriteCompetitionViewSet(BaseFavoriteViewSet):
    """ViewSet for user favorite competitions."""
    
    queryset = UserFavoriteCompetition.objects.select_related('competition').all()
    serializer_class = UserFavoriteCompetitionSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['priority', 'created_at']
    ordering = ['priority']
    
    @action(detail=False, methods=['post'])
    def add(self, request):
        """Add a competition to favorites."""
        serializer = AddFavoriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if serializer.validated_data['entity_type'] != 'competition':
            return Response(
                {'error': 'Use /api/v1/favorites/teams/add/ for teams'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        favorite, created = UserFavoriteCompetition.objects.get_or_create(
            user=request.user,
            competition_id=serializer.validated_data['entity_id']
        )
        
        if not created:
            return Response({'message': 'Competition already in favorites'})
        
        return Response(
            UserFavoriteCompetitionSerializer(favorite).data,
            status=status.HTTP_201_CREATED
        )