# 0022 - Planning Workflow: Master Plan + GitHub Issues/Projects

## Status
Accepted

## Context
Need to establish how to track and manage the implementation plan. The master plan document exists with detailed phases and checkboxes, but we need a workflow for daily execution and progress tracking.

Questions:
- Should the master plan be the only tracking mechanism?
- Should we use GitHub Issues/Projects for tracking?
- How do they relate to each other?
- What's the workflow for daily development?

## Decision
Use a **two-tier tracking system**:

1. **Master Plan Document** (`docs/specification/implementation/implementation-plan.md`)
   - Source of truth for overall roadmap
   - Phase structure and high-level tasks
   - Reference document for planning
   - Updated when phases change or major decisions are made

2. **GitHub Issues/Projects**
   - Individual task tracking
   - Visual progress (Kanban board)
   - Link code (PRs) to tasks
   - Daily workflow management
   - Issues created from master plan checkboxes

**Workflow:**
```
Master Plan (Document)
    ↓
    Convert checkboxes to GitHub Issues
    ↓
GitHub Issues (Individual Tasks)
    ↓
    Organize in GitHub Projects Board
    ↓
GitHub Projects (Kanban: To Do → In Progress → Done)
```

## Alternatives considered

**Option 1: Master Plan Only**
- Pros: Single source of truth, simple
- Cons: No visual tracking, hard to link PRs, no daily workflow tool
- **Rejected:** Too limited for active development tracking

**Option 2: GitHub Issues/Projects Only**
- Pros: Good tracking, visual board, PR linking
- Cons: No master reference document, hard to see big picture
- **Rejected:** Need master plan for overall structure

**Option 3: Master Plan + GitHub Issues/Projects (Two-Tier)**
- Pros: Best of both - master plan for structure, GitHub for execution
- Cons: Need to keep them in sync (acceptable trade-off)
- **Chosen:** Provides structure and execution tracking

## Consequences

### Benefits
- **Clear structure:** Master plan shows overall roadmap
- **Daily tracking:** GitHub Projects shows what's in progress
- **Code linking:** PRs link to issues, issues link to plan
- **Visual progress:** Kanban board shows progress at a glance
- **Flexibility:** Can adjust issues without changing master plan structure
- **History:** GitHub Issues provide detailed history of work

### Workflow
- **Planning:** Update master plan when phases change
- **Execution:** Create issues from master plan checkboxes
- **Daily work:** Track progress in GitHub Projects board
- **Completion:** Mark checkboxes in master plan when issues are done
- **Sync:** Periodically sync master plan with completed issues

### Maintenance
- Master plan updated when phases/structure change
- Issues created from plan checkboxes
- Master plan checkboxes marked when issues complete
- Both stay in sync through regular updates

## Links
- Master Plan: `docs/specification/implementation/implementation-plan.md`
- DevOps Guide: `docs/guides/devops-guide.md` - GitHub Projects setup
- Implementation Plan: `docs/specification/implementation/implementation-plan.md`
