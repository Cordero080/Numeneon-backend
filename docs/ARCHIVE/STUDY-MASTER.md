# NUMENEON STUDY MASTER PLAN

## 🎯 MISSION: Master 22 Critical Files in 14 Days

**Deadline:** January 20, 2026 (Graduation: Jan 24)  
**Study Time:** Jan 6 → Jan 20 = 14 days  
**Goal:** Confidently explain architecture in technical interviews

---

## 👤 WHO I AM

Pablo - UI Lead on NUMENEON (capstone project). 45 years old, career changer, visual-spatial learner with synesthesia. Graduating General Assembly bootcamp January 24th. Need to understand my codebase deeply for technical interviews.

**My Strengths:**

- Visual/spatial thinking
- Pattern recognition (synesthesia helps!)
- UI/UX design background
- Built the entire frontend

**My Challenge:**

- ~100 files in codebase
- Limited time before graduation
- Need to explain technical decisions clearly

---

## 📚 WHAT WE'RE STUDYING

**Frontend:** React 18 + Vite 7.2 + Context API + Axios  
**Backend:** Django 5.2 + DRF + JWT Auth + SQLite  
**Build:** Vite path aliases (@assets, @components, @contexts, etc.)

**Focus:** 22 must-know files (out of 100+ total)

- 14 frontend files
- 8 backend files

---

## 🎓 STUDY METHOD

### Phase 1: File-by-File Linear Study (Days 1-12)

**Goal:** Exposure, not mastery. "I've seen this. I know what lives here."

**For each file:**

1. Read the file with inline comments (explaining syntax)
2. Identify ONE connection to another file
3. Note: "🔗 This connects to [filename]"
4. Write a 2-3 sentence summary
5. Move to next file

**DO NOT:**

- Try to memorize everything
- Get stuck on one file for hours
- Jump around randomly

### Phase 2: Multi-File Flow Tracing (Days 13-14)

**Goal:** Trace complete flows across 3-4 files

**Pick a flow:**

- "Creating a Post": ComposerModal → PostsContext → postsService → apiClient → Backend
- "User Login": Login.jsx → AuthContext → Backend → JWT token → apiClient
- "Loading Feed": Home.jsx → PostsContext → postsService → Backend → TimelineRiverFeed

**For each trace:**

1. Open 3-4 related files
2. Identify where function is DEFINED (file + line)
3. Where it's IMPORTED (file + line)
4. Where it's CALLED (file + line)
5. Practice explaining out loud

**Color coding for roles:**

- 🔴 Entry points (user action starts here)
- 🟡 Orchestrators (manage state, coordinate)
- 🟢 Workers (do the actual work)
- 🔵 Utilities (helpers, tools)

---

## 📅 14-DAY STUDY SCHEDULE

### Days 1-2: Entry Layer (3 files)

- ⏳ main.jsx - How React app starts
- ⏳ App.jsx - Routing and page structure
- ⏳ apiClient.js - Axios setup with JWT interceptors

**What to know:**

- How providers wrap the app (6 total)
- Route definitions
- Layout structure (TopBar + SideNav + content)
- JWT token handling

---

## FILES TO STUDY

**Entry:**

- ⏳ main.jsx → wraps all providers in order
- ⏳ App.jsx → routes + TopBar + SideNav

**Contexts (6 total):**

- ⏳ AuthContext.jsx → login/logout, JWT storage
- ⏳ PostsContext.jsx → posts CRUD, likes
- ⏳ FriendsContext.jsx → friends, requests
- ⏳ MessageContext.jsx → messaging (mock data)
- ⏳ ThemeContext.jsx → dark/light mode
- ⏳ SearchContext.jsx → search modal state (NEW!)

**Services:**

- ⏳ apiClient.js → Axios with JWT interceptors
- ⏳ postsService.js → posts API calls
- ⏳ friendsService.js → friends API calls

**Pages:**

- ⏳ Home.jsx → main feed
- ⏳ Profile.jsx → user profile with dynamic route

**Home Components:**

- ⏳ TimelineRiverFeed.jsx → groups posts, 3-column layout
- ⏳ TimelineRiverRow.jsx → individual post display

**Profile Components:**

- ⏳ TimelineRiver.jsx → profile's timeline
- ⏳ ComposerModal.jsx → create posts

