# 👤 Crystal | M | Friends System

> Friend relationships, requests, and Friends page UI

---

## 🏷️ T-Shirt Size: M (12 files)

**Role:** Friends System Lead  
**Strengths:** Backend + Frontend  
**Focus:** Social connections, friend requests, relationship management

---

## 📋 Task Board

### 🔴 BACKEND - CRITICAL PATH

| ID     | Task                                              | Status     | Priority    | Est. Hours |
| ------ | ------------------------------------------------- | ---------- | ----------- | ---------- |
| CR-001 | friends/models.py - Friendship model              | 📝 Backlog | 🔴 Critical | 2h         |
| CR-002 | friends/serializers.py - Friendship serialization | 📝 Backlog | 🔴 Critical | 2h         |
| CR-003 | friends/views.py - FriendshipViewSet              | 📝 Backlog | 🔴 Critical | 4h         |
| CR-004 | friends/urls.py - Route configuration             | 📝 Backlog | 🔴 Critical | 1h         |

### 🟡 BACKEND - SUPPORTING

| ID     | Task                                 | Status     | Priority  | Est. Hours |
| ------ | ------------------------------------ | ---------- | --------- | ---------- |
| CR-005 | friends/apps.py - Django app config  | 📝 Backlog | 🟢 Low    | 0.25h      |
| CR-006 | friends/**init**.py - Package marker | 📝 Backlog | 🟢 Low    | 0.1h       |
| CR-007 | friends/admin.py - Admin interface   | 📝 Backlog | 🟡 Medium | 0.5h       |

### 🔴 FRONTEND - CRITICAL PATH

| ID     | Task                                  | Status     | Priority    | Est. Hours |
| ------ | ------------------------------------- | ---------- | ----------- | ---------- |
| CR-008 | FriendsContext.jsx - Friends state    | 📝 Backlog | 🔴 Critical | 3h         |
| CR-009 | friendsService.js - API calls wrapper | 📝 Backlog | 🔴 Critical | 2h         |
| CR-010 | Friends.jsx - Friends page            | 📝 Backlog | 🔴 Critical | 4h         |

### 🟡 FRONTEND - SUPPORTING

| ID     | Task                             | Status     | Priority | Est. Hours |
| ------ | -------------------------------- | ---------- | -------- | ---------- |
| CR-011 | Friends/index.js - Barrel export | 📝 Backlog | 🟢 Low   | 0.1h       |

---

## 📊 Progress Tracker

**Total Tasks:** 11  
**Completed:** 0  
**In Progress:** 0  
**Remaining:** 11

```
Progress: [░░░░░░░░░░░░░░░░░░░░] 0%
```

---

## 🔗 Dependencies

**Crystal PROVIDES:**

- `friends/models.py` - Friendship relationships
- `FriendsContext` - Friends state for Pablo's UI
- `friendsService` - API wrapper
- `Friends.jsx` - Friends page UI

**Crystal CONSUMES:**

- `users/models.py` (Natalia) - User ForeignKey for relationships
- `AuthContext` (Natalia) - Current user for friend checks
- `apiClient` (Tito) - HTTP requests

---

## 📝 API Endpoints You Create

| Endpoint                   | Method | Description                   |
| -------------------------- | ------ | ----------------------------- |
| `/api/friends/`            | GET    | List accepted friendships     |
| `/api/friends/pending/`    | GET    | List incoming friend requests |
| `/api/friends/request/`    | POST   | Send friend request           |
| `/api/friends/:id/accept/` | POST   | Accept pending request        |
| `/api/friends/:id/reject/` | POST   | Reject pending request        |
| `/api/friends/:id/`        | DELETE | Remove friendship (unfriend)  |

### Expected Response Format

**GET /api/friends/**

```json
[
  {
    "id": 1,
    "user1": {
      "id": 1,
      "username": "alice",
      "first_name": "Alice",
      "profile": { "avatar": "url" }
    },
    "user2": {
      "id": 2,
      "username": "bob",
      "first_name": "Bob",
      "profile": { "avatar": "url" }
    },
    "status": "accepted",
    "created_at": "2024-12-19T10:00:00Z"
  }
]
```

**GET /api/friends/pending/**

```json
[
  {
    "id": 5,
    "user1": { ... },  // The requester
    "user2": { ... },  // Current user (recipient)
    "status": "pending",
    "action_user": 1,  // Who sent the request
    "created_at": "2024-12-20T10:00:00Z"
  }
]
```

---

## 📋 Friendship Model Fields

| Field         | Type                 | Description                       |
| ------------- | -------------------- | --------------------------------- |
| `user1`       | ForeignKey(User)     | First user in friendship          |
| `user2`       | ForeignKey(User)     | Second user in friendship         |
| `status`      | CharField (choices)  | 'pending', 'accepted', 'rejected' |
| `action_user` | ForeignKey(User)     | Who sent the request              |
| `created_at`  | DateTimeField (auto) | When request was sent             |

**Constraints:**

- `unique_together = ['user1', 'user2']` (one record per pair)
- Cannot friend yourself (user1 != user2)

---

## 🔧 FriendsContext Functions

| Function                      | Description                |
| ----------------------------- | -------------------------- |
| `fetchFriends()`              | GET accepted friendships   |
| `fetchPendingRequests()`      | GET incoming requests      |
| `sendFriendRequest(userId)`   | POST request to user       |
| `acceptRequest(friendshipId)` | Accept and move to friends |
| `rejectRequest(friendshipId)` | Reject and remove          |
| `removeFriend(friendshipId)`  | Unfriend                   |

---

## 🎨 Friends.jsx Features

The Friends page should include:

1. **Friends Section**

   - Grid/list of accepted friends
   - Each card shows: avatar, username, bio
   - Click card → navigate to profile
   - Message icon → open DM

2. **Pending Requests Section**

   - List of incoming requests
   - Accept / Reject buttons
   - Click requester → view their profile

3. **Styling**
   - Use Pablo's design system
   - Glass cards for friend items
   - Neon accents for buttons
   - Responsive (mobile-friendly)

---

## ⚠️ Important Notes

1. **Bidirectional friendships** - When A befriends B, one record covers both directions

2. **Query pattern for "all friends of user X":**

   ```python
   Q(user1=user, status='accepted') | Q(user2=user, status='accepted')
   ```

3. **Only recipient can accept/reject** - Validate action_user != current_user

4. **Duplicate prevention** - Check both (A→B) and (B→A) before creating

5. **FriendsContext consumed by:**
   - Friends page (Crystal)
   - NotificationModal (Pablo) - pending request count
   - MessageModal (Pablo) - friends list for DMs

---

## 📌 Status Legend

- **📝 Backlog** - Not started
- **🔄 In Progress** - Currently working
- **👀 In Review** - PR submitted
- **✅ Done** - Completed and merged
- **🚫 Blocked** - Waiting on dependency

---

_Last Updated: January 8, 2026_
