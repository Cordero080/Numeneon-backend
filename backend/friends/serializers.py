# 🟣 CRYSTAL - Friends System Lead
# serializers.py - Data conversion between Django models and JSON
"""
Create Friends Serializers - format friendship data
"""

from rest_framework import serializers
from .models import Friendship, FriendRequest
from users.serializers import UserSerializer


class FriendshipSerializer(serializers.ModelSerializer):
    """
    Serializer for Friendship model - shows user and friend details
    """

    user = UserSerializer(read_only=True)
    friend = UserSerializer(read_only=True)

    class Meta:
        model = Friendship
        fields = ['id', 'user', 'friend', 'created_at']
        read_only_fields = ['created_at']

  

class FriendRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for FriendRequest model - shows who sent and received
    """
    
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)


    class Meta:
        model = FriendRequest
        fields = ['id', 'from_user', 'to_user', 'created_at']
        read_only_fields = ['created_at']


