"""
TODO: Root URL configuration for NUMENEON backend

This file imports and includes all the app-specific URL patterns.
Each backend team member adds their app's URLs here.

COLLABORATIVE FILE - Each person adds ONE line:
- Natalia: Users/auth URLs at /api/auth/
- Colin: Posts URLs at /api/posts/
- Crystal: Friends URLs at /api/friends/

The admin URL is already configured.

Pattern: path('api/[prefix]/', include('[app].urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django Admin - already configured, don't modify
    path('admin/', admin.site.urls),

    # TODO (Natalia): Add users/auth URLs
    # Uncomment and verify after implementing users/urls.py:
    path('api/auth/', include('users.urls')),

    # TODO (Colin): Add posts URLs
    # Uncomment and verify after implementing posts/urls.py:
    # path('api/posts/', include('posts.urls')),

    # TODO (Crystal): Add friends URLs
    # Uncomment and verify after implementing friends/urls.py:
    # path('api/friends/', include('friends.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
