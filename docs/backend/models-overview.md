# Numeneon Backend Models Overview

> **Last Updated:** January 24, 2026  
> **Total Models:** 7 (6 custom + 1 Django built-in)
> **Database:** PostgreSQL (migrated from SQLite Jan 6, 2026)

---

## Model Inventory

| #   | Model             | App             | Owner   | Purpose                                    |
| --- | ----------------- | --------------- | ------- | ------------------------------------------ |
| 1   | **User**          | Django built-in | -       | Username, email, password, auth            |
| 2   | **Profile**       | users           | Natalia | Extended user data (bio, avatar, location) |
| 3   | **Post**          | posts           | Colin   | User posts with content, type, engagement  |
| 4   | **Like**          | posts           | Colin   | Tracks user-post like relationships        |
| 5   | **Friendship**    | friends         | Crystal | Bidirectional friend connections           |
| 6   | **FriendRequest** | friends         | Crystal | Pending friend requests                    |
| 7   | **Message**       | messages_app    | Pablo   | Direct messages between users              |

---

## 1. User (Django Built-in)

**Location:** `django.contrib.auth.models.User`

| Field         | Type           | Description           |
| ------------- | -------------- | --------------------- |
| `id`          | AutoField      | Primary key           |
| `username`    | CharField(150) | Unique username       |
| `email`       | EmailField     | User email            |
| `password`    | CharField      | Hashed password       |
| `first_name`  | CharField(150) | First name (optional) |
| `last_name`   | CharField(150) | Last name (optional)  |
| `is_active`   | BooleanField   | Account active status |
| `date_joined` | DateTimeField  | Account creation date |

**Relationships:**

- Has ONE `Profile` (via Profile.user)
- Has MANY `Post` (via Post.author)
- Has MANY `Like` (via Like.user)
- Has MANY `Friendship` (via Friendship.user)
- Has MANY `FriendRequest` (sent/received)
- Has MANY `Message` (sent via sent_messages, received via received_messages)

---

## 2. Profile

**Location:** `backend/users/models.py`  
**Owner:** Natalia (Auth & Users Lead)

| Field        | Type                | Constraints                | Description                |
| ------------ | ------------------- | -------------------------- | -------------------------- |
| `id`         | AutoField           | PK                         | Primary key                |
| `user`       | OneToOneField(User) | CASCADE                    | Link to Django User        |
| `bio`        | TextField           | max_length=500, blank=True | User bio                   |
| `avatar`     | URLField            | max_length=500, blank=True | Profile image URL          |
| `location`   | CharField           | max_length=100, blank=True | User location              |
| `website`    | URLField            | max_length=200, blank=True | Personal website           |
| `created_at` | DateTimeField       | auto_now_add               | Profile creation timestamp |
| `updated_at` | DateTimeField       | auto_now                   | Last update timestamp      |

**Relationships:**

```
User ──1:1── Profile
```

**Access Pattern:**

```python
user.profile        # Get profile from user
profile.user        # Get user from profile
```

---

## 3. Post

**Location:** `backend/posts/models.py`  
**Owner:** Colin (Posts Backend Lead)

| Field           | Type             | Constraints                                | Description             |
| --------------- | ---------------- | ------------------------------------------ | ----------------------- |
| `id`            | AutoField        | PK                                         | Primary key             |
| `author`        | ForeignKey(User) | CASCADE, related_name='posts'              | Post creator            |
| `content`       | TextField        | max_length=500, blank=False                | Post text (required)    |
| `type`          | CharField        | max_length=20, choices, default='thoughts' | Post category           |
| `media_url`     | URLField         | max_length=500, blank=True, null=True      | Optional media          |
| `parent`        | ForeignKey(self) | CASCADE, null=True, related_name='replies' | For threaded replies    |
| `created_at`    | DateTimeField    | auto_now_add                               | Post creation timestamp |
| `updated_at`    | DateTimeField    | auto_now                                   | Last update timestamp   |
| `likes_count`   | IntegerField     | default=0                                  | Cached like count       |
| `comment_count` | IntegerField     | default=0                                  | Cached comment count    |
| `shares_count`  | IntegerField     | default=0                                  | Cached share count      |

**Post Types (choices):**

```python
POST_TYPES = [
    ('thoughts', 'Thoughts'),    # Text-only posts
    ('media', 'Media'),          # Posts with images/videos
    ('milestones', 'Milestones'), # Achievement posts
]
```

**Relationships:**

```
User ──1:*── Post (author)
Post ──1:*── Post (parent → replies)
Post ──1:*── Like
```

**Access Patterns:**

```python
user.posts.all()      # All posts by user
post.replies.all()    # All replies to post
post.likes.all()      # All likes on post
post.author           # User who created post
post.parent           # Parent post (if reply)
```

**Meta:**

- Ordering: `-created_at` (newest first)

---

## 4. Like

**Location:** `backend/posts/models.py`  
**Owner:** Colin (Posts Backend Lead)

| Field        | Type             | Constraints                   | Description         |
| ------------ | ---------------- | ----------------------------- | ------------------- |
| `id`         | AutoField        | PK                            | Primary key         |
| `user`       | ForeignKey(User) | CASCADE, related_name='likes' | User who liked      |
| `post`       | ForeignKey(Post) | CASCADE, related_name='likes' | Post that was liked |
| `created_at` | DateTimeField    | auto_now_add                  | Like timestamp      |

**Constraints:**

```python
class Meta:
    unique_together = ('user', 'post')  # One like per user per post
```

**Relationships:**

```
User ──1:*── Like
Post ──1:*── Like
```

**Access Patterns:**

