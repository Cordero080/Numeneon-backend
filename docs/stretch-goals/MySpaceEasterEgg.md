# 🎸 MySpace Easter Egg - Throwback Mode

A nostalgic easter egg feature that pays homage to MySpace, adding fun retro social features to Huddl.

## Overview

When users click "Throwback Mode" in Quick Settings, they unlock MySpace-inspired features that add personality and nostalgia to their profile.

---

## 📋 Implementation Phases

### Phase 1: Basic Toggle (15 min) ✅ Button Added

**Status:** Button UI complete, needs logic

**Tasks:**

- [ ] Add `throwbackMode` state to ProfileCard component
- [ ] Toggle `throwback-active` class on profile container
- [ ] Store preference in localStorage
- [ ] Add subtle retro CSS effects when active (optional scanlines, CRT glow)

**Files to modify:**

- `ProfileCard.jsx` - Add state and toggle logic
- `ProfileCard.css` - Add `.throwback-active` styles

---

### Phase 2: Top 8 Friends (1-2 hours)

**The classic MySpace feature!**

**Tasks:**

- [ ] Create `Top8Friends` component
- [ ] Add friend selection modal (pick from friends list)
- [ ] Display 8 avatar grid on profile (only when throwback mode ON)
- [ ] Drag-and-drop reordering
- [ ] Backend: Add `top_friends` field to User model (JSON array of user IDs)

**New files:**

```
components/
  Top8Friends/
    Top8Friends.jsx
    Top8Friends.css
    FriendSelector.jsx
```

**Backend changes:**

```python
# users/models.py
top_friends = models.JSONField(default=list, blank=True)  # [user_id, user_id, ...]
```

---

### Phase 3: Profile Song (2-3 hours)

**Auto-playing music on your profile!**

**Tasks:**

- [ ] Create `ProfileSong` component with audio player
- [ ] Song picker modal (search/paste link)
- [ ] Integration options:
  - Spotify embed (easiest)
  - SoundCloud embed
  - YouTube audio (via embed)
  - Direct MP3 upload (requires storage)
- [ ] Autoplay toggle (respect user preference)
- [ ] Mini player UI on profile header
- [ ] Backend: Add `profile_song` field to User model

**New files:**

```
components/
  ProfileSong/
    ProfileSong.jsx
    ProfileSong.css
    SongPicker.jsx
```

**Backend changes:**

```python
# users/models.py
profile_song_url = models.URLField(blank=True, null=True)
profile_song_autoplay = models.BooleanField(default=False)
```

**UI Ideas:**

- Cassette tape animation
- Vinyl record spinning
- Retro boombox mini-player

---

### Phase 4: Retro Themes (1-2 hours)

**"Pimp My Profile" - unlock crazy CSS themes**

**Theme Ideas:**
| Theme | Effects |
|-------|---------|
| **Scene Kid 2006** | Neon colors, checkerboard patterns, emo bangs overlay |
| **Glitter Explosion** | Sparkle cursor, glitter GIF backgrounds |
| **Cosmic Space** | Star field background, planet avatars |
| **Grunge** | Torn paper edges, newspaper textures |
| **Y2K Cyber** | Matrix rain, chrome text, futuristic borders |

**Tasks:**

- [ ] Create theme selector modal
- [ ] CSS theme files for each style
- [ ] Cursor customization (`.cursor-sparkle`, `.cursor-crosshair`)
- [ ] Animated backgrounds
- [ ] Store theme preference in backend

**New files:**

```
styles/
  themes/
    throwback-scene.css
    throwback-glitter.css
    throwback-space.css
    throwback-grunge.css
    throwback-y2k.css
```

---

### Phase 5: "Tom" Mode (Fun Easter Egg) (30 min)

**Everyone becomes your friend!**

When activated:

- Display count shows "∞ Friends"
- Tom's avatar appears in your Top 8
- Toast notification: "Tom added you as a friend!"
- Confetti animation

---

## 🎨 Design Notes

### Throwback Mode Indicator

When active, show a subtle badge/indicator:

```jsx
{
  throwbackMode && (
    <div className="throwback-badge">
      <span>🎸</span> Throwback Mode
    </div>
  );
}
```

### CSS Class Structure

```css
/* Base throwback styles */
.profile-card.throwback-active {
  /* Subtle retro effects */
}

.profile-card.throwback-active.theme-scene {
  /* Scene kid theme */
}
.profile-card.throwback-active.theme-glitter {
  /* Glitter theme */
}
.profile-card.throwback-active.theme-space {
  /* Space theme */
}
```

---

## 📊 Effort Summary

| Phase                 | Time    | Priority  | Dependencies        |
| --------------------- | ------- | --------- | ------------------- |
| Phase 1: Toggle       | 15 min  | High      | None                |
| Phase 2: Top 8        | 1-2 hrs | Medium    | Friends list        |
| Phase 3: Profile Song | 2-3 hrs | Medium    | Audio embed service |
| Phase 4: Retro Themes | 1-2 hrs | Low       | Phase 1             |
| Phase 5: Tom Mode     | 30 min  | Low (fun) | None                |

**Total Estimate:** 5-8 hours for full feature

---

## 🚀 MVP Recommendation

Start with **Phase 1 + Phase 4** (toggle + themes) for quick wins:

- 1-2 hours total
- High visual impact
- No backend changes needed
- Fun and shareable

Then add Top 8 and Profile Song later as polished features.

---

## 💡 Future Ideas

- **Bulletin Board** - Post announcements to all friends
- **Profile Views Counter** - "X people viewed your profile today!"
- **Mood Status** - Set your current mood with emoji
- **Kudos/Props** - Send virtual stickers to friends
- **Custom CSS Editor** - Let users write their own profile CSS (sandbox mode)

---

_Created: November 26, 2025_
_Status: Stretch Goal_
_Owner: TBD_
