This file contains specific instructions for adding pseudocode to all backend Python files.

markdown# NUMENEON TEAM REBUILD - Part 3: Backend Instructions

## HOW TO USE THESE FILES

**⚠️ READ [00-START-HERE.md](./00-START-HERE.md) FIRST if you haven't already!**

This is Part 3 of 5. Read these files in order:

0. `00-START-HERE.md` - Quick overview, workflow, FAQ
1. `01-CONTEXT-AND-STRATEGY.md` - Background, strategy, assignments
2. `02-PSEUDOCODE-EXAMPLES.md` - All 12 example templates
3. `03-BACKEND-INSTRUCTIONS.md` ← YOU ARE HERE
4. `04-FRONTEND-INSTRUCTIONS.md` - Frontend pseudocode tasks
5. `05-TEAM-PLAN-FILES.md` - Team markdown file templates

---

## BRANCH: `team-shell-backend`

Before starting:

1. Create branch `team-shell-backend` from main
2. Delete the entire `frontend/` folder
3. Keep `backend/` folder with all files
4. Apply pseudocode as instructed below

**Note:** This project uses **pipenv** for Python dependency management.

- Dependencies are defined in `Pipfile`
- Install packages: `pipenv install <package>`
- Activate virtualenv: `pipenv shell`
- Run commands: `pipenv run python manage.py <command>`

**Database:** This project uses **PostgreSQL** (not SQLite).

- Ensure PostgreSQL is installed: `brew install postgresql` (macOS)
- Create the database: `createdb numeneon`
- settings.py is pre-configured for PostgreSQL on localhost
- Run migrations: `pipenv run python manage.py migrate`

---

## BACKEND FILE LIST BY OWNER

### NATALIA - Users App (11 files)

| File                                                    | Action                             |
| ------------------------------------------------------- | ---------------------------------- |
| `backend/users/models.py`                               | Full pseudocode                    |
| `backend/users/views.py`                                | Full pseudocode                    |
| `backend/users/serializers.py`                          | Full pseudocode                    |
| `backend/users/urls.py`                                 | Full pseudocode                    |
| `backend/users/apps.py`                                 | Minimal pseudocode (just config)   |
| `backend/users/__init__.py`                             | Empty with comment                 |
| `backend/users/management/__init__.py`                  | Empty with comment                 |
| `backend/users/management/commands/__init__.py`         | Empty with comment                 |
| `backend/users/management/commands/create_test_user.py` | Full pseudocode                    |
| `backend/users/migrations/__init__.py`                  | Empty with comment                 |
| `backend/users/migrations/0001_initial.py`              | Reference comment (auto-generated) |

---

### COLIN - Posts App (7 files)

| File                           | Action             |
| ------------------------------ | ------------------ |
| `backend/posts/models.py`      | Full pseudocode    |
| `backend/posts/views.py`       | Full pseudocode    |
| `backend/posts/serializers.py` | Full pseudocode    |
| `backend/posts/urls.py`        | Full pseudocode    |
| `backend/posts/apps.py`        | Minimal pseudocode |
| `backend/posts/__init__.py`    | Empty with comment |
| `backend/posts/admin.py`       | Minimal pseudocode |

---

### CRYSTAL - Friends App (7 files)

| File                             | Action             |
| -------------------------------- | ------------------ |
| `backend/friends/models.py`      | Full pseudocode    |
| `backend/friends/views.py`       | Full pseudocode    |
| `backend/friends/serializers.py` | Full pseudocode    |
| `backend/friends/urls.py`        | Full pseudocode    |
| `backend/friends/apps.py`        | Minimal pseudocode |
| `backend/friends/__init__.py`    | Empty with comment |
| `backend/friends/admin.py`       | Minimal pseudocode |

---

### COLLABORATIVE - Project URLs (1 file)

| File                       | Action                        |
| -------------------------- | ----------------------------- |
| `backend/numeneon/urls.py` | TODO comments for each person |

---

## DETAILED PSEUDOCODE FOR EACH FILE

### NATALIA'S FILES

#### `backend/users/models.py`

