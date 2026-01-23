from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Admin interface for viewing and managing user profiles"""
    list_display = ('id', 'user', 'location', 'created_at', 'updated_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'bio', 'location')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')