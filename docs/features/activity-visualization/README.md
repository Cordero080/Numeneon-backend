# Activity Visualization Feature

## 📁 Contents

| File                                             | Purpose                                                       |
| ------------------------------------------------ | ------------------------------------------------------------- |
| [overview.md](overview.md)                       | Feature design, visual components, what each viz shows        |
| [technical-consensus.md](technical-consensus.md) | Implementation details, SVG algorithms, how it actually works |
| [current-status.md](current-status.md)           | Where this feature is NOW in the app (mock data vs real)      |

---

## Quick Summary

The Activity Visualization component displays user engagement analytics on the **back of the profile flip card**. It includes:

- 🌊 **Wave Chart** - Smooth area chart showing engagement trends (likes, comments, shares)
- 📅 **Heatmap** - GitHub-style grid showing posting frequency by day
- 🍩 **Content Mix Donut** - Breakdown of post types (thoughts/media/milestones)
- ⚡ **Peak Time** - When user is most active

## Current Implementation Status

| Component   | Status    | Data Source          |
| ----------- | --------- | -------------------- |
| Wave Chart  | ✅ Active | Mock (seeded random) |
| Heatmap     | ✅ Active | Mock (seeded random) |
| Content Mix | ✅ Active | Mock (hardcoded)     |
| Peak Time   | ✅ Active | Mock (hardcoded)     |

**See [current-status.md](current-status.md) for full details on what's real vs mock.**
