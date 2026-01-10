# Visual Identity System

## Overview

Numeneon uses a comprehensive design token system and unified utilities to create a cohesive, professional visual identity. Every UI element extends from a core set of variables and reusable classes, ensuring consistency across the entire application.

---

## Design Tokens

### Location

`/src/styles/design-const.css`

### Color Tokens

```css
:root {
  /* Primary Colors */
  --primary: #7cc9ff; /* Cyan - Primary brand color */
  --secondary: #a783ff; /* Purple - Secondary accent */
  --accent: #1ae784; /* Green - Success/accent color */

  /* Surface & Backgrounds */
  --surface: rgba(255, 255, 255, 0.02);
  --surface-hover: rgba(255, 255, 255, 0.06);
  --surface-active: rgba(255, 255, 255, 0.08);

  /* Borders */
  --border: rgba(255, 255, 255, 0.08);
  --border-hover: rgba(255, 255, 255, 0.15);
  --border-active: rgba(255, 255, 255, 0.25);

  /* Glows & Shadows */
  --glow: 0 0 20px rgba(124, 201, 255, 0.25);
  --glow-strong: 0 0 30px rgba(124, 201, 255, 0.4);
}
```

### Typography Tokens

```css
:root {
  /* Font Families */
  --font-main: "degular", sans-serif; /* Body text */
  --font-display: "acme-gothic-extrawide", sans-serif; /* Headings */
  --font-mono: "sweet-square-pro", monospace; /* Code/metrics */

  /* Font Sizes */
  --font-size-xs: 0.75rem; /* 12px */
  --font-size-sm: 0.875rem; /* 14px */
  --font-size-body: 0.95rem; /* 15.2px */
  --font-size-md: 1rem; /* 16px */
  --font-size-lg: 1.125rem; /* 18px */
  --font-size-title: 1.25rem; /* 20px */
  --font-size-xl: 1.5rem; /* 24px */
}
```

### Spacing System (8px base)

```css
:root {
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 40px;
}
```

### Border Radius

```css
:root {
  --radius: 18px; /* Default */
  --radius-sm: 12px; /* Small */
  --radius-lg: 24px; /* Large */
  --radius-full: 999px; /* Pills/circles */
}
```

### Transitions

```css
:root {
  --transition: 0.18s ease; /* Fast, responsive */
  --transition-slow: 0.3s ease; /* Deliberate */
}
```

---

## Unified Button System

### Location

`/src/styles/utilities.css`

### Base Button

All buttons extend from `.btn`:

```css
.btn {
  padding: 10px 22px;
  border-radius: var(--radius-full);
  border: 1px solid var(--border);
  background: var(--surface);
  color: white;
  font-weight: 500;
  letter-spacing: 0.3px;
  font-size: var(--font-size-body);
  transition: var(--transition);
}

.btn:hover {
  background: var(--surface-hover);
  box-shadow: var(--glow);
  transform: translateY(-1px);
}

.btn:active {
  transform: scale(0.97);
}
```

### Button Variants

**Color Variants:**

```html
<button class="btn btn-primary">Primary</button>
<button class="btn btn-secondary">Secondary</button>
<button class="btn btn-accent">Success</button>
```

**Style Variants:**

```html
<button class="btn btn-ghost">Ghost</button>
<button class="btn btn-filled">Filled</button>
```

**Size Variants:**

```html
<button class="btn btn-sm">Small</button>
<button class="btn">Default</button>
<button class="btn btn-lg">Large</button>
<button class="btn btn-icon">Icon Only</button>
```

### Usage Examples

```jsx
// Primary action button
<button className="btn btn-primary btn-lg">
  Get Started
</button>

// Ghost button for secondary actions
<button className="btn btn-ghost">
  Cancel
</button>

// Filled button for CTAs
<button className="btn btn-filled">
  Post
</button>

// Icon-only button
<button className="btn btn-icon">
  <svg>...</svg>
</button>
```

---

## Card System

