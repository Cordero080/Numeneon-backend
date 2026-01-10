# Claude Teaching Prompt - Numeneon App Deep Dive

Hey Claude! I need you to teach me the architecture, component flow, syntax, and systems thinking behind my Numeneon social media app. I built most of this with Copilot's help, and now I need to deeply understand it for technical interviews. I don't just want to memorize - I want to think like a systems architect.

---

## 🎯 Learning Objectives

I need to master:

1. **Component Architecture**: Parent-child relationships, data flow, component hierarchy
2. **React Syntax**: Hooks (useState, useEffect), props, JSX, event handlers, conditional rendering
3. **Routing Flow**: React Router setup, navigation, URL parameters, protected routes
4. **State Management**: Where state lives, when to lift state up, future global state needs
5. **Styling System**: Global styles, component styles, holographic design patterns, responsive CSS
6. **API Integration**: Frontend-backend communication, endpoints, authentication, error handling
7. **Responsive Design**: Mobile-first approach, media queries, responsive state management
8. **Systems Thinking**: Why architecture decisions were made, trade-offs, scalability considerations

---

## 📚 Teaching Approach I Need

Please teach me using:

1. **Concept Explanation**: Start with high-level concept, then drill into specifics
2. **Code Examples**: Show actual code from my project, explain line-by-line
3. **Visual Flow**: Describe data flow with arrows/steps (e.g., "User clicks → state updates → API call → re-render")
4. **Interview Questions**: Pose technical interview questions and walk me through answers
5. **Tracing Exercises**: Have me trace a feature from user action to database and back
6. **Why Over What**: Explain WHY we chose this architecture, not just WHAT it does
7. **Common Pitfalls**: Show me what mistakes to avoid and anti-patterns

---

## 🏗️ Project Structure You'll Be Teaching

