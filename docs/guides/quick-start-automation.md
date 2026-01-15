# Quick Start: Automating Documentation

**Goal**: Keep CHANGELOG.md and ADRs updated as you develop, with minimal effort.

---

## 🚀 5-Minute Setup

### Step 1: Make Scripts Executable

```bash
chmod +x scripts/*.sh
```

That's it! Scripts are ready to use.

---

## 📝 Daily Workflow

### When You Add a Feature

**Use the doc_update_changelog script:**
```bash
# Add to changelog immediately
doc_update_changelog Added "Camera search functionality"

# Commit as usual
git add .
git commit -m "feat: add camera search functionality"
```

**Or use conventional commits (automatic later):**
```bash
# Just use conventional commit format
git commit -m "feat: add camera search functionality"
# Later, generate changelog with: npm run release
```

### When You Fix a Bug

```bash
# Update changelog
doc_update_changelog Fixed "Scraper timeout issue"

# Commit
git commit -m "fix: resolve scraper timeout issue"
```

### When You Make an Architectural Decision

```bash
# Create new ADR (opens template ready to fill)
doc_new_adr "use-prisma-orm"

# Fill in the ADR file that was created
# Then commit
git add docs/project/decisions/0007-use-prisma-orm.md
git commit -m "docs: add ADR for Prisma ORM decision"
```

---

## 🔄 Real-World Example: Adding User Authentication

Here's how you'd document it step-by-step:

### 1. Start the feature
```bash
git checkout -b feature/user-auth
```

### 2. Make an ADR if it's a significant decision
```bash
doc_new_adr "use-supabase-auth"
# Fill in docs/project/decisions/0007-use-supabase-auth.md
```

### 3. Build the feature
```bash
# Make your code changes...
```

### 4. Update changelog as you go
```bash
doc_update_changelog Added "User authentication with email/password and OAuth"
doc_update_changelog Added "Password reset functionality"
```

### 5. Commit with conventional format
```bash
git commit -m "feat: add user authentication"
git commit -m "feat: add password reset flow"
```

### 6. Before merging, review changelog
```bash
# Review CHANGELOG.md - move items from Unreleased to version section
doc_release 0.3.0  # This moves unreleased entries to version
```

### 7. Merge and release
```bash
git checkout main
git merge feature/user-auth
git tag v0.3.0
git push origin main --tags
```

---

## ⚡ Pro Tips

### Tip 1: Use Aliases

Add to your `~/.zshrc` or `~/.bashrc`:
```bash
alias changelog='doc_update_changelog Added'
alias adr='doc_new_adr'
```

Then use:
```bash
changelog "Added new feature" "Added"
adr "Decision title"
```

### Tip 2: Pre-Commit Hook (Optional)

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
# Reminder to update docs if significant changes

if git diff --cached --name-only | grep -E "(supabase/migrations|apps/backend|apps/frontend)" > /dev/null; then
  echo "📝 Reminder: Consider updating CHANGELOG.md or creating an ADR"
  echo "   Run: doc_update_changelog <category> '<entry>'"
  echo "   Or:  doc_new_adr '<decision>'"
fi
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

### Tip 3: Weekly Review (5 minutes)

Every Monday, do this:

```bash
# 1. Review Unreleased items in CHANGELOG.md
# 2. Move important items to a version section if you're releasing
# 3. Update priorities in docs/project/ai-context.md if they changed
```

---

## 🎯 What Gets Automated vs. Manual

### ✅ Automated (with scripts)
- **CHANGELOG.md entries**: Use `doc_update_changelog`
- **ADR creation**: Use `doc_new_adr`

### 📝 Manual (but easy)
- **Filling in ADR details**: Script creates template, you fill in the "why"
- **Reviewing changelog before release**: Move items from Unreleased to version
- **Updating ai-context.md priorities**: When they change (maybe monthly)

