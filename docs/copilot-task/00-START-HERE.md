# 🚀 START HERE: Numeneon Team Rebuild Guide

## What Is This?

This is a **complete instruction set** for rebuilding the Numeneon app as a team using pseudocode shells. Read this FIRST to understand the entire system before diving into the 5 detailed instruction files.

---

## 📋 Quick Context

**What:** Pablo built a complete working cyberpunk social media app (React + Django). The team will now REBUILD it from pseudocode shells to learn architecture, state management, and full-stack patterns.

**Why:** Everyone needs git history showing their contributions, but the app must reproduce EXACTLY as it works now.

**How:** Two shell branches with pseudocode → team fills in the code → app works identically.

---

## 🎯 The Plan (30-Second Version)

1. **Create 2 shell branches** (`team-shell-frontend` + `team-shell-backend`)
2. **Delete opposite folder** (frontend shell deletes backend/, vice versa)
3. **Replace ALL logic with detailed pseudocode** (styles/icons stay intact)
4. **Repo czar creates empty repos** → team forks
5. **Pablo merges shells to dev** → team forks dev
6. **Everyone rebuilds from pseudocode** (including Pablo for git history)
7. **Result:** Working app, everyone has PRs proving contribution

---

## ⚠️ IMPORTANT: Each Team Member Creates a Superuser

After setting up the backend, each person should create their own Django superuser:

```bash
cd backend
pipenv shell
python manage.py createsuperuser
```

**Why?** Access to Django admin (`http://127.0.0.1:8000/admin/`) lets you:

- Create test users and data without API calls
- Debug database issues directly
- View relationships between models
- Seed your own test scenarios

---

## � CRITICAL: What Goes in Shell Branches vs Stays Here

**This `docs/copilot-task/` folder is PLANNING DOCUMENTATION ONLY.**

It does NOT go into the shell branches. The shell branches contain:

- Pseudocode files (team rebuilds these)
- SCSS styles (provided, not rebuilt)
- SVG icons (provided, not rebuilt)
- Config files (vite.config.js, package.json, etc.)

This folder stays in Pablo's original branch as reference for creating the shells.

---

## 🚨 CRITICAL: What Goes in Shell Branches

**This `docs/copilot-task/` folder is PLANNING DOCUMENTATION ONLY.**

It does **NOT** go into the shell branches. Keep it in Pablo's original/planning branch.

**Shell branches contain:**

- Pseudocode files (`.jsx`, `.py` with TODO comments)
- SCSS styles (provided complete, not rebuilt)
- SVG icons (provided complete, not rebuilt)
- Config files (vite.config.js, package.json, etc.)

**Shell branches do NOT contain:**

- `docs/copilot-task/` folder
- `docs/team-plan/` folder (team gets individual `.md` files via other means)
- Any planning/strategy documentation

---

## �📚 The 5 Instruction Files (Read In Order)

### **File 1: [01-CONTEXT-AND-STRATEGY.md](./01-CONTEXT-AND-STRATEGY.md)**

**Read Time:** 10 minutes  
**Purpose:** Big picture strategy, team assignments, branch structure

**You'll Learn:**

- T-shirt sizing (XL → S) and who owns what
- Why styles are provided but logic is rebuilt
- How icons work (modular system + backward compatibility)
- Branch structure (`team-shell-frontend` vs `team-shell-backend`)
- Assets provided vs rebuilt (SCSS, icons, design system)

**Key Sections:**

- Team assignments table (Pablo XL, Natalia L, Colin M, Crystal M, Tito S)
- SVG icon strategy (12 category files + barrel export)
- Branch workflow (fork, feature branch, PR)
- File validation results (148 files validated)

---

### **File 2: [02-PSEUDOCODE-EXAMPLES.md](./02-PSEUDOCODE-EXAMPLES.md)**

**Read Time:** 15 minutes  
**Purpose:** 12 detailed examples showing EXACTLY how pseudocode should look

**You'll Learn:**

- How to write backend model pseudocode (Django ORM)
- How to write view/API endpoint pseudocode (DRF)
- How to write React context pseudocode (state + functions)
- How to write service layer pseudocode (API calls)
- How to write component pseudocode (JSX + logic)
- How to document integration points between files

**Key Examples:**

- Backend Post model (fields, relationships, choices)
- Backend PostViewSet (CRUD + custom actions)
- Frontend PostsContext (state, CRUD functions, useEffect)
- Frontend postsService (API calls with apiClient)
- Login component (form, validation, context usage)
- Login.scss (style structure with TODO comments)
- Collaborative files (urls.py, contexts/index.js)

