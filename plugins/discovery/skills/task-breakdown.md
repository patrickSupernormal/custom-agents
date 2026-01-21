---
skill: task-breakdown
version: "1.0.0"
description: "Decomposing complex tasks into manageable, executable subtasks"
used-by:
  - "@task-decomposer"
  - "@discovery-controller"
  - "@planning-controller"
---

# Task Breakdown

## Overview

Systematic approach to decomposing large, ambiguous tasks into clear, actionable subtasks with proper sequencing and dependency management.

---

## Phase 1: Task Analysis

### Initial Assessment Questions
1. **What is the end deliverable?** (Be specific)
2. **Who is the audience?** (Stakeholder, user, system)
3. **What are the constraints?** (Time, tech, resources)
4. **What already exists?** (Starting point)
5. **What are the unknowns?** (Research needed)

### Complexity Classification
```
SIMPLE: 1-3 steps, clear path, <1 hour
├── Execute directly
└── No breakdown needed

MODERATE: 4-10 steps, some dependencies, 1-4 hours
├── Break into sequential subtasks
└── Single agent can handle

COMPLEX: 10+ steps, multiple dependencies, 4+ hours
├── Break into phases
├── Multiple agents required
└── Coordination checkpoints needed
```

---

## Phase 2: Decomposition Strategy

### Work Breakdown Structure (WBS)
```
TASK: [Main Objective]
│
├── PHASE 1: [First Major Milestone]
│   ├── Subtask 1.1: [Specific action]
│   ├── Subtask 1.2: [Specific action]
│   └── Subtask 1.3: [Specific action]
│
├── PHASE 2: [Second Major Milestone]
│   ├── Subtask 2.1: [Specific action]
│   └── Subtask 2.2: [Specific action]
│
└── PHASE 3: [Final Milestone]
    └── Subtask 3.1: [Specific action]
```

### Subtask Criteria (SMART-A)
Each subtask must be:
- **S**pecific: Clear, unambiguous action
- **M**easurable: Defined completion criteria
- **A**chievable: Can be done by one agent
- **R**elevant: Contributes to main goal
- **T**ime-bound: Reasonable time estimate
- **A**ssignable: Clear agent/skill match

---

## Phase 3: Dependency Mapping

### Dependency Types
| Type | Symbol | Meaning |
|------|--------|---------|
| Blocking | `[B]` | Must complete before next starts |
| Parallel | `[P]` | Can run simultaneously |
| Optional | `[O]` | Nice to have, not blocking |
| Conditional | `[C]` | Only if condition met |

### Dependency Graph Template
```
[Task A] ─[B]─> [Task B] ─[B]─> [Task D]
    │                │
    └──[P]──> [Task C]──┘

Legend:
- A blocks B (B cannot start until A completes)
- A and C can run in parallel
- Both B and C block D
```

### Critical Path Identification
1. List all tasks with durations
2. Identify blocking dependencies
3. Calculate longest path = critical path
4. Focus resources on critical path items

---

## Phase 4: Task Specification

### Subtask Template
```markdown
## Subtask: [Name]
**ID**: [PHASE]-[NUMBER]
**Agent**: @[agent-name]
**Estimated Time**: [duration]
**Dependencies**: [list of task IDs that must complete first]

### Objective
[One sentence describing what this accomplishes]

### Inputs
- [What this task receives]

### Actions
1. [Specific step]
2. [Specific step]
3. [Specific step]

### Outputs
- [What this task produces]

### Completion Criteria
- [ ] [Measurable criterion]
- [ ] [Measurable criterion]
```

---

## Phase 5: Sequencing

### Execution Order Template
```markdown
## Execution Plan

### Wave 1 (Parallel)
- [ ] Task 1.1 (@agent-a)
- [ ] Task 1.2 (@agent-b)

### Checkpoint 1
- Verify: [What to check before proceeding]

### Wave 2 (Sequential)
- [ ] Task 2.1 (@agent-a) [depends on 1.1]
- [ ] Task 2.2 (@agent-a) [depends on 2.1]

### Wave 3 (Parallel)
- [ ] Task 3.1 (@agent-b)
- [ ] Task 3.2 (@agent-c)

### Final Checkpoint
- Verify: [Final validation criteria]
```

---

## Decision Framework

### When to Parallelize
```
✓ Tasks have no shared dependencies
✓ Tasks modify different files/systems
✓ Tasks are in different domains
✓ No task needs output from another
```

### When to Sequence
```
✗ Task B needs output from Task A
✗ Both tasks modify same resource
✗ Order affects outcome
✗ Validation required between steps
```

---

## Common Pitfalls

| Pitfall | Prevention |
|---------|------------|
| Tasks too large | If >2 hours, break down further |
| Tasks too small | Combine if <15 min and related |
| Missing dependencies | Review each task's inputs |
| Unclear completion | Add measurable criteria |
| Wrong agent assignment | Match task to agent specialty |
| Over-parallelization | Consider coordination overhead |

---

## Output Template

```markdown
## Task Breakdown: [Main Task Name]

### Overview
- **Complexity**: Simple/Moderate/Complex
- **Total Subtasks**: [N]
- **Estimated Duration**: [time]
- **Critical Path**: [list key blocking tasks]

### Phases
[WBS structure]

### Dependencies
[Dependency graph]

### Execution Order
[Wave-based execution plan]

### Risk Areas
- [Tasks with uncertainty]
- [Potential blockers]
```

---

## Quality Checklist

- [ ] All subtasks pass SMART-A criteria
- [ ] Dependencies clearly mapped
- [ ] No circular dependencies
- [ ] Agent assignments appropriate
- [ ] Time estimates reasonable
- [ ] Completion criteria defined
- [ ] Critical path identified
