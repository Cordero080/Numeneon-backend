# 👤 Colin | M | Posts System

> Posts CRUD, content management, and post-related state

---

## 🏷️ T-Shirt Size: M (15 files)

**Role:** Posts Lead, Team Lead  
**Strengths:** Backend + Frontend, team coordination  
**Focus:** Post CRUD operations, content types, likes/shares

---

## 📋 Task Board

### 🔴 BACKEND - CRITICAL PATH

| ID    | Task                                      | Status     | Priority    | Est. Hours |
| ----- | ----------------------------------------- | ---------- | ----------- | ---------- |
| C-001 | posts/models.py - Post + Like models      | 📝 Backlog | 🔴 Critical | 3h         |
| C-002 | posts/serializers.py - Post serialization | 📝 Backlog | 🔴 Critical | 2h         |
| C-003 | posts/views.py - PostViewSet + actions    | 📝 Backlog | 🔴 Critical | 4h         |
| C-004 | posts/urls.py - Route configuration       | 📝 Backlog | 🔴 Critical | 1h         |

### 🟡 BACKEND - SUPPORTING

| ID    | Task                               | Status     | Priority  | Est. Hours |
| ----- | ---------------------------------- | ---------- | --------- | ---------- |
| C-005 | posts/apps.py - Django app config  | 📝 Backlog | 🟢 Low    | 0.25h      |
| C-006 | posts/**init**.py - Package marker | 📝 Backlog | 🟢 Low    | 0.1h       |
| C-007 | posts/admin.py - Admin interface   | 📝 Backlog | 🟡 Medium | 0.5h       |

### 🔴 FRONTEND - CRITICAL PATH

| ID    | Task                                      | Status     | Priority    | Est. Hours |
| ----- | ----------------------------------------- | ---------- | ----------- | ---------- |
| C-008 | PostsContext.jsx - Posts state management | 📝 Backlog | 🔴 Critical | 4h         |
| C-009 | postsService.js - API calls wrapper       | 📝 Backlog | 🔴 Critical | 2h         |

---

## 📊 Progress Tracker

**Total Tasks:** 9  
**Completed:** 0  
**In Progress:** 0  
**Remaining:** 9

```
Progress: [░░░░░░░░░░░░░░░░░░░░] 0%
```

---

## 🔗 Dependencies

**Colin PROVIDES:**

- `posts/models.py` - Core content type for the app
- `PostsContext` - Posts state consumed by Pablo's UI
- `postsService` - API wrapper used throughout app

**Colin CONSUMES:**

- `users/models.py` (Natalia) - User ForeignKey for Post.author
- `AuthContext` (Natalia) - Auth state for post ownership checks
- `apiClient` (Tito) - HTTP requests

---

## 📝 API Endpoints You Create

| Endpoint                  | Method | Description               |
| ------------------------- | ------ | ------------------------- |
| `/api/posts/`             | GET    | List all posts            |
| `/api/posts/`             | POST   | Create new post           |
| `/api/posts/:id/`         | GET    | Get single post           |
| `/api/posts/:id/`         | PATCH  | Update post (author only) |
| `/api/posts/:id/`         | DELETE | Delete post (author only) |
| `/api/posts/:id/replies/` | GET    | Get replies to a post     |
| `/api/posts/:id/like/`    | POST   | Toggle like on post       |
| `/api/posts/:id/share/`   | POST   | Increment share count     |

### Expected Response Format

**GET /api/posts/**

```json
[
  {
    "id": 1,
    "author": {
      "id": 5,
      "username": "alice",
      "first_name": "Alice",
      "last_name": "Smith"
    },
    "type": "thoughts",
    "content": "This is a post",
    "media_url": null,
    "parent": null,
    "parent_id": null,
    "created_at": "2024-12-19T10:00:00Z",
    "likes_count": 42,
    "reply_count": 7,
    "shares_count": 3,
    "is_liked": false,
    "visibility": "public"
  }
]
```

---

## 📋 Post Model Fields

| Field          | Type                   | Description                       |
| -------------- | ---------------------- | --------------------------------- |
| `author`       | ForeignKey(User)       | Who created the post              |
| `type`         | CharField (choices)    | 'thoughts', 'media', 'milestones' |
| `content`      | TextField              | Post text content                 |
| `media_url`    | URLField (optional)    | URL for media posts               |
| `parent`       | ForeignKey(self, null) | For replies/threads               |
| `created_at`   | DateTimeField (auto)   | Creation timestamp                |
| `likes_count`  | PositiveIntegerField   | Like counter                      |
| `reply_count`  | PositiveIntegerField   | Reply counter                     |
| `shares_count` | PositiveIntegerField   | Share counter                     |
| `visibility`   | CharField              | 'public', 'friends', 'private'    |

---

## 📋 Like Model Fields

| Field        | Type                 | Description    |
| ------------ | -------------------- | -------------- |
| `user`       | ForeignKey(User)     | Who liked      |
| `post`       | ForeignKey(Post)     | What was liked |
| `created_at` | DateTimeField (auto) | When liked     |

**Constraint:** unique_together = ['user', 'post'] (prevents double-likes)

---

## 🔧 PostsContext Functions

| Function                         | Description                    |
| -------------------------------- | ------------------------------ |
| `fetchPosts()`                   | GET all posts, store in state  |
| `createPost(postData)`           | POST new post, add to state    |
| `updatePost(id, updates)`        | PATCH post, update in state    |
| `deletePost(id)`                 | DELETE post, remove from state |
| `fetchReplies(postId)`           | GET replies for a post         |
| `createReply(parentId, content)` | POST reply to a post           |
| `updateReply(id, updates)`       | PATCH reply content            |
| `deleteReply(id)`                | DELETE reply                   |
| `likePost(id)`                   | Toggle like, update count      |
| `sharePost(id)`                  | Increment share count          |

---

## ⚠️ Important Notes

1. **Post types map to Timeline columns:**

   - `thoughts` → Left column (blue)
   - `media` → Center column (magenta)
   - `milestones` → Right column (gold)

2. **reply_count NOT comment_count** - Field name matters for Pablo's UI

3. **Engagement fields required for ProfileCard analytics:**

   - `likes_count`, `reply_count`, `shares_count` all used in charts

4. **is_liked computed field** - Not stored, calculated per-request based on current user

---

## 📌 Status Legend

- **📝 Backlog** - Not started
- **🔄 In Progress** - Currently working
- **👀 In Review** - PR submitted
- **✅ Done** - Completed and merged
- **🚫 Blocked** - Waiting on dependency

---

_Last Updated: January 8, 2026_
