# Pablo's UI Files (Size: XL)

## Your Mission

You're rebuilding the complex UI system from pseudocode - the same as everyone else on the team. This ensures legitimate git history showing your contributions.

**Your advantage:** You wrote the original, so rebuilding from your own pseudocode is faster. But you still type and commit code like everyone else.

You also configured the **Vite path alias system** to simplify imports across the codebase.

## What You're Doing

**Rebuilding ALL your JSX files from pseudocode.**

SCSS files are PROVIDED (not rebuilt) - you only write JSX logic.

For each component:

1. Read the pseudocode TODO comments
2. Implement the logic
3. Commit with descriptive messages
4. Create PR showing your contribution

## Vite Path Aliases (Configured by Pablo)

You configured path aliases in `vite.config.js` to improve developer experience:

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

    // Page-specific aliases
    '@Home': path.resolve(__dirname, './src/components/pages/Home'),
    '@Profile': path.resolve(__dirname, './src/components/pages/Profile'),
  }
}
```

**Benefits for the team:**

- No more `../../../../../../../` paths
- Consistent imports across the codebase
- Easier refactoring (paths don't break when moving files)
- Cleaner, more readable code

**Usage examples:**

```jsx
// Icons
import { HeartIcon, CloseIcon } from "@assets/icons";

// Contexts
import { useAuth } from "@contexts/AuthContext";
import { usePosts } from "@contexts/PostsContext";

// Services
import apiClient from "@services/apiClient";

// Components
import TopBar from "@components/layout/TopBar";
```

**Team should use aliases everywhere!**

## Your Files (~35 JSX files)

_Note: SCSS files are PROVIDED. Count only includes JSX files you rebuild._

### Entry & Layout

- `frontend/src/App.jsx` - Main app component, routing
- `frontend/src/components/layout/TopBar/` - Top navigation bar (3 files + MessageModal with 8 SCSS partials)
- `frontend/src/components/layout/SideNav/` - Side navigation menu (3 files)

### Home Page System

- `frontend/src/components/pages/Home/` - Main feed page (3 files)
  - `Home.jsx`, `Home.scss`, `index.js`
  - `utils/groupPosts.js` - Utility for organizing posts by user
  - `utils/timeFormatters.js` - **NEW** Relative time formatting utilities
  - `components/DeleteConfirmModal/` - Confirmation dialog (3 files)
  - `components/MediaLightbox/` - Image viewer modal (2 files + 7 SCSS partials in styles/ folder)
  - `components/TimelineRiverFeed/` - Main feed container (3 files)
  - `components/TimelineRiverRow/` - **REFACTORED (Jan 2025)** Modular architecture:
    - `TimelineRiverRow.jsx` - Main orchestrator component
    - `TimelineRiverRow.scss` - Main styles
    - `styles/` - 11 SCSS partials (\_base, \_carousel, \_composer, \_desktop-stack-nav, \_light-mode, \_post-actions, \_post-card, \_post-media, \_responsive, \_smart-deck, \_thread)
    - `components/PostCard/` - Individual post rendering with actions
    - `components/SmartDeck/` - Carousel deck with navigation
    - `components/ThreadView/` - Inline replies thread (Twitter-style)
    - `components/MobileTabNav/` - Mobile category tab navigation
    - `components/RepostModal/` - **NEW (Jan 2026)** Share modal with repost/copy link icons

### Profile Page System

- `frontend/src/components/pages/Profile/` - User profile page (3 files)
  - `Profile.jsx`, `Profile.scss`, `index.js`
  - **NEW (Jan 2026):** All Posts section has expandable full-page comment composer
    - Inline composer shows expand button (MaximizeIcon)
    - Full-page modal shows post context + media + thread + fixed composer
  - `components/ComposerModal/` - Post creation modal (3 files)
  - `components/ProfileCard/` - User profile card with flip animation (5 subcomponents with flip system)
  - `components/TimelineRiver/` - Profile timeline view (MODULAR - Jan 2026):
    - `TimelineRiver.jsx`, `index.js` - Main component
    - `components/RiverSmartDeck/` - Carousel deck navigation
    - `components/RiverPostActions/` - Action buttons (like, share, comment)
    - `components/RiverFeedView/` - Friends feed rows
    - `components/RiverComposer/` - Expandable full-page composer
    - `components/RiverTimelineView/` - River cards display
    - `components/RiverThread/` - Inline thread replies

### Other Pages

- `frontend/src/components/pages/About/` - About page (3 files)
- `frontend/src/components/pages/Landing/` - Landing/marketing page (3 files)
- `frontend/src/components/pages/NotFound/` - 404 error page (3 files)

### Contexts

- `frontend/src/contexts/MessageContext.jsx` - Message system state

### Assets (PROVIDED - Not rebuilt)

- `frontend/src/assets/icons/` - SVG icon system (provided complete)
- `frontend/src/assets/huddl-logo.svg` - Logo file

### Design System (PROVIDED - Not rebuilt)

- `frontend/src/styles/` - All 13 global SCSS files (provided complete)

---

## Pseudocode Format

Your JSX files will have detailed pseudocode like this:

```javascript
// TODO: Create TimelineRiverFeed - main feed container
//
// This component displays all posts in a 3-column "river" layout:
// - Left column: 'thoughts' posts (text-only)
// - Center column: 'media' posts (with images)
// - Right column: 'milestones' posts (achievements)
//
// State you need:
// - posts: Array from PostsContext
// - groupedPosts: Result of groupPosts() utility
//
// Integration points:
// - Consumes: PostsContext via usePosts()
// - Uses: groupPosts.js utility
// - Renders: TimelineRiverRow for each user group
//
// Expected data format from PostsContext:
// {
//   id: number,
//   author: { id, username, profile_picture },
//   type: 'thoughts' | 'media' | 'milestones',
//   content: string,
//   media_url: string | null,
//   likes_count: number,
//   reply_count: number,
//   shares_count: number,
//   is_liked: boolean
// }
//
// Think about:
// - How does groupPosts() organize posts by user?
// - What happens when posts array is empty?
// - How do you handle loading states?

