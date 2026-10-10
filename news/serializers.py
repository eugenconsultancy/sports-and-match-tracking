"""
Serializers for news app.
"""
from rest_framework import serializers
from .models import Article, Category, Tag, ArticleRelation


class CategorySerializer(serializers.ModelSerializer):
    """News category serializer."""
    
    children = serializers.SerializerMethodField()
    article_count = serializers.IntegerField(source='articles.count', read_only=True)
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'parent',
            'is_active', 'sort_order', 'children', 'article_count'
        ]
    
    def get_children(self, obj):
        children = obj.children.filter(is_active=True)
        return CategorySerializer(children, many=True).data


class TagSerializer(serializers.ModelSerializer):
    """Tag serializer."""
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class ArticleListSerializer(serializers.ModelSerializer):
    """Compact article serializer for lists."""
    
    category_name = serializers.CharField(source='category.name', read_only=True, allow_null=True)
    author_name = serializers.CharField(source='author.email', read_only=True, allow_null=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'subtitle', 'summary',
            'cover_image', 'thumbnail', 'category', 'category_name',
            'author', 'author_name', 'tags',
            'status', 'published_at', 'is_featured', 'is_breaking',
            'view_count', 'reading_time_minutes'
        ]


class ArticleDetailSerializer(serializers.ModelSerializer):
    """Detailed article serializer."""
    
    category = CategorySerializer(read_only=True)
    author_name = serializers.CharField(source='author.email', read_only=True, allow_null=True)
    tags = TagSerializer(many=True, read_only=True)
    related_entities = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = [
            'id', 'title', 'slug', 'subtitle', 'body', 'summary',
            'cover_image', 'thumbnail', 'category', 'author', 'author_name',
            'tags', 'status', 'published_at', 'is_featured', 'is_breaking',
            'view_count', 'reading_time_minutes',
            'meta_title', 'meta_description', 'meta_keywords',
            'source_name', 'source_url',
            'created_at', 'updated_at', 'related_entities'
        ]
    
    def get_related_entities(self, obj):
        relations = obj.relations.all()
        result = {'teams': [], 'players': [], 'matches': [], 'competitions': []}
        
        for relation in relations:
            if relation.content_type == 'team' and relation.team:
                result['teams'].append({
                    'id': str(relation.team.id),
                    'name': relation.team.name,
                    'logo': relation.team.logo_url,
                })
            elif relation.content_type == 'player' and relation.player:
                result['players'].append({
                    'id': str(relation.player.id),
                    'name': relation.player.full_name,
                })
            elif relation.content_type == 'match' and relation.match:
                result['matches'].append({
                    'id': str(relation.match.id),
                    'home': relation.match.home_team.name,
                    'away': relation.match.away_team.name,
                })
            elif relation.content_type == 'competition' and relation.competition:
                result['competitions'].append({
                    'id': str(relation.competition.id),
                    'name': relation.competition.name,
                })
        
        return result


class ArticleRelationSerializer(serializers.ModelSerializer):
    """Article relation serializer."""
    
    class Meta:
        model = ArticleRelation
        fields = [
            'id', 'article', 'content_type', 'team', 'player',
            'match', 'competition', 'relevance_score'
        ]