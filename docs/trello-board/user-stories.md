# 📋 NUMENEON - User Stories

> Standard Trello-style user stories for the NUMENEON social media app rebuild.

---

## 🎯 Epic: User Authentication

### US-001: User Registration

**As a** new user  
**I want to** create an account with username, email, and password  
**So that** I can access NUMENEON and connect with others

**Acceptance Criteria:**

- [ ] Registration form with username, email, password, confirm password fields
- [ ] Password validation (minimum 8 characters)
- [ ] Email format validation
- [ ] Duplicate username/email prevention
- [ ] Automatic login after successful registration
- [ ] Redirect to home feed after signup

**Story Points:** 5  
**Owner:** Natalia

---

### US-002: User Login

**As a** returning user  
**I want to** log in with my email and password  
**So that** I can access my account and content

**Acceptance Criteria:**

- [ ] Login form with email and password fields
- [ ] JWT token generation on successful login
- [ ] Token stored in localStorage
- [ ] Redirect to home feed after login
- [ ] Error message for invalid credentials

**Story Points:** 3  
**Owner:** Natalia

---

### US-003: Protected Routes

**As a** user  
**I want** unauthorized users to be blocked from protected pages  
**So that** my content remains private and secure

**Acceptance Criteria:**

- [ ] Non-authenticated users redirected to login
- [ ] Auth check on app load (existing token validation)
- [ ] Loading state while checking authentication
- [ ] Token refresh on expiration (401 handling)

**Story Points:** 3  
**Owner:** Natalia

---

### US-004: User Logout

**As a** logged-in user  
**I want to** log out of my account  
**So that** I can secure my session on shared devices

**Acceptance Criteria:**

- [ ] Logout button accessible in navigation
- [ ] Clear JWT tokens from localStorage
- [ ] Clear user state
- [ ] Redirect to login page

**Story Points:** 2  
**Owner:** Natalia

---

## 🎯 Epic: Posts System

### US-005: View Posts Feed

**As a** user  
**I want to** see a feed of posts from all users  
**So that** I can discover content and stay connected

**Acceptance Criteria:**

- [ ] Posts displayed in Timeline River (3-column layout)
- [ ] Posts grouped by user (one row per user)
- [ ] Posts sorted by most recent
- [ ] Post types separated: thoughts, media, milestones
- [ ] Author info displayed on each post

**Story Points:** 8  
**Owner:** Pablo (UI) + Colin (API/Context)

---

### US-006: Create Post

**As a** user  
**I want to** create a new post  
**So that** I can share my thoughts, media, or milestones

**Acceptance Criteria:**

- [ ] Post composer modal accessible from home/profile
- [ ] Select post type (thoughts/media/milestones)
- [ ] Text content input (required for thoughts/milestones)
- [ ] Media URL input for media posts
- [ ] Post appears in feed immediately after creation
- [ ] Keyboard shortcut: Cmd/Ctrl + Enter to submit

**Story Points:** 5  
**Owner:** Colin

---

### US-007: Edit Post

**As a** post author  
**I want to** edit my existing posts  
**So that** I can fix typos or update content

**Acceptance Criteria:**

- [ ] Edit button visible only on own posts
- [ ] Opens composer with existing content pre-filled
- [ ] Updates post in place without page refresh
- [ ] Maintains original creation timestamp

**Story Points:** 3  
**Owner:** Colin

---

### US-008: Delete Post

**As a** post author  
**I want to** delete my posts  
**So that** I can remove content I no longer want public

**Acceptance Criteria:**

- [ ] Delete button visible only on own posts
- [ ] Confirmation modal before deletion
- [ ] Post removed from feed immediately
- [ ] Associated replies also deleted

**Story Points:** 3  
**Owner:** Colin

---

### US-009: Like/Unlike Post

**As a** user  
**I want to** like and unlike posts  
**So that** I can show appreciation for content

**Acceptance Criteria:**

- [ ] Heart icon toggles filled/unfilled state
- [ ] Like count updates immediately
- [ ] Prevents double-liking (backend validation)
- [ ] Heart animation on click
- [ ] Color varies by post type (cyan/purple/green)

**Story Points:** 3  
**Owner:** Colin (API) + Pablo (UI)

---

### US-010: Reply to Post

**As a** user  
**I want to** reply to posts  
**So that** I can engage in conversations

**Acceptance Criteria:**

- [ ] Comment button opens inline composer
- [ ] Reply appears in thread below parent post
- [ ] Reply count updates on parent post
- [ ] Expand/collapse thread functionality
- [ ] Option to expand composer to full page

**Story Points:** 5  
**Owner:** Colin (API) + Pablo (UI)

---

### US-011: Share/Repost

**As a** user  
**I want to** share posts  
**So that** I can spread content to my network

**Acceptance Criteria:**

- [ ] Repost button opens share modal
- [ ] Options: Repost, Quote repost, Copy link
- [ ] Share count increments
- [ ] Link copied to clipboard on "Copy link"

**Story Points:** 3  
**Owner:** Colin (API) + Pablo (UI)

---

## 🎯 Epic: Friends System

### US-012: View Friends List

**As a** user  
**I want to** see my list of accepted friends  
**So that** I can manage my connections

