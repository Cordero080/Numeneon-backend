# Search Modal

## Overview

Global search accessible from TopBar for finding users and posts.

## Location

`frontend/src/components/layout/TopBar/SearchModal/`

## Search Targets

**Users** - Username, first name, last name, display name  
**Posts** - Post content, author username (limited to 10 results)

## Filter Tabs

- **All** - Both users and posts
- **Users (count)** - Only user results
- **Posts (count)** - Only post results

## Actions

| Result Type | Click Action | Message Icon |
|-------------|--------------|--------------|
| User | Navigate to `/profile/:username` | Open DM |
| Post | Navigate to author's profile | N/A |

## Data Sources

```jsx
const { posts } = usePosts();
const { friends } = useFriends();
const { openMessages } = useMessages();
```

Combines friends list + post authors for user search.

## Responsive Behavior

| Width | Behavior |
|-------|----------|
| > 768px | Centered modal with padding |
| ≤ 768px | Near-full width |
| ≤ 480px | Full screen |

## Keyboard

- **Escape** - Close modal and clear search
- Auto-focus search input on open
