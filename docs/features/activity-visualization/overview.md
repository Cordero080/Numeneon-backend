# Activity Visualization Feature

## Overview

The Activity Visualization component provides users with visual analytics of their posting activity over time, rendered on the back of the profile flip card.

---

## 📊 What Each Visualization Shows (Simple Explanation)

### 🌊 Wave Chart - "Your Engagement Over Time"

**What it shows:** How much people interacted with your posts over the past year.

**In plain English:**

- Imagine a mountain range where taller peaks = more engagement
- **Top wave (blue/cyan):** Total engagement (likes + comments + shares combined)
- **Middle wave (pink):** Just your likes
- **Bottom wave (orange):** Just your comments

**How to read it:**

- Higher peaks = weeks when your posts got lots of attention
- Flat areas = quiet weeks with less interaction
- Green dots mark your best weeks

**Example:** If you posted something viral in March, you'll see a big spike in that area of the chart.

---

### 📅 Heatmap - "When Do You Post?"

**What it shows:** A calendar view of how often you posted each day over the past year.

**In plain English:**

- It's like a GitHub contribution graph but for your posts
- Each tiny square = one day
- Darker squares = you posted more that day
- Lighter/empty squares = you didn't post much

**How to read it:**

- **Rows:** Days of the week (Monday at top, Sunday at bottom)
- **Columns:** Weeks of the year (oldest on left, newest on right)
- **Colors:** Empty → Light blue → Cyan → Bright cyan (more posts)

**Example:** If you always post on Saturdays, you'll see a horizontal stripe of dark squares on the Saturday row.

---

### 🍩 Content Mix Donut Chart

**What it shows:** What types of posts you create most.

**In plain English:**

- A pie chart showing the breakdown of your content
- **Green:** Thoughts (text-only posts)
- **Blue:** Media (posts with images)
- **Pink:** Milestones (achievement posts)

**Example:** If 60% of your posts are Thoughts, the green section will be the biggest slice.

---

### ⚡ Peak Posting Time

**What it shows:** When you're most active.

**In plain English:**

- Analyzes your posting history to find your busiest day and time
- Shows something like "Sat 6PM" meaning you tend to be most active Saturday evenings

---

## Visual Components

### Wave View

- **Smooth area chart** showing activity trends over 52 weeks
- **Three stacked layers** with gradient fills:
  - High activity wave (top layer)
  - Medium activity wave (middle layer)
  - Low activity wave (bottom layer)
- **Dynamic peak detection** displaying optimal posting time (e.g., "Peak Sat 7PM")
- **Interactive toggle buttons** to switch between Wave and Grid views

### Grid/Heatmap View

- **GitHub-style contribution calendar** showing 52 weeks of activity
- **Color-coded intensity levels**:
  - Light gray = low/no activity
  - Light blue = low-medium activity
  - Medium cyan = medium-high activity
  - Bright cyan = high activity
- **Grid layout**: Days of week (Y-axis) × Weeks/Months (X-axis)
- **Consistent toggle interface** matching Wave view

## Top Stats Cards

Both views display the same analytics header:

1. **Profile Views** - Total profile impressions (2.4K)
2. **Engagement Rate** - User interaction percentage (89%)
3. **Avg. Likes/Post** - Average likes per post (156)
4. **Growth This Week** - Weekly growth metric (+23%)

## Technical Implementation

### Data Source

All visualization data is calculated from the `posts` array passed to ProfileCard. No separate API call needed!

**Data comes from PostsContext:**

```javascript
// ProfileCard receives posts from parent
function ProfileCard({ posts, user }) {
  // Calculate visualizations from posts array
}
```

**Required Post Fields:**

```json
{
  "id": 1,
  "type": "thought", // For donut chart
  "created_at": "2024-12-19", // For heatmap calendar
  "likes_count": 42, // For wave chart
  "comments_count": 7, // For wave chart
  "shares_count": 3 // For wave chart
}
```

### How Each Visualization is Calculated

**Wave Chart (waveData):**

