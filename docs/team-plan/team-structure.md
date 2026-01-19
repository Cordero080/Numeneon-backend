# NUMENEON Backend - Team Structure & Workflow

## Project Overview

**NUMENEON** is a cyberpunk-themed social media application. This is the **backend repository** containing the Django REST API that serves the React frontend.

The team will **rebuild from pseudocode shells** to learn architecture and create legitimate git history.

**Why rebuild from pseudocode?**

- **Git history matters** - everyone needs PR records showing their contributions
- **Learning value** - team learns Django, DRF, authentication, and API design
- **AI-assisted** - Pseudocode is detailed enough for AI to help generate accurate code

---

## Tech Stack (Backend)

- **Framework:** Django 5.2+
- **API:** Django REST Framework
- **Database:** PostgreSQL (migrated from SQLite Jan 2026)
- **Auth:** JWT tokens via `djangorestframework-simplejwt`
- **Package Manager:** pipenv

---

## Team Roles (Backend)

| Person      | App        | Focus Areas                                   |
| ----------- | ---------- | --------------------------------------------- |
| **Natalia** | `users/`   | Auth system, Profile model, JWT login         |
| **Colin**   | `posts/`   | Posts model, Like model, CRUD API, engagement |
| **Crystal** | `friends/` | Friendship model, FriendRequest, social graph |

---

## Project Structure (Backend)

```
backend/
├── manage.py                    [Django management]
├── Pipfile                      [Dependencies]
├── posts_and_users.json         [Demo fixture data]
├── numeneon/                    [Django settings]
│   ├── settings.py
│   ├── urls.py                  [Main URL router]
│   ├── wsgi.py
│   └── asgi.py
├── users/                       [Natalia]
│   ├── models.py               (Profile model)
│   ├── views.py                (signup, login, me)
│   ├── serializers.py          (User/Profile serializers)
│   ├── urls.py                 (auth routes)
│   └── migrations/
├── posts/                       [Colin]
│   ├── models.py               (Post, Like models)
│   ├── views.py                (PostViewSet)
│   ├── serializers.py          (PostSerializer)
│   ├── urls.py                 (posts routes)
│   ├── admin.py
│   └── migrations/
└── friends/                     [Crystal]
    ├── models.py               (Friendship, FriendRequest)
    ├── views.py                (friend views)
    ├── serializers.py          (friend serializers)
    ├── urls.py                 (friends routes)
    ├── admin.py
    └── migrations/
```

---

## Quick Start

### ⚠️ IMPORTANT: Read This First!

**DO NOT run `pip install -r requirements.txt`** - This project uses **Pipfile** (pipenv), not requirements.txt!

**DO NOT run `python manage.py migrate`** until Natalia announces migrations are ready!

---

### 1. Clone and Setup Remote

```bash
# Clone Colin's repo (the czar)
git clone https://github.com/colinw10/Numeneon-backend.git
cd Numeneon-backend

# Add czar remote (if you forked instead)
git remote add czar https://github.com/colinw10/Numeneon-backend.git
```

### 2. Setup Environment (Use Pipenv!)

```bash
cd backend
pipenv install --dev    # NOT pip install -r requirements.txt!
pipenv shell
```

### 3. Database Setup (WAIT FOR NATALIA!)

**Order of Operations:**

1. **Natalia** runs `makemigrations` + `migrate` AFTER all models are implemented
2. **Natalia** commits migration files and pushes to czar
3. **Everyone** pulls from czar: `git pull czar dev`
4. **Everyone** runs migrations: `python manage.py migrate`
5. **Everyone** loads seed data: `python manage.py loaddata posts_and_users.json`

```bash
# ONLY after Natalia pushes migrations:
git pull czar dev
python manage.py migrate
python manage.py loaddata posts_and_users.json
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Server runs at `http://127.0.0.1:8000`

---

## API Endpoints Summary

### Users App (`/api/auth/`)

