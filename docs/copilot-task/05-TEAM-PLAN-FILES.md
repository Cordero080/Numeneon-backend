This file contains templates for creating the 6 team plan markdown files in the docs/team-plan/ folder.

markdown# NUMENEON TEAM REBUILD - Part 5: Team Plan Files

## HOW TO USE THESE FILES

**⚠️ READ [00-START-HERE.md](./00-START-HERE.md) FIRST if you haven't already!**

This is Part 5 of 5. Read these files in order:

0. `00-START-HERE.md` - Quick overview, workflow, FAQ
1. `01-CONTEXT-AND-STRATEGY.md` - Background, strategy, assignments
2. `02-PSEUDOCODE-EXAMPLES.md` - All 12 example templates
3. `03-BACKEND-INSTRUCTIONS.md` - Backend pseudocode tasks
4. `04-FRONTEND-INSTRUCTIONS.md` - Frontend pseudocode tasks
5. `05-TEAM-PLAN-FILES.md` ← YOU ARE HERE

---

## CREATE: `docs/team-plan/` FOLDER

Create a folder called `docs/team-plan/` with these 6 files:

1. `natalia.md`
2. `colin.md`
3. `crystal.md`
4. `pablo.md`
5. `tito.md`
6. `team-structure.md`

---

## FILE 1: `docs/team-plan/natalia.md`

````markdown
# Natalia's Tasks (Size: L)

## Your Mission

You're building the authentication system - the foundation that lets users create accounts, log in, and access protected features. Without auth, nobody can use NUMENEON! You're also the team's migration manager, keeping the database healthy as everyone builds their models.

## Files You Own

**Important:** Don't touch anyone else's files to avoid merge conflicts!

### Backend Files (11 total)

| File                                                    | Description                           |
| ------------------------------------------------------- | ------------------------------------- |
| `backend/users/models.py`                               | Profile model (extends Django User)   |
| `backend/users/views.py`                                | Signup, login, current user endpoints |
| `backend/users/serializers.py`                          | User data validation and formatting   |
| `backend/users/urls.py`                                 | Auth API route configuration          |
| `backend/users/apps.py`                                 | Django app config                     |
| `backend/users/__init__.py`                             | Package marker                        |
| `backend/users/management/__init__.py`                  | Management package                    |
| `backend/users/management/commands/__init__.py`         | Commands package                      |
| `backend/users/management/commands/create_test_user.py` | Test user script                      |
| `backend/users/migrations/__init__.py`                  | Migrations package                    |
| `backend/users/migrations/0001_initial.py`              | Initial migration (auto-generated)    |

### Frontend Files (8 total)

| File                                               | Description                              |
| -------------------------------------------------- | ---------------------------------------- |
| `frontend/src/contexts/AuthContext.jsx`            | Auth state (user, login, logout, signup) |
| `frontend/src/components/pages/Login/Login.jsx`    | Login form                               |
| `frontend/src/components/pages/Login/Login.scss`   | Login styling                            |
| `frontend/src/components/pages/Login/index.js`     | Export                                   |
| `frontend/src/components/pages/Signup/Signup.jsx`  | Registration form                        |
| `frontend/src/components/pages/Signup/Signup.scss` | Signup styling                           |
| `frontend/src/components/pages/Signup/index.js`    | Export                                   |
| `frontend/src/components/ui/ProtectedRoute.jsx`    | Route guard                              |

### Special Responsibility: Migration Manager

You review and run ALL database migrations for the team.

---

## Task Breakdown

### ✅ Task 1: Create Profile Model

**Files:** `backend/users/models.py`

**What:** Define database structure for user profiles extending Django's built-in User.

**Why:** Users need profile pictures and bios beyond basic auth info.

**Acceptance Criteria:**

- [ ] Profile model with OneToOneField to User
- [ ] avatar field (URLField, optional)
- [ ] bio field (TextField, optional)
- [ ] created_at timestamp
- [ ] Model visible in Django admin

**Think about:**

- When a User is created, should a Profile auto-create? (Signals)
- What happens if avatar is empty?

---

### ✅ Task 2: Build Auth API Views

**Files:** `backend/users/views.py`, `backend/users/serializers.py`

**What:** Create signup, login, and current user endpoints.

**Why:** Frontend needs to authenticate users and get their data.

**Acceptance Criteria:**

- [ ] POST /api/auth/signup/ creates user + profile, returns JWT
- [ ] POST /api/auth/login/ validates credentials, returns JWT
- [ ] GET /api/auth/me/ returns current user data (requires auth)
- [ ] Proper error responses (400, 401)
- [ ] Passwords never returned in responses

**Think about:**

- How do you generate JWT tokens? (rest_framework_simplejwt)
- What data should /me/ return? (User + nested Profile)

---

### ✅ Task 3: Configure Auth Routes

**Files:** `backend/users/urls.py`, `backend/numeneon/urls.py` (add your line)

**What:** Map URLs to your view functions.

**Why:** Frontend needs to know where to send requests.

**Acceptance Criteria:**

- [ ] /api/auth/signup/ route works
- [ ] /api/auth/login/ route works
- [ ] /api/auth/me/ route works
- [ ] /api/auth/token/refresh/ route works (from simplejwt)
- [ ] Routes included in main urls.py

---

### ✅ Task 4: Create AuthContext

**Files:** `frontend/src/contexts/AuthContext.jsx`

**What:** React context managing user auth state.

**Why:** Many components need to know if user is logged in.

**Acceptance Criteria:**

- [ ] Provides `user` state (object or null)
- [ ] Provides `loading` state
- [ ] Provides `error` state
- [ ] `login(credentials)` function works
- [ ] `signup(userData)` function works
- [ ] `logout()` clears token and user
- [ ] On mount, checks for existing token
- [ ] JWT stored in localStorage
- [ ] Custom `useAuth()` hook exported

