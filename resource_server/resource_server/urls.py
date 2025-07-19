"""
URL configuration for resource_server project.
"""
from django.contrib import admin
from django.urls import path, include, re_path
from photos.views import protected_photos
from django.conf import settings
from django.views.static import serve
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('photos/', protected_photos, name='photos'),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^photos/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),

    ]