```
numeneon/
├── .gitignore
├── BACKEND_README.md
├── BACKEND_SETUP.md
├── Makefile
├── README.md
│
├── backend/
│   ├── db.sqlite3
│   ├── manage.py
│   ├── seed_posts.py
│   │
│   ├── numeneon/                 # Django project settings
│   │   ├── __init__.py
│   │   ├── asgi.py
│   │   ├── settings.py           # CORS, installed apps, database config
│   │   ├── urls.py               # Main URL router (includes app URLs)
│   │   └── wsgi.py
│   │
│   ├── users/                    # User management
│   │   ├── __init__.py
│   │   ├── apps.py
│   │   ├── models.py             # User model (extends Django User)
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   ├── management/
│   │   │   └── commands/
│   │   │       └── create_test_user.py
│   │   └── migrations/
│   │       ├── __init__.py
│   │       └── 0001_initial.py
│   │
│   ├── posts/                    # Posts CRUD
│   │   ├── __init__.py
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py             # Post model (with parent for replies, likes)
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── views.py
│   │   └── migrations/
│   │       ├── __init__.py
│   │       ├── 0001_initial.py
│   │       ├── 0002_post_parent.py
│   │       ├── 0003_post_comment_count_post_likes_count_and_more.py
│   │       └── 0004_like.py      # Like model migration
│   │
│   └── friends/                  # Friend relationships
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── models.py             # Friendship model
│       ├── serializers.py
│       ├── urls.py
│       ├── views.py
│       └── migrations/
│           ├── __init__.py
│           └── 0001_initial.py
│
├── docs/
│   ├── ProfileCard-Flip-System.txt
│   ├── copilot-task-long.txt
│   ├── prompt.md
│   ├── study.md
│   │
│   ├── copilot-task/             # Detailed implementation guides
│   │   ├── 00-START-HERE.md
│   │   ├── 01-CONTEXT-AND-STRATEGY.md
│   │   ├── 02-PSEUDOCODE-EXAMPLES.md
│   │   ├── 03-BACKEND-INSTRUCTIONS.md
│   │   └── 04-FRONTEND-INSTRUCTIONS.md
│   │
│   ├── dev-sessions/
│   │   ├── README.md
│   │   └── 2024-12-23-profile-navigation.md
│   │
│   ├── features/                 # Planned features
│   │   ├── ActivityVisualization.md
│   │   ├── PresentationTalkingPoints.md
│   │   ├── ProfileCardFeatures.md
│   │   ├── ProfileCardFlipSystem.md
│   │   ├── RiverTimeline.md
│   │   └── VisualIdentitySystem.md
│   │
│   ├── features-implemented/     # Completed feature documentation
│   │   ├── CardUserHeaders.md
│   │   ├── EngagementAnalytics.md
│   │   ├── MessagingSystem.md
│   │   ├── MobileCategoryTabs.md
│   │   ├── MobileMessageModal.md
│   │   ├── ProfilePrivacyControls.md
│   │   ├── SearchModal.md
│   │   ├── TimelineCarousel.md
│   │   ├── UnifiedCloseButton.md
│   │   └── UserProfileNavigation.md
│   │
│   ├── refactoring/
│   │   └── SVG-Icons-Refactor.md
│   │
│   ├── stretch-goals/
│   │   ├── AdvancedAnalytics.md
│   │   ├── EngagementRing.md
│   │   ├── MySpaceEasterEgg.md
│   │   ├── Posts.md
│   │   └── README.md
│   │
│   ├── study/
│   │   ├── ActivityVisualizationDeepDive.md
│   │   └── study-prompt.md
│   │
│   ├── team-plan/                # Team member assignments
│   │   ├── team-structure.md
│   │   ├── colin.md
│   │   ├── crystal.md
│   │   ├── natalia.md
│   │   ├── pablo.md
│   │   └── tito.md
│   │
│   └── wireframe-prompt/
│       └── NUMENEON-WIREFRAME-GUIDE.md
│
└── frontend/
    ├── .gitignore
    ├── eslint.config.js
    ├── index.html
    ├── package.json
    ├── package-lock.json
    ├── README.md
    ├── vite.config.js
    │
    ├── public/
    │   └── vite.svg
    │
    └── src/
        ├── App.jsx                # Root component with routing
        ├── main.jsx               # React app entry point
        │
        ├── assets/
        │   ├── icons/              # SVG icon assets
        │   └── icons.jsx           # Icon component exports
        │
        ├── components/
        │   │
        │   ├── layout/            # Persistent UI components
        │   │   │
        │   │   ├── SideNav/
        │   │   │   ├── SideNav.jsx
        │   │   │   ├── SideNav.scss
        │   │   │   └── index.js
        │   │   │
        │   │   └── TopBar/
        │   │       ├── TopBar.jsx
        │   │       ├── TopBar.scss
        │   │       ├── index.js
        │   │       │
        │   │       ├── MessageModal/       # Direct messaging system
        │   │       │   ├── MessageModal.jsx
        │   │       │   ├── MessageModal.scss
        │   │       │   └── styles/
        │   │       │       ├── _animations.scss
        │   │       │       ├── _chat.scss
        │   │       │       ├── _composer.scss
        │   │       │       ├── _conversations.scss
        │   │       │       ├── _header.scss
        │   │       │       ├── _light-mode.scss
        │   │       │       ├── _overlay.scss
        │   │       │       └── _responsive.scss
        │   │       │
        │   │       ├── NotificationModal/    # Notification center
        │   │       │   ├── NotificationModal.jsx
        │   │       │   ├── NotificationModal.scss
        │   │       │   └── index.js
        │   │       │
        │   │       └── SearchModal/          # Global search functionality
        │   │           ├── SearchModal.jsx
        │   │           ├── SearchModal.scss
        │   │           └── index.js
        │   │
        │   ├── pages/             # Route-level components
        │   │   │
        │   │   ├── About/
        │   │   │   ├── About.jsx
        │   │   │   ├── About.scss
        │   │   │   └── index.js
        │   │   │
        │   │   ├── Friends/
        │   │   │   ├── Friends.jsx
        │   │   │   ├── Friends.scss
        │   │   │   └── index.js
        │   │   │
        │   │   ├── Home/
        │   │   │   ├── Home.jsx
        │   │   │   ├── Home.scss
        │   │   │   ├── index.js
        │   │   │   │
        │   │   │   ├── components/
        │   │   │   │   ├── DeleteConfirmModal/
        │   │   │   │   │   ├── DeleteConfirmModal.jsx
        │   │   │   │   │   └── DeleteConfirmModal.scss
        │   │   │   │   │
        │   │   │   │   ├── MediaLightbox/
        │   │   │   │   │   ├── MediaLightbox.jsx
        │   │   │   │   │   ├── MediaLightbox.scss
        │   │   │   │   │   └── styles/
        │   │   │   │   │       ├── _animations.scss
        │   │   │   │   │       ├── _comments.scss
        │   │   │   │   │       ├── _image.scss
        │   │   │   │   │       ├── _info-panel.scss
        │   │   │   │   │       ├── _light-mode.scss
        │   │   │   │   │       ├── _overlay.scss
        │   │   │   │   │       └── _responsive.scss
        │   │   │   │   │
        │   │   │   │   ├── TimelineRiverFeed/
        │   │   │   │   │   ├── TimelineRiverFeed.jsx
        │   │   │   │   │   ├── TimelineRiverFeed.scss
        │   │   │   │   │   └── index.js
        │   │   │   │   │
        │   │   │   │   └── TimelineRiverRow/
        │   │   │   │       ├── TimelineRiverRow.jsx
        │   │   │   │       ├── TimelineRiverRow.scss
        │   │   │   │       ├── index.js
        │   │   │   │       └── styles/
        │   │   │   │           ├── _base.scss
        │   │   │   │           ├── _carousel.scss
        │   │   │   │           ├── _composer.scss
        │   │   │   │           ├── _desktop-stack-nav.scss
        │   │   │   │           ├── _light-mode.scss
        │   │   │   │           ├── _post-actions.scss
        │   │   │   │           ├── _post-card.scss
        │   │   │   │           ├── _post-media.scss
        │   │   │   │           ├── _responsive.scss
        │   │   │   │           ├── _smart-deck.scss
        │   │   │   │           └── _thread.scss
        │   │   │   │
        │   │   │   └── utils/
        │   │   │       └── groupPosts.js
        │   │   │
        │   │   ├── Landing/
        │   │   │   ├── Landing.jsx
        │   │   │   ├── Landing.scss
        │   │   │   └── index.js
        │   │   │
        │   │   ├── Login/
        │   │   │   ├── Login.jsx
        │   │   │   ├── Login.scss
        │   │   │   └── index.js
        │   │   │
        │   │   ├── NotFound/
        │   │   │   ├── NotFound.jsx
        │   │   │   ├── NotFound.scss
        │   │   │   └── index.js
        │   │   │
        │   │   ├── Profile/
        │   │   │   ├── Profile.jsx
        │   │   │   ├── Profile.scss
        │   │   │   ├── index.js
        │   │   │   │
        │   │   │   └── components/
        │   │   │       │
        │   │   │       ├── ComposerModal/
        │   │   │       │   ├── ComposerModal.jsx
        │   │   │       │   ├── ComposerModal.scss
        │   │   │       │   └── index.js
        │   │   │       │
        │   │   │       ├── ProfileCard/
        │   │   │       │   ├── ProfileCard.jsx
        │   │   │       │   ├── ProfileCard.scss
        │   │   │       │   ├── index.js
        │   │   │       │   │
        │   │   │       │   └── components/
        │   │   │       │       ├── ActivityVisualization/
        │   │   │       │       │   ├── ActivityVisualization.jsx
        │   │   │       │       │   ├── ActivityVisualization.scss
        │   │   │       │       │   └── index.js
        │   │   │       │       │
        │   │   │       │       ├── PostTypeBreakdown/
        │   │   │       │       │   ├── PostTypeBreakdown.jsx
        │   │   │       │       │   ├── PostTypeBreakdown.scss
        │   │   │       │       │   └── index.js
        │   │   │       │       │
        │   │   │       │       ├── ProfileCardBack/
        │   │   │       │       │   ├── ProfileCardBack.jsx
        │   │   │       │       │   ├── ProfileCardBack.scss
        │   │   │       │       │   └── index.js
        │   │   │       │       │
        │   │   │       │       ├── ProfileCardFront/
        │   │   │       │       │   ├── ProfileCardFront.jsx
        │   │   │       │       │   ├── ProfileCardFront.scss
        │   │   │       │       │   └── index.js
        │   │   │       │       │
        │   │   │       │       └── QuickSettings/
        │   │   │       │           ├── QuickSettings.jsx
        │   │   │       │           ├── QuickSettings.scss
        │   │   │       │           └── index.js
        │   │   │       │
        │   │   │       └── TimelineRiver/
        │   │   │           ├── TimelineRiver.jsx
        │   │   │           ├── TimelineRiver.scss
        │   │   │           └── index.js
        │   │   │
        │   │   └── Signup/
        │   │       ├── Signup.jsx
        │   │       ├── Signup.scss
        │   │       └── index.js
        │   │
        │   └── ui/                # Reusable UI components
        │       ├── ProtectedRoute.jsx
        │       └── ThemeToggle/
        │           ├── ThemeToggle.jsx
        │           ├── ThemeToggle.scss
        │           └── index.js
        │
        ├── contexts/              # React Context providers
        │   ├── AuthContext.jsx
        │   ├── FriendsContext.jsx
        │   ├── MessageContext.jsx
        │   ├── PostsContext.jsx
        │   ├── ThemeContext.jsx
        │   └── index.js
        │
        ├── services/              # API service layer
        │   ├── apiClient.js
        │   ├── friendsService.js
        │   └── postsService.js
        │
        └── styles/                # Global SCSS modules
            ├── main.scss          # Main entry (imports all partials)
            ├── _animations.scss
            ├── _blobs.scss
            ├── _buttons.scss
            ├── _cards.scss
            ├── _layout.scss
            ├── _light-mode.scss
            ├── _mixins.scss
            ├── _reset.scss
            ├── _theme.scss
            ├── _typography.scss
            ├── _utilities.scss
            └── _variables.scss
```

