# Django Backend Setup Guide

## Here is the basic gist of the backend folders and their use

backend/
├── manage.py              ← Your command center
├── huddl/                 ← Project settings/config
│   ├── settings.py        ← Master config
│   └── urls.py            ← Main routing
├── db.sqlite3             ← Your database
└── venv/                  ← Python packages

This guide will walk you through setting up the Huddl Django backend on your local machine.

---

## 1. Clone the Team Repo (from Czar)

**Important:** Clone Colin's repository (the "czar").

```bash
git clone https://github.com/colinw10/Numeneon-backend.git
cd Numeneon-backend

# Add czar as a remote (for pulling updates later)
git remote add czar https://github.com/colinw10/Numeneon-backend.git
```

---

## 2. Create Your Personal Branch

**Never work directly on `main`.** Always create a new branch for your work.

```bash
git checkout -b yourname-feature
```

**Rule:** Each feature = new branch + pull request.

---

## 3. Backend Folder Setup

Navigate into the backend directory:

```bash
cd backend
```

The backend folder already exists with all the Django apps.

---

## 4. Install Dependencies (USE PIPENV!)

**⚠️ DO NOT use `pip install -r requirements.txt`** - This project uses Pipfile!

Install all dependencies using pipenv:

```bash
pipenv install --dev
pipenv shell
```

Your terminal prompt should now show `(venv)` or similar.

This installs Django and all other required packages automatically from the Pipfile.

---

## 5. Apply Migrations (WAIT FOR NATALIA!)

**⚠️ DO NOT run migrations until Natalia announces they are ready!**

**Order of Operations:**
1. Natalia creates migrations AFTER all models are implemented
2. Natalia pushes migration files to czar
3. Everyone pulls from czar: `git pull czar dev`
4. Everyone runs migrations: `python manage.py migrate`
5. Everyone loads seed data: `python manage.py loaddata posts_and_users.json`

```bash
# ONLY after Natalia pushes migrations:
git pull czar dev
python manage.py migrate
python manage.py loaddata posts_and_users.json
```

This creates all database tables and loads shared test data.

---

## 6. Run the Dev Server

Start the development server:

```bash
python manage.py runserver
```

The server runs at **http://127.0.0.1:8000**

Visit it in your browser to see Django's welcome page.

---

## 7. Workflow Rules

✅ **Do:**

- Always work on your personal branch
- Submit pull requests to `main`
- Keep commits small and clear
- Test locally before pushing

❌ **Don't:**

- Never push directly to `main`
- Don't commit without testing

**Review Process:**

- Team lead (Colin) reviews all PRs
- PRs must be approved before merging
- Discuss changes in PR comments

---

## Quick Reference

```bash
# Install dependencies (NOT pip install -r requirements.txt!)
pipenv install --dev

# Activate virtual environment
pipenv shell

# Pull latest from czar
git pull czar dev

# Run migrations (ONLY after Natalia pushes them!)
python manage.py migrate

# Load seed data
python manage.py loaddata posts_and_users.json

# Start dev server
python manage.py runserver

# Create new branch
git checkout -b yourname-feature

# Check current branch
git branch
```

---

**Next Steps:** Ready to build the Django app architecture.
