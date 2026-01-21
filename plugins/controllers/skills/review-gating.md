---
skill: review-gating
version: "1.0.0"
description: "Quality gate pattern with formal verdicts - SHIP, NEEDS_WORK, MAJOR_RETHINK"
used-by:
  - orchestrator
  - worker
  - qa-auditor
  - follow-up-triggers
---

# Review Gating Skill

## Purpose

Ensure implementation quality through formal review gates before task completion. Prevents accumulating technical debt and catches issues early when they're cheapest to fix.

## Core Concept

Every task implementation goes through a formal review that results in one of three verdicts:

| Verdict | Meaning | Next Action |
|---------|---------|-------------|
| **SHIP** ✅ | Approved | Proceed to completion |
| **NEEDS_WORK** 🔧 | Fixable issues | Worker fixes, re-review |
| **MAJOR_RETHINK** 🚨 | Fundamental problem | Escalate to user |

## Enabling Review Gating

```bash
# Initialize the review system
taskctl review init

# This creates:
# - .tasks/reviews/ directory
# - Sets config: review.enabled = true
# - Sets config: review.maxIterations = 3
```

## The Review Flow

### Standard Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         REVIEW GATE                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Worker                                                         │
│      │                                                           │
│      ▼                                                           │
│   Implements Task                                                │
│      │                                                           │
│      ▼                                                           │
│   Commits Code ─────────────► Main Thread                        │
│                                    │                             │
│                                    ▼                             │
│                              Spawns @qa-auditor                  │
│                                    │                             │
│                                    ▼                             │
│                              Reviews Against Spec                │
│                                    │                             │
│                  ┌─────────────────┼─────────────────┐          │
│                  ▼                 ▼                 ▼          │
│               SHIP ✅        NEEDS_WORK 🔧    MAJOR_RETHINK 🚨  │
│                  │                 │                 │          │
│                  ▼                 ▼                 ▼          │
│             Mark Done         Fix & Retry        Escalate       │
│                               (max 3x)           to User        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Fix Loop

```
   NEEDS_WORK
       │
       ▼
   Worker receives issues
       │
       ▼
   Applies specific fixes
       │
       ▼
   Commits: "fix(task-id): address review feedback"
       │
       ▼
   Returns for re-review
       │
       ▼
   @qa-auditor re-reviews
       │
   ┌───┴───┐
   ▼       ▼
 SHIP   NEEDS_WORK again?
          │
          ▼
      Iteration++
          │
      ┌───┴───┐
      ▼       ▼
   < 3x    >= 3x
      │       │
      ▼       ▼
   Loop    MAJOR_RETHINK
```

## Orchestrator Integration

### In EXECUTE Phase

When spawning worker for a task:

```markdown
## EXECUTE with Review Gating

1. Spawn @worker with task
2. Worker completes and returns "Ready for Review"
3. Check: Is review.enabled?
   - If yes: Spawn @qa-auditor for review
   - If no: Proceed to task completion
4. Handle verdict:
   - SHIP: Mark task done, proceed to next
   - NEEDS_WORK: Return issues to worker, re-spawn
   - MAJOR_RETHINK: Pause, report to user
```

### Spawning for Review

```markdown
Task(@qa-auditor, """
TASK_ID: ca-1-abc.2
EPIC_ID: ca-1-abc
TASKCTL: $PLUGIN_ROOT/plugins/controllers/scripts/taskctl

Review the implementation of task ca-1-abc.2.

The worker reports implementation complete. Review against:
1. Task specification (use taskctl cat ca-1-abc.2)
2. Epic context (use taskctl cat ca-1-abc)
3. Changed files (use git diff HEAD~1)

Issue verdict: SHIP, NEEDS_WORK, or MAJOR_RETHINK
Log result: taskctl review log ca-1-abc.2 --verdict [VERDICT] --notes "[summary]"
""")
```

### Handling NEEDS_WORK

```markdown
# When QA returns NEEDS_WORK

1. Parse the specific issues from QA output
2. Re-spawn worker with fix instructions:

Task(@worker, """
TASK_ID: ca-1-abc.2
EPIC_ID: ca-1-abc
TASKCTL: $PLUGIN_ROOT/plugins/controllers/scripts/taskctl
SPECIALIST_CONTEXT: [original specialist]
REVIEW_ITERATION: 2

## Review Feedback to Address

### Issue 1: [from QA]
- Location: file.ts:45
- Problem: [description]
- Fix: [instruction]

### Issue 2: [from QA]
- Location: file.ts:78
- Problem: [description]
- Fix: [instruction]

Address these specific issues and re-commit.
""")
```

