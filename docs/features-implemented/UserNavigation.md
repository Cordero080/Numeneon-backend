# User Navigation System

## Overview

Users can click on any username or avatar to navigate to that user's profile. All cards display user headers for consistent identity.

## Routes

```jsx
// App.jsx
<Route path="/profile" element={<Profile />} />           // Own profile
<Route path="/profile/:username" element={<Profile />} /> // Other's profile
```

## Clickable User Elements

### Home Feed (TimelineRiverRow.jsx)

```jsx
const handleUserClick = (e, userId, username) => {
  e.stopPropagation();
  if (currentUser?.id === userId) {
    navigate("/profile");
  } else {
    navigate(`/profile/${username}`);
  }
};
```

**Clickable elements:** Avatar (`.river-avatar`), Author name (`.river-author`)

### Profile Friends Feed (TimelineRiver.jsx)

```jsx
<div
  className="friend-row-header clickable-friend"
  onClick={() => navigate(`/profile/${friend.username}`)}
/>
```

## Card User Headers

All timeline cards display the author's avatar + username at the top:

```jsx
<div className="river-card-author">
  <div className="friend-avatar">{getInitials(user)}</div>
  <span className="friend-name">{user.username}</span>
</div>
```

### Card Types with Headers

| Location           | Clickable? | Notes                        |
| ------------------ | ---------- | ---------------------------- |
| Home feed posts    | ✅ Yes     | Navigate to author's profile |
| Friends feed cards | ✅ Yes     | Navigate to friend's profile |
| Own profile posts  | ❌ No      | Already on your profile      |

## Styling

```scss
.clickable-user {
  cursor: pointer;
  transition: all 0.2s ease;
  &:hover {
    filter: drop-shadow(0 0 8px var(--cyan));
    transform: scale(1.05);
  }
}

.clickable-friend:hover {
  background: rgba(79, 255, 255, 0.08);
  transform: translateX(4px);
}
```

## Files Involved

| File                   | Purpose                     |
| ---------------------- | --------------------------- |
| `App.jsx`              | Route definitions           |
| `TimelineRiverRow.jsx` | Home feed user clicks       |
| `TimelineRiver.jsx`    | Profile friends feed clicks |
| `_post-card.scss`      | Hover styles                |
