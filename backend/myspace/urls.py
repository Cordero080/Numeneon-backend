from django.urls import path
from . import views

urlpatterns = [
    # Public - anyone can view
    path('<str:username>/', views.get_myspace_profile, name='myspace-profile'),

    # Authenticated - update your own settings
    path('', views.update_myspace_settings, name='myspace-update'),

    # Playlist management
    path('playlist/', views.add_song_to_playlist, name='playlist-add'),
    path('playlist/<int:song_id>/', views.remove_song_from_playlist, name='playlist-remove'),
    path('playlist/reorder/', views.reorder_playlist, name='playlist-reorder'),
]