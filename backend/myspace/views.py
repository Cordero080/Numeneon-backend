from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import models

from .models import MySpaceProfile, PlaylistSong
from .serializers import (
    MySpaceProfileSerializer,
    PlaylistSongSerializer,
    AddSongToPlaylistSerializer,
    UpdateProfileSongSerializer,
)

# Get whatever User model your project uses (from settings.AUTH_USER_MODEL)
User = get_user_model()


def get_or_create_myspace_profile(user):
    """
    Helper function: gets existing MySpace profile or creates new one.
    Returns tuple: (profile_object, was_created_boolean)
    """
    profile, created = MySpaceProfile.objects.get_or_create(user=user)
    return profile


@api_view(['GET'])  # Only accepts GET requests
@permission_classes([AllowAny])  # Anyone can view (no login required)
def get_myspace_profile(request, username):
    """
    GET /api/myspace/<username>/
    
    Public endpoint - fetch any user's MySpace profile + playlist.
    Used when visiting someone's profile page.
    
    Args:
        username: from URL path (e.g., /api/myspace/pablo/)
    
    Returns:
        JSON with profile_song, playlist array, settings
    """
    # Get user or return 404 if doesn't exist
    user = get_object_or_404(User, username=username)
    
    # Get or create their MySpace profile
    profile = get_or_create_myspace_profile(user)
    
    # Convert Python object to JSON
    serializer = MySpaceProfileSerializer(profile)
    
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])  # Accepts both PUT (full update) and PATCH (partial update)
@permission_classes([IsAuthenticated])  # Must be logged in
def update_myspace_settings(request):
    """
    PUT/PATCH /api/myspace/
    
    Update YOUR OWN MySpace settings (can't update someone else's).
    Used for setting "currently vibing to" song and auto_play setting.
    
    Example request body:
    {
        "title": "Bohemian Rhapsody",
        "artist": "Queen",
        "external_id": "spotify:track:xxx",
        "preview_url": "https://...",
        "album_art": "https://...",
        "auto_play": false
    }
    
    To CLEAR profile song, send null:
    {
        "title": null,
        "artist": null
    }
    """
    # Get the logged-in user's profile
    profile = get_or_create_myspace_profile(request.user)
    
    # Validate incoming data
    serializer = UpdateProfileSongSerializer(data=request.data)

    if serializer.is_valid():
        # Extract validated data
        data = serializer.validated_data

        # Update only fields that were sent in request
        # 'in data' checks if key exists (could be null or a value)
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

        # Save changes to database
        profile.save()

        # Return updated profile as JSON
        return Response(MySpaceProfileSerializer(profile).data)

    # If validation failed, return errors with 400 status
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_song_to_playlist(request):
    """
    POST /api/myspace/playlist/
    
    Add a song to YOUR playlist.
    Frontend searches Spotify/Deezer, sends track data here to save.
    
    Request body:
    {
        "title": "Stairway to Heaven",
        "artist": "Led Zeppelin",
        "duration_ms": 482000,
        "external_id": "spotify:track:yyy",
        "preview_url": "https://...",
        "album_art": "https://..."
    }
    """
    profile = get_or_create_myspace_profile(request.user)
    
    # Validate incoming song data
    serializer = AddSongToPlaylistSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.validated_data

        # Prevent duplicate songs (check by external_id)
        if profile.playlist_songs.filter(external_id=data['external_id']).exists():
            return Response(
                {'error': 'Song already in playlist'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get highest order number in current playlist
        # If playlist empty, max_order will be None, so we use 'or 0'
        max_order = profile.playlist_songs.aggregate(
            max_order=models.Max('order')
        )['max_order'] or 0

        # Create new PlaylistSong at end of playlist
        song = PlaylistSong.objects.create(
            myspace_profile=profile,
            title=data['title'],
            artist=data['artist'],
            duration_ms=data['duration_ms'],
            external_id=data['external_id'],
            preview_url=data.get('preview_url'),  # .get() returns None if key doesn't exist
            album_art=data.get('album_art'),
            order=max_order + 1  # Add to end
        )

        # Return the new song as JSON with 201 Created status
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
    
    Remove a song from YOUR playlist.
    Can only delete your own songs (not someone else's).
    
    Args:
        song_id: from URL (e.g., /api/myspace/playlist/5/)
    """
    profile = get_or_create_myspace_profile(request.user)
    
    # Get song with matching ID AND belonging to this user
    # Returns 404 if not found or belongs to different user
    song = get_object_or_404(PlaylistSong, id=song_id, myspace_profile=profile)
    
    # Delete from database
    song.delete()
    
    # 204 No Content = success but no data to return
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def reorder_playlist(request):
    """
    PATCH /api/myspace/playlist/reorder/
    
    Reorder songs in YOUR playlist (drag-and-drop).
    
    Request body:
    {
        "song_ids": [3, 1, 2]  // New order: song 3 first, then 1, then 2
    }
    
    Frontend sends array of IDs in desired order.
    Backend updates 'order' field for each song.
    """
    profile = get_or_create_myspace_profile(request.user)
    
    # Extract array of song IDs from request
    song_ids = request.data.get('song_ids', [])

    if not song_ids:
        return Response(
            {'error': 'song_ids required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Update order field for each song
    # enumerate gives us (index, value) pairs: (0, 3), (1, 1), (2, 2)
    for index, song_id in enumerate(song_ids):
        # Update only songs that belong to this user
        profile.playlist_songs.filter(id=song_id).update(order=index)

    # Return updated profile with reordered playlist
    return Response(MySpaceProfileSerializer(profile).data)