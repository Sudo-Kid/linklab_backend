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
    social_display_settings = SocialDisplaySettings(many=True)
    user = UserSerializer(many=False)

    class Meta:
        model = models.UserProfile
        fields = ('user', 'template', 'social_display_settings')
