from django.db import models
from django.conf import settings


class MySpaceProfile(models.Model):
    """
    Extends user profile with MySpace-specific settings.
    One-to-one relationship with User.
    """
    
    # ===== RELATIONSHIP =====
    # Links this MySpace profile to a User (one profile per user)
    # CASCADE means: if user is deleted, delete their MySpace profile too
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='myspace_profile'
    )

    # ===== PROFILE SONG ("currently vibing to") =====
    # The main song displayed at top of profile
    profile_song_title = models.CharField(max_length=255, blank=True, null=True)
    profile_song_artist = models.CharField(max_length=255, blank=True, null=True)
    profile_song_external_id = models.CharField(max_length=100, blank=True, null=True)  # Spotify/Deezer ID
    profile_song_preview_url = models.URLField(blank=True, null=True)  # 30-second preview audio
    profile_song_album_art = models.URLField(blank=True, null=True)  # Album cover image

    # ===== SETTINGS =====
    # Should the profile song play automatically when someone visits?
    auto_play = models.BooleanField(default=False)

    # ===== TIMESTAMPS =====
    # auto_now_add=True: sets once when created, never changes
    # auto_now=True: updates every time the record is saved
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'MySpace Profile'
        verbose_name_plural = 'MySpace Profiles'

    def __str__(self):
        # How this object appears in admin and logs
        return f"{self.user.username}'s MySpace"


class PlaylistSong(models.Model):
    """
    Songs in a user's MySpace playlist.
    Order field allows drag-and-drop reordering.
    """
    
    # ===== RELATIONSHIP =====
    # Which MySpace profile owns this song
    # CASCADE: if profile deleted, delete all its songs
    # related_name='playlist_songs': lets you access songs via profile.playlist_songs.all()
    myspace_profile = models.ForeignKey(
        MySpaceProfile,
        on_delete=models.CASCADE,
        related_name='playlist_songs'
    )

    # ===== SONG METADATA =====
    # Data fetched from Spotify/Deezer API and stored here
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    duration_ms = models.IntegerField(default=0)  # Track length in milliseconds
    external_id = models.CharField(max_length=100)  # Spotify/Deezer track ID
    preview_url = models.URLField(blank=True, null=True)  # 30-second preview audio
    album_art = models.URLField(blank=True, null=True)  # Album cover image

    # ===== PLAYLIST ORDERING =====
    # Determines position in playlist (0 = first, 1 = second, etc.)
    # Used for drag-and-drop reordering
    order = models.PositiveIntegerField(default=0)

    # ===== TIMESTAMP =====
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Default sort: by order field, then by creation date
        ordering = ['order', 'created_at']
        verbose_name = 'Playlist Song'
        verbose_name_plural = 'Playlist Songs'

    def __str__(self):
        # How this object appears in admin and logs
        return f"{self.title} by {self.artist}"

    @property
    def duration_formatted(self):
        """
        Convert milliseconds to human-readable time.
        Example: 180000ms -> "3:00"
        """
        total_seconds = self.duration_ms // 1000  # Convert ms to seconds
        minutes = total_seconds // 60  # How many full minutes
        seconds = total_seconds % 60  # Remaining seconds
        return f"{minutes}:{seconds:02d}"  # :02d pads with zero (e.g., "3:05" not "3:5")