---

## 🔑 Key Files to Focus On

### Critical Path (Teach these first)

1. **`frontend/src/main.jsx`** - How React boots up
2. **`frontend/src/App.jsx`** - Routing structure, component imports
3. **`frontend/src/components/layout/SideNav/SideNav.jsx`** - Responsive state management example
4. **`frontend/src/components/pages/Home/Home.jsx`** - Main feature component
5. **`frontend/src/components/pages/Home/components/TimelineRiverFeed/TimelineRiverFeed.jsx`** - Data transformation logic
6. **`frontend/src/components/pages/Profile/Profile.jsx`** - View toggle state management
7. **`backend/numeneon/urls.py`** - Backend routing
8. **`backend/posts/models.py`** - Database models (Post, Like)
9. **`backend/posts/views.py`** - API endpoint logic
10. **`backend/posts/serializers.py`** - Data serialization

### Context Providers (Global State)

1. **`frontend/src/contexts/AuthContext.jsx`** - Authentication state management
2. **`frontend/src/contexts/PostsContext.jsx`** - Posts data and operations
3. **`frontend/src/contexts/FriendsContext.jsx`** - Friend relationships
4. **`frontend/src/contexts/MessageContext.jsx`** - Direct messaging state
5. **`frontend/src/contexts/ThemeContext.jsx`** - Light/dark theme toggle

