# Backend Architecture Documentation

## 🌐 Deployment

| Component         | URL                                   |
| ----------------- | ------------------------------------- |
| Backend (Render)  | https://numeneon-backend.onrender.com |
| Frontend (Vercel) | https://numeneon-frontend.vercel.app  |

---

## 📁 Contents

| File                                     | Purpose                                 |
| ---------------------------------------- | --------------------------------------- |
| [SETUP.md](SETUP.md)                     | Setup instructions & Friends API docs   |
| [models-overview.md](models-overview.md) | All 6 models with fields, relationships |
| [api-endpoints.md](api-endpoints.md)     | All 13 API endpoints                    |
| [erd-prompt.md](erd-prompt.md)           | Prompt to generate ERD diagram          |

---

## Quick Stats

| Metric            | Count                                   |
| ----------------- | --------------------------------------- |
| **Models**        | 7 (6 custom + 1 Django User)            |
| **API Endpoints** | 18                                      |
| **Django Apps**   | 4 (users, posts, friends, messages_app) |

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
