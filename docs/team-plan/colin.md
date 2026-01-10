# Colin's Tasks - Posts System (Backend)

## Your Mission

You're building the Posts system - the heart of NUMENEON's social feed. Users create posts (thoughts, media, milestones), like them, share them, and reply to create threads.

## Files You Own

**Important:** Don't touch anyone else's files to avoid merge conflicts!

### Backend Files (7 total)

- `backend/posts/models.py` - Post and Like models
- `backend/posts/views.py` - Posts API endpoints (CRUD + like + share + replies)
- `backend/posts/serializers.py` - Post data validation and formatting
- `backend/posts/urls.py` - Posts API routes configuration
- `backend/posts/apps.py` - Django app configuration
- `backend/posts/__init__.py` - Package marker
- `backend/posts/admin.py` - Django admin interface for posts

---

## Task Breakdown

### ✅ Task 1: Create Post and Like Models

**Files:** `backend/posts/models.py`

**Post Model Fields:**

| Field           | Type               | Description                             |
| --------------- | ------------------ | --------------------------------------- |
| `author`        | ForeignKey(User)   | Post creator                            |
| `type`          | CharField(choices) | 'thoughts', 'media', or 'milestones'    |
| `content`       | TextField(500)     | Post text (required)                    |
| `media_url`     | URLField           | Optional URL to media (NOT ImageField!) |
| `parent`        | ForeignKey(self)   | For replies (null for top-level posts)  |
| `created_at`    | DateTimeField      | Auto-set on creation                    |
| `updated_at`    | DateTimeField      | Auto-set on save                        |
| `likes_count`   | IntegerField       | Cached like count (default=0)           |
| `comment_count` | IntegerField       | Cached comment count (default=0)        |
| `shares_count`  | IntegerField       | Cached share count (default=0)          |

**Post Model Hints:**

```python
POST_TYPES = [('thoughts', 'Thoughts'), ('media', 'Media'), ('milestones', 'Milestones')]

type = models.CharField(max_length=20, choices=POST_TYPES, default='thoughts')
media_url = models.URLField(blank=True, null=True)
parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
```

**Like Model:**

Tracks which users liked which posts. Use `unique_together` to prevent duplicate likes.

```python
class Like(models.Model):
    user = ForeignKey(User, related_name='likes')
    post = ForeignKey(Post, related_name='likes')
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')
```

---

### ✅ Task 2: Build Post Serializer

**Files:** `backend/posts/serializers.py`

**Key Requirements:**

- Nested author data (not just ID) - import UserSerializer from users app
- Include `is_liked` field (SerializerMethodField) - check if current user liked this post
- Include `reply_count` field (SerializerMethodField) - count of replies
- Accept `parent_id` for creating replies (PrimaryKeyRelatedField with source='parent')

**Expected Output Format:**

```json
{
  "id": 1,
  "author": {
    "id": 5,
    "username": "alice",
    "first_name": "Alice",
    "last_name": "Smith"
  },
  "type": "thoughts",
  "content": "Hello NUMENEON!",
  "media_url": null,
  "parent": null,
  "parent_id": null,
  "created_at": "2024-12-19T10:30:00Z",
  "updated_at": "2024-12-19T10:30:00Z",
  "likes_count": 42,
  "comment_count": 7,
  "shares_count": 3,
  "is_liked": false,
  "reply_count": 2
}
```

**Serializer Hints:**

```python
from users.serializers import UserSerializer

author = UserSerializer(read_only=True)
is_liked = serializers.SerializerMethodField()
reply_count = serializers.SerializerMethodField()
parent_id = serializers.PrimaryKeyRelatedField(
    queryset=Post.objects.all(), source='parent',
    write_only=True, required=False, allow_null=True
)

def get_is_liked(self, obj):
    user = self.context['request'].user
    if user.is_authenticated:
        return Like.objects.filter(user=user, post=obj).exists()
    return False

def get_reply_count(self, obj):
    return obj.replies.count()
```

---

