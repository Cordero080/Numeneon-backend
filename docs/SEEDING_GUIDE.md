# 🌱 Database Seeding Guide

This guide explains how to populate your local database with test data so everyone has the same posts, users, and content to work with.

---

## Prerequisites

Before you can load seed data, you **MUST** have:

1. ✅ All models implemented (Profile, Post, Like, Friendship, FriendRequest)
2. ✅ Migrations created and applied
3. ✅ Virtual environment activated

---

## Quick Start

From the `backend/` directory:

```bash
# 1. Make sure you're in the right folder
cd backend

# 2. Activate virtual environment
pipenv shell

# 3. Run migrations (if not already done)
python manage.py makemigrations
python manage.py migrate

# 4. Load the seed data
python manage.py loaddata posts_and_users.json
```

---

## What Gets Seeded

The `posts_and_users.json` fixture contains:

### 👥 Users

| Username       | Name           | Email             | Password      |
| -------------- | -------------- | ----------------- | ------------- |
| `pabloPistola` | Pablo Cordero  | pablo@test.com    | `test123`     |
| `colinw`       | Colin Weir     | colin@huddl.com   | `test123`     |
| `crystalr`     | Crystal Ruiz   | crystal@huddl.com | `test123`     |
| `nataliap`     | Natalia P      | natalia@huddl.com | `test123`     |
| `arthurb`      | Arthur Bernier | arthur@huddl.com  | `test123`     |
| `titod`        | Tito Del Valle | tito@test.com     | `test123`     |
| `ASI`          | A I            | asi@real.com      | (check admin) |
| `admin`        | Admin          | admin@huddl.com   | (superuser)   |

### 📝 Posts

- **130+ posts** across all users
- Mix of `thoughts`, `media`, and `milestones` types
- Media posts include real Unsplash image URLs
- Posts spread across ~365 days for heatmap testing
- Engagement metrics (likes, comments, shares) pre-populated

### 👫 Friendships

- Pre-configured friend connections between users
- Bidirectional friendships (both directions created)

### 📨 Friend Requests

- Sample pending friend requests for testing

---

## After Seeding: Create YOUR Profile

The seed data includes shared test users. To add **your own** user with a custom bio:

### Option 1: Django Admin

1. Start the server: `python manage.py runserver`
2. Go to `http://localhost:8000/admin/`
3. Login as `admin` (you may need to reset password)
4. Create your User and Profile

### Option 2: Management Command

```bash
python manage.py create_test_user
```

### Option 3: Signup via Frontend

Once the frontend is connected, use the signup flow.

---

## Troubleshooting

### "No installed app with label 'posts'"

→ Models not implemented yet. Complete `posts/models.py` first.

### "Column does not exist"

→ Migrations not applied. Run:

```bash
python manage.py makemigrations
python manage.py migrate
```

### "Duplicate key" or "UNIQUE constraint failed"

→ Data already exists. To start fresh:

```bash
python manage.py flush  # WARNING: Deletes ALL data
python manage.py loaddata posts_and_users.json
```

### Natural Key Errors

→ The fixture uses natural keys (usernames instead of IDs). Make sure your models match the expected structure.

---

## Re-Seeding (Fresh Start)

To completely reset and re-seed:

```bash
# Delete the database
rm db.sqlite3

# Recreate everything
python manage.py migrate
python manage.py loaddata posts_and_users.json
```

---

## Alternative: Run seed_posts.py

If you want to generate **fresh random data** instead of using the fixture:

```bash
python seed_posts.py
```

This will:

- Clear existing posts
- Create/update users
- Generate new posts with random engagement metrics

⚠️ Note: This creates **different** data than the JSON fixture. Use `loaddata` for consistent data across the team.

---

## Reference

The seed data in `backend/` is synced from `backend-x/` (Pablo's reference implementation). If you need to update seeds, coordinate with Pablo.
