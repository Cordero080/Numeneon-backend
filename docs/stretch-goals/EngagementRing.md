# Stretch Goals - Profile Engagement Ring

A dynamic progress ring around the profile avatar that visualizes user activity/engagement.

---

## Current State: Placeholder

**Location:** `ProfileCardFront.jsx` → `.avatar-engagement-ring`

**What exists now:**

- SVG ring with background track and progress arc
- CSS animation that fills to ~12.5% on page load
- Cyan/green glow effect
- No connection to real data

**Code reference:**

```jsx
// ProfileCardFront.jsx lines 78-101
<div className="avatar-engagement-ring">
  <svg width="130" height="130" viewBox="0 0 130 130">
    <circle className="ring-bg" ... />      {/* Background track */}
    <circle className="ring-progress" ... /> {/* Animated fill */}
  </svg>
</div>
```

---

## Future Implementation Options

### Option 1: Profile Completion %

**Easiest to implement**

Show how complete the user's profile is:

- Has avatar uploaded? (+20%)
- Has bio filled? (+20%)
- Has location? (+15%)
- Has cover photo? (+20%)
- Has at least 1 post? (+10%)
- Has at least 1 friend? (+15%)

**Backend needs:**

```python
# users/serializers.py
def get_profile_completion(self, obj):
    score = 0
    if obj.avatar: score += 20
    if obj.bio: score += 20
    if obj.location: score += 15
    if obj.cover_photo: score += 20
    if obj.posts.exists(): score += 10
    if obj.friends.exists(): score += 15
    return score
```

---

### Option 2: Weekly Activity Score

**Medium complexity**

Based on activity in the last 7 days:

- Posts created
- Likes given/received
- Comments made
- Profile views (if tracked)

**Backend needs:**

- Activity logging per action
- Time-windowed aggregation query
- Score calculation endpoint

---

### Option 3: XP / Level System (Gamification)

**Most complex**

Full gamification with levels:

- Level 1-100 system
- XP earned from all activity
- Ring shows progress to next level
- Level badge displayed on profile

**Backend needs:**

```python
# users/models.py
xp_total = models.PositiveIntegerField(default=0)
level = models.PositiveIntegerField(default=1)

def calculate_level(self):
    # XP required doubles each level
    # Level 1: 0-100 XP
    # Level 2: 100-300 XP
    # Level 3: 300-700 XP, etc.
    pass
```

---

### Option 4: Engagement Score

**Integrates with existing analytics**

Use data already shown in ActivityVisualization:

- Calculate from weekly engagement totals
- Ring fills based on user's engagement percentile
- Top 10% users = full ring
- Average users = 50% ring

**Frontend integration:**

```jsx
// ProfileCardFront.jsx
const engagementPercent = calculateEngagementPercentile(weeklyData);
const dashOffset = 377 - (377 * engagementPercent) / 100;
```

---

## Implementation Checklist

### Phase 1: Backend API

- [ ] Choose which metric to track
- [ ] Add fields to User model (if needed)
- [ ] Create calculation endpoint
- [ ] Add to UserSerializer response

### Phase 2: Frontend Integration

- [ ] Fetch engagement score from API
- [ ] Pass to ProfileCardFront as prop
- [ ] Calculate strokeDashoffset from percentage
- [ ] Update CSS animation to use dynamic value

### Phase 3: Polish

- [ ] Add color gradient based on level (green → gold)
- [ ] Add tooltip showing actual value
- [ ] Add loading state while fetching
- [ ] Consider pulsing animation at 100%

---

## Files to Modify

**Backend:**

- `backend/users/models.py` - Add tracking fields
- `backend/users/serializers.py` - Add calculation
- `backend/users/views.py` - Add endpoint if needed

**Frontend:**

- `ProfileCardFront.jsx` - Accept percentage prop, calculate dashoffset
- `ProfileCardFront.scss` - Dynamic animation support
- `Profile.jsx` - Fetch and pass engagement data

---

## Priority: LOW

This is a nice-to-have feature. Core functionality (posts, friends, analytics display) should be complete first.

**Estimated effort:** 2-4 hours depending on chosen option
