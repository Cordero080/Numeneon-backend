"""
asgi.py - Async Server Gateway Interface

This is the entry point for both HTTP and WebSocket connections.
- HTTP requests → Django views (REST API)
- WebSocket requests → Channels consumers (real-time notifications)
"""

import os
from django.core.asgi import get_asgi_application

# ⚠️ IMPORTANT: Set this BEFORE importing anything else from Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'numeneon.settings')

# Initialize Django ASGI application early to ensure AppRegistry is populated
# This MUST happen before importing consumers or routing
django_asgi_app = get_asgi_application()

# Now we can safely import Channels components
from channels.routing import ProtocolTypeRouter, URLRouter
from notifications.middleware import JWTAuthMiddleware
from notifications.routing import websocket_urlpatterns


application = ProtocolTypeRouter({
    # HTTP requests go to Django
    "http": django_asgi_app,

    # WebSocket requests go through our auth middleware, then to URL router
    # Note: Origin validation removed - CORS handles security for HTTP,
    # and JWT auth handles WebSocket security
    "websocket": JWTAuthMiddleware(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})