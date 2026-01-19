# 🌱 Database Seeding Guide

This guide explains how to populate your local database with test data so everyone has the same users, posts, and content.

---

## What is Seeding?

**Seeding = Loading shared data into your database**

Pablo exported his database (users, profiles, posts) into a JSON file. You load that file into YOUR database so you have the same data to work with.

```
Pablo's Database → posts_and_users.json → YOUR Database
```

---

## The Order of Operations

```
1. Natalia runs makemigrations + migrate  →  Creates migration files + tables
2. Natalia commits migration files to git
3. Everyone pulls
4. Everyone runs migrate                   →  Applies migrations to their database
5. Everyone runs loaddata                  →  Loads the shared data
```

---

## For Natalia FIRST (Migration Manager)

**You must do this before anyone else can load data:**

```bash
cd backend
pipenv shell

# Create migration files from models
python manage.py makemigrations

# Apply migrations to create tables
python manage.py migrate

# Commit the migration files!
git add */migrations/*.py
git commit -m "Added migrations"
git push
```

---

## For Everyone AFTER Natalia

Once Natalia has pushed migrations:

```bash
# 1. Pull latest code (includes migration files)
git pull

# 2. Go to backend folder
cd backend

# 3. Activate virtual environment
pipenv shell

# 4. Apply migrations (creates tables in YOUR database)
python manage.py migrate

# 5. Load the seed data (fills tables with data)
python manage.py loaddata posts_and_users.json
```

**That's it!** You now have the same users and posts as everyone else.

---

## What Gets Loaded

The `posts_and_users.json` file contains:

### 👥 Users (12 total)

| Username       | Name           | Email             | Password    |
| -------------- | -------------- | ----------------- | ----------- |
| `pabloPistola` | Pablo Cordero  | pablo@test.com    | `test123`   |
| `colinw`       | Colin Weir     | colin@huddl.com   | `test123`   |
| `crystalr`     | Crystal Ruiz   | crystal@huddl.com | `test123`   |
| `nataliap`     | Natalia P      | natalia@huddl.com | `test123`   |
| `arthurb`      | Arthur Bernier | arthur@huddl.com  | `test123`   |
| `titod`        | Tito Del Valle | tito@test.com     | `test123`   |
| `tito`         | Tito           | tito@huddl.com    | `test123`   |
| `alexr`        | Alex Rivera    | alex@huddl.com    | `test123`   |
| `jordanl`      | Jordan Lee     | jordan@huddl.com  | `test123`   |
| `samc`         | Sam Chen       | sam@huddl.com     | `test123`   |
| `ASI`          | A I            | asi@real.com      | `test123`   |
| `admin`        | Admin          | admin@huddl.com   | (superuser) |

### 👤 Profiles

User profiles with bios and avatars (linked to users above).

### 📝 Posts

- **130+ posts** across all users
- Mix of `thoughts`, `media`, and `milestones` types
- Media posts include real Unsplash image URLs
- Posts spread across ~365 days for heatmap testing
- Engagement metrics (likes, comments, shares) pre-populated

### ❤️ Likes

Pre-existing likes on posts for testing.

---

## Important: Migrations FIRST!

You MUST run migrations before loading data:

```bash
python manage.py migrate      # Creates empty tables (STRUCTURE)
python manage.py loaddata ... # Fills tables with data (DATA)
```

**Why?** The data needs tables to go into. Migrations create the tables.

---

## Troubleshooting

### "No installed app with label 'posts'"

→ Models not implemented yet. Complete your `models.py` files first.

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

## For Pablo Only: Updating Seed Data

If you make changes to users/posts and want to share with the team:

```bash
# 1. Export your database to JSON
python manage.py dumpdata auth.User users.Profile posts --indent 2 > posts_and_users.json

# 2. Commit and push
git add posts_and_users.json
git commit -m "Updated seed data"
git push

# 3. Tell the team to pull and run loaddata again
```

---

## Understanding the Commands

| Command                  | What It Does                                   |
| ------------------------ | ---------------------------------------------- |
| `migrate`                | Creates empty database tables (structure)      |
| `loaddata filename.json` | Loads data FROM a JSON file INTO your database |
| `dumpdata app.Model`     | Saves data FROM your database INTO a JSON file |
| `flush`                  | Deletes ALL data (keeps tables)                |

---

## Visual Flow

```
┌─────────────────────────────────────────────────────────────┐
│                    PABLO'S COMPUTER                         │
│                                                             │
│  Database ──dumpdata──► posts_and_users.json ──git push──►  │
└─────────────────────────────────────────────────────────────┘
                                                      │
                                                      │
                                                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    YOUR COMPUTER                            │
│                                                             │
│  ◄──git pull── posts_and_users.json ──loaddata──► Database  │
└─────────────────────────────────────────────────────────────┘
```

Everyone ends up with the same data! 🎉
