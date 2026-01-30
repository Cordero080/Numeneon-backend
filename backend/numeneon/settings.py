# 🟠 TITO - Infrastructure Lead
# settings.py - Django configuration (CORS setup is critical!)

"""
settings.py - Django's config file (like Express app.js config section)

Configures database, middleware, installed apps, security, and environment vars.
Express equivalent: where you set up app.use(), db connection, env vars, cors, etc.
"""

from pathlib import Path

# Root directory path (like __dirname in Node)
BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key for encryption/hashing (like JWT_SECRET in Express)
# TODO: Move to .env file for production
SECRET_KEY = 'django-insecure-tl6jpad%y3%v%xria!-k=ez-=0h7wqz$ub=&a2*ka9veckq3p8'

# Debug mode - shows detailed errors (like NODE_ENV === 'development')
DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'numeneon-backend.onrender.com',
    '.onrender.com',  # Allow all Render subdomains
    '.vercel.app',  # Allow Vercel frontend for WebSocket connections
]

# INSTALLED_APPS - Django apps/plugins (like Express middleware & route modules)
# Add your custom apps here (e.g., 'api', 'users', 'posts')
INSTALLED_APPS = [
    'daphne', # ASGI server for WebSocket support
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',  # Serves static files (like express.static())
    # Third-party apps
    'rest_framework',
     'channels',
    'rest_framework_simplejwt',  # JWT authentication
    'corsheaders',  # <-- Added for CORS
    # Custom apps
    'users.apps.UsersConfig',
    'posts',
    'friends',
    'messages_app',  # Direct messaging
    'notifications',
    'myspace',
]

# MIDDLEWARE - Request/response pipeline (exactly like Express app.use() chain)
# Executes top-to-bottom on requests, bottom-to-top on responses
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # <-- Added for CORS (must be first)
    'django.middleware.security.SecurityMiddleware',      # Security headers (helmet in Express)
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session handling (express-session)
    'django.middleware.common.CommonMiddleware',           # Common HTTP features
    # 'django.middleware.csrf.CsrfViewMiddleware',         # DISABLED - using JWT, not cookies
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Attaches user to request
    'django.contrib.messages.middleware.MessageMiddleware',     # Flash messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   # X-Frame-Options header
]

# ROOT_URLCONF - Main routes file (like app.use('/api', routes) in Express)
ROOT_URLCONF = 'numeneon.urls'

# TEMPLATES - HTML templating config (we'll use React instead, so ignore this)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI server config (like http.createServer() in Node)
WSGI_APPLICATION = 'numeneon.wsgi.application'
ASGI_APPLICATION = 'numeneon.asgi.application' # For WebSocket support

# DATABASE - Connection config
import os
import dj_database_url

if os.environ.get('DATABASE_URL'):
    # Production: use Render's DATABASE_URL
    DATABASES = {
        'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
    }
else:
    # Local development: use localhost PostgreSQL
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'numeneon',
            'USER': '',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }

# Password validation rules (like bcrypt + validation middleware)
# Relaxed for development - tighten for production!
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        }
    },
]

# Localization settings
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files URL (like app.use('/static', express.static('public')))
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default ID field type for models (like MongoDB ObjectId or auto-increment in SQL)
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS - Allow React frontend to talk to Django
CORS_ALLOWED_ORIGINS = [
    'https://numeneon-frontend.vercel.app',
    'https://numeneon-backend.onrender.com',
]
# Allow any localhost port for development
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://numeneon-frontend.*\.vercel\.app$",
    r"^https://numeneon-frontend-.*\.vercel\.app$",
    r"^http://localhost:\d+$",  # Any localhost port
    r"^http://127\.0\.0\.1:\d+$",  # Any 127.0.0.1 port
]
# JWT goes in Authorization header, not cookies - no credentials needed
CORS_ALLOW_CREDENTIALS = False

# REST Framework settings - JWT only, no session auth = no CSRF needed
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# JWT Settings
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
# Channels (WebSocket) configuration
# Use Redis in production, InMemory for local development
import os
if os.environ.get('REDIS_URL'):
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [os.environ.get('REDIS_URL')],
            },
        },
    }
else:
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        },
    }