### Styling Deep Dive

1. **`frontend/src/styles/_variables.scss`** - Design tokens (colors, spacing, typography)
2. **`frontend/src/styles/_utilities.scss`** - Reusable utility classes
3. **`frontend/src/styles/_reset.scss`** - Global reset and base
4. **`frontend/src/styles/main.scss`** - Entry point that imports all partials
5. **`frontend/src/components/pages/Home/Home.scss`** - Holographic design patterns
6. **`frontend/src/components/layout/SideNav/SideNav.scss`** - Responsive navigation
7. **`frontend/src/components/pages/Home/components/TimelineRiverRow/TimelineRiverRow.scss`** - Card type differentiation

---

## 🎨 Design System to Explain

### Holographic Cosmic Black Theme

**Core Concept**: Futuristic glassmorphism with dark backgrounds, gradient accents, and shimmer animations

**Key Patterns**:

1. **Cosmic Black Backgrounds**:

```css
background: radial-gradient(
    circle at 20% 50%,
    rgba(26, 115, 231, 0.15) 0%,
    transparent 50%
  ), radial-gradient(
    circle at 80% 80%,
    rgba(220, 8, 188, 0.15) 0%,
    transparent 50%
  ), radial-gradient(
    circle at 40% 10%,
    rgba(26, 231, 132, 0.1) 0%,
    transparent 50%
  ), #0a0a0a;
```

_Explain: Why layered radial gradients? How does this create depth?_

2. **Shimmer Animation**:

```css
@keyframes dark-holographic-shimmer {
  0%,
  100% {
    background-position: 0% 50%;
    opacity: 0.8;
  }
  50% {
    background-position: 100% 50%;
    opacity: 1;
  }
}

animation: dark-holographic-shimmer 8s ease infinite;
background-size: 200% 200%;
```

_Explain: How does background-position create movement? Why 200% size?_

3. **Gradient Borders via Pseudo-Elements** (Story Cards):

```css
.story-card {
  position: relative;
  background: rgba(26, 25, 25, 0.15);
  backdrop-filter: blur(25px);
  border-radius: 24px;
}

.story-card::before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: 24px;
  padding: 0.8px;
  background: linear-gradient(
    135deg,
    rgba(26, 231, 132, 0.5),
    rgba(26, 115, 231, 0.5),
    rgba(220, 8, 188, 0.5),
    rgba(26, 231, 132, 0.5)
  );
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events: none;
}
```

_Explain: Why use ::before? What does mask-composite do? Why pointer-events: none?_

4. **Organic Border Radius** (Buttons):

```css
border-radius: 60% 40% 55% 45% / 45% 55% 40% 60%;
```

_Explain: What do these 8 values mean? How does this create organic shapes?_

**Color Palette**:

- Primary Blue: `#1a73e7` / `rgba(26, 115, 231, x)`
- Primary Green: `#1ae784` / `rgba(26, 231, 132, x)`
- Primary Magenta: `#dc08bc` / `rgba(220, 8, 188, x)`
- Base Black: `#0a0a0a`
- Text White: `#ffffff` / `rgba(255, 255, 255, 0.95)`

---

## 🧩 Component Architecture to Teach

### App.jsx Structure

```javascript
import { BrowserRouter, Routes, Route } from "react-router-dom";
import TopBar from "./components/layout/TopBar";
import SideNav from "./components/layout/SideNav";
// ... page imports

function App() {
  return (
    <BrowserRouter>
      <TopBar />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/home" element={<Home />} />
        <Route path="/profile/:username" element={<Profile />} />
        <Route path="/friends" element={<Friends />} />
        <Route path="/about" element={<About />} />
      </Routes>
      <SideNav />
    </BrowserRouter>
  );
}
```

**Teach me**:

- Why are TopBar and SideNav outside `<Routes>`?
- What does `<Route path="/profile/:username">` mean?
- How does React Router prevent full page refreshes?
- What's the difference between `<Link>` and `<a>`?
- When would we need nested routes?

---

### SideNav Responsive Logic

```javascript
const [isDesktop, setIsDesktop] = useState(window.innerWidth > 768);

useEffect(() => {
  const handleResize = () => {
    setIsDesktop(window.innerWidth > 768);
  };

  window.addEventListener("resize", handleResize);

  return () => window.removeEventListener("resize", handleResize);
}, []);

return (
  <nav className={`main-nav ${isDesktop ? "left-nav" : "bottom-nav"}`}>
    {/* nav items */}
  </nav>
);
```

**Teach me**:

- Why useState for window width instead of just checking in render?
- What does `useEffect(() => {}, [])` with empty array mean?
- Why do we need the cleanup function (return)?
- What happens if we forget to remove the event listener?
- How does conditional className work?
- Could we use CSS media queries alone? Why or why not?

---

### Home Component Structure

```javascript
// Expected structure (teach me if this is correct)
function Home() {
  const [posts, setPosts] = useState([]);
  const [isComposerOpen, setIsComposerOpen] = useState(false);

  useEffect(() => {
    // Fetch posts from API
    fetchPosts();
  }, []);

  const fetchPosts = async () => {
    // API call logic
  };

  return (
    <div className="feed-container">
      <div className="story-carousel">{/* Story cards */}</div>

      <div className="composer-input" onClick={() => setIsComposerOpen(true)}>
        {/* Quick composer */}
      </div>

      {isComposerOpen && (
        <ComposerModal onClose={() => setIsComposerOpen(false)} />
      )}

      <TimelineRiverFeed posts={posts} />
    </div>
  );
}
```

**Teach me**:

- Why fetch in useEffect instead of directly in component?
- What's the dependency array `[]` doing?
- How do we pass data from Home to TimelineRiverFeed?
- What's the best way to handle loading states?
- How should we handle API errors?
- When should we refetch posts?

---

### Profile View Toggle Pattern

```javascript
const [activeView, setActiveView] = useState("timeline");

return (
  <div className="user-profile-page">
    <ProfileCard user={userData} />

    <div className="view-mode-toggle">
      <button
        className={`view-toggle-btn ${
          activeView === "timeline" ? "active" : ""
        }`}
        onClick={() => setActiveView("timeline")}
      >
        Timeline
      </button>
      <button
        className={`view-toggle-btn ${
          activeView === "friends" ? "active" : ""
        }`}
        onClick={() => setActiveView("friends")}
      >
        Friends
      </button>
    </div>

    {activeView === "timeline" ? (
      <TimelineRiver posts={userPosts} />
    ) : (
      <FriendsList friends={userFriends} />
    )}
  </div>
);
```

**Teach me**:

- Why use conditional rendering instead of CSS display: none?
- How does ternary operator work in JSX?
- What's the performance difference between approaches?
- Could we use switch statement? When would we?
- How do we prevent re-fetching data on every toggle?

---

## 🔄 Data Flow to Trace

### Example 1: User Creates a Post

Walk me through this flow step-by-step:

1. User types in composer textarea
2. User clicks "Post" button
3. Form submits
4. API request sent
5. Backend processes
6. Database updated
7. Response returned
8. Frontend updates
9. UI re-renders

**For each step, explain**:

- What code executes?
- What file is it in?
- What state changes?
- What triggers the next step?
- What could go wrong?

---

### Example 2: User Navigates to Profile

Trace this flow:

1. User clicks Profile icon in SideNav
2. React Router navigates
3. Profile component mounts
4. User data fetched
5. Profile renders

