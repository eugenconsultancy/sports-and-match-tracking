"""
Main URL configuration for core project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # API Endpoints
    path('api/v1/auth/', include('users_app.urls')),
    path('api/v1/competitions/', include('competitions.urls')),
    path('api/v1/teams/', include('teams.urls')),
    path('api/v1/players/', include('players.urls')),
    path('api/v1/matches/', include('matches.urls')),
    path('api/v1/standings/', include('standings.urls')),
    path('api/v1/polls/', include('polls.urls')),
    path('api/v1/news/', include('news.urls')),
    path('api/v1/favorites/', include('favorites.urls')),
    path('api/v1/notifications/', include('notifications.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)