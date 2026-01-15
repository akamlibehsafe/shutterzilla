# Migration Guide: Moving to AI Documentation Toolkits

This guide helps you migrate from the current mixed setup to fully using the standardized AI Documentation Toolkits.

## Current Situation

You currently have:
- ✅ **New toolkit scripts**: `scripts/doc_*` (already working!)
- ⚠️ **Old scripts**: `scripts/new-adr.sh`, `scripts/update-changelog.sh` (can be removed)
- ✅ **Project content**: `CHANGELOG.md`, `docs/decisions/`, `docs/ai-context.md`, `docs/runbook.md` (keep these!)
- ✅ **Workflow docs**: `docs/QUICK_REF.md`, `docs/DOCUMENTATION_WORKFLOW.md` (from toolkit)

## Migration Steps

### Step 1: Remove Old Scripts

The old scripts are no longer needed:

```bash
# Remove old scripts
rm scripts/new-adr.sh
rm scripts/update-changelog.sh
rm scripts/example-workflow.sh  # If it exists
```

### Step 2: Verify Current Scripts Work

Test that the toolkit scripts are working:

```bash
# Test all scripts
doc_new_adr "test-migration"
doc_update_changelog Added "Testing migration"
doc_check
doc_release 0.3.0  # Use your current version

# Clean up test
rm docs/decisions/000*-test-migration.md
# Manually remove test entry from CHANGELOG.md
```

### Step 3: Verify Pre-commit Hook

Check if pre-commit hook is set up:

```bash
# Check if hook exists and works
ls -la .git/hooks/pre-commit
git commit --allow-empty -m "test: verify pre-commit hook"
```

If missing, the toolkit setup will create it.

### Step 4: Optional - Set Up Toolkit as Submodule

If you want to keep toolkits updated from your toolkit repository:

```bash
# Add development docs toolkit as submodule
git submodule add /path/to/your-toolkit-repo/ai-development-docs-toolkit .docs-toolkit

# Or if you want both toolkits
git submodule add /path/to/your-toolkit-repo .docs-toolkits
```

**Note**: You can continue using scripts directly in your project. The submodule is optional for updates.

### Step 5: Update Documentation References

Update any remaining references to old scripts:

1. **`scripts/README.md`** - Already updated ✅
2. **`docs/AUTOMATION.md`** - Update if it references old scripts
3. **`docs/QUICK-START-AUTOMATION.md`** - Update if needed
4. **`docs/MIGRATION_NOTES.md`** - Can be removed (migration complete)

### Step 6: Optional - Re-run Toolkit Setup

If you want to ensure everything aligns with the latest toolkit:

```bash
# If you have toolkit as submodule
cd .docs-toolkit/ai-development-docs-toolkit
./setup-docs.sh "ShutterZilla"

# Or if toolkit is in separate location
cd /path/to/ai-development-docs-toolkit
./setup-docs.sh "ShutterZilla"
```

**This won't overwrite your content** - it only updates scripts and ensures setup is correct.

## What to Keep

**Keep these project-specific files:**
- ✅ `CHANGELOG.md` - Your changelog history (don't lose this!)
- ✅ `docs/decisions/` - All your ADRs
- ✅ `docs/ai-context.md` - Your project context
- ✅ `docs/runbook.md` - Your operations guide
- ✅ `docs/QUICK_REF.md` - Quick reference (from toolkit, but keep your copy)
- ✅ `docs/DOCUMENTATION_WORKFLOW.md` - Workflow guide (from toolkit, but keep your copy)

## What to Remove

**Remove these old files:**
- ❌ `scripts/new-adr.sh` - Replaced by `doc_new_adr`
- ❌ `scripts/update-changelog.sh` - Replaced by `doc_update_changelog`
- ❌ `scripts/example-workflow.sh` - No longer needed
- ❌ `docs/MIGRATION_NOTES.md` - Migration complete, can remove
- ❌ `docs/STANDARDIZATION_SUMMARY.md` - Historical, can archive or remove

## What to Update

**Update these files:**

1. **`scripts/README.md`** ✅ (already updated)
   - Remove old script references
   - Add toolkit note

2. **`docs/AUTOMATION.md`**
   - Update script examples if they reference old scripts
   - Add note about toolkits

3. **`docs/QUICK-START-AUTOMATION.md`**
   - Update examples to use `doc_*` scripts
   - Remove references to old scripts

## Quick Migration (5 minutes)

```bash
# 1. Remove old scripts
rm scripts/new-adr.sh scripts/update-changelog.sh scripts/example-workflow.sh

# 2. Test new scripts work
doc_check

# 3. Commit changes
git add .
git commit -m "chore: migrate to AI documentation toolkits, remove old scripts"

# Done! ✅
```

## After Migration

### Verify Everything Works

```bash
# Test all scripts
doc_new_adr "verify-migration"
doc_update_changelog Added "Migration to toolkits complete"
doc_check
doc_release 0.3.0  # Or your next version

# Clean up
rm docs/decisions/000*-verify-migration.md
# Remove test entry from CHANGELOG.md
```

### Going Forward

**Option 1: Continue Using Scripts Directly** (Current)
- Scripts are in your project
- Works great, no changes needed
- Update manually if toolkit changes

**Option 2: Use Toolkit as Submodule** (Recommended for updates)
- Add toolkit as submodule
- Can update scripts from toolkit repo
- Still use scripts directly in project

**Option 3: Reference Toolkit for Updates**
- Keep scripts in project
- Reference toolkit docs for updates
- Copy new scripts manually when needed

## Benefits After Migration

1. **Cleaner**: No duplicate/old scripts
2. **Standardized**: Same process as other projects
3. **Maintainable**: Can update from toolkit
4. **Documented**: Complete workflow documentation
5. **Validated**: `doc_check` ensures quality

## Troubleshooting

**"Scripts not found after migration"**
- Check scripts are executable: `chmod +x scripts/doc_*`
- Verify scripts exist: `ls -la scripts/doc_*`

**"Pre-commit hook not working"**
- Check it exists: `ls -la .git/hooks/pre-commit`
- Make executable: `chmod +x .git/hooks/pre-commit`
- Re-run toolkit setup if needed

**"Want to update scripts from toolkit"**
- If using submodule: `git submodule update --remote`
- Or copy new scripts from toolkit manually

## Summary

**You're already 90% migrated!** The toolkit scripts are working. Just:

1. ✅ Remove old scripts (`new-adr.sh`, `update-changelog.sh`)
2. ✅ Update documentation references
3. ✅ Optional: Set up toolkit as submodule for updates

**Your project content (CHANGELOG, ADRs, etc.) stays exactly as is!**

See `docs/MIGRATION_CHECKLIST.md` for a quick checklist.
