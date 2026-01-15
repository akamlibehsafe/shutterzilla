# 0019 - Use Monorepo Structure

## Status
Accepted

## Context
Project consists of multiple related applications and services:
- Frontend (Vue.js SPA)
- Backend (Node.js API)
- Scraper (Python service)
- Infrastructure (database migrations, CI/CD)
- Documentation

Need to organize code in a way that:
- Keeps related code together
- Enables code sharing (TypeScript types, utilities)
- Simplifies development workflow
- Makes it easy to find files
- Scales as project grows

## Decision
Use a **monorepo structure** with clear separation:
- `apps/` - All application code (frontend, backend, scraper)
- `infrastructure/` - Infrastructure as code (migrations, CI/CD)
- `docs/` - All documentation
- Root - Only essential configuration files

## Alternatives considered
- **Separate repositories (polyrepo)**: Pros - isolated codebases, independent versioning. Cons - harder to share code, more repos to manage, complex cross-repo changes, more CI/CD setup
- **Monolithic single folder**: Pros - simple. Cons - no organization, hard to scale, mixing concerns
- **Monorepo with clear structure**: Pros - code sharing easy, single repo to manage, unified CI/CD, clear organization, follows modern best practices. Cons - larger repo (acceptable for this project size)

## Consequences
- **Code sharing**: TypeScript types, utilities, and shared code can be easily shared between frontend and backend
- **Single source of truth**: All code in one place, easier to maintain
- **Unified CI/CD**: Single GitHub Actions workflow can handle all apps
- **Clear organization**: Easy to find code (`apps/`), docs (`docs/`), infrastructure (`infrastructure/`)
- **Scalability**: Easy to add new apps (just create `apps/new-app/`)
- **Future mobile apps**: Structure supports adding Android/iOS apps with shared code in `packages/` (see expansion guide)
- **Professional structure**: Follows modern monorepo patterns (similar to Turborepo, Nx)
- **Clean root directory**: Only essential config files at root
- **Simpler development**: One `git clone`, one `npm install` (with workspaces)
- **Version control**: All related changes in single commit (frontend + backend changes together)

## Links
- Functional Folder Structure: `docs/specification/functional/functional-folder-structure.md`
- Technical Folder Structure: `docs/specification/technical/folder-structure.md`
- Tech Stack Final: `docs/specification/technical/tech-stack-final.md`
- Monorepo Expansion Guide: `docs/guides/monorepo-expansion.md` (future mobile apps, code sharing patterns)
