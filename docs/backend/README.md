# Backend Documentation

> **Last Updated:** January 25, 2026

---

## 🌐 Live URLs

| Component | URL |
|-----------|-----|
| **Backend (Render)** | https://numeneon-backend.onrender.com |
| **Frontend (Vercel)** | https://numeneon-frontend.vercel.app |
| **Admin Panel** | https://numeneon-backend.onrender.com/admin/ |

---

## 📁 Documentation Index

### 🚀 Start Here (New to the project?)

| # | Doc | What it covers |
|---|-----|----------------|
| 1 | [SETUP.md](SETUP.md) | Local dev setup, install dependencies, run server |
| 2 | [../deployment/](../deployment/) | Production deployment, CORS config, test accounts |

### 📖 Reference Docs

| Doc | What it covers |
|-----|----------------|
| [api-endpoints.md](api-endpoints.md) | All 14 API endpoints with request/response examples |
| [models-overview.md](models-overview.md) | All 7 models with fields & relationships |

### 📢 Team Updates (What's New)

| Date | Update |
|------|--------|
| [2025-01-25](team-updates/2025-01-25-messaging-system.md) | ✨ **Direct Messaging + User Search** |

---

## Quick Stats

| Metric | Count |
|--------|-------|
| **Models** | 7 (6 custom + 1 Django User) |
| **API Endpoints** | 14 |
| **Django Apps** | 4 (users, posts, friends, messages_app) |

## Model Summary

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    User     │────┤   Profile   │     │    Post     │
│  (Django)   │1  1│   (users)   │     │   (posts)   │
└─────────────┘     └─────────────┘     └─────────────┘
      │                                       │
      │ 1                                     │ 1
      │                                       │
      ▼ *                                     ▼ *
┌─────────────┐                         ┌─────────────┐
│ Friendship  │                         │    Like     │
│  (friends)  │                         │   (posts)   │
└─────────────┘                         └─────────────┘
      │
      │
      ▼
┌─────────────────┐     ┌─────────────────┐
│  FriendRequest  │     │     Message     │
│    (friends)    │     │ (messages_app)  │
└─────────────────┘     └─────────────────┘
```
