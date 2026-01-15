# 0017 - Prioritize Free Tier Services

## Status
Accepted

## Context
Project constraints:
- Friends/family project (max 10 users)
- Target: $0/month operating cost
- Learning project (not commercial)
- Need to balance features with cost

Every service choice impacts monthly cost. Need a strategy for selecting services that:
- Meet technical requirements
- Stay within free tiers
- Have clear upgrade paths when needed
- Don't compromise on essential features

## Decision
**Prioritize free tier services** for all technology choices. All services must have free tiers suitable for 10 users, with clear upgrade paths when the project scales.

## Alternatives considered
- **Use paid services from start**: Pros - more features, no limits. Cons - monthly costs, overkill for 10 users
- **Mix of free and paid**: Pros - best features. Cons - monthly costs, unnecessary for small project
- **Free tiers only**: Pros - $0/month, sufficient for 10 users, clear upgrade paths exist. Cons - some limitations (acceptable for project scope)

## Consequences
- **Total monthly cost: $0** ✅
- All services have free tiers sufficient for 10 users:
  - Supabase: 500MB DB, 1GB storage
  - Vercel: Unlimited personal projects
  - Resend: 3,000 emails/month
  - Sentry: 5,000 events/month
  - GitHub Actions: 2,000 minutes/month
- Clear upgrade paths when scaling:
  - Supabase Pro: $25/month
  - Resend Pro: $20/month
  - Sentry Pro: $26/month
  - Vercel Pro: $20/month
- Aligns with friends/family project scope
- Cost-conscious approach
- Can scale up when needed (if project grows)

## Links
- Tech Stack Final: `docs/specification/technical/tech-stack-final.md`
- Tech Stack Guide: `docs/specification/technical/tech-stack-guide.md`
- Key Decisions Log: `docs/specification/implementation/key-decisions-log.md`
