# 🟣 CRYSTAL - Friends System Lead
# models.py - Database structure for friendships and friend requests
"""
TODO: Create Friendship models - friend connections and requests

NUMENEON has a friends system with two models:
1. Friendship: Represents an accepted friendship between two users
2. FriendRequest: Represents a pending friend request

IMPORTANT: Directional friendship model!
- user: The person who has this friend
- friend: The person they are friends with
- When Alice adds Bob, create TWO Friendship records (Alice→Bob and Bob→Alice)

Friendship model fields:
- user: The owner of this friend entry (ForeignKey to User)
- friend: The friend (ForeignKey to User)
- created_at: When friendship was created (auto-set)

FriendRequest model fields:
- from_user: Who sent the request (ForeignKey to User)
- to_user: Who received it (ForeignKey to User)
- created_at: When request was sent (auto-set)
- NO STATUS FIELD! Requests are simply deleted when accepted/declined.

Design decision: When request is accepted:
1. Create TWO Friendship records (both directions)
2. DELETE the FriendRequest (don't update status)

Integration points:
- FriendsContext (Crystal's frontend) fetches and displays friends
- Friends.jsx shows friend list and pending requests

Expected response for GET /api/friends/:
[
  { "id": 2, "username": "alice", "first_name": "Alice", "last_name": "Smith" },
  { "id": 3, "username": "bob", "first_name": "Bob", "last_name": "Jones" }
]

Think about:
- How do you get all friends for a user? (Friendship.objects.filter(user=user))
- How do you prevent duplicate friendships? (unique_together constraint)
- How do you prevent self-friendship? (Validate in view)
- When accepting: create BOTH directions of friendship

Hint: user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships')
Hint: friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends_of')
Hint: created_at = models.DateTimeField(auto_now_add=True)
Hint: class Meta: unique_together = ['user', 'friend']
Hint: Add __str__ method: return f"{self.user.username} → {self.friend.username}"
"""

from django.db import models
from django.contrib.auth.models import User


class Friendship(models.Model):
    """
    TODO: Friendship model - user → friend (directional, not symmetric)
    
    Fields: user, friend, created_at
    Meta: unique_together, ordering
    """
    # Your code here
    pass


class FriendRequest(models.Model):
    """
    TODO: FriendRequest model - from_user, to_user, created_at (NO status field!)
    
    Fields: from_user, to_user, created_at
    Meta: unique_together, ordering
    """
    # Your code here
    pass
