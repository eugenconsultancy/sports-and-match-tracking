"""
URL configuration for news app.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ArticleViewSet, CategoryViewSet, TagViewSet, ArticleRelationViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet, basename='article')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'relations', ArticleRelationViewSet, basename='relation')

urlpatterns = [
    path('', include(router.urls)),
]