# 0012 - Use Zoho Mail Free + Gmail Forwarding for Email Receiving

## Status
Accepted

## Context
Need email receiving for:
- Support emails (`hello@shutterzilla.com`)
- User inquiries
- General contact

Requirements:
- Free solution (no paid email hosting)
- Professional email address (@shutterzilla.com)
- Easy to manage (prefer using existing Gmail)
- No need for separate email client

## Decision
Use **Zoho Mail Free** to host `hello@shutterzilla.com`, with automatic forwarding to personal Gmail. Configure Gmail "Send mail as" with Zoho SMTP to send from the professional address.

## Alternatives considered
- **Google Workspace**: Pros - professional, integrated. Cons - $6/user/month, overkill for small project
- **Microsoft 365**: Pros - professional. Cons - paid service, overkill
- **ProtonMail**: Pros - privacy-focused. Cons - paid for custom domain, more complex
- **Cloudflare Email Routing**: Pros - free, simple. Cons - forwarding only, can't send from address easily
- **Zoho Mail Free + Gmail forwarding**: Pros - completely free, professional address, all emails in Gmail, can send from address, MX records in Vercel DNS. Cons - requires Zoho account setup (one-time)

## Consequences
- Zero cost for email receiving
- Professional email address (hello@shutterzilla.com)
- All emails in one place (Gmail)
- Can send from professional address via Gmail
- MX records managed in Vercel DNS
- No need for separate email client
- Free tier sufficient for support needs

## Links
- Tech Stack Guide: `docs/specification/technical/tech-stack-guide.md`
- Tech Stack Final: `docs/specification/technical/tech-stack-final.md`
- Key Decisions Log: `docs/specification/implementation/key-decisions-log.md`
