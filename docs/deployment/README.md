# Deployment Documentation

> **Last Updated:** January 24, 2026

---

## 📁 Contents

| File                                           | Purpose                        |
| ---------------------------------------------- | ------------------------------ |
| [cors-configuration.md](cors-configuration.md) | CORS setup for Vercel ↔ Render |

---

## Deployment Stack

| Component | Platform            | URL                                  |
| --------- | ------------------- | ------------------------------------ |
| Frontend  | Vercel              | https://numeneon-frontend.vercel.app |
| Backend   | Render              | TBD                                  |
| Database  | PostgreSQL (Render) | Internal                             |

---

## Quick Reference

### Frontend → Backend Communication

The React frontend on Vercel makes API calls to the Django backend on Render. CORS must be configured to allow cross-origin requests.

### Environment Differences

| Setting  | Development                        | Production                     |
| -------- | ---------------------------------- | ------------------------------ |
| CORS     | `localhost:5173`, `localhost:3000` | `numeneon-frontend.vercel.app` |
| DEBUG    | `True`                             | `False`                        |
| Database | Local PostgreSQL                   | Render PostgreSQL              |
