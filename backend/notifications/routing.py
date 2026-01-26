"""
WebSocket URL Routing

Maps WebSocket URLs to consumers.
Similar to urls.py but for WebSocket connections instead of HTTP.
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # ws://localhost:8000/ws/notifications/
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]