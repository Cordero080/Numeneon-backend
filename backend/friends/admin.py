# 🟣 CRYSTAL - Friends System Lead
# admin.py - Django admin interface for managing friendships
"""
Register Friends models with Django admin
"""

from django.contrib import admin
from .models import Friendship, FriendRequest

@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'friend', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'friend__username')
    ordering = ('created_at',)


@admin.register(FriendRequest)
class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'from_user', 'to_user', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('from_user__username', 'to_user__username')
    ordering = ('-created_at',)