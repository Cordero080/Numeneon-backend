# Stretch Goal: Real-Time WebSockets

> **Status:** ✅ Implementation Guide Available!
> **Current Implementation:** Polling (every 30 seconds)
>
> **📚 Full Implementation Guide:** See [/docs/websockets/README.md](../websockets/README.md)

---

## What Are WebSockets?

**HTTP (what we use now):**

```
Client: "Any new messages?"     → Server: "No"
Client: "Any new messages?"     → Server: "No"
Client: "Any new messages?"     → Server: "Yes, here's one!"
Client: "Any new messages?"     → Server: "No"
```

The client keeps asking over and over (polling). Wasteful!

**WebSockets:**

```
Client: "I'm listening..."
         ↓
Server: (silence)
Server: (silence)
Server: "New message!" ← pushes instantly when it happens
Server: (silence)
Server: "Friend request!" ← pushes instantly
```

The connection stays open. Server pushes data the moment something happens.

---

## Why WebSockets Are Better

| Aspect          | Polling (Current)                    | WebSockets             |
| --------------- | ------------------------------------ | ---------------------- |
| **Latency**     | 0-30 second delay                    | Instant                |
| **Efficiency**  | Wastes requests checking for nothing | Only sends when needed |
| **Server Load** | High (constant requests)             | Low (idle until event) |
| **Complexity**  | Simple                               | Requires backend setup |

---

## What Would Need Real-Time Updates?

1. **Friend Requests** - See incoming requests instantly
2. **Messages** - Chat updates in real-time (like iMessage)
3. **Notifications** - Likes, comments, new followers
4. **Online Status** - Show who's currently active

---

## Implementation Plan (If We Had More Time)

### Backend (Django Channels)

1. **Install Django Channels:**

   ```bash
   pip install channels channels-redis
   ```

2. **Configure ASGI** (instead of WSGI):

   ```python
   # asgi.py
   from channels.routing import ProtocolTypeRouter, URLRouter
   from channels.auth import AuthMiddlewareStack

   application = ProtocolTypeRouter({
       "http": get_asgi_application(),
       "websocket": AuthMiddlewareStack(
           URLRouter(websocket_urlpatterns)
       ),
   })
   ```

3. **Create WebSocket Consumer:**

   ```python
   # consumers.py
   class NotificationConsumer(AsyncWebsocketConsumer):
       async def connect(self):
           self.user = self.scope["user"]
           await self.channel_layer.group_add(
               f"user_{self.user.id}",
               self.channel_name
           )
           await self.accept()

       async def send_notification(self, event):
           await self.send(text_data=json.dumps(event["data"]))
   ```

4. **Emit Events** when things happen:
   ```python
   # In views.py when friend request is sent
   channel_layer = get_channel_layer()
   async_to_sync(channel_layer.group_send)(
       f"user_{receiver.id}",
       {
           "type": "send_notification",
           "data": {"type": "friend_request", "from": sender.username}
       }
   )
   ```

### Frontend (React)

```jsx
// useWebSocket hook
useEffect(() => {
  const ws = new WebSocket(
    "wss://numeneon-backend.onrender.com/ws/notifications/",
  );

  ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    if (data.type === "friend_request") {
      // Update UI instantly
      refetchFriendRequests();
    }
  };

  return () => ws.close();
}, []);
```

---

## Why We Didn't Implement It

1. **Time constraints** - Capstone deadline
2. **Infrastructure** - Render free tier may not support WebSockets well
3. **Complexity** - Django Channels requires Redis for production
4. **Polling works** - 10-30 second delay is acceptable for a demo

---

## Resources for Future

- [Django Channels Documentation](https://channels.readthedocs.io/)
- [Channels Tutorial](https://channels.readthedocs.io/en/stable/tutorial/)
- [WebSockets on Render](https://render.com/docs/web-services#websocket-support)
