# Scripts

Helper scripts for maintaining project documentation.

## Available Scripts

### `doc_new_adr`
Creates a new Architecture Decision Record (ADR) in `docs/project/decisions/`.

**Usage:**
```bash
doc_new_adr "use-docker-for-deployment"
```

Creates a new ADR file with the next sequential number (e.g., `0007-use-docker-for-deployment.md`) and opens it for editing.

### `doc_update_changelog`
Adds entries to `CHANGELOG.md`.

**Usage:**
```bash
# Add to Unreleased section
doc_update_changelog Added "New feature description"
doc_update_changelog Fixed "Bug fix description"
doc_update_changelog Changed "Behavior change description"
doc_update_changelog Breaking "Breaking change description"
```

**Categories:** `Added`, `Changed`, `Fixed`, `Breaking`

### `doc_check`
Checks documentation status and reminds about updates.

**Usage:**
```bash
doc_check          # Non-blocking check (runs in pre-commit hook)
doc_check --strict # Fails if issues found (for CI)
```

**Checks:**
- CHANGELOG has unreleased entries
- Proposed ADRs exist
- Key files exist (ai-context.md, runbook.md)
- Recent commits without changelog entries

### `doc_release`
Moves unreleased changelog entries to a new version.

**Usage:**
```bash
doc_release 0.4.0
# Or with date:
doc_release 0.4.0 2026-01-20
```

## Setup

Make sure scripts are executable:
```bash
chmod +x scripts/doc_*
```

## Pre-commit Hook

The pre-commit hook automatically runs `doc_check` before every commit (non-blocking reminder).

**To disable:**
```bash
mv .git/hooks/pre-commit .git/hooks/pre-commit.disabled
```

## See Also

- **Quick Reference**: `docs/guides/quick-reference.md` - Quick command reference
- **Complete Workflow**: `docs/guides/documentation-workflow.md` - Detailed workflow guide
- **AI Context**: `docs/project/ai-context.md` - Briefing for AI assistants
- **Runbook**: `docs/project/runbook.md` - Operations guide
- **ADRs**: `docs/project/decisions/` - Architecture Decision Records
- **Changelog**: `CHANGELOG.md` - User-facing changelog

## Using AI Documentation Toolkits

These scripts are part of the **AI Development Documentation Toolkit**. 

- **Toolkit repository**: See your toolkit repo for updates
- **Documentation**: See `docs/QUICK_REF.md` and `docs/DOCUMENTATION_WORKFLOW.md`
- **Migration guide**: See `docs/MIGRATE_TO_TOOLKITS.md` for moving from old scripts

## Migration Status

✅ **Migration complete!** Old scripts have been removed. You're now using the AI Development Documentation Toolkit.

- ✅ Using `doc_new_adr` for ADRs
- ✅ Using `doc_update_changelog` for changelog entries
- ✅ Using `doc_check` for validation
- ✅ Using `doc_release` for releases

See `docs/MIGRATE_TO_TOOLKITS.md` for migration details (already completed).
