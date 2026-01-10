# Colin's Tasks (Size: M)

## Your Mission

You're building the Posts system - the heart of NUMENEON's social feed. Users create posts (thoughts, media, milestones), reply to them, and they all flow into Pablo's cyberpunk Timeline River UI. You're handling both the backend data layer and the frontend state management that ties everything together.

## Files You Own

**Important:** Don't touch anyone else's files to avoid merge conflicts!

### Backend Files (7 total)

- `backend/posts/models.py` - Post data structure (type, content, image, replies)
- `backend/posts/views.py` - Posts API endpoints (CRUD + replies)
- `backend/posts/serializers.py` - Post data validation and formatting
- `backend/posts/urls.py` - Posts API routes configuration
- `backend/posts/apps.py` - Django app configuration
- `backend/posts/__init__.py` - Package marker
- `backend/posts/admin.py` - Django admin interface for posts

### Frontend Files (2 total)

- `frontend/src/contexts/PostsContext.jsx` - Posts state management for entire app
- `frontend/src/services/postsService.js` - Posts API calls wrapper

---

## Task Breakdown

### ✅ Task 1: Create Post Model

**Files:** `backend/posts/models.py`

**What:** Define the database structure for posts

**Why:** This is the core content type - thoughts, media, and milestones that users create

**Acceptance Criteria:**

- [ ] Post has `author` field (ForeignKey to User)
- [ ] Post has `type` field (choices: 'thoughts', 'media', 'milestones')
- [ ] Post has `content` field (text, can be blank for media-only posts)
- [ ] Post has `media_url` field (optional URL field, NOT ImageField)
- [ ] Post has `parent` field (ForeignKey to self, for replies - nullable)
- [ ] Post has `created_at` field (auto-set timestamp)
- [ ] Post has `likes_count` field (integer, default 0)
- [ ] Post has `reply_count` field (integer, default 0) - NOT comment_count!
- [ ] Post has `shares_count` field (integer, default 0)

**Think about:**

- How do you create a self-referential ForeignKey (post replying to another post)?
- What's the difference between `blank=True` and `null=True`?
- For `type` field, how do you restrict to only 3 values? (Django choices)
- Why would `image` need BOTH `blank=True` AND `null=True`?

**Helpful Resources:** Django ForeignKey docs, choices parameter

---

### ✅ Task 2: Build Post Serializers

**Files:** `backend/posts/serializers.py`

**What:** Transform Post model data into JSON for the API, include nested author info

**Why:** Frontend needs author details (username, avatar) with each post, not just author ID

**Acceptance Criteria:**

- [ ] PostSerializer includes all Post model fields
- [ ] Author field is nested (shows username, profile_picture, not just ID)
- [ ] Image field returns full URL, not relative path
- [ ] Created_at is in ISO 8601 format
- [ ] Replies count is included (count of posts with this post as parent)

**Think about:**

- How do you nest another serializer? (SerializerMethodField? Nested serializer?)
- Should you use ModelSerializer or Serializer base class?
- How do you calculate replies count efficiently?

**Helpful Resources:** DRF nested serializers, SerializerMethodField

---

### ✅ Task 3: Build Posts API Views

**Files:** `backend/posts/views.py`

**What:** Create endpoints that handle all post operations

**Why:** Frontend needs to fetch, create, update, delete posts

**Acceptance Criteria:**

- [ ] GET /api/posts/ - List all posts
- [ ] POST /api/posts/ - Create new post (authenticated only)
- [ ] GET /api/posts/:id/ - Get single post
- [ ] PATCH /api/posts/:id/ - Update post (author only)
- [ ] DELETE /api/posts/:id/ - Delete post (author only)
- [ ] GET /api/posts/:id/replies/ - Get all replies to a post
- [ ] POST /api/posts/:id/like/ - Toggle like on a post
- [ ] POST /api/posts/:id/share/ - Share/repost (increments shares_count)

**Think about:**

- Should you use ViewSet or APIView?
- How do you restrict some endpoints to authenticated users only?
- How do you ensure only the author can edit/delete their post?
- For custom endpoints like `/replies/`, how do you add them? (@action decorator?)

**Helpful Resources:** DRF ViewSets, permissions, @action decorator

---

### ✅ Task 4: Configure Posts URL Routes

**Files:** `backend/posts/urls.py`

**What:** Map URL patterns to your views

**Why:** Defines what URLs the frontend can call

**Acceptance Criteria:**

- [ ] All CRUD endpoints mapped correctly
- [ ] Custom endpoints (/replies/, /like/) included
- [ ] Router configured if using ViewSet

**Think about:**

- If using ViewSet, DefaultRouter handles most URLs automatically
- Custom @action endpoints need explicit registration

---

### ✅ Task 5: Django Admin Configuration

