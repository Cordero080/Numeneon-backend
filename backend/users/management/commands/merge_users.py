"""
One-time script to merge duplicate users.
Transfers posts and messages from old users to correct team accounts.

Usage: python manage.py merge_users
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from posts.models import Post, Like
from messages_app.models import Message


class Command(BaseCommand):
    help = 'Merge duplicate users: transfer posts/messages then delete old accounts'

    def handle(self, *args, **options):
        # Mapping: old username → new username (the one to keep)
        merges = [
            {'old': 'colinw', 'new': 'colin'},
            {'old': 'crystalr', 'new': 'crystal'},
            {'old': 'nataliap', 'new': 'natalia'},
        ]

        for merge in merges:
            old_username = merge['old']
            new_username = merge['new']
            
            # Check if old user exists
            try:
                old_user = User.objects.get(username=old_username)
            except User.DoesNotExist:
                self.stdout.write(f"⏭ Old user '{old_username}' not found, skipping")
                continue
            
            # Check if new user exists
            try:
                new_user = User.objects.get(username=new_username)
            except User.DoesNotExist:
                self.stdout.write(self.style.ERROR(f"✗ Target user '{new_username}' not found, skipping"))
                continue

            self.stdout.write(f"\n🔄 Merging {old_username} (id={old_user.id}) → {new_username} (id={new_user.id})")

            # Transfer posts
            posts_count = Post.objects.filter(author=old_user).update(author=new_user)
            self.stdout.write(f"   → Transferred {posts_count} posts")

            # Transfer likes
            likes_count = Like.objects.filter(user=old_user).update(user=new_user)
            self.stdout.write(f"   → Transferred {likes_count} likes")

            # Transfer messages (as sender)
            sent_count = Message.objects.filter(sender=old_user).update(sender=new_user)
            self.stdout.write(f"   → Transferred {sent_count} sent messages")

            # Transfer messages (as receiver)
            recv_count = Message.objects.filter(receiver=old_user).update(receiver=new_user)
            self.stdout.write(f"   → Transferred {recv_count} received messages")

            # Transfer profile data if exists
            try:
                old_profile = old_user.profile
                new_profile, _ = new_user.profile.__class__.objects.get_or_create(user=new_user)
                
                # Copy avatar and bio if new profile is empty
                if hasattr(old_profile, 'avatar') and old_profile.avatar and not new_profile.avatar:
                    new_profile.avatar = old_profile.avatar
                if hasattr(old_profile, 'bio') and old_profile.bio and not new_profile.bio:
                    new_profile.bio = old_profile.bio
                if hasattr(old_profile, 'location') and old_profile.location and not new_profile.location:
                    new_profile.location = old_profile.location
                new_profile.save()
                self.stdout.write(f"   → Transferred profile data")
            except Exception as e:
                self.stdout.write(f"   → Profile transfer skipped: {e}")

            # Delete old user
            old_user.delete()
            self.stdout.write(self.style.SUCCESS(f"   ✓ Deleted old user: {old_username}"))

        self.stdout.write(self.style.SUCCESS('\n✅ Merge complete!'))
        
        # Show remaining users
        self.stdout.write(f"\nRemaining users:")
        for user in User.objects.all().order_by('username'):
            post_count = Post.objects.filter(author=user).count()
            self.stdout.write(f"  {user.username}: {post_count} posts")
