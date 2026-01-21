# Database Seeding Steps (Updated)

## Prerequisites

- PostgreSQL running
- `numeneon` database exists
- You're in the `backend/` directory
- Virtual environment activated (`pipenv shell`)

---

## Fresh Seed (Recommended)

Use this when you want a completely clean slate:

```bash
# 1. Drop and recreate the database
psql -c "DROP DATABASE numeneon;"
psql -c "CREATE DATABASE numeneon;"

# 2. Run migrations
python manage.py migrate

# 3. Load seed data (without profiles - signal handles them)
cat posts_and_users.json | python -c "
import json,sys
d=json.load(sys.stdin)
d=[x for x in d if x['model']!='users.profile']
print(json.dumps(d,indent=2))
" > posts_and_users_noprofiles.json

python manage.py loaddata posts_and_users_noprofiles.json

# 4. Update profiles with bio data from original seed
python manage.py shell -c "
import json
from users.models import Profile

with open('posts_and_users.json') as f:
    data = json.load(f)

for p in [x for x in data if x['model'] == 'users.profile']:
    try:
        profile = Profile.objects.get(user_id=p['fields']['user'])
        profile.bio = p['fields'].get('bio', '')
        profile.avatar = p['fields'].get('avatar', '')
        profile.location = p['fields'].get('location', '')
        profile.website = p['fields'].get('website', '')
        profile.save()
        print(f'Updated {profile.user.username}')
    except Profile.DoesNotExist:
        pass
"

# 5. Create friendships (seed data doesn't include these!)
python manage.py shell -c "
from friends.models import Friendship
from django.contrib.auth.models import User

pablo = User.objects.get(username='pabloPistola')
friends_to_add = ['colinw', 'crystalr', 'nataliap', 'titod', 'arthurb']

for username in friends_to_add:
    friend = User.objects.get(username=username)
    Friendship.objects.get_or_create(user=pablo, friend=friend)
    Friendship.objects.get_or_create(user=friend, friend=pablo)
    print(f'Added: {pablo.username} <-> {friend.username}')
"

# 6. Verify
python manage.py shell -c "
from django.contrib.auth.models import User
from posts.models import Post
from friends.models import Friendship
print(f'Users: {User.objects.count()}')
print(f'Posts: {Post.objects.count()}')
print(f'Friendships: {Friendship.objects.count()}')
"
```

---

## Quick Seed (One Command)

If you've already set up the filtered JSON file:

```bash
psql -c "DROP DATABASE numeneon;" && \
psql -c "CREATE DATABASE numeneon;" && \
python manage.py migrate && \
python manage.py loaddata posts_and_users_noprofiles.json
```

---

## What Gets Seeded

| Model       | Count | Notes                              |
| ----------- | ----- | ---------------------------------- |
| Users       | 12    | All have password `test123`        |
| Profiles    | 12    | Auto-created by signal             |
| Posts       | 149   | Mix of thoughts, media, milestones |
| Likes       | 14    | Pre-existing likes                 |
| Friendships | 0\*   | **Must create manually!**          |

\*The seed data does NOT include friendships. Create them manually or they won't show in the frontend.

---

## Important: The Signal Fix

The `users/signals.py` file MUST use `get_or_create()`:

```python
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Use get_or_create to avoid duplicates when loading fixtures
        Profile.objects.get_or_create(user=instance)
```

If it uses `Profile.objects.create(user=instance)`, loaddata will fail with duplicate key errors.

---

## Troubleshooting

### "Database numeneon does not exist"

```bash
psql -c "CREATE DATABASE numeneon;"
```

### "Duplicate key" errors

```bash
# Nuclear option - drop and recreate
psql -c "DROP DATABASE numeneon;"
psql -c "CREATE DATABASE numeneon;"
python manage.py migrate
```

### "No posts showing" after seed

Check that URLs are uncommented in `backend/numeneon/urls.py`:

```python
path('api/posts/', include('posts.urls')),      # Must be uncommented!
path('api/friends/', include('friends.urls')),  # Must be uncommented!
```

### "No story cards showing"

Friendships don't exist. Run the friendship creation script from step 5 above.
