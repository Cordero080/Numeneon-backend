markdown# NUMENEON TEAM REBUILD - Part 1: Context & Strategy

## HOW TO USE THESE FILES

**⚠️ READ [00-START-HERE.md](./00-START-HERE.md) FIRST if you haven't already!**

This is Part 1 of 5. Read these files in order:

0. `00-START-HERE.md` - Quick overview, workflow, FAQ
1. `01-CONTEXT-AND-STRATEGY.md` ← YOU ARE HERE
2. `02-PSEUDOCODE-EXAMPLES.md` - All 12 example templates
3. `03-BACKEND-INSTRUCTIONS.md` - Backend pseudocode tasks
4. `04-FRONTEND-INSTRUCTIONS.md` - Frontend pseudocode tasks
5. `05-TEAM-PLAN-FILES.md` - Team markdown file templates

---

## BACKGROUND & CONTEXT

I (Pablo) built a complete working prototype of NUMENEON, a cyberpunk-themed social media app with React + Django. Now my 5-person bootcamp team will REBUILD portions of the codebase together as a learning exercise.

**Project Stack:**

- Frontend: React 18+, Vite 7.2+, React Router DOM, Vanilla CSS/SCSS
- Backend: Django 5.2+, Django REST Framework, PostgreSQL, JWT auth, pipenv
- Build: Vite with path aliases (@assets, @components, @contexts, etc.)
- Current state: Fully functional prototype with real API connections

**Team (T-Shirt Sizing):**

| Person      | Size | Files | Focus Area                                             | Rebuild Type    |
| ----------- | ---- | ----- | ------------------------------------------------------ | --------------- |
| **Pablo**   | XL   | ~35   | Complex UI: Timeline, ProfileCard, Carousel, Analytics | Full pseudocode |
| **Natalia** | L    | 19    | Auth system + Migration management                     | Full pseudocode |
| **Colin**   | M    | 15    | Posts CRUD + ComposerModal + DeleteConfirmModal        | Full pseudocode |
| **Crystal** | M    | 12    | Friends system + Friends page                          | Full pseudocode |
| **Tito**    | S    | 6     | Infrastructure: apiClient, Theme, main.jsx             | Full pseudocode |

**CRITICAL: Everyone rebuilds from pseudocode** (including Pablo). This ensures legitimate git history for all team members. Pablo has an advantage since he wrote the original, but he still types and commits code.

---

## THE STRATEGY (FINAL - Dec 2024)

### Approach: Everyone Rebuilds From Pseudocode Shells

**ALL team members** (including Pablo) rebuild their assigned files from pseudocode shells.

- Styles (SCSS) are provided/injected - team focuses on JSX logic
- SVG icons are extracted to shared `icons.jsx` - team imports them
- Each person creates PRs showing their contribution over time

### Why This Works:

- **Git history matters** - everyone has PR records of their work
- **Learning value** - team learns architecture, state, component patterns
- **Realistic scope** - styles provided, logic rebuilt
- **No overlap** - each person owns distinct files

### SVG Icon Strategy:

All inline SVGs extracted to a modular icon system in `frontend/src/assets/icons/`:

```
frontend/src/assets/
├── icons.jsx          # 24 lines - barrel re-export (backwards compatible)
└── icons/
    ├── index.js       # Aggregates all category exports
    ├── navigation.jsx # Target, arrows, back, flip, login/logout
    ├── user.jsx       # UserIcon, GlobeIcon, LockIcon, FriendsIcon, VisibilityIcon (smart)
    ├── engagement.jsx # HeartIcon, CommentIcon, ShareIcon, BookmarkIcon
    ├── actions.jsx    # EditIcon, TrashIcon, CloseIcon, PlusIcon, SendIcon
    ├── media.jsx      # ImageIcon, ExpandIcon, MaximizeIcon, MinimizeIcon
    ├── ui.jsx         # SettingsIcon, EyeIcon, MoreIcon, GridIcon, ClockIcon
    ├── sidenav.jsx    # HexHomeIcon, SignalIcon, NetworkIcon
    ├── analytics.jsx  # BoltIcon, BarChartIcon, ShieldIcon, ActivityIcon
    ├── profile.jsx    # LocationIcon, LinkIcon, CalendarIcon, StarIcon
    ├── messaging.jsx  # MessageBubbleIcon, MessageLineIcon, EmojiIcon
    └── misc.jsx       # MusicIcon, MapPinIcon, PostTriangleIcon
```