```python
"""
TODO: Create the Profile model - extends Django's built-in User

NUMENEON needs to store extra info about users beyond username/email/password.
Django's built-in User model handles auth, but we need to add:
- Profile picture (for display in posts, TopBar, ProfileCard)
- Bio (for the profile page)

Two approaches exist:
1. Extend AbstractUser (replace Django's User entirely)
2. Create Profile model with OneToOneField to User (recommended - simpler)

We recommend approach #2: Create a Profile that links to User.

Fields you need:
- user: OneToOne link to Django's User model
- avatar: URL field (optional - users might not upload one)
- bio: Text field (optional - can be blank)
- created_at: When profile was created

Integration points:
- Posts reference User as author (Colin's Post.author field)
- Frontend ProfileCard displays avatar and bio
- TopBar shows current user's avatar
- Serializers need to combine User + Profile data

Think about:
- What happens when a new User is created? (Signal to auto-create Profile?)
- How do you handle image uploads? (Django's ImageField + media settings)
- Should bio have a max length? (Probably yes - prevents abuse)
- What if user has no avatar? (Frontend needs to handle null)

Hint: Use OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
Hint: For images: ImageField(upload_to='profile_pics/', blank=True, null=True)
Hint: Consider using Django signals to auto-create Profile when User is created
Hint: Add __str__ method to return username for admin readability
"""

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # Your code here
    pass
```

#### `backend/users/views.py`

```python
"""
TODO: Create Authentication Views - signup, login, and current user endpoints

This file handles user registration, login, and fetching current user data.
Unlike Posts/Friends which use ViewSets, auth typically uses function-based views
or simple APIViews because the operations are unique (not standard CRUD).

Also includes a ProfileViewSet for profile CRUD operations.

Endpoints to create:
- POST /api/auth/signup/ - Create new user account
- POST /api/auth/login/ - Authenticate with EMAIL and return JWT tokens
- GET /api/auth/me/ - Get current logged-in user's data

IMPORTANT: Login uses EMAIL, not username!
Frontend sends: { "email": "user@example.com", "password": "..." }

For signup:
- Receive: { username, display_name, email, password }
- Parse display_name into first_name and last_name
- Validate: Username/email not taken
- Create: User + Profile
- Return: { id, username, email, message }

For login (email_login):
- Receive: { email, password }
- Look up user by email, then authenticate with username
- Return: JWT tokens { access, refresh }

For me (current_user):
- Require: Valid JWT token in Authorization header
- Return: Current user's data with nested profile

Expected response format for /api/auth/me/:
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

Think about:
- How do you hash passwords? (Django's User.objects.create_user() handles this)
- Where do JWT tokens come from? (rest_framework_simplejwt is configured in settings)
- How do you return tokens on login? (RefreshToken.for_user(user))
- For /me/, how do you get the current user? (request.user when authenticated)
- What errors should you return? (400 for validation, 401 for bad credentials)
- How do you look up user by email? (User.objects.get(email=email))

Hint: Use @api_view(['POST']) decorator for function-based views
Hint: For JWT: from rest_framework_simplejwt.tokens import RefreshToken
Hint: Token generation: refresh = RefreshToken.for_user(user)
Hint: Use IsAuthenticated permission for /me/ endpoint
Hint: Use AllowAny for signup and login endpoints
Hint: Parse display_name: name_parts = display_name.split(' ', 1)
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile
from .serializers import ProfileSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    # Auto-assign logged-in user when creating profile
    # Your code here
    pass

@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    # Your code here
    pass

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    # Your code here
    pass

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    # Your code here
    pass
```

#### `backend/users/serializers.py`

