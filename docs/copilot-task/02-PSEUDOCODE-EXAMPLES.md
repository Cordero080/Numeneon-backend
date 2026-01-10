This file contains all 12 detailed examples that Copilot praised as "Chef's Kiss" - the templates for every file type.

markdown# NUMENEON TEAM REBUILD - Part 2: Pseudocode Examples

## HOW TO USE THESE FILES

**⚠️ READ [00-START-HERE.md](./00-START-HERE.md) FIRST if you haven't already!**

This is Part 2 of 5. Read these files in order:

0. `00-START-HERE.md` - Quick overview, workflow, FAQ
1. `01-CONTEXT-AND-STRATEGY.md` - Background, strategy, assignments
2. `02-PSEUDOCODE-EXAMPLES.md` ← YOU ARE HERE
3. `03-BACKEND-INSTRUCTIONS.md` - Backend pseudocode tasks
4. `04-FRONTEND-INSTRUCTIONS.md` - Frontend pseudocode tasks
5. `05-TEAM-PLAN-FILES.md` - Team markdown file templates

---

## EXAMPLE 1: Backend Model File

```python
"""
TODO: Create the Post model - this is the core content type for NUMENEON

A post is something a user creates. It can be:
- A 'thoughts' (text-only, goes in left column of Timeline River)
- A 'media' post (has an image, goes in center column)
- A 'milestones' (achievement post, goes in right column)

Posts can also be replies to other posts (nested conversations/threads).

Fields you need:
- author: Who created it? (relationship to User model)
- type: What kind of post? (must be one of: 'thoughts', 'media', 'milestones')
- content: The actual text (can be blank for media-only posts)
- media_url: Optional URL to media (URLField, NOT ImageField!)
- parent: Is this a reply to another post? (can be null)
- created_at: When was it made? (should auto-set on creation)
- likes_count: Number of likes (PositiveIntegerField, default 0)
- reply_count: Number of replies (PositiveIntegerField, default 0) - NOT comment_count!
- shares_count: Number of shares (PositiveIntegerField, default 0)

Engagement metrics are used by Pablo's ProfileCard analytics:
- Wave chart calculates weekly engagement totals
- Heatmap shows posting frequency calendar
- All three metrics contribute to engagement visualization

Integration points:
- Frontend TimelineRiverFeed (Pablo's component) expects posts with these exact fields
- PostsContext (Colin builds this too) will fetch and manage these
- Each post type renders in different column of Pablo's Timeline River UI

Think about:
- How do you make a field optional vs required in Django?
- How do you create a relationship where a Post can reply to another Post?
- What's the difference between blank=True and null=True?
- For the 'type' field, how do you restrict it to only 3 specific values?
- Why would image need both blank=True AND null=True?

Hint: Django has a built-in User model you can import from django.contrib.auth.models
Hint: For the 'type' field, look up Django's 'choices' parameter
Hint: For self-referential relationships (parent post), use ForeignKey('self', ...)
Hint: For created_at, look up auto_now_add parameter
"""

from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    # Your code here
    pass
```

---

## EXAMPLE 2: Backend View File

