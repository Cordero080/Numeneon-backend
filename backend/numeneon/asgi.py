"""
asgi.py - Async server entry point (like Express + Socket.io setup)

ASGI = Async Server Gateway Interface (for WebSockets, async views)
Use this for real-time features. For basic REST APIs, ignore it.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'numeneon.settings')

application = get_asgi_application()
