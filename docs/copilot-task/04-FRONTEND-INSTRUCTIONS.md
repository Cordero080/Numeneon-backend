File 4 of 5:
Name it: 04-FRONTEND-INSTRUCTIONS.md
This file contains specific instructions for adding pseudocode to frontend files (contexts, services, simple UI components) and usage comments to Pablo's UI files.

markdown# NUMENEON TEAM REBUILD - Part 4: Frontend Instructions

## HOW TO USE THESE FILES

**⚠️ READ [00-START-HERE.md](./00-START-HERE.md) FIRST if you haven't already!**

This is Part 4 of 5. Read these files in order:

0. `00-START-HERE.md` - Quick overview, workflow, FAQ
1. `01-CONTEXT-AND-STRATEGY.md` - Background, strategy, assignments
2. `02-PSEUDOCODE-EXAMPLES.md` - All 12 example templates
3. `03-BACKEND-INSTRUCTIONS.md` - Backend pseudocode tasks
4. `04-FRONTEND-INSTRUCTIONS.md` ← YOU ARE HERE
5. `05-TEAM-PLAN-FILES.md` - Team markdown file templates

---

## BRANCH: `team-shell-frontend`

Before starting:

1. Create branch `team-shell-frontend` from main
2. Delete the entire `backend/` folder
3. Keep `frontend/` folder with all files
4. Apply pseudocode/usage comments as instructed below

---

## VITE PATH ALIASES (CONFIGURED)

**NUMENEON uses Vite path aliases to simplify imports and improve developer experience.**

Instead of messy relative paths like `../../../../../../../assets/icons`, use clean aliases:

```javascript
// Configured in vite.config.js:
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

    // Page-specific aliases (most commonly imported)
    '@Home': './src/components/pages/Home',
    '@Profile': './src/components/pages/Profile',
  }
}
```

### Import Examples

**Icons:**

```jsx
// ✅ RECOMMENDED (using alias)
import { HeartIcon, CloseIcon, CommentIcon } from "@assets/icons";

// ✅ ALSO GOOD (category-specific)
import { HeartIcon } from "@assets/icons/engagement";

// ❌ AVOID (relative paths - verbose and fragile)
import { HeartIcon } from "../../../../../../../assets/icons";
```

**Contexts:**

```jsx
// ✅ RECOMMENDED
import { useAuth } from "@contexts/AuthContext";
import { usePosts } from "@contexts/PostsContext";

// ❌ AVOID
import { useAuth } from "../../../contexts/AuthContext";
```

**Services:**

```jsx
// ✅ RECOMMENDED
import apiClient from "@services/apiClient";
import postsService from "@services/postsService";

// ❌ AVOID
import apiClient from "../../../services/apiClient";
```

**Components:**

```jsx
// ✅ RECOMMENDED
import Login from "@components/pages/Login";
import TopBar from "@components/layout/TopBar";

// ❌ AVOID
import Login from "../../pages/Login";
```

**When writing pseudocode in this file, use path aliases in all import examples!**

---

## FRONTEND FILE CATEGORIES

