# Step 2: Settings Configuration

> **Time:** ~10 minutes  
> **File:** `backend/numeneon/settings.py`

---

## Overview

You need to add:

1. `daphne` to INSTALLED_APPS (must be FIRST)
2. `channels` to INSTALLED_APPS
3. ASGI_APPLICATION setting
4. CHANNEL_LAYERS configuration

---

## Step 2.1: Add to INSTALLED_APPS

Open `backend/numeneon/settings.py` and find the `INSTALLED_APPS` list.

**Add `daphne` as the FIRST item** (this is important!):

```python
INSTALLED_APPS = [
    'daphne',  # <-- ADD THIS FIRST (must be before django apps)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'channels',  # <-- ADD THIS (after third-party apps)
    # Custom apps
    'users.apps.UsersConfig',
    'posts',
    'friends',
    'messages_app',
    'notifications',  # <-- ADD THIS (we'll create this app next)
]
```

### Why daphne must be first?

Daphne overrides Django's `runserver` command to support WebSockets. If it's not first, Django's default runserver runs instead.

---

## Step 2.2: Add ASGI_APPLICATION

Find this line in your settings:

```python
WSGI_APPLICATION = 'numeneon.wsgi.application'
```

Add the ASGI application setting **right after it**:

```python
WSGI_APPLICATION = 'numeneon.wsgi.application'
ASGI_APPLICATION = 'numeneon.asgi.application'  # <-- ADD THIS
```

### What's the difference?

- **WSGI** = Web Server Gateway Interface (HTTP only, synchronous)
- **ASGI** = Asynchronous Server Gateway Interface (HTTP + WebSocket, async)

---

## Step 2.3: Configure CHANNEL_LAYERS

Add this at the bottom of your settings.py (before the JWT settings section is fine):

```python
# ==========================================
# CHANNELS / WEBSOCKET CONFIGURATION
# ==========================================
import os

# Channel layer backend for WebSocket communication
if os.environ.get('REDIS_URL'):
    # Production: Use Redis for multi-process communication
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [os.environ.get('REDIS_URL')],
            },
        },
    }
else:
    # Development: Use in-memory layer (single process only)
    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels.layers.InMemoryChannelLayer',
        },
    }
```

### What is a Channel Layer?

Think of it like a **message bus**:

- When View A wants to send a notification to User B's WebSocket...
- View A publishes to the channel layer
- The channel layer delivers to the consumer handling User B's connection

**InMemoryChannelLayer:**

- Works within a single process
- Perfect for development
- Free, no setup required

**RedisChannelLayer:**

- Works across multiple processes/servers
- Required for production (Render runs multiple workers)
- Requires Redis server

---

## Step 2.4: Full Settings Reference

After all changes, these are the relevant sections in your settings.py:

```python
# Near the top - INSTALLED_APPS
INSTALLED_APPS = [
    'daphne',  # Must be first!
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'channels',
    # Custom apps
    'users.apps.UsersConfig',
    'posts',
    'friends',
    'messages_app',
    'notifications',
]

# After WSGI_APPLICATION
WSGI_APPLICATION = 'numeneon.wsgi.application'
ASGI_APPLICATION = 'numeneon.asgi.application'

# Near the bottom (before or after JWT settings)
# ==========================================
# CHANNELS / WEBSOCKET CONFIGURATION
# ==========================================
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
```

---

## Step 2.5: Test the Configuration

Run the development server:

```bash
cd backend
python manage.py runserver
```

You should see:

```
Starting ASGI/Daphne version 4.1.0 development server at http://127.0.0.1:8000/
```

**If you see "Starting ASGI/Daphne"** instead of "Starting development server", channels is configured correctly!

---

## ✅ Checklist

- [ ] Added `daphne` as FIRST item in INSTALLED_APPS
- [ ] Added `channels` to INSTALLED_APPS
- [ ] Added `notifications` to INSTALLED_APPS (we'll create this next)
- [ ] Added `ASGI_APPLICATION` setting
- [ ] Added `CHANNEL_LAYERS` configuration
- [ ] Tested with `runserver` and saw "ASGI/Daphne"

---

## ⚠️ Common Errors

**Error:** `ModuleNotFoundError: No module named 'notifications'`

- This is expected! We haven't created the notifications app yet.
- Temporarily comment out `'notifications'` from INSTALLED_APPS
- Run the server to test Daphne works
- Uncomment after creating the app in the next step

**Error:** `ImproperlyConfigured: Cannot import ASGI_APPLICATION module`

- Check that `ASGI_APPLICATION = 'numeneon.asgi.application'` is spelled correctly
- Make sure the asgi.py file exists at `backend/numeneon/asgi.py`

---

**Next Step:** [03-create-notifications-app.md](./03-create-notifications-app.md)
