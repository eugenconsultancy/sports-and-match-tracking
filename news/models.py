"""
News-related models: articles, categories, tags.
"""
import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """News categories."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True, related_name='children'
    )
    is_active = models.BooleanField(default=True)
    sort_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'news_categories'
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['sort_order', 'name']
    
    def __str__(self):
        return self.name


class Tag(models.Model):
    """Flexible article tagging."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'news_tags'
        verbose_name = _('tag')
        verbose_name_plural = _('tags')
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Article(models.Model):
    """Editorial/news content."""
    
    class Status(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        PUBLISHED = 'published', _('Published')
        ARCHIVED = 'archived', _('Archived')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=500, db_index=True)
    slug = models.SlugField(max_length=500, unique=True)
    subtitle = models.CharField(max_length=500, blank=True)
    body = models.TextField()
    summary = models.TextField(max_length=1000, blank=True)
    cover_image = models.URLField(blank=True)
    thumbnail = models.URLField(blank=True)
    author = models.ForeignKey(
        'users_app.User', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='articles'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='articles'
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles')
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True
    )
    published_at = models.DateTimeField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_breaking = models.BooleanField(default=False)
    view_count = models.IntegerField(default=0)
    reading_time_minutes = models.IntegerField(default=5)
    
    # SEO fields
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(max_length=300, blank=True)
    meta_keywords = models.CharField(max_length=300, blank=True)
    
    # External
    source_name = models.CharField(max_length=255, blank=True)
    source_url = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'news_articles'
        verbose_name = _('article')
        verbose_name_plural = _('articles')
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['status', '-published_at']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['is_featured', '-published_at']),
            models.Index(fields=['is_breaking', '-published_at']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)


class ArticleRelation(models.Model):
    """Links articles to relevant teams, matches, players."""
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    article = models.ForeignKey(
        Article, on_delete=models.CASCADE, related_name='relations'
    )
    # Polymorphic relationship
    content_type = models.CharField(
        max_length=50, choices=[
            ('team', 'Team'),
            ('player', 'Player'),
            ('match', 'Match'),
            ('competition', 'Competition'),
        ]
    )
    team = models.ForeignKey(
        'teams.Team', on_delete=models.CASCADE, null=True, blank=True,
        related_name='article_relations'
    )
    player = models.ForeignKey(
        'players.Player', on_delete=models.CASCADE, null=True, blank=True,
        related_name='article_relations'
    )
    match = models.ForeignKey(
        'matches.Match', on_delete=models.CASCADE, null=True, blank=True,
        related_name='article_relations'
    )
    competition = models.ForeignKey(
        'competitions.Competition', on_delete=models.CASCADE, null=True, blank=True,
        related_name='article_relations'
    )
    relevance_score = models.FloatField(default=1.0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'article_relations'
        verbose_name = _('article relation')
        verbose_name_plural = _('article relations')
        indexes = [
            models.Index(fields=['article', 'content_type']),
            models.Index(fields=['content_type', 'team']),
            models.Index(fields=['content_type', 'player']),
            models.Index(fields=['content_type', 'match']),
        ]
    
    def __str__(self):
        return f"Relation: {self.article.title} → {self.content_type}"