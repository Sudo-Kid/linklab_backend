from functools import reduce

from django.contrib.auth.models import User
from rest_framework import serializers

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
    services_order = serializers.SerializerMethodField()
    user = UserSerializer(many=False)

    class Meta:
        model = models.UserProfile
        fields = (
            'user',
            'template',
            'services',
            'services_order'
        )

    @staticmethod
    def get_services(obj):
        social_settings = {}
        for site in obj.services.all():
            social_settings[site.name] = {
                "limit": site.limit,
            }
        return social_settings

    @staticmethod
    def get_services_order(obj):
        social_settings = []
        for site in obj.services.all():
            social_settings.append(site.name)
        return social_settings
