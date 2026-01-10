# Natalia's Tasks (Size: L)

## Your Mission

You're building the authentication system - the foundation that lets users create accounts, log in, and access protected features. You're also managing all database migrations to keep the team's database healthy as everyone builds.

## Files You Own

**Important:** Don't touch anyone else's files to avoid merge conflicts!

### Backend Files (11 total)

- `backend/users/models.py` - User profile data structure
- `backend/users/views.py` - Signup, login, logout API endpoints
- `backend/users/serializers.py` - User data validation and formatting
- `backend/users/urls.py` - Auth API routes configuration
- `backend/users/apps.py` - Django app configuration
- `backend/users/__init__.py` - Package marker
- `backend/users/management/__init__.py` - Management commands package
- `backend/users/management/commands/__init__.py` - Commands subpackage
- `backend/users/management/commands/create_test_user.py` - Test user creation script
- `backend/users/migrations/0001_initial.py` - Initial database schema
- `backend/users/migrations/__init__.py` - Migrations package marker

### Frontend Files (10 total)

- `frontend/src/contexts/AuthContext.jsx` - Auth state management (user, login, logout, signup)
- `frontend/src/components/pages/Login/Login.jsx` - Login form component
- `frontend/src/components/pages/Login/Login.scss` - Login page styling
- `frontend/src/components/pages/Login/index.js` - Component export
- `frontend/src/components/pages/Signup/Signup.jsx` - Registration form component
- `frontend/src/components/pages/Signup/Signup.scss` - Signup page styling
- `frontend/src/components/pages/Signup/index.js` - Component export
- `frontend/src/components/ui/ProtectedRoute.jsx` - Route guard for authenticated pages
- `frontend/src/services/authService.js` - Auth API calls wrapper

### Special Responsibility

**Migration Management:** You review and run ALL database migrations (yours, Colin's, Crystal's)

---

## Task Breakdown

### ✅ Task 1: Create User Profile Model

**Files:** `backend/users/models.py`

