# 🟡 NATALIA - Auth & Users Lead
# models.py - Extended user profile data
"""
TODO: Create the Profile model - extends Django's built-in User

NUMENEON needs to store extra info about users beyond username/email/password.
Django's built-in User model handles auth, but we need to add:
- Profile picture (for display in posts, TopBar, ProfileCard)
- Bio (for the profile page)

Two approaches exist:
1. Extend AbstractUser (replace Django's User entirely)
2. Create Profile model with OneToOneField to User (recommended - simpler)

We recommend approach #2: Create a Profile that links to User.

Fields you need:
- user: OneToOne link to Django's User model
- avatar: URL field (optional - users might not upload one)
- bio: Text field (optional - can be blank)
- location: CharField for user's location (optional)
- website: URLField for user's website (optional)
- created_at: When profile was created
- updated_at: When profile was last modified

Integration points:
- Posts reference User as author (Colin's Post.author field)
- Frontend ProfileCard displays avatar and bio
- TopBar shows current user's avatar
- Serializers need to combine User + Profile data

Think about:
- What happens when a new User is created? (Signal to auto-create Profile?)
- How do you handle optional fields? (blank=True)
- Should bio have a max length? (Probably yes - prevents abuse)
- What if user has no avatar? (Frontend needs to handle null)

Hint: Use OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
Hint: For URLs: URLField(max_length=500, blank=True)
Hint: Add __str__ method to return username for admin readability
Hint: For timestamps: auto_now_add=True (created), auto_now=True (updated)
"""

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.URLField(max_length=500, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=100, blank=True)
    website = models.URLField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username