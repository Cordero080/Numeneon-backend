# Quick Reference: All Code Files

This file contains all the code you need to create, ready to copy-paste.

---

## 1. requirements.txt (Add to existing)

```
# WebSocket support
channels==4.0.0
daphne==4.1.0
channels-redis==4.2.0
```

---

## 2. backend/notifications/**init**.py

```python
# WebSocket notifications app
default_app_config = 'notifications.apps.NotificationsConfig'
```

---

## 3. backend/notifications/apps.py

```python
from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'
    verbose_name = 'Real-time Notifications'
```

---

## 4. backend/notifications/middleware.py

```python
"""
WebSocket JWT Authentication Middleware

Extracts JWT token from WebSocket query string and authenticates the user.
Since WebSockets don't support headers like HTTP, we pass the token in the URL:
    ws://localhost:8000/ws/notifications/?token=<jwt_token>
"""

from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
from urllib.parse import parse_qs


@database_sync_to_async
def get_user_from_token(token_string):
    """
    Validate JWT token and return the associated user.
    Returns AnonymousUser if token is invalid.
    """
    try:
        # Decode and validate the token
        token = AccessToken(token_string)
        user_id = token.payload.get('user_id')

        # Get and return the user
        user = User.objects.get(id=user_id)
        return user
    except Exception as e:
        print(f"WebSocket auth error: {e}")
        return AnonymousUser()


class JWTAuthMiddleware(BaseMiddleware):
    """
    Custom middleware that extracts JWT from query string and authenticates.

    Usage in frontend:
        const ws = new WebSocket('ws://localhost:8000/ws/notifications/?token=' + jwtToken);
    """

    async def __call__(self, scope, receive, send):
        # Parse query string from the WebSocket URL
        query_string = scope.get('query_string', b'').decode()
        query_params = parse_qs(query_string)

        # Extract token from ?token=xxx
        token_list = query_params.get('token', [])
        token = token_list[0] if token_list else None

        if token:
            # Authenticate user from token
            scope['user'] = await get_user_from_token(token)
        else:
            scope['user'] = AnonymousUser()

        # Continue to the next middleware/consumer
        return await super().__call__(scope, receive, send)
```

---

## 5. backend/notifications/consumers.py

```python
"""
WebSocket Consumer for Real-Time Notifications

Handles:
- User authentication via JWT
- Subscribing users to their personal notification channel
- Sending notifications (friend requests, messages, etc.)
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class NotificationConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer that:
    1. Authenticates users via JWT (handled by middleware)
    2. Subscribes each user to their personal channel (user_{id})
    3. Receives events and forwards them to the connected client
    """

    async def connect(self):
        """
        Called when WebSocket connection is initiated.
        Accepts connection only if user is authenticated.
        """
        self.user = self.scope['user']

        # Reject connection if not authenticated
        if not self.user.is_authenticated:
            print(f"WebSocket connection rejected: not authenticated")
            await self.close(code=4001)  # Custom close code for auth failure
            return

        # Create a unique group name for this user
        # This allows us to send notifications to specific users
        self.group_name = f'user_{self.user.id}'

        # Join the user's personal notification group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name  # This consumer's unique channel
        )

        # Accept the WebSocket connection
        await self.accept()

        print(f"WebSocket connected: {self.user.username} (group: {self.group_name})")

        # Send a welcome message to confirm connection
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': f'Connected as {self.user.username}',
            'user_id': self.user.id
        }))

    async def disconnect(self, close_code):
        """
        Called when WebSocket connection is closed.
        Removes user from their notification group.
        """
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
            print(f"WebSocket disconnected: {self.user.username}")

    async def receive(self, text_data):
        """
        Called when client sends a message through WebSocket.
        Currently just echoes back - extend as needed.
        """
        try:
            data = json.loads(text_data)
            print(f"Received from {self.user.username}: {data}")

            # Echo back for debugging
            await self.send(text_data=json.dumps({
                'type': 'echo',
                'data': data
            }))
        except json.JSONDecodeError:
            await self.send(text_data=json.dumps({
                'type': 'error',
                'message': 'Invalid JSON'
            }))

    # ==========================================
    # NOTIFICATION HANDLERS
    # ==========================================

    async def notification(self, event):
        """Generic notification handler."""
        await self.send(text_data=json.dumps({
            'type': event['notification_type'],
            'data': event['data']
        }))

    async def friend_request(self, event):
        """Handler for friend request notifications."""
        await self.send(text_data=json.dumps({
            'type': 'friend_request',
            'data': event['data']
        }))

    async def friend_accepted(self, event):
        """Handler for friend accepted notifications."""
        await self.send(text_data=json.dumps({
            'type': 'friend_accepted',
            'data': event['data']
        }))

    async def new_message(self, event):
        """Handler for new message notifications."""
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'data': event['data']
        }))
```

---

## 6. backend/notifications/utils.py

```python
"""
Utility functions to send WebSocket notifications.

Usage in views:
    from notifications.utils import notify_user

    notify_user(user_id, 'friend_request', {'from_user': {...}})
"""

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def notify_user(user_id, notification_type, data):
    """
    Send a notification to a specific user via WebSocket.

    Args:
        user_id: The ID of the user to notify
        notification_type: Type of notification (e.g., 'friend_request', 'new_message')
        data: Dictionary containing notification data
    """
    channel_layer = get_channel_layer()
    group_name = f'user_{user_id}'

    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': notification_type.replace('-', '_'),
            'data': data
        }
    )


def notify_friend_request(to_user_id, from_user, request_id):
    """Send a friend request notification."""
    notify_user(to_user_id, 'friend_request', {
        'request_id': request_id,
        'from_user': {
            'id': from_user.id,
            'username': from_user.username,
            'first_name': from_user.first_name,
            'last_name': from_user.last_name,
        }
    })


def notify_friend_accepted(to_user_id, friend):
    """Send a friend accepted notification."""
    notify_user(to_user_id, 'friend_accepted', {
        'friend': {
            'id': friend.id,
            'username': friend.username,
            'first_name': friend.first_name,
            'last_name': friend.last_name,
        }
    })


def notify_new_message(to_user_id, message_data):
    """Send a new message notification."""
    notify_user(to_user_id, 'new_message', message_data)
```