**What:** Define the database structure for user profiles (extending Django's built-in User model)

**Why:** Every social media app needs to store info about users - username, email, password, profile picture, bio, etc.

**Acceptance Criteria:**

- [ ] Profile model created (extends or relates to Django's User model)
- [ ] User has profile_picture field (optional image)
- [ ] User has bio field (optional text)
- [ ] Passwords are automatically hashed (Django handles this with built-in User)
- [ ] Model appears in Django admin

**Think about:**

- What's the difference between extending AbstractUser vs creating a Profile with OneToOne to User?
- Should every field be required, or can some be optional?
- How do you handle file uploads for profile pictures?

**Helpful Resources:** Django docs on extending the User model

---

### ✅ Task 2: Build Authentication Views & Serializers

**Files:** `backend/users/views.py`, `backend/users/serializers.py`

**What:** Create API endpoints for signup, login, and getting current user info

**Why:** Frontend needs to send credentials and receive JWT tokens to maintain logged-in state

**Acceptance Criteria:**

- [ ] POST /api/auth/signup/ creates new user and returns JWT token
- [ ] POST /api/auth/login/ validates credentials and returns JWT token
- [ ] GET /api/auth/me/ returns current user profile (authenticated only)
- [ ] UserSerializer includes id, username, email, profile_picture, bio
- [ ] Passwords are never exposed in API responses

**Think about:**

- How do you use Django REST Framework's token authentication?
- What fields should be required vs optional in signup?
- How do you validate email format?
- Should you allow duplicate usernames?

**Helpful Resources:** DRF authentication docs, simple JWT

---

### ✅ Task 3: Configure URL Routes

**Files:** `backend/users/urls.py`

**What:** Map URL patterns to your views

**Why:** Frontend needs to know where to send requests (/api/auth/login/, etc.)

**Acceptance Criteria:**

- [ ] POST /api/auth/signup/ mapped to signup view
- [ ] POST /api/auth/login/ mapped to login view
- [ ] GET /api/auth/me/ mapped to current user view

**Think about:**

- Should you use ViewSets with routers or individual function-based views?
- What URL patterns make sense for auth?

---

### ✅ Task 4: Build AuthContext (Frontend State Management)

**Files:** `frontend/src/contexts/AuthContext.jsx`

**What:** Create React context that manages logged-in user state across the app

**Why:** Every component needs to know "who is logged in" without passing props everywhere

**Acceptance Criteria:**

- [ ] Stores current user object (or null if logged out)
- [ ] Provides login(username, password) function
- [ ] Provides signup(userData) function
- [ ] Provides logout() function
- [ ] Stores JWT token in localStorage
- [ ] Automatically fetches current user on app load if token exists
- [ ] Clears user state on logout

**Think about:**

- Where should you store the JWT token? (localStorage, sessionStorage, memory?)
- What happens if the token expires?
- Should you fetch user data on every page load?

**Helpful Resources:** Look at PostsContext pattern (Colin), similar structure

---

### ✅ Task 5: Build Auth Service Layer

**Files:** `frontend/src/services/authService.js`

**What:** Functions that make HTTP calls to your auth API endpoints

**Why:** Separates API logic from React components (cleaner code)

**Acceptance Criteria:**

- [ ] signup(userData) calls POST /api/auth/signup/
- [ ] login(credentials) calls POST /api/auth/login/
- [ ] getCurrentUser() calls GET /api/auth/me/
- [ ] All functions return response data
- [ ] Errors are thrown (not swallowed)

**Think about:**

- Should this file handle the JWT token, or should AuthContext handle it?
- How do you attach the token to requests?

**Helpful Resources:** Uses apiClient.js (Tito builds this)

---

### ✅ Task 6: Build Login & Signup Pages

**Files:** `Login.jsx`, `Login.scss`, `Signup.jsx`, `Signup.scss`, `index.js` files

**What:** User-facing forms for authentication

**Why:** Users need a way to create accounts and log in

**Acceptance Criteria:**

- [ ] Login form has username/email and password fields
- [ ] Signup form has username, email, password, and confirm password fields
- [ ] Forms call AuthContext.login() or AuthContext.signup()
- [ ] Show error messages if auth fails
- [ ] Redirect to /home on successful login/signup
- [ ] Link between Login and Signup pages
- [ ] Styled using Pablo's design system (glass-card, neon-glow mixins)

**Think about:**

- How do you prevent form submission from refreshing the page?
- Should you validate passwords match before sending to backend?
- What if the backend returns an error? How do you show it?

**Helpful Resources:** Pablo's design system in `src/styles/`

---

### ✅ Task 7: Build Protected Route Component

**Files:** `frontend/src/components/ui/ProtectedRoute.jsx`

**What:** Component that blocks unauthenticated users from accessing certain pages

**Why:** Home, Profile, Friends pages should only be accessible when logged in

**Acceptance Criteria:**

- [ ] Checks if user is logged in (via AuthContext)
- [ ] If logged in, renders the child component/route
- [ ] If not logged in, redirects to /login
- [ ] Shows loading state while checking auth status

**Think about:**

- How do you wrap a route with this component?
- When should you check if user is logged in? (useEffect? immediately?)
- What if AuthContext is still loading user data?

**Helpful Resources:** React Router's Navigate component for redirects

---

### ✅ Task 8: Create Test User Management Command

**Files:** `backend/users/management/commands/create_test_user.py`

**What:** Django management command to create test users for development

**Why:** Everyone needs test data to work with

**Acceptance Criteria:**

- [ ] Command: `python manage.py create_test_user`
- [ ] Creates a user with username "testuser", password "password123"
- [ ] Creates profile with sample bio and placeholder avatar
- [ ] Doesn't crash if user already exists

**Think about:**

- How do you handle duplicate usernames gracefully?
- Should you create multiple test users?

---

### ✅ Task 9: Database Migrations

**Files:** `backend/users/migrations/0001_initial.py`

**What:** Auto-generated migration file that creates User/Profile tables in database

**Why:** Django needs these to know how to build the database schema

**Acceptance Criteria:**

- [ ] Run `python manage.py makemigrations` after creating models
- [ ] Run `python manage.py migrate` to apply migrations
- [ ] Verify tables exist in database

**Special Responsibility:** You'll also review and run Colin's and Crystal's migrations

---

## Integration Points

**You provide:**

- Auth API endpoints that return JWT tokens
- AuthContext that other components use via useAuth() hook
- ProtectedRoute that wraps authenticated pages
- User model structure with profile data that others reference

**User data format expected by Pablo's UI:**

```javascript
{
  id: number,
  username: string,
  email: string,
  first_name: string,
  last_name: string,
  profile: {
    id: number,
    bio: string,
    avatar: string | null,  // profile picture URL
    location: string,
    website: string
  }
}
```

**You consume:**

- apiClient.js (Tito) - provides axios instance with JWT handling
- Pablo's design system - use for Login/Signup styling

**Work with:**

- **Tito:** He builds apiClient that your authService uses
- **Colin:** His posts reference your User model (author field)
- **Crystal:** Her friends reference your User model (friend relationships)
- **Pablo:** His UI expects specific user data shape from AuthContext

---

## Testing Checklist

- [ ] Can create new user via /api/auth/signup/
- [ ] Can login with correct credentials
- [ ] Cannot login with wrong password
- [ ] Token is stored in localStorage after login
- [ ] Refresh page - still logged in (token persists)
- [ ] Logout clears token and redirects to /login
- [ ] ProtectedRoute blocks access to /home when logged out
- [ ] ProtectedRoute allows access to /home when logged in
- [ ] Profile picture uploads work (if implemented)

---

## 🚀 Stretch Goals (If You Finish Early)

These are **optional** but great for learning and portfolio building!

### Stretch 1: Password Reset Flow

**Backend:**

- Add `POST /api/auth/forgot-password/` endpoint
- Generate reset token, store expiration time
- (Mock) send email with reset link

**Frontend:**

- Create ForgotPassword.jsx page
- Create ResetPassword.jsx page (with token from URL)
- Add "Forgot password?" link to Login page

**Why it's valuable:** Every production app needs this. Great interview talking point.

---

### Stretch 2: Profile Update Endpoint

**Backend:**

- Add `PATCH /api/auth/me/` to update current user's profile
- Support updating bio, location, website, profile picture
- Validate file uploads (size, type)

**Frontend:**

- Add updateProfile() to AuthContext
- Wire up to Pablo's ProfileCard edit functionality

**Why it's valuable:** Demonstrates PATCH vs PUT, file uploads, partial updates.

---

### Stretch 3: Email Verification Flow

**Backend:**

- Generate verification token on signup
- Add `POST /api/auth/verify-email/` endpoint
- Mark user as verified in database

**Frontend:**

- Show "Check your email" message after signup
- Create VerifyEmail.jsx page

**Why it's valuable:** Production-ready auth requires this. Shows attention to security.

---

### Stretch 4: Become the PR Reviewer

Since auth is foundational, you understand data flow better than most:

- Review Colin's Posts PRs - check how he uses User as author
- Review Crystal's Friends PRs - check how she uses User for relationships
- Review Tito's apiClient PR - verify JWT token handling

**Why it's valuable:** Code review is a key senior developer skill. Shows leadership.

---

### Stretch 5: Write Auth Documentation

Create `docs/features-implemented/AuthenticationSystem.md`:

- Document all auth endpoints with request/response examples
- Explain JWT token flow (access + refresh)
- Show how useAuth() hook works
- Common troubleshooting (token expired, CORS issues)

**Why it's valuable:** Technical writing is underrated. Makes onboarding easier.

---

## 💡 Why Your Work Matters

**You're not just building login forms.** You're building:

1. **The trust layer** - Every request depends on your JWT tokens
2. **The identity system** - Colin's posts know WHO posted because of your User model
3. **The security boundary** - Your ProtectedRoute keeps the app safe
4. **The foundation** - If auth breaks, NOTHING works

When employers ask "What did you build?", you can say:

> "I built the authentication system from scratch - backend JWT auth with Django REST Framework, frontend state management with React Context, protected routes, and the user profile system that every other feature depends on."

That's a **strong** answer. 💪
