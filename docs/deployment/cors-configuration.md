# CORS Configuration

> **Last Updated:** January 24, 2026

---

## What Changed

Updated `backend/numeneon/settings.py` to configure CORS for production deployment.

### Before (Development Only)

```python
CORS_ALLOW_ALL_ORIGINS = True  # For development only
```

### After (Production Ready)

```python
CORS_ALLOWED_ORIGINS = [
    'https://numeneon-frontend.vercel.app',
    'http://localhost:5173',  # Vite dev server
    'http://localhost:3000',  # React dev server
]
CORS_ALLOW_CREDENTIALS = True
```

---

## Why This Change

### Problem

- `CORS_ALLOW_ALL_ORIGINS = True` allows **any** website to make requests to our API
- This is a security risk in production (other sites could make authenticated requests)

### Solution

- `CORS_ALLOWED_ORIGINS` explicitly whitelists only trusted domains
- `CORS_ALLOW_CREDENTIALS = True` allows cookies and Authorization headers to be sent cross-origin (required for JWT auth)

---

## Allowed Origins

| Origin | Purpose |
| ------ | ------- |
| `https://numeneon-frontend.vercel.app` | Production frontend on Vercel |
| `http://localhost:5173` | Local Vite dev server |
| `http://localhost:3000` | Local React dev server (CRA) |

---

## How CORS Works

```
┌─────────────────────┐         ┌─────────────────────┐
│   Vercel Frontend   │         │   Render Backend    │
│  (React App)        │         │   (Django API)      │
│                     │         │                     │
│  Origin:            │  HTTP   │  Checks:            │
│  numeneon-frontend  │ ──────► │  Is origin in       │
│  .vercel.app        │         │  CORS_ALLOWED_      │
│                     │ ◄────── │  ORIGINS?           │
│                     │  ✅ Yes │                     │
└─────────────────────┘         └─────────────────────┘
```

1. Browser sends request with `Origin` header
2. Django checks if origin is in `CORS_ALLOWED_ORIGINS`
3. If yes, responds with `Access-Control-Allow-Origin` header
4. Browser allows the response to be read by frontend

---

## Adding New Origins

If you deploy to a new domain, add it to the list:

```python
CORS_ALLOWED_ORIGINS = [
    'https://numeneon-frontend.vercel.app',
    'https://your-new-domain.com',  # Add new domain here
    'http://localhost:5173',
    'http://localhost:3000',
]
```

---

## Related Settings

These were already configured in the project:

```python
# In INSTALLED_APPS
'corsheaders',

# In MIDDLEWARE (must be first!)
'corsheaders.middleware.CorsMiddleware',
```

---

## Troubleshooting

### "CORS policy: No 'Access-Control-Allow-Origin' header"

- Check that the frontend URL is exactly in `CORS_ALLOWED_ORIGINS`
- Trailing slashes matter: `https://example.com` ≠ `https://example.com/`

### "CORS policy: credentials flag is true, but..."

- Ensure `CORS_ALLOW_CREDENTIALS = True` is set
- Frontend must include `credentials: 'include'` in fetch/axios

### Requests work locally but not in production

- Make sure the Vercel URL is in `CORS_ALLOWED_ORIGINS`
- Redeploy backend after changing settings
