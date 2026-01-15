# Monorepo Expansion Guide

This guide explains how to expand the ShutterZilla monorepo to include additional applications, particularly mobile apps, while maintaining code sharing and organization.

## Overview

The monorepo structure is designed to scale as the project grows. Currently, it contains:
- Web applications (Scraper + Collection)
- Backend API
- Scraper service

Future expansion may include:
- Separate mobile apps (Android/iOS)
- Additional web apps
- Admin panels
- Other services

## Current Structure

```
shutterzilla/
├── apps/
│   ├── frontend/          # Vue.js web app (Scraper + Collection)
│   ├── backend/           # Node.js API
│   └── scraper/           # Python scraper
├── infrastructure/
│   ├── supabase/          # Database migrations
│   └── .github/           # CI/CD workflows
└── docs/                  # Documentation
```

## Future Structure (Web + Mobile)

When mobile apps are added, the structure will expand to:

```
shutterzilla/
├── apps/
│   ├── web-scraper/       # Web Scraper app (Vue.js)
│   ├── web-collection/    # Web Collection app (Vue.js)
│   ├── mobile-scraper/   # Mobile Scraper app
│   │   ├── android/       # Android implementation
│   │   └── ios/          # iOS implementation
│   ├── mobile-collection/ # Mobile Collection app
│   │   ├── android/       # Android implementation
│   │   └── ios/          # iOS implementation
│   ├── backend/          # Shared Node.js API
│   └── scraper/          # Python scraper
│
├── packages/             # Shared code across all apps
│   ├── shared-types/     # TypeScript types (used by web + mobile)
│   ├── api-client/       # API client library (used by all apps)
│   ├── business-logic/   # Shared business rules
│   └── utils/           # Shared utilities
│
├── infrastructure/
│   ├── supabase/         # Database migrations
│   └── .github/          # CI/CD workflows
│
└── docs/                 # Documentation
```

## Why This Structure Works

### 1. Code Sharing

All apps can share:
- **Types**: Define `Camera`, `Listing`, `User` once, use everywhere
- **API Client**: One client library for all platforms
- **Business Logic**: Shared validation, calculations, formatting
- **Constants**: Shared config, enums, constants

**Example:**
```typescript
// packages/shared-types/camera.ts
export interface Camera {
  id: string;
  title: string;
  price: number;
  condition: 'excellent' | 'good' | 'fair';
  images: string[];
}

// apps/web-scraper/src/components/CameraCard.vue
import { Camera } from '../../../packages/shared-types/camera';

// apps/mobile-scraper/ios/CameraCard.swift
// Uses same Camera type definition (translated to Swift)

// apps/backend/api/cameras.ts
import { Camera } from '../../../packages/shared-types/camera';
```

### 2. Unified Versioning

- **Single commit** can update web + mobile together
- **Example**: Add new camera field → update types, web UI, mobile UI, API in one commit
- **Atomic changes**: Related changes stay together

### 3. Single CI/CD

- One GitHub Actions workflow can:
  - Build and test all apps
  - Deploy web apps
  - Build mobile app binaries
  - Run tests across all platforms

### 4. Consistent Experience

- Same data models across all platforms
- Same API contracts
- Easier to keep features in sync
- Consistent business logic

## Real-World Examples

This pattern is used by major companies:

- **Google**: Docs, Sheets, Slides (web + mobile) share code
- **Microsoft**: Office suite apps in monorepos
- **Meta**: Facebook, Instagram apps share infrastructure
- **Airbnb**: Web + iOS + Android in monorepos

## Your Specific Case: Google Docs/Photos Pattern

Like Google's approach:
- **Web**: Separate apps (Scraper app, Collection app) - see ADR 0020
- **Mobile**: Separate apps (Scraper app, Collection app, Negativa app)
- **Shared**: Same backend API, same data models, same business logic
- **Mobile Framework**: React Native (see ADR 0020 and React Native guide)

### Recommended Structure for Your Case

