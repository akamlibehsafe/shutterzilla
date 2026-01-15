# Link Updates for GitHub Pages

## Status

After moving files to `docs/pages/`, links may need updating depending on how GitHub Pages serves the files.

## Current Setup

The workflow copies:
- `docs/pages/*` → `_pages/` (root of Pages site)
- `docs/` → `_pages/docs/` (documentation accessible)

## Link Behavior

Since `index.html` is copied to the root of the Pages site, links should work as-is:
- `docs/mockups/current/` → Works (latest version, docs folder is copied)
- `docs/mockups/v1/` → Works (version 1, archived)
- `docs/mockups/v2/` → Works (version 2, when archived)
- `docs/README.md` → Works
- Relative paths → Work correctly

## Testing

After deployment, verify:
1. ✅ `index.html` loads correctly
2. ✅ Links to `docs/mockups/` work
3. ✅ Links to documentation work
4. ✅ `presentation.html` works (if used)

## If Links Break

If links don't work after deployment, update paths in `index.html`:
- Keep relative paths (they'll resolve from Pages root)
- Ensure `docs/` folder references are correct
