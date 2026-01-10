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

## 1. Clone the Team Repo

**Important:** Clone Colin's repository directly — do not fork it.

```bash
git clone https://github.com/colinw10/huddl-app.git
cd huddl-app
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
mkdir backend
cd backend
```

---

## 4. Create Virtual Environment

Set up a Python virtual environment to isolate dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
```

Your terminal prompt should now show `(venv)`.

---

## 5. Install Django

Install Django inside your virtual environment:

```bash
pip install django
django-admin --version
```

The version output confirms Django installed successfully.

---

## 6. Create Django Project

Initialize the Django project inside the `backend` folder:

```bash
django-admin startproject huddl .
```

**Note:** The dot (`.`) prevents creating nested `huddl/huddl` folders.

---

## 7. Apply Initial Migrations

Run Django's initial database migrations:

```bash
python manage.py migrate
```

This initializes Django's built-in tables (users, sessions, etc.).

---

## 8. Run the Dev Server

Start the development server:

```bash
python manage.py runserver
```

The server runs at **http://127.0.0.1:8000**

Visit it in your browser to see Django's welcome page.

---

## 9. Workflow Rules

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
# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py migrate

# Start dev server
python manage.py runserver

# Create new branch
git checkout -b yourname-feature

# Check current branch
git branch
```

---

**Next Steps:** Ready to build the Django app architecture.
