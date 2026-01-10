# 🟣 CRYSTAL - Friends System Lead
# views.py - API endpoints for friend operations
"""
TODO: Create Friends API Views - manage friendships and requests

Unlike Posts (CRUD on single model), friends has custom operations.
Use function-based views with @api_view decorator.

Endpoints to create:
- GET /api/friends/ - List current user's friends (friend_list)
- GET /api/friends/requests/ - List pending friend requests received (pending_requests)
- POST /api/friends/request/:user_id/ - Send friend request to user (send_request)
- POST /api/friends/accept/:request_id/ - Accept a friend request (accept_request)
- POST /api/friends/decline/:request_id/ - Decline a friend request (decline_request)
- DELETE /api/friends/remove/:user_id/ - Remove a friend (remove_friend)

All endpoints require authentication (must be logged in).

IMPORTANT: friend_list returns simple user data, NOT serialized Friendship objects!
Expected response for GET /api/friends/:
[
  { "id": 1, "username": "alice", "first_name": "Alice", "last_name": "Smith" },
  { "id": 2, "username": "bob", "first_name": "Bob", "last_name": "Jones" }
]

Expected response for GET /api/friends/requests/:
[
  {
    "id": 1,
    "from_user": { "id": 5, "username": "charlie", "first_name": "Charlie", "last_name": "Brown" },
    "created_at": "2024-12-19T10:30:00Z"
  }
]

For accept_request:
1. Find the FriendRequest by ID
2. Verify to_user is current user
3. Create TWO Friendship records (both directions)
4. DELETE the FriendRequest
5. Return the new friend's data

For decline_request:
1. Find the FriendRequest by ID
2. Verify to_user is current user
3. DELETE the FriendRequest
4. Return success response

For remove_friend:
1. Delete Friendship where user=me AND friend=target
2. Also delete reverse: user=target AND friend=me
3. Return success

Think about:
- How do you find all friends? (Friendship.objects.filter(user=request.user))
- When accepting, create BOTH directions of friendship
- What if user tries to friend themselves? (Return 400 error)
- What if friend request already exists? (Return 400 error)
- What if users are already friends? (Return 400 error)

Hint: Use @api_view(['GET']) and @api_view(['POST']) decorators
Hint: Use @permission_classes([IsAuthenticated])
Hint: Build response dict manually in views (not using serializers for simple cases)
Hint: Return proper status codes: 201 Created, 400 Bad Request, 404 Not Found
Hint: For accept: Friendship.objects.create(user=to_user, friend=from_user)
Hint: For accept: Friendship.objects.create(user=from_user, friend=to_user)
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import FriendRequest, Friendship


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def friend_list(request):
    """
    TODO: Returns all friends of the logged-in user
    
    Steps:
    1. Get current user from request.user
    2. Query Friendship.objects.filter(user=user)
    3. Build list of friend data dicts (id, username, first_name, last_name)
    4. Return Response(friends)
    """
    # Your code here
    pass


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pending_requests(request):
    """
    TODO: Returns all pending friend requests TO the logged-in user
    
    Steps:
    1. Get current user from request.user
    2. Query FriendRequest.objects.filter(to_user=user)
    3. Build list with id, from_user (nested), created_at
    4. Return Response(pending)
    
    Hint: created_at.isoformat() for ISO timestamp string
    """
    # Your code here
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_request(request, user_id):
    """
    TODO: Sends a friend request to another user
    
    Steps:
    1. Get from_user from request.user
    2. Find to_user by user_id (handle DoesNotExist)
    3. Validate: can't friend yourself
    4. Validate: request doesn't already exist
    5. Create FriendRequest
    6. Return success response with 201 status
    """
    # Your code here
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_request(request, request_id):
    """
    TODO: Accepts a pending friend request
    
    Steps:
    1. Find FriendRequest by request_id (handle DoesNotExist)
    2. Verify friend_request.to_user == request.user
    3. Create Friendship BOTH ways (user→friend AND friend→user)
    4. Delete the FriendRequest
    5. Return success response with 201 status
    """
    # Your code here
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def decline_request(request, request_id):
    """
    TODO: Declines a pending friend request
    
    Steps:
    1. Find FriendRequest by request_id (handle DoesNotExist)
    2. Verify friend_request.to_user == request.user
    3. Delete the FriendRequest
    4. Return success response
    """
    # Your code here
    pass


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_friend(request, user_id):
    """
    TODO: Removes a friend from your friend list
    
    Steps:
    1. Find the friend User by user_id (handle DoesNotExist)
    2. Delete Friendship both ways:
       - Friendship.objects.filter(user=me, friend=target).delete()
       - Friendship.objects.filter(user=target, friend=me).delete()
    3. Return success response
    """
    # Your code here
    pass