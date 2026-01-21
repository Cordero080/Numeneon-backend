# 🟢 COLIN - Posts Backend Lead
# admin.py - Django admin interface for managing posts

from django.contrib import admin
from .models import Post, Like


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "type", "created_at")
    list_filter = ("type", "created_at", "author")
    search_fields = ("author__username", "content")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username",)

