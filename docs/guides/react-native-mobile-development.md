# React Native Mobile Development Guide

This guide documents the decision-making process, considerations, and practical information about using React Native for ShutterZilla mobile apps.

## Overview

ShutterZilla mobile apps will be built using **React Native**, a cross-platform framework that allows building iOS and Android apps from a single codebase using JavaScript/TypeScript.

## Decision Summary

**Decision**: Use React Native for all mobile app development  
**Status**: Accepted  
**ADR**: [0020 - Use React Native for Mobile Apps](../project/decisions/0020-use-react-native-for-mobile-apps.md)

## Why React Native?

### 1. Code Sharing

React Native enables significant code sharing with web apps:

- **TypeScript types**: Same type definitions across web and mobile
- **API client**: Shared API client library
- **Business logic**: Shared validation, calculations, formatting
- **Constants**: Shared config, enums

**Example:**
```typescript
// packages/shared-types/camera.ts (used by web + mobile)
export interface Camera {
  id: string;
  title: string;
  price: number;
  condition: 'excellent' | 'good' | 'fair';
  images: string[];
}

// apps/web-scraper/src/components/CameraCard.vue
import { Camera } from '../../../packages/shared-types/camera';

// apps/mobile-scraper/src/components/CameraCard.tsx
import { Camera } from '../../../packages/shared-types/camera';
```

### 2. Single Codebase

- One React Native app builds for both iOS and Android
- Faster development (write once, deploy to both platforms)
- Easier maintenance (one codebase to update)
- Consistent features across platforms

### 3. Performance

For ShutterZilla's use cases (marketplace, collection management, camera/EXIF), React Native performance is **sufficient**:

- **Lists**: Optimized with `FlatList`/`FlashList` (standard practice)
- **Images**: Well-supported with optimized libraries
- **Forms**: Standard, performs well
- **Navigation**: Smooth with React Navigation
- **Camera**: Native performance (uses native camera APIs)

**Real-world validation**: Major apps like Instagram, Facebook, Discord use React Native successfully.

### 4. Camera and EXIF Support

React Native has excellent support for camera and EXIF data:

**Camera Libraries:**
- `react-native-vision-camera` - Full camera control, photo/video
- `expo-camera` - Simpler API (if using Expo)

**EXIF Libraries:**
- `@lodev09/react-native-exify` - Read and write EXIF (recommended)
- `react-native-exif-reader` - Native modules for GPS/date
- `exifreader` - Pure JavaScript (supports many formats)

**Example for Negativa App:**
```typescript
// Take photo
import { Camera } from 'react-native-vision-camera';
const photo = await camera.takePhoto({ quality: 100 });

// Extract EXIF
import { readExif } from '@lodev09/react-native-exify';
const exifData = await readExif(photo.path);
// Returns: GPS, DateTime, Camera make/model, ISO, aperture, etc.
```

## Performance Considerations

### What React Native Handles Well

✅ **Standard business apps** (90% of apps):
- Lists and feeds
- Forms and data entry
- Navigation between screens
- API calls and data fetching
- Image galleries
- Search and filters

✅ **ShutterZilla's use cases**:
- Marketplace listings (Scraper app)
- Collection management (Collection app)
- Camera access and EXIF (Negativa app)

### Performance Limitations

⚠️ **Edge cases where native might be better**:
- Real-time AR/VR
- Heavy gaming
- Very low-end devices (budget Android)
- Ultra-demanding animations (100+ simultaneous)
- Maximum performance requirements

**For ShutterZilla**: These limitations don't apply. Our apps are standard business apps, not games or AR apps.

### Performance Improvements (2024-2025)

React Native has evolved significantly:
- **Hermes JavaScript engine**: Faster startup, better memory
- **New Architecture**: Fabric renderer, TurboModules, JSI - reduces bridge overhead
- **Optimized libraries**: Better list components, native thread animations

## Functionality: What You Keep vs Lose

### ✅ What You Keep (95% of functionality)

**Performance:**
- Good enough for most apps
- Near-native feel with optimization
- Modern improvements close gaps

**Looks:**
- Can look native with proper styling
- Platform-specific components available
- Examples: Instagram, Facebook, Airbnb look native

**Functionality:**
- Camera access ✅
- Push notifications ✅
- Location services ✅
- File system ✅
- Biometric auth ✅
- Most APIs available via libraries

### ⚠️ What You Lose (Minor limitations)

**Performance edge cases:**
- Startup time: 1.5-2x slower (loading JS bundle)
- Heavy animations: May drop frames in complex UIs
- Large lists: Need careful optimization (1000+ items)
- Low-end devices: Budget Android may show more lag

**Platform features:**
- New OS features: May not have RN wrappers immediately
- Deep platform integration: Some advanced APIs need custom native modules
- App size: 10-20MB larger than minimal native apps

**For ShutterZilla**: These limitations are acceptable trade-offs for faster development and easier maintenance.

## Real-World Examples

### Major Apps Using React Native

**Download and test these on Android to see quality:**

1. **Instagram** (Meta)
   - Camera features, Stories, messaging
   - Heavy React Native usage
   - Smooth performance

2. **Facebook**
   - Creator of React Native
   - Extensive usage

