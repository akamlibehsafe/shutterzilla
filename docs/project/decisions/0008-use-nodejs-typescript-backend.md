# 0008 - Use Node.js + TypeScript for Backend

## Status
Accepted

## Context
Need a backend runtime and framework that:
- Works well with Vercel serverless functions
- Shares language/ecosystem with frontend (Vue.js uses JavaScript/TypeScript)
- Provides type safety for API development
- Has good developer experience
- Fits solo dev + AI workflow

Constraints:
- Must work with Vercel hosting (serverless functions)
- Should minimize context switching between languages
- Need type safety for API reliability

## Decision
Use **Node.js** with **Express.js** and **TypeScript** for the backend API. All API endpoints are serverless functions on Vercel.

## Alternatives considered
- **Python + FastAPI**: Pros - good for data processing, familiar if coming from Python. Cons - different language from frontend, more context switching
- **PHP + Laravel**: Pros - familiar from LAMP background. Cons - doesn't work well with Vercel, different ecosystem
- **Go**: Pros - fast, compiled. Cons - different language, smaller ecosystem, more learning curve
- **Node.js + JavaScript**: Pros - same language as frontend. Cons - no type safety (higher error risk)
- **Node.js + TypeScript**: Pros - same language family as frontend, type safety, excellent Vercel support, large ecosystem, good AI assistance. Cons - none significant

## Consequences
- Code sharing between frontend and backend (TypeScript types, utilities)
- Single language ecosystem (JavaScript/TypeScript) - easier to maintain
- Type safety catches API errors at compile time
- Excellent Vercel serverless function support
- Large npm ecosystem for dependencies
- Good AI assistance (well-documented patterns)
- Express.js is simple and well-understood

## Links
- Tech Stack Guide: `docs/specification/technical/tech-stack-guide.md`
- Tech Stack Final: `docs/specification/technical/tech-stack-final.md`
- Key Decisions Log: `docs/specification/implementation/key-decisions-log.md`
