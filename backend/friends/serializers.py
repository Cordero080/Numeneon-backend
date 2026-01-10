# 🟣 CRYSTAL - Friends System Lead
# serializers.py - Data conversion between Django models and JSON
"""
TODO: Create Friends Serializers - format friendship data

You need serializers for:
1. FriendshipSerializer: Serializes Friendship with nested user/friend data
2. FriendRequestSerializer: Serializes FriendRequest with nested from_user/to_user

These serializers use UserSerializer from the users app for nested user data.

For FriendshipSerializer:
- user: nested UserSerializer (read_only)
- friend: nested UserSerializer (read_only)
- fields: id, user, friend, created_at
- read_only_fields: created_at

For FriendRequestSerializer:
- from_user: nested UserSerializer (read_only)
- to_user: nested UserSerializer (read_only)
- fields: id, from_user, to_user, created_at
- read_only_fields: created_at

NOTE: In views, you may build response dicts manually instead of using
these serializers for simple endpoints like friend_list. These serializers
are useful for more complex scenarios.

Think about:
- Import UserSerializer from users app
- Both serializers are read_only focused (no create via serializer)
- How do you make nested serializers read_only? (read_only=True parameter)

Hint: from users.serializers import UserSerializer
Hint: user = UserSerializer(read_only=True)
Hint: friend = UserSerializer(read_only=True)
"""

from rest_framework import serializers
from .models import Friendship, FriendRequest
from users.serializers import UserSerializer


class FriendshipSerializer(serializers.ModelSerializer):
    """
    TODO: Serializer for Friendship model - shows user and friend details
    
    Add nested serializers:
    - user = UserSerializer(read_only=True)
    - friend = UserSerializer(read_only=True)
    
    class Meta:
        model = Friendship
        fields = ['id', 'user', 'friend', 'created_at']
        read_only_fields = ['created_at']
    """
    # Your code here
    pass


class FriendRequestSerializer(serializers.ModelSerializer):
    """
    TODO: Serializer for FriendRequest model - shows who sent and received
    
    Add nested serializers:
    - from_user = UserSerializer(read_only=True)
    - to_user = UserSerializer(read_only=True)
    
    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'created_at']
        read_only_fields = ['created_at']
    """
    # Your code here
    pass