### Handling MAJOR_RETHINK

```markdown
# When QA returns MAJOR_RETHINK

Do NOT attempt to fix. Report to user:

## Review Escalation: ca-1-abc.2

### Verdict: MAJOR_RETHINK 🚨

The QA auditor has identified fundamental issues requiring your decision:

[Include full MAJOR_RETHINK output from QA]

### Options
1. Option A: [from QA assessment]
2. Option B: [from QA assessment]
3. Option C: [from QA assessment]

### Waiting for Direction
Task is blocked pending your decision on how to proceed.
```

## CLI Commands

### Initialize Review System
```bash
taskctl review init
```
Creates `.tasks/reviews/` and enables review gating.

### Log a Review
```bash
taskctl review log ca-1-abc.2 --verdict SHIP --notes "All criteria met"
taskctl review log ca-1-abc.2 --verdict NEEDS_WORK --notes "Missing error handling"
taskctl review log ca-1-abc.2 --verdict MAJOR_RETHINK --notes "Architecture needs discussion"
```

### Check Iteration Count
```bash
taskctl review count ca-1-abc.2
# Output: 2 (meaning this would be the 3rd review)
```

### List Reviews for Task
```bash
taskctl review list ca-1-abc.2
# Output:
# [1] 2026-01-21T10:30:00Z - NEEDS_WORK
#     Missing error handling for edge case...
# [2] 2026-01-21T11:15:00Z - SHIP
#     All criteria met
```

### Show Review Details
```bash
taskctl review show ca-1-abc.2
# Shows latest review

taskctl review show ca-1-abc.2 --iteration 1
# Shows specific iteration

taskctl review show ca-1-abc.2 --json
# JSON output for parsing
```

## Review Receipt Format

Each review creates a receipt in `.tasks/reviews/`:

```json
{
  "type": "impl_review",
  "task_id": "ca-1-abc.2",
  "epic_id": "ca-1-abc",
  "verdict": "SHIP",
  "reviewer": "qa-auditor",
  "timestamp": "2026-01-21T10:30:00Z",
  "notes": "All acceptance criteria met. Code quality good.",
  "iteration": 2
}
```

## Configuration

```bash
# Check if review is enabled
taskctl config get review.enabled

# Enable/disable review gating
taskctl config set review.enabled true
taskctl config set review.enabled false

# Set max iterations before auto-escalate
taskctl config set review.maxIterations 3
```

## When to Use Review Gating

### Enable For
- Complex features with multiple acceptance criteria
- Code that will be hard to change later
- Tasks involving security or data integrity
- Junior team member implementations
- Critical path work

### Skip For (Optional)
- Simple tasks with obvious implementations
- Documentation-only tasks
- Configuration changes
- Exploratory/spike work

## Integration with Memory

When review gating and memory are both enabled:

### After SHIP
```bash
# If the review process revealed useful learnings:
taskctl memory add --type convention "Always validate input at API boundaries"
```

### After NEEDS_WORK (Fixed)
```bash
# Capture the pitfall that was caught:
taskctl memory add --type pitfall "Edge case: empty array input causes crash. Always check length."
```

### After MAJOR_RETHINK
```bash
# Capture the architectural decision:
taskctl memory add --type decision "Chose Option B: Use optimistic updates with rollback."
```

## Anti-Patterns

1. **Skipping review for "simple" tasks**
   - If in doubt, review. It's cheap insurance.

2. **Rubber-stamping to move faster**
   - Reviews catch real issues. Don't SHIP just to proceed.

3. **Endless NEEDS_WORK loops**
   - After 3 iterations, escalate. Something is fundamentally wrong.

4. **Vague NEEDS_WORK feedback**
   - Always give specific file:line and fix instructions.

5. **Worker guessing at fixes**
   - Worker should only fix what QA explicitly flagged.

## Quality Checklist

Before completing a reviewed task:
- [ ] Review receipt logged via `taskctl review log`
- [ ] Final verdict is SHIP
- [ ] All NEEDS_WORK issues resolved
- [ ] Memory captured for significant learnings
- [ ] Task marked done only after SHIP verdict
