---
skill: dependency-management
version: "1.0.0"
description: "Manage blocking vs non-blocking task dependencies to ensure correct execution order"
used-by:
  - orchestrator
  - frontend-controller
  - backend-controller
  - planning-controller
  - devops-controller
  - qa-controller
---

# Dependency Management Skill

## Purpose

Ensure tasks execute in the correct order by identifying, tracking, and enforcing dependencies between agent tasks.

## Step-by-Step Procedure

### Step 1: Identify Dependency Types

| Type | Symbol | Description | Example |
|------|--------|-------------|---------|
| **BLOCKING** | `[B]` | Must complete before next starts | Schema → API routes |
| **SOFT** | `[S]` | Preferred order, not required | Design → Implementation |
| **PARALLEL** | `[P]` | Can run simultaneously | Header ∥ Footer |
| **OPTIONAL** | `[O]` | Nice to have, skip if unavailable | Optimization pass |

### Step 2: Map Task Relationships

For each task, document:
```yaml
task: Build User API
id: task-003
depends-on:
  - task-001: Database Schema [BLOCKING]
  - task-002: Auth System [BLOCKING]
blocks:
  - task-005: Frontend Integration
  - task-006: API Tests
outputs:
  - /src/api/users/*
  - /src/types/user.ts
```

### Step 3: Build Dependency Graph

```
[Foundation Setup] ──[B]──► [Component Library] ──[B]──► [Page Builds]
        │                           │                        │
        │                           │                        ▼
        │                           └────────[S]────► [Animation Polish]
        │
        └──────────[P]──────► [API Setup] ──[B]──► [Integration]
```

### Step 4: Validate Dependency Graph

Check for:
- **Cycles**: A → B → C → A (invalid, must break)
- **Missing nodes**: Referenced task doesn't exist
- **Orphans**: Tasks with no path to start
- **Dead ends**: Tasks that block nothing and produce no output

### Step 5: Execute with Dependency Awareness

```python
# Pseudocode for execution order
while unfinished_tasks:
    ready = [t for t in unfinished_tasks
             if all(dep.complete for dep in t.blocking_deps)]

    parallel_batch = ready[:MAX_CONCURRENT]
    execute_parallel(parallel_batch)

    for task in parallel_batch:
        task.mark_complete()
        notify_dependents(task)
```

## Dependency Patterns

### Pattern 1: Linear Pipeline
```
[Design Spec] ──► [Foundation] ──► [Components] ──► [Pages] ──► [QA]
     [B]              [B]              [B]            [B]
```
Use when: Each phase builds directly on previous output.

### Pattern 2: Fork-Join
```
              ┌──► [Frontend] ──┐
[Planning] ──►│                 │──► [Integration]
              └──► [Backend] ───┘
```
Use when: Independent work streams converge.

### Pattern 3: Diamond
```
         ┌──► [Task B] ──┐
[Task A] │               │ [Task D]
         └──► [Task C] ──┘
```
Use when: Multiple paths lead to same destination.

### Pattern 4: Layered
```
Layer 1: [A] [B] [C]     (all parallel)
              │
Layer 2: [D] [E]         (depend on Layer 1)
              │
Layer 3: [F]             (depends on Layer 2)
```
Use when: Clear hierarchical structure.

## Tracking Dependencies with TodoWrite

```markdown
## Project: E-commerce Site

### Completed
- [x] Discovery phase
- [x] Design specifications

### In Progress
- [ ] Foundation setup [BLOCKING] ← Currently executing
  - Blocks: Component library, Page builds

### Pending (Blocked)
- [ ] Component library [BLOCKED BY: Foundation]
- [ ] Homepage build [BLOCKED BY: Component library]
- [ ] Product page build [BLOCKED BY: Component library]

### Ready (Unblocked)
- [ ] API architecture [READY - no blockers]
- [ ] Database schema [READY - no blockers]
```

## Handling Dependency Failures

### Failure Scenarios

| Scenario | Impact | Resolution |
|----------|--------|------------|
| Blocking task fails | All dependents stuck | Fix and retry, or find alternative |
| Soft dependency fails | Degraded but functional | Continue with warnings |
| Optional task fails | Minimal impact | Log and skip |
| Circular dependency | Cannot proceed | Restructure tasks |

### Failure Response Protocol

```
1. IDENTIFY which tasks are blocked
2. ASSESS if alternative paths exist
3. NOTIFY about blocked work
4. EITHER:
   a. Fix the failed task and resume
   b. Remove the dependency if non-essential
   c. Restructure to break the blockage
5. UPDATE TodoWrite with new status
```

## Examples

### Example 1: Web Project Setup
```markdown
## Dependency Chain

@setup-dev-foundation [BLOCKING]
├── Creates: /src/styles/*, /src/lib/*
├── Blocks: @setup-dev-components
└── Duration: ~5 min

@setup-dev-components [BLOCKING, depends on foundation]
├── Creates: /src/components/*
├── Blocks: All @page-builder tasks
└── Duration: ~10 min

@page-builder (multiple, parallel after components)
├── Homepage [depends on components]
├── About [depends on components]
└── Contact [depends on components]
```

### Example 2: Feature with Soft Dependencies
```markdown
## User Authentication Feature

@api-architect [BLOCKING]
└── Outputs: API specification document

@database-architect [BLOCKING]
└── Outputs: Schema migrations

@node-engineer [depends on: api-architect, database-architect]
└── Outputs: Auth API endpoints

@react-engineer [SOFT depends on: api-architect]
└── Can start with mock data, integrate later

@security-auditor [depends on: node-engineer]
└── Review after implementation
```

## Common Pitfalls

1. **Implicit dependencies**: Assuming order without documenting
   - Fix: Always explicitly mark [BLOCKING] or [SOFT]

2. **Over-constraining**: Making everything blocking
   - Fix: Ask "Can this truly start without the other?"

3. **Under-constraining**: Missing critical dependencies
   - Fix: Map file inputs/outputs to find hidden dependencies

4. **Stale tracking**: Not updating status when tasks complete
   - Fix: Update TodoWrite immediately on completion

5. **Dependency explosion**: Too many interconnected tasks
   - Fix: Group related tasks; reduce granularity

## Dependency Checklist

Before executing dependent tasks:
- [ ] All [BLOCKING] dependencies complete
- [ ] Outputs from dependencies are accessible
- [ ] No circular dependencies exist
- [ ] TodoWrite reflects current state
- [ ] Failure handling plan exists
- [ ] Dependent tasks notified of completion
