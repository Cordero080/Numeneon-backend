# 🟢 COLIN - Posts Backend Lead
# urls.py - URL routing for posts API endpoints
"""
TODO: Configure URL routes for posts API

Use Django REST Framework's router for automatic URL generation.
Router creates all CRUD URLs from your ViewSet automatically.

Routes created by router:
- GET /api/posts/ - list
- POST /api/posts/ - create
- GET /api/posts/:id/ - retrieve
- PUT /api/posts/:id/ - update
- PATCH /api/posts/:id/ - partial_update
- DELETE /api/posts/:id/ - destroy

Plus your custom @action endpoints:
- GET /api/posts/:id/replies/
- POST /api/posts/:id/like/
- POST /api/posts/:id/share/

Think about:
- DefaultRouter vs SimpleRouter? (DefaultRouter adds API root view)
- How do you register a ViewSet with router?

Hint: from rest_framework.routers import DefaultRouter
Hint: router = DefaultRouter()
Hint: router.register(r'', PostViewSet, basename='post')
Hint: urlpatterns = [path('', include(router.urls))]
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Your code here - create router and register ViewSet
urlpatterns = [
    # Include router.urls here
]