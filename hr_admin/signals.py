# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        profile = instance.userprofile
    except UserProfile.DoesNotExist:
        # If the UserProfile doesn't exist, create it
        profile = UserProfile.objects.create(user=instance)

    # Now, save the profile
    profile.save()
