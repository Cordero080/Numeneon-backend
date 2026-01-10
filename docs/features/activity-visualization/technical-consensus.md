# Activity Visualization - Technical Consensus

## Overview

This document explains **how** the activity visualization actually works at a technical level. Use this to understand the code, modify it, or answer interview questions.

---

## 🌊 Wave Chart Implementation

### The Core Algorithm: `createWavePath()`

**Location:** `ProfileCard.jsx`

The wave chart uses **SVG paths with cubic Bézier curves** to create smooth, organic-looking waves from data points.

```javascript
const createWavePath = (data) => {
  const width = 600;
  const height = 100;
  const points = data.length;
  const segmentWidth = width / (points - 1);

  let path = `M 0,${height - data[0]}`; // Start point

  for (let i = 1; i < points; i++) {
    // Calculate current and previous positions
    const x = i * segmentWidth;
    const y = height - data[i]; // INVERTED: high values = high on screen
    const prevX = (i - 1) * segmentWidth;
    const prevY = height - data[i - 1];

    // Adaptive curve tension based on activity level
    const activityLevel = data[i] / 80;
    const sharpness = 0.4 - activityLevel * 0.39;

    // Control points for Bézier curve
    const cp1x = prevX + segmentWidth * sharpness;
    const cp1y = prevY;
    const cp2x = prevX + segmentWidth * (1 - sharpness);
    const cp2y = y;

    path += ` C ${cp1x},${cp1y} ${cp2x},${cp2y} ${x},${y}`;
  }

  // Close the path to make it fillable
  path += ` L ${width},${height} L 0,${height} Z`;
  return path;
};
```

### Key Concepts

#### 1. SVG Coordinate System Inversion

SVG has Y=0 at the top, increasing downward. We want high values to appear HIGH on screen, so we use `height - data[i]` to flip it.

#### 2. Cubic Bézier Curves (`C` command)

Each curve segment is defined by:

- **Start point** (implicit from previous command)
- **Control point 1** (cp1x, cp1y) - pulls curve as it leaves start
- **Control point 2** (cp2x, cp2y) - pulls curve as it approaches end
- **End point** (x, y)

#### 3. Adaptive Sharpness

The `sharpness` formula creates visual drama:

- **High activity** → Low sharpness (0.01) → Sharp, pointy peaks
- **Low activity** → High sharpness (0.4) → Smooth, flowing curves

This makes busy weeks visually "pop" as dramatic spikes.

#### 4. Closing the Path

The final commands (`L width,height L 0,height Z`) draw lines to the bottom corners and close the shape, creating a fillable area for the gradient.

---

## 🎨 SVG Gradients

### Wave Gradient (Vertical)

```jsx
<linearGradient id="waveGradient" x1="0%" y1="0%" x2="0%" y2="100%">
  <stop offset="0%" stopColor="rgba(26, 231, 132, 0.5)" />   <!-- Top: cyan/green -->
  <stop offset="40%" stopColor="rgba(26, 115, 231, 0.35)" /> <!-- 40%: blue-purple -->
  <stop offset="100%" stopColor="rgba(26, 115, 231, 0.1)" /> <!-- Bottom: faded -->
</linearGradient>
```

**Direction:** `x1=0, y1=0` to `x2=0, y2=100%` = **top to bottom** (vertical)

**Color stops:** Define where each color appears along the gradient line. Colors blend smoothly between stops.

---

## ✨ Glow Effect (SVG Filter)

```jsx
<filter id="glow">
  <feGaussianBlur stdDeviation="2" result="coloredBlur" />
  <feMerge>
    <feMergeNode in="coloredBlur" />
    <feMergeNode in="SourceGraphic" />
  </feMerge>
</filter>
```

**How it works:**

1. `feGaussianBlur` creates a blurred "halo" version of the element
2. `feMerge` layers the blur BEHIND the original sharp graphic
3. Result: Crisp line with soft glowing halo = neon effect

**stdDeviation:** Controls blur radius. 2 = subtle glow. 4-6 = dramatic neon.

---

## 📅 Heatmap Implementation

### Color Mapping

```javascript
const getActivityColor = (level) => {
  const colors = [
    "rgba(255, 255, 255, 0.05)", // Level 0: almost invisible
    "rgba(30, 149, 234, 0.25)", // Level 1: light blue
    "rgba(30, 173, 234, 0.5)", // Level 2: medium cyan
    "rgba(30, 227, 234, 1)", // Level 3: bright cyan
  ];
  return colors[level];
};
```

**Why array lookup?**

- Cleaner than if/else chains
- O(1) performance
- Easy to add/modify levels

### Grid Structure

- **Rows:** 7 (days of week)
- **Columns:** 52 (weeks of year)
- **Cell size:** Small rounded rectangles (3px × 3px with 1px gap)

---

## 🎲 Seeded Random Generator

### The Algorithm (Linear Congruential Generator)

```javascript
const seededRandom = (seed) => {
  let value = seed;
  return () => {
    value = (value * 9301 + 49297) % 233280;
    return value / 233280;
  };
};
```

**Why seeded random instead of Math.random()?**

- Same seed → Same sequence → Consistent visualization
- No "jumpy" UI on re-renders
- Reproducible for debugging
- Each user ID produces unique but stable pattern

**The magic numbers (9301, 49297, 233280):**
These are coefficients for LCG (Linear Congruential Generator). Mathematically chosen to produce:

- Long non-repeating sequences
- Good statistical distribution
- No visible patterns

---

## 📊 Data Flow

```
User Profile Loaded
        ↓
seededRandom(userId) creates generator
        ↓
Generate 52 weeks of mock activity data
        ↓
createWavePath() converts to SVG path
        ↓
Render <path d={...} fill="url(#gradient)" filter="url(#glow)" />
        ↓
User sees smooth animated wave
```

---

## Interview-Ready Explanations

### "How does the wave chart work?"

> "It uses SVG paths with cubic Bézier curves. Each data point becomes a curve segment where control points determine smoothness. I made high-activity weeks sharper and low-activity weeks smoother to add visual drama. The whole path is closed at the bottom to create a fillable area for gradients."

### "Why seeded random?"

> "I needed consistent visualizations across page reloads. Math.random() would make the heatmap change every render, which is jarring. Seeded random from the user ID gives the same 'random' pattern every time for that user."

### "How did you create the glow effect?"

> "SVG filter with Gaussian blur. First blur the element, then merge the blurred version behind the original using feMerge. The blur becomes a soft halo, the original stays sharp on top."
