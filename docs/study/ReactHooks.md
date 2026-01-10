# React Hooks - Interview Study Guide

## 🎯 The 8 Hooks You MUST Know

| Hook              | Purpose                                          | When to Use                              |
| ----------------- | ------------------------------------------------ | ---------------------------------------- |
| `useState`        | Local component state                            | Any state that only this component needs |
| `useEffect`       | Side effects (API calls, subscriptions)          | Data fetching, DOM manipulation, timers  |
| `useContext`      | Access context values                            | Global state (auth, theme, data)         |
| `useRef`          | Mutable reference that doesn't trigger re-render | DOM access, storing previous values      |
| `useMemo`         | Cache expensive calculations                     | Heavy computations, derived data         |
| `useCallback`     | Cache function references                        | Passing callbacks to child components    |
| `useReducer`      | Complex state logic                              | Multiple related state values            |
| `useLayoutEffect` | Sync effect before paint                         | DOM measurements, animations             |

---

## 1. useState - Local State

### What It Does

Stores a value that, when changed, re-renders the component.

### Syntax

```javascript
const [state, setState] = useState(initialValue);
```

### When to Use

- Form inputs
- Toggle states (open/closed, show/hide)
- Counters
- Any component-specific data

### Example from Numeneon

```javascript
// In ComposerModal.jsx
const [content, setContent] = useState("");
const [postType, setPostType] = useState("thoughts");
const [isSubmitting, setIsSubmitting] = useState(false);
```

### Interview Tip

> "useState is for any value that, when changed, should trigger a re-render. Each call creates one piece of state."

---

## 2. useEffect - Side Effects

### What It Does

Runs code AFTER render. Used for anything that interacts with "outside" (APIs, DOM, timers).

### Syntax

```javascript
useEffect(() => {
  // Effect code runs after render
  return () => {
    // Cleanup (optional) - runs before next effect or unmount
  };
}, [dependencies]); // When these change, effect re-runs
```

### Dependency Array Rules

| Array    | Behavior                               |
| -------- | -------------------------------------- |
| `[]`     | Run once on mount only                 |
| `[a, b]` | Run when `a` or `b` changes            |
| No array | Run after EVERY render (rarely wanted) |

### When to Use

- API calls (fetch data on mount)
- Event listeners (add on mount, remove on cleanup)
- Timers (setInterval/setTimeout)
- DOM manipulation

### Example from Numeneon

```javascript
// In Profile.jsx - fetch user data when username changes
useEffect(() => {
  const fetchUserData = async () => {
    const response = await apiClient.get(`/users/${username}/`);
    setUserData(response.data);
  };
  fetchUserData();
}, [username]); // Re-fetch when username param changes
```

### Interview Tip

> "useEffect is for synchronizing your component with external systems. The dependency array controls WHEN it re-runs. Always include values you READ inside the effect."

---

## 3. useContext - Access Global State

### What It Does

Reads values from a Context without prop drilling.

### Syntax

```javascript
const value = useContext(MyContext);
```

### When to Use

- Accessing app-wide state (user, theme, posts)
- Avoiding passing props through many levels
- Sharing data between unrelated components

### Example from Numeneon

```javascript
// In any component that needs auth
import { useAuth } from "@contexts/AuthContext";

function ProfileCard() {
  const { currentUser, isLoggedIn, logout } = useAuth();

  if (!isLoggedIn) return <LoginPrompt />;
  return <div>Welcome, {currentUser.username}</div>;
}
```

### Interview Tip

> "useContext lets any component access context values directly. Combined with a Provider pattern, it's great for global state like auth or theme without Redux."

---

## 4. useRef - Mutable References

### What It Does

Creates a mutable container that persists across renders WITHOUT triggering re-renders.

### Syntax

```javascript
const ref = useRef(initialValue);
// Access: ref.current
```

### Two Main Uses

#### A) DOM Access

```javascript
const inputRef = useRef(null);

useEffect(() => {
  inputRef.current.focus(); // Focus the input on mount
}, []);

return <input ref={inputRef} />;
```

#### B) Storing Previous Values

```javascript
const prevCount = useRef(count);

useEffect(() => {
  prevCount.current = count; // Update ref, no re-render
}, [count]);
```

### When to Use

- Focus management
- Scroll position
- Storing values that shouldn't trigger re-renders
- Holding interval/timeout IDs

### Example from Numeneon

```javascript
// In ComposerModal.jsx - auto-focus textarea
const textareaRef = useRef(null);

useEffect(() => {
  if (isOpen) {
    textareaRef.current?.focus();
  }
}, [isOpen]);
```

### Interview Tip

> "useRef is for values you need to persist but that shouldn't cause re-renders. Common for DOM refs and storing 'previous' values."

---

## 5. useMemo - Cache Calculations

### What It Does

Caches a computed value, only recalculating when dependencies change.

### Syntax

```javascript
const cachedValue = useMemo(() => expensiveCalculation(a, b), [a, b]);
```

### When to Use

- Expensive calculations (filtering, sorting large arrays)
- Creating derived data
- Preventing unnecessary recalculations

### Example

