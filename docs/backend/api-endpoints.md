# Numeneon API Endpoints

> **Last Updated:** January 24, 2026  
> **Total Endpoints:** 14
> **Database:** PostgreSQL (migrated from SQLite Jan 6, 2026)

---

## Endpoint Summary by App

| App         | Base Path       | Endpoints              |
| ----------- | --------------- | ---------------------- |
| **users**   | `/api/auth/`    | 5                      |
| **posts**   | `/api/posts/`   | 6 (via ViewSet router) |
| **friends** | `/api/friends/` | 6                      |

---

## Users App Endpoints (5)

**Base URL:** `http://127.0.0.1:8000/api/auth/`

| Method | Endpoint          | Function           | Description                            |
| ------ | ----------------- | ------------------ | -------------------------------------- |
| POST   | `/signup/`        | `signup()`         | Create new user account                |
| POST   | `/login/`         | `email_login()`    | Login with email/password, returns JWT |
| POST   | `/token/refresh/` | `TokenRefreshView` | Refresh expired access token           |
| GET    | `/me/`            | `current_user()`   | Get logged-in user's info              |
| GET    | `/search/`        | `search_users()`   | Search users by name/username          |

### Request/Response Examples

#### POST `/api/auth/signup/`

```json
// Request
{
  "username": "pablo_cordero",
  "email": "pablo@numeneon.com",
  "password": "securepass123"
}

// Response (201 Created)
{
  "id": 1,
  "username": "pablo_cordero",
  "email": "pablo@numeneon.com"
}
```

#### POST `/api/auth/login/`

```json
// Request
{
  "email": "pablo@numeneon.com",
  "password": "securepass123"
}

// Response (200 OK)
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGci...",
  "user": {
    "id": 1,
    "username": "pablo_cordero",
    "email": "pablo@numeneon.com",
    "profile": {
      "bio": "UI/UX Designer",
      "avatar": "https://...",
      "location": "Los Angeles"
    }
  }
}
```

#### GET `/api/auth/me/`

```
Headers: Authorization: Bearer <access_token>
```

```json
// Response (200 OK)
{
  "id": 1,
  "username": "pablo_cordero",
  "email": "pablo@numeneon.com",
  "profile": { ... }
}
```

#### GET `/api/auth/search/`

**Purpose:** Find users to add as friends. Searches by username, first_name, or last_name.

```
Headers: Authorization: Bearer <access_token>
Query Params: ?q=<search_term>  (minimum 2 characters)
```

```json
// Request: GET /api/auth/search/?q=tito

// Response (200 OK)
[
  {
    "id": 3,
    "username": "tito",
    "first_name": "Tito",
    "last_name": ""
  },
  {
    "id": 11,
    "username": "titod",
    "first_name": "Tito",
    "last_name": "Del Valle",
    "avatar": "https://..."
  }
]

// If query < 2 chars or no matches:
[]
```

**Notes:**

- Requires authentication (JWT token)
- Returns max 20 results
- Excludes the current logged-in user from results
- Case-insensitive search
- Used by the SearchModal in frontend to find new people

---

## Posts App Endpoints (6)

**Base URL:** `http://127.0.0.1:8000/api/posts/`

Uses `DefaultRouter` with `PostViewSet` - auto-generates CRUD routes.

| Method | Endpoint      | Action           | Description         |
| ------ | ------------- | ---------------- | ------------------- |
| GET    | `/`           | `list()`         | Get all posts       |
| POST   | `/`           | `create()`       | Create new post     |
| GET    | `/{id}/`      | `retrieve()`     | Get single post     |
| PUT    | `/{id}/`      | `update()`       | Update post         |
| DELETE | `/{id}/`      | `destroy()`      | Delete post         |
| POST   | `/{id}/like/` | `@action like()` | Toggle like on post |

### Request/Response Examples

#### GET `/api/posts/`

