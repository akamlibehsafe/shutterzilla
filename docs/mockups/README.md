# Mockups

This folder contains all design mockup versions for the ShutterZilla project.

## Structure

```
docs/mockups/
├── current/          # Latest active version (currently v2)
├── v1/              # Version 1 - Original desktop mockups (archived)
├── v2/              # Version 2 - Mobile-responsive mockups (archived, when v3 is created)
└── VERSIONING_STRATEGY.md  # Versioning strategy documentation
```

## Current Versions

- **current/** - Version 2 (Mobile-responsive) - Active for development
- **v1/** - Version 1 (Original desktop) - Archived for reference

## Versioning Strategy

When a new version is created:

1. **Archive current version**: Rename `current/` to `v2/` (or next version number)
2. **Set new version as current**: Create new version and set as `current/`
3. **Update links**: Update documentation links if needed

Example when creating v3:
```bash
# Archive current (v2)
mv docs/mockups/current docs/mockups/v2

# Create v3 and set as current
# (create v3 mockups)
cp -r path/to/v3 docs/mockups/current
```

## Benefits

✅ **Preserves all versions**: Every version is kept and accessible  
✅ **Easy reference**: Can link to specific versions (`docs/mockups/v2/`)  
✅ **Scalable**: Works for any number of versions  
✅ **Current always available**: `current/` always points to latest  

## Usage

- **For development**: Always use `docs/mockups/current/` (latest version)
- **For specific version**: Use `docs/mockups/v1/`, `docs/mockups/v2/`, etc.
- **For historical reference**: Use versioned paths

## Version History

- **v1**: Original desktop-focused mockups (26 pages)
- **v2**: Mobile-responsive mockups (26 pages) - Currently active

See [VERSIONING_STRATEGY.md](./VERSIONING_STRATEGY.md) for detailed versioning strategy.
