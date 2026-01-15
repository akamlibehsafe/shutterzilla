# Mockup Versioning Strategy

## Current Structure

```
docs/mockups/
├── current/     # v2 - Mobile-responsive (active)
└── archive/    # v1 - Original desktop (preserved)
```

## Problem

As the project evolves, there may be more than two versions:
- v1: Original desktop mockups
- v2: Mobile-responsive mockups (current)
- v3: Future version (e.g., updated design system, new features)
- v4+: Additional versions as needed

The current `current/` + `archive/` structure doesn't scale well for multiple versions.

## Recommended Solution: Versioned Folders

### Structure

```
docs/mockups/
├── current/          # Always the latest active version (symlink or copy)
├── v1/              # Original desktop mockups (archived)
├── v2/              # Mobile-responsive mockups (archived)
├── v3/              # Future version (archived)
└── ...              # Additional versions as needed
```

### Benefits

✅ **Preserves all versions**: Every version is kept and accessible  
✅ **Easy reference**: Can link to specific versions (`docs/mockups/v2/`)  
✅ **Scalable**: Works for any number of versions  
✅ **Clear naming**: Version numbers make it obvious which is which  
✅ **Current always available**: `current/` always points to latest  

## Migration Strategy

When a new version (v3) is created:

1. **Archive current version**:
   ```bash
   mv docs/mockups/current docs/mockups/v2
   ```

2. **Set new version as current**:
   ```bash
   cp -r docs/mockups/v3 docs/mockups/current
   # Or if v3 is already created elsewhere:
   mv path/to/v3 docs/mockups/current
   ```

3. **Update links** in `docs/pages/index.html`:
   - Keep `docs/mockups/current/` for latest
   - Update specific version links if needed

## Alternative: Nested Archive Structure

If you prefer keeping archive separate:

```
docs/mockups/
├── current/          # Latest version
└── archive/          # All archived versions
    ├── v1/          # Original desktop
    ├── v2/          # Mobile-responsive
    └── v3/          # Future versions
```

**Pros**: Keeps archive organized  
**Cons**: Longer paths (`docs/mockups/archive/v2/`) - Note: This structure is not recommended, use versioned folders instead

## Recommendation

**Use versioned folders directly under `mockups/`**:
- `docs/mockups/current/` - Latest active version
- `docs/mockups/v1/` - Version 1 (archived)
- `docs/mockups/v2/` - Version 2 (archived)
- `docs/mockups/v3/` - Version 3 (archived)
- etc.

This approach:
- ✅ Simplest structure
- ✅ Easiest to navigate
- ✅ Preserves all versions
- ✅ Easy to reference specific versions
- ✅ Scales infinitely

## Implementation Steps

When creating v3:

1. Create new version: `docs/mockups/v3/`
2. Archive v2: `mv docs/mockups/current docs/mockups/v2`
3. Set v3 as current: `cp -r docs/mockups/v3 docs/mockups/current` (or move if v3 was created elsewhere)
4. Update documentation to reference new structure
5. Update `docs/pages/index.html` links if needed

## Link Strategy

### In Documentation

- **Latest version**: Always use `docs/mockups/current/`
- **Specific version**: Use `docs/mockups/v2/` for version-specific references
- **Historical reference**: Use versioned paths (`docs/mockups/v1/`)

### In index.html

- **Primary link**: `docs/mockups/current/` (always points to latest)
- **Version links**: Optional links to specific versions if needed

## Version Naming Convention

- **v1, v2, v3, etc.**: Sequential version numbers
- **Descriptive names**: Consider adding README in each version folder describing what changed
- **Current**: Always the latest version

## Example: Adding v3

```
# Current state
docs/mockups/
├── current/  (v2 content)
└── archive/  (v1 content)

# Step 1: Rename archive to v1 (already done)
# mv docs/mockups/archive docs/mockups/v1

# Step 2: Rename current to v2
mv docs/mockups/current docs/mockups/v2

# Step 3: Create v3
# (create new mockups in v3 folder)

# Step 4: Set v3 as current
cp -r docs/mockups/v3 docs/mockups/current
# Or if v3 is ready:
mv docs/mockups/v3 docs/mockups/current
# Then recreate v3 as archive:
cp -r docs/mockups/current docs/mockups/v3
```

## Future Considerations

- **Version metadata**: Consider adding `VERSION.md` in each version folder describing changes
- **Breaking changes**: Document major changes between versions
- **Deprecation**: Mark old versions as deprecated but keep them accessible

---

**Recommendation**: Migrate to versioned folder structure (`v1/`, `v2/`, `current/`) for better scalability.
