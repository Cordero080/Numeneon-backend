# 🟣 CRYSTAL - Friends System Lead
# urls.py - URL routing for friends API endpoints
"""
TODO: Configure URL routes for friends API

Map each endpoint to its view function.
These URLs will be included in main urls.py under /api/friends/

Routes to create:
- GET /api/friends/ → friend_list view
- GET /api/friends/requests/ → pending_requests view
- POST /api/friends/request/<int:user_id>/ → send_request view
- POST /api/friends/accept/<int:request_id>/ → accept_request view
- POST /api/friends/decline/<int:request_id>/ → decline_request view
- DELETE /api/friends/remove/<int:user_id>/ → remove_friend view

Think about:
- Use <int:user_id> for URL parameters that are integers
- Each route maps to a view function

Hint: path('', views.friend_list, name='friend_list')
Hint: path('requests/', views.pending_requests, name='pending_requests')
Hint: path('request/<int:user_id>/', views.send_request, name='send_request')
Hint: path('accept/<int:request_id>/', views.accept_request, name='accept_request')
Hint: path('decline/<int:request_id>/', views.decline_request, name='decline_request')
Hint: path('remove/<int:user_id>/', views.remove_friend, name='remove_friend')
"""

from django.urls import path
from . import views

urlpatterns = [
    # Your code here
]