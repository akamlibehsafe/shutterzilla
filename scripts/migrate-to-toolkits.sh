#!/bin/bash

# migrate-to-toolkits.sh
# Helps migrate from old scripts to AI Documentation Toolkits
# Usage: ./scripts/migrate-to-toolkits.sh [--dry-run]

set -e

DRY_RUN=false
if [ "$1" = "--dry-run" ]; then
    DRY_RUN=true
fi

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info() {
    echo -e "${YELLOW}$1${NC}"
}

success() {
    echo -e "${GREEN}$1${NC}"
}

warn() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd -P)"

echo ""
info "🔄 Migration to AI Documentation Toolkits"
info "=========================================="
echo ""

# Check current state
OLD_SCRIPTS=()
if [ -f "$REPO_ROOT/scripts/new-adr.sh" ]; then
    OLD_SCRIPTS+=("scripts/new-adr.sh")
fi
if [ -f "$REPO_ROOT/scripts/update-changelog.sh" ]; then
    OLD_SCRIPTS+=("scripts/update-changelog.sh")
fi
if [ -f "$REPO_ROOT/scripts/example-workflow.sh" ]; then
    OLD_SCRIPTS+=("scripts/example-workflow.sh")
fi

# Check new scripts
NEW_SCRIPTS=()
for script in doc_new_adr doc_update_changelog doc_check doc_release; do
    if [ -f "$REPO_ROOT/scripts/$script" ]; then
        NEW_SCRIPTS+=("scripts/$script")
    fi
done

echo "Current state:"
if [ ${#OLD_SCRIPTS[@]} -gt 0 ]; then
    warn "Found ${#OLD_SCRIPTS[@]} old script(s) to remove:"
    for script in "${OLD_SCRIPTS[@]}"; do
        echo "  - $script"
    done
else
    success "✓ No old scripts found"
fi

if [ ${#NEW_SCRIPTS[@]} -gt 0 ]; then
    success "✓ Found ${#NEW_SCRIPTS[@]} toolkit script(s)"
else
    warn "No toolkit scripts found. Run toolkit setup first."
    exit 1
fi

echo ""

if [ "$DRY_RUN" = true ]; then
    info "DRY RUN MODE - No files will be deleted"
    echo ""
    info "Would remove:"
    for script in "${OLD_SCRIPTS[@]}"; do
        echo "  - $script"
    done
    echo ""
    info "Run without --dry-run to actually remove files"
    exit 0
fi

# Remove old scripts
if [ ${#OLD_SCRIPTS[@]} -gt 0 ]; then
    info "Removing old scripts..."
    for script in "${OLD_SCRIPTS[@]}"; do
        if [ -f "$REPO_ROOT/$script" ]; then
            rm "$REPO_ROOT/$script"
            success "  ✓ Removed $script"
        fi
    done
else
    info "No old scripts to remove"
fi

echo ""
success "✅ Migration complete!"
echo ""
info "Next steps:"
info "  1. Test scripts: doc_check"
info "  2. Review: docs/MIGRATE_TO_TOOLKITS.md"
info "  3. Commit: git add . && git commit -m 'chore: migrate to AI documentation toolkits'"
