# Backend Guide

This is the Django REST API for NUMENEON.

---

## Setup

```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

Server runs at: **http://localhost:8000**

---

## Project Structure

```
backend/
├── huddl/              # Project config (Tito + Pablo)
│   ├── settings.py     # CORS, JWT, database config
│   └── urls.py         # Main router
│
├── posts/              # Posts app (Colin)
│   ├── models.py       # Post model (exists)
│   ├── admin.py        # Register in admin
│   ├── serializers.py  # Convert to JSON (Week 1-2)
│   ├── views.py        # API endpoints
│   └── urls.py         # /api/posts/ routes
│
├── users/              # Users app (Natalia)
│   ├── models.py       # Profile model (exists)
│   ├── admin.py        # Register in admin
│   ├── serializers.py  # Convert to JSON
│   ├── views.py        # Auth endpoints (Week 1-2)
│   └── urls.py         # /api/auth/ routes
│
└── friends/            # Friends app (Crystal)
    ├── models.py       # Friendship model
    ├── admin.py        # Register in admin
    ├── serializers.py  # Convert to JSON
    ├── views.py        # Friends endpoints
    └── urls.py         # /api/friends/ routes
```

---

## Week 1 Tasks (Detailed)

### TITO + PABLO: CORS + JWT Configuration

**Why:** Frontend (localhost:5173) can't talk to backend (localhost:8000) without CORS. JWT is needed for auth.

**Step 1:** Install packages

```bash
pip install django-cors-headers djangorestframework-simplejwt
pip freeze > requirements.txt
```

**Step 2:** Edit `huddl/settings.py`

Add to `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    # ... existing apps ...
    'corsheaders',  # ADD THIS
    'rest_framework_simplejwt',  # ADD THIS
]
```

Add to TOP of `MIDDLEWARE`:

```python
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # MUST BE FIRST
    # ... rest of middleware ...
]
```

Add at BOTTOM of file:

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]

# JWT Settings
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}
```

**Test:** Restart server, open frontend, check browser console for CORS errors (should be gone).

---

### COLIN: Register Post in Admin + Start Serializer

**File 1:** `posts/admin.py`

```python
from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'type', 'content', 'created_at']
    list_filter = ['type', 'created_at']
    search_fields = ['content', 'author__username']
```

**File 2 (stretch):** `posts/serializers.py`

```python
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'author_username', 'type', 'content', 'created_at']
        read_only_fields = ['author', 'created_at']
```

**Test:**

```bash
python3 manage.py createsuperuser
# Create admin/admin123
python3 manage.py runserver
```

Go to http://localhost:8000/admin, login, click Posts, create a test post.

---

### NATALIA: Register Profile in Admin + Auth Views

**File 1:** `users/admin.py`

```python
from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'bio', 'created_at']
    search_fields = ['user__username', 'bio']
```

**File 2 (stretch):** `users/views.py` - Signup endpoint

```python
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Profile

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username taken'}, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    Profile.objects.create(user=user)

    return Response({'message': 'User created'}, status=201)
```

**Test:** Go to admin, click Profiles, should see the model.

---

### CRYSTAL: Create Friendship Model

**File:** `friends/models.py`

```python
from django.db import models
from django.contrib.auth.models import User

class Friendship(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'friend']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} → {self.friend.username}"
```

**Then run:**

```bash
python3 manage.py makemigrations friends
python3 manage.py migrate
```

---

## Week 2 Preview

After Week 1, suggested tasks:

| Person  | Week 2 Task                                      |
| ------- | ------------------------------------------------ |
| Colin   | Post views + postsService.js + Home page logic   |
| Natalia | Auth views + authService.js + Login/Signup forms |
| Crystal | Friendship serializers + views                   |
| Tito    | Utility helpers (with Pablo)                     |
| Pablo   | AuthContext + protected routes + integration     |

> These are suggestions — if you want to swap or take on more, let's talk!

---

## API Endpoints (What We're Building)

```
Auth (Natalia):
POST   /api/auth/signup/     → Create user
POST   /api/auth/login/      → Get JWT token
GET    /api/auth/me/         → Current user info

Posts (Colin):
GET    /api/posts/           → All posts (feed)
POST   /api/posts/           → Create post
GET    /api/posts/:id/       → Single post
DELETE /api/posts/:id/       → Delete post

Friends (Crystal):
GET    /api/friends/         → My friends list
POST   /api/friends/send/    → Send request
POST   /api/friends/respond/ → Accept/reject
```

---

## Common Commands

We use a **Makefile** for quick shortcuts. Instead of typing long commands, just use `make <shortcut>`.

> **Important:** You must be in the project root folder (`huddl-app/`) to use these.

### Quick Reference

```bash
# SERVERS
make b              # Start backend at http://localhost:8000
make f              # Start frontend at http://localhost:5173

# DATABASE
make migrate        # Apply database migrations
make makemigrations # Create new migrations after model changes
make seed           # Populate database with test data
make shell          # Open Django Python shell
make dbshell        # Open SQLite shell (raw SQL)

# USERS
make superuser      # Create admin user for Django admin panel
make users          # List all users in database

# DEPENDENCIES
make install        # Install both frontend and backend deps
make install-frontend
make install-backend

# GIT
make status         # git status
make push           # Push current branch
make pull           # Pull current branch

# CLEANUP
make clean          # Remove Python cache files
```

### Accessing the Database

**Option 1: Django Admin Panel (GUI)**

```bash
make superuser      # Create admin account (first time only)
make b              # Start backend
# Go to http://localhost:8000/admin
# Login with your superuser credentials
```

**Option 2: Django Shell (Python)**

```bash
make shell
```

Then in the shell:

```python
# List all users
from django.contrib.auth.models import User
User.objects.all()

# Find specific user
User.objects.get(username='pablo')

# List all posts
from posts.models import Post
Post.objects.all()

# Create a user manually
User.objects.create_user('testuser', 'test@test.com', 'password123')

# Exit shell
exit()
```

**Option 3: SQLite Shell (Raw SQL)**

```bash
make dbshell
```

Then in SQLite:

```sql
-- List all tables
.tables

-- See users
SELECT * FROM auth_user;

-- See posts
SELECT * FROM posts_post;

-- Exit
.quit
```

### Manual Commands (Without Makefile)

If you need to run commands manually:

```bash
# Activate virtual environment
source venv/bin/activate

# Run server
cd backend && python3 manage.py runserver

# Create migration after model change
cd backend && python3 manage.py makemigrations
cd backend && python3 manage.py migrate

# Create admin user
cd backend && python3 manage.py createsuperuser

# Check for errors
cd backend && python3 manage.py check
```