```python
"""
TODO: Create User Serializers - validate and format user data

Serializers do two jobs:
1. Validate incoming data (login form)
2. Format outgoing data (user JSON for frontend)

Serializers you need:
- EmailLoginSerializer: Custom login that accepts email + password, returns JWT tokens
- UserSerializer: Formats basic user data (id, username, email, first_name, last_name, date_joined)
- ProfileSerializer: Formats Profile data with nested user

IMPORTANT: Login uses EMAIL, not username!
EmailLoginSerializer:
- Fields: email, password (password is write_only)
- Validation: Look up user by email, authenticate with username
- Return: { access, refresh } JWT tokens

For UserSerializer:
- Include: id, username, email, first_name, last_name, date_joined
- Read-only: Don't allow editing user via this serializer

For ProfileSerializer:
- Include: id, user (nested UserSerializer), bio, avatar, location, website, created_at, updated_at
- user is read_only=True (nested)
- created_at, updated_at are read_only

Expected output format for profile:
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

Think about:
- How do you look up user by email in validate()? (User.objects.get(email=email))
- How do you authenticate after finding user? (authenticate(username=user.username, password=password))
- How do you generate JWT tokens? (RefreshToken.for_user(user))
- Should password be write_only? (YES - never return passwords!)
- How do you nest UserSerializer inside ProfileSerializer? (user = UserSerializer(read_only=True))

Hint: Use serializers.Serializer for EmailLoginSerializer (custom validation)
Hint: Use serializers.ModelSerializer for ProfileSerializer and UserSerializer
Hint: For nested: user = UserSerializer(read_only=True)
Hint: For write_only: password = serializers.CharField(write_only=True)
Hint: Import: from rest_framework_simplejwt.tokens import RefreshToken
"""

from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Profile

class EmailLoginSerializer(serializers.Serializer):
    # Custom login with email instead of username
    # Your code here
    pass

class UserSerializer(serializers.ModelSerializer):
    # Basic user data
    # Your code here
    pass

class ProfileSerializer(serializers.ModelSerializer):
    # Profile with nested user
    # Your code here
    pass
```

#### `backend/users/urls.py`

```python
"""
TODO: Configure URL routes for authentication endpoints

This file maps URLs to view functions.
These URLs will be included in the main urls.py under /api/auth/

Routes to create:
- POST /api/auth/signup/ → signup view
- POST /api/auth/login/ → login view
- GET /api/auth/me/ → current_user view
- POST /api/auth/token/refresh/ → JWT token refresh (from simplejwt)

The token refresh endpoint is provided by simplejwt library.

Think about:
- Do you use path() or include() here? (path() for each route)
- How do you import views from the same app? (from .views import ...)
- Should the trailing slash be included? (Yes, Django convention)

Hint: from django.urls import path
Hint: from rest_framework_simplejwt.views import TokenRefreshView
Hint: path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
"""

from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

urlpatterns = [
    # Your code here
]
```

#### `backend/users/apps.py`

```python
"""
TODO: Django app configuration for users app

This is minimal boilerplate. Just configure the app name.

Hint: Django generates most of this automatically
"""

from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'

    # Optional: Add ready() method if using signals for auto-creating profiles
```

#### `backend/users/__init__.py`

```python
# Users app package marker
# This file can be empty - it just tells Python this folder is a package
```

#### `backend/users/management/__init__.py`

```python
# Management commands package marker
# This file can be empty
```

#### `backend/users/management/commands/__init__.py`

```python
# Commands subpackage marker
# This file can be empty
```

#### `backend/users/management/commands/create_test_user.py`

```python
"""
TODO: Create management command to generate test user

This command creates a test user for development/demo purposes.
Run it with: python manage.py create_test_user

What it should do:
1. Create a User with known credentials (e.g., username: testuser, password: testpass123)
2. Create associated Profile
3. Print success message with credentials

This is useful for:
- Quick setup after fresh database
- Demo purposes
- Testing without manual signup

Think about:
- What if user already exists? (Check first, skip or update)
- Should password be hardcoded or accept as argument?
- What default profile data to set?

Hint: Inherit from BaseCommand
Hint: Use User.objects.create_user() for proper password hashing
Hint: Access Profile via user.profile (if using signals) or create manually
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from users.models import Profile

class Command(BaseCommand):
    help = 'Creates a test user for development'

    def handle(self, *args, **options):
        # Your code here
        pass
```

#### `backend/users/migrations/__init__.py`

```python
# Migrations package marker
# This file can be empty
```

#### `backend/users/migrations/0001_initial.py`

```python
"""
NOTE: This file is auto-generated by Django

When you run: python manage.py makemigrations users
Django will create this file based on your models.py

DO NOT write this manually - let Django generate it.

Natalia's responsibility:
1. Define models in models.py
2. Run: python manage.py makemigrations users
3. Review the generated migration
4. Run: python manage.py migrate

This placeholder shows what to expect, but Django creates the actual content.
"""

# Django will generate migration code here
```