### Base Cards

```css
.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  backdrop-filter: blur(20px);
  transition: var(--transition);
}
```

### Interactive Cards

```html
<!-- Hover effect only -->
<div class="card card-hover">Content</div>

<!-- Full interactive (hover + click) -->
<div class="card card-interactive">Content</div>
```

### Card Variants

```html
<!-- Glassmorphic -->
<div class="card card-glass">Content</div>

<!-- Dark variant -->
<div class="card card-dark">Content</div>
```

---

## Micro-Animations

### Fade In on Load

```html
<div class="fade-in">Content fades in with subtle upward movement</div>
```

```css
@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(3px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.fade-in {
  animation: fadeIn 0.4s ease;
}
```

### Hover Lift

```html
<div class="card hover-lift">Lifts up on hover</div>
```

### Active Scale

```html
<button class="btn active-scale">Scales down on click</button>
```

### All Animation Classes

| Class           | Effect                    | Duration |
| --------------- | ------------------------- | -------- |
| `.fade-in`      | Fade up on load           | 0.4s     |
| `.slide-in-up`  | Slide from bottom         | 0.4s     |
| `.scale-in`     | Scale up on load          | 0.3s     |
| `.hover-lift`   | translateY(-2px) on hover | 0.18s    |
| `.hover-glow`   | Glow shadow on hover      | 0.18s    |
| `.active-scale` | scale(0.97) on click      | 0.18s    |

---

## Layout Utilities

### Containers

```html
<!-- Standard container (1150px max) -->
<div class="container">Content</div>

<!-- Narrow container (900px max) -->
<div class="container-narrow">Content</div>

<!-- Wide container (1400px max) -->
<div class="container-wide">Content</div>
```

### Glassmorphism

```html
<!-- Standard glass -->
<div class="glass">Glassmorphic background</div>

<!-- Strong glass -->
<div class="glass-strong">More opaque glass</div>

<!-- Subtle glass -->
<div class="glass-subtle">Very subtle glass</div>
```

---

## Text Utilities

### Opacity Levels

```html
<p class="text-muted">60% opacity</p>
<p class="text-secondary">70% opacity</p>
<p class="text-primary">90% opacity</p>
```

### Special Effects

```html
<!-- Gradient text -->
<h1 class="text-gradient">Gradient from primary to secondary</h1>

<!-- Glowing text -->
<h1 class="text-glow">Text with cyan glow</h1>
```

---

## Spacing Utilities

### Gap

```html
<div class="gap-sm">gap: 8px</div>
<div class="gap-md">gap: 16px</div>
<div class="gap-lg">gap: 24px</div>
<div class="gap-xl">gap: 32px</div>
```

### Padding

```html
<div class="p-sm">padding: 8px</div>
<div class="p-md">padding: 16px</div>
<div class="p-lg">padding: 24px</div>
<div class="p-xl">padding: 32px</div>
```

### Margin

```html
<div class="m-sm">margin: 8px</div>
<div class="m-md">margin: 16px</div>
<div class="m-lg">margin: 24px</div>
<div class="m-xl">margin: 32px</div>
```

---

## Feed Layout Improvements

### Timeline River Feed

**Container:**

- Max-width: `1150px`
- Centered with `margin: 0 auto`
- Vertical gap: `var(--space-lg)` (24px)

**Section Gaps:**

- Between date sections: `var(--space-sm)` (8px)

**Row Gaps:**

- Between posts: `12px` (tighter clustering)

### Card Width Differentiation

```css
/* Thought posts - narrower for text-only */
.timeline-river-row--3-col .river-column:nth-child(1) {
  max-width: 40%;
}

/* Media and achievements - wider for visual content */
.timeline-river-row--3-col .river-column:nth-child(2),
.timeline-river-row--3-col .river-column:nth-child(3) {
  max-width: 55%;
}
```

### Reduced Negative Space in Thought Posts

**Tighter Padding:**