**Acceptance Criteria:**

- [ ] Friends page displays accepted friendships
- [ ] Shows friend's avatar, username, bio
- [ ] Click friend to visit their profile
- [ ] Message button to start DM

**Story Points:** 3  
**Owner:** Crystal

---

### US-013: Send Friend Request

**As a** user  
**I want to** send friend requests  
**So that** I can connect with other users

**Acceptance Criteria:**

- [ ] Add friend button on user profiles
- [ ] Request sent notification
- [ ] Prevents duplicate requests
- [ ] Cannot friend yourself

**Story Points:** 3  
**Owner:** Crystal

---

### US-014: Accept/Reject Friend Requests

**As a** user  
**I want to** accept or reject incoming friend requests  
**So that** I can control who connects with me

**Acceptance Criteria:**

- [ ] Pending requests section on Friends page
- [ ] Accept button adds to friends
- [ ] Reject button removes request
- [ ] Click requester to view their profile

**Story Points:** 3  
**Owner:** Crystal

---

### US-015: Remove Friend

**As a** user  
**I want to** remove friends  
**So that** I can manage my connections

**Acceptance Criteria:**

- [ ] Remove/Unfriend option on friend card
- [ ] Confirmation before removal
- [ ] Updates both users' friend lists

**Story Points:** 2  
**Owner:** Crystal

---

## 🎯 Epic: Profile System

### US-016: View Own Profile

**As a** user  
**I want to** view my profile page  
**So that** I can see my posts and information

**Acceptance Criteria:**

- [ ] ProfileCard displays avatar, name, bio, stats
- [ ] My posts shown in Timeline River
- [ ] Carousel navigation for multiple posts
- [ ] Analytics on card back (flip interaction)

**Story Points:** 8  
**Owner:** Pablo

---

### US-017: View Other User's Profile

**As a** user  
**I want to** view other users' profiles  
**So that** I can learn about them and see their content

**Acceptance Criteria:**

- [ ] Navigate via clicking username/avatar
- [ ] Shows their ProfileCard and posts
- [ ] Hidden: post composer, edit/delete buttons
- [ ] Shows: message button, friend request button

**Story Points:** 5  
**Owner:** Pablo

---

### US-018: Click to Navigate to Profile

**As a** user  
**I want to** click on any username or avatar in the feed  
**So that** I can quickly visit that user's profile

**Acceptance Criteria:**

- [ ] Usernames are clickable throughout app
- [ ] Avatars are clickable throughout app
- [ ] Navigates to `/profile/:username`
- [ ] Cursor changes to pointer on hover

**Story Points:** 3  
**Owner:** Pablo

---

## 🎯 Epic: Theme & Infrastructure

### US-019: Dark/Light Mode Toggle

**As a** user  
**I want to** switch between dark and light themes  
**So that** I can use the app comfortably in any lighting

**Acceptance Criteria:**

- [ ] Theme toggle in TopBar or settings
- [ ] Instant theme change (no page refresh)
- [ ] Preference saved to localStorage
- [ ] Persists across sessions

**Story Points:** 3  
**Owner:** Tito

---

### US-020: API Client with Auth

**As a** developer  
**I want** API calls to automatically include auth tokens  
**So that** I don't need to manually attach tokens

**Acceptance Criteria:**

- [ ] Axios instance with baseURL configured
- [ ] Request interceptor attaches JWT token
- [ ] Response interceptor handles 401 errors
- [ ] Auto-logout on token expiration

**Story Points:** 3  
**Owner:** Tito

---

## 🎯 Epic: Search & Discovery

### US-021: Global Search

**As a** user  
**I want to** search for users and posts  
**So that** I can find specific content or people

**Acceptance Criteria:**

- [ ] Search modal accessible from TopBar
- [ ] Filter tabs: All, Users, Posts
- [ ] User results: click to profile, message icon
- [ ] Post results: click to author's profile
- [ ] Real-time results as you type

**Story Points:** 5  
**Owner:** Pablo

---

## 🎯 Epic: Messaging

### US-022: Direct Messaging

**As a** user  
**I want to** send direct messages to other users  
**So that** I can have private conversations

**Acceptance Criteria:**

- [ ] Message modal accessible from TopBar
- [ ] Conversation list view
- [ ] Chat view with message history
- [ ] Send text messages
- [ ] Mobile-responsive with back button

**Story Points:** 8  
**Owner:** Pablo

---

## 📊 Story Points Summary

| Epic                   | Stories | Total Points |
| ---------------------- | ------- | ------------ |
| Authentication         | 4       | 13           |
| Posts System           | 7       | 30           |
| Friends System         | 4       | 11           |
| Profile System         | 3       | 16           |
| Theme & Infrastructure | 2       | 6            |
| Search & Discovery     | 1       | 5            |
| Messaging              | 1       | 8            |
| **TOTAL**              | **22**  | **89**       |

---

## 📌 Story Status Legend

- **📝 Backlog** - Not started
- **🔄 In Progress** - Currently being worked on
- **👀 In Review** - PR submitted, awaiting review
- **✅ Done** - Completed and merged

---

_Last Updated: January 8, 2026_