---

### COLIN'S FILES

#### `backend/posts/models.py`

```python
"""
TODO: Create the Post model - core content type for NUMENEON

A post is the main content users create. NUMENEON has 3 post types:
- 'thoughts': Text-only posts (displayed in left column of Timeline River)
- 'media': Posts with images (displayed in center column)
- 'milestones': Achievement posts (displayed in right column)

Posts can also be replies to other posts, creating threaded conversations.

Fields you need:
- author: Who created it? (ForeignKey to User)
- type: What kind? (CharField with choices: 'thoughts', 'media', 'milestones')
- content: The text content (TextField, can be blank for media-only)
- media_url: Optional URL to media (URLField, NOT ImageField!)
- parent: Reply to which post? (ForeignKey to self, null for top-level posts)
- created_at: When created? (DateTimeField, auto-set)
- likes_count: Number of likes (PositiveIntegerField, default=0)
- reply_count: Number of replies (PositiveIntegerField, default=0) - NOT comment_count!
- shares_count: Number of shares (PositiveIntegerField, default=0)

IMPORTANT: Use media_url (URLField) NOT image (ImageField)!
- media_url stores a URL string pointing to the image
- This is simpler than handling file uploads

Integration points:
- PostsContext (Colin's frontend) fetches and manages these
- Pablo's TimelineRiverFeed displays posts grouped BY USER (not by date!)
- Pablo's TimelineRiverRow renders individual posts with carousel navigation
- Pablo's ProfileCard.jsx uses engagement metrics for analytics:
  * Wave chart calculates weekly engagement totals (likes + replies + shares)
  * Heatmap shows posting frequency calendar
  * Post type breakdown counts posts by type
- Each column of the Timeline River shows one post type

RIVER TIMELINE "SPACE ECONOMY":
- Each user = ONE row in the feed
- All their posts collected in that row with carousel arrows
- Need 3+ posts per type per user for carousel arrows to appear
- seed_posts.py creates 9 posts per user (3 thoughts, 3 media, 3 milestones)

Expected JSON format (from serializer):
{
  "id": 1,
  "author": {
    "id": 5,
    "username": "alice",
    "first_name": "Alice",
    "last_name": "Smith"
  },
  "type": "thoughts",
  "content": "Hello NUMENEON!",
  "media_url": null,
  "parent": null,
  "parent_id": null,
  "created_at": "2024-12-19T10:30:00Z",
  "likes_count": 42,
  "reply_count": 7,
  "shares_count": 3,
  "is_liked": false
}

IMPORTANT: Engagement fields + is_liked are REQUIRED for ProfileCard analytics!

Think about:
- How do you restrict 'type' to only 3 values? (choices parameter)
- How do you make a post reply to another post? (ForeignKey to 'self')
- What happens when author is deleted? (CASCADE - delete their posts too)
- What happens when parent post is deleted? (CASCADE or SET_NULL?)
- Should content be required? (No - media posts might be image-only)
- How do you order posts? (Meta class with ordering = ['-created_at'])

Hint: POST_TYPE_CHOICES = [('thoughts', 'Thoughts'), ('media', 'Media'), ('milestones', 'Milestones')]
Hint: type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default='thoughts')
Hint: media_url = models.URLField(blank=True, null=True)  # NOT ImageField!
Hint: parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
Hint: created_at = models.DateTimeField(auto_now_add=True)
Hint: likes_count = models.PositiveIntegerField(default=0)
Hint: reply_count = models.PositiveIntegerField(default=0)  # NOT comment_count!
Hint: shares_count = models.PositiveIntegerField(default=0)
"""

from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    # Your code here
    pass


# TODO: Create the Like model - tracks which users liked which posts
#
# This enables the like/unlike toggle functionality.
# Each user can only like a post once (enforced by unique_together).
#
# Fields you need:
# - user: Who liked it? (ForeignKey to User)
# - post: Which post? (ForeignKey to Post)
# - created_at: When did they like it? (DateTimeField, auto-set)
#
# CRITICAL: Use unique_together = ('user', 'post') in Meta class
# This prevents duplicate likes and allows toggle logic in views.
#
# Hint: class Meta: unique_together = ('user', 'post')
# Hint: related_name='likes' on both ForeignKeys for easy access

class Like(models.Model):
    # Your code here
    pass
```

