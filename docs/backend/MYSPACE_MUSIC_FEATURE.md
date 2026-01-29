# MySpace Music Feature - Backend Implementation Guide

## Overview

Build a MySpace-style music player for user profiles with:
- **Profile Song** ("currently vibing to")
- **Playlist Display** with playback controls
- Songs stored in database, fetched from Spotify/Deezer API on frontend

---

## 1. Create the Django App

```bash
cd backend
python manage.py startapp myspace
```

---

## 2. Register the App

**File:** `backend/settings.py`

Add to `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    # ... existing apps
    'myspace',
]
```

---

## 3. Create Models

**File:** `backend/myspace/models.py`

```python
from django.db import models
from django.conf import settings


class MySpaceProfile(models.Model):
    """
    Extends user profile with MySpace-specific settings.
    One-to-one relationship with User.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='myspace_profile'
    )
    
    # Profile song - the "currently vibing to" track
    profile_song_title = models.CharField(max_length=255, blank=True, null=True)
    profile_song_artist = models.CharField(max_length=255, blank=True, null=True)
    profile_song_external_id = models.CharField(max_length=100, blank=True, null=True)  # Spotify/Deezer ID
    profile_song_preview_url = models.URLField(blank=True, null=True)  # 30-sec preview URL
    profile_song_album_art = models.URLField(blank=True, null=True)  # Album cover image
    
    # Optional: auto-play setting
    auto_play = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'MySpace Profile'
        verbose_name_plural = 'MySpace Profiles'

    def __str__(self):
        return f"{self.user.username}'s MySpace"


class PlaylistSong(models.Model):
    """
    Songs in a user's MySpace playlist.
    Order field allows drag-and-drop reordering.
    """
    myspace_profile = models.ForeignKey(
        MySpaceProfile,
        on_delete=models.CASCADE,
        related_name='playlist_songs'
    )
    
    # Song metadata (stored from API response)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    duration_ms = models.IntegerField(default=0)  # Duration in milliseconds
    external_id = models.CharField(max_length=100)  # Spotify/Deezer track ID
    preview_url = models.URLField(blank=True, null=True)  # 30-sec preview
    album_art = models.URLField(blank=True, null=True)  # Album cover
    
    # Playlist ordering
    order = models.PositiveIntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
        verbose_name = 'Playlist Song'
        verbose_name_plural = 'Playlist Songs'

    def __str__(self):
        return f"{self.title} by {self.artist}"
    
    @property
    def duration_formatted(self):
        """Return duration as M:SS or MM:SS string."""
        total_seconds = self.duration_ms // 1000
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"
```

---

## 4. Create Serializers

**File:** `backend/myspace/serializers.py`

```python
from rest_framework import serializers
from .models import MySpaceProfile, PlaylistSong


class PlaylistSongSerializer(serializers.ModelSerializer):
    duration = serializers.CharField(source='duration_formatted', read_only=True)
    
    class Meta:
        model = PlaylistSong
        fields = [
            'id',
            'title',
            'artist',
            'duration',
            'duration_ms',
            'external_id',
            'preview_url',
            'album_art',
            'order',
        ]
        read_only_fields = ['id']


class MySpaceProfileSerializer(serializers.ModelSerializer):
    playlist = PlaylistSongSerializer(source='playlist_songs', many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    
    # Profile song as nested object for cleaner frontend consumption
    profile_song = serializers.SerializerMethodField()
    
    class Meta:
        model = MySpaceProfile
        fields = [
            'id',
            'username',
            'profile_song',
            'profile_song_title',
            'profile_song_artist',
            'profile_song_external_id',
            'profile_song_preview_url',
            'profile_song_album_art',
            'auto_play',
            'playlist',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'username', 'created_at', 'updated_at']
    
    def get_profile_song(self, obj):
        """Return profile song as a structured object, or None."""
        if obj.profile_song_title:
            return {
                'title': obj.profile_song_title,
                'artist': obj.profile_song_artist,
                'external_id': obj.profile_song_external_id,
                'preview_url': obj.profile_song_preview_url,
                'album_art': obj.profile_song_album_art,
            }
        return None


class AddSongToPlaylistSerializer(serializers.Serializer):
    """Serializer for adding a song from Spotify/Deezer to playlist."""
    title = serializers.CharField(max_length=255)
    artist = serializers.CharField(max_length=255)
    duration_ms = serializers.IntegerField()
    external_id = serializers.CharField(max_length=100)
    preview_url = serializers.URLField(required=False, allow_null=True)
    album_art = serializers.URLField(required=False, allow_null=True)


class UpdateProfileSongSerializer(serializers.Serializer):
    """Serializer for setting the profile song."""
    title = serializers.CharField(max_length=255, required=False, allow_null=True)
    artist = serializers.CharField(max_length=255, required=False, allow_null=True)
    external_id = serializers.CharField(max_length=100, required=False, allow_null=True)
    preview_url = serializers.URLField(required=False, allow_null=True)
    album_art = serializers.URLField(required=False, allow_null=True)
    auto_play = serializers.BooleanField(required=False)
```

---

