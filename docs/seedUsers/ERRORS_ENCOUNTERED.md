# Seeding Errors Encountered

## Overview

When running `python manage.py loaddata posts_and_users.json`, we encountered multiple errors due to database state conflicts and signal race conditions.

---

## Error 1: Duplicate Friend Requests

```
psycopg2.errors.UniqueViolation: could not create unique index
"friends_friendrequest_from_user_id_to_user_id_789672c2_uniq"
DETAIL: Key (from_user_id, to_user_id)=(1, 1) is duplicated.
```

**Cause:** The database had existing friend request data where a user sent a request to themselves (user 1 → user 1). The migration was trying to add a `unique_together` constraint but couldn't because of this duplicate.

**Solution:** Truncate the `friends_friendrequest` table before running migrations.

---

## Error 2: Duplicate Friendships

```
psycopg2.errors.UniqueViolation: could not create unique index
"friends_friendship_user_id_friend_id_923d93b4_uniq"
DETAIL: Key (user_id, friend_id)=(1, 1) is duplicated.
```

**Cause:** Same issue - duplicate friendship data where a user was friends with themselves.

**Solution:** Truncate the `friends_friendship` table before running migrations.

---

## Error 3: Signal Creates Profiles Before Loaddata

```
django.db.utils.IntegrityError: duplicate key value violates unique constraint
"users_profile_user_id_key"
DETAIL: Key (user_id)=(10) already exists.
```

**Cause:** This was the tricky one!

1. `loaddata` loads Users first
2. The `post_save` signal in `users/signals.py` fires and creates a Profile for each User
3. `loaddata` then tries to load Profiles from the JSON
4. **CONFLICT** - Profiles already exist from the signal!

**The Race Condition:**

```
loaddata creates User → Signal fires → Profile created automatically
                                              ↓
loaddata tries to create Profile → DUPLICATE KEY ERROR!
```

**Solution:** Modified `signals.py` to use `get_or_create()` instead of `create()`:

```python
# OLD (causes error)
Profile.objects.create(user=instance)

# NEW (safe)
Profile.objects.get_or_create(user=instance)
```

---

## Error 4: Foreign Key Violations on Likes

```
psycopg2.errors.ForeignKeyViolation: insert or update on table "posts_like"
violates foreign key constraint "posts_like_post_id_127195b7_fk_posts_post_id"
DETAIL: Key (post_id)=(1) is not present in table "posts_post".
```

**Cause:** The Likes table had orphaned data pointing to posts that no longer existed after truncating tables.

**Solution:** Complete database reset - drop and recreate the database.

---

## Error 5: 404 on API Endpoints

```
Not Found: /api/friends/requests/
Not Found: /api/friends/
Not Found: /api/posts/
```

**Cause:** The URL routes in `numeneon/urls.py` were commented out:

```python
# path('api/posts/', include('posts.urls')),      # COMMENTED OUT!
# path('api/friends/', include('friends.urls')),  # COMMENTED OUT!
```

**Solution:** Uncomment the URL routes in `backend/numeneon/urls.py`.

---

## Error 6: Story Cards Not Showing

**Cause:** After seeding, there were 0 friendships in the database. The seed data (`posts_and_users.json`) only contained Users, Profiles, and Posts - no Friendships!

**Solution:** Manually create friendships via Django shell:

```python
from friends.models import Friendship
from django.contrib.auth.models import User

pablo = User.objects.get(username='pabloPistola')
friend = User.objects.get(username='colinw')

# Create bidirectional friendships
Friendship.objects.create(user=pablo, friend=friend)
Friendship.objects.create(user=friend, friend=pablo)
```