#### `backend/posts/views.py`

```python
"""
TODO: Create Posts API Views - full CRUD for posts + like toggle

This ViewSet handles all post operations via REST API.
Use ModelViewSet for automatic CRUD operations.

Endpoints (automatic from ModelViewSet):
- GET /api/posts/ - List all posts
- POST /api/posts/ - Create new post
- GET /api/posts/:id/ - Get single post
- PUT /api/posts/:id/ - Full update
- PATCH /api/posts/:id/ - Partial update
- DELETE /api/posts/:id/ - Delete post

Custom endpoints needed:
- GET /api/posts/:id/replies/ - Get all replies to a post
- POST /api/posts/:id/like/ - Toggle like on a post
- POST /api/posts/:id/share/ - Increment share count

Like endpoint behavior:
- If user hasn't liked → create Like, increment likes_count
- If user already liked → delete Like, decrement likes_count
- Return updated post with is_liked: true/false

Share endpoint behavior:
- Simply increment shares_count on the post
- Return updated post with new shares_count
- No toggle logic - each call increments (user can share multiple times)

Permissions:
- List/Retrieve: Allow any (or authenticated only - your choice)
- Create: Authenticated only (need to know who's posting)
- Update/Delete: Author only (can't edit others' posts)
- Like/Share: Authenticated only

For create:
- Automatically set author to request.user
- Don't let users specify author in request body

Expected response format for like endpoint:
{
  "id": 1,
  "likes_count": 43,
  "is_liked": true,
  ... (rest of post fields)
}

Think about:
- How do you auto-set author on create? (Override perform_create())
- How do you restrict update/delete to author only? (Custom permission class)
- For /replies/, how do you filter by parent? (@action decorator + queryset filter)
- For /like/, how do you check if Like already exists? (Like.objects.filter())
- How do you toggle? (If exists → delete, else → create)
- Should posts be ordered newest first? (queryset ordering)
- How do you include nested author data? (Serializer handles this)

Hint: Use ModelViewSet for automatic CRUD
Hint: Override perform_create(self, serializer): serializer.save(author=self.request.user)
Hint: Use @action(detail=True, methods=['get']) for /replies/
Hint: Use @action(detail=True, methods=['post']) for /like/
Hint: Use @action(detail=True, methods=['post']) for /share/
Hint: Filter replies: Post.objects.filter(parent=pk)
Hint: Toggle like: existing = Like.objects.filter(user=user, post=post).first()
Hint: If existing: existing.delete() else: Like.objects.create(user=user, post=post)
Hint: Share is simpler: post.shares_count += 1; post.save()
Hint: For author-only permissions, check obj.author == request.user
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    # Your code here
    pass
```

#### `backend/posts/serializers.py`

```python
"""
TODO: Create Post Serializer - formats post data for API responses

The serializer transforms Post model instances to JSON and validates incoming data.

Key requirement: Nested author data
- Don't just return author: 5 (the ID)
- Return author: { id: 5, username: "alice", first_name: "Alice", last_name: "Smith" }
- Pablo's components expect this nested format!

For input (creating posts):
- Accept: type, content, media_url, parent_id (NOT parent!)
- Don't accept: author, created_at, engagement counts (these are auto-set)

For output (returning posts):
- Include: id, author (nested), type, content, media_url, parent, parent_id, created_at
- Include: likes_count, reply_count, shares_count (REQUIRED for ProfileCard analytics!)
- Include: is_liked (Boolean - has current user liked this post?)
- Author should include: id, username, first_name, last_name

NEW: parent_id field
- Use PrimaryKeyRelatedField for accepting parent_id in POST requests
- Use source='parent' to map to the ForeignKey
- write_only=True so it's only for input

NEW: reply_count field
- SerializerMethodField that counts replies
- Returns count of posts where parent=this post

NEW: is_liked field
- SerializerMethodField that checks if current user has liked this post
- Returns true/false
- Used by frontend to show filled vs empty heart icon

Think about:
- How do you nest author data? (Import and use UserSerializer from users app)
- Should author be read-only? (Yes - set automatically, not by user)
- How do you handle media_url field? (URLField serializes URL automatically)
- For parent field, should it return nested post or just ID? (Just ID is fine)
- How do you accept parent_id but store as parent? (source='parent' on PrimaryKeyRelatedField)
- How do you get current user in serializer? (self.context['request'].user)
- How do you check if user liked post? (Like.objects.filter(user=user, post=obj).exists())

Hint: from users.serializers import UserSerializer
Hint: author = UserSerializer(read_only=True)
Hint: parent_id = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), source='parent', write_only=True, required=False, allow_null=True)
Hint: is_liked = serializers.SerializerMethodField()
Hint: reply_count = serializers.SerializerMethodField()
Hint: def get_is_liked(self, obj): user = self.context['request'].user; return Like.objects.filter(user=user, post=obj).exists()
Hint: def get_reply_count(self, obj): return obj.replies.count()
Hint: Make author read_only so users can't set it manually
"""

from rest_framework import serializers
from .models import Post, Like
from users.serializers import UserSerializer

class PostSerializer(serializers.ModelSerializer):
    # Nested author, is_liked, reply_count, parent_id
    # Your code here
    pass
```