---

## 7. backend/notifications/routing.py

```python
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
```

---

## 8. backend/numeneon/asgi.py (Replace entire file)

```python
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
from channels.security.websocket import AllowedHostsOriginValidator
from notifications.middleware import JWTAuthMiddleware
from notifications.routing import websocket_urlpatterns


application = ProtocolTypeRouter({
    # HTTP requests go to Django
    "http": django_asgi_app,

    # WebSocket requests go through our auth middleware, then to URL router
    "websocket": AllowedHostsOriginValidator(
        JWTAuthMiddleware(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})
```

---

## 9. backend/numeneon/settings.py (Add these sections)

### Add to INSTALLED_APPS (at the top):

```python
INSTALLED_APPS = [
    'daphne',  # <-- ADD THIS FIRST
    'django.contrib.admin',
    # ... rest of your apps ...
    'channels',  # <-- ADD THIS after third-party apps
    # ... custom apps ...
    'notifications',  # <-- ADD THIS
]
```

### Add after WSGI_APPLICATION:

```python
WSGI_APPLICATION = 'numeneon.wsgi.application'
ASGI_APPLICATION = 'numeneon.asgi.application'  # <-- ADD THIS
```

### Add at the bottom (Channels configuration):

```python
# ==========================================
# CHANNELS / WEBSOCKET CONFIGURATION
# ==========================================
import os

if os.environ.get('REDIS_URL'):
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [os.environ.get('REDIS_URL')],
            },
        },
    }
else:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        },
    }
```

---

## 10. backend/friends/views.py (Modifications)

### Add import at top:

```python
from notifications.utils import notify_friend_request, notify_friend_accepted
```

### Modify send_request function:

```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_request(request, user_id):
    """Sends a friend request to another user"""
    from_user = request.user

    try:
        to_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if from_user == to_user:
        return Response({'error': 'You cannot friend yourself'}, status=status.HTTP_400_BAD_REQUEST)

    if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
        return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

    if Friendship.objects.filter(user=from_user, friend=to_user).exists():
        return Response({'error': 'You are already friends'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the friend request
    friend_request = FriendRequest.objects.create(
        from_user=from_user,
        to_user=to_user
    )

    # ✨ Send real-time notification to recipient
    notify_friend_request(
        to_user_id=to_user.id,
        from_user=from_user,
        request_id=friend_request.id
    )

    return Response({'message': 'Friend request sent'}, status=status.HTTP_201_CREATED)
```

### Modify accept_request function:

```python
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_request(request, request_id):
    """Accepts a pending friend request"""
    user = request.user

    try:
        fr = FriendRequest.objects.get(id=request_id)
    except FriendRequest.DoesNotExist:
        return Response({'error': 'Request not found'}, status=status.HTTP_404_NOT_FOUND)

    if fr.to_user != user:
        return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

    # Store the original sender before deleting the request
    original_sender = fr.from_user

    Friendship.objects.create(user=user, friend=original_sender)
    Friendship.objects.create(user=original_sender, friend=user)

    fr.delete()

    # ✨ Send real-time notification to original sender
    notify_friend_accepted(
        to_user_id=original_sender.id,
        friend=user
    )

    return Response({
        'message': 'Friend request accepted',
        'friend': {
            'id': original_sender.id,
            'username': original_sender.username,
            'first_name': original_sender.first_name,
            'last_name': original_sender.last_name
        }
    }, status=status.HTTP_201_CREATED)
```

---

## 11. backend/messages_app/serializers.py (Modifications)

### Add import at top:

```python
from notifications.utils import notify_new_message
```

### Modify MessageSerializer.create():

```python
def create(self, validated_data):
    receiver_id = validated_data.pop('receiver_id')
    receiver = User.objects.get(id=receiver_id)
    validated_data['receiver'] = receiver
    validated_data['sender'] = self.context['request'].user

    # Create the message
    message = super().create(validated_data)

    # ✨ Send real-time notification to recipient
    notify_new_message(
        to_user_id=receiver.id,
        message_data={
            'id': message.id,
            'sender': {
                'id': message.sender.id,
                'username': message.sender.username
            },
            'content': message.content,
            'created_at': message.created_at.isoformat()
        }
    )

    return message
```

---

## Summary Checklist

### New Files to Create:

- [ ] `backend/notifications/__init__.py`
- [ ] `backend/notifications/apps.py`
- [ ] `backend/notifications/middleware.py`
- [ ] `backend/notifications/consumers.py`
- [ ] `backend/notifications/utils.py`
- [ ] `backend/notifications/routing.py`

### Files to Modify:

- [ ] `requirements.txt` - Add channels, daphne, channels-redis
- [ ] `backend/numeneon/settings.py` - Add apps and channel layers
- [ ] `backend/numeneon/asgi.py` - Replace with new routing
- [ ] `backend/friends/views.py` - Add notifications
- [ ] `backend/messages_app/serializers.py` - Add notifications

### Render Deployment:

- [ ] Change start command to use Daphne
- [ ] Add `REDIS_URL` environment variable
