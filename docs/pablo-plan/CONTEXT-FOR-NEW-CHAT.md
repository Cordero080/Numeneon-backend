# Context for New Chat: Backend Shell Branch

## Your Mission

Create an `n-backend` branch (similar to `n-frontend`) that contains:
- **Backend Python files** with pseudocode TODO comments (team implements)
- **Complete documentation** explaining what to build
- **No frontend folder** (delete it)

---

## Files to Read First (In Order)

### 1. Project Overview
```
docs/copilot-task/00-START-HERE.md
docs/copilot-task/01-CONTEXT-AND-STRATEGY.md
```

### 2. Backend Instructions (CRITICAL)
```
docs/copilot-task/03-BACKEND-INSTRUCTIONS.md
```
This file contains:
- File list by owner (Natalia, Colin, Crystal)
- Detailed pseudocode templates for each file
- Database configuration (PostgreSQL)

### 3. Backend Documentation
```
docs/backend/api-endpoints.md    - All API routes with request/response examples
docs/backend/models-overview.md  - Database models and relationships
```

### 4. Team Plan Files
```
docs/team-plan/natalia.md  - Auth & Users tasks
docs/team-plan/colin.md    - Posts tasks  
docs/team-plan/tito.md     - Infrastructure (apiClient, settings)
docs/team-plan/crystal.md  - Friends tasks
```

### 5. Current Backend Implementation (Reference)
```
backend/users/models.py
backend/users/views.py
backend/users/serializers.py
backend/posts/models.py
backend/posts/views.py
backend/posts/serializers.py
backend/friends/models.py
backend/friends/views.py
backend/friends/serializers.py
backend/numeneon/settings.py
backend/numeneon/urls.py
```

---

## Key Backend Facts

### Database: PostgreSQL (not SQLite)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'numeneon',
        'USER': '',  # Uses macOS user by default
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### Package Manager: pipenv
- `Pipfile` and `Pipfile.lock` define dependencies
- Run: `pipenv install` then `pipenv shell`

### Auth: JWT via Simple JWT
- Login uses EMAIL (not username)
- Returns access + refresh tokens
- Frontend sends `Authorization: Bearer <token>`

### Recent Changes (Jan 2026)
1. **PostgreSQL migration** - Moved from SQLite to PostgreSQL
2. **Password validators relaxed** - Min 6 chars for dev
3. **CORS configured** - corsheaders middleware added

---

## What to Do

1. **Create branch** `n-backend` from main
2. **Delete** `frontend/` folder entirely
3. **Convert backend files to pseudocode**:
   - Keep imports and class/function signatures
   - Replace implementations with detailed TODO comments
   - Follow templates in `03-BACKEND-INSTRUCTIONS.md`

4. **Keep these complete** (infrastructure):
   - `backend/numeneon/settings.py` - Configuration
   - `backend/manage.py` - Django CLI
   - `backend/Pipfile` and `Pipfile.lock` - Dependencies

5. **Update docs** if any backend changes were made since the instructions were written

---

## File Ownership Summary

| Owner    | App     | Files Count |
|----------|---------|-------------|
| Natalia  | users   | 11 files    |
| Colin    | posts   | 7 files     |
| Crystal  | friends | 7 files     |
| Tito     | numeneon| settings.py (keep complete) |

---

## Command to Create Shell Branch

```bash
# From numeneon folder, on main branch
git checkout -b n-backend

# Delete frontend
rm -rf frontend/

# Then convert backend files to pseudocode...
```

---

## Pseudocode Style (Example)

```python
"""
TODO: Create the Profile model - extends Django's built-in User

Fields you need:
- user: OneToOne link to Django's User model
- avatar: URL field (optional)
- bio: Text field (optional)
- created_at: When profile was created

Integration points:
- Posts reference User as author
- Frontend ProfileCard displays avatar and bio

Hint: Use OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
"""

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    # Your code here
    pass
```

---

## Success Criteria

When done, `n-backend` branch should:
- ✅ Have no `frontend/` folder
- ✅ Have all backend Python files with pseudocode TODO comments
- ✅ Have complete `settings.py`, `manage.py`, `Pipfile`
- ✅ Have updated documentation reflecting current state
- ✅ Be extractable to a separate project via `git archive n-backend`
