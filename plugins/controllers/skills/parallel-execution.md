---
skill: parallel-execution
version: "1.0.0"
description: "Determine when and how to execute multiple agents simultaneously for optimal throughput"
used-by:
  - orchestrator
  - frontend-controller
  - backend-controller
  - qa-controller
  - discovery-controller
---

# Parallel Execution Skill

## Purpose

Maximize throughput by running independent agent tasks simultaneously while avoiding conflicts from concurrent modifications to shared resources.

## Step-by-Step Procedure

### Step 1: Identify All Tasks

List all discrete tasks that need to be performed:
```
Task A: Build header component
Task B: Build footer component
Task C: Set up API routes
Task D: Write component tests
```

### Step 2: Map Dependencies

For each task, identify:
- **Inputs**: What does this task need to start?
- **Outputs**: What does this task produce?
- **Files touched**: Which files will be read/written?

### Step 3: Build Dependency Graph

```
[Task A] ──────────────────┐
                           ├──► [Task D] (needs A, B complete)
[Task B] ──────────────────┘

[Task C] ──────────────────────► (independent)
```

### Step 4: Apply Parallelization Rules

#### PARALLELIZE when:
- Tasks have **no shared file writes**
- Tasks are in **different domains** (frontend vs backend)
- Tasks produce **independent outputs**
- Tasks are **audits/analysis** (read-only operations)

#### DO NOT PARALLELIZE when:
- Tasks modify the **same file**
- Task B requires **output from Task A**
- Tasks share a **stateful resource** (database schema, config)
- Order matters for **cumulative changes**

### Step 5: Group Into Execution Waves

```
Wave 1 (parallel):     Wave 2 (parallel):     Wave 3 (sequential):
├── Task A             ├── Task D             └── Task F
├── Task B             └── Task E
└── Task C
```

### Step 6: Set Concurrency Limits

| Task Type | Max Concurrent | Reason |
|-----------|----------------|--------|
| Page builds | 3 | Memory/context limits |
| API endpoints | 4 | Independent modules |
| Component builds | 3 | Style coordination |
| Audit tasks | 5 | Read-only operations |
| File-heavy ops | 2 | Prevent conflicts |

## Parallelization Decision Matrix

| Scenario | Parallel? | Reasoning |
|----------|-----------|-----------|
| Header + Footer components | YES | Different files, no dependencies |
| Hero section + Hero animations | NO | Same component, sequential |
| Frontend pages + Backend APIs | YES | Different domains entirely |
| Database schema + API routes | NO | Routes depend on schema |
| Accessibility + Performance audits | YES | Both read-only analysis |
| Build component + Test component | NO | Tests need component first |
| Multiple page builds | YES (max 3) | Independent pages |
| Foundation + Components | NO | Components need foundation |

## Examples

### Example 1: Building Multiple Pages
```markdown
## Parallel Execution Plan

### Wave 1: Foundation (BLOCKING)
- @setup-dev-foundation

### Wave 2: Pages (parallel, max 3)
- @page-builder → Homepage
- @page-builder → About page
- @page-builder → Contact page

### Wave 3: Polish (after Wave 2)
- @animation-engineer → All pages
```

### Example 2: Full-Stack Feature
```markdown
## Parallel Execution Plan

### Wave 1: Planning (BLOCKING)
- @api-architect → Define endpoints

### Wave 2: Implementation (parallel)
- @react-engineer → Build UI components
- @node-engineer → Build API endpoints

### Wave 3: Integration (BLOCKING)
- @integration-engineer → Connect frontend to backend

### Wave 4: Quality (parallel)
- @accessibility-auditor
- @performance-auditor
```

### Example 3: Discovery Phase
```markdown
## Parallel Execution Plan

### Wave 1: Analysis (parallel)
- @brand-analyst → Brand guidelines
- @structure-analyst → Content structure
- @figma-analyst → Design tokens

### Wave 2: Synthesis (after Wave 1)
- @spec-synthesizer → Combine all findings
```

## Conflict Detection

Before parallel execution, check for conflicts:

```
Conflict Types:
├── FILE CONFLICT: Two tasks write to same file
│   └── Resolution: Serialize these tasks
├── DATA CONFLICT: Task B reads what Task A writes
│   └── Resolution: Task A blocks Task B
├── STATE CONFLICT: Shared external resource
│   └── Resolution: Serialize or use locking
└── LOGICAL CONFLICT: Order affects correctness
    └── Resolution: Define explicit ordering
```

## Common Pitfalls

1. **Over-parallelizing**: Running too many agents causes context thrashing
   - Fix: Respect concurrency limits (usually 3-4 max)

2. **Hidden dependencies**: Missing non-obvious relationships
   - Fix: Map file touches explicitly before parallelizing

3. **Race conditions**: Two agents modify related state
   - Fix: Identify shared resources in dependency mapping

4. **Ignoring wave boundaries**: Starting Wave 2 before Wave 1 completes
   - Fix: Use explicit BLOCKING markers and wait for completion

5. **Unbalanced waves**: One slow task holds up entire wave
   - Fix: Break large tasks into smaller parallel units

## Execution Checklist

Before launching parallel agents:
- [ ] All dependencies mapped
- [ ] No file write conflicts
- [ ] Concurrency limits respected
- [ ] Wave boundaries defined
- [ ] BLOCKING tasks identified
- [ ] Fallback plan if one fails