| Method | Endpoint                   | Description                      |
| ------ | -------------------------- | -------------------------------- |
| POST   | `/api/auth/signup/`        | Create new user                  |
| POST   | `/api/auth/login/`         | Login with EMAIL, returns JWT    |
| GET    | `/api/auth/me/`            | Get current user (authenticated) |
| POST   | `/api/auth/token/refresh/` | Refresh JWT token                |

### Posts App (`/api/posts/`)

| Method | Endpoint                   | Description           |
| ------ | -------------------------- | --------------------- |
| GET    | `/api/posts/`              | List all posts        |
| POST   | `/api/posts/`              | Create new post       |
| GET    | `/api/posts/{id}/`         | Get single post       |
| PUT    | `/api/posts/{id}/`         | Update post           |
| DELETE | `/api/posts/{id}/`         | Delete post           |
| GET    | `/api/posts/{id}/replies/` | Get replies to post   |
| POST   | `/api/posts/{id}/like/`    | Toggle like           |
| POST   | `/api/posts/{id}/share/`   | Increment share count |

### Friends App (`/api/friends/`)

| Method | Endpoint                             | Description                 |
| ------ | ------------------------------------ | --------------------------- |
| GET    | `/api/friends/`                      | List current user's friends |
| GET    | `/api/friends/requests/`             | List pending requests       |
| POST   | `/api/friends/request/{user_id}/`    | Send friend request         |
| POST   | `/api/friends/accept/{request_id}/`  | Accept request              |
| POST   | `/api/friends/decline/{request_id}/` | Decline request             |
| DELETE | `/api/friends/remove/{user_id}/`     | Remove friend               |

---

## Demo Users

The fixture (`posts_and_users.json`) includes these test users:

| Username       | Email             | Password |
| -------------- | ----------------- | -------- |
| `pabloPistola` | pablo@test.com    | test123  |
| `titod`        | tito@test.com     | test123  |
| `arthurb`      | arthur@test.com   | test123  |
| `nataliap`     | natalia@test.com  | test123  |
| `colinw`       | colin@huddl.com   | test123  |
| `crystalr`     | crystal@huddl.com | test123  |

---

## Key Design Decisions

### 1. Login Uses EMAIL (Not Username)

Frontend sends `{ "email": "...", "password": "..." }` for login.

Backend must:

1. Look up user by email
2. Authenticate with username

### 2. Directional Friendships

When Alice and Bob become friends, create **TWO** Friendship records:

- `Friendship(user=alice, friend=bob)`
- `Friendship(user=bob, friend=alice)`

### 3. FriendRequest Has NO Status Field

- Accepted requests → Create friendships, DELETE the request
- Declined requests → Just DELETE the request

### 4. Post Engagement Counts

`likes_count`, `comment_count`, `shares_count` are denormalized fields on Post model. Update them when likes/comments/shares happen.

### 5. media_url (Not ImageField)

Posts use `URLField` for `media_url`, not `ImageField`. This stores URL strings pointing to images rather than handling file uploads.

---

## Working with the Shell

Each Python file has detailed pseudocode comments. Example:

```python
"""
TODO: Create the Profile model - extends Django's built-in User

Fields you need:
- user: OneToOne link to Django's User model
- avatar: URL field (optional)
- bio: Text field (optional)
...
"""

class Profile(models.Model):
    # Your code here
    pass
```

Replace `pass` with actual implementation based on the TODO comments.

---

## Getting Updates from Czar

Whenever Colin (czar) merges PRs, pull the latest:

```bash
git fetch czar
git merge czar/dev
# Or shortcut:
git pull czar dev
```

---

## Testing Your Work

```bash
# Run Django tests
python manage.py test

# Check for errors
python manage.py check

# Test endpoints manually
curl http://127.0.0.1:8000/api/posts/
```

---

## Individual Task Files

See detailed instructions for each team member:

- [natalia.md](./natalia.md) - Users/Auth system
- [colin.md](./colin.md) - Posts system
- [crystal.md](./crystal.md) - Friends system
