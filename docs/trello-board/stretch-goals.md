# 🚀 NUMENEON - Stretch Goals

> Features planned for future development phases. Prioritized by impact and complexity.

---

## 📊 Priority Legend

| Priority      | Description                       |
| ------------- | --------------------------------- |
| 🔴 **HIGH**   | Core user experience enhancements |
| 🟡 **MEDIUM** | Profile completeness & analytics  |
| 🟢 **LOW**    | Nice-to-have, polish, easter eggs |

---

## ✅ Recently Completed (From Stretch Goals)

These were stretch goals that have been implemented:

- ✅ **Like/unlike posts** - `POST /api/posts/:id/like/` with heart animation
- ✅ **Reply to posts** - Threaded replies with inline & full-page composer
- ✅ **View posts by user** - Profile TimelineRiver shows user's posts by type
- ✅ **Share count tracking** - Backend field + RepostModal UI
- ✅ **User profile navigation** - Click any username/avatar to visit profile
- ✅ **Search modal** - Global search for users and posts
- ✅ **Direct messaging** - MessageModal with conversation list and chat view

---

## 🔴 HIGH PRIORITY

### SG-001: Bookmark System

**Status:** 📦 Placeholder (UI exists, no backend)

**Description:** Save posts for later viewing in a personal bookmark list.

**Tasks:**

