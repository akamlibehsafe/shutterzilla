# 0018 - Use Zod for Runtime Type Validation

## Status
Accepted

## Context
TypeScript provides compile-time type safety, but runtime validation is still needed for:
- API request payloads (user input from frontend or external sources)
- Environment variables (may be missing or wrong type)
- External API responses (can't trust external data)
- Database query results (defense in depth)

Runtime validation ensures data matches expected types and constraints at runtime, catching errors that TypeScript can't catch (e.g., data from external APIs, user input, environment variables).

## Decision
Use **Zod** for all runtime type validation in the backend API. Validate all API request payloads, environment variables, and external data using Zod schemas.

## Alternatives considered
- **Joi**: Pros - mature, feature-rich. Cons - larger bundle size, more verbose API, less TypeScript integration
- **Yup**: Pros - popular, good validation. Cons - less TypeScript-friendly, more complex API
- **class-validator**: Pros - decorator-based, works with classes. Cons - requires classes, less flexible, more setup
- **io-ts**: Pros - functional approach, good TypeScript integration. Cons - steeper learning curve, more complex
- **Manual validation**: Pros - full control. Cons - error-prone, lots of boilerplate, no type inference
- **Zod**: Pros - excellent TypeScript integration, type inference, simple API, small bundle, great error messages, schema-first approach. Cons - newer than Joi/Yup (but mature enough)

## Consequences
- Type-safe validation with automatic TypeScript type inference
- Runtime safety for all API inputs (catches invalid data)
- Better error messages for invalid inputs
- Single source of truth for data shapes (Zod schema = TypeScript type)
- Can validate environment variables at startup
- Can validate external API responses
- Small bundle size impact
- Easy to use and maintain
- Good developer experience (autocomplete, type hints)

## Links
- Tech Stack Guide: `docs/specification/technical/tech-stack-guide.md`
- Tech Stack Final: `docs/specification/technical/tech-stack-final.md`
- Implementation Plan: `docs/specification/implementation/implementation-plan.md`