```javascript
// Sum engagement per week for the past 52 weeks
posts.forEach((post) => {
  const engagement = post.likes_count + post.comments_count + post.shares_count;
  weeklyEngagement[weekIndex] += engagement;
});
```

**Heatmap (heatmapData):**

```javascript
// Count posts per day, convert to 0-3 intensity levels
// 0 posts = level 0, 1 post = level 1, 2-3 posts = level 2, 4+ posts = level 3
```

**Donut Chart (postTypeData):**

```javascript
// Count posts by type, calculate percentages
const thoughtsPercent = (counts.thoughts / total) * 100;
```

### Rendering

Activity visualization happens **client-side in the browser** using JavaScript charting libraries. This is NOT a 3rd party API - it's a visualization library rendering YOUR data.

**Current implementation uses:**

- Custom SVG path generation for wave charts
- Seeded random number generator for consistent demo data
- Pure React/JavaScript (no external charting dependencies in current version)

**Could be enhanced with libraries like:**

- **Recharts** - Simple React charting library
  ```javascript
  import { AreaChart, Area } from "recharts";
  ```
- **D3.js** - Advanced custom visualizations
  ```javascript
  import * as d3 from "d3";
  ```
- **React Calendar Heatmap** - GitHub-style contribution grids
  ```javascript
  import CalendarHeatmap from "react-calendar-heatmap";
  ```

### Component Structure

```
ActivityVisualization.jsx
├── View mode toggle (Wave/Grid)
├── Peak time badge
├── Wave chart (SVG paths)
│   ├── High activity layer
│   ├── Medium activity layer
│   └── Low activity layer
└── Heatmap grid (52 weeks × 7 days)
```

### Data Flow

1. **User posts content** → Django saves to database
2. **React component mounts** → Requests `/api/user/activity`
3. **Django returns activity metrics** → JSON response
4. **Visualization library renders** → Charts appear in browser
5. **User toggles view** → Re-renders with different visualization

## Key Features

### No External Dependencies

- ✅ Data comes from YOUR Django backend
- ✅ Visualization happens in the browser
- ✅ No HTTP requests to external services
- ✅ All activity data belongs to YOUR users

### Privacy-Focused

- Activity analytics only visible on **profile card back** (private view)
- Not exposed to other users
- Personal insights dashboard

### Performance

- Data generated once per component mount
- Memoized calculations prevent unnecessary re-renders
- Lightweight SVG rendering

## Future Enhancements

### Potential Features

- Export activity data as CSV/JSON
- Configurable date ranges (last 30 days, 6 months, all time)
- Activity streaks and milestones
- Drill-down into specific days/weeks
- Compare activity across different post types

### If External Data Needed (Future)

Only necessary if adding features like:

- **GitHub integration**: Pull actual GitHub contributions
  ```javascript
  fetch("https://api.github.com/users/username/events");
  ```
- **Industry benchmarks**: Compare engagement to platform averages
  ```javascript
  fetch("https://analytics-api.com/social-media-benchmarks");
  ```

But for core Numeneon user activity visualization: **No 3rd party APIs required.**

## Component Files

- `/frontend/src/components/pages/Profile/components/ProfileCard/components/ActivityVisualization/`
  - `ActivityVisualization.jsx` - Renders wave chart and heatmap
  - `ActivityVisualization.scss` - Styles
- `/frontend/src/components/pages/Profile/components/ProfileCard/components/PostTypeBreakdown/`
  - `PostTypeBreakdown.jsx` - Renders donut chart
- Parent: `ProfileCardBack.jsx`
- Data calculation: `ProfileCard.jsx` (from real post data)

## Summary

This is a **visualization system** that transforms your real post data into beautiful, interactive charts:

| Visualization | Data Used                                       | What It Shows              |
| ------------- | ----------------------------------------------- | -------------------------- |
| Wave Chart    | `likes_count`, `comments_count`, `shares_count` | Engagement over 52 weeks   |
| Heatmap       | `created_at`                                    | Posting frequency calendar |
| Donut Chart   | `type`                                          | Content type breakdown     |
| Peak Time     | Heatmap analysis                                | Most active day/time       |

All processing happens **client-side in the browser** - no external APIs needed!
