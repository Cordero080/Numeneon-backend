# NUMENEON Team Structure & Workflow

## Project Overview

**NUMENEON** (formerly HUDDL) is a cyberpunk-themed social media application with a React frontend and Django backend. Pablo built a complete working prototype. Now the 5-person bootcamp team will **rebuild it from pseudocode shells** to learn architecture and create legitimate git history.

**Why rebuild from pseudocode?**

- **Git history matters** - everyone needs PR records showing their contributions
- **Learning value** - team learns architecture, state management, and full-stack patterns
- **Realistic scope** - SCSS styles are provided, team writes JSX/Python logic only
- **No overlap** - each person owns distinct files (zero merge conflicts)
- **AI-assisted** - Pseudocode is detailed enough for AI to help generate accurate code

**CRITICAL:** Everyone rebuilds from pseudocode (including Pablo). This ensures legitimate git history for all team members.

---

## Tech Stack

### Frontend

- **Framework:** React 18+ with Vite 7.2+
- **Routing:** React Router DOM
- **Styling:** Vanilla CSS/SCSS with modular architecture
- **State:** React Context API
- **HTTP Client:** Axios
- **Build:** Vite with path aliases (@assets, @components, @contexts, etc.)
- **Design:** Cyberpunk theme with light/dark mode

### Backend

- **Framework:** Django 5.2+
- **API:** Django REST Framework
- **Database:** SQLite (development)
- **Auth:** JWT tokens
- **Package Manager:** pipenv

---

## ⚠️ IMPORTANT: Superuser vs Seed User

### Superuser (Admin Account)

Create a Django superuser to access the admin panel:

```bash
cd backend
pipenv shell
python manage.py createsuperuser
```

**What it's for:**

- Access Django admin panel (`http://127.0.0.1:8000/admin/`)
- Create/edit/delete any data directly in database
- Debug issues, manage all users
- **NOT for testing the app as a regular user**

### Seed User (Demo Account)

Create a regular user through the app signup to test features:

**What it's for:**

- Test the app as a real user would
- Your "persona" in the demo (e.g., pablo_pistola, natalia_dev)
- Create posts, add friends, see activity visualization
- **This is your main demo account**

### Quick Reference

|                       | Superuser                   | Seed User     |
| --------------------- | --------------------------- | ------------- |
| **Created via**       | `manage.py createsuperuser` | App signup UI |
| **Access admin?**     | ✅ Yes                      | ❌ No         |
| **Use for demos?**    | ❌ No                       | ✅ Yes        |
| **Has activity viz?** | ❌ (no profile)             | ✅ Yes        |

**Each team member should have BOTH** - superuser for debugging, seed user for demos.

---

## Team Roles & T-Shirt Sizing

| Person      | Size | Strengths                               | Focus Areas                             | Rebuild Type    |
| ----------- | ---- | --------------------------------------- | --------------------------------------- | --------------- |
| **Pablo**   | XL   | UI/UX, visual design, artist background | Complex UI (Timeline, ProfileCard, etc) | Full pseudocode |
| **Natalia** | L    | Backend + Frontend, migrations          | Auth system (backend + frontend)        | Full pseudocode |
| **Colin**   | M    | Backend + Frontend, team lead           | Posts system (backend + context)        | Full pseudocode |
| **Crystal** | M    | Backend + Frontend                      | Friends system (backend + context + UI) | Full pseudocode |
| **Tito**    | S    | Infrastructure                          | API client, theme system, app entry     | Full pseudocode |

**T-shirt sizing = complexity × file count**, not hours. Everyone works at their own pace.

---

## Project Structure

