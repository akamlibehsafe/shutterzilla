# Documentation Quick Reference

## Helper Scripts

### Create New ADR
```bash
doc_new_adr "decision-title"
# Example: doc_new_adr "use-docker-for-deployment"
# Creates: docs/decisions/0005-use-docker-for-deployment.md
```

### Add Changelog Entry
```bash
doc_update_changelog <category> "description"

# Categories: Added, Changed, Fixed, Breaking
# Examples:
doc_update_changelog Added "Support for Linux"
doc_update_changelog Fixed "PAT token expiration handling"
doc_update_changelog Changed "Default branch to main"
doc_update_changelog Breaking "Removed deprecated API"
```

### Check Documentation Status
```bash
doc_check          # Non-blocking check (runs in pre-commit hook)
doc_check --strict  # Fails if issues found (for CI)
```

### Create Release
```bash
doc_release 0.4.0
# Or with date:
doc_release 0.4.0 2026-01-20
```

## When to Update What

| Change | CHANGELOG | ADR | Runbook | AI Context |
|--------|-----------|-----|---------|------------|
| New feature | ✅ | Maybe | Maybe | Maybe |
| Bug fix | ✅ | No | Maybe | No |
| Breaking change | ✅ | ✅ | ✅ | ✅ |
| New script | ✅ | Maybe | ✅ | ✅ |
| Architecture decision | ✅ | ✅ | No | ✅ |
| Common issue | No | No | ✅ | ✅ |
| Workflow change | ✅ | Maybe | ✅ | ✅ |

## Typical Workflow

### During Development
```bash
# Add feature
vim apps/frontend/src/components/NewComponent.vue

# Update changelog immediately
doc_update_changelog Added "New component for X"

# Commit
git add apps/frontend/src/components/NewComponent.vue CHANGELOG.md
git commit -m "feat: add new component"
```

### Before Release
```bash
# Check status
doc_check

# Create release
doc_release 0.4.0

# Review, commit, tag
git add CHANGELOG.md
git commit -m "chore: release 0.4.0"
git tag -a v0.4.0 -m "Release 0.4.0"
```

## See Also

- **Complete guide**: `docs/DOCUMENTATION_WORKFLOW.md`
- **AI context**: `docs/ai-context.md`
- **Runbook**: `docs/runbook.md`
- **ADRs**: `docs/decisions/`