**Critical Concept:** Pseudocode is DETAILED, not vague. Includes:

- What to build
- Why it's needed
- How it integrates with other files
- Expected data formats
- Example API responses
- Think-about questions for learning

---

### **File 3: [03-BACKEND-INSTRUCTIONS.md](./03-BACKEND-INSTRUCTIONS.md)**

**Read Time:** 20 minutes  
**Purpose:** Specific pseudocode for EVERY backend Python file

**You'll Learn:**

- Natalia's 11 files (auth system, Profile model, migrations)
- Colin's 7 files (Post model, Like model, posts API)
- Crystal's 7 files (Friendship model, FriendRequest model, friends API)
- Collaborative file (numeneon/urls.py)
- Project-level files (manage.py, settings.py, seed_posts.py)

**Structure:**

- File-by-file pseudocode templates
- Integration points documented
- API response formats shown
- Database relationships explained

---

### **File 4: [04-FRONTEND-INSTRUCTIONS.md](./04-FRONTEND-INSTRUCTIONS.md)**

**Read Time:** 20 minutes  
**Purpose:** Specific pseudocode for frontend JS/JSX files

**You'll Learn:**

- Natalia's 8 frontend files (AuthContext, Login, Signup, ProtectedRoute)
- Colin's 8 frontend files (PostsContext, postsService, ComposerModal, DeleteConfirmModal)
- Crystal's 4 frontend files (FriendsContext, friendsService, Friends page)
- Tito's 6 frontend files (apiClient, ThemeContext, ThemeToggle, main.jsx)
- Pablo's 75+ UI files (usage comments only, logic stays intact)

**Two Categories:**

1. **Full Pseudocode** - Team rebuilds (contexts, services, simple UI)
2. **Usage Comments** - Pablo's complex UI stays intact (Timeline, ProfileCard, Analytics)

**Critical:** Pablo's files get "USAGE" header blocks explaining:

- What the component does
- Props it accepts
- Context it uses
- Integration points
- DO NOT MODIFY warning

---

### **File 5: [05-TEAM-PLAN-FILES.md](./05-TEAM-PLAN-FILES.md)**

**Read Time:** 15 minutes  
**Purpose:** Templates for 6 team markdown files in `docs/team-plan/`

**You'll Learn:**

- Individual task breakdowns for each person
- File ownership lists (backend + frontend)
- Acceptance criteria for each task
- Integration checkpoints
- Testing strategies
- Team structure overview

**6 Files:**

1. `natalia.md` - Auth system + migration management (19 files)
2. `colin.md` - Posts CRUD + modals (15 files)
3. `crystal.md` - Friends system (12 files)
4. `pablo.md` - Complex UI (29 files)
5. `tito.md` - Infrastructure (6 files)
6. `team-structure.md` - Team overview and workflow

---

## 🎨 Assets Provided (NOT Pseudocode)

These files are **complete and working** in shell branches:

### Icons System ✅

```
frontend/src/assets/
├── icons.jsx          # Backward-compatible barrel export
└── icons/             # Modular system (12 category files)
    ├── index.js       # Main aggregator
    ├── navigation.jsx # TargetReticleIcon, BackIcon, FlipIcon, etc.
    ├── user.jsx       # UserIcon, GlobeIcon, LockIcon, VisibilityIcon (smart), etc.
    ├── engagement.jsx # HeartIcon, CommentIcon, ShareIcon, etc.
    ├── actions.jsx    # EditIcon, TrashIcon, CloseIcon, etc.
    ├── media.jsx      # ImageIcon, ExpandIcon, etc.
    ├── ui.jsx         # SettingsIcon, EyeIcon, GridIcon, etc.
    ├── sidenav.jsx    # HexHomeIcon, SignalIcon, NetworkIcon
    ├── analytics.jsx  # BoltIcon, BarChartIcon, ActivityIcon, etc.
    ├── profile.jsx    # LocationIcon, LinkIcon, CalendarIcon, etc.
    ├── messaging.jsx  # MessageBubbleIcon, EmojiIcon
    └── misc.jsx       # MusicIcon, MapPinIcon, PostTriangleIcon
```

### Vite Path Aliases ✅

To simplify imports and improve developer experience, Vite is configured with path aliases:

```javascript
// vite.config.js configuration:
resolve: {
  alias: {
    '@': './src',                    // Root source
    '@assets': './src/assets',       // Icons, images, SVGs
    '@components': './src/components', // All React components
    '@contexts': './src/contexts',   // Context providers
    '@services': './src/services',   // API service layers
    '@utils': './src/utils',         // Utility functions
    '@styles': './src/styles',       // Global SCSS files
  }
}
```