```python
"""
TODO: Create Posts API Views - handles all HTTP requests for posts

This file contains the views that respond to frontend API calls.
Your PostViewSet should handle:
- GET /api/posts/ - List all posts
- POST /api/posts/ - Create new post
- GET /api/posts/:id/ - Get single post
- PATCH /api/posts/:id/ - Update post
- DELETE /api/posts/:id/ - Delete post
- GET /api/posts/:id/replies/ - Get all replies to a post

Integration points:
- Frontend postsService.js (Colin builds this too) calls these endpoints
- PostsContext uses the service to manage state
- Pablo's Timeline components display the returned data

Expected response format for GET /api/posts/:
[
  {
    "id": 1,
    "author": {
      "id": 5,
      "username": "alice",
      "first_name": "Alice",
      "last_name": "Smith"
    },
    "type": "thoughts",
    "content": "This is a post",
    "media_url": null,
    "parent": null,
    "parent_id": null,
    "created_at": "2024-12-19T10:00:00Z",
    "likes_count": 42,
    "reply_count": 7,
    "shares_count": 3,
    "is_liked": false
  }
]

IMPORTANT: Engagement fields (likes_count, reply_count, shares_count)
are REQUIRED by Pablo's ProfileCard.jsx for analytics visualizations.

Think about:
- How do you restrict endpoints to authenticated users only?
- Should you use APIView, ViewSet, or ModelViewSet? (Hint: ModelViewSet is easiest)
- How do you include nested author data (not just author ID)?
- For the /replies/ endpoint, how do you filter posts by parent ID?
- What HTTP methods should be allowed? (GET, POST, PATCH, DELETE)

Hint: Django REST Framework's ModelViewSet gives you CRUD for free
Hint: Use serializers to format the response (you'll build serializers.py next)
Hint: For nested author data, your serializer needs a nested UserSerializer
Hint: Look up @action decorator for custom endpoints like /replies/
"""

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Post
from .serializers import PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    # Your code here
    pass
```

---

## EXAMPLE 3: Frontend Context File

```javascript
// TODO: Create PostsContext - manages all post data for the app
//
// This context is the "source of truth" for posts. Any component that needs
// to display posts (Home, Profile) or create/edit/delete posts (ComposerModal)
// gets data from here.
//
// State you need:
// - posts: Array of post objects from the API
// - loading: Boolean - are we fetching data?
// - error: String - any error messages from API calls
//
// Functions you need to provide:
// - fetchPosts(): Get all posts from /api/posts/ and store them
// - createPost(postData): Send new post to API, add to local state
// - updatePost(id, updates): Edit existing post
// - deletePost(id): Remove post from API and local state
// - getReplies(parentId): Get all replies to a specific post
//
// Integration points:
// - Uses postsService.js (you're building this too) for actual API calls
// - Wraps App.jsx so all routes can access posts
// - Pablo's Home.jsx and Profile.jsx consume this to display posts
// - Pablo's ComposerModal uses createPost() when user submits
// - Pablo's TimelineRiverFeed expects posts array in specific format
//
// Post object format (from backend):
// {
//   id: number,
//   author: { id: number, username: string, first_name: string, last_name: string },
//   type: 'thoughts' | 'media' | 'milestones',
//   content: string,
//   media_url: string | null,
//   created_at: ISO timestamp string,
//   parent: number | null,
//   parent_id: number | null,
//   likes_count: number,      // REQUIRED for ProfileCard analytics
//   reply_count: number,      // REQUIRED for ProfileCard analytics (NOT comment_count!)
//   shares_count: number,     // REQUIRED for ProfileCard analytics
//   is_liked: boolean         // Has current user liked this post?
// }
//
// NOTE: Engagement fields (likes_count, reply_count, shares_count) are
// required by Pablo's ProfileCard.jsx for the analytics visualizations:
// - Wave chart uses weekly engagement totals
// - Heatmap shows posting frequency
// - Post type breakdown counts by type
//
// Think about:
// - How do you update state after a successful API call?
// - What happens if the API call fails? Should error state be set?
// - Should you refetch all posts after creating one, or just add new post to array?
// - When should fetchPosts() run? (Hint: useEffect on component mount)
// - How do you provide this state to all child components?
// - Should posts be sorted? (By date? Newest first?)
//
// Hint: Use createContext() to create the context
// Hint: Create a custom hook like useAuth() that components can use
// Hint: Look at AuthContext.jsx (Natalia builds) as a reference for structure
// Hint: For async operations, use async/await for cleaner code

import { createContext, useState, useEffect, useContext } from "react";
import * as postsService from "../services/postsService";

export const PostsContext = createContext();

export function PostsProvider({ children }) {
  // Your code here
}

export function usePosts() {
  // Your code here - custom hook to consume context
}
```

