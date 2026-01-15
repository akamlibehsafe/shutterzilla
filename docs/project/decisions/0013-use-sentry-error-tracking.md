# 0013 - Use Sentry for Error Tracking

## Status
Accepted

## Context
Need error tracking and monitoring for:
- Frontend errors (Vue.js)
- Backend API errors (Node.js)
- Crashes and exceptions
- User context for debugging

Requirements:
- Free tier for initial 10 users
- Easy integration
- Good error details (stack traces, user context)
- Email alerts for critical errors

## Decision
Use **Sentry** for error tracking in both frontend and backend. Configured to track Vue.js errors and Node.js API errors.

## Alternatives considered
- **Rollbar**: Pros - similar features. Cons - free tier more limited, less popular
- **Bugsnag**: Pros - good features. Cons - paid service, no free tier
- **LogRocket**: Pros - session replay. Cons - paid service, overkill for this project
- **Custom logging**: Pros - full control. Cons - need to build everything, no error grouping, no alerts
- **Sentry**: Pros - excellent free tier (5,000 events/month), great error details, stack traces, user context, email alerts, easy integration, popular. Cons - none significant

## Consequences
- Free tier sufficient for 10 users (5,000 events/month)
- Automatic error grouping and deduplication
- Rich error context (stack traces, user info, browser/OS)
- Email alerts for critical errors
- Easy integration with Vue.js and Node.js
- Clear upgrade path (Sentry Pro: $26/month for 50,000 events)
- Essential for monitoring application health

## Links
- Tech Stack Guide: `docs/specification/technical/tech-stack-guide.md`
- Tech Stack Final: `docs/specification/technical/tech-stack-final.md`
- Key Decisions Log: `docs/specification/implementation/key-decisions-log.md`