**How to import icons (using Vite path aliases - recommended):**

```jsx
// Method 1: From barrel export using alias (cleanest)
import { HeartIcon, CommentIcon, CloseIcon } from "@assets/icons";

// Method 2: From specific category using alias (tree-shakeable)
import { HeartIcon } from "@assets/icons/engagement";
import { CloseIcon } from "@assets/icons/actions";
```

**Legacy relative paths still work but are not recommended:**

```jsx
// OLD (still works but verbose)
import { HeartIcon } from "../../assets/icons";
```

**Icon API (consistent across ALL icons):**

```jsx
<HeartIcon size={18} className="my-class" onClick={handleClick} />
```

- `size` - Controls width AND height (default varies by icon)
- `className` - For styling overrides
- `...props` - Pass-through for onClick, aria-label, etc.

**Finding the right icon:**

1. Check the category files - icons are grouped semantically
2. See `docs/refactoring/SVG-Icons-Refactor.md` for full icon inventory
3. All 70+ icons listed with their category

Icons provided as completed files (not pseudocode) - team just imports them

---

## BRANCH STRUCTURE

Create TWO shell branches from main:

1. **`team-shell-frontend` branch:**

   - Delete the entire `backend/` folder
   - Keep `frontend/` folder with all files
   - Replace implementation with pseudocode shells
   - Inject SCSS styles (provided)
   - Inject `icons.jsx` (provided)

2. **`team-shell-backend` branch:**
   - Delete the entire `frontend/` folder
   - Keep `backend/` folder with all files
   - Replace implementation with pseudocode shells

**Workflow for each team member:**

1. Clone shell repo
2. Create feature branch: `git checkout -b [name]/[feature]`
3. Build from pseudocode over multiple commits
4. Create PR to merge into main
5. Git history shows contribution timeline

---

## ASSETS PROVIDED (Not Pseudocode)

These files are PROVIDED as-is, not rebuilt:

| File                               | Why Provided                            |
| ---------------------------------- | --------------------------------------- |
| `frontend/src/assets/icons/`       | All SVG icons (modular system)          |
| `frontend/vite.config.js`          | Build config with path aliases          |
| `frontend/src/styles/*` (13 files) | Design system (variables, mixins, etc.) |
| All `.scss` files                  | Styles injected, team writes JSX only   |

**Vite Path Aliases (Configured):**

Path aliases are configured in `vite.config.js` to simplify imports:

```javascript
resolve: {
  alias: {
    // Root aliases
    '@': path.resolve(__dirname, './src'),
    '@assets': path.resolve(__dirname, './src/assets'),
    '@components': path.resolve(__dirname, './src/components'),
    '@contexts': path.resolve(__dirname, './src/contexts'),
    '@services': path.resolve(__dirname, './src/services'),
    '@utils': path.resolve(__dirname, './src/utils'),
    '@styles': path.resolve(__dirname, './src/styles'),

    // Component type aliases
    '@layout': path.resolve(__dirname, './src/components/layout'),
    '@pages': path.resolve(__dirname, './src/components/pages'),
    '@ui': path.resolve(__dirname, './src/components/ui'),

    // Page-specific aliases (most commonly imported)
    '@Home': path.resolve(__dirname, './src/components/pages/Home'),
    '@Profile': path.resolve(__dirname, './src/components/pages/Profile'),
  }
}
```

Team members should **use these aliases** instead of relative paths for cleaner code.

**Import examples:**

```jsx
// Icons
import { HeartIcon, CloseIcon } from "@assets/icons";

// Contexts
import { useAuth } from "@contexts/AuthContext";

// Cross-page imports
import TimelineRiver from "@Profile/components/TimelineRiver";
```

---

## FILE VALIDATION (Already Completed)

- ✅ 148 files validated - almost all paths correct
- ❌ 1 incorrect path - `backend/users/admin.py` doesn't exist (removed)
- 📝 7 missing files added - 5 `index.js` for Pablo, 2 `__init__.py` for Natalia
- 🤝 ~27 shared/config files identified as "do not touch"

---

## FILE CATEGORIES & ASSIGNMENTS