#### `backend/posts/urls.py`

```python
"""
TODO: Configure URL routes for posts API

Use Django REST Framework's router for automatic URL generation.
Router creates all CRUD URLs from your ViewSet automatically.

Routes created by router:
- GET /api/posts/ - list
- POST /api/posts/ - create
- GET /api/posts/:id/ - retrieve
- PUT /api/posts/:id/ - update
- PATCH /api/posts/:id/ - partial_update
- DELETE /api/posts/:id/ - destroy

Plus your custom @action endpoints.

Think about:
- DefaultRouter vs SimpleRouter? (DefaultRouter adds API root view)
- How do you register a ViewSet with router?

Hint: from rest_framework.routers import DefaultRouter
Hint: router = DefaultRouter()
Hint: router.register(r'', PostViewSet, basename='post')
Hint: urlpatterns = router.urls
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

# Your code here
```

#### `backend/posts/apps.py`

```python
"""
TODO: Django app configuration for posts app

Minimal boilerplate - just configure the app name.
"""

from django.apps import AppConfig

class PostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'posts'
```

#### `backend/posts/__init__.py`

```python
# Posts app package marker
# This file can be empty
```

#### `backend/posts/admin.py`

```python
"""
TODO: Register Post model with Django admin

This allows you to view/edit posts in Django's admin interface.
Useful for debugging and managing test data.

Optional enhancements:
- list_display: Show columns in list view
- list_filter: Filter by type, author
- search_fields: Search by content

Hint: from .models import Post
Hint: admin.site.register(Post)
Hint: Or use @admin.register(Post) decorator with ModelAdmin class
"""

from django.contrib import admin
from .models import Post

# Your code here
```

---

### CRYSTAL'S FILES

#### `backend/friends/models.py`

```python
"""
TODO: Create Friendship models - friend connections and requests

NUMENEON has a friends system with two models:
1. Friendship: Represents an accepted friendship between two users
2. FriendRequest: Represents a pending friend request

IMPORTANT: Different from typical symmetric friendship pattern!
This implementation uses a DIRECTIONAL friendship model:
- user: The person who has this friend
- friend: The person they are friends with
- When Alice adds Bob, create TWO Friendship records (Alice→Bob and Bob→Alice)

Friendship model:
- user: The owner of this friend entry (ForeignKey to User)
- friend: The friend (ForeignKey to User)
- created_at: When friendship was created (auto-set)

FriendRequest model:
- from_user: Who sent the request (ForeignKey to User)
- to_user: Who received it (ForeignKey to User)
- created_at: When request was sent (auto-set)
- NO STATUS FIELD! Requests are simply deleted when accepted/declined.

Design decision: When request is accepted:
1. Create TWO Friendship records (both directions)
2. DELETE the FriendRequest (don't update status)

Integration points:
- FriendsContext (Crystal's frontend) fetches and displays friends
- Friends.jsx shows friend list and pending requests
- TopBar might show friend request notifications

Expected response for GET /api/friends/:
[
  { "id": 2, "username": "alice", "first_name": "Alice", "last_name": "Smith" },
  { "id": 3, "username": "bob", "first_name": "Bob", "last_name": "Jones" }
]

Think about:
- How do you get all friends for a user? (Friendship.objects.filter(user=user))
- When accepting: create Friendship(user=to_user, friend=from_user) AND Friendship(user=from_user, friend=to_user)
- When declining: just delete the FriendRequest
- How do you prevent duplicate friendships? (Check in view before creating)
- How do you prevent self-friendship? (Validate in view)

Hint: user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships')
Hint: friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends_of')
Hint: created_at = models.DateTimeField(auto_now_add=True)
Hint: class Meta: unique_together = ['user', 'friend']
"""

from django.db import models
from django.contrib.auth.models import User

class Friendship(models.Model):
    # user → friend (directional, not symmetric)
    # Your code here
    pass

class FriendRequest(models.Model):
    # from_user, to_user, created_at (NO status field!)
    # Your code here
    pass
```