**Files:** `backend/posts/admin.py`

**What:** Register Post model in Django admin interface

**Why:** Allows easy viewing/editing of posts during development

**Acceptance Criteria:**

- [ ] Post model registered
- [ ] List display shows author, type, content preview, created_at
- [ ] Can filter by type and author
- [ ] Can search by content

**Think about:**

- What fields are most useful to see in the admin list?
- Should content be truncated in the list view?

---

### ✅ Task 6: Build PostsContext (Frontend State)

**Files:** `frontend/src/contexts/PostsContext.jsx`

**What:** React context that manages all post data for the app

**Why:** Home and Profile pages both need posts - context provides single source of truth

**Acceptance Criteria:**

- [ ] Stores `posts` array in state
- [ ] Provides `fetchPosts()` function
- [ ] Provides `createPost(postData)` function
- [ ] Provides `updatePost(id, updates)` function
- [ ] Provides `deletePost(id)` function
- [ ] Provides `getReplies(parentId)` function
- [ ] Provides `likePost(id)` function
- [ ] Provides `sharePost(id)` function (increments shares_count)
- [ ] Handles loading and error states
- [ ] Fetches posts on mount

**Think about:**

- Should you refetch all posts after creating one, or just add the new post to state?
- How do you handle errors from API calls?
- When should `fetchPosts()` run? (useEffect on mount)
- How do you sort posts? (By created_at, newest first?)

**Helpful Resources:** Look at AuthContext (Natalia) for similar pattern

---

### ✅ Task 7: Build Posts Service Layer

**Files:** `frontend/src/services/postsService.js`

**What:** Functions that make HTTP requests to posts API

**Why:** Separates API logic from React components

**Acceptance Criteria:**

- [ ] `getPosts()` - Fetch all posts
- [ ] `getPost(id)` - Fetch single post
- [ ] `createPost(postData)` - Create new post
- [ ] `updatePost(id, updates)` - Update post
- [ ] `deletePost(id)` - Delete post
- [ ] `getReplies(parentId)` - Fetch replies
- [ ] `likePost(id)` - Toggle like
- [ ] All functions return response.data
- [ ] Image uploads handled with FormData

**Think about:**

- For image uploads, how should data be formatted? (FormData for multipart/form-data)
- Should you handle errors here or let them bubble up to context?
- How do you use apiClient.js (Tito's file)?

**Helpful Resources:** Uses apiClient.js (Tito), FormData for file uploads

---

## Integration Points

**You provide:**

- Posts API endpoints (GET/POST/PATCH/DELETE /api/posts/)
- PostsContext with `usePosts()` hook
- Post data format: `{ id, author: {username, profile_picture}, type, content, image, created_at, parent }`

**You consume:**

- User model (Natalia) - posts have author (ForeignKey to User)
- apiClient.js (Tito) - for making authenticated API calls
- Pablo's TimelineRiverFeed - renders your posts array
- Pablo's ComposerModal - calls your createPost() function

**Work with:**

- **Natalia:** Your Post model references her User model for author field
- **Tito:** Your postsService uses his apiClient
- **Pablo:** His UI expects specific post data format from your context

---

## Post Data Format (Critical!)

Pablo's Timeline UI expects posts in this EXACT format:

```javascript
{
  id: 1,
  author: {
    id: 5,
    username: "alice",
    profile_picture: "https://..."  // full URL
  },
  type: "thoughts",  // or "media" or "milestones" (NOT singular!)
  content: "This is my post text",
  media_url: "https://..." | null,  // NOT 'image'!
  parent: 3 | null,  // ID of parent post if this is a reply
  parent_id: 3 | null,  // Also include parent_id
  created_at: "2024-12-19T10:00:00Z",  // ISO format
  likes_count: 5,
  reply_count: 2,  // NOT comment_count!
  shares_count: 3,  // NEW - required for share button
  is_liked: false  // Has current user liked this post?
}
```

**Column Logic:**

- `type === 'thoughts'` → Left column (text posts)
- `type === 'media'` → Center column (image posts)
- `type === 'milestones'` → Right column (achievements)

---

## Testing Checklist

- [ ] Can create new post via /api/posts/
- [ ] Can create post with image upload
- [ ] Can create reply to existing post (parent field set)
- [ ] Can fetch all posts via /api/posts/
- [ ] Can update own post (content, image)
- [ ] Cannot update someone else's post (403 error)
- [ ] Can delete own post
- [ ] Cannot delete someone else's post (403 error)
- [ ] Can fetch replies to a post via /api/posts/:id/replies/
- [ ] Posts show correct author info (username, avatar)
- [ ] Posts appear in correct Timeline River column based on type
- [ ] PostsContext.fetchPosts() populates posts in UI
- [ ] PostsContext.createPost() adds post to Timeline immediately
