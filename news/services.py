"""
Service layer for news app.
Contains business logic for article management, search, and content delivery.
"""
import logging
from django.db import transaction
from django.db.models import Q, F, Count
from django.utils import timezone
from django.core.cache import cache

logger = logging.getLogger(__name__)


class NewsService:
    """Service class for news-related business logic."""
    
    @staticmethod
    def get_featured_articles(limit=10):
        """Get featured articles for homepage display."""
        from .models import Article
        
        cache_key = f'news:featured:{limit}'
        articles = cache.get(cache_key)
        
        if articles is None:
            articles = list(
                Article.objects.filter(
                    status='published',
                    is_featured=True
                ).select_related(
                    'category', 'author'
                ).prefetch_related(
                    'tags'
                ).order_by('-published_at')[:limit]
            )
            cache.set(cache_key, articles, 300)  # Cache for 5 minutes
        
        return articles
    
    @staticmethod
    def get_breaking_news(limit=5):
        """Get breaking news articles."""
        from .models import Article
        
        return Article.objects.filter(
            status='published',
            is_breaking=True
        ).select_related(
            'category', 'author'
        ).order_by('-published_at')[:limit]
    
    @staticmethod
    def get_articles_by_entity(entity_type, entity_id, limit=20):
        """
        Get articles related to a specific entity (team, player, match, competition).
        """
        from .models import Article, ArticleRelation
        
        filter_kwargs = {
            'content_type': entity_type,
            f'{entity_type}_id': entity_id,
        }
        
        article_ids = ArticleRelation.objects.filter(
            **filter_kwargs
        ).values_list('article_id', flat=True)
        
        return Article.objects.filter(
            id__in=article_ids,
            status='published'
        ).select_related(
            'category', 'author'
        ).prefetch_related(
            'tags'
        ).order_by('-published_at')[:limit]
    
    @staticmethod
    def get_articles_by_category(category_slug, limit=20, offset=0):
        """Get articles filtered by category."""
        from .models import Article
        
        return Article.objects.filter(
            category__slug=category_slug,
            status='published'
        ).select_related(
            'category', 'author'
        ).prefetch_related(
            'tags'
        ).order_by('-published_at')[offset:offset + limit]
    
    @staticmethod
    def get_articles_by_tag(tag_slug, limit=20, offset=0):
        """Get articles filtered by tag."""
        from .models import Article
        
        return Article.objects.filter(
            tags__slug=tag_slug,
            status='published'
        ).select_related(
            'category', 'author'
        ).prefetch_related(
            'tags'
        ).order_by('-published_at')[offset:offset + limit]
    
    @staticmethod
    def search_articles(query, limit=20, offset=0):
        """Search articles by title, body, and summary."""
        from .models import Article
        
        return Article.objects.filter(
            Q(title__icontains=query) |
            Q(body__icontains=query) |
            Q(summary__icontains=query) |
            Q(subtitle__icontains=query),
            status='published'
        ).select_related(
            'category', 'author'
        ).prefetch_related(
            'tags'
        ).order_by('-published_at')[offset:offset + limit]
    
    @staticmethod
    def get_related_articles(article_id, limit=5):
        """Get articles related to the same entities or category."""
        from .models import Article, ArticleRelation
        
        article = Article.objects.get(id=article_id)
        
        # Get related entity IDs
        relation_article_ids = set()
        
        for relation in article.relations.all():
            filter_kwargs = {
                'content_type': relation.content_type,
            }
            
            if relation.content_type == 'team' and relation.team_id:
                filter_kwargs['team_id'] = relation.team_id
            elif relation.content_type == 'player' and relation.player_id:
                filter_kwargs['player_id'] = relation.player_id
            elif relation.content_type == 'match' and relation.match_id:
                filter_kwargs['match_id'] = relation.match_id
            elif relation.content_type == 'competition' and relation.competition_id:
                filter_kwargs['competition_id'] = relation.competition_id
            else:
                continue
            
            ids = ArticleRelation.objects.filter(
                **filter_kwargs
            ).exclude(
                article_id=article_id
            ).values_list('article_id', flat=True)
            
            relation_article_ids.update(ids)
        
        # Get articles in same category
        if article.category:
            category_ids = article.category_id
        
        related = Article.objects.filter(
            Q(id__in=relation_article_ids) |
            Q(category_id=article.category_id),
            status='published'
        ).exclude(
            id=article_id
        ).select_related(
            'category', 'author'
        ).prefetch_related(
            'tags'
        ).order_by('-published_at')[:limit]
        
        return related
    
    @staticmethod
    @transaction.atomic
    def publish_article(article_id, publish_time=None):
        """Publish an article."""
        from .models import Article
        
        article = Article.objects.select_for_update().get(id=article_id)
        article.status = 'published'
        article.published_at = publish_time or timezone.now()
        article.save(update_fields=['status', 'published_at'])
        
        # Invalidate caches
        cache.delete_pattern('news:featured:*')
        cache.delete_pattern('news:category:*')
        
        logger.info(f"Published article: {article.title}")
        return article
    
    @staticmethod
    @transaction.atomic
    def increment_view_count(article_id):
        """Increment article view count atomically."""
        from .models import Article
        
        Article.objects.filter(id=article_id).update(
            view_count=F('view_count') + 1
        )
    
    @staticmethod
    def get_popular_articles(days=7, limit=10):
        """Get most viewed articles in the last N days."""
        from .models import Article
        
        cutoff = timezone.now() - timezone.timedelta(days=days)
        
        return Article.objects.filter(
            status='published',
            published_at__gte=cutoff
        ).select_related(
            'category', 'author'
        ).order_by('-view_count')[:limit]
    
    @staticmethod
    def get_category_tree():
        """Get the full category tree with article counts."""
        from .models import Category
        
        cache_key = 'news:category_tree'
        tree = cache.get(cache_key)
        
        if tree is None:
            categories = Category.objects.filter(
                is_active=True, parent__isnull=True
            ).prefetch_related(
                'children__children'
            ).annotate(
                article_count=Count('articles', filter=Q(articles__status='published'))
            ).order_by('sort_order', 'name')
            
            tree = list(categories)
            cache.set(cache_key, tree, 600)  # Cache for 10 minutes
        
        return tree
    
    @staticmethod
    @transaction.atomic
    def create_article_relation(article_id, content_type, entity_id, relevance_score=1.0):
        """Create a relation between an article and an entity."""
        from .models import ArticleRelation
        
        kwargs = {
            'article_id': article_id,
            'content_type': content_type,
            f'{content_type}_id': entity_id,
            'relevance_score': relevance_score,
        }
        
        relation, created = ArticleRelation.objects.get_or_create(
            article_id=article_id,
            content_type=content_type,
            **{f'{content_type}_id': entity_id},
            defaults={'relevance_score': relevance_score}
        )
        
        return relation
    
    @staticmethod
    def get_article_meta(article_id):
        """Get SEO metadata for an article."""
        from .models import Article
        
        article = Article.objects.only(
            'title', 'meta_title', 'meta_description',
            'meta_keywords', 'cover_image', 'summary', 'slug'
        ).get(id=article_id)
        
        return {
            'title': article.meta_title or article.title,
            'description': article.meta_description or (article.summary[:160] if article.summary else ''),
            'keywords': article.meta_keywords,
            'image': article.cover_image,
            'url': f'/news/{article.slug}',
        }