```javascript
// In TimelineRiverFeed.jsx - group posts by date
const groupedPosts = useMemo(() => {
  return groupPostsByDate(posts); // Only recalculate when posts change
}, [posts]);
```

### When NOT to Use

- Simple calculations (React is fast, don't over-optimize)
- Values that change every render anyway

### Interview Tip

> "useMemo caches a VALUE. Use it when you have expensive calculations that don't need to re-run on every render. But don't overuse it—premature optimization is bad."

---

## 6. useCallback - Cache Functions

### What It Does

Caches a function reference, only creating a new function when dependencies change.

### Syntax

```javascript
const cachedFn = useCallback(
  (arg) => {
    doSomething(arg, dependency);
  },
  [dependency]
);
```

### When to Use

- Passing callbacks to optimized child components (React.memo)
- Preventing unnecessary child re-renders
- When function identity matters

### Example

```javascript
// Parent component
const handleLike = useCallback(
  (postId) => {
    likePost(postId);
  },
  [likePost]
);

return <PostCard onLike={handleLike} />; // PostCard won't re-render unnecessarily
```

### useMemo vs useCallback

```javascript
// These are equivalent:
useCallback(fn, deps);
useMemo(() => fn, deps);

// useMemo caches a VALUE
// useCallback caches a FUNCTION
```

### Interview Tip

> "useCallback caches a FUNCTION reference. It's mainly useful when passing callbacks to memoized children, preventing unnecessary re-renders."

---

## 7. useReducer - Complex State

### What It Does

Alternative to useState for complex state logic with multiple sub-values.

### Syntax

```javascript
const [state, dispatch] = useReducer(reducer, initialState);

function reducer(state, action) {
  switch (action.type) {
    case "increment":
      return { count: state.count + 1 };
    case "decrement":
      return { count: state.count - 1 };
    default:
      return state;
  }
}
```

### When to Use

- State with multiple related values
- Next state depends on previous state
- Complex update logic
- Want Redux-like patterns without Redux

### Example

```javascript
const initialState = { posts: [], loading: false, error: null };

function postsReducer(state, action) {
  switch (action.type) {
    case "FETCH_START":
      return { ...state, loading: true };
    case "FETCH_SUCCESS":
      return { posts: action.payload, loading: false, error: null };
    case "FETCH_ERROR":
      return { ...state, loading: false, error: action.payload };
    default:
      return state;
  }
}
```

### useState vs useReducer

| useState            | useReducer                |
| ------------------- | ------------------------- |
| Simple values       | Complex objects           |
| Independent updates | Related state transitions |
| Inline logic        | Separated reducer logic   |

### Interview Tip

> "useReducer is useState on steroids. I use it when state has multiple related values that update together, like loading + data + error states."

---

## 8. useLayoutEffect - Sync Before Paint

### What It Does

Same as useEffect, but fires BEFORE the browser paints. Blocks visual updates.

### Syntax

```javascript
useLayoutEffect(() => {
  // Runs synchronously after DOM mutations, before paint
}, [deps]);
```

### When to Use

- DOM measurements (need element size before render)
- Preventing visual flicker
- Animations that need immediate DOM access

### When NOT to Use

- Most cases (useEffect is usually fine)
- If it blocks rendering, it slows the app

### Example

```javascript
// Measure element before browser paints
useLayoutEffect(() => {
  const { width, height } = elementRef.current.getBoundingClientRect();
  setDimensions({ width, height });
}, []);
```

### Interview Tip

> "useLayoutEffect is useEffect that runs synchronously before paint. I only use it when I need DOM measurements to prevent flicker. 99% of the time, useEffect is correct."

---

## 🎤 Interview Questions & Answers

### Q: "What's the difference between useMemo and useCallback?"

> "useMemo caches a VALUE—the result of a calculation. useCallback caches a FUNCTION—the function itself. useCallback is essentially useMemo for functions."

### Q: "When would you use useReducer over useState?"

> "When state is complex—multiple related values that update together. Like loading + data + error for an API call. Or when next state depends heavily on previous state. It separates update logic into a reducer function."

### Q: "Why do you need to specify dependencies in useEffect?"

> "The dependency array tells React WHEN to re-run the effect. If I fetch data based on `userId`, I need `[userId]` so it re-fetches when the user changes. Missing dependencies cause bugs."

### Q: "What happens if you forget the dependency array?"

> "The effect runs after EVERY render—probably not what you want. For API calls, that means infinite fetch loops. Always include the array, even if empty."

### Q: "How does useRef differ from useState?"

> "useState changes trigger re-renders. useRef changes do NOT. Use useRef when you need to store something without affecting the UI—like DOM references, previous values, or interval IDs."

### Q: "What's the Context + useContext pattern?"

> "Create a Context with createContext(), wrap your app in a Provider that holds state, then any child can read that state with useContext(). It's React's built-in solution for global state without prop drilling."

---

## 📊 Quick Reference

```
Need state that re-renders?     → useState
Need to fetch data?             → useEffect with []
Need global state?              → useContext
Need DOM access?                → useRef
Need to cache calculations?     → useMemo
Need to cache callbacks?        → useCallback
Have complex state logic?       → useReducer
Need sync DOM measurements?     → useLayoutEffect
```