**Benefits:**

- No more `../../../../../../../` paths
- Consistent imports across the codebase
- Easier refactoring (paths don't break when moving files)

**Examples:**

```jsx
// OLD (relative paths)
import { HeartIcon } from "../../../../../../../assets/icons";
import { useAuth } from "../../../contexts/AuthContext";
import apiClient from "../../../services/apiClient";

// NEW (path aliases)
import { HeartIcon } from "@assets/icons";
import { useAuth } from "@contexts/AuthContext";
import apiClient from "@services/apiClient";
```

### SCSS System ✅

**How to use:**

```jsx
// Import using Vite path alias (recommended - cleaner imports)
import { HeartIcon, CloseIcon } from "@assets/icons";

// Or from specific category (tree-shakeable)
import { HeartIcon } from "@assets/icons/engagement";

// Usage
<HeartIcon size={18} className="custom-class" onClick={handleClick} />;
```

**Note:** The `@assets` alias replaces long relative paths like `../../assets`

### Styles System ✅

```
frontend/src/styles/
├── main.scss           # Master import file
├── _variables.scss     # Colors, spacing, breakpoints
├── _theme.scss         # Dark/light theme tokens
├── _mixins.scss        # Reusable style patterns
├── _reset.scss         # CSS reset
├── _typography.scss    # Font styles
├── _buttons.scss       # Button components
├── _cards.scss         # Card layouts
├── _layout.scss        # Page structure
├── _utilities.scss     # Helper classes
├── _animations.scss    # Keyframes, transitions
├── _blobs.scss         # Background effects
└── _light-mode.scss    # Light theme overrides
```

**All component .scss files** are also provided (70+ files)

---

## 👥 Team Assignments (T-Shirt Method)

| Person      | Size | Files | Focus                                            | Complexity                        |
| ----------- | ---- | ----- | ------------------------------------------------ | --------------------------------- |
| **Pablo**   | XL   | 29    | Timeline River, ProfileCard, Analytics, Carousel | Very High (canvas, complex state) |
| **Natalia** | L    | 19    | Auth system, migrations                          | High (Django auth, database)      |
| **Colin**   | M    | 15    | Posts CRUD, modals                               | Medium (REST API, forms)          |
| **Crystal** | M    | 12    | Friends system                                   | Medium (relationships, requests)  |
| **Tito**    | S    | 6     | Infrastructure, Theme                            | Low (utilities, config)           |

**Key Rule:** NO TWO PEOPLE TOUCH THE SAME FILE (prevents merge conflicts)

---

## 🔄 Workflow Overview

### Phase 1: Preparation (Pablo) ← **YOU ARE HERE**

1. ✅ Organize copilot-task folder (5 instruction files)
2. ✅ Move team-plan to `docs/team-plan/`
3. ✅ Validate icons system exists
4. ⏳ Create `team-shell-backend` branch
5. ⏳ Create `team-shell-frontend` branch

### Phase 2: Repo Setup (Repo Czar)

1. Create empty `numeneon-frontend` repo
2. Create empty `numeneon-backend` repo
3. Team forks both repos

### Phase 3: Shell Merge (Pablo)

1. Clone czar's repos
2. Merge `team-shell-frontend` into frontend repo
3. Merge `team-shell-backend` into backend repo
4. Push to czar's dev branch
5. Team pulls/forks updated dev branch

### Phase 4: Team Rebuild (Everyone)

1. Clone dev branch
2. Create feature branch: `[name]/[feature]`
3. Fill in pseudocode over multiple commits
4. Test integration with other team members
5. Create PR to main
6. Git history shows contribution timeline

### Phase 5: Integration & Testing

1. Merge all PRs
2. Test full app functionality
3. Fix any integration issues
4. Deploy

---

## 🚨 Critical Success Factors

### ✅ What Makes This Work

1. **Styles Provided** → Team only writes JSX/Python logic
2. **Icons Complete** → No reproduction issues (too complex)
3. **Detailed Pseudocode** → Clear expectations, integration points
4. **No File Overlap** → Zero merge conflicts
5. **Git History** → Everyone (including Pablo) has commits

### ⚠️ Potential Risks

1. **Pablo's Complex UI** - Timeline River, ProfileCard, Analytics heatmaps
   - **Mitigation:** Pablo's files stay intact, just get usage comments
2. **API Contract Mismatches** - Frontend expects different format than backend returns
   - **Mitigation:** Pseudocode documents exact request/response formats
3. **Integration Dependencies** - Component needs context that isn't ready yet
   - **Mitigation:** Pseudocode lists all dependencies and integration points
4. **State Management Timing** - Async state updates, race conditions
   - **Mitigation:** Pseudocode shows useEffect dependencies and cleanup

---

## 📊 Expected Accuracy

**High Confidence (95%+):**

- Backend models/serializers (clear Django patterns)
- API endpoints (REST conventions)
- Auth flow (standard JWT)
- Simple UI (Login, Signup, Friends list)
- Icons system (already complete)

**Medium Confidence (85-90%):**

- Timeline River UI (3-column layout, state choreography)
- ProfileCard flip system (canvas rendering, animations)
- Analytics visualizations (heatmaps, wave charts)

**Success Factor:** With detailed pseudocode + provided styles + complete icons, the app should reproduce at **90-95% accuracy**. Edge cases and subtle timing issues are the main risk.

---

## 🎯 Next Steps

### If You're Pablo:

Ready to create shell branches? Say:

> "Let's create the shell branches"

And I'll:

1. Create `team-shell-backend` (delete frontend, add pseudocode)
2. Create `team-shell-frontend` (delete backend, add pseudocode + styles + icons)
3. Ensure your pseudocode is detailed (for git history)

### If You're A Team Member:

1. **Read all 5 instruction files** (01 → 05)
2. **Open your team-plan file** (`docs/team-plan/[your-name].md`)
3. **Wait for shells to be ready** (czar will notify)
4. **Fork the repos** when available
5. **Start with Task 1** in your team plan

### If You're The Repo Czar:

1. Wait for Pablo to create shell branches
2. Create empty `numeneon-frontend` and `numeneon-backend` repos
3. Invite team as collaborators
4. Tell team to fork

---

## 📖 File Reference

### This Folder (`docs/copilot-task/`)

- `00-START-HERE.md` ← **YOU ARE HERE**
- `01-CONTEXT-AND-STRATEGY.md` - Big picture, team, strategy
- `02-PSEUDOCODE-EXAMPLES.md` - 12 detailed templates
- `03-BACKEND-INSTRUCTIONS.md` - Every backend file
- `04-FRONTEND-INSTRUCTIONS.md` - Every frontend file
- `05-TEAM-PLAN-FILES.md` - Team markdown templates

### Team Plans (`docs/team-plan/`)

- `natalia.md` - Auth tasks (19 files)
- `colin.md` - Posts tasks (15 files)
- `crystal.md` - Friends tasks (12 files)
- `pablo.md` - UI tasks (~35 files)
- `tito.md` - Infrastructure tasks (6 files)
- `team-structure.md` - Team overview

### Other Docs

- `docs/refactoring/SVG-Icons-Refactor.md` - Icon inventory
- `docs/features/` - Feature specifications
- `docs/features-implemented/` - Completed features

---

## 💡 Pro Tips

1. **Read in order** - Each file builds on the previous
2. **Check integration points** - Pseudocode lists dependencies
3. **Test early and often** - Don't wait till the end
4. **Ask about API contracts** - Frontend/backend must match exactly
5. **Use git history** - Small, focused commits > huge PRs
6. **Reference examples** - File 02 has 12 detailed templates

---

## ❓ Common Questions

**Q: Does Pablo rebuild his files too?**  
A: YES! Everyone rebuilds from pseudocode, including Pablo. This ensures legitimate git history for all team members. Pablo has an advantage since he wrote the original, but he still types and commits code like everyone else.

**Q: Do I rebuild the .scss files?**  
A: NO. Styles are provided. You only write JSX/Python logic.

**Q: Can I use AI to generate code?**  
A: Yes! That's expected. The pseudocode is detailed enough that AI can generate accurate code.

**Q: What if two people need to modify the same file?**  
A: They won't. The t-shirt method ensures zero file overlap.

**Q: How detailed is the pseudocode?**  
A: Very. It includes:

- What to build
- Why it's needed
- Integration points
- Data formats
- Example responses
- Learning questions

**Q: When do we start coding?**  
A: After Pablo creates shell branches and czar sets up repos (Phase 3).

---

## 🎉 You're Ready!

If you understand:

- The plan (2 shells → team rebuilds → working app)
- The structure (5 instruction files + team plans)
- The workflow (fork → feature branch → PR)
- The assets (icons + styles provided)

Then **start reading File 01: Context & Strategy** →

---

**Last Updated:** January 8, 2026  
**Version:** 1.2 (Updated component structure, added SearchContext, PostCard modularization)  
**Maintained By:** Pablo (UI Lead)
