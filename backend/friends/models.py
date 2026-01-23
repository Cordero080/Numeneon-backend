# 🟣 CRYSTAL - Friends System Lead
# models.py - Database structure for friendships and friend requests
"""
Create Friendship models - friend connections and requests
"""

from django.db import models
from django.contrib.auth.models import User


class Friendship(models.Model):
    """
    Friendship model - user → friend (directional, not symmetric)
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friendships'
    )
    friend = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='friends_of'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} -> {self.friend.username}"


  


class FriendRequest(models.Model):
    """
    FriendRequest model - from_user, to_user, created_at (NO status field!)
    """
    from_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_requests'
    )
    to_user = models.ForeignKey(
      User,
      on_delete=models.CASCADE,
      related_name='received_requests'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.from_user.username} -> {self.to_user.username}"
