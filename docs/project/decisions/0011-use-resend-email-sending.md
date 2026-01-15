# 0011 - Use Resend for Email Sending

## Status
Accepted

## Context
Need email service for automated emails:
- Email verification (sign-up)
- Password reset
- Search notifications (future)
- Transactional emails

Requirements:
- Free tier for initial 10 users
- Good deliverability
- Domain verification (send from @shutterzilla.com)
- Modern API
- Easy integration with Supabase Auth

## Decision
Use **Resend** for all automated email sending. Configured to send from `noreply@shutterzilla.com` and `hello@shutterzilla.com` with SPF/DKIM records.

## Alternatives considered
- **SendGrid**: Pros - popular, reliable. Cons - free tier limited (100/day), more complex setup
- **Mailgun**: Pros - good API. Cons - free tier limited (5,000/month), more complex
- **Amazon SES**: Pros - very cheap, scalable. Cons - complex setup, AWS account needed, billing complexity
- **Postmark**: Pros - great deliverability. Cons - paid service, no free tier
- **Resend**: Pros - excellent free tier (3,000/month, 100/day), modern API, great deliverability, easy domain verification, simple integration. Cons - newer service (but stable)

## Consequences
- Free tier sufficient for 10 users (3,000 emails/month)
- Modern, clean API
- Good deliverability rates
- Domain verification with SPF/DKIM records
- Easy integration with Supabase Auth
- Clear upgrade path (Resend Pro: $20/month for 50,000 emails)

## Links
- Tech Stack Guide: `docs/specification/technical/tech-stack-guide.md`
- Tech Stack Final: `docs/specification/technical/tech-stack-final.md`
- Key Decisions Log: `docs/specification/implementation/key-decisions-log.md`
