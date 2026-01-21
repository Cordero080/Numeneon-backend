# 🟣 CRYSTAL - Friends System Lead
# urls.py - URL routing for friends API endpoints
"""
Configure URL routes for friends API
"""

from django.urls import path
from . import views

urlpatterns = [
    path('', views.friend_list, name='friend_list')
    path('requests/', views.pending_requests, name='pending_requests')
    path('request/<int:user_id>/', views.send_request, name='send_request')
    path('accept/<int:request_id>/', views.accept_request, name='accept_request')
    path('decline/<int:request_id>/', views.decline_request, name='decline_request')
    path('remove/<int:user_id>/', views.remove_friend, name='remove_friend')
    
]