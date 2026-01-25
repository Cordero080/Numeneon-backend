# Test Accounts & Seed Data on Production (Render)

> **Last Updated:** January 24, 2026

---

## Quick Start

After deploy, the database is pre-populated with users and posts. Just log in and explore!

---

## Test Accounts (For Teammates)

| Username     | Email              | Password | Notes        |
| ------------ | ------------------ | -------- | ------------ |
| natalia      | natalia@test.com   | test123  | Team login   |
| crystal      | crystal@test.com   | test123  | Team login   |
| colin        | colin@test.com     | test123  | Team login   |
| pabloPistola | pablo@test.com     | test123  | Team login   |
| admin        | admin@numeneon.com | admin123 | Django admin |

### How to Log In

1. Go to: https://numeneon-frontend.vercel.app/login
2. Enter your **EMAIL** (not username!) and password
3. Click Login

Example:

```
Email: natalia@test.com
Password: test123
```

---

## Seed Data Users (Post Authors)

These users are created by `seed_posts.py` and have posts in the feed:

| Username     | Email            | First Name | Posts    |
| ------------ | ---------------- | ---------- | -------- |
| pabloPistola | pablo@test.com   | Pablo      | 24 posts |
| titod        | tito@test.com    | Tito       | 22 posts |
| arthurb      | arthur@test.com  | Arthur     | 22 posts |
| nataliap     | natalia@test.com | Natalia    | 20 posts |
| colinw       | colin@test.com   | Colin      | 22 posts |
| crystalr     | crystal@test.com | Crystal    | 20 posts |

**All passwords:** `test123`

---

## What to Expect After Deploy

### Posts (~130 total)

- Posts spread across 365 days (for heatmap/analytics)
- 3 post types: `thoughts`, `media`, `milestones`
- Media posts have real image URLs (auroras, cyberpunk cities, tech)
- Engagement stats (likes, comments, shares) for analytics

### Sample Post Content

- Pablo: "Kata: choreographed violence against nobody."
- Arthur: "Quantum entanglement > WiFi reliability."
- Natalia: "Django ORM is just SQL with extra steps."
- Colin: "Meetings could have been emails. All of them."
- Crystal: "CSS grid finally makes sense. Only took a week."
- Tito: "Debugging is leaving angry comments for past me."

### Messages

- Sample conversations between users (from `seed_messages`)

---

## Admin Panel

To access Django admin:

1. Go to: https://numeneon-backend.onrender.com/admin/
2. Login with:
   - Username: `admin`
   - Password: `admin123`

---

## Triggering a Fresh Seed

If you need to reset and re-seed:

1. Go to **Render Dashboard** → your Web Service
2. Click **Manual Deploy** → **Clear build cache & deploy**
3. Wait for deploy to complete (~2-3 min)

Note: `seed_posts.py` clears existing posts before creating new ones.

---

## Important Notes

**Two sets of users exist:**

- **Team logins** (natalia, crystal, colin) - for you to log in
- **Seed users** (nataliap, colinw, crystalr) - authors of posts in feed

They have similar names but different usernames.

**Use EMAIL to login, not username!**
The login form uses email. Use `natalia@test.com`, not `natalia`.
