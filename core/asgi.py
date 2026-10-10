"""
ASGI config for core project.
"""
import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.config.settings')

django_asgi_app = get_asgi_application()

# Import after Django setup to avoid AppRegistryNotReady
from matches.routing import websocket_urlpatterns as match_ws_urls
from polls.routing import websocket_urlpatterns as poll_ws_urls

websocket_urlpatterns = match_ws_urls + poll_ws_urls

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        )
    ),
})