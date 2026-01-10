# Stretch Goals for Posts (Social Media)

## ✅ Completed Features

These features have been implemented:

- ✅ **Like/unlike a post** - `POST /api/posts/:id/like/` toggles like, Like model tracks user likes
- ✅ **Reply to a post** - Threaded replies with `parent` field, nested display in Timeline River
- ✅ **See posts by a specific user** - Profile page TimelineRiver shows user's posts by type
- ✅ **Share count tracking** - `shares_count` field on Post model (UI placeholder ready)

---

## 🔄 In Progress / Partially Complete

- 🔄 **Share a post** - Backend endpoint exists (`POST /api/posts/:id/share/`), frontend icon is placeholder
- 🔄 **Bookmark a post** - Frontend icon exists as placeholder, no backend yet

---

## 📋 Future Enhancements

### Post Interactions

- [ ] **Repost/Quote post** - Create new post that references original
- [ ] **Bookmark system** - Save posts for later, personal bookmark list
- [ ] **Report post** - Flag inappropriate content

### Post Discovery

- [ ] **Trending posts** - Algorithm based on recent engagement velocity
- [ ] **Search posts** - Full-text search by content
- [ ] **Hashtag system** - Parse hashtags, create tag pages

### Media Enhancements

- [ ] **Video posts** - Support video upload/embed
- [ ] **Image galleries** - Multiple images per post
- [ ] **GIF picker** - Integration with Giphy/Tenor

### Engagement Analytics

- [ ] **Post insights** - View count, engagement rate per post
- [ ] **Virality score** - How fast post gained traction
- [ ] **Best time to post** - Analyze when user's posts perform best

---

## Backend Reference

**Existing endpoints:**

```
GET    /api/posts/              - List all posts (with filters)
POST   /api/posts/              - Create post
GET    /api/posts/:id/          - Get single post
PATCH  /api/posts/:id/          - Update post
DELETE /api/posts/:id/          - Delete post
GET    /api/posts/:id/replies/  - Get replies to a post
POST   /api/posts/:id/like/     - Toggle like on post
POST   /api/posts/:id/share/    - Increment share count
```

**Models:**

- `Post` - Core post model with type, content, media_url, parent (for replies)
- `Like` - Tracks which user liked which post (prevents double-likes)