```python
user.likes.all()      # All likes by user
post.likes.all()      # All likes on post
post.likes.count()    # Count of likes
```

---

## 5. Friendship

**Location:** `backend/friends/models.py`  
**Owner:** Crystal (Friends System Lead)

| Field        | Type             | Constraints                         | Description           |
| ------------ | ---------------- | ----------------------------------- | --------------------- |
| `id`         | AutoField        | PK                                  | Primary key           |
| `user`       | ForeignKey(User) | CASCADE, related_name='friendships' | The user              |
| `friend`     | ForeignKey(User) | CASCADE, related_name='friends'     | Their friend          |
| `created_at` | DateTimeField    | auto_now_add                        | Friendship start date |

**Constraints:**

```python
class Meta:
    unique_together = ['user', 'friend']  # No duplicate friendships
    ordering = ['-created_at']            # Newest first
```

**Relationships:**

```
User ──*:*── User (via Friendship as junction table)
```

**Access Patterns:**

```python
user.friendships.all()  # Friendships where user is the main person
user.friends.all()      # Friendships where user is the friend
```

**Note:** Friendships are typically bidirectional—when A befriends B, create TWO rows:

1. `Friendship(user=A, friend=B)`
2. `Friendship(user=B, friend=A)`

---

## 6. FriendRequest

**Location:** `backend/friends/models.py`  
**Owner:** Crystal (Friends System Lead)

| Field        | Type             | Constraints                               | Description       |
| ------------ | ---------------- | ----------------------------------------- | ----------------- |
| `id`         | AutoField        | PK                                        | Primary key       |
| `from_user`  | ForeignKey(User) | CASCADE, related_name='sent_requests'     | Request sender    |
| `to_user`    | ForeignKey(User) | CASCADE, related_name='received_requests' | Request recipient |
| `created_at` | DateTimeField    | auto_now_add                              | Request timestamp |

**Constraints:**

```python
class Meta:
    unique_together = ['from_user', 'to_user']  # One request per pair
    ordering = ['-created_at']                   # Newest first
```

**Relationships:**

```
User (from_user) ──1:*── FriendRequest
User (to_user) ──1:*── FriendRequest
```

**Access Patterns:**

```python
user.sent_requests.all()      # Requests this user sent
user.received_requests.all()  # Requests sent TO this user
```

**Lifecycle:**

1. User A sends request → `FriendRequest(from_user=A, to_user=B)` created
2. User B accepts → FriendRequest deleted, TWO Friendships created
3. User B declines → FriendRequest deleted, no Friendships created

---

## Relationship Diagram (Text)

```
                    ┌──────────────────────────────────────┐
                    │              USER                     │
                    │  (Django auth.User)                   │
                    │                                       │
                    │  id, username, email, password        │
                    │  first_name, last_name, date_joined   │
                    └───────────────┬──────────────────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          │                         │                         │
          ▼ 1:1                     ▼ 1:*                     ▼ 1:*
    ┌───────────┐            ┌───────────┐            ┌─────────────────┐
    │  PROFILE  │            │   POST    │            │   FRIENDSHIP    │
    │           │            │           │            │                 │
    │  bio      │            │  content  │            │  user (FK)      │
    │  avatar   │            │  type     │            │  friend (FK)    │
    │  location │            │  media    │            │  created_at     │
    │  website  │            │  parent   │◄──┐        └─────────────────┘
    └───────────┘            │  likes_ct │   │
                             │  comment  │   │               │
                             │  shares   │   │               │
                             └─────┬─────┘   │               ▼ related
                                   │         │        ┌─────────────────┐
                                   │ 1:*     │ self   │  FRIENDREQUEST  │
                                   │         │ FK     │                 │
                                   ▼         │        │  from_user (FK) │
                             ┌───────────┐   │        │  to_user (FK)   │
                             │   LIKE    │───┘        │  created_at     │
                             │           │            └─────────────────┘
                             │  user(FK) │
                             │  post(FK) │
                             │  created  │
                             └───────────┘
```

---

## 7. Message

**Location:** `backend/messages_app/models.py`  
**Owner:** Pablo

| Field        | Type             | Constraints   | Description               |
| ------------ | ---------------- | ------------- | ------------------------- |
| `id`         | AutoField        | PK            | Primary key               |
| `sender`     | ForeignKey(User) | CASCADE       | User who sent the message |
| `receiver`   | ForeignKey(User) | CASCADE       | User who receives message |
| `content`    | TextField        | -             | Message text content      |
| `is_read`    | BooleanField     | default=False | Whether message was read  |
| `created_at` | DateTimeField    | auto_now_add  | Message sent timestamp    |

**Relationships:**

```
User ──1:*── Message (as sender, via sent_messages)
User ──1:*── Message (as receiver, via received_messages)
```

**Access Pattern:**

```python
user.sent_messages.all()      # Messages user sent
user.received_messages.all()  # Messages user received
message.sender                # Get sender user
message.receiver              # Get receiver user
```

**Seed Command:**

```bash
python manage.py seed_messages         # Add sample messages
python manage.py seed_messages --clear  # Clear and reseed
```

---

## Database Statistics

| Table         | Est. Rows (Dev) | Growth Pattern                |
| ------------- | --------------- | ----------------------------- |
| User          | ~10             | Manual seed                   |
| Profile       | ~10             | 1:1 with User                 |
| Post          | ~50-100         | Grows with user activity      |
| Like          | ~100-200        | Grows with engagement         |
| Friendship    | ~20-40          | Grows with connections        |
| FriendRequest | ~5-10           | Transient (accepted/declined) |
| Message       | ~20-50          | Grows with user messaging     |
