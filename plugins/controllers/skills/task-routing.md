---
skill: task-routing
version: "1.0.0"
description: "Analyze user requests and route to the appropriate specialist agents"
used-by:
  - orchestrator
  - research-controller
  - planning-controller
  - frontend-controller
  - backend-controller
  - discovery-controller
  - design-controller
  - qa-controller
  - devops-controller
---

# Task Routing Skill

## Purpose

Route incoming requests to the most appropriate specialist agent(s) based on intent analysis, domain classification, and task requirements.

## Step-by-Step Procedure

### Step 1: Parse User Intent

1. Identify the **action verb** (build, research, fix, analyze, explain, etc.)
2. Extract the **domain** (frontend, backend, design, infrastructure, etc.)
3. Note any **constraints** (deadline, technology stack, file references)
4. Detect **implicit needs** (research before building, planning before complex work)

### Step 2: Classify Request Type

| Classification | Indicators | Primary Route |
|----------------|------------|---------------|
| **Exploratory** | "what", "how does", "compare" | @research-controller |
| **Strategic** | "plan", "architect", "design system" | @planning-controller |
| **Educational** | "explain", "teach", "tutorial" | @learning-controller |
| **Implementation** | "build", "create", "implement" | domain-specific controller |
| **Diagnostic** | "fix", "debug", "why isn't" | @analysis-controller or domain controller |
| **Operational** | "deploy", "configure", "set up" | @devops-controller |

### Step 3: Apply Domain Routing Decision Tree

```
Is this a web project request?
├── YES → Does it involve UI/UX?
│         ├── YES → @frontend-controller
│         └── NO → Does it involve APIs/data?
│                   ├── YES → @backend-controller
│                   └── NO → @devops-controller
└── NO → Is it about understanding something?
         ├── YES → @research-controller or @learning-controller
         └── NO → Is it about communication?
                   ├── YES → @communication-controller
                   └── NO → @general-dev-controller
```

### Step 4: Validate Routing Decision

Before spawning, verify:
- [ ] The agent has the required capabilities for this task
- [ ] Prerequisites are met (specs exist, dependencies resolved)
- [ ] The scope matches the agent's specialization
- [ ] No blocking dependencies are waiting

### Step 5: Formulate Task Prompt

Structure the task for the target agent:
```markdown
## Task: [Clear action statement]

### Context
[Relevant background the agent needs]

### Deliverables
- [Specific output 1]
- [Specific output 2]

### Constraints
- [Technology/approach constraints]
- [Time/scope constraints]
```

## Routing Examples

### Example 1: Ambiguous Request
**User:** "Help me with the login page"

**Analysis:**
- Action unclear (build? fix? design?)
- Domain: frontend/auth

**Response:** Ask clarifying questions:
1. "Is this a new login page or fixing an existing one?"
2. "What technology stack are you using?"
3. "Do you have a design spec or should I create one?"

### Example 2: Clear Implementation Request
**User:** "Build the hero section from the Figma design on the homepage"

**Analysis:**
- Action: build (implementation)
- Domain: frontend, specific component
- Artifact: Figma design exists

**Route:** @frontend-controller → @page-builder or @react-engineer

### Example 3: Multi-Domain Request
**User:** "Add user authentication to the app"

**Analysis:**
- Spans frontend (UI) + backend (API) + possibly devops (secrets)
- Complex, needs coordination

**Route:**
1. @planning-controller (architecture first)
2. Then parallel: @frontend-controller + @backend-controller

## Common Pitfalls

1. **Over-routing**: Sending simple tasks to controllers instead of direct specialists
   - Fix: For atomic, single-domain tasks, route directly to specialist

2. **Under-clarifying**: Assuming intent without confirmation
   - Fix: Always ask when action verb is missing or ambiguous

3. **Missing prerequisites**: Routing to implementation before specs exist
   - Fix: Check for existing specs; route to @design-controller first if missing

4. **Ignoring context**: Not considering project state or previous work
   - Fix: Review TodoWrite state and recent agent outputs before routing

5. **Single-threading complex work**: Not identifying parallel opportunities
   - Fix: Always ask "Can any of these tasks run simultaneously?"

## Quality Checklist

Before finalizing a routing decision:
- [ ] Intent is clear or clarified
- [ ] Domain is correctly identified
- [ ] Agent capabilities match requirements
- [ ] Dependencies are checked
- [ ] Task prompt is well-structured
- [ ] Parallel opportunities are identified
