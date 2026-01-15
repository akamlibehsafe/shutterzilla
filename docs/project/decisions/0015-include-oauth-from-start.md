# 0015 - Include Social Login (OAuth) from the Start

## Status
Accepted

## Context
Authentication options:
- Email/password only
- Email/password + OAuth (Google, Facebook, etc.)

Considerations:
- User convenience (OAuth is faster sign-up)
- Learning opportunity (OAuth implementation)
- Implementation complexity
- Supabase Auth handles OAuth flow

## Decision
Include **Google and Facebook OAuth** authentication from project start, in addition to email/password. Supabase Auth handles the OAuth flow.

## Alternatives considered
- **Email/password only**: Pros - simpler, fewer integrations. Cons - slower sign-up, less convenient, miss learning opportunity
- **Add OAuth later**: Pros - can focus on core features first. Cons - need to add later anyway, more work to retrofit
- **OAuth from start**: Pros - better UX, faster sign-up, learn OAuth early, Supabase makes it easy, no custom implementation needed. Cons - additional setup (Google/Facebook apps) but one-time

## Consequences
- Better user experience (faster sign-up with OAuth)
- Learning opportunity (OAuth flow, provider setup)
- Supabase Auth handles all complexity (no custom OAuth code)
- Need to set up Google and Facebook OAuth apps (one-time)
- More authentication options for users
- Can add more providers later if needed

## Links
- Tech Stack Guide: `docs/specification/technical/tech-stack-guide.md`
- Tech Stack Final: `docs/specification/technical/tech-stack-final.md`
- Key Decisions Log: `docs/specification/implementation/key-decisions-log.md`
