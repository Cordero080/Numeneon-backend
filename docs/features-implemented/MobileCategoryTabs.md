# Mobile Category Tabs

## Overview

On mobile (≤768px), the profile timeline's three-column layout becomes a tab-based navigation.

## Tab Colors

| Tab | Icon | Active Color |
|-----|------|--------------|
| Thoughts | 💬 Chat bubble | Blue `rgba(77, 171, 247, 1)` |
| Media | 🖼️ Image | Magenta `rgba(233, 78, 200, 1)` |
| Milestones | ✓ Checkmark | Gold `rgba(255, 215, 0, 1)` |

## Implementation

```jsx
const [mobileCategory, setMobileCategory] = useState("thoughts");

<div className="mobile-category-tabs">
  <button 
    className={`mobile-category-tab ${mobileCategory === 'thoughts' ? 'active' : ''}`}
    onClick={() => setMobileCategory('thoughts')}
  >
    <svg>...</svg>
    <span>Thoughts</span>
  </button>
  {/* Similar for media and milestones */}
</div>
```

## Visibility Control

```scss
.river-streams.mobile-show-thoughts .left-stream { display: flex; }
.river-streams.mobile-show-media .center-stream { display: flex; }
.river-streams.mobile-show-milestones .right-stream { display: flex; }
```

## Location

**Component:** `TimelineRiver/TimelineRiver.jsx`  
**Styles:** `TimelineRiver/TimelineRiver.scss`
