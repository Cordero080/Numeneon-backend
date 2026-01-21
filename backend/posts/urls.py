# 🟢 COLIN - Posts Backend Lead
# urls.py - URL routing for posts API endpoints

from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet


router = DefaultRouter()
router.register(r"", PostViewSet, basename="post")

urlpatterns = [
    path("", include(router.urls)),
]
