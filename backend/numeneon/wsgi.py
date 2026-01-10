"""
wsgi.py - Production server entry point (like server.listen() in Express)

WSGI = Web Server Gateway Interface (Python's standard for web servers)
Used by production servers like Gunicorn or uWSGI. Rarely touched.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'numeneon.settings')

application = get_wsgi_application()