**ALL frontend JSX files become pseudocode** (including Pablo's). Everyone rebuilds from pseudocode.

**SCSS files are PROVIDED** - team writes JSX only.

### Files by Owner:

- **Natalia:** AuthContext, Login, Signup, ProtectedRoute (8 files)
- **Colin:** PostsContext, postsService, ComposerModal, DeleteConfirmModal (8 files)
- **Crystal:** FriendsContext, friendsService, Friends page (5 files)
- **Tito:** apiClient, ThemeContext, ThemeToggle, main.jsx (6 files)
- **Pablo:** Timeline system, ProfileCard, MediaLightbox, Layout (~35 JSX files)
- **Collaborative:** contexts/index.js (everyone adds their export)

---

## CATEGORY A: FULL PSEUDOCODE FILES

### NATALIA'S FRONTEND FILES

#### `frontend/src/contexts/AuthContext.jsx`

```javascript
// TODO: Create AuthContext - manages user authentication state
//
// This context is the "source of truth" for authentication. Every component
// that needs to know if a user is logged in, who they are, or needs to
// log in/out/signup gets that from here.
//
// State you need:
// - user: Object with user data (id, username, email, first_name, last_name, profile) or null if not logged in
// - isLoading: Boolean - are we checking auth status? (important for initial load)
// - isAuthenticated: Boolean - is user logged in?
// - error: String - any error messages from auth operations
//
// Functions you need to provide:
// - login(credentials): Send EMAIL/password to API, store tokens, set user
// - signup(userData): Create account, auto-login, redirect
// - logout(): Clear tokens and user state
// - checkAuth(): Check if token exists and is valid, fetch current user
//
// IMPORTANT: Login uses EMAIL, not username!
// Frontend sends: { email: "user@example.com", password: "..." }
// Backend returns: { access: "...", refresh: "..." }
//
// Integration points:
// - Uses apiClient.js (Tito builds) for HTTP requests
// - Wraps entire app in App.jsx (or main.jsx)
// - Login.jsx and Signup.jsx call login() and signup()
// - ProtectedRoute.jsx checks if user exists
// - TopBar.jsx displays current user info
// - PostsContext and FriendsContext check isAuthenticated before fetching
//
// User object format (from backend /api/auth/me/):
// {
//   id: number,
//   username: string,
//   email: string,
//   first_name: string,
//   last_name: string,
//   profile: {
//     id: number,
//     bio: string,
//     avatar: string | null,
//     location: string,
//     website: string
//   }
// }
//
// Token storage:
// - Store JWT access token AND refresh token in localStorage
// - Keys: 'accessToken' and 'refreshToken'
// - On login: save both tokens, then fetch user with /api/auth/me/
// - On app load: check localStorage for accessToken, if exists fetch user
// - On logout: clear both tokens from localStorage, set user to null
// - On 401 error: token expired, apiClient handles refresh automatically
//
// Think about:
// - What happens on initial app load? (Check for existing token, fetch user)
// - How do you handle token refresh? (apiClient interceptor handles this)
// - What if /api/auth/me/ fails? (Token invalid, logout)
// - Should isLoading be true during login/signup? (Yes, for button states)
// - PostsContext and FriendsContext should wait for authLoading to be false
//
// Hint: Use createContext() and useContext()
// Hint: Create custom useAuth() hook for easy consumption
// Hint: useEffect on mount to check existing auth
// Hint: Store tokens: localStorage.setItem('accessToken', token)
// Hint: Get token: localStorage.getItem('accessToken')
// Hint: Remove tokens: localStorage.removeItem('accessToken')

import { createContext, useState, useEffect, useContext } from "react";
import apiClient from "@services/apiClient"; // Use path alias

export const AuthContext = createContext();

export function AuthProvider({ children }) {
  // Your code here
}

export function useAuth() {
  // Your code here - return useContext(AuthContext)
}
```

#### `frontend/src/components/pages/Login/Login.jsx`

```javascript
// TODO: Create Login component - user authentication form
//
// This is where existing users sign in to NUMENEON.
//
// IMPORTANT: Login uses EMAIL, not username!
//
// Component should:
// 1. Display a form with EMAIL and password fields
// 2. Call AuthContext.login() when user submits
// 3. Redirect to /home on successful login
// 4. Display error messages if login fails
//
// State you need:
// - formData: { email: '', password: '' }
// - localError: For form validation errors (optional, context has error too)
//
// Integration points:
// - Uses AuthContext's login() function and error state
// - Uses React Router's useNavigate for redirect
// - Links to /signup for new users
// - Uses Pablo's design system for styling
//
// User flow:
// 1. User enters email and password
// 2. User clicks "Log In" button
// 3. Component calls login({ email, password })
// 4. If success: redirect to /home
// 5. If error: display error message
//
// Think about:
// - How do controlled inputs work? (value + onChange)
// - What prevents page refresh on submit? (e.preventDefault())
// - When do you redirect? (After successful login, check user state)
// - How do you show loading state? (Disable button, show spinner)
// - Should you validate before submitting? (Optional but nice UX)
//
// STYLING:
// - Import './Login.scss'
// - Use Pablo's design system variables and mixins
// - Check src/styles/_variables.scss and _mixins.scss
//
// Hint: const { login, error, isLoading } = useAuth();
// Hint: const navigate = useNavigate();
// Hint: After login succeeds, navigate('/home');
// Hint: Use useEffect to redirect when user becomes truthy

import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "@contexts/AuthContext";
import "./Login.scss";

export default function Login() {
  // Your code here
}
```

#### `frontend/src/components/pages/Login/Login.scss`

```scss
// TODO: Style the Login page
//
// IMPORTANT: Pablo's design system is already built!
// You should USE it, not rebuild it.
//
// Available from Pablo's system:
// - Variables: var(--color-primary), var(--color-bg-secondary), var(--spacing-lg), etc.
// - Mixins: @include glass-card, @include neon-glow, @include scan-lines
// - Buttons: Global .btn-primary, .btn-secondary classes exist
// - Check: src/styles/_variables.scss and src/styles/_mixins.scss
//
// Classes to style:
// - .login-page: Full page container (center content)
// - .login-form: Form wrapper (use glass-card mixin)
// - .form-title: "Log In" heading
// - .form-group: Input wrapper (label + input)
// - .form-input: Text inputs (style with focus states)
// - .error-message: Error text (use --color-danger)
// - .submit-btn: Submit button (use global button class or custom)
// - .signup-link: Link to signup page
//
// Layout:
// - Center form on page (flexbox: justify-content + align-items center)
// - Form has max-width for readability
// - Responsive: full-width on mobile, constrained on desktop
//
// Cyberpunk feel:
// - Use glass-card mixin for frosted glass effect
// - Add neon-glow on focus states
// - Use color variables for consistency
//
// Example:
// .login-form {
//   @include glass-card;
//   padding: var(--spacing-xl);
//   max-width: 400px;
//   width: 100%;
// }
//
// .form-input:focus {
//   @include neon-glow;
// }

@use "../../../styles/variables" as *;
@use "../../../styles/mixins" as *;

.login-page {
  // Your code here
}

.login-form {
  // Your code here
}

.form-title {
  // Your code here
}

.form-group {
  // Your code here
}

.form-input {
  // Your code here
}

.error-message {
  // Your code here
}

.submit-btn {
  // Your code here
}

.signup-link {
  // Your code here
}
```

#### `frontend/src/components/pages/Login/index.js`

```javascript
// TODO: Export Login component (barrel export)
//
// This makes imports cleaner:
// import Login from './Login' instead of import Login from './Login/Login'

export { default } from "./Login";
```

#### `frontend/src/components/pages/Signup/Signup.jsx`

```javascript
// TODO: Create Signup component - new user registration form
//
// This is where new users create accounts for NUMENEON.
//
// Component should:
// 1. Display form with: username, email, password, confirm password
// 2. Validate passwords match before submitting
// 3. Call AuthContext.signup() when user submits
// 4. Redirect to /home on successful signup
// 5. Display error messages if signup fails
//
// State you need:
// - formData: { username: '', email: '', password: '', confirmPassword: '' }
// - localError: For validation errors (passwords don't match)
//
// Integration points:
// - Uses AuthContext's signup() function
// - Uses React Router's useNavigate for redirect
// - Links to /login for existing users
// - Uses Pablo's design system for styling
//
// Validation:
// - Username: required
// - Email: required, valid email format (optional - backend validates too)
// - Password: required, maybe minimum length
// - Confirm Password: must match password
//
// Think about:
// - What if passwords don't match? (Show error, don't submit)
// - What if username/email taken? (Backend returns error, display it)
// - Should you show password requirements? (Nice UX)
// - Clear form on error or keep values? (Keep values - less frustrating)
//
// Hint: Similar structure to Login.jsx
// Hint: Validate before calling signup()
// Hint: if (password !== confirmPassword) setLocalError('Passwords do not match')

import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuth } from "@contexts/AuthContext";
import "./Signup.scss";

export default function Signup() {
  // Your code here
}
```

#### `frontend/src/components/pages/Signup/Signup.scss`

```scss
// TODO: Style the Signup page
//
// Very similar to Login.scss - same layout, same design system usage.
// Consider if you can share styles or keep them separate (your choice).
//
// Classes to style:
// - .signup-page: Full page container
// - .signup-form: Form wrapper (glass-card)
// - .form-title: "Sign Up" heading
// - .form-group: Input wrappers
// - .form-input: Text inputs
// - .error-message: Error display
// - .submit-btn: Submit button
// - .login-link: Link to login page
//
// Same patterns as Login.scss apply here.

@use "../../../styles/variables" as *;
@use "../../../styles/mixins" as *;

.signup-page {
  // Your code here
}

.signup-form {
  // Your code here
}

// ... rest of your styles
```

#### `frontend/src/components/pages/Signup/index.js`

```javascript
// TODO: Export Signup component (barrel export)

export { default } from "./Signup";
```

#### `frontend/src/components/ui/ProtectedRoute.jsx`

```javascript
// TODO: Create ProtectedRoute component - guards authenticated routes
//
// This component wraps routes that require login.
// If user is not authenticated, redirect to /login.
// If user is authenticated, render the child component.
//
// Usage in App.jsx:
// } />
//
// Component should:
// 1. Check if user is logged in (via AuthContext)
// 2. If loading, show loading state (spinner or nothing)
// 3. If not logged in, redirect to /login
// 4. If logged in, render children
//
// Props:
// - children: The component to render if authenticated
//
// Integration points:
// - Uses AuthContext's user and loading state
// - Uses React Router's Navigate component for redirect
// - Wraps protected routes in App.jsx
//
// Think about:
// - What if auth is still loading? (Don't redirect yet!)
// - What's the difference between Navigate and useNavigate? (Navigate is component)
// - Should you preserve the intended destination? (Advanced: location state)
//
// Hint: const { user, loading } = useAuth();
// Hint: if (loading) return Loading... or null
// Hint: if (!user) return
// Hint: return children;

import { Navigate } from "react-router-dom";
import { useAuth } from "@contexts/AuthContext";

export default function ProtectedRoute({ children }) {
  // Your code here
}
```

---

### COLIN'S FRONTEND FILES

#### `frontend/src/contexts/PostsContext.jsx`

```javascript
// TODO: Create PostsContext - manages all post data for the app
//
// This context is the "source of truth" for posts. Components that display
// or modify posts get their data and functions from here.
//
// State you need:
// - posts: Array of post objects from the API
// - isLoading: Boolean - are we fetching?
// - error: String - any error messages
//
// Functions you need to provide:
// - fetchPosts(): Get all posts from API, store in state
// - fetchPostsByUsername(username): Get posts by a specific user (for profile pages)
// - createPost(postData): Create new post, add to state
// - updatePost(id, updates): Edit existing post
// - deletePost(id): Remove post from API and state
// - fetchReplies(postId): Get all replies for a post
// - createReply(parentId, content): Create a reply to a post
// - likePost(id): Toggle like on a post, update state with new likes_count
// - sharePost(id): Increment share count, update state with new shares_count
//
// IMPORTANT: Wait for AuthContext to finish loading before fetching!
// - Import useAuth and check authLoading and isAuthenticated
// - useEffect should depend on [user, authLoading, isAuthenticated]
//
// fetchPostsByUsername behavior:
// - Calls postsService.getByUsername(username)
// - Merges returned posts into existing posts (avoid duplicates)
// - Returns { success: true, data: [...] } or { success: false, error: "..." }
//
// likePost behavior:
// - Calls postsService.like(id) which hits POST /api/posts/:id/like/
// - Backend returns updated post with new likes_count and is_liked
// - Update that post in local state so UI reflects change immediately
// - Timeline River shows filled/empty heart based on is_liked
//
// sharePost behavior:
// - Calls postsService.share(id) which hits POST /api/posts/:id/share/
// - Backend increments shares_count and returns updated post
// - Update that post in local state
//
// createReply behavior:
// - Calls postsService.createReply(parentId, content)
// - Increment reply_count on the parent post in local state
//
// Integration points:
// - Uses postsService.js (you build this too) for API calls
// - Pablo's Home.jsx consumes posts for TimelineRiverFeed
// - Pablo's Profile.jsx consumes posts filtered by user + shows "All Posts" section
// - Pablo's ComposerModal calls createPost()
// - Pablo's DeleteConfirmModal calls deletePost()
// - Pablo's TimelineRiverRow calls likePost() on heart icon click
// - Pablo's TimelineRiverRow calls sharePost() on share icon click
//
// RIVER TIMELINE "SPACE ECONOMY":
// - Posts are grouped BY USER (not by date!) in groupPosts.js
// - Each user = ONE row with carousel navigation between posts
// - MAX_POSTS_PER_TYPE = 12 (carousel capped for performance)
// - Profile page: River Timeline (max 12 per type) + "All Posts" section below (chronological, unlimited)
// - Home feed: Same max 12 limit per user per type
// - Need 2+ posts per type per user for carousel arrows to appear
// - seed_posts.py creates 9 posts/user (3 per type) for testing
//
// Post object format:
// {
//   id: number,
//   author: { id: number, username: string, first_name: string, last_name: string },
//   type: 'thoughts' | 'media' | 'milestones',
//   content: string,
//   media_url: string | null,  // NOT 'image'!
//   parent: number | null,
//   parent_id: number | null,
//   created_at: string (ISO timestamp),
//   likes_count: number,      // REQUIRED for ProfileCard analytics
//   reply_count: number,      // NOT 'comment_count'!
//   shares_count: number,     // REQUIRED for ProfileCard analytics
//   is_liked: boolean         // Has current user liked this post?
// }
//
// IMPORTANT: Engagement fields are used by Pablo's ProfileCard.jsx:
// - Wave chart calculates weekly engagement totals
// - Heatmap shows posting frequency calendar
// - These fields MUST be included in the API response!
//
// Think about:
// - When should fetchPosts() run? (After auth is done loading AND user is authenticated)
// - After createPost, refetch all or just add to array? (Add to array is faster)
// - After likePost, how do you update just that one post? (map and replace)
// - How do you handle optimistic updates vs waiting for API?
// - Should posts be sorted? (Newest first: sort by created_at descending)
// - How do you merge posts from fetchPostsByUsername? (avoid duplicates by ID)
//
// Hint: const { user, isLoading: authLoading, isAuthenticated } = useAuth();
// Hint: useEffect depends on [user, authLoading, isAuthenticated]
// Hint: if (authLoading) return; // Wait for auth
// Hint: if (user && isAuthenticated) fetchPosts();
// Hint: After create: setPosts(prev => [newPost, ...prev]);
// Hint: After delete: setPosts(prev => prev.filter(p => p.id !== id));
// Hint: After update/like: setPosts(prev => prev.map(p => p.id === id ? updated : p));
// Hint: For merge: const existingIds = new Set(prev.map(p => p.id));

import { createContext, useState, useEffect, useContext } from "react";
import postsService from "@services/postsService";
import { useAuth } from "@contexts/AuthContext";

export const PostsContext = createContext();

export function PostsProvider({ children }) {
  // Your code here
}

export function usePosts() {
  // Your code here
}
```

#### `frontend/src/services/postsService.js`

```javascript
// TODO: Create Posts Service - handles all posts API calls
//
// This file contains functions that make HTTP requests to the backend.
// It's the bridge between PostsContext and the Django API.
//
// IMPORTANT: Export as default object with methods, NOT named exports!
//
// Functions you need:
// - getAll(): GET /api/posts/ → returns array of posts
// - getByUsername(username): GET /api/posts/?username=xxx → returns posts by user
// - getById(id): GET /api/posts/:id/ → returns single post
// - create(data): POST /api/posts/ → returns created post
// - createReply(parentId, data): POST /api/posts/ with parent_id → returns created reply
// - update(id, updates): PATCH /api/posts/:id/ → returns updated post
// - delete(id): DELETE /api/posts/:id/ → returns nothing (204)
// - getReplies(postId): GET /api/posts/:id/replies/ → returns array of replies
// - like(id): POST /api/posts/:id/like/ → toggles like, returns updated post
// - share(id): POST /api/posts/:id/share/ → increments share count, returns updated post
//
// getByUsername behavior:
// - Appends ?username=xxx query parameter to /api/posts/
// - Backend filters posts by author.username
// - Used for viewing a specific user's profile posts
//
// createReply behavior:
// - Sends POST to /api/posts/ with parent_id in the data
// - Spread the data object and add parent_id: parentId
//
// like behavior:
// - Sends POST to /api/posts/:id/like/
// - Backend toggles the like (creates or deletes Like record)
// - Returns updated post with new likes_count and is_liked boolean
// - Frontend uses is_liked to show filled/empty heart icon
//
// share behavior:
// - Sends POST to /api/posts/:id/share/
// - Backend increments shares_count (no toggle - each call adds)
// - Returns updated post with new shares_count
//
// Integration points:
// - Uses apiClient.js (Tito builds) - already has JWT headers configured
// - PostsContext calls these functions
// - All functions return response.data (not full axios response)
//
// Think about:
// - Should you handle errors here or throw them? (Throw - let context handle)
// - All trailing slashes matter for Django! (/posts/ not /posts)
//
// Hint: import apiClient from './apiClient';
// Hint: const response = await apiClient.get('/posts/');
// Hint: return response.data;
// Hint: For getByUsername: apiClient.get(`/posts/?username=${username}`)
// Hint: For createReply: apiClient.post('/posts/', { ...data, parent_id: parentId })
// Hint: For like: await apiClient.post(`/posts/${id}/like/`);
// Hint: For share: await apiClient.post(`/posts/${id}/share/`);

import apiClient from "./apiClient";

const postsService = {
  // getAll, getByUsername, getById, create, createReply, update, delete, getReplies, like, share
  // Your code here
};

export default postsService;
```

---

### CRYSTAL'S FRONTEND FILES

#### `frontend/src/contexts/FriendsContext.jsx`

```javascript
// TODO: Create FriendsContext - manages friends list and requests
//
// This context handles the social graph - who is friends with whom,
// and pending friend requests.
//
// State you need:
// - friends: Array of friend user objects
// - pendingRequests: Array of pending friend requests (received) - NOT just 'requests'!
// - isLoading: Boolean
// - error: String
//
// Functions you need to provide:
// - fetchFriends(): Get current user's friends list AND pending requests (in parallel!)
// - sendRequest(userId): Send friend request to user
// - acceptRequest(requestId): Accept a friend request
// - declineRequest(requestId): Decline a friend request
// - removeFriend(userId): Unfriend someone
//
// IMPORTANT: Wait for AuthContext to finish loading before fetching!
// - Import useAuth and check authLoading
// - useEffect should depend on [user, authLoading]
// - If authLoading, return early (don't fetch yet)
//
// fetchFriends behavior:
// - Fetch BOTH friends AND pending requests in parallel using Promise.all
// - friendsService.getAll() for friends
// - friendsService.getPendingRequests() for pending requests
// - Set both states at once
//
// Integration points:
// - Uses friendsService.js (you build this too) for API calls
// - Friends.jsx displays friends list and pending requests
// - TopBar might show request count notification
//
// Friend object format:
// {
//   id: number,
//   username: string,
//   first_name: string,
//   last_name: string
// }
//
// Request object format:
// {
//   id: number,
//   from_user: { id: number, username: string, first_name: string, last_name: string },
//   created_at: string
// }
//
// Think about:
// - When to fetch? (After auth is done loading AND user exists)
// - After accepting request: add to friends, remove from pendingRequests
// - After declining: just remove from pendingRequests
// - After removing friend: filter out from friends array
// - Clear data when logged out (user becomes null)
//
// Hint: const { user, isLoading: authLoading } = useAuth();
// Hint: useEffect depends on [user, authLoading]
// Hint: if (authLoading) return;
// Hint: if (user) fetchFriends(); else clear arrays
// Hint: Promise.all([friendsService.getAll(), friendsService.getPendingRequests()])
// Hint: After accept: setFriends(prev => [...prev, newFriend]); setPendingRequests(prev => prev.filter(...))

import { createContext, useState, useEffect, useContext } from "react";
import friendsService from "@services/friendsService";
import { useAuth } from "@contexts/AuthContext";

export const FriendsContext = createContext();

export function FriendsProvider({ children }) {
  // Your code here
}

export function useFriends() {
  // Your code here
}
```

#### `frontend/src/services/friendsService.js`

```javascript
// TODO: Create Friends Service - handles all friends API calls
//
// IMPORTANT: Export as default object with methods, NOT named exports!
//
// Functions you need:
// - getAll(): GET /api/friends/ → array of friend users
// - getPendingRequests(): GET /api/friends/requests/ → array of pending requests
// - sendRequest(userId): POST /api/friends/request/:userId/ → created request
// - acceptRequest(requestId): POST /api/friends/accept/:requestId/ → new friend data
// - declineRequest(requestId): POST /api/friends/decline/:requestId/ → success
// - remove(userId): DELETE /api/friends/remove/:userId/ → success (no response body)
//
// Note the URL patterns:
// - /friends/ (no params) for listing friends
// - /friends/requests/ for pending requests
// - /friends/request/:userId/ for sending request (note singular 'request')
// - /friends/accept/:requestId/ for accepting
// - /friends/decline/:requestId/ for declining
// - /friends/remove/:userId/ for removing friend
//
// acceptRequest returns the new friend's data so you can add to friends array
//
// Integration points:
// - Uses apiClient.js (Tito builds)
// - FriendsContext calls these functions
//
// Hint: Same pattern as postsService.js
// Hint: apiClient.post(`/friends/request/${userId}/`)
// Hint: apiClient.delete(`/friends/remove/${userId}/`)
// Hint: For remove, use await without return (no response body)

import apiClient from "./apiClient";

const friendsService = {
  // getAll, getPendingRequests, sendRequest, acceptRequest, declineRequest, remove
  // Your code here
};

export default friendsService;
```

#### `frontend/src/components/pages/Friends/Friends.jsx`

```javascript
// TODO: Create Friends component - displays friends list and requests
//
// This page shows:
// 1. List of current friends
// 2. Pending friend requests (with accept/decline buttons)
// 3. Maybe a search/add friends feature (optional)
//
// Sections:
// - Friend Requests (if any pending)
// - My Friends list
//
// For each friend request:
// - Show sender's username, name
// - Accept button → calls acceptRequest()
// - Decline button → calls declineRequest()
//
// For each friend:
// - Show username, name
// - Remove button → calls removeFriend() (maybe with confirmation)
//
// Integration points:
// - Uses FriendsContext for data and actions
// - Uses Pablo's design system for styling
//
// Think about:
// - What if user has no friends? (Show friendly message)
// - What if no pending requests? (Hide that section or show "No pending requests")
// - Should remove friend have a confirmation? (Good UX - prevents accidents)
// - Loading states for each action?
//
// Hint: const { friends, pendingRequests, acceptRequest, declineRequest, removeFriend } = useFriends();
// Hint: Map over friends and pendingRequests to render lists
// Hint: Note: variable is 'pendingRequests' not 'requests'

import { useEffect } from "react";
import { useFriends } from "@contexts/FriendsContext";
import "./Friends.scss";

export default function Friends() {
  // Your code here
}
```

#### `frontend/src/components/pages/Friends/Friends.scss`

```scss
// TODO: Style the Friends page
//
// Use Pablo's design system for consistency.
//
// Sections to style:
// - .friends-page: Page container
// - .friends-section: Section wrapper (for requests, for friends list)
// - .section-title: "Friend Requests", "My Friends" headings
// - .friend-card: Individual friend/request card
// - .friend-avatar: Profile picture
// - .friend-info: Username and any other info
// - .friend-actions: Button container
// - .accept-btn, .decline-btn, .remove-btn: Action buttons
// - .empty-message: "No friends yet" type messages
//
// Layout:
// - Cards in a grid or list
// - Responsive: stack on mobile, grid on desktop
//
// Hint: Use glass-card mixin for cards
// Hint: Use flexbox or grid for layout
// Hint: Button colors: accept = primary/success, decline/remove = danger

@use "../../../styles/variables" as *;
@use "../../../styles/mixins" as *;

.friends-page {
  // Your code here
}

.friends-section {
  // Your code here
}

.friend-card {
  // Your code here
}

// ... rest of your styles
```

#### `frontend/src/components/pages/Friends/index.js`

```javascript
// TODO: Export Friends component (barrel export)

export { default } from "./Friends";
```

---

### TITO'S FRONTEND FILES

#### `frontend/src/main.jsx`

```javascript
// TODO: Create React entry point - bootstraps the entire app
//
// This is where React mounts to the DOM and wraps the app with providers.
//
// What this file does:
// 1. Import React and ReactDOM
// 2. Import global styles (main.scss)
// 3. Import App component
// 4. Import all context providers
// 5. Wrap App with providers in correct order
// 6. Mount to #root element
//
// Provider nesting order (outer to inner):
// 1. BrowserRouter (from react-router-dom)
// 2. ThemeProvider (yours)
// 3. AuthProvider (Natalia's)
// 4. PostsProvider (Colin's)
// 5. FriendsProvider (Crystal's)
// 6. MessageProvider (Pablo's - already built)
// 7. App
//
// Why this order?
// - Router must be outermost for navigation to work
// - Theme is independent, can be anywhere
// - Auth is needed by Posts/Friends (they might need user.id)
// - Message is UI-only, can be innermost
//
// Think about:
// - What if a provider isn't built yet? (Comment it out temporarily)
// - StrictMode: Keep it for development warnings
//
// Hint: Import providers from '../contexts' (the index.js exports them)
// Hint: Or import individually: import { AuthProvider } from '../contexts/AuthContext'

import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import "./styles/main.scss";

// Import providers (uncomment as they're built)
// import { ThemeProvider } from './contexts/ThemeContext';
// import { AuthProvider } from './contexts/AuthContext';
// import { PostsProvider } from './contexts/PostsContext';
// import { FriendsProvider } from './contexts/FriendsContext';
// import { MessageProvider } from './contexts/MessageContext';

ReactDOM.createRoot(document.getElementById("root")).render({
  /* Nest providers here - uncomment as built */
});
```

#### `frontend/src/services/apiClient.js`

```javascript
// TODO: Create API Client - axios instance with JWT authentication
//
// This is the foundation for ALL API calls. Every service uses this.
// It handles:
// 1. Base URL configuration
// 2. Automatically attaching JWT token to requests
// 3. Handling 401 errors (token expired)
// 4. Token refresh (optional advanced feature)
//
// Configuration:
// - Base URL: 'http://localhost:8000/api' (Django backend)
// - Default headers: Content-Type application/json
// - Request interceptor: Add Authorization header with token
// - Response interceptor: Handle 401 errors
//
// Request interceptor:
// - Before each request, check localStorage for token
// - If token exists, add header: Authorization: Bearer
//
// Response interceptor:
// - If response is 401 (unauthorized), token is invalid/expired
// - Clear token from localStorage
// - Optionally redirect to login or let AuthContext handle it
//
// Think about:
// - What if there's no token? (Don't add Authorization header)
// - What if token is expired? (401 response, handle gracefully)
// - Should you try to refresh the token? (Advanced - optional)
// - How do other services use this? (import apiClient; apiClient.get('/posts/'))
//
// Hint: import axios from 'axios';
// Hint: const apiClient = axios.create({ baseURL: 'http://localhost:8000/api' });
// Hint: apiClient.interceptors.request.use((config) => { ... });
// Hint: apiClient.interceptors.response.use((response) => response, (error) => { ... });

import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:8000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor - add auth token
apiClient.interceptors.request.use(
  (config) => {
    // Your code here
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - handle 401 errors
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    // Your code here
    return Promise.reject(error);
  }
);

export default apiClient;
```

#### `frontend/src/contexts/ThemeContext.jsx`

```javascript
// TODO: Create ThemeContext - manages light/dark theme state
//
// NUMENEON supports light and dark modes. This context manages which
// theme is active and provides a toggle function.
//
// State you need:
// - theme: 'light' | 'dark'
//
// Functions you need:
// - toggleTheme(): Switch between light and dark
// - setTheme(theme): Set specific theme (optional)
//
// How theming works:
// - Pablo's CSS uses CSS custom properties (variables)
// - Light mode overrides are in _light-mode.scss
// - Add class 'light-mode' to document.body for light mode
// - Remove class for dark mode (default)
//
// Persistence:
// - Store preference in localStorage
// - On load, check localStorage for saved preference
// - If none, default to dark mode (or check system preference)
//
// Integration points:
// - ThemeToggle component calls toggleTheme()
// - Theme class applied to document.body
//
// Think about:
// - Should you respect system preference? (prefers-color-scheme media query)
// - How do you apply theme on initial load? (useEffect, or check before render)
// - When theme changes, update localStorage
//
// Hint: document.body.classList.add('light-mode') / .remove('light-mode')
// Hint: localStorage.getItem('theme') / localStorage.setItem('theme', theme)
// Hint: window.matchMedia('(prefers-color-scheme: light)').matches

import { createContext, useState, useEffect, useContext } from "react";

export const ThemeContext = createContext();

export function ThemeProvider({ children }) {
  // Your code here
}

export function useTheme() {
  // Your code here
}
```

#### `frontend/src/components/ui/ThemeToggle/ThemeToggle.jsx`

```javascript
// TODO: Create ThemeToggle component - button to switch themes
//
// Simple component that displays current theme and toggles it on click.
//
// Component should:
// 1. Show icon/label for current theme (sun for light, moon for dark)
// 2. Call toggleTheme() when clicked
//
// Integration points:
// - Uses ThemeContext's theme state and toggleTheme function
// - Placed in TopBar or settings area
//
// Think about:
// - What icon to show? (Sun/moon, or light/dark label)
// - Accessible? (Button with aria-label)
// - Animation on toggle? (Optional nice touch)
//
// Hint: const { theme, toggleTheme } = useTheme();
// Hint: {theme === 'dark' ? '☀️' : '🌙'}

import { useTheme } from "@contexts/ThemeContext";
import "./ThemeToggle.scss";

export default function ThemeToggle() {
  // Your code here
}
```

#### `frontend/src/components/ui/ThemeToggle/ThemeToggle.scss`

```scss
// TODO: Style the ThemeToggle button
//
// Keep it simple - it's just a button.
//
// Style:
// - .theme-toggle: The button itself
// - Match Pablo's design system
// - Maybe a subtle hover effect
//
// Consider:
// - Size appropriate for TopBar
// - Clear clickable affordance
// - Icon should be visible in both themes

@use "../../../styles/variables" as *;
@use "../../../styles/mixins" as *;

.theme-toggle {
  // Your code here
}
```

#### `frontend/src/components/ui/ThemeToggle/index.js`

```javascript
// TODO: Export ThemeToggle component (barrel export)

export { default } from "./ThemeToggle";
```

---

### COLLABORATIVE FILE

#### `frontend/src/contexts/index.js`

```javascript
// TODO: Export all context providers and hooks
//
// This file makes it easy to import multiple contexts in one line:
// import { useAuth, usePosts, useFriends } from '../contexts';
//
// COLLABORATIVE FILE - Each context owner adds their exports:
// - Natalia: AuthProvider, useAuth
// - Colin: PostsProvider, usePosts
// - Crystal: FriendsProvider, useFriends
// - Tito: ThemeProvider, useTheme
// - Pablo: MessageProvider, useMessage (already built)

// TODO (Natalia): Export AuthContext
// export { AuthProvider, useAuth } from './AuthContext';

// TODO (Colin): Export PostsContext
// export { PostsProvider, usePosts } from './PostsContext';

// TODO (Crystal): Export FriendsContext
// export { FriendsProvider, useFriends } from './FriendsContext';

// TODO (Tito): Export ThemeContext
// export { ThemeProvider, useTheme } from './ThemeContext';

// Pablo's MessageContext (already built)
// export { MessageProvider, useMessage } from './MessageContext';
```

---

## CATEGORY B: PABLO'S UI FILES (Usage Comments Only)

For ALL of Pablo's ~75 component files, add a USAGE comment block at the top.
Keep ALL implementation code intact. Mark as "DO NOT MODIFY".

### Template for Pablo's Components:

```javascript
/**
 * COMPONENT USAGE (For Team Reference)
 * DO NOT MODIFY THIS FILE
 *
 * Purpose: [What this component does]
 *
 * Data Requirements:
 * - Consumes: [Which context(s) via which hook(s)]
 * - Expects: [What data format]
 *
 * Props: [If any]
 * - propName: type - description
 *
 * Integration Points:
 * - Used by: [Parent component(s)]
 * - Renders: [Child component(s)]
 * - Calls: [What context functions it uses]
 *
 * Team Integration:
 * - [Name]: [What they need to build for this to work]
 *
 * This is Pablo's complete UI implementation.
 * Your job is to build the backend and contexts that provide data
 * in the format this component expects.
 */

// ... Pablo's complete implementation follows ...
```

### Files to Add Usage Comments:

**Layout Components:**

- `frontend/src/App.jsx`
  - **Note:** Contains routes for both `/profile` (own) and `/profile/:username` (others)
  - Profile navigation uses React Router's `useParams()` to detect which user to show
- `frontend/src/components/layout/TopBar/TopBar.jsx`
- `frontend/src/components/layout/TopBar/MessageModal/MessageModal.jsx`
- `frontend/src/components/layout/SideNav/SideNav.jsx`

**Home Page System:**

- `frontend/src/components/pages/Home/Home.jsx`
- `frontend/src/components/pages/Home/utils/groupPosts.js` ← **Groups by USER ONLY (not date!), MAX 12 posts per type, uses `orderId` field**
- `frontend/src/components/pages/Home/utils/timeFormatters.js` ← **NEW (Jan 2025):** `formatRelativeTime()` utility
- `frontend/src/components/pages/Home/components/DeleteConfirmModal/DeleteConfirmModal.jsx`
- `frontend/src/components/pages/Home/components/MediaLightbox/MediaLightbox.jsx`
- `frontend/src/components/pages/Home/components/TimelineRiverFeed/TimelineRiverFeed.jsx`
- `frontend/src/components/pages/Home/components/TimelineRiverRow/TimelineRiverRow.jsx`
  - **REFACTORED (Jan 2025):** Now uses modular sub-components
  - Sub-components in `TimelineRiverRow/components/`:
    - `PostCard/` - Individual post rendering with all actions
    - `SmartDeck/` - Carousel deck with prev/next navigation
    - `ThreadView/` - Inline replies thread (Twitter-style)
    - `MobileTabNav/` - Mobile category tab navigation
    - `RepostModal/` - **NEW (Jan 2026)** Share modal with repost/copy link icons
  - Usernames and avatars are clickable → navigate to user's profile
  - Uses `handleUserClick()` with `useNavigate()` from React Router
  - CSS classes: `.clickable-user` with hover glow effects

**Profile Page System:**

- `frontend/src/components/pages/Profile/Profile.jsx`
  - **Note:** Supports viewing own profile (`/profile`) AND other users (`/profile/:username`)
  - Uses `useParams()` to detect which profile to show
  - `isOwnProfile` flag controls conditional rendering of composer, toggle, edit/delete
  - `profileUser` lookup from friends or post authors
  - **Layout:** ProfileCard → River Timeline (max 12 per type) → All Posts section (chronological)
  - **NEW (Jan 2026):** All Posts section has expandable full-page comment composer
    - Inline composer shows expand button (MaximizeIcon) to open full-page view
    - Full-page composer shows original post context (author, content, media) + thread replies
    - Media images scale to fill modal width (100%) with aspect ratio preserved
    - Matches PostCard's full-page composer from the feed
- `frontend/src/components/pages/Profile/components/ComposerModal/ComposerModal.jsx`
- `frontend/src/components/pages/Profile/components/ProfileCard/ProfileCard.jsx`
- `frontend/src/components/pages/Profile/components/ProfileCard/components/ActivityVisualization/ActivityVisualization.jsx`
  - **Note:** SCSS includes responsive breakpoints (600px, 480px, 375px) for wave/heatmap toggle buttons
  - Toggle buttons scale down on mobile, activity meta hidden on very small screens
  - Engagement values boosted: High=800-1500, Medium=400-800, Low=200-400
- `frontend/src/components/pages/Profile/components/ProfileCard/components/PostTypeBreakdown/PostTypeBreakdown.jsx`
- `frontend/src/components/pages/Profile/components/ProfileCard/components/ProfileCardBack/ProfileCardBack.jsx`
- `frontend/src/components/pages/Profile/components/ProfileCard/components/ProfileCardFront/ProfileCardFront.jsx`
- `frontend/src/components/pages/Profile/components/ProfileCard/components/QuickSettings/QuickSettings.jsx`
- `frontend/src/components/pages/Profile/components/TimelineRiver/TimelineRiver.jsx`
  - **Note:** Accepts `isOwnProfile` prop to conditionally show edit/delete buttons
  - Friends Feed headers are clickable → navigate to friend's profile
  - **NEW (Jan 2026):** Expandable full-page comment composer matching feed behavior
    - `renderCommentSection()` now includes expand button + full-page portal
    - Full-page view shows post context, thread replies, and fixed composer at bottom
    - Works for both own profile and visiting friend profiles

**Other Pages:**

- `frontend/src/components/pages/About/About.jsx`
- `frontend/src/components/pages/Landing/Landing.jsx`
- `frontend/src/components/pages/NotFound/NotFound.jsx`

**Contexts:**

- `frontend/src/contexts/MessageContext.jsx`

**Also add usage comments to all index.js files in Pablo's domain.**

---

## SHARED FILES (DO NOT TOUCH)

These files are pre-configured:

- `frontend/eslint.config.js`
- `frontend/vite.config.js`
- `frontend/package.json`
- `frontend/index.html`
- All 13 files in `frontend/src/styles/`

---

**NEXT:** Read `05-TEAM-PLAN-FILES.md` for team markdown file templates
