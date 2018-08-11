from django.contrib import admin

from . import models

admin.site.register(models.Template)
admin.site.register(models.UserProfile)
admin.site.register(models.SocialDisplaySettings)
