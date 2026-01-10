# VisibilityIcon Smart Component Refactor

> Consolidating hardcoded SVG privacy icons into a reusable smart component

**Date:** January 7, 2026  
**File:** `frontend/src/assets/icons/user.jsx`  
**Component:** `VisibilityIcon`

---

## The Problem

The privacy/visibility icon in [PostCard.jsx](frontend/src/components/pages/Home/components/TimelineRiverRow/components/PostCard/PostCard.jsx#L113-L124) was hardcoded as an inline SVG with conditional rendering logic.

### Before Refactor

```jsx
{
  /* Privacy icon */
}
<svg
  className="privacy-icon"
  width="20"
  height="20"
  viewBox="0 0 24 24"
  fill="none"
>
  {post.visibility === "private" ? (
    <path
      d="M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zm-6 9c-1.1 0-2-.9-2-2s.9-2 2-2 2 .9 2 2-.9 2-2 2zm3.1-9H8.9V6c0-1.71 1.39-3.1 3.1-3.1 1.71 0 3.1 1.39 3.1 3.1v2z"
      fill="currentColor"
    />
  ) : post.visibility === "public" ? (
    <path
      d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"
      fill="currentColor"
    />
  ) : (
    <path
      d="M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z"
      fill="currentColor"
    />
  )}
</svg>;
```

**Problems:**

- 15 lines of hardcoded SVG
- Breaks icon system consistency
- Logic scattered in UI component
- Not reusable elsewhere
- Harder to maintain

---

## The Solution

### New Smart Component

Created `VisibilityIcon` in [user.jsx](frontend/src/assets/icons/user.jsx) that automatically renders the correct icon based on the `visibility` prop:

```jsx
/** Smart Visibility Icon - switches between Lock/Globe/Friends based on visibility prop */
export const VisibilityIcon = ({
  visibility = "public",
  size = 20,
  className = "",
  ...props
}) => {
  if (visibility === "private") {
    return <LockIcon size={size} className={className} {...props} />;
  }

  if (visibility === "public") {
    return <GlobeIcon size={size} className={className} {...props} />;
  }

  // Default to friends/connections
  return <FriendsIcon size={size} className={className} {...props} />;
};
```

### Updated PostCard Usage

```jsx
import {
  UserIcon,
  HeartDynamicIcon,
  MessageBubbleIcon,
  // ... other icons
  VisibilityIcon, // ← NEW
} from "@assets/icons";

// In JSX:
{
  /* Privacy icon */
}
<VisibilityIcon
  visibility={post.visibility}
  size={20}
  className="privacy-icon"
/>;
```

**Result:** 15 lines of inline SVG → 1 clean line

---

## Benefits

### 1. Consistency

- Follows the same icon pattern as all other icons
- Standard API: `size`, `className`, `...props`

### 2. Reusability

- Can be used anywhere visibility needs to be shown
- Already imported with other icons

### 3. Maintainability

- Logic lives in one place
- Update once, works everywhere
- Easier to test

### 4. Cleaner Code

- PostCard.jsx is now more readable
- Separation of concerns (UI vs. icon logic)

### 5. Extensibility

- Easy to add new visibility states
- Could add `hover` effects in one place
- Could add `title` tooltips centrally

---

## Integration Points

### Icons Already Existed

The individual icons were already in the icon system:

- `LockIcon` - Private visibility
- `GlobeIcon` - Public visibility
- `FriendsIcon` - Friends-only visibility

### New Smart Component

`VisibilityIcon` is a **smart wrapper** that:

1. Takes a `visibility` prop ('private' | 'public' | 'friends')
2. Renders the appropriate icon component
3. Passes through all other props (`size`, `className`, etc.)

---

## Files Updated

### Created/Modified:

1. [frontend/src/assets/icons/user.jsx](frontend/src/assets/icons/user.jsx) - Added `VisibilityIcon`
2. [frontend/src/assets/icons/index.js](frontend/src/assets/icons/index.js) - Exported `VisibilityIcon`
3. [frontend/src/components/pages/Home/components/TimelineRiverRow/components/PostCard/PostCard.jsx](frontend/src/components/pages/Home/components/TimelineRiverRow/components/PostCard/PostCard.jsx) - Replaced inline SVG

### Documentation to Update:

- `docs/copilot-task/02-PSEUDOCODE-EXAMPLES.md` - Add VisibilityIcon to examples
- `docs/copilot-task/05-TEAM-PLAN-FILES.md` - Update icon list
- `docs/refactoring/SVG-Icons-Refactor.md` - Add VisibilityIcon to smart components
- Team study plans - Update icon patterns

---

## Pattern for Future Smart Icons

This establishes a pattern for other conditional icons:

```jsx
// Template for smart icon components
export const SmartIcon = ({ state, size = 20, className = "", ...props }) => {
  if (state === "option1") {
    return <Icon1 size={size} className={className} {...props} />;
  }
  if (state === "option2") {
    return <Icon2 size={size} className={className} {...props} />;
  }
  // Default
  return <Icon3 size={size} className={className} {...props} />;
};
```

### Other Candidates:

- `OnlineStatusIcon` - Online/Away/Busy/Offline states
- `NotificationIcon` - Badge counts, unread states
- `BookmarkIcon` - Filled/unfilled states (if not already dynamic)

---

## Team Impact

### For Team Rebuild:

✅ **Good news:** This simplifies the pseudocode!

Instead of teaching the team to write:

```jsx
// Complex conditional SVG rendering...
```

They now learn:

```jsx
<VisibilityIcon visibility={post.visibility} size={20} />
```

### Documentation Updates Needed:

1. Update pseudocode examples to use `VisibilityIcon`
2. Add to icon list in all team files
3. Update study materials showing modern pattern
4. Add note about "smart icons" concept

---

## Lessons Learned

1. **Look for patterns** - When you see conditional inline SVGs, consider a smart component
2. **Smart components are powerful** - Logic centralization improves maintainability
3. **Consistency matters** - Following established patterns makes code more predictable
4. **Separation of concerns** - UI components shouldn't contain icon rendering logic

---

## Comparison

### Before: Manual Conditional Rendering

```jsx
{
  post.visibility === "private" ? (
    <svg>...</svg> // 5 lines
  ) : post.visibility === "public" ? (
    <svg>...</svg> // 5 lines
  ) : (
    <svg>...</svg> // 5 lines
  );
}
```

### After: Smart Component

```jsx
<VisibilityIcon visibility={post.visibility} size={20} />
```

**15 lines → 1 line** ✨

---

## Future Considerations

### Potential Enhancements:

1. **Tooltips:** Add visibility label on hover
2. **Animation:** Subtle transition when toggling visibility
3. **Accessibility:** Enhanced ARIA labels per state
4. **Size variants:** Predefined size props (sm, md, lg)
5. **Color variants:** Theme-aware coloring

### Usage Tracking:

- Currently used in: PostCard.jsx
- Could be used in: Profile settings, Post composer, Privacy controls

---

## Related Refactors

This continues the work from:

- **SVG Icons Refactor (Dec 2024)** - Extracted 70+ icons into modular system
- **Icon System Documentation** - Established standardized icon API

Next potential refactors:

- ProfileCard avatar rendering (simplify)
- Notification badge icon system
- Theme icon toggles

---

## Git History

```
[Timestamp] - Extract VisibilityIcon smart component
  - Created VisibilityIcon in user.jsx
  - Exported from icons/index.js
  - Updated PostCard.jsx to use new component
  - Reduced PostCard.jsx by 14 lines
```