**Backend:**

- ⏳ numeneon/settings.py → Django config
- ⏳ numeneon/urls.py → main router
- ⏳ posts/models.py → Post, Like models
- ⏳ posts/serializers.py → JSON conversion
- ⏳ posts/views.py → PostViewSet
- ⏳ users/views.py → signup, login
- ⏳ friends/views.py → friend operations
- ⏳ friends/models.py → Friendship, FriendRequest

---

## PROJECT STRUCTURE (Updated Jan 2026)

```
frontend/src/
├── main.jsx (🔴 ENTRY - React app starts here)
├── App.jsx (🟡 ORCHESTRATOR - Routing + layout logic)
│
├── contexts/ (🟡 ORCHESTRATORS - Global state managers)
│   ├── index.js (barrel export)
│   ├── AuthContext.jsx (user login/logout, JWT storage)
│   ├── PostsContext.jsx (posts CRUD, likes, comments)
│   ├── FriendsContext.jsx (friends list, requests)
│   ├── MessageContext.jsx (messaging - mock data)
│   ├── ThemeContext.jsx (dark/light mode toggle)
│   └── SearchContext.jsx (search modal state) ← NEW!
│
├── services/ (🔵 UTILITIES - API communication layer)
│   ├── apiClient.js (axios instance, JWT interceptors)
│   ├── postsService.js (posts API calls)
│   └── friendsService.js (friends/users API calls)
│
├── components/
│   ├── layout/ (🟡 ORCHESTRATORS - App frame)
│   │   ├── TopBar/ (header with modals)
│   │   │   ├── SearchModal/ (global search)
│   │   │   ├── MessageModal/ (DMs)
│   │   │   └── NotificationModal/ (notifications)
│   │   └── SideNav/ (navigation - desktop sidebar / mobile bottom)
│   │
│   ├── pages/ (🟢 WORKERS - Main view components)
│   │   ├── Home/ (main feed)
│   │   │   └── components/
│   │   │       ├── TimelineRiverFeed/ (post groups)
│   │   │       ├── TimelineRiverRow/ (post orchestrator)
│   │   │       │   └── components/
│   │   │       │       ├── PostCard/ (individual post)
│   │   │       │       ├── SmartDeck/ (carousel)
│   │   │       │       ├── ThreadView/ (replies)
│   │   │       │       ├── MobileTabNav/ (mobile tabs)
│   │   │       │       └── RepostModal/ (share modal)
│   │   │       ├── DeleteConfirmModal/
│   │   │       └── MediaLightbox/
│   │   │
│   │   ├── Profile/ (user profile page)
│   │   │   └── components/
│   │   │       ├── ProfileCard/ (flip card with front/back)
│   │   │       ├── TimelineRiver/ (profile timeline)
│   │   │       └── ComposerModal/ (create posts)
│   │   │
│   │   ├── Landing/ (public homepage)
│   │   ├── Login/ (auth form)
│   │   ├── Signup/ (registration)
│   │   ├── Friends/ (friends list)
│   │   ├── About/ (about page)
│   │   └── NotFound/ (404)
│   │
│   └── ui/ (🔵 UTILITIES - Reusable components)
│       ├── ProtectedRoute.jsx (auth guard)
│       └── ThemeToggle/ (dark/light switch)
│
├── assets/icons/ (🔵 UTILITIES - SVG components by category)
│   ├── index.js (master export)
│   ├── navigation.jsx, user.jsx, engagement.jsx
│   ├── actions.jsx, media.jsx, ui.jsx
│   ├── sidenav.jsx, analytics.jsx, profile.jsx
│   └── messaging.jsx, misc.jsx
│
└── styles/ (🎨 VISUAL - SCSS architecture)
    ├── main.scss (imports all partials)
    ├── _variables.scss, _theme.scss, _light-mode.scss
    ├── _reset.scss, _typography.scss, _mixins.scss
    ├── _buttons.scss, _cards.scss, _layout.scss
    ├── _animations.scss, _blobs.scss, _utilities.scss
```

### BACKEND STRUCTURE (Django REST API)

```
backend/
├── manage.py (Django CLI)
├── db.sqlite3 (database)
│
├── numeneon/ (Django project config)
│   ├── settings.py (CORS, JWT, installed apps)
│   └── urls.py (🔴 MAIN ROUTER - /api/auth, /api/posts, /api/friends)
│
├── users/ (authentication app)
│   ├── models.py (Profile extends User)
│   ├── views.py (signup, email_login, current user)
│   ├── serializers.py (User ↔ JSON)
│   └── urls.py (/api/auth/signup, /api/auth/login)
│
├── posts/ (posts/comments/likes app)
│   ├── models.py (Post, Like models)
│   ├── views.py (PostViewSet with @actions)
│   ├── serializers.py (Post ↔ JSON with nested author)
│   └── urls.py (router for /api/posts/)
│
└── friends/ (relationships app)
    ├── models.py (Friendship, FriendRequest)
    ├── views.py (function-based views)
    ├── serializers.py
    └── urls.py (/api/friends/)
```

---

## 🔄 KEY FLOWS TO MASTER

### FLOW 1: Creating a Post (Frontend → Backend → Frontend)

```
1. 🔴 ENTRY: User clicks "Post" in ComposerModal
2. 🟡 ORCHESTRATOR: PostsContext.createPost(data) called
3. 🟢 WORKER: postsService.create(data) executes
4. 🔵 UTILITY: apiClient.post('/posts/', data) - JWT added
5. 🌐 BACKEND: POST /api/posts/ → PostViewSet.create()
6. 🌐 BACKEND: PostSerializer validates, Post.objects.create()
7. 🌐 BACKEND: Returns new post JSON (201)
8. 🟢 WORKER: postsService returns response.data
9. 🟡 ORCHESTRATOR: PostsContext adds post to state
10. 🔴 UI: Components re-render with new post
```

### FLOW 2: User Login

```
1. 🔴 ENTRY: User submits Login form
2. 🟡 ORCHESTRATOR: AuthContext.login(credentials)
3. 🔵 UTILITY: apiClient.post('/auth/login/', credentials)
4. 🌐 BACKEND: email_login() validates, generates JWT
5. 🌐 BACKEND: Returns { access, refresh, user }
6. 🟡 ORCHESTRATOR: AuthContext stores in localStorage
7. 🟡 ORCHESTRATOR: Sets currentUser state
8. 🔴 UI: Redirects to /home
```

### FLOW 3: Liking a Post

```
1. 🔴 ENTRY: User clicks heart in TimelineRiverRow
2. 🟡 ORCHESTRATOR: PostsContext.likePost(id)
3. 🟢 WORKER: postsService.like(id)
4. 🔵 UTILITY: apiClient.post('/posts/{id}/like/')
5. 🌐 BACKEND: PostViewSet.like() - @action
6. 🌐 BACKEND: Toggle Like, update post.likes_count
7. 🌐 BACKEND: Returns updated post
8. 🟡 ORCHESTRATOR: PostsContext updates post in state
9. 🔴 UI: Heart toggles, count updates
```

---

## BACKEND API ENDPOINTS REFERENCE

### Auth (/api/auth/)

- POST /api/auth/signup/ → Create account
- POST /api/auth/login/ → Login, returns JWT
- GET /api/auth/current/ → Get current user

### Posts (/api/posts/)

- GET /api/posts/ → List feed posts
- GET /api/posts/?username=xxx → User's posts
- POST /api/posts/ → Create post
- GET /api/posts/:id/ → Single post
- DELETE /api/posts/:id/ → Delete post
- POST /api/posts/:id/like/ → Toggle like
- POST /api/posts/:id/share/ → Increment share
- GET /api/posts/:id/replies/ → Get replies

### Friends (/api/friends/)

- GET /api/friends/ → List friends
- GET /api/friends/requests/ → Pending requests
- POST /api/friends/request/:id/ → Send request
- POST /api/friends/accept/:id/ → Accept request
- POST /api/friends/decline/:id/ → Decline
- DELETE /api/friends/remove/:id/ → Unfriend

---

## TEACHING RULES (For Claude Sessions)

1. Comment INSIDE the code first, then explain after
2. Full sentences - no assumptions
3. Explain syntax that might be confusing
4. Show what block does and in what order things run
5. Note connections with 🔗 CONNECTION: filename
6. One mini-connection per file, then stop
7. Don't overwhelm - exposure, not mastery
