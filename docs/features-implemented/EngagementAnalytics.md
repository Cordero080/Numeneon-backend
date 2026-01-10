# Engagement Analytics

## Overview

Visual representations of user activity through heatmaps and engagement data on the ProfileCard back.

## Components

### Activity Heatmap (ActivityVisualization.jsx)

GitHub-style contribution grid showing daily activity levels.

**Location:** `ProfileCard/components/ActivityVisualization/`

**Activity Levels:**

| Level | Range | Color |
|-------|-------|-------|
| 0 | Empty | Transparent |
| 1 | 1-400 | `rgba(79, 255, 255, 0.2)` |
| 2 | 401-800 | `rgba(79, 255, 255, 0.4)` |
| 3 | 801-1500 | `rgba(79, 255, 255, 0.7)` |
| 4 | 1500+ | `var(--cyan)` with glow |

### Post Type Breakdown (PostTypeBreakdown.jsx)

Shows distribution of user's content types (thoughts, media, milestones).

**Location:** `ProfileCard/components/PostTypeBreakdown/`

## Key Implementation

```jsx
// Heatmap cell rendering
<div className={`heatmap-cell level-${day.level}`} 
     title={`${day.date}: ${day.count} interactions`} />
```

## Data

Currently uses mock data with engagement tiers:
- 50% chance low activity
- 35% chance medium  
- 15% chance high

**Future:** Will use real post/like/comment timestamps from API.

## Files

| Component | Purpose |
|-----------|---------|
| `ActivityVisualization/` | GitHub-style contribution grid |
| `PostTypeBreakdown/` | Content type pie/bar chart |
| `QuickSettings/` | Profile settings panel |
