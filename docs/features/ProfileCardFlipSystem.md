# ProfileCard Flip System

## Overview

The NUMENEON ProfileCard uses a 3D flip-card architecture to separate public profile information (front) from private analytics (back). This creates an elegant user experience while providing deep activity insights when needed.

---

## Component Architecture

```
ProfileCard/
├── ProfileCard.jsx          # Main container - orchestrates flip & data
├── ProfileCard.scss
├── index.js
└── components/
    ├── ActivityVisualization/
    │   ├── ActivityVisualization.jsx    # Wave chart + Heatmap toggle
    │   └── ActivityVisualization.scss
    ├── PostTypeBreakdown/
    │   ├── PostTypeBreakdown.jsx        # Donut chart for content mix
    │   └── PostTypeBreakdown.scss
    ├── ProfileCardBack/
    │   ├── ProfileCardBack.jsx          # Back face container
    │   └── ProfileCardBack.scss
    ├── ProfileCardFront/
    │   ├── ProfileCardFront.jsx         # Front face (user info)
    │   └── ProfileCardFront.scss
    └── QuickSettings/
        ├── QuickSettings.jsx            # Settings buttons grid
        └── QuickSettings.scss
```

---

## Front Card - Public Profile View

### Header Section

- **Banner Background**: Gradient overlay with glassmorphic fade effect
- **Avatar**: 150px circular avatar with futuristic glow ring
  - Tri-color gradient glow (green/blue/magenta)
  - Glassmorphic backdrop blur effect
  - Positioned to overlap banner
  - **Engagement Ring**: SVG progress ring showing activity level

### Profile Information

- **Name & Handle**: Display name with @username handle
- **Bio**: Multi-line user biography
- **Location**: Geographic location with pin icon
- **Website Link**: Clickable external link
- **Join Date**: Account creation date with calendar icon

### Stats Row

Positioned directly below profile details for quick insights:

- **Following**: Number of users this person follows
- **Followers**: Number of users following this person
- **Posts**: Total number of posts created
- Each stat includes subtle glow effect on hover

### Action Buttons

Glassmorphic pill container in top-right with three actions:

- **Share Profile**: Share user profile externally
- **More Options**: Additional profile actions menu
- **Analytics**: Flip card to reveal analytics dashboard

---

## Back Card - Private Analytics Dashboard

### Analytics Grid

Four key metrics displayed in a glassmorphic grid:

1. **Profile Views** (2.4K) - Eye icon, total views count
2. **Engagement Rate** (89%) - Lightning bolt, interaction percentage
3. **Avg. Likes/Post** (156) - Heart icon, average engagement
4. **Growth This Week** (+23%) - Bar chart, weekly change

### Activity Visualization Section

#### Toggle Controls

Glassmorphic button group with two visualization modes:

- **Wave View**: Dynamic layered activity visualization
- **Grid View**: GitHub-style contribution heatmap

#### Wave Visualization

- **Data Range**: 52 weeks of activity history
- **Three Activity Layers**:
  - High Activity (Green) - Sharp, dramatic peaks
  - Medium Activity (Magenta) - 70% intensity
  - Low Activity (Orange) - 40% intensity
- **Dynamic Peak Sharpness**: Higher activity = sharper, more dramatic spikes
- **Peak Markers**: Glowing indicators on highest activity points
- **Stats Display**: Average posts/week and peak posting time

#### Heatmap Grid (GitHub-style)

- **Grid Layout**: 52 weeks × 7 days = full year view
- **Activity Levels**: 4-level intensity scale (0-3)
- **Color Coding**: Green gradient from light (low) to bright (high)
- **Design**:
  - Circular cells (10px diameter) with glassmorphic effects
  - Month labels across top (Jan-Dec)
  - Day labels on left (Mon/Wed/Fri)
  - Hover effects with scale animation
- **Responsive**: Horizontal scroll on mobile, full width on desktop
- **Custom Scrollbar**: Futuristic glassmorphic design with tri-color gradient