### CATEGORY 1: PABLO (XL - ~35 JSX files)

**Rebuilds these complex UI components from pseudocode:**

_Note: SCSS files are PROVIDED (not rebuilt). Count only includes JSX files._

**Timeline System (Home page):**

```
frontend/src/components/pages/Home/
├── Home.jsx, index.js (2 JSX)
├── utils/
│   ├── groupPosts.js (post grouping algorithm)
│   └── timeFormatters.js (relative time formatting)
├── components/
│   ├── TimelineRiverFeed/ (2 JSX: .jsx + index.js)
│   ├── TimelineRiverRow/ (MODULAR - refactored Jan 2025)
│   │   ├── TimelineRiverRow.jsx, index.js (2 JSX)
│   │   └── components/
│   │       ├── PostCard/ (2 JSX)
│   │       ├── SmartDeck/ (2 JSX)
│   │       ├── ThreadView/ (2 JSX)
│   │       ├── MobileTabNav/ (2 JSX)
│   │       ├── RepostModal/ (2 JSX - Jan 2026)
│   │       └── index.js (barrel export)
│   └── MediaLightbox/ (2 JSX)
```

**Profile System:**

```
frontend/src/components/pages/Profile/
├── Profile.jsx, index.js (2 JSX)
├── components/
│   ├── ComposerModal/ (2 JSX)
│   ├── ProfileCard/ (2 JSX + subcomponents)
│   │   ├── ProfileCardFront.jsx
│   │   ├── ProfileCardBack.jsx
│   │   └── ActivityVisualization/ (2 JSX)
│   └── TimelineRiver/ (NEW MODULAR - Jan 2026)
│       ├── TimelineRiver.jsx, index.js (2 JSX)
│       └── components/
│           ├── RiverSmartDeck/ (2 JSX)
│           ├── RiverPostActions/ (2 JSX)
│           ├── RiverFeedView/ (2 JSX)
│           ├── RiverComposer/ (2 JSX)
│           ├── RiverTimelineView/ (2 JSX)
│           ├── RiverThread/ (2 JSX)
│           └── index.js (barrel export)
```

**Key Complexity:**

- 3D flip animation (ProfileCard)
- Carousel deck system (SmartDeck component within TimelineRiverRow)
- Analytics charts: Wave, Heatmap, Donut (ProfileCardBack)
- Touch handlers for mobile swipe
- Thread expansion for replies (ThreadView component)
- Modular post cards (PostCard component)
- Mobile tab navigation (MobileTabNav component)

---

### CATEGORY 2: COLIN (M - 15 files)

**Backend (7 files):**

- `backend/posts/models.py`, `views.py`, `serializers.py`, `urls.py`, `apps.py`
- `backend/posts/__init__.py`, `admin.py`

**Frontend (8 files):**

- `frontend/src/contexts/PostsContext.jsx`
- `frontend/src/services/postsService.js`
- `frontend/src/components/pages/Home/components/ComposerModal/` (3 files)
- `frontend/src/components/pages/Home/components/DeleteConfirmModal/` (3 files)

**Why ComposerModal + DeleteConfirmModal → Colin:**

- ComposerModal creates posts → Colin owns PostsContext
- DeleteConfirmModal deletes posts → Colin owns PostsContext
- Keeps post-related UI with post-related logic

---

### CATEGORY 3: NATALIA (L - 19 files)

**Backend (11 files):**

- `backend/users/models.py`, `views.py`, `serializers.py`, `urls.py`, `apps.py`
- `backend/users/__init__.py`
- `backend/users/management/__init__.py`, `commands/__init__.py`, `commands/create_test_user.py`
- `backend/users/migrations/0001_initial.py`, `__init__.py`

**Frontend (8 files):**

- `frontend/src/contexts/AuthContext.jsx`
- `frontend/src/components/pages/Login/` (Login.jsx, Login.scss, index.js)
- `frontend/src/components/pages/Signup/` (Signup.jsx, Signup.scss, index.js)
- `frontend/src/components/ui/ProtectedRoute.jsx`

**Special Responsibility:** Migration Manager (reviews all team migrations)

---

### CATEGORY 4: CRYSTAL (M - 12 files)

**Backend (7 files):**

