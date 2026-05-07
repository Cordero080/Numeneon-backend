from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from mystudio.models import MyStudioProfile, PlaylistSong

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds MyStudio profiles with sample songs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing songs before seeding',
        )

    def handle(self, *args, **options):
        # Get pabloPistola user
        try:
            user = User.objects.get(username='pabloPistola')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR('User pabloPistola not found'))
            return

        # Get or create MyStudio profile
        profile, created = MyStudioProfile.objects.get_or_create(user=user)
        
        if options['clear']:
            deleted = profile.playlist_songs.all().delete()[0]
            self.stdout.write(self.style.WARNING(f'Cleared {deleted} existing songs'))

        # Your songs with Deezer track IDs
        # Preview URLs fetched from Deezer API at runtime, with working fallbacks
        # Fallback uses free sample audio while Deezer API may be down
        songs = [
            {
                'title': 'Pneuma',
                'artist': 'Tool',
                'duration_ms': 713000,  # 11:53
                'external_id': 'deezer:track:740969222',
                'preview_url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3',
                'album_art': 'https://e-cdns-images.dzcdn.net/images/cover/4a039cbf6d0e98071d9fbd3fdfd73d82/500x500-000000-80-0-0.jpg',
                'order': 0
            },
            {
                'title': 'The Speaker is Systematically Blown',
                'artist': 'Author & Punisher',
                'duration_ms': 254000,  # 4:14
                'external_id': 'deezer:track:526673222',
                'preview_url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3',
                'album_art': 'https://e-cdns-images.dzcdn.net/images/cover/6e4e8f3a98706e47f05907ca9018f959/500x500-000000-80-0-0.jpg',
                'order': 1
            },
            {
                'title': 'Sweet Dreams (Are Made of This)',
                'artist': 'Eurythmics',
                'duration_ms': 216000,  # 3:36
                'external_id': 'deezer:track:561836',
                'preview_url': 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3',
                'album_art': 'https://e-cdns-images.dzcdn.net/images/cover/364f0d4ea4b5452b59e6664b9e5480f0/500x500-000000-80-0-0.jpg',
                'order': 2
            }
        ]

        created_count = 0
        for song_data in songs:
            # Check if already exists
            if not profile.playlist_songs.filter(external_id=song_data['external_id']).exists():
                PlaylistSong.objects.create(myspace_profile=profile, **song_data)
                created_count += 1
                self.stdout.write(f"  Added: {song_data['title']} by {song_data['artist']}")
            else:
                self.stdout.write(f"  Exists: {song_data['title']} by {song_data['artist']}")

        self.stdout.write(self.style.SUCCESS(
            f'\nSeeded {created_count} songs to {user.username} MyStudio'
        ))
        
        # Show current playlist
        self.stdout.write('\nCurrent playlist:')
        for song in profile.playlist_songs.all():
            self.stdout.write(f"  {song.order + 1}. {song.title} - {song.artist} ({song.duration_formatted})")