### Post Type Breakdown (Donut Chart)

Visual breakdown of content types:

- **Thoughts** (Cyan): Text-based posts percentage
- **Media** (Blue): Photo/video posts percentage
- **Milestones** (Magenta): Achievement posts percentage

### Quick Settings

Grid of quick action buttons:

- Theme toggle
- Privacy settings
- Notification preferences
- Account settings

---

## Design System

### Color Palette

| Color      | Hex       | Usage                    |
| ---------- | --------- | ------------------------ |
| Cyan       | `#00d4ff` | Primary accent, thoughts |
| Emerald    | `#1ae784` | Success, high activity   |
| Magenta    | `#dc08bc` | Highlights, milestones   |
| Pink       | `#ff6b9d` | Notifications, warnings  |
| Purple     | `#a783ff` | Secondary accent         |
| Background | `#010102` | Base dark theme          |

### Glassmorphic Effects

- **Backdrop Blur**: 10px blur on containers
- **Border**: 1px semi-transparent white borders
- **Shadows**: Multi-layered colored glows
- **Transparency**: Layered rgba backgrounds for depth

### Typography

- **Display Name**: acme-gothic-extrawide (bold, uppercase feel)
- **Analytics Numbers**: sweet-square-pro (Typekit font)
- **Body Text**: System font stack with proper fallbacks

---

## Animation System

### Card Flip

```scss
.profile-flip-card {
  transform-style: preserve-3d;
  transition: transform 0.6s ease;

  &.flipped {
    transform: rotateY(180deg);
  }
}
```

### Hover Effects

- Scale transforms on interactive elements
- Color transitions with glow intensification
- Shimmer animation on header

### Wave Animation

- SVG path morphing for dynamic peaks
- Bezier curves for smooth transitions
- Activity-based sharpness calculation

---

## Data Generation

### Seeded Random

Consistent data generation using deterministic seeds:

```javascript
const seededRandom = (seed) => {
  let value = seed;
  return () => {
    value = (value * 9301 + 49297) % 233280;
    return value / 233280;
  };
};
```

### Activity Calculation

- **Heatmap**: 0-3 scale for intensity levels
- **Wave Heights**: Dynamic calculation based on activity level
- **Peak Detection**: Automatic identification of highest activity periods

---

## Props Reference

### ProfileCard

| Prop           | Type     | Description        |
| -------------- | -------- | ------------------ |
| `isFlipped`    | boolean  | Current flip state |
| `setIsFlipped` | function | Toggle flip state  |
| `posts`        | array    | User's post data   |
| `user`         | object   | User profile data  |

### ActivityVisualization

| Prop              | Type     | Description                  |
| ----------------- | -------- | ---------------------------- |
| `viewMode`        | string   | 'wave' or 'heatmap'          |
| `setViewMode`     | function | Toggle view mode             |
| `waveData`        | array    | High activity data points    |
| `mediumWaveData`  | array    | Medium activity (70%)        |
| `lowWaveData`     | array    | Low activity (40%)           |
| `heatmapData`     | array    | 52×7 grid of activity levels |
| `bestPostingTime` | string   | Peak posting time display    |

---

## User Experience Flow

1. **Initial View**: User sees public profile with clean, minimal information
2. **Click Analytics**: Card flips to reveal detailed activity dashboard
3. **Toggle Visualizations**: Switch between wave and heatmap views
4. **Explore Data**: Hover over peaks/cells to see activity details
5. **Quick Actions**: Use quick settings for common tasks
6. **Return**: Click back button to flip to profile view

---

## Performance Optimizations

- **useMemo**: Memoized data generation for wave and heatmap
- **SVG Rendering**: Efficient vector graphics for wave visualization
- **CSS Transforms**: Hardware-accelerated flip animation
- **Lazy Loading**: Analytics data only calculated when card is flipped

---

_Last Updated: December 2025_
