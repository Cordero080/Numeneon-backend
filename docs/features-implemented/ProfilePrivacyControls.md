# Profile Privacy Controls

## Overview

When viewing another user's profile, edit/delete controls are hidden.

## Detection Logic

```jsx
const { username: profileUsername } = useParams();
const isOwnProfile = !profileUsername || profileUsername === currentUser?.username;
```

- `/profile` → Own profile
- `/profile/{yourUsername}` → Own profile  
- `/profile/{otherUsername}` → Other's profile

## Conditional Elements

### Shown Only on Own Profile

| Element | Purpose |
|---------|---------|
| Post Composer | Write new posts |
| Friends Feed Toggle | Switch between views |
| Edit Button | Edit existing posts |
| Delete Button | Delete posts |

### Implementation

```jsx
{isOwnProfile && <PostComposer user={currentUser} />}

{isOwnProfile && (
  <div className="post-actions">
    <button onClick={(e) => handleEdit(e, post)}>✎</button>
    <button onClick={(e) => handleDelete(e, post.id)}>✕</button>
  </div>
)}
```

## Visible on All Profiles

✅ Profile picture, bio, Activity Heatmap, Timeline posts (read-only), Like/comment icons

❌ Post composer, Edit/delete buttons, Friends Feed toggle, Settings

## Files

| File | Changes |
|------|---------|
| `Profile.jsx` | `isOwnProfile` logic, conditional rendering |
| `TimelineRiver.jsx` | `isOwnProfile` prop for edit/delete buttons |