#### `backend/friends/views.py`

```python
"""
TODO: Create Friends API Views - manage friendships and requests

Unlike Posts (CRUD on single model), friends has custom operations.
Use function-based views with @api_view decorator.

Endpoints to create:
- GET /api/friends/ - List current user's friends
- GET /api/friends/requests/ - List pending friend requests (received)
- POST /api/friends/request/:user_id/ - Send friend request to user
- POST /api/friends/accept/:request_id/ - Accept a friend request
- POST /api/friends/decline/:request_id/ - Decline a friend request
- DELETE /api/friends/remove/:user_id/ - Remove a friend

All endpoints require authentication (must be logged in).

IMPORTANT: friend_list returns simple user data, NOT serialized Friendship objects!
Expected response for GET /api/friends/:
[
  {
    "id": 1,
    "username": "alice",
    "first_name": "Alice",
    "last_name": "Smith"
  },
  {
    "id": 2,
    "username": "bob",
    "first_name": "Bob",
    "last_name": "Jones"
  }
]

Expected response for GET /api/friends/requests/:
[
  {
    "id": 1,
    "from_user": {
      "id": 5,
      "username": "charlie",
      "first_name": "Charlie",
      "last_name": "Brown"
    },
    "created_at": "2024-12-19T10:30:00Z"
  }
]

For accept_request:
1. Find the FriendRequest by ID
2. Verify to_user is current user
3. Create TWO Friendship records (both directions)
4. DELETE the FriendRequest
5. Return the new friend's data

For decline_request:
1. Find the FriendRequest by ID
2. Verify to_user is current user
3. DELETE the FriendRequest
4. Return success response

For remove_friend:
1. Delete Friendship where user=me AND friend=target
2. Also delete reverse: user=target AND friend=me
3. Return success

Think about:
- How do you find all friends? (Friendship.objects.filter(user=request.user))
- When accepting, create BOTH directions of friendship
- What if user tries to friend themselves? (Return 400 error)
- What if friend request already exists? (Return 400 error)
- What if users are already friends? (Return 400 error)

Hint: Use @api_view(['GET']) and @api_view(['POST']) decorators
Hint: Use @permission_classes([IsAuthenticated])
Hint: Build response dict manually in views (not using serializers for simple cases)
Hint: Return proper status codes: 201 Created, 400 Bad Request, 404 Not Found
Hint: For accept: Friendship.objects.create(user=to_user, friend=from_user)
Hint: For accept: Friendship.objects.create(user=from_user, friend=to_user)
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from .models import Friendship, FriendRequest

# Your views here:
# friend_list, pending_requests, send_request, accept_request, decline_request, remove_friend
```

#### `backend/friends/serializers.py`