**Think about:**

- What if token exists but is expired?
- When should loading be true?

---

### ✅ Task 5: Build Login & Signup Pages

**Files:** Login/, Signup/ folders (JSX, SCSS, index.js)

**What:** User-facing forms for authentication.

**Why:** Users need a way to sign in and create accounts.

**Acceptance Criteria:**

- [ ] Login form with username/password fields
- [ ] Signup form with username/email/password/confirm fields
- [ ] Forms call AuthContext functions on submit
- [ ] Redirect to /home on success
- [ ] Display errors clearly
- [ ] Uses Pablo's design system (glass-card, variables)
- [ ] Mobile responsive

**Think about:**

- How do you prevent page refresh on submit?
- What if passwords don't match on signup?

---

### ✅ Task 6: Create ProtectedRoute

**Files:** `frontend/src/components/ui/ProtectedRoute.jsx`

**What:** Component that redirects unauthenticated users.

**Why:** Some pages (Home, Profile) require login.

**Acceptance Criteria:**

- [ ] Checks AuthContext for user
- [ ] If loading, shows loading state
- [ ] If no user, redirects to /login
- [ ] If user exists, renders children

---

## Migration Manager Duties

### Your Workflow:

1. **Your migrations:** `python manage.py makemigrations users`
2. **Review Colin's:** Check `backend/posts/migrations/` files
3. **Review Crystal's:** Check `backend/friends/migrations/` files
4. **Run all:** `python manage.py migrate`

### When to Run:

