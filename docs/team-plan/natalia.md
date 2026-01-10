# Natalia's Tasks - Auth & Users System (Backend)

## Your Mission

You're building the authentication system - the foundation that lets users create accounts, log in, and access protected features. You own the Users app and manage the Profile model.

## Files You Own

**Important:** Don't touch anyone else's files to avoid merge conflicts!

### Backend Files (11 total)

- `backend/users/models.py` - Profile model (extends Django User)
- `backend/users/views.py` - Signup, login, current user API endpoints
- `backend/users/serializers.py` - User/Profile data validation and formatting
- `backend/users/urls.py` - Auth API routes configuration
- `backend/users/apps.py` - Django app configuration
- `backend/users/__init__.py` - Package marker
- `backend/users/management/__init__.py` - Management commands package
- `backend/users/management/commands/__init__.py` - Commands subpackage
- `backend/users/management/commands/create_test_user.py` - Test user creation script
- `backend/users/migrations/__init__.py` - Migrations package marker
- `backend/users/migrations/0001_initial.py` - Initial database schema (auto-generated)

---

## ⚠️ CRITICAL: Login Uses EMAIL, Not Username!

The frontend sends `{ "email": "...", "password": "..." }` for login.

You must:

1. Look up user by email: `User.objects.get(email=email)`
2. Authenticate with username: `authenticate(username=user.username, password=password)`

---

## Task Breakdown

### ✅ Task 1: Create Profile Model

**Files:** `backend/users/models.py`

**Profile Model Fields:**

| Field        | Type                | Description                        |
| ------------ | ------------------- | ---------------------------------- |
| `user`       | OneToOneField(User) | Link to Django's built-in User     |
| `bio`        | TextField           | User bio (optional, max 500 chars) |
| `avatar`     | URLField            | Profile image URL (optional)       |
| `location`   | CharField           | User location (optional, max 100)  |
| `website`    | URLField            | Personal website (optional)        |
| `created_at` | DateTimeField       | Auto-set on creation               |
| `updated_at` | DateTimeField       | Auto-set on save                   |

**Model Hints:**

```python
user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
bio = models.TextField(max_length=500, blank=True)
avatar = models.URLField(max_length=500, blank=True)
location = models.CharField(max_length=100, blank=True)
website = models.URLField(max_length=200, blank=True)
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```

---

### ✅ Task 2: Build Authentication Serializers

**Files:** `backend/users/serializers.py`

**Serializers to Create:**

1. **EmailLoginSerializer** - Custom login with email + password, returns JWT tokens
2. **UserSerializer** - Basic user data (id, username, email, first_name, last_name, date_joined)
3. **ProfileSerializer** - Profile with nested UserSerializer

**EmailLoginSerializer Logic:**

```python
class EmailLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Look up user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError('Invalid credentials')

        # Authenticate with username
        authenticated = authenticate(username=user.username, password=password)
        if not authenticated:
            raise serializers.ValidationError('Invalid credentials')

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }
```

**ProfileSerializer Output Format:**

```json
{
  "id": 1,
  "user": {
    "id": 1,
    "username": "alice",
    "email": "alice@example.com",
    "first_name": "Alice",
    "last_name": "Smith",
    "date_joined": "2024-12-01T..."
  },
  "bio": "Hello world!",
  "avatar": "url or null",
  "location": "",
  "website": "",
  "created_at": "...",
  "updated_at": "..."
}
```

---

### ✅ Task 3: Build Authentication Views

**Files:** `backend/users/views.py`

**Endpoints to Create:**

| Method | Endpoint            | Function         | Description                  |
| ------ | ------------------- | ---------------- | ---------------------------- |
| POST   | `/api/auth/signup/` | `signup()`       | Create new user account      |
| POST   | `/api/auth/login/`  | `email_login()`  | Login with email, return JWT |
| GET    | `/api/auth/me/`     | `current_user()` | Get logged-in user's info    |

**Also include:** `ProfileViewSet` for profile CRUD operations

**Signup Flow:**

1. Receive: `{ username, display_name, email, password }`
2. Parse `display_name` into `first_name` and `last_name` (split on first space)
3. Validate: username/email not taken
4. Create User with `User.objects.create_user()` (auto-hashes password!)
5. Create Profile for the user
6. Return: `{ id, username, email, message }`

**Login Flow (email_login):**

1. Use `EmailLoginSerializer` to validate and generate tokens
2. Return: `{ access, refresh }`

**Current User Flow (current_user):**

1. Require authenticated user (JWT in header)
2. Return user data with nested profile

**Expected Response for /api/auth/me/:**

```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "first_name": "Alice",
  "last_name": "Smith",
  "profile": {
    "id": 1,
    "bio": "Hello world!",
    "avatar": "url or null",
    "location": "",
    "website": ""
  }
}
```

---

### ✅ Task 4: Configure URL Routes

**Files:** `backend/users/urls.py`

**Routes to Configure:**

```python
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.email_login, name='login'),
    path('me/', views.current_user, name='current_user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

---

### ✅ Task 5: Create Test User Management Command

**Files:** `backend/users/management/commands/create_test_user.py`

**Purpose:** Quick way to create test user for development/demo.

```bash
python manage.py create_test_user
```

**Should Create:**

- User with known credentials (e.g., `testuser` / `testpass123`)
- Associated Profile
- Print success message with credentials

---

## Integration Points

**You provide:**

- User authentication endpoints at `/api/auth/`
- Profile model that other apps reference
- UserSerializer that other serializers nest

**Other apps consume:**

- Colin's `Post.author` references User
- Crystal's `Friendship.user/friend` references User
- Both apps import `UserSerializer` for nested user data

---

## JWT Authentication

This project uses `djangorestframework-simplejwt` for JWT tokens.

**Settings already configured in `settings.py`:**

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

**Generate tokens:**

```python
from rest_framework_simplejwt.tokens import RefreshToken

refresh = RefreshToken.for_user(user)
access_token = str(refresh.access_token)
refresh_token = str(refresh)
```

**Frontend sends:**

```
Authorization: Bearer <access_token>
```

---

## Testing Checklist

- [ ] Can signup with username, display_name, email, password
- [ ] Signup creates User + Profile
- [ ] Cannot signup with duplicate username or email
- [ ] Can login with EMAIL and password (not username!)
- [ ] Login returns JWT access and refresh tokens
- [ ] Can access /api/auth/me/ with valid token
- [ ] /api/auth/me/ returns user with nested profile
- [ ] Cannot access /api/auth/me/ without token (401)
- [ ] Can refresh token at /api/auth/token/refresh/

---

## Fixture Data

After running migrations, load the demo data:

```bash
python manage.py loaddata posts_and_users.json
```

This includes:

- 6+ test users with password `test123`: `pabloPistola`, `titod`, `arthurb`, `nataliap`, `colinw`, `crystalr`
- Profile data (bio, location, website)
