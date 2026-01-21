---
skill: scope-management
version: "1.0.0"
description: "Identifying, preventing, and managing scope creep in projects"
used-by:
  - "@scope-manager"
  - "@task-decomposer"
  - "@discovery-controller"
---

# Scope Management

## Overview

Framework for defining clear project boundaries, identifying scope creep early, and managing scope changes through structured decision-making.

---

## Phase 1: Scope Definition

### Scope Statement Template
```markdown
## Project Scope Statement

### In Scope
Explicitly included in this project:
1. [Deliverable 1] - [Brief description]
2. [Deliverable 2] - [Brief description]
3. [Deliverable 3] - [Brief description]

### Out of Scope
Explicitly excluded from this project:
1. [Item 1] - [Why excluded]
2. [Item 2] - [Why excluded]

### Assumptions
- [Assumption 1]
- [Assumption 2]

### Constraints
- Budget: [Amount]
- Timeline: [Duration]
- Resources: [Limitations]

### Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
```

### Scope Boundaries Diagram
```
┌─────────────────────────────────────────────────────┐
│                    PROJECT SCOPE                     │
│  ┌─────────────────────────────────────────────┐    │
│  │              MUST HAVE (P1)                 │    │
│  │  [Core features essential for launch]       │    │
│  └─────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────┐    │
│  │              SHOULD HAVE (P2)               │    │
│  │  [Important but not launch-blocking]        │    │
│  └─────────────────────────────────────────────┘    │
│  ┌─────────────────────────────────────────────┐    │
│  │              COULD HAVE (P3)                │    │
│  │  [Nice to have if time permits]             │    │
│  └─────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────┘
                          │
                    SCOPE BOUNDARY
                          │
┌─────────────────────────────────────────────────────┐
│                   OUT OF SCOPE                       │
│  [Features/work explicitly not included]             │
└─────────────────────────────────────────────────────┘
```

---

## Phase 2: Scope Creep Detection

### Warning Signs
| Signal | Description | Risk Level |
|--------|-------------|------------|
| "While we're at it..." | Adding work to existing tasks | Medium |
| "Quick addition" | Underestimated new features | High |
| "Just one more thing" | Incremental expansion | Medium |
| "Can we also..." | Unplanned requests | High |
| "It would be nice if..." | Feature wishlist growth | Low |
| "The stakeholder mentioned..." | Unvetted requirements | High |

### Creep Categories
```
FEATURE CREEP: Adding new functionality
├── New features not in original scope
├── Enhanced versions of planned features
└── "Gold plating" beyond requirements

REQUIREMENT CREEP: Changing specifications
├── Moving success criteria
├── Changing definitions
└── Adding acceptance criteria

INSTRUCTION CREEP: Expanding directions
├── Additional guidelines
├── New constraints
└── Process changes
```

---

## Phase 3: Change Evaluation

### Change Request Template
```markdown
## Scope Change Request

### Request
[Clear description of proposed change]

### Requester
[Who is asking for this]

### Justification
[Why this is being requested]

### Impact Assessment
- **Timeline Impact**: [None/Days/Weeks]
- **Budget Impact**: [None/$X]
- **Resource Impact**: [None/Requires X]
- **Risk Impact**: [None/New risks introduced]

### Dependencies
- [What else is affected]

### Alternatives Considered
1. [Alternative approach]
2. [Do nothing option]

### Recommendation
[Accept/Reject/Defer] because [rationale]
```

### Decision Matrix
```
                    HIGH VALUE
                        │
    DEFER               │           ACCEPT
    (Low urgency,       │           (Worth the cost)
     high value)        │
                        │
    ────────────────────┼────────────────────
    LOW COST            │           HIGH COST
                        │
    ACCEPT              │           REJECT
    (Easy win)          │           (Not worth it)
                        │
                    LOW VALUE
```

---

## Phase 4: Scope Control

### Scope Lock Levels
```
LEVEL 1: FLEXIBLE
├── Changes welcomed with simple approval
└── Early project phase

LEVEL 2: CONTROLLED
├── Changes require impact assessment
├── Approval from project lead
└── Mid-project phase

LEVEL 3: LOCKED
├── Only critical changes accepted
├── Formal change control process
└── Late project phase

LEVEL 4: FROZEN
├── No changes except showstoppers
└── Final phase before delivery
```

### Trade-off Negotiations
When scope must increase, something else must give:
```
SCOPE ↑ requires one of:
├── TIMELINE ↑ (more time)
├── BUDGET ↑ (more resources)
├── QUALITY ↓ (reduced polish)
└── SCOPE ↓ (remove something else)
```

---

## Phase 5: Communication

### Stakeholder Response Templates

**Accepting a change:**
```
"This change is approved. Impact: [timeline/budget/other change].
We'll need to [adjustment required]."
```

**Rejecting a change:**
```
"This change is outside our current scope because [reason].
We can consider it for [future phase/version]."
```

**Deferring a change:**
```
"Great idea. I've added this to our backlog for [future phase].
For now, we're focused on [current priorities]."
```

**Negotiating a change:**
```
"We can include this if we [trade-off].
Alternatively, we could [simpler version]."
```

---

## Scope Creep Prevention Checklist

### At Project Start
- [ ] Written scope statement approved
- [ ] Out-of-scope items explicitly listed
- [ ] Change control process defined
- [ ] Stakeholder expectations aligned

### During Project
- [ ] All requests evaluated against scope
- [ ] Changes documented and assessed
- [ ] Trade-offs communicated clearly
- [ ] Scope lock level appropriate to phase

### At Each Milestone
- [ ] Scope reviewed against original
- [ ] Creep identified and addressed
- [ ] Remaining work re-estimated
- [ ] Stakeholders updated

---

## Common Pitfalls

| Pitfall | Prevention |
|---------|------------|
| Vague initial scope | Document specific deliverables |
| Fear of saying no | Use deferral, not rejection |
| Hidden scope growth | Review scope at each milestone |
| Scope-budget disconnect | Always state impact of changes |
| Stakeholder end-runs | Single point for scope decisions |
| Gold plating | Define "done" precisely |

---

## Output Template

```markdown
## Scope Management Report

### Current Scope Status
- **Lock Level**: [1-4]
- **Scope Health**: [On Track/At Risk/Exceeded]
- **Changes This Period**: [N]

### Pending Change Requests
| Request | Impact | Recommendation |
|---------|--------|----------------|
| [X]     | [Y]    | [Z]            |

### Scope Drift Analysis
- Original scope: [X items]
- Current scope: [Y items]
- Net change: [+/- Z items]

### Recommendations
- [Actions to maintain scope control]
```