```
numeneon/
├── backend/                 [Django]
│   ├── users/              [Natalia] - Auth system
│   ├── posts/              [Colin] - Posts/content system
│   ├── friends/            [Crystal] - Friend relationships
│   ├── numeneon/           [Shared] - Django config
│   └── manage.py           [Shared] - Django management
│
├── frontend/               [React]
│   ├── src/
│   │   ├── components/
│   │   │   ├── layout/    [Pablo - Pre-built]
│   │   │   ├── pages/
│   │   │   │   ├── Home/         [Pablo - Pre-built]
│   │   │   │   │   └── components/TimelineRiverRow/
│   │   │   │   │       ├── components/  [PostCard, SmartDeck, ThreadView, MobileTabNav, RepostModal]
│   │   │   │   │       └── styles/ (11 SCSS partials)
│   │   │   │   ├── Profile/      [Pablo - Pre-built]
│   │   │   │   ├── Login/        [Natalia - Rebuild]
│   │   │   │   ├── Signup/       [Natalia - Rebuild]
│   │   │   │   └── Friends/      [Crystal - Rebuild]
│   │   │   └── ui/               [Mixed]
│   │   ├── contexts/
│   │   │   ├── AuthContext.jsx       [Natalia]
│   │   │   ├── PostsContext.jsx      [Colin]
│   │   │   ├── FriendsContext.jsx    [Crystal]
│   │   │   ├── ThemeContext.jsx      [Tito]
│   │   │   └── MessageContext.jsx    [Pablo - Pre-built]
│   │   ├── services/
│   │   │   ├── apiClient.js          [Tito]
│   │   │   ├── authService.js        [Natalia]
│   │   │   ├── postsService.js       [Colin]
│   │   │   └── friendsService.js     [Crystal]
│   │   ├── styles/          [Pablo - Design system, DO NOT TOUCH]
│   │   └── main.jsx         [Tito - App entry point]
│   └── package.json         [Shared config]
│
└── docs/team-plan/         [This folder]
    ├── natalia.md
    ├── colin.md
    ├── crystal.md
    ├── pablo.md
    ├── tito.md
    └── team-structure.md
```

---

## Recent Updates (Jan 2026)

### Expandable Full-Page Comment Composer (Jan 2026)

Profile pages now have expandable comment composers that match the feed's behavior:

- **Inline composer** shows expand button (MaximizeIcon) in input wrapper
- **Clicking expand** opens full-page modal via React Portal
- **Full-page view** includes:
  - Original post context (avatar, author name, @handle, timestamp)
  - Post content and media (images scale to 100% width)
  - Thread replies if any exist
  - Fixed composer at bottom with action buttons
- **Applies to:**
  - `TimelineRiver.jsx` - `renderCommentSection()` function
  - `Profile.jsx` - All Posts section inline composers
- **State:** `isComposerFullPage` / `setIsComposerFullPage`
- **Works for** both own profile (`/profile`) and friend profiles (`/profile/:username`)

### Vite Path Aliases (Dec 2024)

Implemented path aliases in `vite.config.js` to simplify imports:

```javascript
resolve: {
  alias: {
    // Root aliases
    '@': './src',
    '@assets': './src/assets',
    '@components': './src/components',
    '@contexts': './src/contexts',
    '@services': './src/services',
    '@utils': './src/utils',
    '@styles': './src/styles',

    // Component type aliases
    '@layout': './src/components/layout',
    '@pages': './src/components/pages',
    '@ui': './src/components/ui',

    // Page-specific aliases
    '@Home': './src/components/pages/Home',
    '@Profile': './src/components/pages/Profile',
  }
}
```

**Benefits:**