**Explain**:

- How does `<Link to="/profile/:username">` work?
- How does Profile component get the username?
- When does useEffect run?
- What happens to the old component (Home)?
- How do we pass data between routes?

---

## 🎤 Interview Questions to Prepare Me For

### React Fundamentals

1. "Explain the difference between props and state in your Numeneon app. Give examples from your code."
2. "Walk me through your component hierarchy. Which components are parents of which?"
3. "Why did you choose functional components with hooks instead of class components?"
4. "Explain how React Router works in your App.jsx. What happens when a user navigates?"
5. "What's the purpose of the dependency array in useEffect? Show me examples from your code."

### State Management

1. "Where does authentication state live in your app? How would you make it global?"
2. "Explain the data flow when a user creates a post. Where is state updated?"
3. "When would you lift state up? Give me an example from your app."
4. "How do you prevent unnecessary re-renders in your components?"
5. "What are the trade-offs of component-level state vs global state?"

### Styling & CSS

1. "Explain your holographic design system. How do you achieve gradient borders?"
2. "Why use pseudo-elements for decorative effects instead of extra divs?"
3. "Walk me through your responsive design strategy. How does SideNav adapt?"
4. "What's the difference between backdrop-filter and background-filter?"
5. "Explain mask-composite. What problem does it solve in your story cards?"

### API Integration

1. "How does your frontend communicate with the backend? What library do you use?"
2. "Explain your API endpoint structure. How are URLs organized?"
3. "How do you handle authentication tokens in API requests?"
4. "What happens if an API call fails? How do you handle errors?"
5. "Explain the difference between optimistic UI updates and waiting for server response."

### Architecture & Design

1. "Why did you organize components into layout, pages, and ui folders?"
2. "Explain the Single Responsibility Principle in the context of your components."
3. "How would you add real-time features like live notifications?"
4. "What are the benefits of separating concerns between frontend and backend?"
5. "If you had to refactor one thing about your architecture, what would it be and why?"

### Performance

1. "How would you optimize your Home feed for 1000+ posts?"
2. "Explain when you'd use React.memo, useCallback, and useMemo."
3. "What's the performance difference between conditional rendering and CSS display: none?"
4. "How would you implement infinite scroll on your timeline?"
5. "Explain code splitting. Where would you apply it in this app?"

---

## 🧠 Systems Thinking Exercises

### Exercise 1: Feature Planning

"I want to add a 'like' feature to posts. Walk me through:"

- What components need to change?
- What new state do we need?
- What API endpoints do we need?
- How does the data flow?
- What edge cases should we handle?
- How do we make it performant?

### Exercise 2: Bug Tracing

"Users report the feed doesn't update after posting. How would you debug?"

- Where would you start looking?
- What tools would you use?
- What console.logs would you add?
- What are the likely causes?
- How would you fix it?

### Exercise 3: Architecture Decision

"Should we use Context API or Redux for global state? Explain trade-offs."

- What are the benefits of each?
- What are the drawbacks?
- How much state do we have?
- How complex is the data flow?
- What's your recommendation and why?

### Exercise 4: Scalability Planning

"The app is growing to 100K users. What changes are needed?"

- Database optimization?
- API caching?
- Frontend performance?
- State management refactor?
- Infrastructure changes?

---

## 📋 Specific Concepts to Clarify

### React Hooks Deep Dive

Please explain in detail with examples from my code:

1. **useState**:

   - When to use vs when to use refs?
   - How does batching work?
   - Functional updates (setState(prev => ...))
   - Multiple setState calls in one function

2. **useEffect**:

   - Lifecycle equivalent (componentDidMount, etc.)
   - Cleanup functions (when/why)
   - Dependency array rules
   - Common mistakes (infinite loops, stale closures)
   - useEffect vs useLayoutEffect

3. **Custom Hooks** (future):
   - When to extract logic into custom hook?
   - How to name them?
   - Example: useAuth, useFetch, useResponsive

### React Router Deep Dive

1. **Routing Concepts**:

   - BrowserRouter vs HashRouter
   - Route matching algorithm
   - URL parameters (`:username`)
   - Query strings (search params)
   - Programmatic navigation (useNavigate)

2. **Advanced Patterns**:
   - Protected routes (auth required)
   - Nested routes
   - Route-based code splitting
   - Redirects and fallbacks

### CSS Architecture

1. **Pseudo-Elements**:

   - ::before vs ::after
   - content property
   - When to use vs extra elements
   - Limitations (no pseudo on void elements)

2. **Advanced CSS**:

   - backdrop-filter browser support
   - mask vs clip-path
   - Custom properties (CSS variables)
   - calc() function use cases

