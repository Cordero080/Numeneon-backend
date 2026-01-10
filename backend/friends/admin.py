# 🟣 CRYSTAL - Friends System Lead
# admin.py - Django admin interface for managing friendships
"""
TODO: Register Friends models with Django admin

Register both Friendship and FriendRequest models.
Useful for debugging friend connections.

Optional enhancements:
- list_display: Show columns in list view
- list_filter: Filter by created_at
- search_fields: Search by user__username, friend__username
- ordering: Sort by -created_at

Hint: admin.site.register(Friendship)
Hint: admin.site.register(FriendRequest)
Hint: Or use @admin.register decorator with ModelAdmin class
"""

from django.contrib import admin
from .models import Friendship, FriendRequest

# Your code here
