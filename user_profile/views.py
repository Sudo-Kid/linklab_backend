from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied

from allauth.socialaccount.models import SocialAccount

from . import models
from . import serializers


class UserView(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfile

    def retrieve(self, request, pk=None, **_kwargs):
        user = get_object_or_404(self.queryset, user__username=pk)
        serializer = self.serializer_class(user)
        return Response(serializer.data)

    def update(self, request, pk=None, **kwargs):
        if request.user.username != pk:
            raise PermissionDenied(
                detail={'error': 'permission denied'},
                code=403
            )
        partial = kwargs.pop('partial', False)
        instance = get_object_or_404(self.queryset, user__username=pk)
        serializer = serializers.UpdateUserProfileSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(methods=['PATCH'], url_path='social', detail=True)
    def update_social_settings(self, request, pk=None, **kwargs):
        if request.user.username != pk:
            raise PermissionDenied(
                detail={'error': 'permission denied'},
                code=403
            )

        partial = kwargs.pop('partial', False)
        user = get_object_or_404(self.queryset, user__username=pk)
        instance = get_object_or_404(
            models.UserProfile.objects.all(),
            user=user.user
        )
        serializer = serializers.UpdateSocialDisplaySettingsSerializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    def create(self, request, **kwargs):
        user = models.UserProfile.objects.get(
            user__username=request.user.username)

        data = {
            'name': request.data['name'],
            'user': user.id,
            'username': request.data['username'],
            'position': request.data['position'],
            'limit': request.data['limit']
        }

        serializer = serializers.UpdateSocialDisplaySettingsSerializer(
            data=data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