- `backend/friends/models.py`, `views.py`, `serializers.py`, `urls.py`, `apps.py`
- `backend/friends/__init__.py`, `admin.py`

**Frontend (5 files):**

- `frontend/src/contexts/FriendsContext.jsx`
- `frontend/src/services/friendsService.js`
- `frontend/src/components/pages/Friends/` (Friends.jsx, Friends.scss, index.js)

**Integration Note:** NotificationModal consumes FriendsContext for pending requests

---

### CATEGORY 5: TITO (S - 6 files)

- `frontend/src/main.jsx`
- `frontend/src/services/apiClient.js`
- `frontend/src/contexts/ThemeContext.jsx`
- `frontend/src/components/ui/ThemeToggle/` (ThemeToggle.jsx, ThemeToggle.scss, index.js)

**Critical:** apiClient.js must be built FIRST - all services depend on it

---

### CATEGORY 6: PROVIDED (SCSS + Config - Not Rebuilt)

**SCSS files for ALL components** (team writes JSX only):

- All `.scss` files are provided complete
- SCSS partials (`_*.scss`) provided complete
- Design system (`frontend/src/styles/`) provided complete

**Layout Components (Pablo rebuilds JSX, SCSS provided):**

- All files in `frontend/src/components/layout/TopBar/` (TopBar, MessageModal, NotificationModal, SearchModal)
- All files in `frontend/src/components/layout/SideNav/`

**Other Pages (styles injected):**

- `frontend/src/components/pages/About/` (all files)
- `frontend/src/components/pages/Landing/` (all files)
- `frontend/src/components/pages/NotFound/` (all files)

**Contexts (already complete):**

- `frontend/src/contexts/MessageContext.jsx`

**Design System (DO NOT TOUCH):**

- All 13 files in `frontend/src/styles/`

**Icon Library (PROVIDED - just import and use):**

- `frontend/src/assets/icons.jsx` (barrel re-export)
- `frontend/src/assets/icons/` directory (11 category files + index.js)
- See `docs/refactoring/SVG-Icons-Refactor.md` for full documentation

---

## FILE COUNT SUMMARY

```
XL Pablo:    ███████████████████████████████████  ~35 JSX files (complex animations, charts)
L  Natalia:  ███████████████████                  19 files (auth foundation)
M  Colin:    ███████████████                      15 files (posts + modals)
M  Crystal:  ████████████                         12 files (friends system)
S  Tito:     ██████                                6 files (infrastructure)
                                                 ───
                                                  ~87 files rebuilt by team
```

**Note:** SCSS files are PROVIDED (not counted). Pablo's count reflects JSX files only.

---

## BUILD DEPENDENCY CHAIN

**Phase 1 - Foundation (Start Here):**

```
Tito: apiClient.js → Everyone's services depend on this
Natalia: users/models.py → Colin/Crystal need User ForeignKey
```

**Phase 2 - Backend Models:**

```
Colin: posts/models.py (parallel)
Crystal: friends/models.py (parallel)
```

**Phase 3 - Backend APIs:**

```
Natalia: users/views.py, serializers.py, urls.py
Colin: posts/views.py, serializers.py, urls.py
Crystal: friends/views.py, serializers.py, urls.py
```

**Phase 4 - Frontend Services:**

```
Colin: postsService.js
Crystal: friendsService.js
```

**Phase 5 - Frontend Contexts:**

```
Natalia: AuthContext.jsx → Must complete before others
Colin: PostsContext.jsx → Waits for AuthContext
Crystal: FriendsContext.jsx → Waits for AuthContext
Tito: ThemeContext.jsx
```

**Phase 6 - Frontend Pages/Components:**

```
Natalia: Login/, Signup/, ProtectedRoute.jsx
Colin: ComposerModal/, DeleteConfirmModal/
Crystal: Friends/ page
Pablo: TimelineRiverFeed, TimelineRiverRow, ProfileCard, MediaLightbox
Tito: ThemeToggle/, main.jsx (provider nesting)
```

---

### CATEGORY 7: COLLABORATIVE FILES

- `backend/numeneon/urls.py` - Each backend person adds their `include()` line
- `frontend/src/contexts/index.js` - Each context owner adds their export

---

### CATEGORY 8: SHARED CONFIG (DO NOT TOUCH)

