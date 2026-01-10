# River Timeline Feature

## Overview

The River Timeline is Numeneon's signature feed display that groups posts by user into rows with carousel navigation. Each row holds up to 12 posts per category. When any category fills up, a fresh new row is created for that user — the old row stays in the feed, just further down.

---

## 🌊 The "River" Concept

Imagine three parallel streams flowing down your feed:

| Left Stream     | Center Stream | Right Stream  |
| --------------- | ------------- | ------------- |
| 💭 Thoughts     | 🖼️ Media      | 🏆 Milestones |
| Text-only posts | Image/video   | Achievements  |

Each **row = one user + one epoch**. An epoch is a batch of posts (max 12 per category). When any category hits 12, the row is "sealed" and a new epoch begins. Rows are sorted by **most recent activity** — the row with the newest post appears at the top.

### Epoch Example

```
User A posts 12 thoughts, 3 media, 0 milestones → Epoch 1 sealed (thoughts maxed)
User A posts 2 more thoughts, 1 media         → Epoch 2 created at top

Feed looks like:
┌─────────────────────────────────────────────┐
│ User A - Epoch 2 (newest)                   │
│ [Thoughts 2/12] [Media 1/12] [Milestones 0] │
├─────────────────────────────────────────────┤
│ User B - Epoch 1                            │
│ [Thoughts 5/12] [Media 2/12] [Milestones 1] │
├─────────────────────────────────────────────┤
│ User A - Epoch 1 (sealed, scroll to find)   │
│ [Thoughts 12/12] [Media 3/12] [Milestones 0]│
└─────────────────────────────────────────────┘
```

**Key points:**

- Categories are **independent** — thoughts hitting 12 doesn't cap media/milestones in that row
- Old rows **persist** in the feed (scrollable history)
- Each row sorted by its **most recent post timestamp**

---

## ✨ Key Design Principles

### 1. Space Economy

**Problem:** Traditional feeds show one post per row, creating infinite scroll fatigue.

**Solution:** Group posts from the same user into rows with carousel navigation. Each row can hold up to 12 posts per category before a new row is created.

```
Traditional Feed:          River Timeline (with epochs):
┌─────────────────┐        ┌───────┬───────┬───────┐
│ User A - Post 1 │        │ UserA │ UserA │ UserA │
├─────────────────┤        │ Ep2   │ Ep2   │ Ep2   │ ← Newest epoch
│ User B - Post 1 │        │ ◀ 2/12│ ◀ 1/12│       │
├─────────────────┤        ├───────┼───────┼───────┤
│ User A - Post 2 │        │ UserB │ UserB │ UserB │
├─────────────────┤        │ Ep1   │ Ep1   │ Ep1   │
│ User A - Post 3 │        │ ◀ 5/12│ ◀ 3/12│ ◀ 1/12│
├─────────────────┤        ├───────┼───────┼───────┤
│ ...13 more...   │        │ UserA │ UserA │ UserA │
└─────────────────┘        │ Ep1   │ Ep1   │ Ep1   │ ← Sealed (thoughts=12)
                           │ 12/12 │ ◀ 3/12│       │
                           └───────┴───────┴───────┘
```

### 2. Content Type Separation

Each column has a distinct purpose:

- **Thoughts (cyan/left):** Quick text updates, reflections, quotes
- **Media (purple/center):** Photos, videos, visual content
- **Milestones (green/right):** Achievements, life events, celebrations

### 3. Epoch System (MAX_POSTS_PER_TYPE = 12)

To keep carousels navigable while allowing infinite scrolling:

- Maximum **12 posts per type** per row (epoch)
- When **any category hits 12**, that row is "sealed"
- A **fresh new row** is created for that user's next post
- Old rows **stay in the feed** — just further down as you scroll
- Categories are **independent** — thoughts filling doesn't affect media/milestones in that row

### 4. Carousel Navigation

Chamfered nav buttons with neon glow effects, dimmed by default until hovered:

