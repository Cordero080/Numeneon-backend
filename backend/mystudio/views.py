from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.db import models
import requests

from .models import MyStudioProfile, PlaylistSong
from .serializers import (
    MyStudioProfileSerializer,
    PublicMyStudioProfileSerializer,
    PlaylistSongSerializer,
    AddSongToPlaylistSerializer,
    UpdateProfileSongSerializer,
)

# Get whatever User model your project uses (from settings.AUTH_USER_MODEL)
User = get_user_model()


def get_or_create_mystudio_profile(user):
    """
    Helper function: gets existing MyStudio profile or creates new one.
    Returns tuple: (profile_object, was_created_boolean)
    """
    profile, created = MyStudioProfile.objects.get_or_create(user=user)
    return profile


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_my_mystudio_profile(request):
    """
    GET /api/mystudio/profile/
    
    Get the current authenticated user's own MyStudio profile.
    """
    profile = get_or_create_mystudio_profile(request.user)
    serializer = PublicMyStudioProfileSerializer(profile)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def search_songs(request):
    """
    GET /api/mystudio/search/?q=song+name
    
    Search for songs using Deezer API. Returns tracks with preview URLs.
    """
    query = request.GET.get('q', '').strip()
    if not query:
        return Response({'error': 'Query parameter "q" is required'}, status=400)
    
    try:
        resp = requests.get(f'https://api.deezer.com/search?q={query}&limit=10', timeout=10)
        data = resp.json()
        
        results = []
        for track in data.get('data', []):
            results.append({
                'id': track.get('id'),
                'title': track.get('title'),
                'artist': track.get('artist', {}).get('name'),
                'album': track.get('album', {}).get('title'),
                'album_art': track.get('album', {}).get('cover_medium'),
                'preview_url': track.get('preview'),
                'duration_ms': track.get('duration', 0) * 1000,
                'external_id': str(track.get('id')),
            })
        
        return Response({'results': results})
    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])  # Only accepts GET requests
@permission_classes([AllowAny])  # Anyone can view (no login required)
def get_mystudio_profile(request, username):
    """
    GET /api/mystudio/<username>/
    
    Public endpoint - fetch any user's MyStudio profile + playlist.
    Used when visiting someone's profile page.
    
    Args:
        username: from URL path (e.g., /api/mystudio/pablo/)
    
    Returns:
        JSON with profile_song, playlist array, settings
    """
    # Get user or return 404 if doesn't exist
    user = get_object_or_404(User, username=username)
    
    # Get or create their MyStudio profile
    profile = get_or_create_mystudio_profile(user)
    
    # Use PublicMyStudioProfileSerializer for frontend-expected format
    serializer = PublicMyStudioProfileSerializer(profile)
    
    return Response(serializer.data)


@api_view(['PUT', 'PATCH'])  # Accepts both PUT (full update) and PATCH (partial update)
@permission_classes([IsAuthenticated])  # Must be logged in
def update_mystudio_settings(request):
    """
    PUT/PATCH /api/mystudio/
    
    Update YOUR OWN MyStudio settings (can't update someone else's).
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
    profile = get_or_create_mystudio_profile(request.user)
    
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
        if 'avatar' in data:
            profile.avatar = data['avatar'] or ''

        # Save changes to database
        profile.save()

        # Return updated profile as JSON
        return Response(MyStudioProfileSerializer(profile).data)

    # If validation failed, return errors with 400 status
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


MAX_PLAYLIST_SONGS = 5  # Top 5 songs limit


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_song_to_playlist(request):
    """
    POST /api/mystudio/playlist/
    
    Add a song to YOUR playlist (max 5 songs).
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
    profile = get_or_create_mystudio_profile(request.user)
    
    # Check playlist limit
    if profile.playlist_songs.count() >= MAX_PLAYLIST_SONGS:
        return Response(
            {'error': f'Playlist limit reached. Maximum {MAX_PLAYLIST_SONGS} songs allowed.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
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
    DELETE /api/mystudio/playlist/<song_id>/
    
    Remove a song from YOUR playlist.
    Can only delete your own songs (not someone else's).
    
    Args:
        song_id: from URL (e.g., /api/mystudio/playlist/5/)
    """
    profile = get_or_create_mystudio_profile(request.user)
    
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
    PATCH /api/mystudio/playlist/reorder/
    
    Reorder songs in YOUR playlist (drag-and-drop).
    
    Request body:
    {
        "song_ids": [3, 1, 2]  // New order: song 3 first, then 1, then 2
    }
    
    Frontend sends array of IDs in desired order.
    Backend updates 'order' field for each song.
    """
    profile = get_or_create_mystudio_profile(request.user)
    
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
    return Response(MyStudioProfileSerializer(profile).data)