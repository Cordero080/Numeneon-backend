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