from django.db.models.signals import post_save # The signal sent AFTER a save
from django.contrib.auth.models import User    # The sender (the User model)
from django.dispatch import receiver           # The decorator to "catch" the signal
from .models import Profile                  # You'll import your Profile model here later

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        print(f"✅ Signal triggered: Creating profile for {instance.username}")
        Profile.objects.create(user=instance)