---

## EXAMPLE 4: Frontend Service File

```javascript
// TODO: Create Posts Service - handles all API calls related to posts
//
// This file contains functions that make HTTP requests to the backend posts API.
// It's the bridge between PostsContext (state management) and the Django backend.
//
// Functions you need:
// - getPosts(): Fetch all posts from GET /api/posts/
// - getPost(id): Fetch single post from GET /api/posts/:id/
// - getReplies(parentId): Fetch replies from GET /api/posts/:id/replies/
// - createPost(postData): Create new post via POST /api/posts/
// - updatePost(id, updates): Update post via PATCH /api/posts/:id/
// - deletePost(id): Delete post via DELETE /api/posts/:id/
//
// Integration points:
// - Uses apiClient.js (Tito builds this) for axios instance with JWT auth
// - PostsContext (you're building this too) calls these functions
// - All functions should return the response data, not the full axios response
//
// Expected input for createPost():
// {
//   type: 'thoughts' | 'media' | 'milestones',
//   content: string,
//   image: File | null (for media posts),
//   parent: number | null (for replies)
// }
//
// Expected return format (matches backend response):
// Single post: { id, author: {...}, type, content, image, parent, created_at }
// Multiple posts: [ {...}, {...}, ... ]
//
// Think about:
// - Do you need to handle auth tokens? (No! apiClient handles that)
// - Should these functions handle errors or throw them? (Throw them, let context handle)
// - For image uploads, how should data be formatted? (FormData for multipart/form-data)
// - Should you validate input before sending to API?
// - What if the API returns an error? (Let it throw, context will catch)
//
// Hint: Import apiClient and use apiClient.get(), apiClient.post(), etc.
// Hint: Use async/await for cleaner promise handling
// Hint: Return response.data, not the whole response object
// Hint: For image uploads, create FormData and append fields

import apiClient from "./apiClient";

export async function getPosts() {
  // Your code here
}

export async function createPost(postData) {
  // Your code here
}

export async function updatePost(id, updates) {
  // Your code here
}

export async function deletePost(id) {
  // Your code here
}

export async function getReplies(parentId) {
  // Your code here
}
```

---

## EXAMPLE 5: Simple Frontend Component (JSX)

```javascript
// TODO: Create Login component - user authentication form
//
// This is where existing users sign in to NUMENEON.
//
// Component should:
// 1. Display a form with username/email and password fields
// 2. Call AuthContext.login() when user submits
// 3. Redirect to /home on successful login
// 4. Display error messages if login fails (wrong password, network error, etc.)
//
// State you need:
// - formData: Object with username and password fields
// - Or separate username and password state (your choice)
//
// Integration points:
// - Uses AuthContext's login() function (Natalia builds AuthContext)
// - Uses React Router's useNavigate for redirect after login
// - Links to Signup page (/signup) for new users
// - Uses Pablo's design system for styling (glass-card mixin, variables)
//
// User flow:
// 1. User types username and password
// 2. User clicks submit button
// 3. Component calls AuthContext.login({ username, password })
// 4. If successful, navigate to /home
// 5. If failed, show error message from AuthContext
//
// Think about:
// - How do you handle form input changes? (controlled inputs with onChange)
// - What happens when user clicks submit? (preventDefault to stop page refresh!)
// - When should you navigate to /home? (after successful login, in useEffect?)
// - How do you show loading state while waiting for API response?
// - Should error message clear when user starts typing again? (better UX)
// - How do you access AuthContext? (useAuth hook)
//
// STYLING:
// - Import './Login.scss' for component-specific styles
// - Pablo's global design system has variables and mixins you can use
// - Check src/styles/_variables.scss for color/spacing variables
// - Check src/styles/_mixins.scss for glass-card, neon-glow, etc.
// - You'll write Login.scss (separate pseudocode for that file)
//
// Hint: Use async/await for the login call
// Hint: Store username/password in a single formData object for cleaner code
// Hint: useNavigate() hook from react-router-dom for programmatic navigation
// Hint: Look at Signup.jsx structure (you'll build that too) - similar pattern
//
// ICONS:
// - All icons are in frontend/src/assets/icons/ (modular by category)
// - Import what you need: import { LoginIcon, EyeIcon } from '../../assets/icons'
// - Use with size prop: <LoginIcon size={20} className="icon" />
// - Find icons by category: navigation.jsx, actions.jsx, ui.jsx, etc.
// - Full icon list: docs/refactoring/SVG-Icons-Refactor.md

import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext";
import { LoginIcon, EyeIcon, EyeOffIcon } from "../../assets/icons";
import "./Login.scss";

export default function Login() {
  // Your code here
}
```