import { usePosts } from "@contexts/PostsContext";
import { groupPosts } from "../utils/groupPosts";
import TimelineRiverRow from "../TimelineRiverRow";
import "./TimelineRiverFeed.scss";

function TimelineRiverFeed() {
  // Your implementation here
}

export default TimelineRiverFeed;
```

---

## Key Integration Points

### For Home/Timeline Components

**What Colin needs to know:**

- TimelineRiverFeed expects posts array with specific format
- Posts must have `type` field ('thoughts', 'media', 'milestones') for column placement
- Posts must include nested author object (username, profile_picture)
- ComposerModal calls PostsContext.createPost() to add new posts

### For Profile Components

**What Colin + Natalia need to know:**

- ProfileCard expects user object with username, bio, profile_picture
- TimelineRiver (on profile) filters posts by author
- ComposerModal on profile defaults to current user

### For Friends Page

**What Crystal needs to know:**

- (Crystal is building this page herself)

### For TopBar/Nav Components

**What team needs to know:**

- TopBar uses AuthContext.logout() for logout button
- TopBar uses ThemeContext.toggleTheme() for theme switch
- MessageModal uses MessageContext for messages
- NotificationModal will use FriendsContext for friend requests

---

## Example: Documented TimelineRiverFeed.jsx

```javascript
/**
 * COMPONENT USAGE (For Team Reference)
 *
 * Purpose: Main feed component that displays posts in a 3-column "river" layout
 * - Left column: 'thought' posts (text-only)
 * - Center column: 'media' posts (with images)
 * - Right column: 'milestone' posts (achievements)
 *
 * Data Requirements:
 * - Consumes: PostsContext via usePosts() hook
 * - Expects: posts array from context
 * - Uses: groupPosts utility (organizes posts by user+date)
 *
 * Expected Data Format (from backend):
 * {
 *   id: number,
 *   author: { id: number, username: string, profile_picture: string },
 *   type: 'thoughts' | 'media' | 'milestones',
 *   content: string,
 *   media_url: string | null,  // NOT 'image'!
 *   created_at: ISO timestamp string (e.g., "2024-12-19T10:00:00Z"),
 *   parent: number | null,
 *   parent_id: number | null,
 *   likes_count: number,
 *   reply_count: number,      // NOT 'comment_count'!
 *   shares_count: number,
 *   is_liked: boolean
 * }
 *
 * Integration Points:
 * - Used by: Home.jsx (main feed page)
 * - Renders: TimelineRiverRow components for each user/date group
 * - Calls: PostsContext.fetchPosts() on component mount
 * - groupPosts.js uses `orderId` field for sorting (NOT `oderId` - typo fixed Jan 2025)
 *
 * TimelineRiverRow Architecture (Jan 2025 Refactor):
 * - PostCard.jsx handles individual post rendering (like, share, comment, edit, delete)
 * - SmartDeck.jsx handles carousel deck with prev/next navigation
 * - ThreadView.jsx handles inline replies thread display
 * - MobileTabNav.jsx handles mobile category tab switching
 *
 * Import Pattern (Use Vite Path Aliases):
 * import { usePosts } from '@contexts/PostsContext';
 * import { HeartIcon, CommentIcon } from '@assets/icons';
 *
 * Team Integration:
 * - Colin: Build PostsContext to provide the posts array in above format
 * - Colin: Build postsService to fetch from /api/posts/
 * - Colin: Ensure backend /api/posts/ returns posts matching above format
 * - Natalia: Ensure author data includes id, username, profile_picture
 *
 * DO NOT MODIFY THIS FILE
 * This is Pablo's complete UI implementation. Your job is to build the
 * backend and contexts that provide data in the format this component expects.
 */