Backend Config: `manage.py`, `seed_posts.py`, `numeneon/settings.py`, etc.
Frontend Config: `eslint.config.js`, `vite.config.js`, `package.json`, `index.html`
Global Styles: All 13 files in `frontend/src/styles/`

---

## PSEUDOCODE STYLE GUIDELINES

### Core Principle: "What + Why, Not How"

Every pseudocode TODO should:

1. State WHAT to build (the functionality)
2. Explain WHY it matters (integration context)
3. Show EXPECTED OUTPUT (data format for integration)
4. Give LEARNING PROMPTS ("Think about...")
5. NOT dictate HOW (they figure out implementation)

### Template:

```
// TODO: [What to build]
//
// [Why it matters / how it fits in the app]
//
// [Expected input/output format if relevant]
//
// Think about:
// - [Question that makes them reason about edge cases]
// - [Question about design decisions]
//
// Hint: [Gentle nudge toward React/Django feature, NOT exact code]
```

---

## MIGRATION WORKFLOW CLARIFICATION

- **Colin & Crystal:** Run `makemigrations` for their own apps
- **Natalia:** Reviews migration files, runs central `migrate` command
- Natalia is the gatekeeper, not the sole creator

---

## groupPosts.js DECISION

This file stays in Pablo's domain with full implementation intact.
Add a USAGE/reference comment explaining what it does.
It's NOT pseudocode - team just needs to understand its purpose.

**IMPORTANT UPDATE (Dec 2024):**
Grouping changed from date+user to **USER ONLY** for "space economy":

- OLD: Each row = one user + one date (same user appeared in multiple rows)
- NEW: Each row = one user (ALL their posts in one row with carousel)
- This enables carousel arrows (need 3+ posts per type per user)
- See `docs/features/RiverTimeline.md` for full documentation

---

## PLACEHOLDER COMPONENTS (Team Awareness)

Some UI components exist as placeholders with no backend:

| Component           | Location                       | Status      | Notes                                         |
| ------------------- | ------------------------------ | ----------- | --------------------------------------------- |
| **Engagement Ring** | ProfileCardFront.jsx (L78-101) | Placeholder | Decorative SVG animation only                 |
| **Share Button**    | TimelineRiverRow.jsx           | ✅ COMPLETE | Backend endpoint + frontend sharePost() wired |
| **Bookmark Button** | TimelineRiverRow.jsx           | Placeholder | No backend yet                                |

See `docs/stretch-goals/` for implementation plans.

---

## RECENT IMPLEMENTATION NOTES

**TimelineRiverFeed.jsx:**

- `useMemo` was REMOVED from post grouping logic for fresh renders
- Grouping now happens directly without memoization caching

**groupPosts.js - River Timeline "Space Economy" (Dec 2024):**

- Changed from grouping by `date + userId` to **`userId` only**
- Each user now appears as exactly ONE row in the timeline
- All posts (thoughts, media, milestones) collected in that single row
- Carousel arrows navigate between posts of the same type
- `mostRecentDate` tracks when user was last active (shown in header)
- This enables "space economy" - scan 10 users at a glance vs 30+ rows

**Home.jsx & Profile.jsx Inline Composers:**

- Both pages have inline quick-post composers with triangle submit button
- Triangle button is positioned INSIDE the input wrapper
- Cmd/Ctrl + Enter keyboard shortcut also submits
- Both call PostsContext `createPost()` directly

**ActivityVisualization.scss - Responsive Toggle Buttons (commit a7a57d8):**

- Wave/Heatmap toggle buttons now scale properly on all mobile sizes
- Breakpoints added: 600px, 480px, 375px (supports iPhone 6+)
- Toggle buttons: Reduced padding, min-width/height, icon sizes for small screens
- Activity header: Added `flex-wrap: wrap` for narrow viewports
- Activity meta: Hidden on screens ≤480px to prioritize toggle visibility
- Wave chart container: Responsive padding/border-radius adjustments
- CSS Location: `frontend/src/components/pages/Profile/components/ProfileCard/components/ActivityVisualization/ActivityVisualization.scss`

**User Profile Navigation (Dec 2024):**

