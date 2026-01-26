# WebSocket Implementation Guide for Numeneon

> **Goal:** Add real-time notifications for friend requests, friend acceptances, and messages using Django Channels.

---

## 📋 Overview

This guide will walk you through adding WebSocket support to the Numeneon backend. By the end, you'll have:

- Real-time friend request notifications
- Real-time friend acceptance notifications
- Real-time message notifications
- JWT authentication for WebSocket connections

---

## 🛠 Tech Stack Addition

| Component           | Purpose                                        |
| ------------------- | ---------------------------------------------- |
| **Django Channels** | WebSocket support for Django                   |
| **channels-redis**  | Channel layer backend (production)             |
| **daphne**          | ASGI server (replaces gunicorn for WebSockets) |

---

## 📂 Files to Create/Modify

### New Files to Create

| File                                  | Purpose                           |
| ------------------------------------- | --------------------------------- |
| `backend/notifications/`              | New Django app for WebSockets     |
| `backend/notifications/__init__.py`   | Package marker                    |
| `backend/notifications/consumers.py`  | WebSocket connection handler      |
| `backend/notifications/routing.py`    | WebSocket URL routing             |
| `backend/notifications/middleware.py` | JWT authentication for WebSockets |
| `backend/notifications/utils.py`      | Helper functions to emit events   |

### Files to Modify

| File                                  | Changes                                 |
| ------------------------------------- | --------------------------------------- |
| `requirements.txt`                    | Add channels, daphne, channels-redis    |
| `backend/numeneon/settings.py`        | Add Channels config, ASGI settings      |
| `backend/numeneon/asgi.py`            | Configure Channels routing              |
| `backend/friends/views.py`            | Emit WebSocket events                   |
| `backend/messages_app/serializers.py` | Emit WebSocket events on message create |

---

## 📖 Documentation Structure

1. **[01-installation.md](./01-installation.md)** - Install dependencies
2. **[02-settings-config.md](./02-settings-config.md)** - Configure Django settings
3. **[03-create-notifications-app.md](./03-create-notifications-app.md)** - Create the notifications app
4. **[04-modify-views.md](./04-modify-views.md)** - Add WebSocket events to existing views
5. **[05-asgi-config.md](./05-asgi-config.md)** - Configure ASGI routing
6. **[06-render-deployment.md](./06-render-deployment.md)** - Deploy to Render with WebSockets
7. **[07-frontend-integration.md](./07-frontend-integration.md)** - Connect from React frontend

---

## 🔄 How It Works (Architecture)

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (React)                        │
│  1. User logs in → gets JWT token                           │
│  2. Opens WebSocket: ws://localhost:8000/ws/notifications/  │
│     with token in query string                              │
│  3. Listens for events: friend_request, friend_accepted,    │
│     new_message                                             │
└─────────────────────┬───────────────────────────────────────┘
                      │ WebSocket Connection
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   BACKEND (Django Channels)                  │
│                                                              │
│  ┌──────────────────┐     ┌─────────────────────────────┐   │
│  │  NotificationConsumer  │     │  Channel Layer (Redis)     │   │
│  │  - authenticate()      │     │  - Groups: user_1, user_2  │   │
│  │  - connect()           │     │  - Pub/Sub messaging       │   │
│  │  - disconnect()        │     └─────────────────────────────┘   │
│  │  - receive()           │                 ▲                │
│  └──────────┬─────────────┘                 │                │
│             │                               │                │
│             │ subscribes to               emit event        │
│             │ group "user_{id}"            to group         │
│             ▼                               │                │
│  ┌─────────────────────────────────────────┴────────────┐   │
│  │                  REST API Views                       │   │
│  │  - send_request() → emit "friend_request"            │   │
│  │  - accept_request() → emit "friend_accepted"         │   │
│  │  - MessageSerializer.create() → emit "new_message"   │   │
│  └───────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Event Types

### 1. Friend Request Sent

```json
{
  "type": "friend_request",
  "data": {
    "request_id": 123,
    "from_user": {
      "id": 1,
      "username": "alice",
      "first_name": "Alice",
      "last_name": "Smith"
    },
    "created_at": "2025-01-26T10:30:00Z"
  }
}
```

### 2. Friend Request Accepted

```json
{
  "type": "friend_accepted",
  "data": {
    "friend": {
      "id": 2,
      "username": "bob",
      "first_name": "Bob",
      "last_name": "Jones"
    }
  }
}
```

### 3. New Message

```json
{
  "type": "new_message",
  "data": {
    "id": 456,
    "sender": {
      "id": 1,
      "username": "alice"
    },
    "content": "Hey, how are you?",
    "created_at": "2025-01-26T10:30:00Z"
  }
}
```

---

## ⏱ Estimated Time

| Step                     | Time           |
| ------------------------ | -------------- |
| Installation             | 5 min          |
| Settings config          | 10 min         |
| Create notifications app | 20 min         |
| Modify views             | 15 min         |
| ASGI config              | 10 min         |
| Testing locally          | 15 min         |
| Render deployment        | 20 min         |
| **Total**                | **~1.5 hours** |

---

## 🚀 Quick Start

If you want to get started immediately, follow these steps in order:

```bash
# 1. Install dependencies
pip install channels daphne channels-redis

# 2. Add to requirements.txt
echo "channels==4.0.0" >> requirements.txt
echo "daphne==4.1.0" >> requirements.txt
echo "channels-redis==4.2.0" >> requirements.txt

# 3. Follow the docs in order:
#    01-installation.md
#    02-settings-config.md
#    03-create-notifications-app.md
#    04-modify-views.md
#    05-asgi-config.md
#    06-render-deployment.md
```

---

## 🧪 Testing Locally

After implementation, test with this Python script or browser console:

```javascript
// Browser console test
const token = "your-jwt-token-here";
const ws = new WebSocket(
  `ws://localhost:8000/ws/notifications/?token=${token}`,
);

ws.onopen = () => console.log("Connected!");
ws.onmessage = (e) => console.log("Event:", JSON.parse(e.data));
ws.onerror = (e) => console.error("Error:", e);
ws.onclose = () => console.log("Disconnected");
```

---

## ❓ FAQ

**Q: Do I need Redis for local development?**
A: No! We use `InMemoryChannelLayer` for local dev. Redis is only needed for production.

**Q: Will this break my existing REST API?**
A: No! REST API continues to work exactly the same. WebSockets are additive.

**Q: What about CORS for WebSockets?**
A: WebSockets don't use CORS. The browser sends the Origin header, and you can check it in the consumer if needed.

**Q: Can I test without the frontend?**
A: Yes! Use the browser console JavaScript above, or tools like `websocat` or Postman.

---

**Next Step:** Start with [01-installation.md](./01-installation.md)
