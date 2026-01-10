# Session: User Profile Navigation & Privacy Controls

**Date:** December 23, 2024  
**Commit:** `235649c`  
**Branch:** `master-ui`

---

## Goals

1. Click on a username in the Home feed → navigate to that user's profile
2. When viewing another user's profile, hide edit/delete buttons (privacy)
3. Display correct user name, username, and posts on other users' profiles

---

## Problems Encountered & Solutions

### Problem 1: "undefined's Timeline" and Empty Profile

**Symptoms:**

- Clicking a username navigated to `/profile/undefined`
- Profile page showed "undefined" for name and username
- No posts displayed on other users' profiles

**Root Cause:**
The `groupPosts.js` utility only stored partial user data:

```javascript
// BEFORE - Missing username!
user: {
  id: orderId,
  name: authorName,
  avatar: getInitials(...)
}
```

When `TimelineRiverRow.jsx` called `navigate(/profile/${user.username})`, `user.username` was undefined.

**Solution:**
Added complete user data to `groupPosts.js`:

```javascript
// AFTER - All required fields
user: {
  id: orderId,
  name: authorName,
  username: authorObj?.username || ...,
  first_name: authorObj?.first_name || '',
  last_name: authorObj?.last_name || '',
  avatar: getInitials(...)
}
```

**Files Changed:**

- `frontend/src/components/pages/Home/utils/groupPosts.js`

---

### Problem 2: Profile Bio/Location/Website Not Showing

**Symptoms:**

- Own profile showed "No bio yet" even though bio existed in database
- Location and website were not displayed

**Root Cause:**
The backend returns nested profile data:

```json
{
  "id": 1,
  "username": "pabloPistola",
  "first_name": "Pablo",
  "last_name": "Cordero",
  "profile": {
    "bio": "A Sentient Android",
    "location": "Brooklyn, NY",
    "website": "https://github.com/..."
  }
}
```

But `ProfileCardFront.jsx` was accessing `user?.bio` instead of `user?.profile?.bio`.

**Solution:**
Fixed data access paths:

```jsx
// BEFORE
{user?.bio || 'No bio yet'}
{user?.location && ...}
{user?.website && ...}

// AFTER
{user?.profile?.bio || 'No bio yet'}
{user?.profile?.location && ...}
{user?.profile?.website && ...}
```

**Files Changed:**

- `frontend/src/components/pages/Profile/components/ProfileCard/components/ProfileCardFront/ProfileCardFront.jsx`

---

### Problem 3: Hardcoded User Data

**Symptoms:**

- Every profile showed "@pabloPistola" as the handle
- Location was always "Brooklyn, NY"
- GitHub link was hardcoded

**Root Cause:**
`ProfileCardFront.jsx` had hardcoded values from initial development:

```jsx
<span className="profile-handle">@pabloPistola</span>
<span>Brooklyn, NY</span>
<a href="https://github.com/pablodcordero">...</a>
```

**Solution:**
Made all values dynamic:

```jsx
<span className="profile-handle">@{user?.username || "user"}</span>;
{
  user?.profile?.location && <span>{user.profile.location}</span>;
}
{
  user?.profile?.website && <a href={user.profile.website}>...</a>;
}
```

**Files Changed:**

- `frontend/src/components/pages/Profile/components/ProfileCard/components/ProfileCardFront/ProfileCardFront.jsx`

---

### Problem 4: Profile User Lookup Failed

**Symptoms:**

- When navigating to `/profile/titod`, the profileUser was not found
- Fallback showed empty first_name/last_name

**Root Cause:**
The `Profile.jsx` lookup order checked friends first, then posts. But for users who aren't friends yet, or when friends data hadn't loaded, it fell back to an empty object.

**Solution:**

1. Check posts first (they always have complete author data)
2. Then check friends list
3. Improved fallback to at least show the username from URL

```javascript
const profileUser = useMemo(() => {
  if (isOwnProfile) return currentUser;

  // Posts have complete author data - check first
  const postMatch = posts.find(p => p.author?.username === profileUsername)?.author;
  if (postMatch) return postMatch;

  // Friends list as backup
  const friendMatch = friends?.find(f => f.username === profileUsername);
  if (friendMatch) return friendMatch;

  // Fallback - use username from URL
  return { username: profileUsername, first_name: profileUsername, last_name: '' };
}, [...]);
```

**Files Changed:**

- `frontend/src/components/pages/Profile/Profile.jsx`

---

## Data Flow Diagram

```
Home Feed Click
      │
      ▼
TimelineRiverRow.jsx
   handleUserClick(e, user.id, user.username)
      │
      ▼
   navigate(`/profile/${username}`)
      │
      ▼
App.jsx Route: /profile/:username
      │
      ▼
Profile.jsx
   useParams() → { username: "titod" }
   profileUser = lookup from posts/friends
      │
      ▼
ProfileCard.jsx
   user={profileUser}
      │
      ▼
ProfileCardFront.jsx
   displayName = user.first_name + user.last_name
   handle = @user.username
   bio = user.profile?.bio
```

---

## Key Takeaways

1. **Always trace data flow end-to-end** - The bug started in `groupPosts.js` but manifested in `Profile.jsx`

2. **Check backend response structure** - `user.bio` vs `user.profile.bio` is a common gotcha

3. **Remove hardcoded values early** - Placeholder data from initial dev can hide bugs

4. **Use optional chaining defensively** - `user?.profile?.bio` prevents crashes when data is loading

5. **Add loading states** - Prevents rendering with incomplete data

---

## Files Modified (Summary)

| File                   | Change                                               |
| ---------------------- | ---------------------------------------------------- |
| `groupPosts.js`        | Added username, first_name, last_name to user object |
| `Profile.jsx`          | Improved profileUser lookup, added loading state     |
| `ProfileCardFront.jsx` | Fixed data access paths, removed hardcoded values    |
| `TimelineRiverRow.jsx` | Added handleUserClick navigation                     |
| `TimelineRiver.jsx`    | Added isOwnProfile prop, clickable friend headers    |
| `App.jsx`              | Added /profile/:username route                       |
