# Backend Setup & Updates

> **Last Updated:** January 24, 2026

---

## 🚀 Pull Latest Changes

```bash
git pull origin dev
```

---

## 📦 Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

**New packages added:**

- `gunicorn` - Production WSGI server
- `dj-database-url` - Database URL parsing
- `python-dotenv` - Environment variable loading

---

## 🗄️ Database

Using **PostgreSQL** via `DATABASE_URL` environment variable.

If you don't have it set, add to your `.env`:

```
DATABASE_URL=postgresql://user:password@host:port/dbname
```

Run migrations:

```bash
python manage.py migrate
```

---

## � Messages App (NEW)

The `messages_app` provides direct messaging between users.

### Setup After Pulling

```bash
cd backend
python manage.py migrate          # Creates messages_app tables
python manage.py seed_messages    # Seeds sample conversations
```

**Required users for seeding:** `pabloPistola`, `arthurb`, `nataliap`, `colinw`, `crystalr`, `titod`

### Messages API Endpoints

All endpoints require authentication (`Authorization: Bearer <token>`)

| Method | Endpoint                                     | Description                     |
| ------ | -------------------------------------------- | ------------------------------- |
| GET    | `/api/messages/`                             | List all your messages          |
| POST   | `/api/messages/`                             | Send a new message              |
| GET    | `/api/messages/conversations/`               | List all conversations          |
| GET    | `/api/messages/conversation/<user_id>/`      | Get messages with specific user |
| POST   | `/api/messages/conversation/<user_id>/read/` | Mark messages from user as read |

### Send Message (POST `/api/messages/`)

**Request Body:**

```json
{
  "receiver_id": 2,
  "content": "Hey, what's up?"
}
```

**Response:**

```json
{
  "id": 1,
  "sender": { "id": 1, "username": "pabloPistola" },
  "receiver": { "id": 2, "username": "arthurb" },
  "content": "Hey, what's up?",
  "is_read": false,
  "created_at": "2026-01-24T10:30:00Z"
}
```

### Reseed Messages

To clear and reseed:

```bash
python manage.py seed_messages --clear
```

---

## �👥 Friends API Endpoints

All endpoints require authentication (`Authorization: Bearer <token>`)

| Method | Endpoint                             | Description                   |
| ------ | ------------------------------------ | ----------------------------- |
| GET    | `/api/friends/`                      | List your friends             |
| GET    | `/api/friends/requests/`             | Get pending incoming requests |
| POST   | `/api/friends/request/<user_id>/`    | Send friend request           |
| POST   | `/api/friends/accept/<request_id>/`  | Accept friend request         |
| POST   | `/api/friends/decline/<request_id>/` | Decline friend request        |
| DELETE | `/api/friends/remove/<user_id>/`     | Remove a friend               |

### Example Responses

#### GET `/api/friends/`

```json
[
  { "id": 2, "username": "colinw", "last_name": "Wilson" },
  { "id": 3, "username": "crystalr", "last_name": "Rodriguez" }
]
```

#### GET `/api/friends/requests/`

```json
[
  {
    "id": 5,
    "from_user": {
      "id": 4,
      "username": "nataliap",
      "first_name": "Natalia",
      "last_name": "Perez"
    },
    "created_at": "2026-01-24T10:30:00Z"
  }
]
```

#### POST `/api/friends/request/4/`

```json
{ "message": "Friend request sent" }
```

#### POST `/api/friends/accept/5/`

```json
{
  "message": "Friend request accepted",
  "friend": {
    "id": 4,
    "username": "nataliap",
    "first_name": "Natalia",
    "last_name": "Perez"
  }
}
```

---

## 🚀 Deployment (Render)

A `build.sh` script is included for Render deployment:

```bash
#!/usr/bin/env bash
set -o errexit
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate
```

---

## 🔍 Useful Commands

**Check users in database:**

```bash
python manage.py shell -c "from django.contrib.auth.models import User; [print(f'{u.username} | {u.email}') for u in User.objects.all()]"
```

**Run dev server:**

```bash
python manage.py runserver
```

**Create superuser for admin:**

```bash
python manage.py createsuperuser
```

**Access admin panel:**

```
http://127.0.0.1:8000/admin/
```
