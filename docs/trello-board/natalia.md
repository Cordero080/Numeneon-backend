# 👤 Natalia | L | Auth System + Migration Manager + Trello Board

> Authentication foundation, user management, database migrations, and Trello board maintenance

---

## 🏷️ T-Shirt Size: L (19 files + Trello responsibility)

**Role:** Auth Lead, Migration Manager, Trello Board Owner  
**Strengths:** Backend + Frontend, database management  
**Focus:** User authentication, JWT tokens, profile management

---

## 📋 Task Board

### 🔴 BACKEND - CRITICAL PATH

| ID    | Task                                                | Status     | Priority    | Est. Hours |
| ----- | --------------------------------------------------- | ---------- | ----------- | ---------- |
| N-001 | users/models.py - Profile model                     | 📝 Backlog | 🔴 Critical | 2h         |
| N-002 | users/serializers.py - User/Profile serialization   | 📝 Backlog | 🔴 Critical | 2h         |
| N-003 | users/views.py - Auth endpoints (signup, login, me) | 📝 Backlog | 🔴 Critical | 4h         |
| N-004 | users/urls.py - Route configuration                 | 📝 Backlog | 🔴 Critical | 1h         |

### 🟡 BACKEND - SUPPORTING

| ID    | Task                                          | Status     | Priority  | Est. Hours |
| ----- | --------------------------------------------- | ---------- | --------- | ---------- |
| N-005 | users/apps.py - Django app config             | 📝 Backlog | 🟢 Low    | 0.25h      |
| N-006 | users/**init**.py - Package marker            | 📝 Backlog | 🟢 Low    | 0.1h       |
| N-007 | users/management/**init**.py                  | 📝 Backlog | 🟢 Low    | 0.1h       |
| N-008 | users/management/commands/**init**.py         | 📝 Backlog | 🟢 Low    | 0.1h       |
| N-009 | users/management/commands/create_test_user.py | 📝 Backlog | 🟡 Medium | 1h         |
| N-010 | users/migrations/**init**.py                  | 📝 Backlog | 🟢 Low    | 0.1h       |
| N-011 | users/migrations/0001_initial.py              | 📝 Backlog | 🟡 Medium | 0.5h       |

### 🔴 FRONTEND - CRITICAL PATH

| ID    | Task                                    | Status     | Priority    | Est. Hours |
| ----- | --------------------------------------- | ---------- | ----------- | ---------- |
| N-012 | AuthContext.jsx - Auth state management | 📝 Backlog | 🔴 Critical | 4h         |
| N-013 | Login.jsx - Login form component        | 📝 Backlog | 🔴 Critical | 3h         |
| N-014 | Signup.jsx - Registration form          | 📝 Backlog | 🔴 Critical | 3h         |
| N-015 | ProtectedRoute.jsx - Route guard        | 📝 Backlog | 🔴 Critical | 1h         |

### 🟡 FRONTEND - SUPPORTING

| ID    | Task                            | Status     | Priority | Est. Hours |
| ----- | ------------------------------- | ---------- | -------- | ---------- |
| N-016 | Login/index.js - Barrel export  | 📝 Backlog | 🟢 Low   | 0.1h       |
| N-017 | Signup/index.js - Barrel export | 📝 Backlog | 🟢 Low   | 0.1h       |

### 🔧 MIGRATION MANAGEMENT

| ID    | Task                                | Status     | Priority  | Est. Hours |
| ----- | ----------------------------------- | ---------- | --------- | ---------- |
| N-018 | Review Colin's posts migrations     | 📝 Backlog | 🟡 Medium | 0.5h       |
| N-019 | Review Crystal's friends migrations | 📝 Backlog | 🟡 Medium | 0.5h       |
| N-020 | Run central `migrate` command       | 📝 Backlog | 🟡 Medium | 0.25h      |

### 📋 TRELLO BOARD MANAGEMENT (ONGOING)

| ID    | Task                            | Status     | Priority  | Frequency |
| ----- | ------------------------------- | ---------- | --------- | --------- |
| N-021 | Update task statuses            | 🔄 Ongoing | 🟡 Medium | Daily     |
| N-022 | Add new tasks as discovered     | 🔄 Ongoing | 🟡 Medium | As needed |
| N-023 | Archive completed tasks         | 🔄 Ongoing | 🟢 Low    | Weekly    |
| N-024 | Track blockers and dependencies | 🔄 Ongoing | 🔴 High   | Daily     |
| N-025 | Update stretch goals progress   | 🔄 Ongoing | 🟢 Low    | Weekly    |
| N-026 | Sync with team on PR status     | 🔄 Ongoing | 🟡 Medium | Daily     |

---

## 📊 Progress Tracker

**Total Tasks:** 20 (excluding ongoing Trello tasks)  
**Completed:** 0  
**In Progress:** 0  
**Remaining:** 20

```
Progress: [░░░░░░░░░░░░░░░░░░░░] 0%
```

---

## 🔗 Dependencies

**Natalia PROVIDES:**

- `users/models.py` - Colin & Crystal need User ForeignKey
- `AuthContext` - Everyone needs auth state
- `ProtectedRoute` - App.jsx needs route guards
- JWT authentication system

**Natalia CONSUMES:**

- `apiClient` (Tito) - Must be ready first for API calls

**Natalia MANAGES:**

- All database migrations (reviews + runs central migrate)
- Trello board updates

---

## 🎯 Special Responsibilities

### Migration Management

As Migration Manager, Natalia:

1. **Reviews** migration files from Colin and Crystal
2. **Runs** central `python manage.py migrate` command
3. **Resolves** any migration conflicts
4. **Validates** database schema is correct

### Trello Board Ownership

As Trello Board Owner, Natalia:

1. **Updates** task statuses as team reports progress
2. **Adds** new tasks when discovered during development
3. **Tracks** blockers and communicates them to team
4. **Archives** completed tasks weekly
5. **Syncs** with team on PR review status

---

## 📝 API Endpoints You Create

| Endpoint                   | Method | Description                           |
| -------------------------- | ------ | ------------------------------------- |
| `/api/auth/signup/`        | POST   | Create new user account               |
| `/api/auth/login/`         | POST   | Authenticate with EMAIL, return JWT   |
| `/api/auth/me/`            | GET    | Get current user data (requires auth) |
| `/api/auth/token/refresh/` | POST   | Refresh expired JWT token             |

### Expected Request/Response Formats

**POST /api/auth/signup/**

```json
// Request
{ "username": "alice", "email": "alice@example.com", "password": "..." }

// Response
{ "id": 1, "username": "alice", "email": "alice@example.com", "message": "User created successfully" }
```

**POST /api/auth/login/**

```json
// Request
{ "email": "alice@example.com", "password": "..." }

// Response
{ "access": "eyJ...", "refresh": "eyJ..." }
```

**GET /api/auth/me/**

```json
// Response
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "first_name": "Alice",
  "last_name": "Smith",
  "profile": {
    "id": 1,
    "bio": "Hello world!",
    "avatar": "url or null"
  }
}
```

---

## ⚠️ Important Notes

1. **Login uses EMAIL, not username** - Frontend sends email field
2. **JWT tokens go in localStorage** - Keys: `accessToken`, `refreshToken`
3. **AuthContext must complete before other contexts** - They wait for auth
4. **Profile auto-creates with User** - Use Django signals

---

## 📌 Status Legend

- **📝 Backlog** - Not started
- **🔄 In Progress** - Currently working
- **🔄 Ongoing** - Recurring task
- **👀 In Review** - PR submitted
- **✅ Done** - Completed and merged
- **🚫 Blocked** - Waiting on dependency

---

_Last Updated: January 8, 2026_
