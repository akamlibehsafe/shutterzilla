# Migration Checklist: Moving to Toolkits

Quick checklist to migrate from current setup to using AI Documentation Toolkits.

## ✅ Pre-Migration Check

- [ ] Verify current scripts work: `doc_new_adr`, `doc_update_changelog`, `doc_check`, `doc_release`
- [ ] Backup current state: `git commit -am "Backup before toolkit migration"`
- [ ] Note location of toolkit repository (if using submodule)

## 🗑️ Remove Old Files

- [ ] Remove `scripts/new-adr.sh`
- [ ] Remove `scripts/update-changelog.sh`
- [ ] Remove `scripts/example-workflow.sh` (if exists)
- [ ] Remove `docs/MIGRATION_NOTES.md` (migration complete)
- [ ] Remove `docs/STANDARDIZATION_SUMMARY.md` (can archive)

## 📝 Update Documentation

- [ ] Update `scripts/README.md` - Remove old script references
- [ ] Update `docs/AUTOMATION.md` - Reference toolkits
- [ ] Update `docs/QUICK-START-AUTOMATION.md` - Update examples
- [ ] Update `docs/ai-context.md` - Add toolkit reference (optional)
- [ ] Update `README.md` - Add toolkit note (optional)

## ✅ Verify Setup

- [ ] Test `doc_new_adr "test"`
- [ ] Test `doc_update_changelog Added "test"`
- [ ] Test `doc_check`
- [ ] Test `doc_release 0.3.0` (or current version)
- [ ] Verify pre-commit hook runs: `git commit --allow-empty -m "test"`
- [ ] Clean up test files

## 🔄 Optional: Re-run Toolkit Setup

If you want to ensure alignment with latest toolkit:

- [ ] Locate toolkit: `/path/to/ai-development-docs-toolkit`
- [ ] Run setup: `./setup-docs.sh "ShutterZilla"`
- [ ] Verify no content was overwritten
- [ ] Test scripts still work

## 📋 What to Keep

**Keep these (they're your project content):**
- ✅ `CHANGELOG.md`
- ✅ `docs/decisions/` (all ADRs)
- ✅ `docs/ai-context.md`
- ✅ `docs/runbook.md`
- ✅ `docs/QUICK_REF.md`
- ✅ `docs/DOCUMENTATION_WORKFLOW.md`

## 🎯 After Migration

- [ ] Commit changes: `git add . && git commit -m "Migrate to AI documentation toolkits"`
- [ ] Update team/docs about toolkit usage
- [ ] Consider adding toolkit as submodule for future updates

## ✅ Done!

You're now using the standardized AI Documentation Toolkits!

**See `docs/MIGRATE_TO_TOOLKITS.md` for detailed migration guide.**
