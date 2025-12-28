# Git Branching Strategy

This document defines the branching workflow for the Evolution of Todo project.

## 📋 Overview

This project follows **GitHub Flow** - a simplified branching model optimized for continuous delivery:

```
main (always deployable)
  ↓
feature branch (short-lived)
  ↓
Pull Request + Review
  ↓
Merge to main + Delete branch
```

## 🌳 Branch Structure

### Main Branch

- **Name**: `main`
- **Purpose**: Production-ready code
- **Protection**: Always deployable, all tests passing
- **Lifespan**: Permanent

**Rules**:
- ✅ All code must be merged via Pull Request
- ✅ Must pass all tests before merge
- ✅ Never commit directly to main (except critical hotfixes)
- ✅ Always represents the current state of the project

### Feature Branches

- **Naming**: `<issue-number>-<feature-name>` (e.g., `001-cli-todo-app`, `002-database-setup`)
- **Purpose**: Develop a single feature or fix
- **Lifespan**: Short-lived (hours to days, not weeks)
- **Branched from**: `main`
- **Merged to**: `main`

**Rules**:
- ✅ One feature per branch
- ✅ Create from latest `main`
- ✅ Merge back to `main` via Pull Request
- ✅ Delete after successful merge

## 🔄 Workflow

### 1. Start a New Feature

```bash
# Update main to latest
git checkout main
git pull origin main

# Create feature branch from main
git checkout -b 005-new-feature

# Verify you're on the new branch
git branch
```

### 2. Develop the Feature

```bash
# Make changes
# Edit files...

# Commit frequently with descriptive messages
git add .
git commit -m "feat: implement user authentication"

# Push to remote regularly (backup + collaboration)
git push origin 005-new-feature
```

### 3. Keep Feature Branch Updated

```bash
# If main has new commits while you're working
git checkout main
git pull origin main

git checkout 005-new-feature
git merge main  # Or: git rebase main (advanced)

# Resolve conflicts if any, then push
git push origin 005-new-feature
```

### 4. Create Pull Request

```bash
# Push final changes
git push origin 005-new-feature

# Create PR on GitHub
gh pr create --title "Add new feature" --body "Description of changes"

# Or use GitHub web interface
```

### 5. Code Review & Merge

```bash
# After approval, merge via GitHub UI (creates merge commit)
# Or via CLI:
gh pr merge 123 --merge

# Pull updated main
git checkout main
git pull origin main
```

### 6. Clean Up

```bash
# Delete local feature branch
git branch -d 005-new-feature

# Delete remote feature branch (if not auto-deleted)
git push origin --delete 005-new-feature
```

## 📏 Commit Message Conventions

