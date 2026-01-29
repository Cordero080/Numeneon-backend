from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import MySpaceProfile, PlaylistSong


class PlaylistSongInline(admin.TabularInline):
    """
    Shows playlist songs directly inside MySpaceProfile admin page.
    Instead of navigating to separate page, you see songs as a table.
    """
    model = PlaylistSong
    extra = 0  # Don't show empty rows for adding new songs
    ordering = ['order']  # Sort by playlist order


@admin.register(MySpaceProfile)
class MySpaceProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for MySpace profiles.
    """
    # Columns shown in the list view
    list_display = ['user', 'profile_song_title', 'auto_play', 'created_at']
    
    # Add search box at top
    search_fields = ['user__username', 'profile_song_title']
    
    # Show playlist songs inline (embedded in this page)
    inlines = [PlaylistSongInline]


@admin.register(PlaylistSong)
class PlaylistSongAdmin(admin.ModelAdmin):
    """
    Admin interface for individual playlist songs.
    """
    list_display = ['title', 'artist', 'myspace_profile', 'order']
    list_filter = ['myspace_profile']  # Filter dropdown by profile
    search_fields = ['title', 'artist']