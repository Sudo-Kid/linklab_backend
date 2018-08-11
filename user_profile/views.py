from rest_framework import viewsets

from . import models
from . import serializers


class UserView(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfile
