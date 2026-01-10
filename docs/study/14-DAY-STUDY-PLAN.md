# 🎯 14-DAY NUMENEON MASTERY PLAN

**Start:** January 6, 2026  
**Deadline:** January 20, 2026  
**Graduation:** January 24, 2026

---

## 📊 THE NUMBERS

- **Total Files in Project:** ~100 files
- **Must-Know Files:** 22 files (14 frontend + 8 backend)
- **That's only 22% of codebase!**
- **Daily Goal:** ~1.5 files/day
- **Final 4 Days:** Practice explaining flows out loud

---

## 🗓️ DAILY SCHEDULE

### WEEK 1: FRONTEND FOUNDATION

#### Day 1 (Jan 6 - TODAY): Entry + Infrastructure

**Files:** main.jsx, App.jsx, apiClient.js

**Learn:**

- How React app initializes
- Provider nesting order (Auth → Posts → Friends → Message → Theme → Search)
- Route definitions and protected routes
- Axios interceptors for JWT tokens

**Interview Question:** "How does your app start up and handle authentication?"

---

#### Day 2 (Jan 7): Auth + State Management

**Files:** AuthContext.jsx, PostsContext.jsx, FriendsContext.jsx

**Learn:**

- Context API pattern
- Login/logout flow
- How contexts call services
- Token storage in localStorage

**Interview Question:** "How do you manage global state?"

---

#### Day 3 (Jan 8): Services Layer

**Files:** postsService.js, friendsService.js

**Learn:**

- Service layer pattern (separation of concerns)
- Async/await with API calls
- How services wrap apiClient
- Same pattern across all services

**Interview Question:** "Walk me through your API architecture"

---

#### Day 4 (Jan 9): Main Feed

**Files:** Home.jsx, TimelineRiverFeed.jsx

**Learn:**

- How pages consume contexts
- Post grouping by date
- 3-column layout logic

**Interview Question:** "Explain your component hierarchy"

---

#### Day 5 (Jan 10): Post Display + Actions

**Files:** TimelineRiverRow.jsx

**Learn:**

- Individual post rendering
- Like/comment/share actions
- Vite path aliases (@assets, @contexts)
- Carousel for multiple posts
- PostCard, ThreadView, RepostModal all use `@components/pages/Home/utils/timeFormatters`

**Interview Question:** "Walk me through your main feed feature"

**Pro Tip:** Notice how ALL files now use path aliases - no more `../../../../` patterns!

---

#### Day 6 (Jan 11): Profile Page

**Files:** Profile.jsx, TimelineRiver.jsx

**Learn:**

- Dynamic routing (/profile/:username)
- useParams hook
- ProfileCard integration
- Expandable comment composer

**Interview Question:** "How do you handle dynamic routes?"

---

#### Day 7 (Jan 12): Post Creation

**Files:** ComposerModal.jsx, SearchContext.jsx

**Learn:**

- Modal patterns (createPortal)
- Form state management
- Post types (thought, media, milestone)
- Simple context for UI state

**Interview Question:** "Explain the full flow of creating a post"

---

### WEEK 2: BACKEND + INTEGRATION

#### Day 8 (Jan 13): Django Configuration

**Files:** numeneon/settings.py, numeneon/urls.py

**Learn:**

- REST framework settings
- CORS configuration
- URL routing to apps (/api/auth/, /api/posts/, /api/friends/)

**Interview Question:** "How is your backend configured?"

---

#### Day 9 (Jan 14): Posts Backend - Models

**Files:** posts/models.py

**Learn:**

- Django model fields
- Relationships (ForeignKey for author, parent)
- Post types (thoughts, media, milestones)
- Like model with unique constraint

**Interview Question:** "Describe your database schema"

---

#### Day 10 (Jan 15): Posts Backend - API

**Files:** posts/serializers.py, posts/views.py

**Learn:**

- Model ↔ JSON conversion
- Nested serializers (author data)
- ViewSet CRUD operations
- Custom actions (@action decorator for like, share, replies)

**Interview Question:** "How do your API endpoints work?"

---

#### Day 11 (Jan 16): Auth Backend

**Files:** users/views.py, users/urls.py

**Learn:**

- JWT token generation
- User signup flow
- Login validation
- @api_view and @permission_classes decorators

**Interview Question:** "Walk me through user authentication"

---

#### Day 12 (Jan 17): Friends Backend

**Files:** friends/views.py, friends/models.py

**Learn:**

- Function-based views
- FriendRequest model (from_user, to_user)
- Friendship model
- Accept/decline request flow

**Interview Question:** "Explain the friends system"

---

#### Day 13 (Jan 18): Integration Review

**No new files - Review everything**

**Activities:**

1. Re-read MustKnow.txt (especially the FLOWS section)
2. Trace "Creating a Post" flow end-to-end
3. Trace "User Login" flow end-to-end
4. Identify any gaps

---

#### Day 14 (Jan 19): Flow Practice

**Practice these flows WITHOUT looking at code:**

1. Creating a Post (10 steps)
2. User Login (10 steps)
3. Liking a Post (11 steps)
4. Loading User Profile (10 steps)
5. Sending Friend Request (9 steps)

---

### FINAL STRETCH: INTERVIEW PREP

#### Days 15-17 (Jan 20-22): Mock Interview Practice

**Flow Practice Sessions:**

Session 1: "Creating a Post" - Trace all 10 steps
Session 2: "User Login" - Trace all 10 steps
Session 3: "Liking a Post" - Trace all 11 steps

**Practice explaining out loud:**

- Start with high-level ("User clicks, frontend calls context, context calls service...")
- Then drill into specifics ("apiClient adds JWT token via interceptor...")

---

#### Day 18-20 (Jan 23-24): Final Review

**Mock Interview Questions:**

1. "Walk me through your architecture"
2. "How does authentication work?"
3. "Explain how a post gets created"
4. "What technologies did you use and why?"
5. "What was the most challenging part?"
6. "How would you scale this?"

---

## 🎤 INTERVIEW PREP CHEAT SHEET

### Opening Statement

```
"NUMENEON is a cyberpunk-themed social media platform I built for
my capstone. It's a full-stack React and Django application with
JWT authentication and a modular component architecture. I focused
on clean separation of concerns - Context API for state, service
layer for API calls, and reusable UI components."
```

### Architecture Overview

```
"The frontend uses React 18 with Vite for fast builds. I chose
Context API over Redux because it's simpler for our scale - we have
6 contexts managing auth, posts, friends, messages, theme, and search.
Each context uses a service layer that wraps Axios for API calls.
The backend is Django REST Framework with three apps: users for auth,
posts for content, friends for relationships. JWT tokens handle
authentication with interceptors adding tokens to every request."
```

### Key Technical Decisions

**Q: Why Vite over Create React App?**

```
"Faster dev server, better HMR, native ES modules, built-in support
for path aliases. I configured @assets, @components, @contexts aliases
to keep imports clean and prevent broken paths during refactoring."
```

**Q: Why Context API over Redux?**

```
"Six clear state domains with minimal overlap. Context API provides
what we need without Redux boilerplate. If we needed time-travel
debugging or complex middleware, I'd reconsider."
```

**Q: Why separate service layer?**

```
"Keeps API logic out of components. If endpoints change, I update
one service file instead of many components. Also makes testing easier
and provides a clear abstraction over the API."
```

---

## ✅ COMPLETION CHECKLIST

### Week 1 (Days 1-7) - Frontend

- [ ] Day 1: main.jsx, App.jsx, apiClient.js
- [ ] Day 2: AuthContext.jsx, PostsContext.jsx, FriendsContext.jsx
- [ ] Day 3: postsService.js, friendsService.js
- [ ] Day 4: Home.jsx, TimelineRiverFeed.jsx
- [ ] Day 5: TimelineRiverRow.jsx
- [ ] Day 6: Profile.jsx, TimelineRiver.jsx
- [ ] Day 7: ComposerModal.jsx, SearchContext.jsx

### Week 2 (Days 8-14) - Backend + Integration

- [ ] Day 8: numeneon/settings.py, numeneon/urls.py
- [ ] Day 9: posts/models.py
- [ ] Day 10: posts/serializers.py, posts/views.py
- [ ] Day 11: users/views.py, users/urls.py
- [ ] Day 12: friends/views.py, friends/models.py
- [ ] Day 13: Integration review
- [ ] Day 14: Flow practice

### Final Stretch (Days 15-20) - Interview Prep

- [ ] Days 15-17: Mock interview practice
- [ ] Days 18-20: Final review and graduation prep

---

## 🚨 IF YOU'RE RUNNING SHORT ON TIME

### Priority 1 (Absolute Must-Know - 10 files)

1. apiClient.js (how frontend talks to backend)
2. AuthContext.jsx (authentication state)
3. PostsContext.jsx (posts state management)
4. postsService.js (API calls)
5. Home.jsx (main UI)
6. TimelineRiverFeed.jsx (displaying posts)
7. numeneon/settings.py (Django config)
8. posts/models.py (database)
9. posts/views.py (API endpoints)
10. users/views.py (auth endpoints)

### Priority 2 (Important - 7 files)

11. App.jsx (routing)
12. main.jsx (app entry)
13. Profile.jsx (profile page)
14. TimelineRiverRow.jsx (post display)
15. ComposerModal.jsx (creating posts)
16. posts/serializers.py (JSON conversion)
17. FriendsContext.jsx (friends state)

### Priority 3 (Nice to Know - 5 files)

18. friendsService.js (same pattern as postsService)
19. SearchContext.jsx (simple UI state)
20. friends/views.py
21. friends/models.py
22. numeneon/urls.py

---

## 💪 YOU GOT THIS!

**Remember:**

- You BUILT this entire frontend
- You already KNOW the patterns
- This is just organizing knowledge you have
- Focus on explaining FLOWS, not memorizing code
- 22 files out of 100+ = totally doable!

**Graduation is January 24th. You've come so far. Finish strong! 🚀**