```
apps/
├── web-scraper/           # Vue.js Scraper app
├── web-collection/        # Vue.js Collection app
├── mobile-scraper/        # React Native (iOS + Android)
│   ├── src/               # Shared React Native code
│   ├── android/           # Android config only
│   └── ios/               # iOS config only
├── mobile-collection/     # React Native (iOS + Android)
│   ├── src/
│   ├── android/
│   └── ios/
├── mobile-negativa/       # React Native (iOS + Android) - Camera/EXIF app
│   ├── src/
│   ├── android/
│   └── ios/
├── app-switcher/          # Web landing/switcher
└── backend/               # Shared API

packages/
├── shared-types/          # Camera, Listing, etc. types
├── api-client/            # Supabase client wrapper
└── business-logic/        # Validation, calculations
```

**Note**: Mobile apps use React Native (single codebase for iOS + Android). See `docs/guides/react-native-mobile-development.md` for details.

## How to Add a New App

### Step 1: Create App Folder

```bash
mkdir -p apps/mobile-scraper/android
mkdir -p apps/mobile-scraper/ios
```

### Step 2: Set Up Shared Packages

```bash
mkdir -p packages/shared-types
mkdir -p packages/api-client
```

### Step 3: Extract Shared Code

Move common code from existing apps to `packages/`:
- Types → `packages/shared-types/`
- API client → `packages/api-client/`
- Utilities → `packages/utils/`

### Step 4: Update Imports

Update all apps to import from `packages/`:
```typescript
// Before
import { Camera } from '../types/camera';

// After
import { Camera } from '../../../packages/shared-types/camera';
```

### Step 5: Update CI/CD

Add build steps for new apps in `.github/workflows/`:
```yaml
- name: Build Android App
  run: cd apps/mobile-scraper/android && ./gradlew build

- name: Build iOS App
  run: cd apps/mobile-scraper/ios && xcodebuild
```

## Benefits for Future Growth

1. **Easy to add mobile apps**: Just create new folders
2. **Code reuse**: Share types, API client, business logic
3. **Keep in sync**: Update camera model once, all apps benefit
4. **Unified releases**: Release web + mobile features together
5. **Easier maintenance**: One place to fix bugs, one place to add features

## Best Practices

### 1. Keep Shared Code in `packages/`

- Don't duplicate code across apps
- Extract common functionality to `packages/`
- All apps import from shared packages

### 2. Platform-Specific Code Stays in Apps

- UI components are platform-specific
- Platform APIs (camera, notifications) stay in app folders
- Only business logic and types are shared

### 3. Version Together

- When adding a feature, update all relevant apps
- Keep API contracts consistent
- Use same version numbers across apps

### 4. Test Across Platforms

- CI/CD should test all apps
- Shared code should have tests
- Platform-specific code has platform-specific tests

## Migration Path

When you're ready to add mobile apps:

1. **Phase 1**: Extract shared code to `packages/`
   - Move types to `packages/shared-types/`
   - Create `packages/api-client/`
   - Update web app to use shared packages

2. **Phase 2**: Create mobile app structure
   - Create `apps/mobile-scraper/` and `apps/mobile-collection/`
   - Set up Android and iOS projects
   - Import shared packages

3. **Phase 3**: Implement mobile apps
   - Use shared API client
   - Use shared types (translated to native types)
   - Implement platform-specific UI

4. **Phase 4**: Update CI/CD
   - Add mobile build steps
   - Add mobile tests
   - Set up mobile deployment

## Related Documentation

- **ADR 0019**: Monorepo structure decision
- **ADR 0020**: React Native for mobile apps decision
- **ADR 0002**: Separate apps decision
- **React Native Guide**: `docs/guides/react-native-mobile-development.md`
- **Folder Structure**: `docs/specification/functional/functional-folder-structure.md`
- **Tech Stack**: `docs/specification/technical/tech-stack-final.md`

---

**Last Updated:** 2026-01-XX  
**Status:** Planning document for future expansion
