# Crystal's Tasks - Friends System (Backend)

## Your Mission

You're building the Friends system - connections between users. You handle friend requests, approvals, and the social graph that makes NUMENEON a network.

## Files You Own

**Important:** Don't touch anyone else's files to avoid merge conflicts!

### Backend Files (7 total)

- `backend/friends/models.py` - Friendship & FriendRequest models
- `backend/friends/views.py` - Friends API endpoints
- `backend/friends/serializers.py` - Friend data validation and formatting
- `backend/friends/urls.py` - Friends API routes configuration
- `backend/friends/apps.py` - Django app configuration
- `backend/friends/__init__.py` - Package marker
- `backend/friends/admin.py` - Django admin interface for friendships

---

## ⚠️ CRITICAL: Model Design (Directional Friendships)

**Your models use a DIRECTIONAL approach, NOT a status-based one!**

### Friendship Model (Two records per friendship)

```python
class Friendship(models.Model):
    user = ForeignKey(User, related_name='friendships')   # Owner of this entry
    friend = ForeignKey(User, related_name='friends_of')  # The friend
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'friend']
```

**When Alice and Bob become friends, create TWO records:**

- `Friendship(user=alice, friend=bob)`
- `Friendship(user=bob, friend=alice)`

### FriendRequest Model (NO status field!)

```python
class FriendRequest(models.Model):
    from_user = ForeignKey(User, related_name='sent_requests')
    to_user = ForeignKey(User, related_name='received_requests')
    created_at = DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['from_user', 'to_user']
```

**When request is accepted:**

1. Create TWO Friendship records (both directions)
2. DELETE the FriendRequest (don't update status - just delete it!)

**When request is declined:**

1. DELETE the FriendRequest

---

## Task Breakdown

### ✅ Task 1: Create Friendship Models

**Files:** `backend/friends/models.py`

**Acceptance Criteria:**

- [ ] Friendship model with `user`, `friend`, `created_at` fields
- [ ] FriendRequest model with `from_user`, `to_user`, `created_at` fields
- [ ] NO status field on FriendRequest!
- [ ] `unique_together` constraints to prevent duplicates
- [ ] `__str__` methods for admin readability

**Model Hints from Shell:**

```python
# Friendship
user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships')
friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friends_of')
created_at = models.DateTimeField(auto_now_add=True)

# FriendRequest
from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
created_at = models.DateTimeField(auto_now_add=True)
```

---

### ✅ Task 2: Build Friendship Serializers

**Files:** `backend/friends/serializers.py`

**Acceptance Criteria:**

- [ ] FriendshipSerializer with nested user/friend data
- [ ] FriendRequestSerializer with nested from_user/to_user data
- [ ] Import UserSerializer from users app for nesting

**NOTE:** In views, you may build response dicts manually for simple endpoints like `friend_list`. These serializers are for more complex scenarios.

---

### ✅ Task 3: Build Friends API Views

**Files:** `backend/friends/views.py`

**Endpoints to create (function-based views):**

| Method | Endpoint                             | Function             | Description                 |
| ------ | ------------------------------------ | -------------------- | --------------------------- |
| GET    | `/api/friends/`                      | `friend_list()`      | List current user's friends |
| GET    | `/api/friends/requests/`             | `pending_requests()` | List incoming requests      |
| POST   | `/api/friends/request/<user_id>/`    | `send_request()`     | Send friend request         |
| POST   | `/api/friends/accept/<request_id>/`  | `accept_request()`   | Accept a request            |
| POST   | `/api/friends/decline/<request_id>/` | `decline_request()`  | Decline a request           |
| DELETE | `/api/friends/remove/<user_id>/`     | `remove_friend()`    | Remove a friend             |

**Expected Response for GET /api/friends/:**

```json
[
  { "id": 1, "username": "alice", "first_name": "Alice", "last_name": "Smith" },
  { "id": 2, "username": "bob", "first_name": "Bob", "last_name": "Jones" }
]
```

**Expected Response for GET /api/friends/requests/:**

```json
[
  {
    "id": 1,
    "from_user": {
      "id": 5,
      "username": "charlie",
      "first_name": "Charlie",
      "last_name": "Brown"
    },
    "created_at": "2024-12-19T10:30:00Z"
  }
]
```

**Key Implementation Details:**

- `friend_list`: Query `Friendship.objects.filter(user=request.user)` and return friend data
- `pending_requests`: Query `FriendRequest.objects.filter(to_user=request.user)`
- `send_request`: Validate (can't friend self, no existing request), create FriendRequest
- `accept_request`: Create TWO Friendships, DELETE the FriendRequest
- `decline_request`: Just DELETE the FriendRequest
- `remove_friend`: Delete BOTH Friendship records

---

### ✅ Task 4: Configure Friends URL Routes

**Files:** `backend/friends/urls.py`

**Routes to configure:**

```python
urlpatterns = [
    path('', views.friend_list, name='friend_list'),
    path('requests/', views.pending_requests, name='pending_requests'),
    path('request/<int:user_id>/', views.send_request, name='send_request'),
    path('accept/<int:request_id>/', views.accept_request, name='accept_request'),
    path('decline/<int:request_id>/', views.decline_request, name='decline_request'),
    path('remove/<int:user_id>/', views.remove_friend, name='remove_friend'),
]
```

---

### ✅ Task 5: Django Admin Configuration

**Files:** `backend/friends/admin.py`

**Acceptance Criteria:**

- [ ] Register Friendship and FriendRequest models
- [ ] List display shows relevant fields
- [ ] Can filter and search

---

## Integration Points

**You provide:**

- Friends API endpoints at `/api/friends/`
- Friendship data (list of friends for a user)
- Friend request management

**You consume:**

- User model (Natalia) - friendships link two users
- JWT auth (simplejwt) - all endpoints require authentication

**Work with:**

- **Natalia:** Your models reference her User model via ForeignKey

---

## Testing Checklist

- [ ] Can send friend request to another user
- [ ] Cannot send duplicate request to same user
- [ ] Cannot send request to yourself (should error)
- [ ] Pending requests appear in recipient's pending list
- [ ] Can accept friend request
- [ ] Accepted friendship creates TWO Friendship records
- [ ] FriendRequest is DELETED after acceptance (not updated)
- [ ] Can decline friend request (deletes request)
- [ ] Can remove friend (deletes BOTH Friendship records)
- [ ] Friend list shows correct data

---

## Fixture Data

After running migrations, load the demo data:

```bash
python manage.py loaddata posts_and_users.json
```

This includes pre-created friendships between demo users.
