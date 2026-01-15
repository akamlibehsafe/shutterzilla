# 0020 - Use React Native for Mobile Apps

## Status
Accepted

## Context
Future mobile app development requires choosing between:
- **Native development**: Separate iOS (Swift) and Android (Kotlin/Java) codebases
- **Cross-platform framework**: Single codebase for both platforms (React Native, Flutter, etc.)

Requirements for mobile apps:
- **Scraper App**: Lists, search, filters, image galleries
- **Collection App**: Forms, data management, statistics
- **Negativa App**: Camera access, EXIF data extraction, image processing
- Per-app access control (different users may have access to different apps)
- Code sharing with web apps (types, API client, business logic)
- Maintainable codebase (solo dev + AI workflow)

## Decision
Use **React Native** for all mobile app development (iOS and Android). Mobile apps will be separate React Native applications in the monorepo:
- `apps/mobile-scraper/` - React Native app
- `apps/mobile-collection/` - React Native app
- `apps/mobile-negativa/` - React Native app

## Alternatives considered
- **Native iOS + Android (separate codebases)**: Pros - maximum performance, full platform features, native look/feel. Cons - two codebases to maintain, slower development, harder code sharing, more expensive
- **Flutter**: Pros - good performance, single codebase. Cons - different language (Dart), less code sharing with web (TypeScript), smaller ecosystem
- **React Native**: Pros - single codebase for iOS+Android, excellent code sharing with web (TypeScript), large ecosystem, good performance for business apps, camera/EXIF support, easier maintenance, faster development. Cons - slightly larger app size, some performance edge cases (acceptable for this use case)

## Consequences
- **Single codebase per app**: One React Native app builds for both iOS and Android
- **Code sharing**: TypeScript types, API client, business logic shared with web apps via `packages/`
- **Faster development**: One codebase to write and maintain
- **Good performance**: Sufficient for marketplace, collection, and camera apps (validated by major apps like Instagram, Discord, Facebook)
- **Camera/EXIF support**: Well-supported via libraries (react-native-vision-camera, @lodev09/react-native-exify)
- **Per-app access control**: Easier to implement with separate apps
- **Native feel**: Can achieve native look/feel with proper styling and platform-specific components
- **Migration path**: If native needed later, UI would need recreation (but business logic, types, API contracts reusable)

## Real-World Validation
Major apps using React Native successfully:
- Instagram (Meta) - Camera features, Stories, messaging
- Facebook - Core app features
- Discord - Real-time messaging, voice/video
- Pinterest - Image-heavy feeds
- Walmart - E-commerce
- Uber Eats - Real-time updates, maps
- Coinbase - Financial app
- Kraken - Crypto trading (2.5x performance improvement with New Architecture)

## Links
- Monorepo Structure: ADR 0019
- Separate Apps Decision: ADR 0002
- Monorepo Expansion Guide: `docs/guides/monorepo-expansion.md`
- React Native Mobile Guide: `docs/guides/react-native-mobile-development.md`
