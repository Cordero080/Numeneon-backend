# Tito's Tasks (Size: S)

## Your Mission

You're building the infrastructure layer - the foundational utilities that everyone else depends on. You handle API configuration, theme switching, and the app entry point. Small number of files, but critical to the entire system working.

## Files You Own

**Important:** Don't touch anyone else's files to avoid merge conflicts!

### Frontend Files (6 total)

- `frontend/src/main.jsx` - App entry point, wraps with all providers
- `frontend/src/services/apiClient.js` - Axios instance with JWT auth handling
- `frontend/src/contexts/ThemeContext.jsx` - Light/dark mode state management
- `frontend/src/components/ui/ThemeToggle/ThemeToggle.jsx` - Theme switch button
- `frontend/src/components/ui/ThemeToggle/ThemeToggle.scss` - Theme toggle styling
- `frontend/src/components/ui/ThemeToggle/index.js` - Component export

---

## Task Breakdown

### ✅ Task 1: Configure API Client

**Files:** `frontend/src/services/apiClient.js`

**What:** Create axios instance that automatically attaches JWT tokens to requests

**Why:** Every API call needs authentication - this centralizes token handling

**Acceptance Criteria:**

- [ ] Creates axios instance with baseURL (http://localhost:8000 for development)
- [ ] Request interceptor attaches JWT token from localStorage to Authorization header
- [ ] Response interceptor handles 401 errors (token expired) by clearing auth state
- [ ] All API calls throughout the app use this client

**Think about:**

- Where is the JWT token stored? (localStorage, set by AuthContext)
- What format should the Authorization header use? ("Bearer <token>")
- What happens if token is missing? (should still allow request for public endpoints)
- What if token expires mid-session? (401 error → logout user)

**Helpful Resources:** Axios interceptors docs

---

### ✅ Task 2: Build Theme Context

**Files:** `frontend/src/contexts/ThemeContext.jsx`

**What:** React context that manages light/dark mode for the entire app

**Why:** Users can switch between light and dark themes, needs to persist and be accessible everywhere

**Acceptance Criteria:**

- [ ] Stores current theme ('light' or 'dark') in state
- [ ] Provides `toggleTheme()` function
- [ ] Saves theme preference to localStorage
- [ ] Reads theme from localStorage on mount (persists across sessions)
- [ ] Applies `data-theme` attribute to document root
- [ ] Defaults to 'dark' if no preference saved

**Think about:**

- How do you apply theme to the whole app? (data-theme attribute on <html> or <body>)
- Should theme change be instant or animated?
- What if localStorage is disabled? (fallback to state only)

**Helpful Resources:** Look at other contexts for pattern (AuthContext, PostsContext)

---

### ✅ Task 3: Build Theme Toggle Component

**Files:** `ThemeToggle.jsx`, `ThemeToggle.scss`, `index.js`

**What:** Button that switches between light and dark mode

**Why:** User-facing control for theme preference

**Acceptance Criteria:**

- [ ] Displays sun icon for light mode, moon icon for dark mode
- [ ] Calls ThemeContext.toggleTheme() on click
- [ ] Icon animates smoothly on theme switch
- [ ] Styled using Pablo's design system
- [ ] Small, unobtrusive (fits in TopBar)

**Think about:**

- Should the button show the current theme or the one you'll switch to?
- How do you animate the icon transition smoothly?
- Should there be tooltip/label or just icon?

**Helpful Resources:** Pablo's icon system, design system for button styling

---

### ✅ Task 4: Configure App Entry Point

**Files:** `frontend/src/main.jsx`

**What:** Root file that renders the entire app with all context providers

**Why:** React needs a single entry point, and all contexts must wrap the app here

**Acceptance Criteria:**

- [ ] Wraps App.jsx with all context providers:
  - ThemeProvider (yours)
  - AuthProvider (Natalia)
  - PostsProvider (Colin)
  - FriendsProvider (Crystal)
  - MessageProvider (Pablo - already built)
- [ ] Providers nested in correct order (outer to inner)
- [ ] Renders to root DOM element
- [ ] Includes React StrictMode for development warnings

**Think about:**

- What order should providers be nested? (Theme outermost, then Auth, then data contexts)
- Why does order matter? (inner providers can consume outer contexts)

**Helpful Resources:** React context provider pattern, main.jsx is standard React entry point

---

## Integration Points

**You provide:**

- **apiClient.js** - Used by authService (Natalia), postsService (Colin), friendsService (Crystal)
- **ThemeContext** - Consumed by ThemeToggle component and Pablo's theme-dependent components
- **main.jsx** - Wraps everyone's contexts so they're accessible app-wide

**You consume:**

- AuthContext (Natalia) - apiClient reads token from AuthContext's localStorage
- All contexts from team members - you wrap them in main.jsx

**Work with:**

- **Everyone!** Your files are the foundation. They build on top of you.
- **Natalia:** Your apiClient uses her auth token
- **Colin & Crystal:** Their services use your apiClient
- **Pablo:** Your theme system controls his CSS variables

---

## API Client Configuration

`apiClient.js` should be configured like this:

```javascript
import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:8000", // Django backend
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor - attach token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - handle 401
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid - clear auth state
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      window.location.href = "/login"; // Force redirect
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

---

## Theme System

Pablo's CSS uses CSS variables that automatically change based on `data-theme` attribute:

```scss
// In Pablo's _variables.scss (already built - DON'T MODIFY)
[data-theme="dark"] {
  --bg-primary: #0a0a0a;
  --text-primary: #ffffff;
  --color-accent: #4fffff;
  // ... many more
}

[data-theme="light"] {
  --bg-primary: #ffffff;
  --text-primary: #000000;
  --color-accent: #1a73e7;
  // ... many more
}
```

Your job in ThemeContext:

1. Toggle between 'dark' and 'light'
2. Set `document.documentElement.setAttribute('data-theme', theme)`
3. Save to localStorage

CSS does the rest automatically!

---

## Context Provider Nesting Order

In `main.jsx`, nest providers like this:

```javascript
<React.StrictMode>
  <ThemeProvider>
    {" "}
    {/* Outermost - theme affects everything */}
    <AuthProvider>
      {" "}
      {/* Auth needed by data contexts */}
      <PostsProvider>
        {" "}
        {/* Data contexts in any order */}
        <FriendsProvider>
          <MessageProvider>
            <App />
          </MessageProvider>
        </FriendsProvider>
      </PostsProvider>
    </AuthProvider>
  </ThemeProvider>
</React.StrictMode>
```

**Why this order?**

- Theme outermost - affects all visual rendering
- Auth second - other contexts need to know if user is logged in
- Data contexts (Posts, Friends, Messages) don't depend on each other, any order works

---

## Testing Checklist

- [ ] App renders without errors in browser
- [ ] All context providers accessible throughout app (useTheme, useAuth, etc. work)
- [ ] API calls to backend include Authorization header with token
- [ ] 401 errors automatically log user out and redirect to /login
- [ ] Theme toggle switches between light and dark mode
- [ ] Theme preference persists after page refresh (localStorage)
- [ ] Pablo's CSS variables update when theme changes
- [ ] Sun/moon icon shows correct current theme

---

## Integration Testing

After team members build their features:

- [ ] Natalia's login sets token → your apiClient uses it
- [ ] Colin's posts service can make API calls using your apiClient
- [ ] Crystal's friends service can make API calls using your apiClient
- [ ] All API calls automatically fail gracefully when token expires