import { usePosts } from "@contexts/PostsContext";
import { groupPosts } from "../utils/groupPosts";
import TimelineRiverRow from "../TimelineRiverRow";
import "./TimelineRiverFeed.scss";

// ... Pablo's complete implementation (DO NOT MODIFY) ...
```

---

## Your Task Checklist

- [ ] Rebuild all Home page JSX components from pseudocode
- [ ] Rebuild all Profile page JSX components from pseudocode
- [ ] Rebuild TopBar and SideNav JSX from pseudocode
- [ ] Rebuild About, Landing, NotFound page JSX from pseudocode
- [ ] Rebuild App.jsx from pseudocode
- [ ] Rebuild MessageContext.jsx from pseudocode
- [ ] Create meaningful commits showing your progress
- [ ] Create PR with your contributions

---

## Design System (PROVIDED - Reference for Implementation)

Your global styles are the team's design foundation. Make sure they know:

**Variables Available** (`_variables.scss`):

- Colors: `--bg-primary`, `--text-primary`, `--color-accent`, etc.
- Spacing: `--space-xs`, `--space-sm`, `--space-md`, `--space-lg`, etc.
- Typography: `--font-main`, `--font-title`, `--font-size-body`, etc.
- Theme switching: CSS variables change automatically based on `data-theme='light'` or `data-theme='dark'`

**Mixins Available** (`_mixins.scss`):

- `@include glass-card` - Glassmorphic card background
- `@include neon-glow($color)` - Cyberpunk glow effect
- `@include fade-in($duration)` - Fade in animation
- Many more...

**Pre-built Button Classes** (`_buttons.scss`):

- `.btn-primary` - Main action button
- `.btn-secondary` - Secondary action button
- `.btn-danger` - Destructive action button
- All buttons theme-aware (adapt to light/dark mode)

**Team Usage:**

- Natalia: Use these for Login/Signup styling
- Crystal: Use these for Friends page styling
- Tito: Use these for ThemeToggle styling

---

## Important Reminders

1. **Don't modify your implementation** - just add documentation
2. **Be specific about data formats** - team needs exact field names and types
3. **Highlight critical integration points** - where your UI calls context functions
4. **Note column logic** - post type determines Timeline River column
5. **Reference design system** - so team knows what's available for their components
