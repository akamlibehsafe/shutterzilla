# Documentation Automation Guide

This guide explains how to automate the maintenance of project documentation as you continue development.

**🚀 New to automation?** Start with [QUICK-START-AUTOMATION.md](./QUICK-START-AUTOMATION.md) for a 5-minute setup and daily workflow examples.

**📋 Quick Reference**: See [QUICK_REF.md](./QUICK_REF.md) for command reference.

**🔄 Standardized Workflow**: This project uses the **AI Development Documentation Toolkit**. See [DOCUMENTATION_WORKFLOW.md](./DOCUMENTATION_WORKFLOW.md) for the complete guide.

**🔄 Migrating?** See [MIGRATE_TO_TOOLKITS.md](./MIGRATE_TO_TOOLKITS.md) to migrate from old scripts to toolkits.

---

## Overview

The project has four main documentation types that benefit from automation:

1. **CHANGELOG.md**: User-facing "what changed" per release
2. **docs/project/decisions/**: ADRs (Architecture Decision Records) - "why we did X instead of Y"
3. **docs/project/runbook.md**: Operations guide (manual updates as needed)
4. **docs/project/ai-context.md**: Living briefing for AI/contributors (manual updates as needed)

---

## Automation Strategies

### 1. CHANGELOG.md Automation

#### Option A: Git-based Automation (Recommended)

Use git commit messages to auto-populate CHANGELOG.

**Setup**:
1. Use [Conventional Commits](https://www.conventionalcommits.org/) format in commit messages:
   ```
   feat: add user authentication
   fix: resolve scraper timeout issue
   docs: update tech stack guide
   chore: update dependencies
   ```

2. Use a tool like [git-chglog](https://github.com/git-chglog/git-chglog) or [standard-version](https://github.com/conventional-changelog/standard-version):

   **Using standard-version** (Node.js):
   ```bash
   npm install --save-dev standard-version
   # Add to package.json:
   "scripts": {
     "release": "standard-version"
   }
   ```

   **Using git-chglog** (Go-based, language-agnostic):
   ```bash
   # Install git-chglog
   brew install git-chglog  # macOS
   # or download from https://github.com/git-chglog/git-chglog/releases
   
   # Initialize config
   git-chglog --init
   
   # Generate changelog
   git-chglog -o CHANGELOG.md
   ```

**Workflow**:
```bash
# 1. Make changes with conventional commits
git commit -m "feat: add camera detail page"
git commit -m "fix: resolve image loading issue"

# 2. Before release, generate changelog
npm run release  # or git-chglog -o CHANGELOG.md

# 3. Review generated CHANGELOG.md
# 4. Commit and tag
git commit -am "chore: update changelog"
git tag v0.3.0
git push origin main --tags
```

#### Option B: Use doc_update_changelog Script (Recommended for this project)

We provide a script that adds entries to CHANGELOG.md:

**Usage:**
```bash
doc_update_changelog Added "New feature description"
doc_update_changelog Fixed "Bug fix description"
```

**The script is already set up** - just use it as you work!

#### Option C: Manual with Templates (If you prefer)

You can manually edit CHANGELOG.md, but using `doc_update_changelog` is recommended.
  echo "Usage: $0 <version> <entry> [type]"
  echo "Example: $0 'Unreleased' 'Added user authentication' 'Added'"
  exit 1
fi

# Add to Unreleased section if version is "Unreleased"
if [ "$VERSION" == "Unreleased" ]; then
  sed -i '' "/^## Unreleased$/a\\
\\
- $ENTRY
" CHANGELOG.md
else
  # Create new version section
  sed -i '' "/^## Unreleased$/a\\
\\
## $VERSION - $(date +%Y-%m-%d)\\
### $TYPE\\
- $ENTRY
" CHANGELOG.md
fi

echo "Updated CHANGELOG.md"
```

**Usage**:
```bash
doc_update_changelog Added "User authentication"
```

#### Option C: GitHub Actions Automation

Automate CHANGELOG generation on releases:

**Create `.github/workflows/release.yml`**:
```yaml
name: Release

on:
  release:
    types: [published]

jobs:
  update-changelog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: metcalfc/changelog-generator@v4.3.2
        with:
          myToken: ${{ secrets.GITHUB_TOKEN }}
          excludedLabels: |
            skip-changelog
            duplicate
            question
            invalid
          templateFile: .github/changelog-template.hbs
      - name: Commit changelog
        run: |
          git config user.name github-actions
          git config user.email github-actions@github.com
          git add CHANGELOG.md
          git commit -m "chore: update changelog for ${{ github.event.release.tag_name }}" || exit 0
          git push
```

---

### 2. ADR Automation

ADRs (Architecture Decision Records) should be created when making significant architectural decisions.

#### Option A: Use doc_new_adr Script (Recommended)

**The `doc_new_adr` script is already set up.** Just use it:

```bash
doc_new_adr "use-prisma-orm"
# Creates: docs/project/decisions/0007-use-prisma-orm.md
# Edit the file to fill in: Context, Decision, Alternatives, Consequences
```

#### Option B: Git Hook (Interactive)

**Create `.git/hooks/pre-commit`** (or use Husky):
```bash
#!/bin/bash
# Prompt for ADR when certain files change
# Example: if database schema changes, prompt for ADR

if git diff --cached --name-only | grep -q "supabase/migrations"; then
  echo "⚠️  Database migration detected. Consider creating an ADR:"
  echo "   doc_new_adr \"decision-title\""
  read -p "Continue commit? (y/n) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi
```

**Or use Husky (Node.js)**:
```bash
npm install --save-dev husky
npx husky install

# Create pre-commit hook
npx husky add .husky/pre-commit "node scripts/check-adr.js"
```

---

### 3. AI Context Automation

`docs/project/ai-context.md` should be updated manually, but you can create reminders.

#### Option A: Update Script with Prompts

**Create `scripts/update-ai-context.sh`**:
```bash
#!/bin/bash
# Interactive script to update ai-context.md

echo "Updating AI Context..."
echo ""

# Prompt for current priorities
echo "What are the current priorities? (press Enter when done)"
read -r -d '' PRIORITIES
echo ""

# Update priorities section
sed -i '' "/^### What's Next$/,/^### What Not to Change$/c\\
### What's Next\\
$(echo "$PRIORITIES" | sed 's/^/1. /')\\
\\
### What Not to Change
" docs/project/ai-context.md

# Update last modified date
sed -i '' "s/\*\*Last Updated\*\*:.*/\*\*Last Updated\*\*: $(date +%Y-%m-%d)/" docs/project/ai-context.md