---

## EXAMPLE 6: Simple Component SCSS File

```scss
// TODO: Style the Login page
//
// IMPORTANT: Pablo's design system is already built!
// - Variables: Use var(--color-primary), var(--spacing-lg), etc.
//   Check src/styles/_variables.scss to see all available variables
// - Mixins: Use @include glass-card, @include neon-glow, etc.
//   Check src/styles/_mixins.scss to see all available mixins
// - Buttons: Classes already exist in _buttons.scss (btn-primary, btn-secondary)
// - Theme: Light/dark mode variables handled automatically
//
// What you need to style:
// - .login-container: Main page wrapper (full viewport height, centered)
// - .login-form: Form container (use glass-card mixin for cyberpunk look)
// - .form-group: Individual input groups (spacing between fields)
// - .error-message: Error display styling (use color-danger variable)
// - .link-text: Link to signup page (subtle styling)
//
// Layout requirements:
// - Center the form on the page (vertically and horizontally)
// - Use consistent spacing from Pablo's spacing variables
// - Form should be responsive (look good on mobile AND desktop)
// - Don't override button styles - they're styled globally already
//
// Think about:
// - How do you center content both vertically and horizontally? (flexbox)
// - Should inputs have focus states? (yes! use neon-glow mixin on :focus)
// - What color should error messages be? (check variables for --color-danger)
// - How wide should the form be? (max-width for desktop, full-width on mobile)
// - Should the background be the page-level background or custom?
//
// Example of using Pablo's design system:
// .login-form {
//   background: var(--color-bg-secondary);
//   padding: var(--spacing-xl);
//   @include glass-card;
//   @include neon-glow;
// }
//
// Responsive example:
// @media (max-width: 768px) {
//   .login-container {
//     padding: var(--spacing-md);
//   }
// }

@use "../../styles/variables" as *;
@use "../../styles/mixins" as *;

.login-container {
  // Your code here
}

.login-form {
  // Your code here
}

.form-group {
  // Your code here
}

.error-message {
  // Your code here
}

.link-text {
  // Your code here
}
```

---

## EXAMPLE 7: Utility Function File (Reference Only)

