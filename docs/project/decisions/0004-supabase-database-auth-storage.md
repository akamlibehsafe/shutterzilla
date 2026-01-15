# 0004 - Use Supabase for Database, Auth, and Storage

## Status
Accepted

## Context
Need to choose infrastructure for:
- Database (PostgreSQL preferred for relational data)
- Authentication (email/password + OAuth)
- File storage (user-uploaded camera photos)

Constraints:
- Must be free tier for initial 10 users
- Should minimize number of services to manage
- Should work well with Vercel hosting
- Need easy setup for solo dev workflow

## Decision
Use Supabase for all three: PostgreSQL database, built-in authentication (email/password + OAuth), and file storage in a single service.

## Alternatives considered
- **Firebase**: Pros - Google-backed, real-time features. Cons - NoSQL (need SQL for this project), more expensive, different mental model
- **Separate services (Postgres + Auth0 + S3)**: Pros - best-of-breed. Cons - three services to manage, three billing accounts, more complex setup, higher cost
- **PlanetScale + Clerk + Cloudinary**: Pros - modern stack. Cons - three services, more setup complexity
- **Supabase**: Pros - all-in-one, PostgreSQL (familiar), built-in auth, storage included, excellent free tier, great docs. Cons - newer than Firebase (but mature enough)

## Consequences
- Single service to manage (simpler operations)
- PostgreSQL database (familiar, powerful)
- Built-in auth with OAuth support (no custom implementation)
- File storage included (no separate S3 setup)
- Free tier sufficient for 10 users (500MB DB, 1GB storage)
- Clear upgrade path when scaling
- Open source (can self-host if needed)

## Links
- Tech Stack Guide: `docs/specification/tech-stack-guide.md`
- Tech Stack Final: `docs/specification/tech-stack-final.md`
