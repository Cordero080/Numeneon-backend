"""
WebSocket Consumer for Real-Time Notifications

Handles:
- User authentication via JWT
- Subscribing users to their personal notification channel
- Sending notifications (friend requests, messages, etc.)
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer


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
            await self.close(code=4001)
            return

        # Create a unique group name for this user
        self.group_name = f'user_{self.user.id}'

        # Join the user's personal notification group
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

        print(f"WebSocket connected: {self.user.username} (group: {self.group_name})")

        # Send a welcome message
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': f'Connected as {self.user.username}',
            'user_id': self.user.id
        }))

    async def disconnect(self, close_code):
        """
        Called when WebSocket connection is closed.
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