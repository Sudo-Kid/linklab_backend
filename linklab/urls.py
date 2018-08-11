from django.contrib import admin
from django.urls import path, include

from rest_framework.routers import DefaultRouter

from user_profile import views as user_views

router = DefaultRouter()
router.register(r'users', user_views.UserView, base_name='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('api/', include(router.urls)),
]
