"""
Django admin configuration for news app.
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Article, Category, Tag, ArticleRelation


class ArticleRelationInline(admin.TabularInline):
    """Inline relations within article admin."""
    
    model = ArticleRelation
    extra = 1
    fields = ['content_type', 'team', 'player', 'match', 'competition', 'relevance_score']
    raw_id_fields = ['team', 'player', 'match', 'competition']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin view for Category model."""
    
    list_display = ['name', 'slug', 'parent', 'is_active', 'sort_order', 'article_count']
    list_filter = ['is_active']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    autocomplete_fields = ['parent']
    
    fieldsets = (
        ('Category Details', {
            'fields': ('name', 'slug', 'description', 'parent')
        }),
        ('Display', {
            'fields': ('is_active', 'sort_order')
        }),
    )
    
    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = 'Articles'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin view for Tag model."""
    
    list_display = ['name', 'slug', 'article_count']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at']
    
    def article_count(self, obj):
        return obj.articles.count()
    article_count.short_description = 'Articles'


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin view for Article model."""
    
    list_display = [
        'title', 'category', 'status', 'author',
        'published_at', 'is_featured', 'is_breaking',
        'view_count', 'image_preview'
    ]
    list_filter = [
        'status', 'is_featured', 'is_breaking',
        'category', 'author'
    ]
    search_fields = [
        'title', 'subtitle', 'body', 'summary',
        'meta_title', 'meta_description'
    ]
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['view_count', 'created_at', 'updated_at']
    filter_horizontal = ['tags']
    inlines = [ArticleRelationInline]
    autocomplete_fields = ['author', 'category']
    date_hierarchy = 'published_at'
    
    fieldsets = (
        ('Content', {
            'fields': (
                'title', 'slug', 'subtitle', 'body', 'summary'
            )
        }),
        ('Media', {
            'fields': ('cover_image', 'thumbnail')
        }),
        ('Classification', {
            'fields': (
                'author', 'category', 'tags',
                'status', 'is_featured', 'is_breaking'
            )
        }),
        ('Publishing', {
            'fields': ('published_at', 'reading_time_minutes')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Source', {
            'fields': ('source_name', 'source_url'),
            'classes': ('collapse',)
        }),
        ('Statistics', {
            'fields': ('view_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def image_preview(self, obj):
        if obj.thumbnail or obj.cover_image:
            return format_html(
                '<img src="{}" style="max-height: 40px; border-radius: 4px;" />',
                obj.thumbnail or obj.cover_image
            )
        return '-'
    image_preview.short_description = 'Image'
    
    actions = ['make_published', 'make_featured', 'make_draft']
    
    @admin.action(description='Publish selected articles')
    def make_published(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='published', published_at=timezone.now())
    
    @admin.action(description='Mark as featured')
    def make_featured(self, request, queryset):
        queryset.update(is_featured=True)
    
    @admin.action(description='Move to drafts')
    def make_draft(self, request, queryset):
        queryset.update(status='draft')


@admin.register(ArticleRelation)
class ArticleRelationAdmin(admin.ModelAdmin):
    """Admin view for ArticleRelation model."""
    
    list_display = [
        'article_link', 'content_type', 'entity_name', 'relevance_score'
    ]
    list_filter = ['content_type']
    search_fields = [
        'article__title', 'team__name', 'player__full_name',
        'match__home_team__name', 'competition__name'
    ]
    readonly_fields = ['created_at']
    autocomplete_fields = ['article', 'team', 'player', 'match', 'competition']
    
    fieldsets = (
        ('Relation', {
            'fields': ('article', 'content_type', 'relevance_score')
        }),
        ('Entity', {
            'fields': ('team', 'player', 'match', 'competition')
        }),
    )
    
    def article_link(self, obj):
        from django.urls import reverse
        url = reverse('admin:news_article_change', args=[obj.article_id])
        return format_html('<a href="{}">{}</a>', url, obj.article.title[:50])
    article_link.short_description = 'Article'
    
    def entity_name(self, obj):
        if obj.content_type == 'team' and obj.team:
            return obj.team.name
        elif obj.content_type == 'player' and obj.player:
            return obj.player.full_name
        elif obj.content_type == 'match' and obj.match:
            return str(obj.match)
        elif obj.content_type == 'competition' and obj.competition:
            return obj.competition.name
        return '-'
    entity_name.short_description = 'Entity'