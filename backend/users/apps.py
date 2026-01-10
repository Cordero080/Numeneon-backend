# 🟡 NATALIA - Auth & Users Lead
# apps.py - Django app configuration
"""
TODO: Django app configuration for users app

This is minimal boilerplate. Just configure the app name.

Hint: Django generates most of this automatically
"""

from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # Optional: Add ready() method if using signals for auto-creating profiles