```jsx
// Arrows appear when posts.length > 1
{
  posts.length > 1 && (
    <div className="smart-deck-nav">
      <button className="smart-deck-nav-btn" onClick={prevCard}>
        ◀
      </button>
      <div className="smart-deck-dots">{/* position indicators */}</div>
      <button className="smart-deck-nav-btn" onClick={nextCard}>
        ▶
      </button>
    </div>
  );
}
```

---

## 🔧 Technical Implementation

### Grouping Logic (Epoch-Based)

Located in `frontend/src/components/pages/Home/utils/groupPosts.js`:

```javascript
// Maximum posts per type in carousel (prevents excessive clicking)
const MAX_POSTS_PER_TYPE = 12;

export const groupPostsByUserAndEpoch = (posts, options = {}) => {
  const maxPosts = options.maxPostsPerType ?? MAX_POSTS_PER_TYPE;

  // Track epochs per user: { userId: [epoch1, epoch2, ...] }
  const userEpochs = {};

  // Sort posts oldest-first so we fill epochs chronologically
  const sortedPosts = [...posts].sort(
    (a, b) => new Date(a.created_at) - new Date(b.created_at)
  );

  sortedPosts.forEach((post) => {
    const userId = post.userId || post.author?.id || post.author;
    const type = post.type || "thoughts";

    if (!userEpochs[userId]) {
      userEpochs[userId] = [];
    }

    // Find the latest epoch that can still accept this post type
    let targetEpoch = userEpochs[userId].find(
      (epoch) => epoch[type].length < maxPosts
    );

    // If no epoch has room, create a new one
    if (!targetEpoch) {
      targetEpoch = {
        user: { id: userId, name: post.author?.username },
        epochIndex: userEpochs[userId].length,
        thoughts: [],
        media: [],
        milestones: [],
        mostRecentTimestamp: 0,
      };
      userEpochs[userId].push(targetEpoch);
    }

    // Add post to the epoch
    targetEpoch[type].push(post);
    targetEpoch.mostRecentTimestamp = Math.max(
      targetEpoch.mostRecentTimestamp,
      new Date(post.created_at).getTime()
    );
  });

  // Flatten all epochs into a single array
  return Object.values(userEpochs).flat();
};

export const sortGroupedPosts = (grouped) => {
  // Sort by most recent post timestamp (newest first)
  return grouped.sort((a, b) => b.mostRecentTimestamp - a.mostRecentTimestamp);
};
```

### Epoch Logic Explained

**When does a new epoch get created?**

A new row (epoch) is created when the current epoch can't fit the new post:

- If `thoughts` has 12 posts and user posts another thought → new epoch
- If `media` has 12 posts and user posts another media → new epoch
- If `milestones` has 12 posts and user posts another milestone → new epoch

**Categories are independent:**

- User has 12 thoughts, 3 media, 0 milestones in Epoch 1
- User posts a new media → goes into Epoch 1 (media only has 3)
- User posts a new thought → creates Epoch 2 (thoughts is full)

### Why Epoch-Based Grouping?

**Previous (flawed):** Grouped by `userId` only

- ❌ Users with 50+ posts had unusable carousels
- ❌ Capped at 12 meant content was hidden
- ❌ No way to scroll through older content

**Current (correct):** Grouped by `userId + epoch`

- ✅ Each row = max 12 per category (manageable carousel)
- ✅ New epochs create fresh rows at top
- ✅ Old rows stay in feed (scrollable history)
- ✅ Categories independent within each epoch
- ✅ Users can scroll to find older epochs

### Why Recency Sorting (Pure, No Engagement Weighting)?

Rows are sorted by **most recent post timestamp only**. Reactions/likes do NOT affect visibility.

**Why pure recency (not engagement-weighted)?**

- ✅ Predictable: users know exactly why content is where it is
- ✅ Fair: avoids "rich get richer" where popular users dominate forever
- ✅ No gaming: can't manipulate feed position with fake engagement
- ✅ Simple: easy to implement, debug, and reason about

**Design decision:** Fresh content rises, old content sinks. No algorithmic boosting.

---

## 📱 Profile Page Integration

The Profile page uses River Timeline differently:

```
┌─────────────────────────────────┐
│      Profile Card (header)       │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│   River Timeline (carousel)      │
│   [Thoughts] [Media] [Milestones]│
│    max 12 per type, arrows       │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│        All Posts Section         │
│  Chronological list (unlimited)  │
│  ┌─────────────────────────────┐│
│  │ Post (newest)               ││
│  └─────────────────────────────┘│
│  ┌─────────────────────────────┐│
│  │ Post                        ││
│  └─────────────────────────────┘│
│         ... (scroll)             │
└─────────────────────────────────┘
```

- **River Timeline:** Quick category preview (max 12 per type)
- **All Posts:** Full chronological feed for deep exploration

---

## 🗂️ Component Structure

```
frontend/src/components/pages/Home/
├── Home.jsx                    # Main page
├── utils/
│   └── groupPosts.js           # Grouping logic (MAX_POSTS=12)
└── components/
    ├── TimelineRiverFeed/
    │   └── TimelineRiverFeed.jsx    # Renders grouped rows
    └── TimelineRiverRow/
        ├── TimelineRiverRow.jsx     # Single user row with smart decks
        └── styles/
            ├── _smart-deck.scss     # Chamfered nav buttons
            ├── _carousel.scss       # Mobile carousel
            └── _responsive.scss     # Responsive breakpoints

frontend/src/components/pages/Profile/
├── Profile.jsx                      # Profile page with All Posts section
└── components/
    └── TimelineRiver/
        └── TimelineRiver.jsx        # Profile-specific timeline
```

---

## 🎯 Why This Design is Efficient

| Benefit                    | Description                                                  |
| -------------------------- | ------------------------------------------------------------ |
| **Scan Speed**             | See 10 users at a glance vs scrolling through 30+ posts      |
| **Context Grouping**       | User's content grouped per epoch, not scattered              |
| **Type Discovery**         | Quickly see if someone posts thoughts vs media vs milestones |
| **Scrollable History**     | Old epochs stay in feed — scroll to find them                |
| **Carousel Depth**         | Click arrows to explore without leaving the row              |
| **Capped at 12**           | Each row manageable (12 clicks max per type)                 |
| **Independent Categories** | Thoughts filling doesn't block media/milestones in same row  |
| **Fresh Content**          | New posts create new epochs that rise to top                 |
| **No Rich-Get-Richer**     | Pure recency sorting — no engagement manipulation            |

---

## 🎨 Visual Design

### Carousel Buttons

- **Chamfered corners** (not hexagonal)
- **Dimmed by default** (opacity: 0.5)
- **Neon glow on hover** (type-specific colors)
- **Smooth transitions** (0.3s cubic-bezier)

### Dot Indicators

- **Square with rounded corners** (8px default, 24px active)
- **Gradient fill when active** (matches type color)
- **Neon box-shadow glow**

### Type Colors

| Type       | Color            | Glow                     |
| ---------- | ---------------- | ------------------------ |
| Thoughts   | Cyan (#4fffff)   | rgba(79, 255, 255, 0.6)  |
| Media      | Purple (#c9a8ff) | rgba(201, 168, 255, 0.6) |
| Milestones | Green (#1ae784)  | rgba(26, 231, 132, 0.6)  |

---

## 🔗 Related Features

- **Activity Visualization:** Wave chart and heatmap on Profile Card
- **Profile Card:** Flip card with analytics on back
- **All Posts Section:** Chronological feed below River Timeline on Profile

---

## Summary

The River Timeline transforms a traditional endless feed into a structured, scannable view where:

1. **One row = one user + one epoch** (space economy with scrollable history)
2. **Three columns = three content types** (visual organization)
3. **Max 12 per category per row** (manageable carousels)
4. **New epoch when any category fills** (fresh rows appear at top)
5. **Categories are independent** (thoughts filling doesn't cap media/milestones)
6. **Pure recency sorting** (no engagement-based manipulation)
7. **Old epochs persist** (scroll down to find them)

This design respects users' time while preserving content richness and avoiding algorithmic "rich get richer" dynamics.