3. **Responsive Patterns**:
   - Mobile-first vs desktop-first
   - When to use JS vs CSS media queries
   - Container queries (future)
   - Fluid typography

### Django REST Framework

1. **Models**:

   - Field types (CharField, ForeignKey, etc.)
   - Model methods
   - Meta class options
   - Relationships (OneToMany, ManyToMany)

2. **Serializers**:

   - ModelSerializer vs Serializer
   - Field validation
   - Nested serializers
   - Read-only vs write-only fields

3. **Views**:

   - APIView vs ViewSet
   - Generic views (ListCreateAPIView, etc.)
   - Mixins
   - Permissions and authentication

4. **URLs**:
   - Router (DefaultRouter)
   - URL patterns
   - Namespacing
   - API versioning

---

## 🎯 Outcome I'm Looking For

After you teach me, I should be able to:

1. **Explain any part of the codebase** to a senior engineer
2. **Trace data flow** from user action to database and back
3. **Justify architectural decisions** (why components are structured this way)
4. **Identify code smells** and suggest refactors
5. **Design new features** with proper component structure
6. **Debug issues** by understanding the system holistically
7. **Answer interview questions** with confidence and specificity
8. **Think in terms of trade-offs** (not just "right" vs "wrong")
9. **Understand performance implications** of my code choices
10. **Explain styling patterns** and when to use each technique

---

## 📝 Teaching Format I Prefer

For each concept:

1. **What**: High-level explanation
2. **Where**: Show me in my code (with file paths and line numbers)
3. **Why**: Explain the reasoning and trade-offs
4. **How**: Walk through the mechanics step-by-step
5. **Alternatives**: What other approaches exist?
6. **Common Mistakes**: What to avoid
7. **Interview Question**: How would I explain this in an interview?
8. **Practice Exercise**: A small task to reinforce learning

---

## 🚀 Let's Start!

Please begin by:

1. **High-level architecture overview**: Explain how frontend and backend connect
2. **Component tree visualization**: Show me the parent-child relationships
3. **Data flow example**: Trace one feature end-to-end (like creating a post)
4. **Routing explanation**: How does navigation work?
5. **Styling system**: Explain the holographic design pattern

Then, based on my questions, we can dive deeper into specific files and concepts.

I'm ready to learn! Please teach me like I'm going to be grilled by a senior engineer in a technical interview, and I need to prove I understand not just what the code does, but WHY it's structured this way and HOW all the pieces fit together.

Let's build my systems thinking! 🧠🚀

---

## 🏆 Implemented Features to Study

These features are already built - study them to understand implementation patterns:

### Layout & Navigation

1. **SearchModal** (`TopBar/SearchModal/`) - Global search with filtering
2. **NotificationModal** (`TopBar/NotificationModal/`) - Real-time notification center
3. **MessageModal** (`TopBar/MessageModal/`) - Direct messaging with conversation view
4. **SideNav** - Responsive navigation (desktop sidebar ↔ mobile bottom nav)

### Profile System

1. **ProfileCard Flip System** - 3D card flip with front/back views
2. **ProfileCardFront** - User avatar, stats, bio display
3. **ProfileCardBack** - ActivityVisualization, QuickSettings, PostTypeBreakdown
4. **ProfilePrivacyControls** - Visibility settings per profile section
5. **UserProfileNavigation** - Navigate to any user's profile via clicking headers

### Timeline & Posts

1. **TimelineRiverFeed** - Main feed component with post grouping
2. **TimelineRiverRow** - Individual post rows with carousel support
3. **TimelineCarousel** - Horizontal scrolling through post stacks
4. **MediaLightbox** - Full-screen media viewing with comments
5. **DeleteConfirmModal** - Safe deletion confirmation pattern
6. **CardUserHeaders** - Clickable user headers on all cards

### Analytics & Visualization

1. **ActivityVisualization** - GitHub-style contribution grid
2. **PostTypeBreakdown** - Pie/bar chart of content types
3. **EngagementAnalytics** - Likes, comments, shares metrics

### Mobile Experience

1. **MobileCategoryTabs** - Touch-friendly category switching
2. **MobileMessageModal** - Optimized messaging for small screens
3. **UnifiedCloseButton** - Consistent close pattern across modals

---

## 🔄 Context Provider Deep Dive

Study these context files to understand global state management:

### AuthContext.jsx

**Purpose**: Manage user authentication state
**Key Concepts**:

- Login/logout functions
- Token storage (localStorage)
- Current user data
- Protected route integration

**Interview Question**: "How do you persist authentication across page refreshes?"

### PostsContext.jsx