- Users can click any username/avatar in the timeline to visit that user's profile
- Route: `/profile/:username` added to App.jsx for viewing other users
- Route: `/profile` remains for viewing your own profile
- TimelineRiverRow.jsx: Added `handleUserClick()` with navigation logic
- TimelineRiver.jsx (Profile): Added clickable friend headers in Friends Feed
- CSS: `.clickable-user` and `.clickable-friend` classes with hover effects
- Full documentation: `docs/features-implemented/UserProfileNavigation.md`

**TimelineRiverRow Modularization (Jan 2025):**

- Refactored monolithic TimelineRiverRow.jsx into smaller, focused components
- New components extracted:
  - `PostCard.jsx` - Individual post rendering with all actions (like, share, comment, edit, delete)
  - `SmartDeck.jsx` - Carousel deck display with prev/next navigation
  - `ThreadView.jsx` - Inline replies thread (Twitter-style)
  - `MobileTabNav.jsx` - Mobile category tab navigation (thoughts/media/milestones)
- New utility: `utils/timeFormatters.js` - `formatRelativeTime()` function extracted
- TimelineRiverRow.jsx now orchestrates sub-components instead of handling everything
- All components use barrel exports via `components/index.js`

**Bug Fixes (Jan 2025):**

- Fixed typo: `oderId` → `orderId` across groupPosts.js, TimelineRiverFeed.jsx
- Wired up `sharePost()` function to Repost button (was imported but unused)
- Fixed light mode blobs: Disabled `mix-blend-mode: screen` for light theme (was causing white-out)
- **Updated all imports to use Vite path aliases:**
  - TimelineRiverFeed.jsx, PostCard.jsx, ThreadView.jsx, RepostModal.jsx now use `@components` and `@assets`
  - TopBar.jsx uses `@components/ui/ThemeToggle`
  - No more relative paths like `'../../../../utils/file'`

**Profile Privacy Controls (Dec 2024):**

- When viewing another user's profile, certain UI elements are hidden
- `isOwnProfile` detection: `!profileUsername || profileUsername === currentUser?.username`
- Hidden on other profiles: Post Composer, View Mode Toggle, Edit/Delete buttons
- Profile.jsx: Added `useParams()`, `isOwnProfile` logic, `profileUser` lookup
- TimelineRiver.jsx: Accepts `isOwnProfile` prop, conditionally renders action buttons
- Full documentation: `docs/features-implemented/ProfilePrivacyControls.md`

**Engagement Analytics Boost (Dec 2024):**

- Heatmap activity levels boosted for better visual density
- High tier: 800-1500 likes (was 400-800)
- Medium tier: 400-800 likes (was 200-400)
- Low tier: 200-400 likes (was 100-200)
- `ANALYTICS_NOW` now uses live `Date.now()` instead of hardcoded date
- Full documentation: `docs/features-implemented/EngagementAnalytics.md`

**Unified Close Button System (Dec 2024):**

- Created `.close-btn-glow` class for all modal/overlay X buttons
- Dark mode: Crimson glow (rgba(255, 77, 109)) with 90° spin on hover
- Light mode: Deeper red with `pointer-events: auto !important` fix
- Applied to: MessageModal, SearchModal, ComposerModal, MediaLightbox, TimelineRiver
- CSS Location: `frontend/src/styles/_buttons.scss` (lines 173-215)
- Light mode override: `frontend/src/styles/_light-mode.scss`

**Mobile MessageModal Improvements (Dec 2024):**

- Added `mobileView` state with 'list' and 'chat' values for panel toggling
- Back button to return to conversation list on mobile
- Full viewport coverage (z-index 9999) to properly cover navbar
- Search/filter for conversations by name, username, or message content
- Files: `MessageModal.jsx`, `_responsive.scss`
- Full documentation: `docs/features-implemented/MobileMessageModal.md`

**Profile Carousel Navigation (Dec 2024):**

- Chamfered corner nav buttons using `clip-path: polygon()`
- Always show dots (removed conditional index/total count display)
- Transparent container - floating buttons and dots, no background
- Column-specific glow colors: Blue (thoughts), Magenta (media), Gold (milestones)
- CSS Location: `TimelineRiver.scss` (lines 124-350)

**Mobile Category Tabs (Dec 2024):**

- Tab-based navigation for profile timeline on mobile (768px breakpoint)
- Three tabs: Thoughts (blue), Media (magenta), Milestones (gold)
- `mobileCategory` state controls which column is visible
- Glow effects on active tabs matching column colors
- CSS Location: `TimelineRiver.scss` (lines 1050-1190)

