from django.db import models
from django.contrib.auth.models import User


class Template(models.Model):
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=256, default='default')

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    template = models.ForeignKey(Template, on_delete=models.PROTECT)
    discord = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self):
        return self.user.username


class SocialDisplaySettings(models.Model):
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField(max_length=256, default='twitch')
    limit = models.PositiveIntegerField(default=6)
    position = models.PositiveIntegerField(default=0, null=True)
    username = models.CharField(max_length=256, null=True, blank=True)
    user = models.ForeignKey(
        UserProfile, on_delete=models.PROTECT, null=True,
        blank=True, related_name='services')

    def __str__(self):
        return self.name + ' ' + self.user.user.username
