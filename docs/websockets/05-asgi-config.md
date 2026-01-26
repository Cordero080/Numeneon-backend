# Step 5: ASGI Configuration

> **Time:** ~10 minutes  
> **File:** `backend/numeneon/asgi.py`

---

## Overview

The ASGI application is the entry point for both HTTP and WebSocket requests. We need to configure it to:

1. Route HTTP requests to Django
2. Route WebSocket requests to Channels consumers
3. Apply our JWT authentication middleware

---

## Step 5.1: Update asgi.py

**File:** `backend/numeneon/asgi.py`

Replace the entire contents with:

```python
"""
asgi.py - Async Server Gateway Interface

This is the entry point for both HTTP and WebSocket connections.
- HTTP requests → Django views (REST API)
- WebSocket requests → Channels consumers (real-time notifications)
"""

import os
from django.core.asgi import get_asgi_application

# ⚠️ IMPORTANT: Set this BEFORE importing anything else from Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'numeneon.settings')

# Initialize Django ASGI application early to ensure AppRegistry is populated
# This MUST happen before importing consumers or routing
django_asgi_app = get_asgi_application()

# Now we can safely import Channels components
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from notifications.middleware import JWTAuthMiddleware
from notifications.routing import websocket_urlpatterns


application = ProtocolTypeRouter({
    # HTTP requests go to Django
    "http": django_asgi_app,

    # WebSocket requests go through our auth middleware, then to URL router
    "websocket": AllowedHostsOriginValidator(
        JWTAuthMiddleware(
            URLRouter(
                websocket_urlpatterns
            )
        )
    ),
})
```

---

## Understanding the Configuration

### ProtocolTypeRouter

Routes requests based on protocol type:

- `"http"` → Regular Django views
- `"websocket"` → Channels consumers

```python
ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": ...
})
```

### AllowedHostsOriginValidator

Security wrapper that checks the `Origin` header against `ALLOWED_HOSTS`:

- Prevents WebSocket connections from unauthorized origins
- Uses the same `ALLOWED_HOSTS` setting from `settings.py`

```python
AllowedHostsOriginValidator(
    ...  # Wrapped content
)
```

### JWTAuthMiddleware

Our custom middleware that:

1. Extracts JWT token from query string
2. Validates the token
3. Attaches user to `scope['user']`

```python
JWTAuthMiddleware(
    URLRouter(...)
)
```

### URLRouter

Routes WebSocket URLs to consumers (like Django's URL routing):

```python
URLRouter(
    websocket_urlpatterns  # From notifications/routing.py
)
```

---

## Request Flow Diagram

```
Client Request
      │
      ▼
┌─────────────────────┐
│  ProtocolTypeRouter │
└──────────┬──────────┘
           │
     ┌─────┴─────┐
     │           │
   HTTP       WebSocket
     │           │
     ▼           ▼
┌─────────┐  ┌───────────────────────┐
│ Django  │  │ AllowedHostsValidator │
│  ASGI   │  └───────────┬───────────┘
└─────────┘              │
     │                   ▼
     │           ┌───────────────────┐
     │           │ JWTAuthMiddleware │
     │           │   - Extract token │
     │           │   - Validate JWT  │
     │           │   - Set user      │
     │           └───────────┬───────┘
     │                       │
     │                       ▼
     │               ┌───────────────┐
     │               │   URLRouter   │
     │               │ /ws/notif/ →  │
     │               └───────┬───────┘
     │                       │
     ▼                       ▼
┌─────────┐          ┌────────────────────┐
│  Views  │          │ NotificationConsumer│
│ (REST)  │          │   (WebSocket)      │
└─────────┘          └────────────────────┘
```

---

## Why Import Order Matters

Notice this comment in the code:

```python
# ⚠️ IMPORTANT: Set this BEFORE importing anything else from Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'numeneon.settings')

# Initialize Django ASGI application early to ensure AppRegistry is populated
django_asgi_app = get_asgi_application()

# Now we can safely import Channels components
from channels.routing import ...
```

This order is **critical** because:

1. Django apps must be configured before importing models/consumers
2. `get_asgi_application()` initializes the Django app registry
3. Consumers may import Django models, which require the registry

---

## Testing the Configuration

After updating asgi.py, run:

```bash
cd backend
python manage.py runserver
```

You should see:

```
Starting ASGI/Daphne version 4.1.0 development server at http://127.0.0.1:8000/
```

### Test WebSocket Connection

Open browser console and run:

```javascript
// Replace with actual JWT token from login
const token = "your-jwt-token";
const ws = new WebSocket(
  `ws://localhost:8000/ws/notifications/?token=${token}`,
);

ws.onopen = () => console.log("✅ Connected!");
ws.onmessage = (e) => console.log("📩 Message:", JSON.parse(e.data));
ws.onerror = (e) => console.error("❌ Error:", e);
ws.onclose = (e) => console.log("🔌 Closed:", e.code);
```

Expected result:

```
✅ Connected!
📩 Message: {type: 'connection_established', message: 'Connected as alice', user_id: 1}
```

---

## Troubleshooting

### Error: `ModuleNotFoundError: No module named 'notifications'`

The notifications app hasn't been created yet. Make sure you:

1. Ran `python manage.py startapp notifications`
2. Created all the files in Step 3
3. Added `'notifications'` to `INSTALLED_APPS`

### Error: `ImproperlyConfigured: Requested setting DEFAULT_INDEX_TABLESPACE`

You're importing Django modules before calling `django.setup()` or `get_asgi_application()`.

Check that your import order matches the example above.

### Error: `WebSocket connection to 'ws://...' failed`

1. Check the server is running
2. Check the URL is correct (`ws://localhost:8000/ws/notifications/`)
3. Check the token is valid
4. Check browser console for more details

### No error but connection closes immediately

The JWT token might be invalid or expired. Check:

1. The token is from a recent login
2. The token format is correct (just the token, no "Bearer " prefix)

---

## ✅ Checklist

- [ ] Updated `backend/numeneon/asgi.py` with the new configuration
- [ ] Verified import order (os.environ → get_asgi_application → other imports)
- [ ] Server starts with "ASGI/Daphne" message
- [ ] Can connect via WebSocket (test in browser console)

---

**Next Step:** [06-render-deployment.md](./06-render-deployment.md)