### 🔄 Fully Automated (optional, advanced)
- **Generate changelog from git commits**: Use `standard-version` or `git-chglog`
- **GitHub Actions**: Auto-generate on releases
- **Pre-commit hooks**: Remind you to document changes

---

## 📋 Quick Reference

### Changelog Entry Types
- `Added`: New features
- `Changed`: Changes to existing features
- `Fixed`: Bug fixes
- `Breaking`: Breaking changes (requires version bump)

### When to Create ADR
Create an ADR when you make a decision that:
- Affects architecture (database, frameworks, tools)
- Has trade-offs worth documenting
- Might be questioned later ("why did we choose X?")

**Don't create ADR for**: Obvious choices, trivial decisions, temporary workarounds.

### Changelog Workflow
1. **During development**: Add to "Unreleased" section
2. **Before release**: Move items to version section (e.g., "0.3.0")
3. **After release**: Start fresh with new "Unreleased" items

---

## 🔧 Advanced: Full Automation with standard-version

If you want fully automatic changelog generation:

### Setup (one time)
```bash
npm install --save-dev standard-version
```

Add to `package.json`:
```json
{
  "scripts": {
    "release": "standard-version",
    "release:minor": "standard-version --release-as minor",
    "release:patch": "standard-version --release-as patch"
  }
}
```

### Usage
```bash
# Make commits with conventional format
git commit -m "feat: add user authentication"
git commit -m "fix: resolve scraper timeout"

# Before release, generate changelog automatically
npm run release

# This will:
# 1. Generate CHANGELOG.md from commits
# 2. Bump version in package.json
# 3. Create git tag
# 4. Commit everything

# Push
git push origin main --follow-tags
```

**Conventional commit formats:**
- `feat:` → Added section
- `fix:` → Fixed section
- `BREAKING CHANGE:` → Breaking section
- `docs:`, `chore:`, `style:` → Not included (internal changes)

---

## 🎓 Example: Complete Feature Cycle

```bash
# 1. Start feature
git checkout -b feature/camera-search

# 2. Make decision → Create ADR
doc_new_adr "use-algolia-search"
# Fill in docs/project/decisions/0007-use-algolia-search.md

# 3. Implement feature (make code changes)

# 4. Update changelog as you go
doc_update_changelog Added "Camera search with filters"
doc_update_changelog Added "Saved search functionality"

# 5. Commit
git add .
git commit -m "feat: add camera search with Algolia"
git commit -m "feat: add saved search functionality"

# 6. Test and fix
doc_update_changelog Fixed "Search filter edge case"
git commit -m "fix: resolve search filter edge case"

# 7. Before merge, prepare release
doc_release 0.3.0  # Moves all unreleased entries to version

# 8. Merge
git checkout main
git merge feature/camera-search
git tag v0.3.0
git push origin main --tags
```

---

## ❓ FAQ

**Q: Do I need to update changelog for every commit?**  
A: No, just for user-facing changes. Internal refactoring doesn't need changelog entries.

**Q: When should I create an ADR?**  
A: When choosing between alternatives that have trade-offs. Example: "Should we use Prisma or raw SQL?" → Yes, create ADR. "Should we use async/await?" → No, too trivial.

**Q: Can I automate everything?**  
A: Mostly yes, but reviewing and filling ADR details should be manual (they require thought).

**Q: What if I forget to document?**  
A: That's okay! You can always add entries later. Use `git log` to see what changed and add to changelog retroactively.

---

## 🎯 Recommended Workflow Summary

**Daily:**
- Use scripts to add changelog entries as you work
- Create ADRs for significant decisions
- Use conventional commit messages

**Weekly (5 min):**
- Review Unreleased section in CHANGELOG.md
- Update `docs/project/ai-context.md` if priorities changed

**Before Release:**
- Move items from Unreleased to version section
- Review all ADRs are accepted (not proposed)
- Tag release

---

**That's it! Start using the scripts today and your docs will stay up-to-date.**

For more details, see [docs/guides/automation.md](./automation.md).