3. **Discord**
   - Real-time messaging, voice/video
   - Complex UI, smooth performance

4. **Pinterest**
   - Image-heavy feeds
   - Good for image performance validation

5. **Walmart**
   - E-commerce features
   - Good for marketplace app reference

6. **Uber Eats**
   - Real-time updates, maps
   - Restaurant dashboard

7. **Coinbase**
   - Financial app
   - Migrated to React Native, performance improvements

8. **Kraken**
   - Crypto trading
   - Recently upgraded to New Architecture (2.5x faster)

### What to Look For When Testing

- **Performance**: Launch speed, scroll smoothness, animations
- **UI/UX**: Native feel, Material Design compliance, gestures
- **Features**: Camera, real-time updates, complex UI

## Migration Considerations

### If You Need to Switch to Native Later

**What would be reusable:**
- ✅ Business logic (TypeScript → Swift/Kotlin translation)
- ✅ API client structure (contracts stay same)
- ✅ Types/Models (structure reusable, code rewritten)
- ✅ Design/UX (mockups, wireframes)

**What would need complete rewrite:**
- ❌ **UI components** (80-90% of effort)
  - Every screen, component, layout
  - Navigation system
  - Animations, gestures
  - Platform-specific styling

- ❌ State management (different patterns)
- ❌ Navigation (different systems)
- ❌ Platform-specific code

**Effort estimate:**
- Small app (5-10 screens): 2-4 months
- Medium app (20-30 screens): 4-8 months
- Large app (50+ screens): 8-12+ months

**UI recreation with AI assistance:**
- Can help significantly with UI recreation
- Component-by-component translation
- Screen-by-screen recreation
- Platform-specific optimizations
- Still requires testing, refinement, platform decisions

**Bottom line**: Migration is possible but significant work. Better to choose the right approach upfront.

## Project Structure

### Mobile Apps in Monorepo

```
apps/
├── web-scraper/          # Vue.js web app
├── web-collection/       # Vue.js web app
├── mobile-scraper/       # React Native (iOS + Android)
│   ├── src/              # Shared React Native code
│   ├── android/          # Android config only
│   └── ios/              # iOS config only
├── mobile-collection/    # React Native (iOS + Android)
│   ├── src/
│   ├── android/
│   └── ios/
├── mobile-negativa/      # React Native (iOS + Android)
│   ├── src/
│   ├── android/
│   └── ios/
└── app-switcher/         # Web landing/switcher

packages/
├── shared-types/         # TypeScript types (all apps)
├── api-client/          # API client (all apps)
└── business-logic/      # Shared logic
```

### Per-App Access Control

Separate apps enable easier per-app access control:

```typescript
// App Switcher checks permissions
const userApps = getUserAccessibleApps(user);
// Returns: ['scraper'] or ['collection'] or ['scraper', 'collection']

// Each app checks access
router.beforeEach((to, from, next) => {
  if (!hasAccessToApp(user, 'scraper')) {
    redirectToAppSwitcher();
  }
});
```

## Recommended Libraries

### Core
- **React Native**: Core framework
- **TypeScript**: Type safety
- **React Navigation**: Navigation

### Camera & EXIF (for Negativa app)
- **react-native-vision-camera**: Camera access
- **@lodev09/react-native-exify**: EXIF read/write

### UI & Styling
- **React Native Reanimated**: Smooth animations
- **React Native Gesture Handler**: Gesture handling
- Platform-specific styling for native look

### State Management
- **Zustand** or **Redux Toolkit**: State management
- **React Query**: API data fetching

### Lists & Performance
- **FlashList**: Optimized list component
- **react-native-fast-image**: Optimized image loading

## Best Practices

### 1. Extract Shared Code Early

Move common code to `packages/`:
- Types → `packages/shared-types/`
- API client → `packages/api-client/`
- Business logic → `packages/business-logic/`

### 2. Platform-Specific Code

Use platform-specific files when needed:
```typescript
// Component.ios.tsx
// Component.android.tsx
// Component.tsx (shared)
```

### 3. Performance Optimization

- Use `FlashList` for long lists
- Optimize images (lazy loading, caching)
- Use native thread animations (Reanimated)
- Profile and optimize bottlenecks

### 4. Native Modules

For advanced features, create custom native modules:
- Bridge to native APIs
- Platform-specific functionality
- Performance-critical code

## Related Documentation

- **ADR 0020**: React Native decision
- **ADR 0019**: Monorepo structure
- **ADR 0002**: Separate apps decision
- **Monorepo Expansion Guide**: `docs/guides/monorepo-expansion.md`
- **Folder Structure**: `docs/specification/functional/functional-folder-structure.md`

## Resources

### Official Documentation
- [React Native Docs](https://reactnative.dev/)
- [React Native Vision Camera](https://react-native-vision-camera.com/)
- [React Navigation](https://reactnavigation.org/)

### Libraries
- [@lodev09/react-native-exify](https://github.com/lodev09/react-native-exify) - EXIF library
- [React Native Reanimated](https://docs.swmansion.com/react-native-reanimated/) - Animations
- [FlashList](https://shopify.github.io/flash-list/) - Optimized lists

---

**Last Updated:** 2026-01-XX  
**Status:** Active development guide
