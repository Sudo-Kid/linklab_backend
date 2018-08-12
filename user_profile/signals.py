from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User

from . import models


@receiver(post_save, sender=User)
def my_callback(instance, created, **_kwargs):
    if not created:
        return

    template = models.Template.objects.get(name='default')
    user_profile = models.UserProfile(
        user=instance,
        template=template
    )
    user_profile.save()
    social_display = models.SocialDisplaySettings(
        name='twitch',
        limit=6,
        position=0,
        username=user_profile.user.username,
        user=user_profile
    )
    social_display.save()
