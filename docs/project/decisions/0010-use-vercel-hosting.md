# 0010 - Use Vercel for Hosting

## Status
Accepted

## Context
Need hosting for:
- Vue.js frontend (SPA)
- Node.js backend API (serverless functions)
- Automatic deployments from GitHub
- Preview deployments for feature branches
- CDN for static assets
- SSL certificates

Constraints:
- Must be free tier for initial 10 users
- Should support serverless functions
- Need preview deployments for testing
- Solo dev workflow (minimal complexity)

## Decision
Use **Vercel** for hosting both frontend and backend. Frontend is a Vue.js SPA, backend uses Vercel serverless functions.

## Alternatives considered
- **Netlify**: Pros - similar to Vercel, good free tier. Cons - slightly less popular, fewer features
- **AWS (S3 + Lambda)**: Pros - very flexible, scalable. Cons - complex setup, billing complexity, overkill for small project
- **DigitalOcean App Platform**: Pros - simple. Cons - paid service, more expensive
- **Traditional VPS (DigitalOcean Droplet)**: Pros - full control. Cons - server management, no automatic deployments, need to configure everything
- **Vercel**: Pros - excellent free tier (unlimited personal projects), automatic deployments, preview URLs, built-in CDN, SSL, serverless functions, great DX, zero config. Cons - vendor lock-in (but acceptable for this project)

## Consequences
- Zero server management (serverless)
- Automatic deployments on git push
- Preview URLs for every feature branch (test before merge)
- Built-in CDN and SSL
- Serverless functions for API (scales automatically)
- Free tier more than sufficient for 10 users
- Analytics and logs built-in
- Simple workflow (push to deploy)
- Vendor lock-in (but migration path exists if needed)

## Links
- Tech Stack Guide: `docs/specification/technical/tech-stack-guide.md`
- Tech Stack Final: `docs/specification/technical/tech-stack-final.md`
- Deployment Strategy: ADR 0005
- Key Decisions Log: `docs/specification/implementation/key-decisions-log.md`