- Cleaner imports: `@assets/icons` instead of `../../../../../../../assets/icons`
- Easier refactoring (paths don't break when moving files)
- Consistent import patterns across the codebase

**Team should use aliases in all new code!**

### TimelineRiverRow Modularization

The monolithic `TimelineRiverRow.jsx` has been refactored into focused sub-components:

- **PostCard/** - Individual post rendering with all actions (like, share, comment, edit, delete)
- **SmartDeck/** - Carousel deck with prev/next navigation
- **ThreadView/** - Inline replies thread (Twitter-style)
- **MobileTabNav/** - Mobile category tab navigation
- **timeFormatters.js** - New utility for relative time formatting

### Critical Field Name Fixes

- `oderId` → `orderId` (typo fixed in groupPosts.js, TimelineRiverFeed.jsx)
- Post types are PLURAL: `'thoughts'`, `'media'`, `'milestones'` (not singular)
- Use `media_url` NOT `image` for post media
- Use `reply_count` NOT `comment_count`
- `shares_count` is now wired up and functional
- `is_liked` boolean needed for heart icon state

### Import Path Cleanup (Jan 2025)

**All component imports updated to use Vite path aliases:**

- TimelineRiverFeed.jsx → `@components/pages/Home/utils/groupPosts`
- PostCard.jsx, ThreadView.jsx, RepostModal.jsx → `@components/pages/Home/utils/timeFormatters`
- TopBar.jsx → `@components/ui/ThemeToggle`

**Result:** Cleaner, more maintainable imports. No more `'../../../../utils/file'` patterns!

### Light Mode Blob Fix

- Disabled `mix-blend-mode: screen` for light theme in `_blobs.scss`
- Screen blend adds light, causing white-out on light backgrounds
- Now uses `mix-blend-mode: normal` for light mode

---

## Work Distribution

### Backend Files

| App        | Owner   | File Count | Purpose                                 |
| ---------- | ------- | ---------- | --------------------------------------- |
| `users/`   | Natalia | 11         | User model, auth views, serializers     |
| `posts/`   | Colin   | 7          | Post model, CRUD views, serializers     |
| `friends/` | Crystal | 7          | Friendship model, requests, serializers |

### Frontend Files

| Category             | Owner   | File Count | Purpose                  | Rebuild Type    |
| -------------------- | ------- | ---------- | ------------------------ | --------------- |
| Contexts             | N/C/C/T | 4          | State management layers  | Full pseudocode |
| Services             | N/C/C/T | 4          | API call wrappers        | Full pseudocode |
| Login/Signup         | Natalia | 8          | Auth UI                  | Full pseudocode |
| Friends page         | Crystal | 3          | Friends management UI    | Full pseudocode |
| Theme/Infrastructure | Tito    | 4          | API client, theme toggle | Full pseudocode |
| Pablo's UI           | Pablo   | ~35        | Complex UI components    | Full pseudocode |

_Note: SCSS files are PROVIDED (not rebuilt). Counts only include JSX files._

---

## Data Flow Architecture

### Request Flow (Frontend → Backend)

```
User Action (click, submit)
    ↓
React Component (Login.jsx, ComposerModal, etc.)
    ↓
Context Function (AuthContext.login(), PostsContext.createPost())
    ↓
Service Function (authService.login(), postsService.createPost())
    ↓
API Client (apiClient.js with JWT token)
    ↓
HTTP Request
    ↓
Django View (users/views.py, posts/views.py)
    ↓
Serializer (validation, formatting)
    ↓
Model (database query/save)
    ↓
Serializer (format response)
    ↓
HTTP Response
    ↓
Service (returns data)
    ↓
Context (updates state)
    ↓
Component (re-renders with new data)
```

### Example: Creating a Post

1. User types post in `ComposerModal.jsx` (Pablo's UI)
2. User clicks "Post" button
3. `ComposerModal` calls `PostsContext.createPost({ type, content, image })`
4. `PostsContext` calls `postsService.createPost(postData)`
5. `postsService` uses `apiClient.post('/api/posts/', postData)`
6. `apiClient` attaches JWT token from localStorage
7. Django `PostViewSet.create()` receives request
8. `PostSerializer` validates data
9. `Post` model saves to database
10. `PostSerializer` formats response with nested author data
11. Response flows back through service → context → component
12. `TimelineRiverFeed` re-renders with new post in feed

---

## Critical Integration Points

### 1. Post Data Format

**Colin's backend must return posts in this exact format:**

```javascript
{
  id: 1,
  author: {
    id: 5,
    username: "alice",
    profile_picture: "https://..."  // full URL
  },
  type: "thoughts",  // or "media" or "milestones" (PLURAL forms!)
  content: "This is my post",
  media_url: "https://..." | null,  // NOT 'image'!
  parent: 3 | null,
  parent_id: 3 | null,
  created_at: "2024-12-19T10:00:00Z",  // ISO 8601
  likes_count: 5,
  reply_count: 2,  // NOT 'comment_count'!
  shares_count: 3,  // Required for share/repost button
  is_liked: false  // Has current user liked this post?
}
```

**Why?** Pablo's `TimelineRiverFeed` expects this structure. Column placement depends on `type` field.

**Important field name notes:**

- `media_url` NOT `image`
- `reply_count` NOT `comment_count`
- `shares_count` for repost tracking
- `is_liked` for heart icon state
- Type values are PLURAL: 'thoughts', 'media', 'milestones'

### 2. User/Auth Data Format

**Natalia's backend must return user data in this format:**

```javascript
{
  id: 5,
  username: "alice",
  email: "alice@example.com",
  profile_picture: "https://..." | null,
  bio: "This is my bio" | null
}
```

**Why?** Posts, friends, and profile components all expect this nested in responses.

### 3. Friendship Data Format

**Crystal's backend must return friendships in this format:**

```javascript
{
  id: 1,
  user1: { id: 5, username: "alice", profile_picture: "..." },
  user2: { id: 7, username: "bob", profile_picture: "..." },
  status: "accepted",  // or "pending" or "rejected"
  action_user: 5,  // who sent the request
  created_at: "2024-12-19T10:00:00Z"
}
```

---

## Collaborative Files

Some files require multiple people to add content:

### 1. `backend/numeneon/urls.py`

Each backend person adds ONE line:

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('users.urls')),      # Natalia adds this
    path('api/posts/', include('posts.urls')),     # Colin adds this
    path('api/friends/', include('friends.urls')), # Crystal adds this
]
```

### 2. `frontend/src/contexts/index.js`

Each context owner adds ONE export:

```javascript
export { AuthProvider, useAuth } from "./AuthContext"; // Natalia
export { PostsProvider, usePosts } from "./PostsContext"; // Colin
export { FriendsProvider, useFriends } from "./FriendsContext"; // Crystal
export { ThemeProvider, useTheme } from "./ThemeContext"; // Tito
export { MessageProvider, useMessage } from "./MessageContext"; // Pablo
```

### 3. `frontend/src/main.jsx`

Tito configures this file, nesting everyone's providers:

```javascript
<ThemeProvider>      // Tito
  <AuthProvider>      // Natalia
    <PostsProvider>    // Colin
      <FriendsProvider>  // Crystal
        <MessageProvider>  // Pablo
          <App />
```

---

## Workflow & Best Practices

### Branch Strategy

- Everyone works on `main` branch for now
- **Later** (in January): Create two branches for separate repos
  - `team-shell-frontend` (delete backend/)
  - `team-shell-backend` (delete frontend/)

### Avoiding Merge Conflicts

1. **Never modify files you don't own** (see individual task files)
2. **Collaborative files:** Only add your specific lines (marked with TODO comments)
3. **Shared files:** Read-only (configs, Pablo's design system)
4. **Communicate:** Let team know before modifying any shared config

### Development Workflow

1. Read your task file (`natalia.md`, `colin.md`, etc.)
2. Start with backend (models → serializers → views → URLs)
3. Test backend with Django admin or Postman/curl
4. Build frontend service layer
5. Build context layer
6. Build/modify UI components (if applicable)
7. Test integration end-to-end

### Testing Strategy

- **Backend:** Use Django admin + Postman to test APIs manually
- **Frontend:** Use React DevTools to inspect context state
- **Integration:** Test in browser with network tab open
- **Each person:** Run through their testing checklist in task file

---

## Communication Channels

### Daily Standups (Suggested)

- What did you complete yesterday?
- What are you working on today?
- Any blockers?

### Integration Points to Discuss

- **Natalia ↔ Colin:** User model structure for post author
- **Natalia ↔ Crystal:** User model structure for friendships
- **Colin ↔ Pablo:** Post data format for Timeline UI
- **Crystal ↔ Pablo:** Friend request notification format for TopBar
- **Tito ↔ Everyone:** API client configuration, any auth issues

---

## Getting Started

### 1. Read Your Task File

- `natalia.md` - Auth system
- `colin.md` - Posts system
- `crystal.md` - Friends system
- `pablo.md` - UI documentation
- `tito.md` - Infrastructure

### 2. Review Integration Points

- Who depends on your work?
- Whose work do you depend on?

### 3. Start with Backend

- Models first (database structure)
- Then serializers (data formatting)
- Then views (API endpoints)
- Test with Django admin

### 4. Build Frontend Layer

- Service functions (API calls)
- Context (state management)
- Components (UI)

### 5. Test Integration

- Can frontend fetch data from backend?
- Does data format match expectations?
- Do all CRUD operations work?

---

## Success Criteria

**Project is complete when:**

- [ ] Users can signup and login
- [ ] Users can create posts (thoughts, media, milestones)
- [ ] Posts appear in Timeline River UI with correct column placement
- [ ] Users can send/accept/reject friend requests
- [ ] Friends page shows connections
- [ ] Theme toggle switches between light/dark mode
- [ ] All contexts provide data to Pablo's UI
- [ ] All API endpoints return data in expected formats
- [ ] No merge conflicts occur during development
- [ ] Comment composers expand to full-page view on Profile pages

---

## Resources

### Django/DRF Docs

- Models: https://docs.djangoproject.com/en/4.2/topics/db/models/
- Views: https://www.django-rest-framework.org/api-guide/viewsets/
- Serializers: https://www.django-rest-framework.org/api-guide/serializers/

### React Docs

- Context: https://react.dev/learn/passing-data-deeply-with-context
- Hooks: https://react.dev/reference/react

### Pablo's Design System

- All files in `frontend/src/styles/`
- Variables in `_variables.scss`
- Mixins in `_mixins.scss`
- Button styles in `_buttons.scss`

---

## Questions?

Check with:

- **Pablo** - UI integration, design system, data format questions
- **Colin** - Team lead, general questions, posts system
- **Natalia** - Auth issues, user model questions, migrations
- **Crystal** - Friends system questions
- **Tito** - API client issues, theme problems
