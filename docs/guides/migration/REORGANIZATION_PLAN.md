# Documentation Reorganization Plan

## Current Issues

1. **Too many files at `docs/` root** - 10+ markdown files mixed together
2. **Unclear separation** - Process docs (automation, workflow) mixed with project docs (specs, decisions)
3. **Mockup versions** - Two versions (v1/v2) could be better organized
4. **Specification folder** - Many files without clear categorization
5. **Migration docs** - Temporary migration docs should be archived

## Proposed Structure

```
docs/
├── README.md                    # Main index (updated)
│
├── guides/                      # Process & workflow documentation
│   ├── automation.md            # How to automate docs
│   ├── quick-reference.md       # Quick command reference
│   ├── documentation-workflow.md # Complete workflow guide
│   └── migration/               # Migration docs (archive)
│       ├── migrate-to-toolkits.md
│       ├── migration-checklist.md
│       └── migration-complete.md
│
├── project/                     # Project-specific documentation
│   ├── ai-context.md            # AI/contributor briefing
│   ├── runbook.md               # Operations guide
│   ├── decisions/               # ADRs (moved from docs/decisions/)
│   │   └── *.md
│   └── releases/                # Release notes
│       └── release-notes-v0.2.md
│
├── specification/               # Technical specifications
│   ├── design/                  # Design-related specs
│   │   ├── design-system.md
│   │   ├── component-library.md
│   │   └── page-inventory.md
│   ├── technical/               # Technical specs
│   │   ├── tech-stack-guide.md
│   │   ├── tech-stack-final.md
│   │   ├── data-models.md
│   │   └── folder-structure.md
│   ├── implementation/          # Implementation docs
│   │   ├── implementation-plan.md
│   │   ├── implementation-notes.md
│   │   ├── implementation-*.md (all other impl docs)
│   │   └── key-decisions-log.md
│   └── functional/              # Functional specs
│       └── functional-requirements.md
│
├── mockups/                     # Design mockups
│   ├── current/                 # v2 (active)
│   │   └── (all v2 files)
│   └── archive/                 # v1 (preserved)
│       └── (all v1 files)
│
└── assets/                      # Branding & assets
    └── branding/                # (existing)
```

## File Moves

### From `docs/` root → `docs/guides/`
- `AUTOMATION.md` → `guides/automation.md`
- `QUICK_REF.md` → `guides/quick-reference.md`
- `DOCUMENTATION_WORKFLOW.md` → `guides/documentation-workflow.md`
- `QUICK-START-AUTOMATION.md` → `guides/quick-start-automation.md`

### From `docs/` root → `docs/guides/migration/`
- `MIGRATE_TO_TOOLKITS.md` → `guides/migration/migrate-to-toolkits.md`
- `MIGRATION_CHECKLIST.md` → `guides/migration/migration-checklist.md`
- `MIGRATION_COMPLETE.md` → `guides/migration/migration-complete.md`
- `MIGRATION_SUMMARY.md` → `guides/migration/migration-summary.md`
- `TOOLKIT_MIGRATION_SUMMARY.md` → `guides/migration/toolkit-migration-summary.md`

### From `docs/` root → `docs/project/`
- `ai-context.md` → `project/ai-context.md`
- `runbook.md` → `project/runbook.md`
- `release-notes-v0.2.md` → `project/releases/release-notes-v0.2.md`

### From `docs/decisions/` → `docs/project/decisions/`
- All ADR files (0001-*.md, etc.)

### From `docs/specification/` → `docs/specification/design/`
- `design-system.md`
- `component-library.md`
- `page-inventory.md`

### From `docs/specification/` → `docs/specification/technical/`
- `tech-stack-guide.md`
- `tech-stack-final.md`
- `data-models.md`
- `folder-structure.md`

### From `docs/specification/` → `docs/specification/implementation/`
- `implementation-*.md` (all files)
- `key-decisions-log.md`

### From `docs/specification/` → `docs/specification/functional/`
- `functional-requirements.md`

### Mockups
- `docs/mockupsv2/` → `docs/mockups/current/`
- `docs/mockupsv1/` → `docs/mockups/archive/`

## Benefits

1. **Clear separation**: Process docs vs. project docs
2. **Better discoverability**: Logical grouping
3. **Easier navigation**: Fewer files at root
4. **Scalability**: Easy to add new docs in right place
5. **Cleaner root**: Only README.md at docs root

## Implementation Steps

1. Create new folder structure
2. Move files to new locations
3. Update all internal links
4. Update README.md and other index files
5. Update references in root README.md
6. Test all links work

## Notes

- Keep `docs/README.md` as main index
- Update all cross-references
- Consider symlinks if needed for backward compatibility (not recommended)
- Archive old structure in git history