echo "Updated docs/project/ai-context.md"
```

#### Option B: GitHub Action (Weekly Reminder)

**Create `.github/workflows/docs-reminder.yml`**:
```yaml
name: Documentation Reminder

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9 AM
  workflow_dispatch:

jobs:
  reminder:
    runs-on: ubuntu-latest
    steps:
      - name: Create issue
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.create({
              owner: context.repo.owner,
              repo: context.repo.repo,
              title: '📚 Weekly: Update AI Context & Changelog',
              body: `
              This is a weekly reminder to:
              
              1. Update \`docs/project/ai-context.md\` with current priorities
              2. Move items from "Unreleased" to version sections in \`CHANGELOG.md\`
              3. Review if any ADRs need updating
              
              **Scripts available:**
              - \`doc_update_changelog\` - Add changelog entries
              - \`doc_new_adr\` - Create new ADR
              - Manually edit \`docs/project/ai-context.md\` when priorities change
              `,
              labels: ['documentation', 'maintenance']
            })
```

---

## Recommended Workflow

### Daily Development

1. **Make changes** with conventional commit messages:
   ```bash
   git commit -m "feat: add camera search functionality"
   ```

2. **For significant decisions**, create ADR:
   ```bash
   doc_new_adr "use-algolia-search"
   ```

3. **For bug fixes or features**, update CHANGELOG:
   ```bash
   doc_update_changelog Added "Camera search functionality"
   ```

### Before Release

1. **Generate/update CHANGELOG**:
   ```bash
   npm run release  # or git-chglog -o CHANGELOG.md
   ```

2. **Review CHANGELOG.md** and move items from "Unreleased" to version section

3. **Update AI context** if priorities changed:
   ```bash
   # Manually edit docs/project/ai-context.md if priorities changed
   ```

4. **Tag release**:
   ```bash
   git tag v0.3.0
   git push origin main --tags
   ```

---

## Quick Setup

### Minimal Setup (5 minutes)

The scripts are already set up in your project! Just use them:

```bash
# Test scripts
doc_new_adr "test-decision"
doc_update_changelog Added "Test entry"
doc_check
```

### Full Setup (15 minutes)

1. **Install standard-version**:
   ```bash
   npm install --save-dev standard-version
   # Add to package.json:
   "scripts": {
     "release": "standard-version"
   }
   ```
   
2. **Set up GitHub Actions** (optional):
   - Copy `.github/workflows/release.yml` from above
   - Copy `.github/workflows/docs-reminder.yml` from above

3. **Set up pre-commit hook** (optional):
   - Use Husky or git hooks as shown above

---

## Tools & Resources

### CHANGELOG Tools
- **[standard-version](https://github.com/conventional-changelog/standard-version)**: Node.js, simple
- **[git-chglog](https://github.com/git-chglog/git-chglog)**: Go-based, language-agnostic
- **[changelog-generator-action](https://github.com/metcalfc/changelog-generator)**: GitHub Actions

### Commit Message Tools
- **[Commitizen](https://github.com/commitizen/cz-cli)**: Interactive commit message tool
- **[Conventional Commits](https://www.conventionalcommits.org/)**: Commit message standard

### Documentation Tools
- **[ADR Tools](https://github.com/npryce/adr-tools)**: ADR management (optional, for complex projects)

---

## Tips

1. **Start simple**: Use manual scripts first, then automate as needed
2. **Be consistent**: Use conventional commits from day one
3. **Review regularly**: Set aside 10 minutes weekly to review docs
4. **Update AI context**: When priorities change, update immediately
5. **Link ADRs**: Reference ADRs in code comments when implementing decisions

---

**Last Updated**: 2026-01-15