Follow [Conventional Commits](https://www.conventionalcommits.org/) format:

```
<type>(<scope>): <description>

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring (no feature change, no bug fix)
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, config)

### Examples

```bash
git commit -m "feat(auth): add JWT authentication"
git commit -m "fix(api): resolve 404 error on task deletion"
git commit -m "docs: update README with deployment instructions"
git commit -m "test(crud): add integration tests for update endpoint"
```

## 🏷️ Version Tagging

Tag releases to mark significant milestones:

```bash
# Tag a release
git tag -a v1.0.0 -m "Release version 1.0.0 - Feature X complete"

# Push tags to remote
git push origin --tags

# List all tags
git tag -l
```

### Semantic Versioning

Format: `vMAJOR.MINOR.PATCH[-LABEL]`

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)
- **LABEL**: Pre-release identifier (e.g., `-alpha`, `-beta`, `-phase1-cli`)

**Examples**:
- `v1.0.0-phase1-cli` - Phase I CLI App
- `v1.1.0-phase2-database` - Phase II Database Integration
- `v1.2.0-phase2-backend-api` - Phase II Backend API
- `v1.3.0-phase2-frontend` - Phase II Frontend

## 🚫 What NOT to Do

### ❌ Anti-Pattern: Long-Lived Feature Branches

**Problem**: Feature branches that live for weeks/months without merging
```
main:          [commit A] ────────────────────────────────────→
                  ↓
feature-branch:   [B] → [C] → [D] → [E] → [F] → [G] → [H]
                  (never merged, diverges from main)
```

**Why it's bad**:
- Merge conflicts accumulate
- Integration issues discovered late
- Main branch becomes outdated
- Hard to track "current" state

**Solution**: Merge frequently (every few days or when feature is complete)

### ❌ Anti-Pattern: Direct Commits to Main

**Problem**: Committing directly to main without PR/review
```bash
# BAD - Don't do this
git checkout main
git commit -m "quick fix"
git push origin main
```

**Why it's bad**:
- Bypasses code review
- May break tests
- No audit trail

**Solution**: Always use feature branches + Pull Requests

### ❌ Anti-Pattern: Multiple Features in One Branch

**Problem**: Mixing unrelated changes in a single branch
```bash
# BAD - Don't do this
git checkout -b 005-multiple-features
# Implements auth + database + UI changes
```

**Why it's bad**:
- Hard to review
- Can't merge partially
- Difficult to rollback

**Solution**: One branch = one feature/fix

## 📊 Current Project Status

### ✅ Corrected Workflow (2025-12-28)

All feature branches have been properly merged to main:

```
main: [Initial] → [001] → [002] → [003] → [004] → (current)
         ↓         ↓       ↓       ↓       ↓
Branches: 001     002     003     004   (merged & can be deleted)
Tags:   v1.0.0  v1.1.0  v1.2.0  v1.3.0
```

**Changes Made**:
1. Updated main README to reflect all phases
2. Merged `002-database-setup` → main
3. Merged `003-backend-api` → main
4. Merged `004-frontend-nextjs` → main
5. Tagged each phase release
6. Pushed all changes to GitHub

### 🎯 Next Steps

**For Future Features**:
1. Create new branch from latest `main`
2. Develop feature
3. Create PR
4. Review + Merge
5. Delete feature branch
6. Tag release if significant

## 🔍 Inspecting Branch History

### Check what's in a branch

```bash
# Compare feature branch to main
git diff main..feature-branch

# List commits in feature branch not in main
git log main..feature-branch --oneline

# Visualize branch history
git log --graph --oneline --all --decorate
```

### Check if branch is merged

```bash
# List merged branches
git branch --merged main

# List unmerged branches
git branch --no-merged main
```

## 🛠️ Common Scenarios

### Scenario 1: Feature Branch Conflicts with Main

```bash
# Your feature branch has conflicts with main
git checkout feature-branch
git fetch origin
git merge origin/main

# Resolve conflicts in editor
# Then:
git add .
git commit -m "merge: resolve conflicts with main"
git push origin feature-branch
```

### Scenario 2: Need to Update Feature Branch with Latest Main

```bash
git checkout main
git pull origin main

git checkout feature-branch
git merge main
git push origin feature-branch
```

### Scenario 3: Accidentally Committed to Wrong Branch

```bash
# You committed to main instead of feature branch
git checkout main
git log  # Note the commit hash (e.g., abc123)

# Move commit to feature branch
git checkout feature-branch
git cherry-pick abc123

# Remove from main
git checkout main
git reset --hard HEAD~1  # CAREFUL! Only if not pushed to remote
```

## 📚 Resources

- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Semantic Versioning](https://semver.org/)
- [Git Branching - Basic Branching and Merging](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging)

## 🤝 Contributing

When contributing to this project:

1. **Read this document** before creating branches
2. **Follow the workflow** outlined above
3. **Write clear commit messages** using conventional commits
4. **Keep PRs small and focused** - one feature/fix per PR
5. **Update documentation** when adding features
6. **Write tests** before merging to main

---

**Last Updated**: 2025-12-28
**Status**: All phases merged to main, proper workflow established