**Purpose**: Centralized posts data management
**Key Concepts**:

- CRUD operations for posts
- Optimistic updates
- Cache invalidation patterns
- Feed pagination

**Interview Question**: "Why use Context instead of prop drilling for posts?"

### FriendsContext.jsx

**Purpose**: Friend relationships and suggestions
**Key Concepts**:

- Friend request flow (send/accept/decline)
- Friends list management
- Friend suggestions algorithm

### MessageContext.jsx

**Purpose**: Direct messaging state
**Key Concepts**:

- Conversation management
- Message history
- Unread counts
- Real-time updates (future WebSocket)

### ThemeContext.jsx

**Purpose**: Light/dark mode toggle
**Key Concepts**:

- CSS variable switching
- localStorage persistence
- System preference detection
- Theme-aware component styling

---

## 🎨 SCSS Architecture Study

Your project uses a modular SCSS architecture. Study these patterns:

### Global Partials (`frontend/src/styles/`)

- **\_variables.scss** - CSS custom properties, breakpoints
- **\_mixins.scss** - Reusable SCSS mixins (responsive, flexbox helpers)
- **\_reset.scss** - Normalize browser defaults
- **\_typography.scss** - Font stacks, text utilities
- **\_animations.scss** - Keyframes, transition presets
- **\_buttons.scss** - Button variants and states
- **\_cards.scss** - Card component styles
- **\_layout.scss** - Grid systems, containers
- **\_light-mode.scss** - Light theme overrides
- **\_blobs.scss** - Decorative blob shapes
- **\_utilities.scss** - Utility classes (margins, padding, etc.)
- **\_theme.scss** - Theme-specific styling

### Component-Level SCSS Patterns

Each component folder has its own `.scss` file. Complex components split styles into partials:

```
TimelineRiverRow/
├── TimelineRiverRow.scss      # Main styles, imports partials
└── styles/
    ├── _base.scss
    ├── _carousel.scss
    ├── _light-mode.scss
    └── _responsive.scss
```

**Interview Question**: "Why split component styles into partials?"

---

## 🔌 API Service Layer Study

### apiClient.js

**Purpose**: Axios instance configuration
**Key Concepts**:

- Base URL configuration
- Request/response interceptors
- Token injection
- Error handling middleware

### postsService.js

**Purpose**: Posts API operations
**Key Methods to understand**:

- `getPosts()` - Fetch feed with pagination
- `createPost()` - New post with media upload
- `updatePost()` - Edit existing post
- `deletePost()` - Remove post
- `likePost()` / `unlikePost()` - Engagement

### friendsService.js

**Purpose**: Friends API operations
**Key Methods**:

- `getFriends()` - User's friend list
- `sendFriendRequest()` - Initiate connection
- `acceptFriendRequest()` - Confirm friendship
- `removeFriend()` - End friendship

---

## 🗄️ Backend Models Study

### Post Model (posts/models.py)

**Fields to understand**:

- `author` - ForeignKey to User
- `content` - TextField for post body
- `parent` - Self-referential ForeignKey (for replies/threads)
- `likes_count` - Denormalized count field
- `comment_count` - Denormalized count field
- `created_at` / `updated_at` - Timestamps

**Interview Question**: "Why denormalize like counts instead of using aggregation?"

### Like Model (posts/models.py)

**Fields**:

- `user` - ForeignKey to User
- `post` - ForeignKey to Post
- `created_at` - Timestamp

**Key Concept**: Unique constraint on (user, post) prevents double-likes

### Friendship Model (friends/models.py)

**Fields**:

- `from_user` - Who sent request
- `to_user` - Who received request
- `status` - pending/accepted/declined
- `created_at` - Timestamp

**Interview Question**: "How would you query mutual friends?"

---

## 📚 Documentation Resources

Your project has excellent documentation - use these for deeper study:

### Implementation Guides (`docs/copilot-task/`)

- **00-START-HERE.md** - Project overview and setup
- **01-CONTEXT-AND-STRATEGY.md** - Architecture decisions explained
- **02-PSEUDOCODE-EXAMPLES.md** - Code patterns and examples
- **03-BACKEND-INSTRUCTIONS.md** - Django/DRF patterns
- **04-FRONTEND-INSTRUCTIONS.md** - React/Vite patterns

### Feature Documentation (`docs/features-implemented/`)

Read these to understand completed features:

- **MessagingSystem.md** - DM architecture
- **SearchModal.md** - Search implementation
- **TimelineCarousel.md** - Carousel logic
- **ProfilePrivacyControls.md** - Privacy patterns
- **EngagementAnalytics.md** - Analytics system
