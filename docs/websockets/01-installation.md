# Step 1: Installation

> **Time:** ~5 minutes

---

## What You're Installing

| Package          | Purpose                                             |
| ---------------- | --------------------------------------------------- |
| `channels`       | Django extension for WebSockets & async             |
| `daphne`         | ASGI server (like gunicorn but supports WebSockets) |
| `channels-redis` | Redis backend for channel layer (production)        |

---

## Step 1.1: Install Packages

In your terminal, navigate to your project root and run:

```bash
cd /Users/pablodcordero/code/ga/unit-4/Numeneon-backend
pip install channels daphne channels-redis
```

---

## Step 1.2: Update requirements.txt

Add these lines to your `requirements.txt`:

```
# WebSocket support
channels==4.0.0
daphne==4.1.0
channels-redis==4.2.0
```

Your `requirements.txt` should now look like:

```
asgiref==3.11.0
Django==5.2.10
django-cors-headers==4.9.0
djangorestframework==3.16.1
djangorestframework_simplejwt==5.5.1
psycopg2-binary==2.9.11
PyJWT==2.10.1
sqlparse==0.5.5
gunicorn
dj-database-url
python-dotenv
whitenoise

# WebSocket support
channels==4.0.0
daphne==4.1.0
channels-redis==4.2.0
```

---

## Step 1.3: Verify Installation

Run this to verify channels is installed:

```bash
python -c "import channels; print(f'Channels version: {channels.__version__}')"
```

Expected output:

```
Channels version: 4.0.0
```

---

## What Each Package Does

### `channels`

- Extends Django to handle WebSocket connections
- Provides "consumers" (like views for WebSockets)
- Manages channel layers (communication between processes)

### `daphne`

- ASGI server that can handle both HTTP and WebSocket
- Replaces gunicorn for WebSocket support
- Developed by the Django Channels team

### `channels-redis`

- Uses Redis as a message broker between server instances
- Required for production (multiple workers need to communicate)
- Not needed for local development (we use in-memory layer)

---

## 💡 Note on Redis

For **local development**, we'll use `InMemoryChannelLayer` - no Redis needed!

For **production** (Render), you'll need a Redis instance. Options:

- Render Redis (paid add-on)
- Redis Cloud free tier
- Upstash Redis (serverless, free tier available)

We'll cover this in the deployment guide.

---

## ✅ Checklist

- [ ] Ran `pip install channels daphne channels-redis`
- [ ] Added packages to `requirements.txt`
- [ ] Verified installation with test command

---

**Next Step:** [02-settings-config.md](./02-settings-config.md)
