# Vercel Build Control

This project uses `vercel.json` to control when Vercel builds and deploys the application.

## Current Status: Builds Disabled

Builds are currently **disabled** because the app is not ready for deployment yet.

## How It Works

The `vercel.json` file contains an `ignoreCommand` that Vercel runs before each build:
- **Exit code `0`** → Build is **skipped** (deployment canceled)
- **Exit code `1` (or non-zero)** → Build **proceeds** (deployment continues)

**Note:** This is counterintuitive! Exit 0 usually means "success", but in Vercel's `ignoreCommand`, exit 0 means "skip this build".

## Enabling Builds

When the app is ready for deployment, you have two options:

### Option 1: Enable Builds (Change exit code)
Edit `vercel.json` and change `exit 0` to `exit 1`:

```json
{
  "ignoreCommand": "exit 1"
}
```

Or remove the `ignoreCommand` line entirely.

### Option 2: Remove Build Control (Delete file)
Simply delete `vercel.json` to allow all builds.

## Advanced: Conditional Builds

You can make builds conditional. See `docs/guides/vercel-build-control.md` for examples:
- Build only on specific branches
- Build only when environment variable is set
- Build only when marker file exists

## Documentation

For more details, see: `docs/guides/vercel-build-control.md`
