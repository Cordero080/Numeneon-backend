# 🟡 NATALIA - Auth & Users Lead
# urls.py - URL routing for authentication endpoints
"""
TODO: Configure URL routes for authentication endpoints

This file maps URLs to view functions.
These URLs will be included in the main urls.py under /api/auth/

Routes to create:
- POST /api/auth/signup/ → signup view
- POST /api/auth/login/ → email_login view  
- GET /api/auth/me/ → current_user view
- POST /api/auth/token/refresh/ → JWT token refresh (from simplejwt)

The token refresh endpoint is provided by simplejwt library.

Think about:
- Do you use path() or include() here? (path() for each route)
- How do you import views from the same app? (from .views import ...)
- Should the trailing slash be included? (Yes, Django convention)

Hint: from django.urls import path
Hint: from rest_framework_simplejwt.views import TokenRefreshView
Hint: path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
Hint: path('signup/', views.signup, name='signup')
Hint: path('login/', views.email_login, name='login')
Hint: path('me/', views.current_user, name='current_user')
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Your code here
]