- After any model changes (yours or teammates')
- Before testing/demos
- When someone reports database errors

### Helpful Commands:

```bash
python manage.py showmigrations      # See status
python manage.py makemigrations      # Create migrations
python manage.py migrate             # Apply migrations
python manage.py migrate --fake app 0001  # Mark as done without running
```

---

## Integration Points

**You Provide:**

- AuthContext → Used by everyone
- User model → Colin/Crystal reference via ForeignKey
- Login/Signup pages → App routing uses these
- ProtectedRoute → Wraps authenticated pages

**You Consume:**

- Pablo's design system → For Login/Signup styling
- Tito's apiClient.js → For making API calls

**Work Closely With:**

- **Tito:** apiClient must handle JWT tokens correctly
- **Colin & Crystal:** Their models have ForeignKey to User
- **Pablo:** Ensure auth UI matches design system
````

---

## FILE 2: `docs/team-plan/colin.md`

```markdown
# Colin's Tasks (Size: M)

## Your Mission

You're building the posts system - the core content that users create and view. Posts are what make NUMENEON a social app! Your backend serves the data, your context manages it, and you also build the modals for creating and deleting posts.

## Files You Own

### Backend Files (7 total)

| File                           | Description                               |
| ------------------------------ | ----------------------------------------- |
| `backend/posts/models.py`      | Post model (type, content, image, parent) |
| `backend/posts/views.py`       | Posts CRUD ViewSet                        |
| `backend/posts/serializers.py` | Post data formatting                      |
| `backend/posts/urls.py`        | Posts API routes                          |
| `backend/posts/apps.py`        | Django app config                         |
| `backend/posts/__init__.py`    | Package marker                            |
| `backend/posts/admin.py`       | Admin registration                        |

### Frontend Files (8 total)

| File                                                                                       | Description            |
| ------------------------------------------------------------------------------------------ | ---------------------- |
| `frontend/src/contexts/PostsContext.jsx`                                                   | Posts state management |
| `frontend/src/services/postsService.js`                                                    | Posts API calls        |
| `frontend/src/components/pages/Home/components/ComposerModal/ComposerModal.jsx`            | Create post form       |
| `frontend/src/components/pages/Home/components/ComposerModal/ComposerModal.scss`           | Composer styling       |
| `frontend/src/components/pages/Home/components/ComposerModal/index.js`                     | Export                 |
| `frontend/src/components/pages/Home/components/DeleteConfirmModal/DeleteConfirmModal.jsx`  | Delete confirmation    |
| `frontend/src/components/pages/Home/components/DeleteConfirmModal/DeleteConfirmModal.scss` | Delete modal styling   |
| `frontend/src/components/pages/Home/components/DeleteConfirmModal/index.js`                | Export                 |

---

## Task Breakdown

### ✅ Task 1: Create Post Model

**Files:** `backend/posts/models.py`

**What:** Define database structure for posts.

**Why:** Posts are the main content - thoughts, media, milestones.

**Acceptance Criteria:**

- [ ] author field (ForeignKey to User)
- [ ] type field (choices: 'thoughts', 'media', 'milestones')
- [ ] content field (TextField, can be blank)
- [ ] media_url field (URLField, optional) - NOT ImageField!
- [ ] parent field (ForeignKey to self, for replies)
- [ ] created_at timestamp (auto)
- [ ] likes_count field (PositiveIntegerField, default=0)
- [ ] reply_count field (PositiveIntegerField, default=0) - NOT comment_count!
- [ ] shares_count field (PositiveIntegerField, default=0)
- [ ] Ordered by newest first
- [ ] Like model with user, post ForeignKeys and unique_together constraint

**IMPORTANT:** Engagement fields are REQUIRED for Pablo's ProfileCard analytics!
The wave chart and heatmap use these metrics to visualize user activity.
Toggle buttons are mobile-responsive (breakpoints: 600px, 480px, 375px).

**RIVER TIMELINE "SPACE ECONOMY":**

- Posts grouped BY USER (not by date!) in groupPosts.js
- Each user = ONE row with carousel navigation
- Need 3+ posts per type per user for carousel arrows
- seed_posts.py creates 9 posts/user (3 per type) for testing

**Like Model Requirements:**

- user: ForeignKey to User (who liked)
- post: ForeignKey to Post (which post)
- created_at: DateTimeField (auto_now_add)
- unique_together: ('user', 'post') - prevents duplicate likes

**Think about:**

- What happens when a user is deleted? (CASCADE)
- What happens when parent post is deleted?

---

### ✅ Task 2: Build Posts ViewSet

**Files:** `backend/posts/views.py`, `backend/posts/serializers.py`

**What:** Create full CRUD API for posts.

**Why:** Frontend needs to create, read, update, delete posts.

**Acceptance Criteria:**

- [ ] GET /api/posts/ lists all posts
- [ ] POST /api/posts/ creates post (authenticated)
- [ ] GET /api/posts/:id/ gets single post
- [ ] PATCH /api/posts/:id/ updates post (author only)
- [ ] DELETE /api/posts/:id/ deletes post (author only)
- [ ] GET /api/posts/:id/replies/ gets replies
- [ ] POST /api/posts/:id/like/ toggles like (creates/deletes Like, updates likes_count)
- [ ] POST /api/posts/:id/share/ increments shares_count
- [ ] Author auto-set from request.user
- [ ] Nested author data in response (id, username, first_name, last_name)
- [ ] Include engagement fields in response (likes_count, reply_count, shares_count)
- [ ] Include `is_liked` boolean in response (has current user liked this post?)

**Think about:**

- How do you auto-set author? (perform_create)
- How do you restrict edit/delete to author only?

---

### ✅ Task 3: Configure Posts Routes

**Files:** `backend/posts/urls.py`, `backend/numeneon/urls.py` (add your line)

**What:** Set up URL routing with DRF router.

**Why:** Router auto-generates CRUD URLs from ViewSet.

**Acceptance Criteria:**

- [ ] Router registered with PostViewSet
- [ ] Routes included in main urls.py at /api/posts/

---

### ✅ Task 4: Create PostsContext

**Files:** `frontend/src/contexts/PostsContext.jsx`

**What:** React context managing posts state.

**Why:** Multiple components need access to posts data.

**Acceptance Criteria:**

- [ ] `posts` state (array)
- [ ] `isLoading` state
- [ ] `error` state
- [ ] `fetchPosts()` gets all posts
- [ ] `fetchPostsByUsername(username)` gets posts by a specific user
- [ ] `createPost(data)` creates and adds to state
- [ ] `updatePost(id, data)` updates in state
- [ ] `deletePost(id)` removes from state
- [ ] `fetchReplies(postId)` gets replies for a post
- [ ] `createReply(parentId, content)` creates reply, increments parent's reply_count
- [ ] `likePost(id)` toggles like, updates post in state
- [ ] `sharePost(id)` increments share count, updates post in state
- [ ] Custom `usePosts()` hook exported
- [ ] Posts sorted newest first
- [ ] Wait for AuthContext to finish loading before fetching
- [ ] Post objects include engagement fields (likes_count, reply_count, shares_count)
- [ ] Post objects include `is_liked` boolean for current user

**NOTE:** Pablo's ProfileCard.jsx consumes posts for analytics visualizations.
Posts must include engagement fields for the wave chart and heatmap to work!

**RIVER TIMELINE NOTE:** groupPosts.js groups BY USER (not date!).
Each user = ONE row with carousel navigation between posts.

**Think about:**

- Fetch on mount or let components trigger?
- After create, refetch all or just add to array?

---

### ✅ Task 5: Create Posts Service

**Files:** `frontend/src/services/postsService.js`

**What:** Functions that make API calls for posts.

**Why:** Separates API logic from state management.

**Acceptance Criteria:**

- [ ] `getPosts()` fetches all
- [ ] `getPost(id)` fetches one
- [ ] `createPost(data)` creates new
- [ ] `updatePost(id, data)` updates
- [ ] `deletePost(id)` deletes
- [ ] `getReplies(postId)` fetches replies
- [ ] `likePost(id)` toggles like, returns updated post
- [ ] `sharePost(id)` increments share count, returns updated post
- [ ] Uses Tito's apiClient
- [ ] Handles FormData for image uploads

---

## Integration Points

**You Provide:**

- PostsContext → Pablo's Home, Profile, ComposerModal use it
- Posts API → Returns data Pablo's UI expects
- Post format with nested author data

**You Consume:**

- Natalia's User model → ForeignKey reference
- Tito's apiClient → For HTTP requests

**Work Closely With:**

- **Pablo:** Ensure post data format matches his components
- **Natalia:** Your Post.author references her User model
```

---

## FILE 3: `docs/team-plan/crystal.md`

```markdown
# Crystal's Tasks (Size: M)

## Your Mission

You're building the friends system - the social connections between users. Friend requests, accepting/declining, viewing friends list. This makes NUMENEON truly social!

## Files You Own

### Backend Files (7 total)

| File                             | Description                       |
| -------------------------------- | --------------------------------- |
| `backend/friends/models.py`      | Friendship + FriendRequest models |
| `backend/friends/views.py`       | Friends API views                 |
| `backend/friends/serializers.py` | Friends data formatting           |
| `backend/friends/urls.py`        | Friends API routes                |
| `backend/friends/apps.py`        | Django app config                 |
| `backend/friends/__init__.py`    | Package marker                    |
| `backend/friends/admin.py`       | Admin registration                |

### Frontend Files (5 total)

| File                                                 | Description              |
| ---------------------------------------------------- | ------------------------ |
| `frontend/src/contexts/FriendsContext.jsx`           | Friends state management |
| `frontend/src/services/friendsService.js`            | Friends API calls        |
| `frontend/src/components/pages/Friends/Friends.jsx`  | Friends page UI          |
| `frontend/src/components/pages/Friends/Friends.scss` | Friends styling          |
| `frontend/src/components/pages/Friends/index.js`     | Export                   |

---

## Task Breakdown

### ✅ Task 1: Create Friends Models

**Files:** `backend/friends/models.py`

**What:** Define Friendship and FriendRequest database structures.

**Why:** Need to track who is friends with whom, and pending requests.

**Acceptance Criteria:**

- [ ] Friendship model with user, friend fields (DIRECTIONAL, not symmetric!)
- [ ] FriendRequest model with from_user, to_user (NO status field!)
- [ ] created_at timestamps
- [ ] Prevent duplicate friendships (unique_together)
- [ ] Prevent self-friendship (validate in view)

**IMPORTANT: Different from typical symmetric pattern!**

- When accepting a request, create TWO Friendship records (both directions)
- When removing, delete BOTH Friendship records
- FriendRequest has NO status field - just delete when accepted/declined

**Think about:**

- How do you query "all friends of user X"? (Friendship.objects.filter(user=X))
- When accepting: create Friendship(user=to_user, friend=from_user) AND Friendship(user=from_user, friend=to_user)
- When declining: just delete the FriendRequest

---

### ✅ Task 2: Build Friends Views

**Files:** `backend/friends/views.py`, `backend/friends/serializers.py`

**What:** Create API endpoints for friend operations.

**Why:** Frontend needs to manage friendships.

**Acceptance Criteria:**

- [ ] GET /api/friends/ lists current user's friends
- [ ] GET /api/friends/requests/ lists pending requests
- [ ] POST /api/friends/request/:user_id/ sends request
- [ ] POST /api/friends/accept/:request_id/ accepts (creates TWO friendships, deletes request)
- [ ] POST /api/friends/decline/:request_id/ declines (deletes request)
- [ ] DELETE /api/friends/remove/:user_id/ unfriends (deletes BOTH directions)
- [ ] All require authentication
- [ ] Proper error handling
- [ ] Returns simple user dicts (id, username, first_name, last_name)

**Think about:**

- What if already friends? (Error)
- What if request already sent? (Error)
- When accepting, create BOTH Friendship directions and DELETE request

---

### ✅ Task 3: Configure Friends Routes

**Files:** `backend/friends/urls.py`, `backend/numeneon/urls.py` (add your line)

**What:** Map URLs to view functions.

**Acceptance Criteria:**

- [ ] All friend endpoints routed
- [ ] Routes included in main urls.py at /api/friends/

---

### ✅ Task 4: Create FriendsContext

**Files:** `frontend/src/contexts/FriendsContext.jsx`

**What:** React context managing friends state.

**Acceptance Criteria:**

- [ ] `friends` state (array of users)
- [ ] `requests` state (array of requests)
- [ ] `isLoading` and `error` states
- [ ] `fetchFriends()` gets both friends AND pending requests in parallel
- [ ] `sendRequest(userId)`
- [ ] `acceptRequest(requestId)`
- [ ] `declineRequest(requestId)`
- [ ] `removeFriend(userId)`
- [ ] Custom `useFriends()` hook
- [ ] Wait for AuthContext to finish loading before fetching
- [ ] Clear data when logged out

**Note:** Variable names are `friends` and `pendingRequests` (not just `requests`)

---

### ✅ Task 5: Create Friends Service

**Files:** `frontend/src/services/friendsService.js`

**What:** Functions for friends API calls.

**Acceptance Criteria:**

- [ ] `getAll()` - GET /api/friends/
- [ ] `getPendingRequests()` - GET /api/friends/requests/
- [ ] `sendRequest(userId)` - POST /api/friends/request/:userId/
- [ ] `acceptRequest(requestId)` - POST /api/friends/accept/:requestId/
- [ ] `declineRequest(requestId)` - POST /api/friends/decline/:requestId/
- [ ] `remove(userId)` - DELETE /api/friends/remove/:userId/
- [ ] Export as default object (not named exports)
- [ ] Uses Tito's apiClient

---

### ✅ Task 6: Build Friends Page

**Files:** `Friends.jsx`, `Friends.scss`, `index.js`

**What:** UI for viewing friends and handling requests.

**Why:** Users need to see and manage their friendships.

**Acceptance Criteria:**

- [ ] Shows list of friends
- [ ] Shows pending requests with accept/decline buttons
- [ ] Remove friend button (with confirmation)
- [ ] Empty states for no friends/no requests
- [ ] Uses Pablo's design system
- [ ] Mobile responsive

---

## Integration Points

**You Provide:**

- FriendsContext → Friends.jsx consumes it
- Friends API → Manages social connections
- Friends page → Part of app navigation

**You Consume:**

- Natalia's User model → ForeignKey references
- Tito's apiClient → For HTTP requests
- Pablo's design system → For styling

**Work Closely With:**

- **Natalia:** Your models reference User
- **Pablo:** Ensure Friends page matches design system
```

---

## FILE 4: `docs/team-plan/pablo.md`

````markdown
# Pablo's Tasks (Size: XL)

## Your Mission

You're rebuilding the most complex UI components in NUMENEON - the Timeline River system with carousel navigation, the 3D flip ProfileCard with analytics charts, and the MediaLightbox. These require sophisticated state management, animations, and data visualization.

## Files You Own (29+ total)

### Timeline System (Refactored Jan 2025 - Modular Architecture)

| File                                                                                      | Description                                           |
| ----------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| `frontend/src/components/pages/Home/Home.jsx`                                             | Home page wrapper                                     |
| `frontend/src/components/pages/Home/Home.scss`                                            | Home styling                                          |
| `frontend/src/components/pages/Home/index.js`                                             | Export                                                |
| `frontend/src/components/pages/Home/utils/groupPosts.js`                                  | Post grouping algorithm                               |
| `frontend/src/components/pages/Home/utils/timeFormatters.js`                              | **NEW** Relative time formatting                      |
| `frontend/src/components/pages/Home/components/TimelineRiverFeed/TimelineRiverFeed.jsx`   | Main feed container                                   |
| `frontend/src/components/pages/Home/components/TimelineRiverFeed/TimelineRiverFeed.scss`  | Feed styling                                          |
| `frontend/src/components/pages/Home/components/TimelineRiverFeed/index.js`                | Export                                                |
| `frontend/src/components/pages/Home/components/TimelineRiverRow/TimelineRiverRow.jsx`     | Main orchestrator (uses sub-components)               |
| `frontend/src/components/pages/Home/components/TimelineRiverRow/TimelineRiverRow.scss`    | Row styling                                           |
| `frontend/src/components/pages/Home/components/TimelineRiverRow/index.js`                 | Export                                                |
| `frontend/src/components/pages/Home/components/TimelineRiverRow/styles/*.scss`            | SCSS partials                                         |
| `frontend/src/components/pages/Home/components/TimelineRiverRow/components/index.js`      | **NEW** Barrel export for sub-components              |
| `frontend/src/components/pages/Home/components/TimelineRiverRow/components/PostCard/`     | **NEW** Individual post card rendering                |
| `frontend/src/components/pages/Home/components/TimelineRiverRow/components/SmartDeck/`    | **NEW** Carousel deck with navigation                 |
| `frontend/src/components/pages/Home/components/TimelineRiverRow/components/ThreadView/`   | **NEW** Inline replies thread display                 |
| `frontend/src/components/pages/Home/components/TimelineRiverRow/components/MobileTabNav/` | **NEW** Mobile category tab navigation                |
| `frontend/src/components/pages/Home/components/TimelineRiverRow/components/RepostModal/`  | **NEW (Jan 2026)** Share modal with repost/copy icons |
| `frontend/src/components/pages/Home/components/MediaLightbox/MediaLightbox.jsx`           | Image viewer modal                                    |
| `frontend/src/components/pages/Home/components/MediaLightbox/MediaLightbox.scss`          | Lightbox styling                                      |
| `frontend/src/components/pages/Home/components/MediaLightbox/index.js`                    | Export                                                |
| `frontend/src/components/pages/Home/components/MediaLightbox/styles/*.scss`               | 7 SCSS partials                                       |

### Profile Card System (12 files)

| File                                                                                              | Description                |
| ------------------------------------------------------------------------------------------------- | -------------------------- |
| `frontend/src/components/pages/Profile/components/ProfileCard/ProfileCard.jsx`                    | Card container with flip   |
| `frontend/src/components/pages/Profile/components/ProfileCard/ProfileCard.scss`                   | Card styling               |
| `frontend/src/components/pages/Profile/components/ProfileCard/index.js`                           | Export                     |
| `frontend/src/components/pages/Profile/components/ProfileCard/components/ProfileCardFront.jsx`    | Front face (avatar, stats) |
| `frontend/src/components/pages/Profile/components/ProfileCard/components/ProfileCardBack.jsx`     | Back face (analytics)      |
| `frontend/src/components/pages/Profile/components/ProfileCard/components/ActivityVisualization/*` | Wave chart, heatmap        |

---

## Task Breakdown

### ✅ Task 1: Build groupPosts Algorithm

**File:** `utils/groupPosts.js`

**What:** Groups posts by USER (not date) for "space economy" layout.

**Why:** Each user = ONE row with all their posts, enabling carousel navigation.

**Acceptance Criteria:**

- [ ] Input: Array of posts from PostsContext
- [ ] Output: Object keyed by userId
- [ ] Each user entry has: thoughts[], media[], milestones[]
- [ ] Each entry has mostRecentDate for "Last active" display
- [ ] Posts within each type sorted by date (newest first)

**Algorithm:**

```javascript
// Input: [{ id, author: { id, username }, type, created_at, ... }, ...]
// Output: {
//   "userId": {
//     user: { id, name, avatar },
//     thoughts: [posts...],
//     media: [posts...],
//     milestones: [posts...],
//     mostRecentDate: Date
//   }
// }
```

---

### ✅ Task 2: Build TimelineRiverFeed

**Files:** TimelineRiverFeed.jsx, .scss, index.js

**What:** Container that fetches posts and renders rows.

**Why:** Main feed component on Home page.

**Acceptance Criteria:**

- [ ] Consumes PostsContext via usePosts()
- [ ] Calls fetchPosts() on mount
- [ ] Passes posts through groupPosts()
- [ ] Renders TimelineRiverRow for each user
- [ ] Shows loading state while fetching
- [ ] Shows empty state when no posts

---

### ✅ Task 3: Build TimelineRiverRow (MODULAR ARCHITECTURE - Refactored Jan 2025)

**Files:** TimelineRiverRow.jsx + sub-components + SCSS

**What:** Single row showing one user's posts across 3 columns with carousel.

**Why:** Core timeline interaction - refactored into modular sub-components for maintainability.

**Architecture (Jan 2025 Refactor):**

The original monolithic TimelineRiverRow.jsx has been split into focused sub-components:

```
TimelineRiverRow/
├── TimelineRiverRow.jsx      # Main orchestrator
├── TimelineRiverRow.scss
├── styles/                   # 11 SCSS partials
└── components/
    ├── index.js              # Barrel export
    ├── PostCard/             # Individual post with all actions
    │   ├── PostCard.jsx
    │   └── PostCard.scss
    ├── SmartDeck/            # Carousel deck with navigation
    │   ├── SmartDeck.jsx
    │   └── SmartDeck.scss
    ├── ThreadView/           # Inline replies thread
    │   ├── ThreadView.jsx
    │   └── ThreadView.scss
    ├── MobileTabNav/         # Mobile category tabs
    │   ├── MobileTabNav.jsx
    │   └── MobileTabNav.scss
    └── RepostModal/          # Share modal (Jan 2026)
        ├── RepostModal.jsx
        └── RepostModal.scss
```

**State (in TimelineRiverRow.jsx - passed to sub-components):**

- [ ] `deckIndex` - { thoughts: 0, media: 0, milestones: 0 } for carousel
- [ ] `expandedThreadId` - which post's replies are showing
- [ ] `threadReplies` - cached replies per post
- [ ] `editingPostId` - which post is being edited
- [ ] `deleteModalPostId` - which post has delete modal open
- [ ] `isMobile` - responsive breakpoint detection
- [ ] `mobileActiveTab` - which column showing on mobile

**Sub-Component Responsibilities:**

- **PostCard.jsx**: Renders a single post card with all action buttons (like, share, comment, edit, delete), media display, VisibilityIcon (smart component)
- **SmartDeck.jsx**: Carousel container with prev/next navigation when 3+ posts, shows current index
- **ThreadView.jsx**: Twitter-style inline replies thread, fetches and displays replies
- **MobileTabNav.jsx**: Tab buttons for switching between thoughts/media/milestones on mobile

**Utility Files:**

- `utils/timeFormatters.js` - `formatRelativeTime()` extracted for reuse
- `utils/groupPosts.js` - Groups posts by user (uses `orderId` not `oderId` - typo fixed Jan 2025)

**Icons Used (import from icons.jsx):**

- UserIcon, HeartIcon, HeartFilledIcon, CommentIcon, ShareIcon
- EditIcon, TrashIcon, ExpandIcon, VisibilityIcon (smart - replaces GlobeIcon/LockIcon/FriendsIcon inline logic)
- ChevronLeftIcon, ChevronRightIcon

---

### ✅ Task 4: Build ProfileCard with 3D Flip

**Files:** ProfileCard.jsx, ProfileCardFront.jsx, ProfileCardBack.jsx

**What:** User profile card that flips between front (info) and back (analytics).

**Why:** Signature UI feature - shows user stats and activity visualization.

**Acceptance Criteria:**

- [ ] `isFlipped` state controls rotation
- [ ] CSS 3D transform: `rotateY(180deg)` on flip
- [ ] Front: Avatar, username, bio, follower stats
- [ ] Back: Analytics charts (wave, heatmap, donut)
- [ ] Flip button triggers animation
- [ ] `isOwnProfile` prop controls what's shown

---

### ✅ Task 5: Build Analytics Visualizations

**Files:** ActivityVisualization component

**What:** Wave chart and heatmap showing engagement over time.

**Why:** Visual representation of user activity.

**Wave Chart:**

- [ ] SVG path showing weekly engagement totals
- [ ] X-axis: 52 weeks
- [ ] Y-axis: Normalized engagement (likes + replies + shares)
- [ ] Animated draw-on effect

**Heatmap:**

- [ ] 52x7 grid (weeks × days)
- [ ] Color intensity based on post count
- [ ] Levels: 0 (empty), 1 (low), 2 (medium), 3 (high)
- [ ] Hover shows date and count

**Post Type Donut:**

- [ ] SVG donut chart
- [ ] Segments: Thoughts (green), Media (blue), Milestones (magenta)
- [ ] Percentages calculated from user's posts

---

### ✅ Task 6: Build MediaLightbox

**Files:** MediaLightbox.jsx, .scss, index.js

**What:** Full-screen modal for viewing images.

**Why:** Allows expanding media posts.

**Acceptance Criteria:**

- [ ] Opens via portal (createPortal)
- [ ] Shows image full-size
- [ ] Close on backdrop click or X button
- [ ] Close on Escape key
- [ ] Smooth fade-in animation

---

## Integration Points

**You Consume:**

- PostsContext (Colin) → posts array, likePost(), sharePost(), deletePost()
- AuthContext (Natalia) → current user for edit/delete permissions
- FriendsContext (Crystal) → for friend status checks
- Icons from `assets/icons.jsx` → all SVG icons

**You Provide:**

- Complete Timeline UI → displays posts from Colin's context
- ProfileCard analytics → visualizes engagement data
- MediaLightbox → image viewing experience

**Work Closely With:**

- **Colin:** Post data format must match your expectations
- **Natalia:** User data format for profile display
- **Tito:** Import icons from shared icons.jsx
````

---

## FILE 5: `docs/team-plan/tito.md`

```markdown
# Tito's Tasks (Size: S)

## Your Mission

You're building the infrastructure layer - the foundation that everyone else depends on. The API client that handles authentication, the theme system, and the app's entry point. Small file count, but critical importance!

## Files You Own (6 total)

| File                                                      | Description             |
| --------------------------------------------------------- | ----------------------- |
| `frontend/src/main.jsx`                                   | React app entry point   |
| `frontend/src/services/apiClient.js`                      | Axios with JWT handling |
| `frontend/src/contexts/ThemeContext.jsx`                  | Light/dark theme state  |
| `frontend/src/components/ui/ThemeToggle/ThemeToggle.jsx`  | Theme switch button     |
| `frontend/src/components/ui/ThemeToggle/ThemeToggle.scss` | Button styling          |
| `frontend/src/components/ui/ThemeToggle/index.js`         | Export                  |

---

## Task Breakdown

### ✅ Task 1: Create API Client

**Files:** `frontend/src/services/apiClient.js`

**What:** Axios instance with JWT authentication handling.

**Why:** EVERY API call goes through this. Critical foundation.

**Acceptance Criteria:**

- [ ] Base URL: http://localhost:8000/api
- [ ] Request interceptor adds Authorization header
- [ ] Gets token from localStorage
- [ ] Response interceptor handles 401 errors
- [ ] Clears token on 401 (expired)
- [ ] Exports configured axios instance

**Think about:**

- What if no token exists? (Don't add header)
- What if token is expired? (401 response)

---

### ✅ Task 2: Create ThemeContext

**Files:** `frontend/src/contexts/ThemeContext.jsx`

**What:** Manages light/dark theme state.

**Why:** NUMENEON supports both themes.

**Acceptance Criteria:**

- [ ] `theme` state ('light' | 'dark')
- [ ] `toggleTheme()` function
- [ ] Persists to localStorage
- [ ] Applies class to document.body
- [ ] Loads saved preference on mount
- [ ] Custom `useTheme()` hook

**How theming works:**

- Dark mode: default (no class)
- Light mode: add 'light-mode' class to body
- Pablo's CSS handles the rest

---

### ✅ Task 3: Create ThemeToggle

**Files:** `ThemeToggle.jsx`, `ThemeToggle.scss`, `index.js`

**What:** Button to switch themes.

**Acceptance Criteria:**

- [ ] Shows current theme icon (sun/moon)
- [ ] Calls toggleTheme() on click
- [ ] Accessible (proper button, aria-label)
- [ ] Styled with Pablo's design system

---

### ✅ Task 4: Set Up main.jsx

**Files:** `frontend/src/main.jsx`

**What:** App entry point with provider nesting.

**Acceptance Criteria:**

- [ ] Imports React, ReactDOM
- [ ] Imports global styles
- [ ] Wraps App with BrowserRouter
- [ ] Nests all context providers
- [ ] Mounts to #root

**Provider Order (outer to inner):**

1. BrowserRouter
2. ThemeProvider
3. AuthProvider
4. PostsProvider
5. FriendsProvider
6. MessageProvider
7. App

---

## Integration Points

**You Provide:**

- apiClient → Used by ALL services (posts, friends, auth)
- ThemeContext → Used by ThemeToggle, affects entire app
- main.jsx → Bootstraps everything

**You Consume:**

- Pablo's design system → For ThemeToggle styling
- All contexts → You wire them together in main.jsx

**Work Closely With:**

- **Natalia:** Her AuthContext depends on apiClient for API calls
- **Colin:** His postsService depends on apiClient
- **Crystal:** Her friendsService depends on apiClient
- **Everyone:** You're the glue that connects everything
```

---

## FILE 6: `docs/team-plan/team-structure.md`

```markdown
# NUMENEON Project Structure & Ownership

## Team Overview

| Person  | Size | Focus Area                  |
| ------- | ---- | --------------------------- |
| Pablo   | XL   | UI Architecture (pre-built) |
| Natalia | L    | Auth + Migration Management |
| Colin   | M    | Posts System                |
| Crystal | M    | Friends System              |
| Tito    | S    | Infrastructure              |

---

## File Ownership Map

### Backend
```

backend/
├── manage.py [SHARED]
├── seed_posts.py [SHARED]
│
├── numeneon/ [SHARED CONFIG]
│ ├── settings.py (pre-configured)
│ ├── urls.py [COLLABORATIVE]
│ └── ...
│
├── users/ [NATALIA]
│ ├── models.py ← Build this
│ ├── views.py ← Build this
│ ├── serializers.py ← Build this
│ ├── urls.py ← Build this
│ └── migrations/ ← Manage all team migrations
│
├── posts/ [COLIN]
│ ├── models.py ← Build this
│ ├── views.py ← Build this
│ ├── serializers.py ← Build this
│ ├── urls.py ← Build this
│ └── ...
│
└── friends/ [CRYSTAL]
├── models.py ← Build this
├── views.py ← Build this
├── serializers.py ← Build this
├── urls.py ← Build this
└── ...

```

### Frontend
```

frontend/src/
├── main.jsx [TITO]
├── App.jsx [PABLO - intact]
│
├── contexts/
│ ├── index.js [COLLABORATIVE]
│ ├── AuthContext.jsx [NATALIA]
│ ├── PostsContext.jsx [COLIN]
│ ├── FriendsContext.jsx [CRYSTAL]
│ ├── ThemeContext.jsx [TITO]
│ └── MessageContext.jsx [PABLO - intact]
│
├── services/
│ ├── apiClient.js [TITO]
│ ├── postsService.js [COLIN]
│ └── friendsService.js [CRYSTAL]
│
├── components/
│ ├── layout/ [PABLO - intact]
│ ├── pages/
│ │ ├── Home/ [PABLO - intact]
│ │ ├── Profile/ [PABLO - intact]
│ │ ├── Login/ [NATALIA]
│ │ ├── Signup/ [NATALIA]
│ │ ├── Friends/ [CRYSTAL]
│ │ ├── About/ [PABLO - intact]
│ │ ├── Landing/ [PABLO - intact]
│ │ └── NotFound/ [PABLO - intact]
│ └── ui/
│ ├── ProtectedRoute.jsx [NATALIA]
│ └── ThemeToggle/ [TITO]
│
└── styles/ [PABLO - DO NOT TOUCH]
└── (13 files)

```

---

## Data Flow Diagrams

### Posts Flow
```

Django Post Model [Colin]
↓
Post API ViewSet [Colin]
↓
postsService.js [Colin]
↓
PostsContext [Colin]
↓
usePosts() hook
↓
TimelineRiverFeed [Pablo]

```

### Auth Flow
```

Django User Model [Natalia]
↓
Auth API Views [Natalia]
↓
apiClient.js [Tito]
↓
AuthContext [Natalia]
↓
useAuth() hook
↓
Login/Signup/TopBar [Natalia/Pablo]

```

### Friends Flow
```

Django Friendship Model [Crystal]
↓
Friends API Views [Crystal]
↓
friendsService.js [Crystal]
↓
FriendsContext [Crystal]
↓
useFriends() hook
↓
Friends.jsx [Crystal]

```

---

## File Counts (UPDATED Dec 2024)

| Person | Backend | Frontend | Total | Notes |
|--------|---------|----------|-------|-------|
| Pablo (XL) | 0 | 29 | **29** | Timeline, ProfileCard, MediaLightbox |
| Natalia (L) | 11 | 8 | **19** | Auth system + migrations |
| Colin (M) | 7 | 8 | **15** | Posts + ComposerModal + DeleteConfirmModal |
| Crystal (M) | 7 | 5 | **12** | Friends system |
| Tito (S) | 0 | 6 | **6** | Infrastructure |
| Shared | ~10 | ~17 | ~27 | Config, styles (DO NOT TOUCH) |

```

XL Pablo: █████████████████████████████ 29 files
L Natalia: ███████████████████ 19 files
M Colin: ███████████████ 15 files
M Crystal: ████████████ 12 files
S Tito: ██████ 6 files

````

---

## Critical Rules

1. **NO TWO PEOPLE work on the same file** - prevents merge conflicts
2. **Everyone rebuilds from pseudocode** - git history shows contribution
3. **Styles (SCSS) are provided** - team focuses on JSX logic
4. **SVG icons in shared icons.jsx** - team imports, not inline
5. **Global styles untouchable** - everyone uses, nobody modifies
6. **Collaborative files** - each person adds exactly ONE thing

---

## API Response Formats

### Post Object (REQUIRED FORMAT - includes engagement metrics + is_liked)

```json
{
  "id": 1,
  "author": {
    "id": 5,
    "username": "alice",
    "first_name": "Alice",
    "last_name": "Smith"
  },
  "type": "thoughts",
  "content": "Hello NUMENEON!",
  "media_url": null,
  "parent": null,
  "parent_id": null,
  "created_at": "2024-12-19T10:30:00Z",
  "likes_count": 42,
  "reply_count": 7,
  "shares_count": 3,
  "is_liked": false
}
````

**⚠️ CRITICAL:** Engagement fields + is_liked are REQUIRED:

- `likes_count`, `reply_count`, `shares_count` → Used by wave chart
- `created_at` → Used by heatmap calendar
- `type` → Used by post type breakdown donut chart
- `is_liked` → Heart icon state (filled/empty) in TimelineRiverRow

**RIVER TIMELINE "SPACE ECONOMY":**

- groupPosts.js groups posts BY USER (not by date!)
- Each user = ONE row with carousel navigation
- Need 3+ posts per type per user for carousel arrows
- seed_posts.py creates 9 posts/user (3 per type)

### User Object

```json
{
  "id": 1,
  "username": "alice",
  "email": "alice@example.com",
  "first_name": "Alice",
  "last_name": "Smith",
  "date_joined": "2024-12-01T...",
  "profile": {
    "id": 1,
    "bio": "Cyberpunk enthusiast",
    "avatar": null,
    "location": "",
    "website": ""
  }
}
```

### Friend Object (in list)

```json
{
  "id": 2,
  "username": "bob",
  "first_name": "Bob",
  "last_name": "Jones"
}
```

### Friend Request Object

```json
{
  "id": 1,
  "from_user": {
    "id": 3,
    "username": "charlie",
    "first_name": "Charlie",
    "last_name": "Brown"
  },
  "created_at": "2024-12-19T09:00:00Z"
}
```

---

## SUMMARY: FILES TO CREATE

Create `docs/team-plan/` folder with:

1. `natalia.md` - Auth system tasks
2. `colin.md` - Posts system tasks
3. `crystal.md` - Friends system tasks
4. `pablo.md` - Integration support tasks
5. `tito.md` - Infrastructure tasks
6. `team-structure.md` - Full ownership map

---

## FINAL CHECKLIST

After creating all 5 instruction files and 6 team plan files:

**For Copilot to execute:**

### On `team-shell-backend` branch:

- [ ] Delete `frontend/` folder
- [ ] Add pseudocode to all Natalia backend files (11)
- [ ] Add pseudocode to all Colin backend files (7)
- [ ] Add pseudocode to all Crystal backend files (7)
- [ ] Add TODO comments to collaborative urls.py

### On `team-shell-frontend` branch:

- [ ] Delete `backend/` folder
- [ ] Add pseudocode to Natalia frontend files (8)
- [ ] Add pseudocode to Colin frontend files (2)
- [ ] Add pseudocode to Crystal frontend files (5)
- [ ] Add pseudocode to Tito frontend files (6)
- [ ] Add TODO comments to collaborative contexts/index.js
- [ ] Add USAGE comments to Pablo's ~40 JSX files

### In project root (both branches):

- [ ] Create `docs/team-plan/` folder with 6 markdown files

---

**END OF TEAM REBUILD DOCUMENTATION**

That's all 5 files! Here's the summary:
FileNameContent101-CONTEXT-AND-STRATEGY.mdBackground, strategy, assignments, pseudocode guidelines202-PSEUDOCODE-EXAMPLES.mdAll 11 example templates303-BACKEND-INSTRUCTIONS.mdFull pseudocode for all backend Python files404-FRONTEND-INSTRUCTIONS.mdFull pseudocode for frontend + usage comment instructions505-TEAM-PLAN-FILES.mdTemplates for all 6 team-plan markdown files

```

```