- [ ] Create Bookmark model (user + post relationship)
- [ ] POST /api/posts/:id/bookmark/ endpoint
- [ ] GET /api/bookmarks/ endpoint (list user's bookmarks)
- [ ] DELETE /api/bookmarks/:id/ endpoint
- [ ] Wire BookmarkIcon click to API
- [ ] Bookmarks page/section on profile

**Complexity:** Medium  
**Backend:** Colin  
**Frontend:** Pablo

---

### SG-002: Repost/Quote Post

**Status:** 📝 Planned

**Description:** Create a new post that references the original post.

**Tasks:**

- [ ] Add `repost_of` field to Post model (ForeignKey to self)
- [ ] "Repost" creates a link post (no additional content)
- [ ] "Quote repost" allows adding commentary
- [ ] Display original post embedded in repost
- [ ] Track repost count on original

**Complexity:** Medium  
**Backend:** Colin  
**Frontend:** Pablo

---

### SG-003: Notifications System

**Status:** 📝 Planned

**Description:** Alert users when someone likes, comments, or follows them.

**Tasks:**

- [ ] Notification model (type, actor, target, read status)
- [ ] GET /api/notifications/ endpoint
- [ ] PATCH /api/notifications/:id/read/ endpoint
- [ ] NotificationModal bell icon with unread count
- [ ] Real-time updates (websockets - advanced)

**Complexity:** High  
**Backend:** Natalia  
**Frontend:** Pablo

---

## 🟡 MEDIUM PRIORITY

### SG-004: Profile Completion Ring

**Status:** 📦 Placeholder (decorative animation only)

**Description:** Dynamic progress ring around profile avatar showing completion percentage.

**Current Location:** `ProfileCardFront.jsx` (lines 78-101)

**Option A - Profile Completion %:**

- [ ] Has avatar? (+20%)
- [ ] Has bio? (+20%)
- [ ] Has location? (+15%)
- [ ] Has cover photo? (+20%)
- [ ] Has at least 1 post? (+10%)
- [ ] Has at least 1 friend? (+15%)

**Option B - Weekly Activity Score:**

- [ ] Posts created this week
- [ ] Likes given/received
- [ ] Comments made
- [ ] Profile views

**Complexity:** Low (Option A) / Medium (Option B)  
**Backend:** Natalia  
**Frontend:** Pablo

---

### SG-005: HUDDL Score (Reputation)

**Status:** 📋 Future

**Description:** Trust/reputation metric unique to NUMENEON.

**Features:**

- Score range: 0-100
- Factors: Post quality, engagement rate, consistency
- Display: Badge on profile stats row

**Backend Needs:**

- User activity logging
- Weighted scoring algorithm
- Historical score tracking

**Complexity:** High  
**Owner:** TBD

---

### SG-006: Post Insights / Analytics

**Status:** 📋 Future

**Description:** View count and engagement rate per post.

**Features:**

- View count tracking (anonymous)
- Engagement rate calculation
- "X people viewed this" display
- GraphLineIcon button wired to modal

**Backend Needs:**

- Post view event logging
- Time-windowed aggregations

**Complexity:** Medium  
**Backend:** Colin  
**Frontend:** Pablo

---

### SG-007: Best Posting Time Analysis

**Status:** 📋 Future

**Description:** AI-powered optimal posting time recommendations.

**Features:**

- Analyze when user's posts get most engagement
- Show: "Peak Hour: 8 PM, Peak Day: Thursday"
- Visualize as small bar chart on ProfileCardBack

**Backend Needs:**

- Post timestamp + engagement correlation
- Pattern detection algorithm

**Complexity:** High  
**Owner:** TBD

---

## 🟢 LOW PRIORITY

### SG-008: MySpace Easter Egg - Throwback Mode

**Status:** 📋 Future (Fun feature!)

**Description:** Nostalgic easter egg that adds MySpace-inspired features.

**Phase 1 - Basic Toggle (15 min):**

- [ ] `throwbackMode` state in ProfileCard
- [ ] Toggle in Quick Settings
- [ ] Retro CSS effects (scanlines, CRT glow)

**Phase 2 - Top 8 Friends (1-2 hours):**

- [ ] `Top8Friends` component
- [ ] Friend selection modal
- [ ] 8 avatar grid on profile
- [ ] Drag-and-drop reordering
- [ ] Backend: `top_friends` JSON field

**Phase 3 - Profile Song (2-3 hours):**

- [ ] `ProfileSong` component with audio player
- [ ] Song picker modal (Spotify/SoundCloud embed)
- [ ] Autoplay toggle (respect user preference)
- [ ] Cassette tape / vinyl record animation

**Complexity:** Low → Medium (per phase)  
**Owner:** Pablo (stretch goal)

---

### SG-009: Video Posts

**Status:** 📋 Future

**Description:** Support video upload/embed in media posts.

**Tasks:**

- [ ] Video URL field or file upload
- [ ] Video player component
- [ ] Thumbnail generation
- [ ] Autoplay on scroll (muted)

**Complexity:** High  
**Owner:** TBD

---

### SG-010: Image Galleries

**Status:** 📋 Future

**Description:** Multiple images per post with carousel/grid display.

**Tasks:**

- [ ] `media_urls` JSON field (array of URLs)
- [ ] Gallery display in PostCard
- [ ] MediaLightbox carousel navigation
- [ ] Upload multiple images

**Complexity:** Medium  
**Owner:** TBD

---

### SG-011: GIF Picker

**Status:** 📋 Future

**Description:** Integration with Giphy/Tenor for GIF selection.

**Tasks:**

- [ ] GIF picker modal in composer
- [ ] Giphy/Tenor API integration
- [ ] Search and trending GIFs
- [ ] Insert GIF as media_url

**Complexity:** Medium  
**Owner:** TBD

---

### SG-012: Hashtag System

**Status:** 📋 Future

**Description:** Parse hashtags from post content, create tag pages.

**Tasks:**

- [ ] Hashtag parsing on post creation
- [ ] Hashtag model (or JSON field)
- [ ] Hashtag pages showing all posts with tag
- [ ] Clickable hashtags in post content
- [ ] Trending hashtags

**Complexity:** Medium  
**Backend:** Colin  
**Frontend:** Pablo

---

### SG-013: Virality Score

**Status:** 📋 Future

**Description:** Measures how quickly posts gain traction.

**Features:**

- Score: 1-10 scale
- Calculation: Interaction speed within first hour/day
- High score = rapid engagement growth

**Backend Needs:**

- Interaction timestamps
- Engagement velocity calculations

**Complexity:** Medium  
**Owner:** TBD

---

### SG-014: Profile Views Tracking

**Status:** 📋 Future

**Description:** Show profile visit statistics.

**Features:**

- Last 7 days view count
- Anonymous tracking (don't reveal who viewed)
- Display: "🔍 241 profile views this week"

**Complexity:** Low  
**Backend:** Natalia  
**Frontend:** Pablo

---

## 📋 Stretch Goal Status Summary

| ID     | Name               | Priority  | Status         | Owner         |
| ------ | ------------------ | --------- | -------------- | ------------- |
| SG-001 | Bookmark System    | 🔴 HIGH   | 📦 Placeholder | Colin/Pablo   |
| SG-002 | Repost/Quote Post  | 🔴 HIGH   | 📝 Planned     | Colin/Pablo   |
| SG-003 | Notifications      | 🔴 HIGH   | 📝 Planned     | Natalia/Pablo |
| SG-004 | Profile Ring       | 🟡 MEDIUM | 📦 Placeholder | Natalia/Pablo |
| SG-005 | HUDDL Score        | 🟡 MEDIUM | 📋 Future      | TBD           |
| SG-006 | Post Insights      | 🟡 MEDIUM | 📋 Future      | Colin/Pablo   |
| SG-007 | Best Post Time     | 🟡 MEDIUM | 📋 Future      | TBD           |
| SG-008 | MySpace Easter Egg | 🟢 LOW    | 📋 Future      | Pablo         |
| SG-009 | Video Posts        | 🟢 LOW    | 📋 Future      | TBD           |
| SG-010 | Image Galleries    | 🟢 LOW    | 📋 Future      | TBD           |
| SG-011 | GIF Picker         | 🟢 LOW    | 📋 Future      | TBD           |
| SG-012 | Hashtag System     | 🟢 LOW    | 📋 Future      | Colin/Pablo   |
| SG-013 | Virality Score     | 🟢 LOW    | 📋 Future      | TBD           |
| SG-014 | Profile Views      | 🟢 LOW    | 📋 Future      | Natalia/Pablo |

---

## 📌 Status Legend

- **📝 Planned** - Designed, ready for implementation
- **📦 Placeholder** - UI exists, needs backend
- **📋 Future** - Nice to have, not prioritized
- **🔄 In Progress** - Currently being worked on
- **✅ Done** - Completed

---

_Last Updated: January 8, 2026_