**Light Mode Fixes (Dec 2024):**

- `.river-post-actions` background: transparent (was grey in light mode)
- Heart/like icon visibility: darker stroke colors (rgba(0, 0, 0, 0.55))
- MessageModal "Start conversation" text now visible
- Close button clickability fixed with `pointer-events: auto !important`

**SearchModal Component (Dec 2024):**

- New global search modal for users and posts
- Accessible from TopBar targeting reticle icon
- Filters: All, Users, Posts with tab switching
- User results: Click to visit profile, message icon to open DM
- Post results: Click to navigate to author's profile
- Files: `frontend/src/components/layout/TopBar/SearchModal/`

**Friends Page Interactivity (Dec 2024):**

- Friend cards are now clickable - navigate to their profile
- Message icon opens DM with that friend
- Request cards are clickable - view requester's profile
- File: `frontend/src/components/pages/Friends/Friends.jsx`

**ProfileCard Context Awareness (Dec 2024):**

- `isOwnProfile` prop passed through ProfileCard components
- Other users' profiles show Save/Bookmark button (purple accent)
- Own profile shows More Options and Analytics flip button
- QuickSettings only shown on own profile (back of card)
- Files: `ProfileCard.jsx`, `ProfileCardFront.jsx`, `ProfileCardBack.jsx`

**Thread/Reply System in TimelineRiver (Dec 2024):**

- "View X replies" link expands thread below post
- Reply composer for adding comments to any post
- Edit/delete own replies with inline forms
- Uses `fetchReplies()`, `createReply()`, `updateReply()`, `deleteReply()` from PostsContext
- Files: `TimelineRiver.jsx` (lines 325-620)

**Card User Headers (Dec 2024):**

- All timeline cards now display avatar + username INSIDE the card
- Provides consistent visual identity so users know whose content they're viewing
- Applied to: Home feed, Friends Feed, My Timeline carousel, River Continuation, All Posts section
- Friends Feed cards are clickable (navigate to friend's profile)
- My Timeline cards show profile owner info (not clickable - already on profile)
- Helper function `getInitials(user)` extracts initials for avatar display
- CSS: `.river-card-author`, `.friend-avatar`, `.friend-name`, `.clickable-friend`
- Full documentation: `docs/features-implemented/CardUserHeaders.md`

**Friends Feed Mobile Category Tabs (Dec 2024):**

- Mobile category tabs now work for Friends Feed (not just My Timeline)
- `mobileCategory` state shared across both view modes
- Tabs placed inside feed mode section for proper scoping
- CSS classes: `.friend-row .river-streams.mobile-show-{category}`
- Each friend row respects the selected mobile category

**River Continuation Spacing (Dec 2024):**

- Reduced gap between carousel section and river continuation
- `.timeline-river` bottom padding: 200px → 40px
- `.river-continuation` margin: var(--space-2xl) → var(--space-lg)
- `.all-posts-section` margin: var(--space-xl) → var(--space-lg)

**All Posts Section User Headers (Dec 2024):**

- Added `getInitials()` helper function to Profile.jsx
- All Posts cards now show profile owner's avatar and username
- Consistent with timeline cards structure

**Expandable Comment Composer on Profile Pages (Jan 2026):**

- Profile pages (TimelineRiver + All Posts section) now have expandable full-page comment composers
- Inline composer shows expand button (MaximizeIcon) next to input field
- Clicking expand opens full-page modal via React Portal (matches feed's PostCard behavior)
- Full-page view includes:
  - Original post context (avatar, author name, @handle, timestamp, content, media)
  - Media images scale to fill modal width (100%) with aspect ratio preserved
  - Thread replies displayed if any exist
  - Fixed composer at bottom with media upload button
- Works for both own profile (`/profile`) and visiting friend profiles (`/profile/:username`)
- State: `isComposerFullPage` + `setIsComposerFullPage` in both Profile.jsx and TimelineRiver.jsx
- CSS: `.full-page-composer-overlay`, `.full-page-composer`, `.reply-context-media`

---

**NEXT:** Read `02-PSEUDOCODE-EXAMPLES.md` for all 11 example templates
