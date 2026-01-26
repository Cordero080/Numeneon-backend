# Step 7: Frontend Integration

> **Time:** ~15-30 minutes  
> **Target:** React frontend with existing JWT authentication

---

## Overview

This guide shows how to connect your React frontend to the WebSocket server and handle real-time notifications.

---

## Step 7.1: Create a WebSocket Service

Create a new file in your React project:

**File:** `src/services/websocket.js`

```javascript
/**
 * WebSocket Service for Real-Time Notifications
 *
 * Handles:
 * - Connection management with auto-reconnect
 * - JWT authentication via query string
 * - Event dispatching to React components
 */

class WebSocketService {
  constructor() {
    this.socket = null;
    this.listeners = {};
    this.reconnectAttempts = 0;
    this.maxReconnectAttempts = 5;
    this.reconnectDelay = 3000; // 3 seconds
  }

  /**
   * Connect to WebSocket server
   * @param {string} token - JWT access token
   */
  connect(token) {
    if (this.socket?.readyState === WebSocket.OPEN) {
      console.log("WebSocket already connected");
      return;
    }

    // Use wss:// for production (HTTPS), ws:// for local development
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const host = import.meta.env.VITE_API_URL
      ? new URL(import.meta.env.VITE_API_URL).host
      : "localhost:8000";

    const wsUrl = `${protocol}//${host}/ws/notifications/?token=${token}`;

    console.log("Connecting to WebSocket:", wsUrl.replace(token, "***"));

    this.socket = new WebSocket(wsUrl);

    this.socket.onopen = () => {
      console.log("✅ WebSocket connected");
      this.reconnectAttempts = 0;
      this.emit("connected", {});
    };

    this.socket.onmessage = (event) => {
      try {
        const message = JSON.parse(event.data);
        console.log("📩 WebSocket message:", message);

        // Emit event to all listeners of this type
        this.emit(message.type, message.data);
      } catch (error) {
        console.error("Failed to parse WebSocket message:", error);
      }
    };

    this.socket.onerror = (error) => {
      console.error("❌ WebSocket error:", error);
      this.emit("error", error);
    };

    this.socket.onclose = (event) => {
      console.log("🔌 WebSocket closed:", event.code, event.reason);
      this.emit("disconnected", { code: event.code, reason: event.reason });

      // Auto-reconnect if not intentionally closed
      if (
        event.code !== 1000 &&
        this.reconnectAttempts < this.maxReconnectAttempts
      ) {
        this.reconnectAttempts++;
        console.log(
          `Reconnecting in ${this.reconnectDelay}ms (attempt ${this.reconnectAttempts})`,
        );
        setTimeout(() => this.connect(token), this.reconnectDelay);
      }
    };
  }

  /**
   * Disconnect from WebSocket server
   */
  disconnect() {
    if (this.socket) {
      this.socket.close(1000, "Client disconnected");
      this.socket = null;
    }
  }

  /**
   * Add event listener
   * @param {string} event - Event type (e.g., 'friend_request', 'new_message')
   * @param {function} callback - Handler function
   * @returns {function} Unsubscribe function
   */
  on(event, callback) {
    if (!this.listeners[event]) {
      this.listeners[event] = [];
    }
    this.listeners[event].push(callback);

    // Return unsubscribe function
    return () => {
      this.listeners[event] = this.listeners[event].filter(
        (cb) => cb !== callback,
      );
    };
  }

  /**
   * Emit event to all listeners
   * @param {string} event - Event type
   * @param {object} data - Event data
   */
  emit(event, data) {
    if (this.listeners[event]) {
      this.listeners[event].forEach((callback) => callback(data));
    }
  }

  /**
   * Check if connected
   * @returns {boolean}
   */
  isConnected() {
    return this.socket?.readyState === WebSocket.OPEN;
  }
}

// Export singleton instance
export const wsService = new WebSocketService();
export default wsService;
```

---

## Step 7.2: Create a React Hook

**File:** `src/hooks/useWebSocket.js`

```javascript
import { useEffect, useCallback } from "react";
import { wsService } from "../services/websocket";

/**
 * Hook to connect to WebSocket and subscribe to events
 *
 * @param {string} token - JWT access token
 * @param {object} handlers - Event handlers { eventType: handlerFunction }
 *
 * @example
 * useWebSocket(token, {
 *   friend_request: (data) => console.log('New friend request!', data),
 *   new_message: (data) => console.log('New message!', data),
 * });
 */
