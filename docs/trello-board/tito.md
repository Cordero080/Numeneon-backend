# 👤 Tito | S | Infrastructure

> API client, theme system, and app entry point

---

## 🏷️ T-Shirt Size: S (6 files)

**Role:** Infrastructure Lead  
**Strengths:** Utilities, configuration  
**Focus:** Foundation layer that everyone depends on

---

## 📋 Task Board

### 🔴 CRITICAL PATH (BUILD FIRST!)

| ID    | Task                                         | Status     | Priority    | Est. Hours |
| ----- | -------------------------------------------- | ---------- | ----------- | ---------- |
| T-001 | apiClient.js - Axios instance + interceptors | 📝 Backlog | 🔴 Critical | 2h         |

### 🟡 CONTEXT & COMPONENTS

| ID    | Task                                     | Status     | Priority  | Est. Hours |
| ----- | ---------------------------------------- | ---------- | --------- | ---------- |
| T-002 | ThemeContext.jsx - Light/dark mode state | 📝 Backlog | 🟡 Medium | 2h         |
| T-003 | ThemeToggle.jsx - Theme switch button    | 📝 Backlog | 🟡 Medium | 1h         |
| T-004 | ThemeToggle/index.js - Barrel export     | 📝 Backlog | 🟢 Low    | 0.1h       |

### 🔴 APP ENTRY (BUILD LAST)

| ID    | Task                                     | Status     | Priority    | Est. Hours |
| ----- | ---------------------------------------- | ---------- | ----------- | ---------- |
| T-005 | main.jsx - Provider nesting + app render | 📝 Backlog | 🔴 Critical | 1h         |

---

## 📊 Progress Tracker

**Total Tasks:** 5  
**Completed:** 0  
**In Progress:** 0  
**Remaining:** 5

```
Progress: [░░░░░░░░░░░░░░░░░░░░] 0%
```

---

## 🔗 Dependencies

**Tito PROVIDES:**

- `apiClient.js` - **EVERYONE** depends on this for HTTP requests
- `ThemeContext` - Pablo's components use theme state
- `main.jsx` - Wraps all providers around app

**Tito CONSUMES:**

- `AuthContext` (Natalia) - Wrapped in main.jsx
- `PostsContext` (Colin) - Wrapped in main.jsx
- `FriendsContext` (Crystal) - Wrapped in main.jsx
- `MessageContext` (Pablo) - Wrapped in main.jsx
- `SearchContext` (Pablo) - Wrapped in main.jsx

---

## ⚠️ CRITICAL: Build Order

```
1. apiClient.js    ← BUILD FIRST (everyone blocked without this)
2. ThemeContext    ← Can build in parallel with others
3. ThemeToggle     ← After ThemeContext
4. main.jsx        ← BUILD LAST (needs all contexts ready)
```

---

## 📝 apiClient.js Configuration

```javascript
import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://localhost:8000", // Django backend
  headers: {
    "Content-Type": "application/json",
  },
});

// Request interceptor - attach JWT token
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("accessToken");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - handle 401 (token expired)
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid - logout user
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

---

## 📝 ThemeContext Pattern

| State/Function  | Description           |
| --------------- | --------------------- |
| `theme`         | 'light' or 'dark'     |
| `toggleTheme()` | Switch between themes |

**Features:**

- Save preference to localStorage
- Read from localStorage on mount
- Default to 'dark' if no preference
- Apply `data-theme` attribute to document root

---

## 📝 main.jsx Provider Nesting

```jsx
// Provider nesting order (outer to inner)
<ThemeProvider>
  {" "}
  {/* Tito - outermost */}
  <AuthProvider>
    {" "}
    {/* Natalia */}
    <PostsProvider>
      {" "}
      {/* Colin */}
      <FriendsProvider>
        {" "}
        {/* Crystal */}
        <MessageProvider>
          {" "}
          {/* Pablo */}
          <SearchProvider>
            {" "}
            {/* Pablo */}
            <App />
          </SearchProvider>
        </MessageProvider>
      </FriendsProvider>
    </PostsProvider>
  </AuthProvider>
</ThemeProvider>
```

**Why this order?**

- Theme is purely visual, doesn't need auth
- Auth is foundation for data contexts
- PostsContext/FriendsContext need auth state
- MessageContext/SearchContext need all data contexts

---

## 📝 ThemeToggle Component

**Features:**

- Sun icon for light mode
- Moon icon for dark mode
- Smooth icon transition animation
- Calls `toggleTheme()` from context
- Small, fits in TopBar

**Icons:** Import from `@assets/icons`

---

## ⚠️ Important Notes

1. **apiClient MUST be first** - All services (auth, posts, friends) import it

2. **Token storage keys:**

   - Access token: `localStorage.getItem('accessToken')`
   - Refresh token: `localStorage.getItem('refreshToken')`

3. **401 handling:**

   - Clear tokens
   - Redirect to /login
   - Forces re-authentication

4. **Theme attribute:**

   - Apply to `<html>` or `<body>` element
   - `document.documentElement.setAttribute('data-theme', theme)`

5. **StrictMode:**
   - Include in main.jsx for development warnings
   - `<React.StrictMode><App /></React.StrictMode>`

---

## 📌 Status Legend

- **📝 Backlog** - Not started
- **🔄 In Progress** - Currently working
- **👀 In Review** - PR submitted
- **✅ Done** - Completed and merged
- **🚫 Blocked** - Waiting on dependency

---

_Last Updated: January 8, 2026_