```javascript
/**
 * UTILITY REFERENCE (Pablo's Implementation - DO NOT MODIFY)
 *
 * Purpose: Groups posts by USER ONLY for Timeline River "space economy" layout
 *
 * KEY DESIGN: Each user = ONE row (not one row per date!)
 * This enables carousel navigation - all posts from same user in one place
 *
 * Input format (array of posts from API):
 * [
 *   { id: 1, author: { id: 5, username: "alice" }, created_at: "2024-12-19T10:00:00Z", type: "thoughts", ... },
 *   { id: 2, author: { id: 5, username: "alice" }, created_at: "2024-12-15T14:00:00Z", type: "media", ... },
 *   { id: 3, author: { id: 5, username: "alice" }, created_at: "2024-11-20T09:00:00Z", type: "milestones", ... },
 *   { id: 4, author: { id: 7, username: "bob" }, created_at: "2024-12-18T09:00:00Z", type: "thoughts", ... }
 * ]
 *
 * Output format (grouped by userId only):
 * {
 *   "5": {
 *     user: { id: 5, name: "alice", avatar: "AL" },
 *     thoughts: [post1],
 *     media: [post2],
 *     milestones: [post3],
 *     mostRecentDate: Date("2024-12-19")
 *   },
 *   "7": {
 *     user: { id: 7, name: "bob", avatar: "BO" },
 *     thoughts: [post4],
 *     media: [],
 *     milestones: [],
 *     mostRecentDate: Date("2024-12-18")
 *   }
 * }
 *
 * WHY USER-ONLY GROUPING?
 * - Space Economy: See 10 users at a glance vs scrolling 30+ rows
 * - Carousel Arrows: Need 3+ posts per type to show navigation arrows
 * - Context: All of a user's content together, not scattered by date
 *
 * Integration points:
 * - Called by Pablo's TimelineRiverFeed component
 * - Input comes from PostsContext (Colin's array of posts)
 * - Output feeds TimelineRiverRow components with carousel state
 * - Row header shows "Last active: [mostRecentDate]"
 *
 * Team Reference:
 * - Colin: Your PostsContext provides the input array
 * - seed_posts.py: Creates 9 posts per user (3 per type) for carousel testing
 * - This function transforms data for Pablo's UI display
 *
 * See also: docs/features/RiverTimeline.md for full documentation
 */

// ... Pablo's complete implementation follows (DO NOT MODIFY) ...
```

---

## EXAMPLE 8: Simple Export File (index.js)

```javascript
// TODO: Export the Login component
//
// This is a barrel export that makes imports cleaner elsewhere in the app.
//
// Without this file:
// import Login from './Login/Login.jsx'
//
// With this file:
// import Login from './Login'
//
// Why? It's a common React pattern that keeps import paths shorter and cleaner.
//
// Just export the default export from Login.jsx

export { default } from "./Login";
```

---

## EXAMPLE 9: Using the Icon Library

```javascript
// REFERENCE: How to use NUMENEON's modular icon system
//
// All 70+ SVG icons are organized by category in frontend/src/assets/icons/
//
// ICON CATEGORIES (browse these files to find what you need):
// ├── navigation.jsx  → TargetReticleIcon, ChevronLeftIcon, BackIcon, FlipIcon, LoginIcon, LogoutIcon
// ├── user.jsx        → UserIcon, GlobeIcon, LockIcon, FriendsIcon, HexProfileIcon, VisibilityIcon (smart)
// ├── engagement.jsx  → HeartIcon, HeartFilledIcon, HeartDynamicIcon (smart), CommentIcon, ShareIcon, BookmarkIcon
// ├── actions.jsx     → EditIcon, TrashIcon, CloseIcon, PlusIcon, CheckIcon, SendIcon, ShatterIcon
// ├── media.jsx       → ImageIcon, ExpandIcon, MaximizeIcon, MinimizeIcon
// ├── ui.jsx          → SettingsIcon, EyeIcon, EyeOffIcon, MoreIcon, GridIcon, ClockIcon
// ├── sidenav.jsx     → HexHomeIcon, SignalIcon, NetworkIcon, CircuitInfoIcon
// ├── analytics.jsx   → BoltIcon, BarChartIcon, ShieldIcon, ActivityIcon, GraphLineIcon
// ├── profile.jsx     → LocationIcon, LinkIcon, CalendarIcon, StarIcon, MilestoneIcon
// ├── messaging.jsx   → MessageBubbleIcon, MessageLineIcon, EmojiIcon, ThoughtBubbleIcon
// └── misc.jsx        → MusicIcon, MapPinIcon, PostTriangleIcon
//
// SMART ICONS (conditional rendering based on props):
// - VisibilityIcon: Automatically shows LockIcon/GlobeIcon/FriendsIcon based on visibility prop
// - HeartDynamicIcon: Toggles between filled/outline based on filled prop
//
// HOW TO IMPORT:
// Method 1 - From barrel export (recommended):
import { HeartIcon, CommentIcon, TrashIcon } from "../../assets/icons";

// Method 2 - From specific category file (tree-shakeable):
import { HeartIcon } from "../../assets/icons/engagement";
import { TrashIcon } from "../../assets/icons/actions";

// HOW TO USE:
// Every icon accepts these props:
// - size: number (controls both width & height)
// - className: string (for CSS styling)
// - ...props: any other props pass through (onClick, aria-label, etc.)

function MyComponent() {
  return (
    <div>
      {/* Basic usage */}
      <HeartIcon size={18} />

      {/* With className for styling */}
      <CommentIcon size={20} className="action-icon" />

      {/* With click handler */}
      <TrashIcon size={16} className="delete-btn" onClick={handleDelete} />

      {/* HeartDynamicIcon is special - has filled prop */}
      <HeartDynamicIcon
        size={18}
        filled={isLiked} // true = filled, false = outline
        fillColor="#3b82f6" // color when filled
        strokeColor="rgba(201,168,255,0.5)" // color when outline
      />
    </div>
  );
}

// FINDING THE RIGHT ICON:
// 1. Think about what category it belongs to (engagement? actions? ui?)
// 2. Open that category file and browse the exports
// 3. Or check docs/refactoring/SVG-Icons-Refactor.md for full inventory
//
// FULL DOCUMENTATION: docs/refactoring/SVG-Icons-Refactor.md
```

