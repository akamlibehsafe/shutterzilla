# 0014 - Use Cloud Supabase Projects (No Local Docker)

## Status
Accepted

## Context
Supabase can be run in two ways:
- Local Docker containers (self-hosted locally)
- Cloud projects (hosted by Supabase)

Need to choose approach for development and production. Considerations:
- Setup complexity
- Local infrastructure management
- Internet dependency
- Development workflow
- Solo dev + AI workflow

## Decision
Connect directly to Supabase cloud projects (`shutterzilla-dev` and `shutterzilla-prod`) instead of running local Docker containers.

## Alternatives considered
- **Local Docker setup**: Pros - works offline, full control, faster for some operations. Cons - Docker setup complexity, local infrastructure management, need to maintain Docker, more moving parts
- **Cloud projects only**: Pros - zero local setup, no Docker needed, simpler workflow, Supabase handles everything, same environment as production. Cons - requires internet connection (acceptable trade-off)

## Consequences
- Zero local infrastructure setup (no Docker)
- Simpler development workflow
- Same environment as production (dev/prod Supabase projects)
- No Docker maintenance or troubleshooting
- Requires internet connection for development (acceptable)
- Free tier sufficient for both dev and prod projects
- Can test migrations directly on cloud projects

## Links
- Tech Stack Guide: `docs/specification/technical/tech-stack-guide.md`
- Tech Stack Final: `docs/specification/technical/tech-stack-final.md`
- Key Decisions Log: `docs/specification/implementation/key-decisions-log.md`
