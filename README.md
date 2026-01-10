# NUMENEON

> A cyberpunk-themed social media app with a unique **River Timeline** feed design.

Built with **React + Vite** (frontend) and **Django REST Framework** (backend).

---

## 🌊 The River Timeline

NUMENEON's signature feature is the **River Timeline** — a feed that flows like three parallel streams instead of one endless scroll.

```
┌─────────────────────────────────────────────────────────┐
│                    RIVER TIMELINE                        │
├───────────────┬───────────────┬─────────────────────────┤
│ 💭 THOUGHTS   │ 🖼️ MEDIA      │ 🏆 MILESTONES           │
│ Text posts    │ Photos/videos │ Achievements            │
├───────────────┼───────────────┼─────────────────────────┤
│ User A Ep2    │ User A Ep2    │ User A Ep2              │
│ [◀ 2/12 ▶]    │ [◀ 1/12 ▶]    │                         │
├───────────────┼───────────────┼─────────────────────────┤
│ User B        │ User B        │ User B                  │
│ [◀ 5/12 ▶]    │ [◀ 3/12 ▶]    │ [◀ 1/12 ▶]              │
├───────────────┼───────────────┼─────────────────────────┤
│ User A Ep1    │ User A Ep1    │ User A Ep1              │
│ [12/12 full]  │ [◀ 3/12 ▶]    │                         │
└───────────────┴───────────────┴─────────────────────────┘
```

**How it works:**

1. **One row = one user + one epoch** — A user's posts are grouped into a single row
2. **Three columns = three content types** — Thoughts (text), Media (images), Milestones (achievements)
3. **Carousel navigation** — Click arrows to browse posts without scrolling
4. **Max 12 per category** — When any column fills up, a new "epoch" (row) is created
5. **Pure recency sorting** — Newest activity rises to the top, no algorithmic manipulation

**Why this design?**

- **Scan 10 users at a glance** instead of scrolling through 30+ individual posts
- **Context stays grouped** — see all of someone's recent content together
- **Discover content types** — quickly see if someone posts thoughts vs media vs achievements
- **No "rich get richer"** — engagement doesn't boost visibility, only recency matters

See [docs/features/RiverTimeline.md](./docs/features/RiverTimeline.md) for the full technical specification.

---

## ✨ Key Features

| Feature                  | Description                                                          |
| ------------------------ | -------------------------------------------------------------------- |
| **River Timeline**       | Three-column feed with epoch-based grouping and carousel navigation  |
| **Profile Flip Card**    | Dual-sided card — profile info on front, analytics dashboard on back |
| **Engagement Analytics** | Wave chart + GitHub-style activity heatmap                           |
| **Direct Messaging**     | Real-time DMs with conversation list                                 |
| **User Navigation**      | Click any avatar/username to view their profile                      |
| **Card User Headers**    | Every card shows who posted it (avatar + username inside)            |
| **Mobile Category Tabs** | Tab-based navigation for mobile (Thoughts/Media/Milestones)          |
| **Search Modal**         | Search users and posts globally                                      |
| **Theme Toggle**         | Dark mode (cyberpunk) / Light mode (clean)                           |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python seed_posts.py       # Create demo data
python manage.py runserver
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App runs at `http://localhost:5173` • API at `http://localhost:8000`

---

## 📁 Project Structure

```
numeneon/
├── backend/                 # Django REST API
│   ├── numeneon/           # Project settings
│   ├── users/              # Auth & profiles
│   ├── posts/              # Posts, likes, replies
│   ├── friends/            # Friend requests & connections
│   └── seed_posts.py       # Demo data generator
│
├── frontend/               # React + Vite
│   └── src/
│       ├── components/
│       │   ├── layout/     # TopBar, SideNav, MessageModal
│       │   └── pages/      # Home, Profile, Login, etc.
│       ├── contexts/       # Auth, Posts, Friends, Messages, Theme
│       ├── services/       # API client
│       └── styles/         # Global SCSS design system
│
└── docs/                   # Documentation
    ├── features/           # Feature specs (RiverTimeline, etc.)
    └── features-implemented/  # Implementation details
```

---

## 🎨 Design System

**Colors:**

- Cyan `#4fffff` — Thoughts, primary actions
- Purple `#c9a8ff` — Media, secondary
- Green `#1ae784` — Milestones, success
- Magenta `#e94ec8` — Accents

**Fonts:**

- Orbitron — Headings (futuristic)
- Rajdhani — Body text (clean, readable)

**Effects:**

- Glassmorphic surfaces with backdrop blur
- Neon glow shadows
- Chamfered corners (clip-path, not border-radius)
- Scan line overlays

---

## 📖 Documentation

- [Backend Setup](./BACKEND_SETUP.md)
- [River Timeline](./docs/features/RiverTimeline.md)
- [Implemented Features](./docs/features-implemented/README.md)
- [Visual Identity](./docs/features/VisualIdentitySystem.md)

---

## 🛠️ Tech Stack

| Layer    | Tech                                          |
| -------- | --------------------------------------------- |
| Frontend | React 18, Vite, React Router, SCSS            |
| Backend  | Django 4.x, Django REST Framework, Simple JWT |
| Database | SQLite (dev), PostgreSQL (prod)               |

---

## 👥 Team

- **Pablo** — UI Architecture, Visual Design
- **Natalia** — Backend, Auth, Migrations
- **Colin** — Posts, Team Lead
- **Crystal** — Friends, Frontend
- **Tito** — Infrastructure, Utilities

---

_"In the neon glow, every post tells a story."_
