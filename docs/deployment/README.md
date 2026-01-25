# Deployment Documentation

> **Last Updated:** January 25, 2026

---

## 🌐 Live URLs

| Component | Platform | URL |
|-----------|----------|-----|
| **Frontend** | Vercel | https://numeneon-frontend.vercel.app |
| **Backend** | Render | https://numeneon-backend.onrender.com |
| **Admin Panel** | Render | https://numeneon-backend.onrender.com/admin/ |
| **Database** | PostgreSQL (Render) | Internal connection |

---

## 📁 Docs in this folder

| File | What it covers |
|------|----------------|
| [test-accounts.md](test-accounts.md) | Login credentials, seed data users |
| [cors-configuration.md](cors-configuration.md) | CORS/CSRF troubleshooting for Vercel ↔ Render |

---

## 🚀 How Deployment Works

### Auto-Deploy from GitHub

1. **Render** watches `colinw10/Numeneon-backend` → `dev` branch
2. **Vercel** watches `colinw10/Numeneon-frontend` → `dev` branch
3. Push to `dev` → Auto deploys in ~2-3 minutes

### What happens on deploy (build.sh)

1. `pip install -r requirements.txt` - Install Python packages
2. `python manage.py migrate` - Apply database migrations
3. Creates admin superuser (`admin` / `admin123`)
4. Creates team test users (natalia, crystal, colin, pabloPistola)
5. Runs `seed_posts.py` - Creates ~130 sample posts
6. Runs `seed_messages` - Creates sample DM conversations

---

## 🔑 Quick Reference

### Environment Differences

| Setting | Development | Production |
|---------|-------------|------------|
| CORS | `localhost:5173` | `numeneon-frontend.vercel.app` + regex for previews |
| DEBUG | `True` | `False` |
| Database | Local SQLite/PostgreSQL | Render PostgreSQL |
| CSRF | Middleware disabled | Middleware disabled (JWT-only API) |

### Git Remotes

```bash
# Your fork
origin = git@github.com:YOUR_USERNAME/Numeneon-backend.git

# Team repo (Render deploys from here)
czar = https://github.com/colinw10/Numeneon-backend.git
```

### Deploy Workflow

```bash
# 1. Make changes locally
# 2. Commit to your branch
git add -A && git commit -m "your message"

# 3. Push to czar to trigger deploy
git push czar dev
```
