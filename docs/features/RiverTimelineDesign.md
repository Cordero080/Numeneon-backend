# River Timeline: Condensed Feed Design

## Overview

The River Timeline is a revolutionary approach to social media feeds that solves the "feed clutter" problem caused by prolific posters. Instead of displaying posts in a scattered, chronological waterfall, posts are **organized by user and category**, then **condensed into navigable carousel rows**.

---

## The Problem with Traditional Feeds

In conventional social media feeds, posts appear in strict chronological order:

```
┌─────────────────────────────┐
│ @alice: "Just woke up"      │  ← 9:05am
├─────────────────────────────┤
│ @bob: Photo of sunset       │  ← 9:04am
├─────────────────────────────┤
│ @alice: "Making coffee"     │  ← 9:03am
├─────────────────────────────┤
│ @charlie: "Big news!"       │  ← 9:02am
├─────────────────────────────┤
│ @alice: Photo of coffee     │  ← 9:01am
├─────────────────────────────┤
│ @alice: "Best morning ever" │  ← 9:00am
└─────────────────────────────┘
```

**Problems:**

1. **Feed Domination**: Alice posted 4 times in 5 minutes, drowning out Bob and Charlie
2. **Subconscious Irritation**: Users may grow tired of seeing the same person repeatedly
3. **Scroll Fatigue**: Important posts get buried under high-volume posters
4. **Perception vs Reality**: A person who posts frequently online may seem "annoying" even if they're perfectly pleasant in real life

---

## The River Timeline Solution

The River Timeline condenses a user's posts into **category-based rows with carousels**:

```
┌──────────────────────────────────────────────────────────────────┐
│                         @alice                                    │
├────────────────────┬────────────────────┬────────────────────────┤
│     THOUGHTS       │       MEDIA        │      MILESTONES        │
│  ┌──────────────┐  │  ┌──────────────┐  │  ┌──────────────────┐  │
│  │ "Best morn.."│  │  │ [☕ photo]   │  │  │  No milestones   │  │
│  │              │  │  │              │  │  │                  │  │
│  └──────────────┘  │  └──────────────┘  │  └──────────────────┘  │
│     ◀ ●●○○ ▶      │      ◀ ●○ ▶       │                        │
│     (4 posts)      │     (2 posts)      │                        │
└────────────────────┴────────────────────┴────────────────────────┘
```

**Benefits:**

1. **One Row Per User**: Alice takes 1 row instead of 4
2. **Category Organization**: Thoughts, Media, and Milestones are separated
3. **Carousel Navigation**: Dots show count; arrows navigate between posts
4. **Equal Visibility**: Every friend gets fair representation

---

## Row-Chunking Algorithm

When a category exceeds 12 posts, it creates a new row. **Newest posts appear at the top.**

### Example: User with 15 thoughts, 3 media, 1 milestone

```
ROW 1 (NEWEST):
┌────────────────────┬────────────────────┬────────────────────────┐
│     THOUGHTS       │       MEDIA        │      MILESTONES        │
│  Posts 1-3 (new)   │   Posts 1-3        │     Post 1             │
│     ◀ ●●● ▶        │     ◀ ●●● ▶        │       ● (1)            │
└────────────────────┴────────────────────┴────────────────────────┘

ROW 2 (OLDER):
┌────────────────────┬────────────────────┬────────────────────────┐
│     THOUGHTS       │       MEDIA        │      MILESTONES        │
│  Posts 4-15 (old)  │     (empty)        │       (empty)          │
│   ◀ ●●●●●●●●●●●● ▶ │                    │                        │
│      (12 posts)    │                    │                        │
└────────────────────┴────────────────────┴────────────────────────┘
```

### Chunking Logic (Pseudocode)

```javascript
const CAROUSEL_LIMIT = 12;

function chunkPostsIntoRows(posts) {
  if (posts.length <= 12) return [posts];

  const rows = [];
  const remainder = posts.length % 12;

  // First row gets the remainder (newest posts)
  if (remainder > 0) {
    rows.push(posts.slice(0, remainder));
  }

  // Remaining rows get 12 each
  for (let i = remainder; i < posts.length; i += 12) {
    rows.push(posts.slice(i, i + 12));
  }

  return rows;
}
```

**Why remainder first?**

- Posts are sorted newest-first from the API
- The remainder represents the most recent posts
- Users see newest content at the top

---

## Visual Space Distribution

When a user has fewer categories, columns redistribute:

| Categories Present                  | Layout                 |
| ----------------------------------- | ---------------------- |
| All 3 (thoughts, media, milestones) | Equal thirds           |
| 2 categories                        | 50/50 split            |
| 1 category                          | Centered or full width |

This ensures no wasted visual space while maintaining clarity.

---

## UX Benefits

### 1. **Reduced Feed Anxiety**

Users no longer feel overwhelmed by prolific posters. The carousel condenses activity into a manageable, skimmable format.

### 2. **Fair Representation**

Every friend gets equal visual weight in the feed, regardless of posting frequency.

### 3. **Intentional Engagement**

Users actively choose to explore a friend's posts via the carousel, rather than passively scrolling past them.

### 4. **Content Discovery**

The category separation helps users find what they're looking for (e.g., "I want to see Sarah's photos, not her random thoughts").

### 5. **Reduced Social Friction**

The "annoyance illusion" is eliminated. A friend who posts 20 times a day takes the same visual space as one who posts once a week.

---

## Technical Implementation

### Components

| Component               | Purpose                                 |
| ----------------------- | --------------------------------------- |
| `RiverTimelineView.jsx` | Own profile timeline with row-chunking  |
| `RiverFeedView.jsx`     | Friends feed with per-user row-chunking |
| `RiverSmartDeck.jsx`    | Carousel navigation (arrows + dots)     |

### Key Constants

```javascript
const CAROUSEL_LIMIT = 12; // Max posts per carousel before new row
```

### State Management

Deck indices are stored per-user, per-category, per-row:

```javascript
const deckIndices = {
  "alice-thoughts-row0": 2, // Alice's newest thoughts, viewing post #3
  "alice-thoughts-row1": 0, // Alice's older thoughts, viewing post #1
  "bob-media-row0": 5, // Bob's media, viewing post #6
};
```

---

## Performance Considerations

1. **Lazy Rendering**: Only the currently visible post in each carousel is fully rendered
2. **Memoization**: `chunkPostsIntoRows` results are cached per render cycle
3. **Pagination-Ready**: The row system naturally supports infinite scroll pagination

---

## Future Enhancements

- [ ] Swipe gesture support for mobile carousels
- [ ] "See all" expansion for power users who want the traditional view
- [ ] Animated transitions between carousel items
- [ ] Row collapse/expand for very long feeds

---

## Conclusion

The River Timeline transforms social media consumption from passive scrolling to intentional browsing. By condensing posts into user-centric, category-organized rows, it creates a more equitable, less anxiety-inducing feed experience.

**The philosophy**: Your friend who posts 5 times a day isn't annoying—the traditional feed design made them seem that way.
