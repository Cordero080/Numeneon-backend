# Crystal's Tasks (Size: M)

## Your Mission

You're building the Friends system - connections between users. You handle friend requests, approvals, and the social graph that makes NUMENEON a network. Plus you're building the Friends page UI where users manage their connections.

## Files You Own

**Important:** Don't touch anyone else's files to avoid merge conflicts!

### Backend Files (7 total)

- `backend/friends/models.py` - Friendship data structure (requests, status)
- `backend/friends/views.py` - Friends API endpoints (send request, accept, remove)
- `backend/friends/serializers.py` - Friend data validation and formatting
- `backend/friends/urls.py` - Friends API routes configuration
- `backend/friends/apps.py` - Django app configuration
- `backend/friends/__init__.py` - Package marker
- `backend/friends/admin.py` - Django admin interface for friendships

### Frontend Files (5 total)

- `frontend/src/contexts/FriendsContext.jsx` - Friends state management
- `frontend/src/services/friendsService.js` - Friends API calls wrapper
- `frontend/src/components/pages/Friends/Friends.jsx` - Friends page UI
- `frontend/src/components/pages/Friends/Friends.scss` - Friends page styling
- `frontend/src/components/pages/Friends/index.js` - Component export

---

## Task Breakdown

### ✅ Task 1: Create Friendship Model

**Files:** `backend/friends/models.py`

**What:** Define the database structure for friend relationships

**Why:** Social networks need to track who's connected to who

**Acceptance Criteria:**

- [ ] Friendship has `user1` field (ForeignKey to User)
- [ ] Friendship has `user2` field (ForeignKey to User)
- [ ] Friendship has `status` field (choices: 'pending', 'accepted', 'rejected')
- [ ] Friendship has `created_at` field (auto-set timestamp)
- [ ] Friendship has `action_user` field (who sent the request)
- [ ] Constraint: Cannot friend yourself (user1 != user2)
- [ ] Constraint: Only one friendship record per user pair

**Think about:**

- How do you prevent duplicate friendships? (unique_together constraint)
- Should the model be directional (A→B) or bidirectional?
- How do you query "all friends of user X"? (filter by user1 OR user2)
- What's the difference between a pending request and accepted friendship?

**Helpful Resources:** Django constraints, unique_together

---

### ✅ Task 2: Build Friendship Serializers

**Files:** `backend/friends/serializers.py`

**What:** Transform Friendship data into JSON, include user details

**Why:** Frontend needs to show username, avatar for friend requests and friend lists

**Acceptance Criteria:**

- [ ] FriendshipSerializer includes all Friendship fields
- [ ] User1 and user2 are nested (show username, profile_picture)
- [ ] Status field is included
- [ ] Created_at is in ISO format
- [ ] Serializer can handle creating new friendships

**Think about:**

- How do you nest user data without exposing passwords?
- Should you show who sent the request (action_user)?
- How do you validate that user1 != user2 when creating?

**Helpful Resources:** DRF nested serializers, validation

---

### ✅ Task 3: Build Friends API Views

**Files:** `backend/friends/views.py`

**What:** Create endpoints for friend operations

**Why:** Users need to send requests, accept/reject them, and remove friends

**Acceptance Criteria:**

- [ ] GET /api/friends/ - List all accepted friendships for current user
- [ ] GET /api/friends/pending/ - List incoming friend requests
- [ ] POST /api/friends/request/ - Send friend request to another user
- [ ] POST /api/friends/:id/accept/ - Accept pending request
- [ ] POST /api/friends/:id/reject/ - Reject pending request
- [ ] DELETE /api/friends/:id/ - Remove friendship (unfriend)

**Think about:**

- How do you get "all friends of current user" (WHERE user1=X OR user2=X)?
- Should only the recipient be able to accept/reject requests?
- What happens if you send a request to someone who already sent you one?
- How do you prevent duplicate requests?

**Helpful Resources:** DRF ViewSets, Q objects for OR queries, @action decorator

---

### ✅ Task 4: Configure Friends URL Routes

**Files:** `backend/friends/urls.py`

**What:** Map URL patterns to your views

**Why:** Defines what URLs the frontend can call

**Acceptance Criteria:**

- [ ] All endpoints mapped correctly
- [ ] Custom actions (/pending/, /accept/, /reject/) configured

---

### ✅ Task 5: Django Admin Configuration

**Files:** `backend/friends/admin.py`

**What:** Register Friendship model in Django admin

**Why:** Easy viewing/management during development

**Acceptance Criteria:**