### ✅ Task 3: Build Posts API Views (ViewSet)

**Files:** `backend/posts/views.py`

**Use ModelViewSet for automatic CRUD operations.**

**Standard Endpoints (automatic from ViewSet):**

| Method | Endpoint           | Action       | Description     |
| ------ | ------------------ | ------------ | --------------- |
| GET    | `/api/posts/`      | `list()`     | Get all posts   |
| POST   | `/api/posts/`      | `create()`   | Create new post |
| GET    | `/api/posts/{id}/` | `retrieve()` | Get single post |
| PUT    | `/api/posts/{id}/` | `update()`   | Update post     |
| DELETE | `/api/posts/{id}/` | `destroy()`  | Delete post     |

**Custom Actions (use @action decorator):**

| Method | Endpoint                   | Action      | Description           |
| ------ | -------------------------- | ----------- | --------------------- |
| GET    | `/api/posts/{id}/replies/` | `replies()` | Get replies to a post |
| POST   | `/api/posts/{id}/like/`    | `like()`    | Toggle like on post   |
| POST   | `/api/posts/{id}/share/`   | `share()`   | Increment share count |

**Key Implementation Details:**

- `get_queryset()`: For list action, return only top-level posts (`parent__isnull=True`). Support `?username=` filter.
- `perform_create()`: Auto-set `author=request.user`
- `like()`: Toggle - if Like exists, delete it (decrement count); if not, create it (increment count)
- `share()`: Simply increment `shares_count`

**View Hints:**

```python
@action(detail=True, methods=['get'])
def replies(self, request, pk=None):
    post = self.get_object()
    replies = Post.objects.filter(parent=post)
    serializer = self.get_serializer(replies, many=True)
    return Response(serializer.data)

@action(detail=True, methods=['post'])
def like(self, request, pk=None):
    post = self.get_object()
    user = request.user
    existing = Like.objects.filter(user=user, post=post).first()
    if existing:
        existing.delete()
        post.likes_count -= 1
    else:
        Like.objects.create(user=user, post=post)
        post.likes_count += 1
    post.save()
    return Response(self.get_serializer(post).data)
```

---

### ✅ Task 4: Configure Posts URL Routes

**Files:** `backend/posts/urls.py`

**Use DefaultRouter with ViewSet:**

```python
from rest_framework.routers import DefaultRouter
from .views import PostViewSet

router = DefaultRouter()
router.register(r'', PostViewSet, basename='post')

urlpatterns = router.urls
```

The router auto-generates all CRUD routes plus custom @action routes.

---

### ✅ Task 5: Django Admin Configuration

**Files:** `backend/posts/admin.py`

**Acceptance Criteria:**

- [ ] Post model registered
- [ ] Like model registered
- [ ] List display shows author, type, content preview, created_at
- [ ] Can filter by type and author

---

## Integration Points

**You provide:**

- Posts API endpoints at `/api/posts/`
- Like toggle functionality
- Share counting
- Reply threading

**You consume:**

- User model (Natalia) - author field references User
- JWT auth (simplejwt) - all endpoints require authentication

**Work with:**

- **Natalia:** Your Post.author references her User model

---

## Testing Checklist

- [ ] Can create a post (thoughts, media, milestones)
- [ ] Can retrieve all posts (GET /api/posts/)
- [ ] Can filter posts by username (?username=)
- [ ] Can retrieve single post
- [ ] Can update own post
- [ ] Can delete own post
- [ ] Cannot edit/delete other users' posts
- [ ] Can like a post (creates Like, increments likes_count)
- [ ] Can unlike a post (deletes Like, decrements likes_count)
- [ ] Can share a post (increments shares_count)
- [ ] Can create reply (post with parent_id)
- [ ] Can get replies for a post (GET /api/posts/{id}/replies/)
- [ ] is_liked field correctly shows current user's like status

---

## Fixture Data

After running migrations, load the demo data:

```bash
python manage.py loaddata posts_and_users.json
```

This includes 130+ posts with engagement data (likes, comments, shares).
