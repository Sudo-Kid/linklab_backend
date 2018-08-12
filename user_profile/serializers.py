from django.conf import settings
from django.contrib.auth.models import User

from rest_framework import serializers

import requests

from allauth.socialaccount.models import SocialAccount

from . import models


class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Template
        fields = ('name', )


class SocialDisplaySettings(serializers.ModelSerializer):
    class Meta:
        model = models.SocialDisplaySettings
        fields = ('name', 'limit', )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', )


class UserProfile(serializers.ModelSerializer):
    services = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    class Meta:
        model = models.UserProfile
        fields = (
            'user',
            'services'
        )

    @staticmethod
    def get_youtube_videos(service):
        if service.username:
            user = service.username
        else:
            user = service.user.user.username

        response = requests.get(
            settings.GOOGLE_CHANNEL_API.format(
                user=user,
                YOUR_API_KEY=settings.GOOGLE_API_KEY
            )
        )

        response.raise_for_status()

        json = response.json()
        channel_id = json['items'][0]['id']
        playlist_id = json['items'][0]['contentDetails']['relatedPlaylists']['uploads']

        response = requests.get(
            settings.GOOGLE_PLAYLIST_API.format(
                playlist_id=playlist_id,
                YOUR_API_KEY=settings.GOOGLE_API_KEY
            )
        )

        response.raise_for_status()

        videos = response.json().get('items', [])

        if not videos:
            return

        youtube_url = 'https://www.youtube.com/watch?v='
        return_data = {
            'channel_url': 'https://www.youtube.com/channel/' + channel_id,
            'data': []
        }
        for video in videos[:6]:
            snippet = video['snippet']

            return_data['data'].append({
                'title': snippet['title'],
                'url': youtube_url + video['snippet']['resourceId']['videoId'],
                'thumbnails': video['snippet']['thumbnails']
            })

        return return_data

    @staticmethod
    def get_twitch_videos(service):
        twitch = SocialAccount.objects.get(
            provider='twitch', user=service.user.user)
        user_id = twitch.extra_data['_id']
        url = settings.TWITCH_VIDEO_API.format(user_id=user_id)
        header = {
            "Client-ID": settings.TWITCH_CLIENT_ID,
            "Accept": "application/vnd.twitchtv.v5+json",
            "scope": "openid channel_editor",
        }
        response = requests.get(url, headers=header)
        response.raise_for_status()
        return_data = {
            'channel_url': 'https://www.twitch.tv/' + twitch.extra_data['name'],
            'data': []
        }
        for video in response.json()['data']:
            title = video.get('title', '')
            url = video.get('url', '')
            t_url = video.get('thumbnail_url', '')
            thumbnails = {
                'default': {
                    'url': t_url.replace('%{width}', '120').replace('%{height}', '90')
                },
                'medium': {
                    'url': t_url.replace('%{width}', '320').replace('%{height}', '180')
                },
                'high': {
                    'url': t_url.replace('%{width}', '480').replace('%{height}', '360')
                },
                'standard': {
                    'url': t_url.replace('%{width}', '640').replace('%{height}', '480')
                },
                'maxres': {
                    'url': t_url.replace('%{width}', '1280').replace('%{height}', '720')
                },
            }
            return_data['data'].append({
                'title': title,
                'url': url,
                'thumbnails': thumbnails
            })
        return return_data

    def get_videos(self, service):
        if service.name == 'youtube':
            return self.get_youtube_videos(service)
        if service.name == 'twitch':
            return self.get_twitch_videos(service)
        else:
            return {}

    def get_services(self, obj):
        social_settings = {}
        for service in obj.services.all():
            # noinspection PyBroadException
            try:
                social_settings[service.name] = self.get_videos(service)
            except Exception:
                print('error')
                social_settings[service.name] = {}

        discord = obj.discord
        if discord:
            if discord.startswith('http'):
                social_settings['discord'] = {
                    'url': obj.discord
                }
            else:
                social_settings['discord'] = {
                    'url': 'https://discord.gg/' + obj.discord
                }
        return social_settings

    @staticmethod
    def get_user(obj):
        twitch = SocialAccount.objects.get(
            provider='twitch', user=obj.user)

        services_order = []
        for service in obj.services.all().order_by('position'):
            services_order.append(service.name)

        twitch_extra = twitch.extra_data
        twitch_extra.pop('partnered')
        twitch_extra.pop('email')
        twitch_extra.pop('notifications')
        twitch_extra.pop('_links')
        twitch_extra.pop('_id')
        twitch_extra['username'] = obj.user.username
        twitch_extra['template'] = obj.template.name
        twitch_extra['services_order'] = obj.template.name
        return twitch_extra


class UpdateUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        fields = ('template', 'discord')


class UpdateSocialDisplaySettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SocialDisplaySettings
        fields = ('name', 'limit', 'position', 'user', 'username')
