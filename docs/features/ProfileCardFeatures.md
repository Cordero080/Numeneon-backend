# Profile Card Features

## Overview

The Numeneon profile card uses a flip-card architecture to separate public profile information (front) from private analytics (back). This creates a clean user experience while providing deep insights when needed.

---

## Front Card - Public Profile View

### Header Section

- **Banner Background**: Gradient overlay with glassmorphic fade effect
- **Avatar**: 150px circular avatar with futuristic glow ring
  - Tri-color gradient glow (green/blue/magenta)
  - Glassmorphic backdrop blur effect
  - Positioned to overlap banner

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

### Activity Overview Section

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

### Analytics Metrics

#### Current Stats

- **This Week Growth**: Percentage change in followers (+23%)
- **Post Count**: Total posts with dynamic calculation

#### Legend

Color-coded activity levels with glassmorphic design:

- None (barely visible)
- Low (25% green opacity)
- Medium (50% green opacity)
- High (100% green - full glow)

---

## Design System

### Color Palette

- **Primary**: Green (#1EEA4C) - High activity, success states
- **Secondary**: Blue (#1A73E7) - Medium activity, interactive elements
- **Accent**: Magenta (#EA1EA2) - Low activity, highlights
- **Background**: Dark cosmic theme with subtle transparency

### Glassmorphic Effects

- **Backdrop Blur**: 10px blur on containers
- **Border**: 1px semi-transparent white borders
- **Shadows**: Multi-layered colored glows
- **Transparency**: Layered rgba backgrounds for depth

### Typography

- **Display Name**: acme-gothic-extrawide (bold, uppercase feel)
- **Analytics Numbers**: sweet-square-pro (Typekit font)
- **Body Text**: System font stack with proper fallbacks

### Animations

- **Card Flip**: 3D transform with 0.6s ease transition
- **Hover Effects**: Scale transforms, color transitions, glow intensification
- **Shimmer**: Subtle background animation on header
- **Scrollbar**: Glow effect on hover

---

## User Experience Flow

1. **Initial View**: User sees public profile with clean, minimal information
2. **Click Analytics**: Card flips to reveal detailed activity dashboard
3. **Toggle Visualizations**: Switch between wave and heatmap views
4. **Explore Data**: Hover over peaks/cells to see activity details
5. **Return**: Click back button to flip to profile view

---

## Technical Implementation

### Data Generation

- **Seeded Random**: Consistent data generation using seed (12345)
- **Activity Calculation**: 0-3 scale for heatmap intensity
- **Wave Heights**: Dynamic calculation with sharpness based on activity level

### Components

- **ProfileCard.jsx**: Main flip card component with state management
- **ProfileCard.css**: Complete styling with 1100+ lines
- **View Mode State**: Toggle between 'wave' and 'heatmap'

### Performance

- **useMemo**: Memoized data generation for wave and heatmap
- **SVG Rendering**: Efficient vector graphics for wave visualization
- **CSS Transforms**: Hardware-accelerated flip animation
