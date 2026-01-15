# 0005 - Use Simplified Deployment Strategy (main branch = production)

## Status
Accepted

## Context
Traditional multi-environment setup (dev/test/prod) requires:
- Multiple Vercel projects
- Multiple Supabase projects (already have dev/prod)
- Complex branching strategy
- More CI/CD configuration
- More overhead for solo dev + AI workflow

Constraints:
- Solo developer working with AI assistance
- Small user base (max 10 users)
- Need quick iteration and testing
- Want to minimize complexity

## Decision
Use `main` branch for production and feature branches for preview deployments. No separate dev/test environments in Vercel.

## Alternatives considered
- **Traditional dev/staging/prod**: Pros - isolated environments, safe testing. Cons - more projects, more config, slower workflow for solo dev
- **Feature branches = previews**: Pros - test before merge, minimal overhead. Cons - production on main (acceptable risk for small project)
- **Simplified (main = prod, branches = previews)**: Pros - simple, fast, Vercel auto-preview URLs, test before merge. Cons - production on main (but can test on preview first)

## Consequences
- Faster development workflow (less context switching)
- Feature branches automatically get preview URLs (Vercel)
- Can test thoroughly on preview before merging to main
- Single production deployment (main branch)
- Simpler CI/CD (no multi-environment logic)
- Lower cognitive overhead
- Still have dev/prod Supabase projects for database safety

## Links
- Tech Stack Final: `docs/specification/tech-stack-final.md`
- Implementation Plan: `docs/specification/implementation-plan.md`