- [ ] Friendship model registered
- [ ] List display shows user1, user2, status, created_at
- [ ] Can filter by status
- [ ] Can search by username

---

### ✅ Task 6: Build FriendsContext (Frontend State)

**Files:** `frontend/src/contexts/FriendsContext.jsx`

**What:** React context that manages friend data across the app

**Why:** Multiple components need friend data (Friends page, TopBar notifications, search results)

**Acceptance Criteria:**

- [ ] Stores `friends` array (accepted friendships)
- [ ] Stores `pendingRequests` array (incoming requests)
- [ ] Provides `fetchFriends()` function
- [ ] Provides `fetchPendingRequests()` function
- [ ] Provides `sendFriendRequest(userId)` function
- [ ] Provides `acceptRequest(friendshipId)` function
- [ ] Provides `rejectRequest(friendshipId)` function
- [ ] Provides `removeFriend(friendshipId)` function
- [ ] Handles loading and error states

**Think about:**

- Should you fetch friends on mount?
- How do you know when new friend requests arrive? (polling? websockets later?)
- After accepting a request, should you move it from pending to friends array?

**Helpful Resources:** Look at PostsContext (Colin) for similar pattern

---

### ✅ Task 7: Build Friends Service Layer

**Files:** `frontend/src/services/friendsService.js`

**What:** Functions that make HTTP requests to friends API

**Why:** Separates API logic from React components

**Acceptance Criteria:**

- [ ] `getFriends()` - Fetch accepted friendships
- [ ] `getPendingRequests()` - Fetch incoming requests
- [ ] `sendFriendRequest(userId)` - Send request
- [ ] `acceptRequest(id)` - Accept request
- [ ] `rejectRequest(id)` - Reject request
- [ ] `removeFriend(id)` - Unfriend
- [ ] All functions return response.data

**Think about:**

- Do you need to pass auth token? (No! apiClient handles it)
- Should you handle errors or throw them?

**Helpful Resources:** Uses apiClient.js (Tito)

---

### ✅ Task 8: Build Friends Page UI

**Files:** `Friends.jsx`, `Friends.scss`, `index.js`

**What:** Page where users see their friends list and pending requests

**Why:** Users need a centralized place to manage connections

**Acceptance Criteria:**

- [ ] Shows list of accepted friends with username, avatar
- [ ] Shows "Remove Friend" button for each friend
- [ ] Shows pending incoming requests in separate section
- [ ] Shows "Accept" and "Reject" buttons for each request
- [ ] Shows stats: "X connected, Y pending"
- [ ] Calls FriendsContext functions for all actions
- [ ] Styled using Pablo's design system (glass-card, neon-glow)
- [ ] Responsive (looks good on mobile and desktop)

**Think about:**

- How do you distinguish between friends and pending requests in the UI?
- Should you show who sent the request vs who received it?
- What happens after accepting a request? (refetch friends list?)
- Should there be a search/filter for large friend lists?

**Helpful Resources:** Pablo's design system in `src/styles/`

---

## Integration Points

**You provide:**

- Friends API endpoints
- FriendsContext with `useFriends()` hook
- Friends page UI
- Friendship data format: `{ id, user1: {...}, user2: {...}, status, created_at }`

**You consume:**

- User model (Natalia) - friendships link two users
- apiClient.js (Tito) - for authenticated API calls
- Pablo's design system - for Friends page styling

**Work with:**

- **Natalia:** Your Friendship model references her User model
- **Tito:** Your friendsService uses his apiClient
- **Pablo:** His TopBar NotificationModal will consume your pendingRequests

---

## Friendship Data Format

Backend should return friendships in this format:

```javascript
{
  id: 1,
  user1: {
    id: 5,
    username: "alice",
    profile_picture: "https://..."
  },
  user2: {
    id: 7,
    username: "bob",
    profile_picture: "https://..."
  },
  status: "accepted",  // or "pending" or "rejected"
  action_user: 5,  // ID of user who sent the request
  created_at: "2024-12-19T10:00:00Z"
}
```

---

## Testing Checklist

- [ ] Can send friend request to another user
- [ ] Cannot send duplicate request to same user
- [ ] Cannot send request to yourself (should error)
- [ ] Pending requests appear in recipient's pending list
- [ ] Can accept friend request
- [ ] Accepted friendship appears in both users' friends lists
- [ ] Can reject friend request
- [ ] Rejected request disappears from pending list
- [ ] Can remove friend (unfriend)
- [ ] Removed friendship disappears from friends list for both users
- [ ] Friends page shows correct counts ("10 connected, 2 pending")
- [ ] UI updates immediately after accepting/rejecting/removing