```css
.river-column:nth-child(1) .river-post-card {
  padding: 16px 18px; /* Instead of 20px */
}
```

**Larger Font:**

```css
.river-column:nth-child(1) .river-post-content {
  font-size: 1.05rem; /* Instead of 20px */
  line-height: 1.45; /* Instead of 1.6 */
}
```

---

## Best Practices

### 1. Always Use Tokens

❌ **Don't:**

```css
.my-component {
  padding: 16px;
  border-radius: 12px;
  color: rgba(255, 255, 255, 0.6);
  transition: 0.2s ease;
}
```

✅ **Do:**

```css
.my-component {
  padding: var(--space-md);
  border-radius: var(--radius-sm);
  color: var(--text-secondary);
  transition: var(--transition);
}
```

### 2. Extend Base Classes

❌ **Don't:**

```html
<button style="padding: 10px 20px; border-radius: 999px;">Click me</button>
```

✅ **Do:**

```html
<button class="btn btn-primary">Click me</button>
```

### 3. Combine Utility Classes

```html
<!-- Card with fade-in animation and hover lift -->
<div class="card card-glass fade-in hover-lift">Content</div>

<!-- Button with active scale -->
<button class="btn btn-filled active-scale">Submit</button>
```

### 4. Use Semantic Naming

```html
<!-- Good: Describes purpose -->
<button class="btn btn-primary">Submit Post</button>

<!-- Bad: Describes appearance -->
<button class="blue-rounded-button">Submit Post</button>
```

---

## Component Examples

### Post Card with Full System

```jsx
function PostCard({ post }) {
  return (
    <div className="card card-hover fade-in">
      <div className="p-lg">
        <h3 className="text-primary">{post.title}</h3>
        <p className="text-secondary">{post.content}</p>

        <div
          className="gap-sm"
          style={{ display: "flex", marginTop: "var(--space-md)" }}
        >
          <button className="btn btn-primary btn-sm active-scale">Like</button>
          <button className="btn btn-ghost btn-sm active-scale">Comment</button>
          <button className="btn btn-ghost btn-sm active-scale">Share</button>
        </div>
      </div>
    </div>
  );
}
```

### Modal with Glassmorphism

```jsx
function Modal({ children, onClose }) {
  return (
    <div className="modal-overlay fade-in">
      <div
        className="card card-glass scale-in"
        style={{
          maxWidth: "600px",
          padding: "var(--space-xl)",
        }}
      >
        <button
          onClick={onClose}
          className="btn btn-icon btn-ghost"
          style={{
            position: "absolute",
            top: "var(--space-md)",
            right: "var(--space-md)",
          }}
        >
          ×
        </button>
        {children}
      </div>
    </div>
  );
}
```

---

## Performance Considerations

### CSS Variables Performance

- ✅ Design tokens compile to native CSS custom properties
- ✅ Fast updates via single variable changes
- ✅ No JavaScript overhead
- ✅ Browser-optimized

### Animation Performance

All animations use GPU-accelerated properties:

- ✅ `transform` (translateY, scale)
- ✅ `opacity`
- ❌ Avoid animating `width`, `height`, `margin`, `padding`

### Utility Class Strategy

- ✅ Utilities are shared across all components (smaller bundle)
- ✅ No duplicate styles
- ✅ Cached by browser efficiently

---

## Future Enhancements

### Planned Additions

1. **Dark/Light Mode Toggle**

   - Theme switching via CSS variables
   - Smooth transitions between modes

2. **Motion Preferences**

   - Respect `prefers-reduced-motion`
   - Disable animations for accessibility

3. **Color Scheme Generator**

   - Generate complementary palettes
   - Accessibility contrast checking

4. **Component Library**
   - Storybook integration
   - Interactive documentation
   - Copy-paste examples

---

## Related Documentation

- [Design Constants Reference](./design-const.css)
- [Utilities Reference](./utilities.css)
- [Component Architecture](../study.md)
- [Profile Card Features](./ProfileCardFeatures.md)