export function useWebSocket(token, handlers = {}) {
  // Connect on mount, disconnect on unmount
  useEffect(() => {
    if (token) {
      wsService.connect(token);
    }

    return () => {
      // Don't disconnect on unmount - we want persistent connection
      // wsService.disconnect();
    };
  }, [token]);

  // Subscribe to events
  useEffect(() => {
    const unsubscribes = [];

    Object.entries(handlers).forEach(([event, handler]) => {
      const unsubscribe = wsService.on(event, handler);
      unsubscribes.push(unsubscribe);
    });

    return () => {
      unsubscribes.forEach((unsub) => unsub());
    };
  }, [handlers]);

  // Return connection status and manual controls
  return {
    isConnected: wsService.isConnected(),
    connect: useCallback(() => wsService.connect(token), [token]),
    disconnect: useCallback(() => wsService.disconnect(), []),
  };
}

export default useWebSocket;
```

---

## Step 7.3: Create a Notification Provider

**File:** `src/context/NotificationContext.jsx`

```jsx
import {
  createContext,
  useContext,
  useState,
  useEffect,
  useCallback,
} from "react";
import { wsService } from "../services/websocket";
import { useAuth } from "./AuthContext"; // Your existing auth context

const NotificationContext = createContext();

export function NotificationProvider({ children }) {
  const { token, user } = useAuth(); // Get token from your auth context
  const [notifications, setNotifications] = useState([]);
  const [unreadCount, setUnreadCount] = useState(0);

  // Connect to WebSocket when token is available
  useEffect(() => {
    if (token) {
      wsService.connect(token);
    }

    return () => {
      wsService.disconnect();
    };
  }, [token]);

  // Handle friend request notifications
  useEffect(() => {
    const unsubscribe = wsService.on("friend_request", (data) => {
      console.log("🔔 Friend request received:", data);

      const notification = {
        id: Date.now(),
        type: "friend_request",
        title: "New Friend Request",
        message: `${data.from_user.username} sent you a friend request`,
        data: data,
        read: false,
        timestamp: new Date(),
      };

      setNotifications((prev) => [notification, ...prev]);
      setUnreadCount((prev) => prev + 1);

      // Show browser notification if permitted
      if (Notification.permission === "granted") {
        new Notification("New Friend Request", {
          body: `${data.from_user.username} wants to be your friend`,
          icon: "/logo.png",
        });
      }
    });

    return unsubscribe;
  }, []);

  // Handle friend accepted notifications
  useEffect(() => {
    const unsubscribe = wsService.on("friend_accepted", (data) => {
      console.log("🔔 Friend request accepted:", data);

      const notification = {
        id: Date.now(),
        type: "friend_accepted",
        title: "Friend Request Accepted",
        message: `${data.friend.username} accepted your friend request`,
        data: data,
        read: false,
        timestamp: new Date(),
      };

      setNotifications((prev) => [notification, ...prev]);
      setUnreadCount((prev) => prev + 1);
    });

    return unsubscribe;
  }, []);

  // Handle new message notifications
  useEffect(() => {
    const unsubscribe = wsService.on("new_message", (data) => {
      console.log("🔔 New message received:", data);

      const notification = {
        id: Date.now(),
        type: "new_message",
        title: "New Message",
        message: `${data.sender.username}: ${data.content.substring(0, 50)}...`,
        data: data,
        read: false,
        timestamp: new Date(),
      };

      setNotifications((prev) => [notification, ...prev]);
      setUnreadCount((prev) => prev + 1);
    });

    return unsubscribe;
  }, []);

  // Mark notification as read
  const markAsRead = useCallback((notificationId) => {
    setNotifications((prev) =>
      prev.map((n) => (n.id === notificationId ? { ...n, read: true } : n)),
    );
    setUnreadCount((prev) => Math.max(0, prev - 1));
  }, []);

  // Mark all as read
  const markAllAsRead = useCallback(() => {
    setNotifications((prev) => prev.map((n) => ({ ...n, read: true })));
    setUnreadCount(0);
  }, []);

  // Clear all notifications
  const clearAll = useCallback(() => {
    setNotifications([]);
    setUnreadCount(0);
  }, []);

  const value = {
    notifications,
    unreadCount,
    markAsRead,
    markAllAsRead,
    clearAll,
  };

  return (
    <NotificationContext.Provider value={value}>
      {children}
    </NotificationContext.Provider>
  );
}

