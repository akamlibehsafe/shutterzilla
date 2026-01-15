# 0009 - Use Prisma ORM

## Status
Accepted

## Context
Need a way to interact with PostgreSQL database (Supabase) from Node.js backend. Options include:
- Raw SQL queries
- Query builders
- ORMs (Object-Relational Mappers)

Requirements:
- Type safety (TypeScript)
- Good developer experience
- Migration management
- Works with Supabase PostgreSQL
- Good documentation

## Decision
Use **Prisma** as the ORM and database toolkit for all database operations.

## Alternatives considered
- **Raw SQL**: Pros - full control, no abstraction. Cons - no type safety, more boilerplate, manual migration management
- **TypeORM**: Pros - mature, feature-rich. Cons - more complex, steeper learning curve, more opinionated
- **Drizzle ORM**: Pros - lightweight, SQL-like. Cons - newer, smaller ecosystem
- **Kysely**: Pros - type-safe query builder. Cons - newer, less ORM features
- **Prisma**: Pros - excellent TypeScript support, great developer experience, built-in migrations, excellent docs, type-safe queries, works with Supabase. Cons - some limitations with complex queries (but sufficient for this project)

## Consequences
- Type-safe database queries (compile-time error checking)
- Automatic migration generation and management
- Excellent developer experience (autocomplete, type hints)
- Prisma Client provides clean API for database operations
- Schema defined in Prisma schema file (single source of truth)
- Can generate types from schema
- Some complex queries may need raw SQL (but rare)

## Links
- Tech Stack Guide: `docs/specification/technical/tech-stack-guide.md`
- Tech Stack Final: `docs/specification/technical/tech-stack-final.md`
- Implementation Plan: `docs/specification/implementation/implementation-plan.md`