```json
// Response (200 OK)
[
  {
    "id": 1,
    "author": {
      "id": 1,
      "username": "pablo_cordero",
      "profile": { "avatar": "https://..." }
    },
    "content": "Hello Numeneon!",
    "type": "thoughts",
    "media_url": null,
    "parent": null,
    "likes_count": 5,
    "comment_count": 2,
    "shares_count": 0,
    "created_at": "2026-01-08T12:00:00Z",
    "updated_at": "2026-01-08T12:00:00Z"
  }
]
```

#### POST `/api/posts/`

```json
// Request
{
  "content": "My first post!",
  "type": "thoughts"
}

// Response (201 Created)
{
  "id": 2,
  "author": { ... },
  "content": "My first post!",
  "type": "thoughts",
  ...
}
```

#### POST `/api/posts/{id}/like/`

```json
// Response (200 OK) - Liked
{
  "id": 1,
  "likes_count": 6,
  "user_has_liked": true,
  ...
}

// Response (200 OK) - Unliked (toggle)
{
  "id": 1,
  "likes_count": 5,
  "user_has_liked": false,
  ...
}
```

### Query Parameters

| Param      | Example           | Description                     |
| ---------- | ----------------- | ------------------------------- |
| `username` | `?username=pablo` | Filter posts by author username |

---

## Friends App Endpoints (6)

**Base URL:** `http://127.0.0.1:8000/api/friends/`

| Method | Endpoint                 | Function             | Description                 |
| ------ | ------------------------ | -------------------- | --------------------------- |
| GET    | `/`                      | `friend_list()`      | Get all friends             |
| GET    | `/requests/`             | `pending_requests()` | Get pending friend requests |
| POST   | `/request/{user_id}/`    | `send_request()`     | Send friend request         |
| POST   | `/accept/{request_id}/`  | `accept_request()`   | Accept friend request       |
| POST   | `/decline/{request_id}/` | `decline_request()`  | Decline friend request      |
| DELETE | `/remove/{user_id}/`     | `remove_friend()`    | Remove friend               |

### Request/Response Examples

#### GET `/api/friends/`

```json
// Response (200 OK)
[
  {
    "id": 1,
    "username": "natalia_dev",
    "profile": {
      "avatar": "https://...",
      "bio": "Backend wizard"
    }
  },
  {
    "id": 2,
    "username": "colin_codes",
    "profile": { ... }
  }
]
```

#### GET `/api/friends/requests/`

```json
// Response (200 OK)
[
  {
    "id": 5,
    "from_user": {
      "id": 3,
      "username": "crystal_react"
    },
    "created_at": "2026-01-07T15:30:00Z"
  }
]
```

#### POST `/api/friends/request/{user_id}/`

```json
// POST /api/friends/request/5/

// Response (201 Created)
{
  "message": "Friend request sent",
  "request_id": 10
}
```

#### POST `/api/friends/accept/{request_id}/`

```json
// POST /api/friends/accept/5/

// Response (200 OK)
{
  "message": "Friend request accepted",
  "friend": {
    "id": 3,
    "username": "crystal_react"
  }
}
```

#### DELETE `/api/friends/remove/{user_id}/`

```json
// DELETE /api/friends/remove/3/

// Response (200 OK)
{
  "message": "Friend removed"
}
```

---

## Authentication

All endpoints (except `/signup/` and `/login/`) require JWT authentication.

**Header Format:**

```
Authorization: Bearer <access_token>
```

**Token Lifecycle:**

1. Login returns `access` (15 min) + `refresh` (7 days) tokens
2. Use `access` token for all API calls
3. When `access` expires, call `/token/refresh/` with `refresh` token
4. Get new `access` token, continue using API

---

## Error Responses

| Code | Meaning      | Example                |
| ---- | ------------ | ---------------------- |
| 400  | Bad Request  | Invalid data format    |
| 401  | Unauthorized | Missing/invalid JWT    |
| 403  | Forbidden    | Not owner of resource  |
| 404  | Not Found    | Resource doesn't exist |
| 500  | Server Error | Backend bug            |

```json
// Example error response
{
  "detail": "Authentication credentials were not provided."
}
```
