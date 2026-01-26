# Step 3: Create Notifications App

> **Time:** ~20 minutes  
> **Location:** `backend/notifications/`

---

## Overview

We'll create a new Django app called `notifications` that contains:

- WebSocket consumer (handles connections)
- JWT authentication middleware for WebSockets
- Routing configuration
- Utility functions to emit events

---

## Step 3.1: Create the App Structure

Run this command from the `backend` directory:

```bash
cd backend
python manage.py startapp notifications
```

This creates:

```
backend/notifications/
    __init__.py
    admin.py
    apps.py
    models.py
    tests.py
    views.py
    migrations/
        __init__.py
```

We'll add these files:

- `consumers.py` - WebSocket connection handler
- `routing.py` - WebSocket URL routing
- `middleware.py` - JWT authentication for WebSockets
- `utils.py` - Helper functions to send notifications

---

## Step 3.2: Create middleware.py

**File:** `backend/notifications/middleware.py`

This authenticates WebSocket connections using JWT tokens.

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

### What This Does:

1. Intercepts WebSocket connection before it reaches the consumer
2. Extracts JWT token from URL query string (`?token=xxx`)
3. Validates the token using `simplejwt`
4. Attaches the user to `scope['user']` (like `request.user` in views)

---

## Step 3.3: Create consumers.py

**File:** `backend/notifications/consumers.py`

This handles WebSocket connections and sends notifications to users.

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

            # You can handle client-to-server messages here
            # For now, we're only using server-to-client

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
    # These are called via channel layer messages
    # ==========================================

    async def notification(self, event):
        """
        Generic notification handler.
        Called when channel layer sends a message with type='notification'.

        Event format:
        {
            'type': 'notification',  # Maps to this method
            'notification_type': 'friend_request',  # The actual event type
            'data': {...}  # Event payload
        }
        """
        # Forward the notification to the WebSocket client
        await self.send(text_data=json.dumps({
            'type': event['notification_type'],
            'data': event['data']
        }))

    async def friend_request(self, event):
        """
        Handler for friend request notifications.
        Called when someone sends a friend request to this user.
        """
        await self.send(text_data=json.dumps({
            'type': 'friend_request',
            'data': event['data']
        }))

    async def friend_accepted(self, event):
        """
        Handler for friend accepted notifications.
        Called when someone accepts this user's friend request.
        """
        await self.send(text_data=json.dumps({
            'type': 'friend_accepted',
            'data': event['data']
        }))

    async def new_message(self, event):
        """
        Handler for new message notifications.
        Called when someone sends a message to this user.
        """
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'data': event['data']
        }))
```

### Key Concepts:

**Groups:**

- Each user is added to a group named `user_{id}`
- To notify user #5, we send to group `user_5`
- The channel layer routes it to all consumers in that group

**Event Handlers:**

- `notification()`, `friend_request()`, etc. are called by the channel layer
- The `type` in the message determines which handler runs
- For example, `{'type': 'friend_request', ...}` calls `friend_request()`

---

## Step 3.4: Create utils.py

**File:** `backend/notifications/utils.py`

Helper functions to send notifications from anywhere in your code.

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

    Example:
        notify_user(5, 'friend_request', {
            'from_user': {'id': 1, 'username': 'alice'},
            'request_id': 123
        })
    """
    channel_layer = get_channel_layer()
    group_name = f'user_{user_id}'

    # Send message to the user's group
    # The 'type' determines which handler method is called in the consumer
    async_to_sync(channel_layer.group_send)(
        group_name,
        {
            'type': notification_type.replace('-', '_'),  # friend-request → friend_request
            'data': data
        }
    )


def notify_friend_request(to_user_id, from_user, request_id):
    """
    Send a friend request notification.

    Args:
        to_user_id: ID of user receiving the request
        from_user: User object who sent the request
        request_id: ID of the FriendRequest object
    """
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
    """
    Send a friend accepted notification.

    Args:
        to_user_id: ID of user who originally sent the request
        friend: User object who accepted the request
    """
    notify_user(to_user_id, 'friend_accepted', {
        'friend': {
            'id': friend.id,
            'username': friend.username,
            'first_name': friend.first_name,
            'last_name': friend.last_name,
        }
    })


def notify_new_message(to_user_id, message_data):
    """
    Send a new message notification.

    Args:
        to_user_id: ID of user receiving the message
        message_data: Serialized message data
    """
    notify_user(to_user_id, 'new_message', message_data)
```

### How It Works:

1. **`get_channel_layer()`** - Gets the configured channel layer (Redis or InMemory)
2. **`group_send()`** - Sends a message to all consumers in a group
3. **`async_to_sync()`** - Converts async channel layer call to sync (for use in Django views)

---

## Step 3.5: Create routing.py

**File:** `backend/notifications/routing.py`

WebSocket URL routing (like urls.py for WebSockets).

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

### URL Pattern:

- HTTP: `http://localhost:8000/api/...`
- WebSocket: `ws://localhost:8000/ws/notifications/`

We use `ws/` prefix to differentiate WebSocket routes from HTTP routes.

---

## Step 3.6: Update apps.py (Optional)

**File:** `backend/notifications/apps.py`

Add a nice label:

```python
from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'
    verbose_name = 'Real-time Notifications'
```

---

## Step 3.7: Create **init**.py

**File:** `backend/notifications/__init__.py`

Make sure it exists (should be created by `startapp`, but just in case):

```python
# WebSocket notifications app
default_app_config = 'notifications.apps.NotificationsConfig'
```

---

## Final Directory Structure

After completing this step:

```
backend/notifications/
    __init__.py          # Package marker
    admin.py             # Not used (no models)
    apps.py              # App configuration
    consumers.py         # WebSocket connection handler ⭐
    middleware.py        # JWT authentication ⭐
    models.py            # Not used
    routing.py           # WebSocket URL routing ⭐
    tests.py             # Not used yet
    utils.py             # Helper functions ⭐
    views.py             # Not used
    migrations/
        __init__.py
```

Files marked with ⭐ are the ones we created/modified.

---

## ✅ Checklist

- [ ] Created notifications app with `python manage.py startapp notifications`
- [ ] Created `middleware.py` with `JWTAuthMiddleware`
- [ ] Created `consumers.py` with `NotificationConsumer`
- [ ] Created `utils.py` with `notify_user` and helper functions
- [ ] Created `routing.py` with websocket URL patterns
- [ ] Updated `apps.py` (optional)
- [ ] Verified `__init__.py` exists

---

**Next Step:** [04-modify-views.md](./04-modify-views.md)
