---
skill: task-routing
version: "2.1.0"
description: "Route user requests directly to specialist agents (2-tier architecture)"
used-by:
  - orchestrator
  - main-thread
see-also:
  - complexity-detection (determine SIMPLE vs COMPLEX mode first)
  - multi-track-orchestration (for MODERATE/COMPLEX tasks)
---

# Task Routing Skill

## Prerequisites

**Before using this skill:** Run `complexity-detection.md` to determine if the request is SIMPLE, MODERATE, or COMPLEX.

- **SIMPLE mode** → Use this skill (direct routing to single specialist)
- **MODERATE/COMPLEX mode** → Use `multi-track-orchestration.md` instead

## Purpose

Route incoming requests directly to specialist agents. Claude Code uses a 2-tier architecture: Main Thread → Specialists. There are no intermediate controllers.

## Step-by-Step Procedure

### Step 1: Parse User Intent

1. Identify the **action verb** (build, research, fix, analyze, explain, etc.)
2. Extract the **domain** (frontend, backend, design, infrastructure, etc.)
3. Note any **constraints** (deadline, technology stack, file references)
4. Detect **implicit needs** (research before building, planning before complex work)

### Step 2: Route to Specialist(s)

| Request Type | Indicators | Route To |
|--------------|------------|----------|
| **Research** | "what", "how does", "compare", "find out" | `Explore` or custom web researcher |
| **Planning** | "plan", "architect", "break down" | `Plan` or custom planner |
| **Learning** | "explain", "teach", "tutorial" | custom tutorial/docs agent |
| **Frontend** | "build page", "component", "UI" | @frontend-developer, @build-page |
| **Backend** | "API", "database", "endpoint" | @backend-architect, @api-architect |
| **Debugging** | "fix", "debug", "why isn't" | @debugger |
| **DevOps** | "deploy", "CI/CD", "configure" | @devops-engineer |
| **QA** | "test", "audit", "quality" | @test-engineer (or parallel audits) |

### Step 3: Validate Before Spawning

- [ ] The agent has required capabilities for this task
- [ ] Prerequisites are met (specs exist, dependencies resolved)
- [ ] Scope matches the agent's specialization
- [ ] No blocking dependencies waiting

### Step 4: Formulate Task Prompt

```markdown
## Task: [Clear action statement]

### Context
[Relevant background the agent needs]

### Deliverables
- [Specific output 1]
- [Specific output 2]

### Constraints
- [Technology/approach constraints]
```

## Routing Examples

### Example 1: Ambiguous Request
**User:** "Help me with the login page"

**Response:** Ask clarifying questions:
1. "Is this a new login page or fixing an existing one?"
2. "What technology stack are you using?"

Then route to appropriate specialist.

### Example 2: Clear Implementation
**User:** "Build the hero section from the Figma design"

**Route:** @build-section or @frontend-developer directly

### Example 3: Multi-Domain Request
**User:** "Add user authentication to the app"

**Route (parallel where possible):**
1. @frontend-developer (auth UI)
2. @backend-architect (auth API)
3. @auth-engineer (security patterns)

## Common Patterns

### Single Domain Task
```
Main thread → Task(@specialist) → Synthesize result
```

### Multi-Domain Task
```
Main thread:
├── Task(@specialist-1) [parallel]
├── Task(@specialist-2) [parallel]
└── Task(@specialist-3) [parallel]
→ Synthesize all results
```

### Sequential Task
```
Main thread → Task(@specialist-1)
           → Task(@specialist-2) [uses output from 1]
           → Synthesize
```

## Quality Checklist

- [ ] Intent is clear or clarified
- [ ] Domain correctly identified
- [ ] Spawning specialist directly (NOT a controller)
- [ ] Task prompt is well-structured
- [ ] Parallel opportunities identified
