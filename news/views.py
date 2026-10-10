"""
Views for news app.
"""
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import Q
from django.db.models import F
from rest_framework.decorators import action

from .models import Article, Category, Tag, ArticleRelation
from .serializers import (
    ArticleListSerializer, ArticleDetailSerializer,
    CategorySerializer, TagSerializer, ArticleRelationSerializer
)


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for news articles."""
    
    queryset = Article.objects.select_related(
        'category', 'author'
    ).prefetch_related('tags', 'relations').all()
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'is_featured', 'is_breaking', 'author']
    search_fields = ['title', 'subtitle', 'body', 'summary']
    ordering_fields = ['published_at', 'view_count', 'created_at']
    ordering = ['-published_at', '-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        return ArticleDetailSerializer
    
    def get_queryset(self):
        # Only return published articles for non-admin users
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(status='published')
        return queryset
    
    @method_decorator(cache_page(60 * 5))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        # Increment view count
        instance = self.get_object()
        Article.objects.filter(pk=instance.pk).update(
            view_count=F('view_count') + 1
        )
        return super().retrieve(request, *args, **kwargs)
    
    @action(detail=False, methods=['get'])
    def breaking(self, request):
        """Get breaking news."""
        articles = self.get_queryset().filter(
            is_breaking=True, status='published'
        ).order_by('-published_at')[:10]
        
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured articles."""
        articles = self.get_queryset().filter(
            is_featured=True, status='published'
        ).order_by('-published_at')[:10]
        
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_entity(self, request):
        """Get articles related to a specific entity (team, player, match)."""
        entity_type = request.query_params.get('type')
        entity_id = request.query_params.get('id')
        
        if not entity_type or not entity_id:
            return Response(
                {'error': 'type and id parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        articles = self.get_queryset().filter(
            relations__content_type=entity_type,
            **{f'relations__{entity_type}_id': entity_id}
        ).distinct()
        
        page = self.paginate_queryset(articles)
        if page is not None:
            serializer = ArticleListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ArticleListSerializer(articles, many=True)
        return Response(serializer.data)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for news categories."""
    
    queryset = Category.objects.filter(is_active=True).prefetch_related('children')
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'description']


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for tags."""
    
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class ArticleRelationViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for article relations."""
    
    queryset = ArticleRelation.objects.select_related(
        'article', 'team', 'player', 'match', 'competition'
    ).all()
    serializer_class = ArticleRelationSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['article', 'content_type']