## 5. Create Views

**File:** `backend/myspace/views.py`

```python
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

from .models import MySpaceProfile, PlaylistSong
from .serializers import (
    MySpaceProfileSerializer,
    PlaylistSongSerializer,
    AddSongToPlaylistSerializer,
    UpdateProfileSongSerializer,
)

User = get_user_model()


def get_or_create_myspace_profile(user):
    """Helper to get or create a MySpace profile for a user."""
    profile, created = MySpaceProfile.objects.get_or_create(user=user)
    return profile


@api_view(['GET'])
@permission_classes([AllowAny])
def get_myspace_profile(request, username):
    """
    GET /api/myspace/<username>/
    
    Get a user's MySpace profile with their playlist.
    Public endpoint - anyone can view.
    """
    user = get_object_or_404(User, username=username)
    profile = get_or_create_myspace_profile(user)
    serializer = MySpaceProfileSerializer(profile)
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_myspace_settings(request):
    """
    PUT/PATCH /api/myspace/
    
    Update the authenticated user's MySpace settings.
    Can update profile song and auto_play setting.
    
    Request body example:
    {
        "title": "Song Name",
        "artist": "Artist Name",
        "external_id": "spotify:track:xxx",
        "preview_url": "https://...",
        "album_art": "https://...",
        "auto_play": true
    }
    
    To clear profile song, send null values:
    {
        "title": null,
        "artist": null
    }
    """
    profile = get_or_create_myspace_profile(request.user)
    serializer = UpdateProfileSongSerializer(data=request.data)
    
    if serializer.is_valid():
        data = serializer.validated_data
        
        # Update profile song fields if provided
        if 'title' in data:
            profile.profile_song_title = data['title']
        if 'artist' in data:
            profile.profile_song_artist = data['artist']
        if 'external_id' in data:
            profile.profile_song_external_id = data['external_id']
        if 'preview_url' in data:
            profile.profile_song_preview_url = data['preview_url']
        if 'album_art' in data:
            profile.profile_song_album_art = data['album_art']
        if 'auto_play' in data:
            profile.auto_play = data['auto_play']
        
        profile.save()
        
        return Response(MySpaceProfileSerializer(profile).data)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_song_to_playlist(request):
    """
    POST /api/myspace/playlist/
    
    Add a song to the authenticated user's playlist.
    
    Request body:
    {
        "title": "Song Name",
        "artist": "Artist Name",
        "duration_ms": 180000,
        "external_id": "spotify:track:xxx",
        "preview_url": "https://...",
        "album_art": "https://..."
    }
    """
    profile = get_or_create_myspace_profile(request.user)
    serializer = AddSongToPlaylistSerializer(data=request.data)
    
    if serializer.is_valid():
        data = serializer.validated_data
        
        # Check if song already in playlist (by external_id)
        if profile.playlist_songs.filter(external_id=data['external_id']).exists():
            return Response(
                {'error': 'Song already in playlist'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the next order number
        max_order = profile.playlist_songs.aggregate(
            max_order=models.Max('order')
        )['max_order'] or 0
        
        song = PlaylistSong.objects.create(
            myspace_profile=profile,
            title=data['title'],
            artist=data['artist'],
            duration_ms=data['duration_ms'],
            external_id=data['external_id'],
            preview_url=data.get('preview_url'),
            album_art=data.get('album_art'),
            order=max_order + 1
        )
        
        return Response(
            PlaylistSongSerializer(song).data,
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_song_from_playlist(request, song_id):
    """
    DELETE /api/myspace/playlist/<song_id>/
    
    Remove a song from the authenticated user's playlist.
    """
    profile = get_or_create_myspace_profile(request.user)
    song = get_object_or_404(PlaylistSong, id=song_id, myspace_profile=profile)
    song.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def reorder_playlist(request):
    """
    PATCH /api/myspace/playlist/reorder/
    
    Reorder songs in playlist.
    
    Request body:
    {
        "song_ids": [3, 1, 2]  // New order of song IDs
    }
    """
    profile = get_or_create_myspace_profile(request.user)
    song_ids = request.data.get('song_ids', [])
    
    if not song_ids:
        return Response(
            {'error': 'song_ids required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Update order for each song
    for index, song_id in enumerate(song_ids):
        profile.playlist_songs.filter(id=song_id).update(order=index)
    
    return Response(MySpaceProfileSerializer(profile).data)
```

**Note:** Add this import at the top of views.py:
```python
from django.db import models
```

---

## 6. Create URL Patterns

**File:** `backend/myspace/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    # Get user's MySpace profile (public)
    path('<str:username>/', views.get_myspace_profile, name='myspace-profile'),
    
    # Update own MySpace settings (authenticated)
    path('', views.update_myspace_settings, name='myspace-update'),
    
    # Playlist management (authenticated)
    path('playlist/', views.add_song_to_playlist, name='playlist-add'),
    path('playlist/<int:song_id>/', views.remove_song_from_playlist, name='playlist-remove'),
    path('playlist/reorder/', views.reorder_playlist, name='playlist-reorder'),
]
```

---