---

## EXAMPLE 10: Collaborative File (Backend URLs)

```python
"""
TODO: Root URL configuration for NUMENEON backend

This file imports and includes all the app-specific URL patterns.
Each backend team member adds their app's URLs here.

COLLABORATIVE FILE - Each person adds ONE line:
- Natalia: Users/auth URLs
- Colin: Posts URLs
- Crystal: Friends URLs

Pattern: path('api/[app-name]/', include('[app-name].urls'))
"""

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # TODO (Natalia): Add users app URLs
    # Uncomment and complete this line:
    # path('api/auth/', include('users.urls')),

    # TODO (Colin): Add posts app URLs
    # Uncomment and complete this line:
    # path('api/posts/', include('posts.urls')),

    # TODO (Crystal): Add friends app URLs
    # Uncomment and complete this line:
    # path('api/friends/', include('friends.urls')),
]
```

---

## EXAMPLE 11: Collaborative File (Frontend Context Exports)

```javascript
// TODO: Export all context providers and hooks
//
// This file makes it easy to import multiple contexts in one line.
//
// COLLABORATIVE FILE - Each context owner adds their exports:
// - Natalia: AuthContext, useAuth
// - Colin: PostsContext, usePosts
// - Crystal: FriendsContext, useFriends
// - Tito: ThemeContext, useTheme
// - Pablo: MessageContext, useMessage
//
// Usage elsewhere:
// import { useAuth, usePosts, useFriends } from '../contexts'

// TODO (Natalia): Export AuthContext
// Uncomment and complete this line:
// export { AuthProvider, useAuth } from './AuthContext';

// TODO (Colin): Export PostsContext
// Uncomment and complete this line:
// export { PostsProvider, usePosts } from './PostsContext';

// TODO (Crystal): Export FriendsContext
// Uncomment and complete this line:
// export { FriendsProvider, useFriends } from './FriendsContext';

// TODO (Tito): Export ThemeContext
// Uncomment and complete this line:
// export { ThemeProvider, useTheme } from './ThemeContext';

// TODO (Pablo): Export MessageContext
// Already built - uncomment this line:
// export { MessageProvider, useMessage } from './MessageContext';
```

---

## EXAMPLE 12: Pablo's Component (Usage Comment Only)

