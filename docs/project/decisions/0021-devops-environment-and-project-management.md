# 0021 - DevOps Environment Strategy and Project Management

## Status
Accepted

## Context
Need to define DevOps practices for ShutterZilla, including:
- How to manage different environments (DEV, TST, PRD)
- How to provide realistic test data for preview deployments
- How to organize and track development work
- How to avoid merge conflicts and branch complexity

Constraints:
- Solo developer working with AI assistance
- Small project (max 10 users)
- Need simple, maintainable workflow
- Want to learn DevOps best practices
- Need realistic test data for meaningful testing

Key concerns:
- Branch-based environments can lead to merge conflicts when jumping between branches
- Preview deployments need realistic data for meaningful testing
- Need project management tool for organizing work

## Decision
Adopt **configuration-based environment management** with the following approach:

### Environment Strategy
- **Configuration-based (not branch-based)**: Environments controlled by environment variables, not Git branches
- **Two-environment approach**: Preview (DEV) + Production (PRD)
  - Preview deployments (feature branches) → DEV Supabase via environment variables
  - Production deployments (`main` branch) → PROD Supabase via environment variables
- **Key principle**: Branches are for features, not environments

### Data Seeding Strategy
- **Artificial/generated test data** for DEV Supabase
- Seeding script generates realistic fake data (1000+ camera listings, test users, collections)
- Safe, repeatable, sufficient for most testing scenarios
- Can add production data snapshot (anonymized) later if needed

### Project Management
- **GitHub Projects** for organizing development work
- Kanban board with issues linked to PRs
- Labels for phases, areas, priorities
- Milestones for tracking progress

## Alternatives considered

### Environment Management

**Branch-based environments (develop → staging → main):**
- Pros: Clear separation, traditional approach
- Cons: Merge conflicts when jumping between branches, complex workflow, risky for solo dev
- **Rejected**: Too complex and error-prone for solo dev workflow

**Configuration-based environments (feature → main with env vars):**
- Pros: Simple workflow, no merge conflicts, environments controlled by config, one source of truth
- Cons: Need to understand environment variables (acceptable learning curve)
- **Chosen**: Simpler, safer, better for solo dev

**Three environments (DEV/TST/PRD):**
- Pros: More testing stages, closer to enterprise workflows
- Cons: More setup, more complexity, may be overkill for small project
- **Rejected for now**: Can add staging later if needed

### Data Seeding

**Artificial/generated data:**
- Pros: Simple, safe, repeatable, no privacy concerns, sufficient for most testing
- Cons: May not catch all real-world edge cases
- **Chosen**: Best starting point, can enhance later

**Production data copy (anonymized):**
- Pros: Real data, catches real edge cases, always current
- Cons: More complex, requires anonymization, privacy concerns, needs production access
- **Rejected for now**: Can add later when needed

**No seeding (empty database):**
- Pros: Simple
- Cons: Can't test meaningfully, hard to verify features work
- **Rejected**: Need realistic data for testing

### Project Management

**GitHub Projects:**
- Pros: Free, integrated with GitHub, simple Kanban, good for learning, perfect for solo dev
- Cons: Less powerful than enterprise tools
- **Chosen**: Best fit for solo dev, good learning value

**Jira/Atlassian:**
- Pros: Industry standard, powerful features, enterprise workflows
- Cons: Paid (free tier limited), more complex, separate tool, overkill for small project
- **Rejected for now**: Can learn later if joining team that uses it

**No project management tool:**
- Pros: Simple
- Cons: Hard to track progress, no organization, difficult to plan
- **Rejected**: Need organization for solo dev + learning

## Consequences

### Environment Management
- **Simple workflow**: Feature branch → Preview (DEV) → Merge to main → Production (PRD)
- **No merge conflicts**: One branch (`main`), environments controlled by config
- **Easy to understand**: Clear separation between code (branches) and environments (config)
- **Scalable**: Can add staging environment later without changing workflow
- **Safe**: No risk of deploying wrong code to wrong environment
- **Learning value**: Understands configuration-based environments (industry standard)

### Data Seeding
- **Realistic testing**: Preview deployments have meaningful test data
- **Safe**: No production data risk, can reset anytime
- **Repeatable**: Generate fresh test data when needed
- **Maintainable**: Seeding script can be enhanced as project grows
- **Future flexibility**: Can add production snapshot later if needed

### Project Management
- **Organized workflow**: Issues track work, PRs link to issues
- **Visual progress**: Kanban board shows what's in progress
- **Learning value**: Understands Kanban, issue tracking, agile basics
- **Integrated**: Works seamlessly with GitHub (PRs, commits, issues)
- **Scalable**: Can add more structure (sprints, epics) later if needed

### Overall
- **Lower cognitive overhead**: Simple, clear workflow
- **Faster development**: Less time managing environments and branches
- **Better testing**: Realistic test data enables meaningful testing
- **Professional practices**: Follows industry-standard DevOps patterns
- **Learning opportunity**: Understands modern DevOps practices

## Links
- DevOps Guide: `docs/guides/devops-guide.md` - Comprehensive DevOps documentation
- Tech Stack Guide: `docs/specification/technical/tech-stack-guide.md` - Complete tech stack
- Simplified Deployment Strategy (ADR 0005): `docs/project/decisions/0005-simplified-deployment-strategy.md` - Related deployment decision
- Cloud Supabase (ADR 0014): `docs/project/decisions/0014-use-cloud-supabase-no-local-docker.md` - Related Supabase decision