## 7. Register URLs in Main Router

**File:** `backend/urls.py`

Add to urlpatterns:
```python
from django.urls import path, include

urlpatterns = [
    # ... existing patterns
    path('api/myspace/', include('myspace.urls')),
]
```

---

## 8. Register Admin

**File:** `backend/myspace/admin.py`

```python
from django.contrib import admin
from .models import MySpaceProfile, PlaylistSong


class PlaylistSongInline(admin.TabularInline):
    model = PlaylistSong
    extra = 0
    ordering = ['order']


@admin.register(MySpaceProfile)
class MySpaceProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'profile_song_title', 'auto_play', 'created_at']
    search_fields = ['user__username', 'profile_song_title']
    inlines = [PlaylistSongInline]


@admin.register(PlaylistSong)
class PlaylistSongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'myspace_profile', 'order']
    list_filter = ['myspace_profile']
    search_fields = ['title', 'artist']
```

---

## 9. Create and Run Migrations

```bash
cd backend
python manage.py makemigrations myspace
python manage.py migrate
```

---

## 10. API Endpoints Summary

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| `GET` | `/api/myspace/<username>/` | No | Get user's MySpace profile + playlist |
| `PUT/PATCH` | `/api/myspace/` | Yes | Update own profile song & settings |
| `POST` | `/api/myspace/playlist/` | Yes | Add song to playlist |
| `DELETE` | `/api/myspace/playlist/<id>/` | Yes | Remove song from playlist |
| `PATCH` | `/api/myspace/playlist/reorder/` | Yes | Reorder playlist songs |

---

## 11. Example API Responses

### GET /api/myspace/johndoe/
```json
{
  "id": 1,
  "username": "johndoe",
  "profile_song": {
    "title": "Bohemian Rhapsody",
    "artist": "Queen",
    "external_id": "spotify:track:xxx",
    "preview_url": "https://p.scdn.co/mp3-preview/...",
    "album_art": "https://i.scdn.co/image/..."
  },
  "auto_play": false,
  "playlist": [
    {
      "id": 1,
      "title": "Bohemian Rhapsody",
      "artist": "Queen",
      "duration": "5:54",
      "duration_ms": 354000,
      "external_id": "spotify:track:xxx",
      "preview_url": "https://...",
      "album_art": "https://...",
      "order": 0
    },
    {
      "id": 2,
      "title": "Stairway to Heaven",
      "artist": "Led Zeppelin",
      "duration": "8:02",
      "duration_ms": 482000,
      "external_id": "spotify:track:yyy",
      "preview_url": "https://...",
      "album_art": "https://...",
      "order": 1
    }
  ],
  "created_at": "2026-01-29T10:00:00Z",
  "updated_at": "2026-01-29T12:30:00Z"
}
```

---

## 12. Frontend Integration Notes

Your `MusicPlayer.jsx` component will need to:

1. **Fetch profile on mount:**
   ```javascript
   GET /api/myspace/${username}/
   ```

2. **Map API response to your track structure:**
   ```javascript
   const tracks = response.playlist.map(song => ({
     id: song.id,
     title: song.title,
     artist: song.artist,
     duration: song.duration,
     previewUrl: song.preview_url,
     albumArt: song.album_art
   }));
   ```

3. **Add song from Spotify/Deezer search:**
   ```javascript
   POST /api/myspace/playlist/
   Body: { title, artist, duration_ms, external_id, preview_url, album_art }
   ```

---

## Quick Start Checklist

- [ ] Create app: `python manage.py startapp myspace`
- [ ] Add `'myspace'` to `INSTALLED_APPS` in settings.py
- [ ] Create models in `myspace/models.py`
- [ ] Create serializers in `myspace/serializers.py`
- [ ] Create views in `myspace/views.py`
- [ ] Create URLs in `myspace/urls.py`
- [ ] Add `path('api/myspace/', include('myspace.urls'))` to main urls.py
- [ ] Set up admin in `myspace/admin.py`
- [ ] Run `python manage.py makemigrations myspace`
- [ ] Run `python manage.py migrate`
- [ ] Test endpoints with Postman or curl

---

## Prompt for Claude

Copy this to get help building the feature:

```
I need to build a MySpace-style music feature for my Django backend. 

Here's the spec:
- Django REST Framework backend
- Two models: MySpaceProfile (one-to-one with User) and PlaylistSong (FK to MySpaceProfile)
- MySpaceProfile stores: profile song (title, artist, external_id, preview_url, album_art), auto_play setting
- PlaylistSong stores: title, artist, duration_ms, external_id, preview_url, album_art, order

Endpoints needed:
- GET /api/myspace/<username>/ - public, returns profile + playlist
- PUT /api/myspace/ - authenticated, update profile song settings
- POST /api/myspace/playlist/ - authenticated, add song
- DELETE /api/myspace/playlist/<id>/ - authenticated, remove song
- PATCH /api/myspace/playlist/reorder/ - authenticated, reorder songs

I'm storing song metadata from Spotify/Deezer API. The frontend will search the music API directly and send the track data to my backend to save.

Please help me implement this step by step.
```