export function useNotifications() {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error(
      "useNotifications must be used within NotificationProvider",
    );
  }
  return context;
}
```

---

## Step 7.4: Add Provider to App

**File:** `src/App.jsx` (or your root component)

```jsx
import { NotificationProvider } from "./context/NotificationContext";
import { AuthProvider } from "./context/AuthContext";

function App() {
  return (
    <AuthProvider>
      <NotificationProvider>
        {/* Your existing app */}
        <Router>{/* ... */}</Router>
      </NotificationProvider>
    </AuthProvider>
  );
}
```

---

## Step 7.5: Create Notification Bell Component

**File:** `src/components/NotificationBell.jsx`

```jsx
import { useState } from "react";
import { useNotifications } from "../context/NotificationContext";

export function NotificationBell() {
  const { notifications, unreadCount, markAsRead, markAllAsRead } =
    useNotifications();
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="relative">
      {/* Bell Icon */}
      <button onClick={() => setIsOpen(!isOpen)} className="relative p-2">
        🔔
        {unreadCount > 0 && (
          <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
            {unreadCount}
          </span>
        )}
      </button>

      {/* Dropdown */}
      {isOpen && (
        <div className="absolute right-0 mt-2 w-80 bg-white shadow-lg rounded-lg z-50">
          <div className="p-3 border-b flex justify-between items-center">
            <h3 className="font-semibold">Notifications</h3>
            <button onClick={markAllAsRead} className="text-sm text-blue-500">
              Mark all read
            </button>
          </div>

          <div className="max-h-96 overflow-y-auto">
            {notifications.length === 0 ? (
              <p className="p-4 text-gray-500 text-center">No notifications</p>
            ) : (
              notifications.map((notification) => (
                <div
                  key={notification.id}
                  onClick={() => markAsRead(notification.id)}
                  className={`p-3 border-b cursor-pointer hover:bg-gray-50 ${
                    !notification.read ? "bg-blue-50" : ""
                  }`}
                >
                  <p className="font-medium">{notification.title}</p>
                  <p className="text-sm text-gray-600">
                    {notification.message}
                  </p>
                  <p className="text-xs text-gray-400">
                    {new Date(notification.timestamp).toLocaleTimeString()}
                  </p>
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}
```

---

## Step 7.6: Request Browser Notification Permission

Add this to your app initialization:

```javascript
// Request permission on app load
if ("Notification" in window && Notification.permission === "default") {
  Notification.requestPermission();
}
```

---

## Testing Locally

### Test 1: Connection

1. Start your Django server: `python manage.py runserver`
2. Login to your React app
3. Open browser console
4. Look for: `✅ WebSocket connected`

### Test 2: Friend Request

1. Open two browser windows (or use incognito)
2. Login as User A in Window 1
3. Login as User B in Window 2
4. From User A, send a friend request to User B
5. Watch Window 2's console for: `🔔 Friend request received`

### Test 3: Messages

1. Same setup as above
2. From User A, send a message to User B
3. Watch Window 2's console for: `🔔 New message received`

---

## Production Environment

Remember to set your environment variable:

```bash
# .env or .env.production
VITE_API_URL=https://numeneon-backend.onrender.com
```

The WebSocket service will automatically:

- Use `wss://` for production
- Use `ws://` for localhost

---

## ✅ Checklist

- [ ] Created `src/services/websocket.js`
- [ ] Created `src/hooks/useWebSocket.js`
- [ ] Created `src/context/NotificationContext.jsx`
- [ ] Added `NotificationProvider` to App
- [ ] Created `NotificationBell` component
- [ ] Tested WebSocket connection
- [ ] Tested friend request notifications
- [ ] Tested message notifications

---

## Next Steps

1. **Style the notification components** to match your app
2. **Add sound effects** for notifications
3. **Persist notifications** to localStorage or backend
4. **Add typing indicators** for real-time chat
5. **Add online/offline status** for friends

---

## Complete! 🎉

You now have a fully functional real-time notification system using Django Channels and WebSockets!
