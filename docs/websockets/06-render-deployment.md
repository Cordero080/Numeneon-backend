# Step 6: Render Deployment

> **Time:** ~20 minutes  
> **Complexity:** Medium

---

## Overview

Deploying Django Channels to Render requires:

1. A Redis instance (for channel layer)
2. Switching from Gunicorn to Daphne
3. Updating environment variables

---

## Step 6.1: Set Up Redis

### Option A: Render Redis (Recommended for Production)

1. Go to your Render dashboard
2. Click "New +" → "Redis"
3. Choose a name (e.g., `numeneon-redis`)
4. Select the free tier or paid tier based on needs
5. Click "Create Redis"
6. Copy the **Internal Redis URL** (looks like `redis://red-xxxxx:6379`)

### Option B: Upstash Redis (Free Tier, Good for Testing)

1. Go to [upstash.com](https://upstash.com)
2. Create a free account
3. Create a new Redis database
4. Copy the Redis URL (looks like `rediss://default:xxx@xxx.upstash.io:6379`)

---

## Step 6.2: Update build.sh

**File:** `/Numeneon-backend/build.sh`

Add daphne to the build process:

```bash
#!/usr/bin/env bash
# exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

cd backend
python manage.py collectstatic --no-input
python manage.py migrate
```

(This should already work - just make sure `daphne` is in `requirements.txt`)

---

## Step 6.3: Update Render Start Command

In your Render Web Service settings:

**Current (Gunicorn):**

```bash
gunicorn backend.numeneon.wsgi:application
```

**New (Daphne):**

```bash
cd backend && daphne -b 0.0.0.0 -p $PORT numeneon.asgi:application
```

### Breaking it down:

- `cd backend` - Navigate to the backend folder
- `daphne` - ASGI server (replaces gunicorn)
- `-b 0.0.0.0` - Bind to all interfaces
- `-p $PORT` - Use Render's assigned port
- `numeneon.asgi:application` - Path to ASGI application

---

## Step 6.4: Add Environment Variables

In Render dashboard → Your Service → Environment:

| Key            | Value                                         |
| -------------- | --------------------------------------------- |
| `REDIS_URL`    | `redis://red-xxxxx:6379` (from Step 6.1)      |
| `DATABASE_URL` | (already set)                                 |
| `SECRET_KEY`   | (already set - consider generating a new one) |
| `DJANGO_DEBUG` | `False`                                       |

---

## Step 6.5: Update ALLOWED_HOSTS

**File:** `backend/numeneon/settings.py`

Make sure your Render domain is in `ALLOWED_HOSTS`:

```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'numeneon-backend.onrender.com',
    '.onrender.com',  # Allow all Render subdomains
]
```

This is already correct in your settings! ✅

---

## Step 6.6: Update CORS for WebSocket Origin

WebSocket connections send an `Origin` header. While CORS doesn't apply to WebSockets, our `AllowedHostsOriginValidator` checks the origin against `ALLOWED_HOSTS`.

Add your frontend domain:

```python
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    'numeneon-backend.onrender.com',
    '.onrender.com',
    # Frontend origins (for WebSocket validation)
    'numeneon-frontend.vercel.app',
]
```

---

## Step 6.7: Production WebSocket URL

Update your frontend to use the correct WebSocket URL:

**Development:**

```javascript
ws://localhost:8000/ws/notifications/?token=${token}
```

**Production (Render):**

```javascript
wss://numeneon-backend.onrender.com/ws/notifications/?token=${token}
```

Note: `wss://` (secure) instead of `ws://` because Render uses HTTPS.

---

## Step 6.8: Create a render.yaml (Optional)

For Infrastructure as Code, create `render.yaml` in your repo root:

```yaml
services:
  - type: web
    name: numeneon-backend
    runtime: python
    buildCommand: ./build.sh
    startCommand: cd backend && daphne -b 0.0.0.0 -p $PORT numeneon.asgi:application
    envVars:
      - key: DATABASE_URL
        fromDatabase:
          name: numeneon-db
          property: connectionString
      - key: REDIS_URL
        fromService:
          type: redis
          name: numeneon-redis
          property: connectionString
      - key: SECRET_KEY
        generateValue: true

databases:
  - name: numeneon-db
    plan: free

redis:
  - name: numeneon-redis
    plan: free
```

---

## Deployment Checklist

Before deploying:

1. **requirements.txt** has:

   ```
   channels==4.0.0
   daphne==4.1.0
   channels-redis==4.2.0
   ```

2. **REDIS_URL** environment variable is set

3. **Start command** is updated to use Daphne:

   ```
   cd backend && daphne -b 0.0.0.0 -p $PORT numeneon.asgi:application
   ```

4. **ALLOWED_HOSTS** includes your domains

5. **Test locally** first with:
   ```bash
   REDIS_URL=redis://localhost:6379 python manage.py runserver
   ```
   (Only if you have Redis running locally)

---

## Troubleshooting Production Issues

### WebSocket returns 403

Check:

1. Origin header matches `ALLOWED_HOSTS`
2. Token is valid
3. CORS isn't blocking (it shouldn't for WebSockets)

### WebSocket connection times out

Check:

1. Daphne is running (check Render logs)
2. URL uses `wss://` not `ws://`
3. Port is not in URL (Render handles routing)

### "Connection refused" error

Check:

1. Render service is deployed and running
2. URL is correct (`wss://your-app.onrender.com/ws/notifications/`)
3. No trailing issues with the path

### Redis connection errors

Check:

1. `REDIS_URL` is set correctly
2. Redis instance is running
3. URL format is correct (`redis://` or `rediss://` for TLS)

---

## Cost Considerations

| Component          | Free Tier | Notes                            |
| ------------------ | --------- | -------------------------------- |
| Render Web Service | Yes       | Limited hours/month on free tier |
| Render Redis       | No        | $10/month minimum                |
| Upstash Redis      | Yes       | 10,000 commands/day free         |
| Redis Cloud        | Yes       | 30MB free                        |

**Recommendation:** Use Upstash free tier for development/testing, upgrade to Render Redis for production.

---

## ✅ Checklist

- [ ] Set up Redis (Render Redis, Upstash, or Redis Cloud)
- [ ] Added `REDIS_URL` environment variable in Render
- [ ] Updated start command to use Daphne
- [ ] Updated `ALLOWED_HOSTS` with all domains
- [ ] Updated frontend to use `wss://` in production
- [ ] Deployed and tested

---

**Next Step:** [07-frontend-integration.md](./07-frontend-integration.md)
