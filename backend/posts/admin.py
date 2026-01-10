# 🟢 COLIN - Posts Backend Lead
# admin.py - Django admin interface for managing posts
"""
TODO: Register Post model with Django admin

This allows you to view/edit posts in Django's admin interface.
Useful for debugging and managing test data.

Optional enhancements:
- list_display: Show columns in list view (id, author, type, created_at)
- list_filter: Filter by type, created_at
- search_fields: Search by author__username, content
- ordering: Sort by -created_at (newest first)
- readonly_fields: created_at, updated_at

Hint: from .models import Post
Hint: admin.site.register(Post)
Hint: Or use @admin.register(Post) decorator with ModelAdmin class for more control
"""

from django.contrib import admin
from .models import Post

# Your code here