```python
"""
TODO: Create Friends Serializers - format friendship data

You need serializers for:
1. FriendshipSerializer: Serializes Friendship with nested user/friend data
2. FriendRequestSerializer: Serializes FriendRequest with nested from_user/to_user

These serializers use UserSerializer from the users app for nested user data.

For FriendshipSerializer:
- user: nested UserSerializer (read_only)
- friend: nested UserSerializer (read_only)
- fields: id, user, friend, created_at
- read_only_fields: created_at

For FriendRequestSerializer:
- from_user: nested UserSerializer (read_only)
- to_user: nested UserSerializer (read_only)
- fields: id, from_user, to_user, created_at
- read_only_fields: created_at

NOTE: In views, you may build response dicts manually instead of using
these serializers for simple endpoints like friend_list. These serializers
are useful for more complex scenarios.

Think about:
- Import UserSerializer from users app
- Both serializers are read_only focused (no create via serializer)
- How do you make nested serializers read_only? (read_only=True parameter)

Hint: from users.serializers import UserSerializer
Hint: user = UserSerializer(read_only=True)
Hint: friend = UserSerializer(read_only=True)
"""

from rest_framework import serializers
from .models import Friendship, FriendRequest
from users.serializers import UserSerializer

class FriendshipSerializer(serializers.ModelSerializer):
    # Nested user and friend
    # Your code here
    pass

class FriendRequestSerializer(serializers.ModelSerializer):
    # Nested from_user and to_user
    # Your code here
    pass
```

#### `backend/friends/urls.py`

```python
"""
TODO: Configure URL routes for friends API

Map each endpoint to its view function.
These will be included in main urls.py under /api/friends/

Routes:
- GET /api/friends/ → friend_list view
- GET /api/friends/requests/ → friend_requests view
- POST /api/friends/request// → send_request view
- POST /api/friends/accept// → accept_request view
- POST /api/friends/decline// → decline_request view
- DELETE /api/friends/remove// → remove_friend view

Think about:
- Use  for URL parameters that are integers
- Each route maps to a view function

Hint: path('', views.friend_list, name='friend_list')
Hint: path('request//', views.send_request, name='send_request')
"""

from django.urls import path
from . import views

urlpatterns = [
    # Your code here
]
```

#### `backend/friends/apps.py`

```python
"""
TODO: Django app configuration for friends app

Minimal boilerplate.
"""

from django.apps import AppConfig

class FriendsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'friends'
```

#### `backend/friends/__init__.py`

```python
# Friends app package marker
# This file can be empty
```

#### `backend/friends/admin.py`

```python
"""
TODO: Register Friends models with Django admin

Register both Friendship and FriendRequest models.
Useful for debugging friend connections.

Hint: admin.site.register(Friendship)
Hint: admin.site.register(FriendRequest)
"""

from django.contrib import admin
from .models import Friendship, FriendRequest

# Your code here
```

---

### COLLABORATIVE FILE

#### `backend/numeneon/urls.py`

```python
"""
TODO: Root URL configuration for NUMENEON backend

This file imports and includes all the app-specific URL patterns.
Each backend team member adds their app's URLs here.

COLLABORATIVE FILE - Each person adds ONE line:
- Natalia: Users/auth URLs at /api/auth/
- Colin: Posts URLs at /api/posts/
- Crystal: Friends URLs at /api/friends/

The admin URL is already configured.

Pattern: path('api/[prefix]/', include('[app].urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # TODO (Natalia): Add users/auth URLs
    # path('api/auth/', include('users.urls')),

    # TODO (Colin): Add posts URLs
    # path('api/posts/', include('posts.urls')),

    # TODO (Crystal): Add friends URLs
    # path('api/friends/', include('friends.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## SHARED FILES (DO NOT TOUCH)

These files are pre-configured and should not be modified:

- `backend/manage.py`
- `backend/seed_posts.py` - **Populates demo data (see structure below)**
- `backend/numeneon/__init__.py`
- `backend/numeneon/settings.py` - **Configured for PostgreSQL**
- `backend/numeneon/asgi.py`
- `backend/numeneon/wsgi.py`

**seed_posts.py Structure (Dec 2024 update):**

```python
# Creates 6 users × 9 posts each = 54 total posts
# Each user has: 3 thoughts, 3 media, 3 milestones
# Posts spread across 365 days using 'days_ago' field
# Engagement: likes (2-50), comments (0-12), shares (0-8)
# This enables:
#   - Wave chart shows wavy engagement patterns
#   - Heatmap shows year-long activity
#   - Carousel arrows work (3+ posts per type per user)
```

---

**NEXT:** Read `04-FRONTEND-INSTRUCTIONS.md` for frontend pseudocode tasks
