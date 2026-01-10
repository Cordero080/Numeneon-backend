# Activity Visualization - Current Status

> **Last Updated:** January 8, 2026

## 🚦 Implementation Status: FRONTEND COMPLETE (Mock Data)

The Activity Visualization feature is **fully functional in the UI** but uses **mock/generated data** instead of real analytics from the backend.

---

## What's Working Now

| Component       | Status     | What It Shows               | Data Source                                      |
| --------------- | ---------- | --------------------------- | ------------------------------------------------ |
| **Wave Chart**  | ✅ Renders | 3-layer engagement wave     | `seededRandom(userId)` generates 52 weeks        |
| **Heatmap**     | ✅ Renders | 52×7 day grid               | `seededRandom(userId)` generates activity levels |
| **View Toggle** | ✅ Works   | Switch between Wave/Heatmap | `viewMode` state                                 |
| **Gradients**   | ✅ Applied | Cyan-to-blue vertical fade  | SVG `<linearGradient>`                           |
| **Glow Effect** | ✅ Applied | Neon halo on waves          | SVG `<filter>` with blur                         |
| **Content Mix** | ✅ Renders | Donut chart breakdown       | Hardcoded percentages                            |
| **Peak Time**   | ✅ Renders | "Sat 7PM" style label       | Hardcoded value                                  |

---

## How Mock Data Works

The visualization attempts to use **real post data** first. If a user has less than 5 weeks of activity (sparse data), it falls back to **impressive demo data** generated from their user ID.

### Demo Data Fallback Logic

```javascript
// Check if real data is too sparse (< 10% filled for heatmap, < 5 weeks for waves)
// If sparse → use seededRandom(userId) for consistent, impressive demo

// Demo heatmap: weighted distribution for "lit up" look
// 15% empty, 20% low, 30% medium, 35% high activity

// Demo waves: base 30% height + variance for natural-looking curves
// No flat zeros, always has interesting variation
```

### Why Fallback?

- **New users** and **seed users** don't have 52 weeks of real posts
- Empty charts look broken, not "new"
- Seeded random ensures each user has **consistent** demo data (same every reload)
- Each user's ID produces a **unique pattern** (pablo_pistola looks different than natalia_dev)

### When Real Data Kicks In

Once a user has significant activity (5+ weeks of engagement), the visualization switches to showing **real data** automatically.

---

## What's Missing for Real Data

### Backend Requirements

1. **Activity Tracking Model** (new)

   ```python
   class ActivityLog(models.Model):
       user = models.ForeignKey(User, on_delete=models.CASCADE)
       activity_type = models.CharField(max_length=20)  # post, like, comment
       created_at = models.DateTimeField(auto_now_add=True)
   ```

2. **Analytics Endpoints** (new)

   ```
   GET /api/analytics/weekly/      → 52-week engagement data
   GET /api/analytics/daily/       → 365-day activity counts
   GET /api/analytics/content-mix/ → Post type breakdown
   ```

3. **Aggregation Logic**
   - Group posts/likes/comments by week
   - Calculate engagement scores
   - Track peak posting times

### Frontend Requirements

1. **Replace mock generators with API calls**

   ```javascript
   // Instead of:
   const data = generateMockData(userId);

   // Do:
   const { data: analytics } = useQuery(["analytics", userId], fetchAnalytics);
   ```

2. **Handle loading/error states**
3. **Cache analytics data** (doesn't change frequently)

---

## Stretch Goal: Real Analytics

This is documented in [stretch-goals/AdvancedAnalytics.md](../../stretch-goals/AdvancedAnalytics.md)

**Priority:** LOW (nice-to-have after core features work)

**Effort:**

- Backend: ~8 hours (new model, migrations, endpoints)
- Frontend: ~4 hours (swap mock → real, add loading states)

---

## Testing the Current Implementation

1. **Log in to your account**
2. **Navigate to YOUR profile** (`/profile`)
3. **Click the profile card** to flip it
4. **Back of card shows Activity Visualization**
5. **Toggle between Wave/Heatmap views**

Both views should render immediately with consistent (but fake) data.

---

## Privacy Design Decision

**Activity Visualization is ONLY visible to the logged-in user on their OWN profile.**

| Scenario                       | Activity Viz Visible? |
| ------------------------------ | --------------------- |
| Viewing YOUR profile           | ✅ Yes                |
| Viewing someone else's profile | ❌ No                 |
| Logged out                     | ❌ No                 |

**Why?** This is a social network, not a business analytics tool. Showing other users' posting frequency and engagement patterns would feel invasive and "nosy." Activity data is personal—it's for self-reflection, not surveillance.

This aligns with the privacy-first approach documented in [ProfilePrivacyControls.md](../../features-implemented/ProfilePrivacyControls.md).

---

## File Locations

| Component       | Path                                                                                                             |
| --------------- | ---------------------------------------------------------------------------------------------------------------- |
| Main component  | `src/components/pages/Profile/components/ProfileCard/components/ActivityVisualization/ActivityVisualization.jsx` |
| Wave path logic | `src/components/pages/Profile/components/ProfileCard/ProfileCard.jsx` (createWavePath)                           |
| Styles          | `ActivityVisualization.scss` (same folder)                                                                       |

---

## Summary

✅ **Looks complete** - Users see beautiful wave charts and heatmaps  
⚠️ **Not connected** - Data is generated, not fetched from backend  
🎯 **Next step** - Build analytics API when time permits
