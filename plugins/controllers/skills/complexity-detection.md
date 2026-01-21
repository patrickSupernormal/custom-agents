---
skill: complexity-detection
version: "1.0.0"
description: "Detect task complexity to determine simple vs multi-track orchestration mode"
used-by:
  - orchestrator
  - main-thread
---

# Complexity Detection Skill

## Purpose

Analyze incoming requests to determine whether they should be routed directly to a single specialist (simple mode) or decomposed into multiple parallel tracks (complex mode).

## Complexity Scoring Matrix

| Signal | Points | Examples |
|--------|--------|----------|
| Multiple domains (frontend AND backend) | +2 | "Build feature with UI and API" |
| Multiple deliverables (build X, Y, Z) | +2 | "Create homepage, about page, and contact page" |
| Scope keywords (all, entire, complete, full) | +2 | "Complete redesign", "Full implementation" |
| Sequential workflow (first...then) | +1 | "First research, then implement" |
| Research + implement | +2 | "Find best approach and build it" |
| Quality gates mentioned | +1 | "Make sure tests pass", "Ensure accessible" |
| Ambiguous/vague request | +1 | "Help with the app" |
| Discovery needed first | +2 | "Figure out how to..." |
| Cross-cutting concerns | +1 | "With proper error handling and logging" |
| Integration requirement | +1 | "Connect to existing system" |

## Complexity Thresholds

| Score | Mode | Action |
|-------|------|--------|
| 0-2 | SIMPLE | Direct single-agent routing |
| 3-4 | MODERATE | 2-3 parallel tracks |
| 5+ | COMPLEX | Full multi-track orchestration |

## Override Rules

### Force SIMPLE (regardless of score)

- Single verb + single noun ("Fix the button", "Debug login")
- Explicit agent mention ("Use @debugger to...")
- Small scope indicators ("just", "only", "quick")
- Single file references ("in index.tsx")
- Question-only requests ("How does X work?")

### Force COMPLEX (regardless of score)

- Discovery commands (/discover, /audit)
- Deployment commands (/deploy, /launch)
- Multi-page requests ("all pages", "every component")
- End-to-end indicators ("from scratch", "complete feature")
- Full-stack indicators ("frontend and backend")

## Step-by-Step Procedure

### Step 1: Extract Keywords

Scan the request for:
- Action verbs (build, fix, research, deploy, test)
- Domain indicators (UI, API, database, component)
- Scope modifiers (all, entire, complete, just, only)
- Sequencing words (first, then, after, before)

### Step 2: Calculate Base Score

```
score = 0
for each signal in request:
    score += signal.points
```

### Step 3: Check Overrides

```
if has_force_simple_indicator:
    return SIMPLE
if has_force_complex_indicator:
    return COMPLEX
```

### Step 4: Determine Mode

```
if score <= 2:
    return SIMPLE
elif score <= 4:
    return MODERATE
else:
    return COMPLEX
```

## Examples

### Example 1: Simple (Score: 1)
**Request:** "Fix the typo in the header component"
- Single action: fix (+0)
- Single target: header component (+0)
- Scope modifier: "the" (specific) (+0)
- Small scope implied (+0)
**Override:** "Fix" + single file = FORCE SIMPLE
**Result:** SIMPLE → Route to @debugger

### Example 2: Moderate (Score: 4)
**Request:** "Build a contact form with validation"
- Action: build (+0)
- Deliverable: form (+1)
- Implicit: frontend (+0)
- Quality gate: validation (+1)
- Multiple concerns: UI + logic (+2)
**Result:** MODERATE → 2-3 tracks (UI, validation logic, maybe API)

### Example 3: Complex (Score: 7)
**Request:** "Build user authentication with signup, login, forgot password, and profile pages"
- Multiple deliverables: 4 pages (+2)
- Multiple domains: frontend + backend (+2)
- Scope keyword: implied "complete" (+2)
- Cross-cutting: auth across all (+1)
**Result:** COMPLEX → Full multi-track orchestration

### Example 4: Override to Simple
**Request:** "Just update the button color to blue"
- "Just" = small scope override
**Result:** FORCE SIMPLE → @css-architect directly

### Example 5: Override to Complex
**Request:** "Build the entire checkout flow end-to-end"
- "entire" + "end-to-end" = force complex override
**Result:** FORCE COMPLEX → Full multi-track

## Output Format

```markdown
## Complexity Assessment

**Request:** [original request]

### Scoring
| Signal | Points |
|--------|--------|
| [detected signal] | +X |
| [detected signal] | +X |
| **Total** | **X** |

### Override Check
- Force Simple: [Yes/No - reason]
- Force Complex: [Yes/No - reason]

### Result
**Mode:** [SIMPLE/MODERATE/COMPLEX]
**Action:** [Route directly / Create 2-3 tracks / Full orchestration]
```

## Integration with Orchestration

After complexity detection:

- **SIMPLE:** Use `task-routing.md` skill directly
- **MODERATE:** Use `multi-track-orchestration.md` with 2-3 tracks
- **COMPLEX:** Use full `multi-track-orchestration.md` with all 5 phases

### Epic Creation Trigger

For MODERATE and COMPLEX modes, create an epic to persist state:

```bash
# Initialize state directory (safe to run multiple times)
taskctl init

# Create epic with complexity score context
EPIC_ID=$(taskctl epic create "[Brief task description]")

# Write complexity assessment to epic spec
# The spec at .tasks/specs/$EPIC_ID.md should include:
# - Original request
# - Complexity score breakdown
# - Mode determination
# - Rationale for decomposition approach
```

**When to Create Epic:**
- MODERATE mode (score 3-4): Yes, create epic
- COMPLEX mode (score 5+): Yes, create epic
- SIMPLE mode (score 0-2): No epic (direct routing)

**Epic Spec Template:**
```markdown
# [Task Title]

## Original Request
[User's original request verbatim]

## Complexity Assessment
- **Score:** [X]
- **Mode:** [MODERATE/COMPLEX]
- **Signals:**
  - [Signal 1]: +X points
  - [Signal 2]: +X points

## Decomposition Approach
[Brief explanation of how task will be broken down]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
```

## Quality Checklist

- [ ] All keywords extracted from request
- [ ] Score calculated correctly
- [ ] Override rules checked
- [ ] Mode determination matches score/override
- [ ] Appropriate next skill identified
