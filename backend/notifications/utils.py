"""
Utility functions to send WebSocket notifications.

Usage in views:
    from notifications.utils import notify_friend_request

    notify_friend_request(user_id=5, from_user=request.user, request_id=123)
"""

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import logging

logger = logging.getLogger(__name__)


def notify_user(user_id, notification_type, data):
    """
    Send a notification to a specific user via WebSocket.

    Args:
        user_id: The ID of the user to notify
        notification_type: Type of notification (e.g., 'friend_request', 'new_message')
        data: Dictionary containing notification data
    """
    try:
        channel_layer = get_channel_layer()
        if channel_layer is None:
            logger.warning("Channel layer is None, skipping notification")
            return
            
        group_name = f'user_{user_id}'

        # Send message to the user's group
        async_to_sync(channel_layer.group_send)(
            group_name,
            {
                'type': notification_type.replace('-', '_'),
                'data': data
            }
        )
    except Exception as e:
        logger.error(f"Failed to send notification: {e}")
        # Don't re-raise - notifications should not break the main request


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


def notify_new_post(to_user_id, post_data):
    """
    Send a new post notification to a friend.

    Args:
        to_user_id: ID of user to notify (a friend)
        post_data: Serialized post data
    """
    notify_user(to_user_id, 'new_post', post_data)