```javascript
/**
 * COMPONENT USAGE (For Team Reference)
 *
 * Purpose: Main feed component that displays posts in a 3-column "river" layout
 * - Left column: 'thoughts' posts (text-only)
 * - Center column: 'media' posts (with images)
 * - Right column: 'milestones' posts (achievements)
 *
 * SPACE ECONOMY DESIGN:
 * - Each user = ONE row (not grouped by date!)
 * - All posts from same user collected in single row
 * - Carousel arrows navigate between posts of same type
 * - Row header shows "Last active: [date]" instead of specific date
 *
 * Data Requirements:
 * - Consumes: PostsContext via usePosts() hook
 * - Expects: posts array from context
 * - Uses: groupPosts utility (Pablo's utility) to organize posts by USER
 *
 * Post Format Expected (from backend):
 * {
 *   id: number,
 *   author: { id: number, username: string, first_name: string, last_name: string },
 *   type: 'thoughts' | 'media' | 'milestones',
 *   content: string,
 *   media_url: string | null,
 *   created_at: ISO timestamp string (e.g., "2024-12-19T10:00:00Z"),
 *   parent: number | null,
 *   parent_id: number | null,
 *   likes_count: number,
 *   reply_count: number,
 *   shares_count: number,
 *   is_liked: boolean
 * }
 *
 * Integration Points:
 * - Used by: Home.jsx (Pablo's page component)
 * - Renders: TimelineRiverRow components (Pablo's component) for each user
 * - Calls: PostsContext.fetchPosts() on component mount
 * - Carousel arrows appear when user has 3+ posts of same type
 *
 * TimelineRiverRow Architecture (Refactored Jan 2025):
 * - Main orchestrator in TimelineRiverRow.jsx
 * - Sub-components: PostCard, SmartDeck, ThreadView, MobileTabNav
 * - Utilities: timeFormatters.js (formatRelativeTime), groupPosts.js
 *
 * Team Integration:
 * - Colin: Build PostsContext to provide posts array in above format
 * - Colin: Build postsService with likePost() and sharePost() functions
 * - Colin: Ensure backend /api/posts/ returns posts with is_liked boolean
 * - Natalia: Ensure author data includes id, username, avatar
 * - seed_posts.py: Creates 9 posts per user (3 per type) for carousel testing
 *
 * DO NOT MODIFY THIS FILE
 * This is Pablo's complete UI implementation. Your job is to build the
 * backend and contexts that provide data in the format this component expects.
 */

import { usePosts } from "../../../contexts/PostsContext";
import { groupPosts } from "../utils/groupPosts";
import TimelineRiverRow from "./TimelineRiverRow";
import "./TimelineRiverFeed.scss";

// ... Pablo's complete implementation follows (DO NOT MODIFY) ...
```

```

---

## IMPORTANT: Placeholder Components (Team Awareness)

### Engagement Ring on ProfileCard Avatar

**Location:** `frontend/src/components/pages/Profile/ProfileCardFront.jsx` (lines 78-101)

**Current State:** The engagement ring around the profile avatar is a **PLACEHOLDER** with decorative CSS animation. It fills to ~12.5% on page load as a visual demonstration.

**What it does now:**

- SVG circle with `strokeDasharray="377"` and animated `strokeDashoffset` (377→330)
- Ring fills slightly on page load via CSS animation
- Purely decorative - no real data backing it

**Why it's a placeholder:**
The ring is designed to eventually show real engagement data, but requires backend features not yet built.

**Do NOT:**

- Assume the ring shows real data
- Try to "fix" why it only fills partially
- Connect it to existing engagement fields without implementing proper backend

**Stretch Goal Options (see `docs/stretch-goals/EngagementRing.md`):**

1. Profile Completion % - Easiest, based on filled profile fields
2. Weekly Activity - Based on posts/likes this week
3. XP/Level System - Gamification, most complex
4. Engagement Score - Combined metrics like overall user engagement

**Team Action:** When implementing, see `EngagementRing.md` stretch goal document for full implementation checklist.

---

**NEXT:** Read `03-BACKEND-INSTRUCTIONS.md` for specific backend implementation tasks
```
