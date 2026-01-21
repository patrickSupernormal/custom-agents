---
skill: re-anchoring
version: "1.0.0"
description: "Pattern for context re-synchronization before task execution to prevent drift"
used-by:
  - worker
  - all-specialists
requires:
  - taskctl CLI
---

# Re-anchoring Skill

## Purpose

Prevent context drift by re-reading the source of truth before every task. This pattern ensures that even after context compaction, long pauses, or accumulated conversation, the agent starts from verified reality rather than potentially stale assumptions.

## Why Re-anchoring Matters

### The Drift Problem
As conversations progress, context accumulates and can become stale:
- Earlier decisions may have been superseded
- Code may have changed since last read
- Assumptions from previous tasks may not apply

### The Solution
Before every task implementation:
1. Read the authoritative specification
2. Check the actual state of the codebase
3. Compare expectation vs reality
4. Only then proceed with implementation

## Mandatory Re-anchor Steps

### Step 1: Read Task Specification

```bash
# Get the authoritative task definition
taskctl cat $TASK_ID
```

Parse the output for:
- **Title**: What this task is called
- **Description**: Detailed requirements
- **Acceptance Criteria**: What "done" looks like
- **Dependencies**: What must be done first

**Key Question:** "Do I understand exactly what needs to be built?"

### Step 2: Read Epic Context

```bash
# Get epic metadata
taskctl epic show $EPIC_ID

# Get epic specification
taskctl cat $EPIC_ID
```

Understand:
- **Overall Goal**: Why this epic exists
- **Decisions Made**: Architectural choices already decided
- **Related Tasks**: How this task fits with others
- **Constraints**: Technical or business limitations

**Key Question:** "Do I understand how this task fits the bigger picture?"

### Step 3: Check Repository State

```bash
# What files are modified?
git status

# What were recent changes?
git log -5 --oneline

# What branch am I on?
git branch --show-current

# What does the relevant code look like NOW?
# (Read specific files mentioned in spec)
```

Verify:
- Branch is correct for this work
- No uncommitted changes that conflict
- Recent commits align with expectations
- Relevant files exist and match expected state

**Key Question:** "Is the codebase in the state I expect?"

### Step 4: Validate Starting Point

Compare spec requirements against current state:

```markdown
## Validation Checklist

### Expected State (from spec)
- [ ] [File/feature that should exist]
- [ ] [Dependency that should be available]
- [ ] [State that should be in place]

### Actual State (from git/read)
- [x] [What actually exists]
- [x] [What's actually available]
- [ ] [What's missing or different]

### Delta
- **Already done:** [list items]
- **Still needed:** [list items]
- **Conflicts:** [any mismatches]
```

**Key Question:** "What exactly needs to change from current state to meet spec?"

### Step 5: Read Memory (if enabled)

```bash
# Check if memory is enabled
taskctl config get memory.enabled

# If true, read relevant learnings
taskctl memory list --type pitfall
taskctl memory list --type convention
taskctl memory list --type decision
```

Apply relevant learnings:
- **Pitfalls**: Mistakes to avoid
- **Conventions**: Patterns to follow
- **Decisions**: Choices already made

**Key Question:** "What have we learned that applies here?"

## When to Re-anchor

### Always Re-anchor
- Start of every new task
- After returning from a pause/break
- After any context compaction message
- When something feels "off" or uncertain
- Before claiming task completion

### Quick Re-anchor (abbreviated)
For continuation within same task:
```bash
git status                    # Check nothing unexpected changed
taskctl task show $TASK_ID    # Verify still in_progress
```

### Full Re-anchor
For new tasks or after any interruption:
- All 5 steps above
- No shortcuts

## Re-anchor Output Template

After completing re-anchor, document your understanding:

```markdown
## Re-anchor Complete: $TASK_ID

### Task Understanding
**Goal:** [One sentence summary]
**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

### Current State
**Branch:** [branch name]
**Recent commits:** [relevant commits]
**Relevant files:**
- `path/to/file.ts` - [current state summary]

### Implementation Plan
1. [First step]
2. [Second step]
3. [Verification step]

### Applicable Memory
- **Pitfall to avoid:** [if any]
- **Convention to follow:** [if any]

### Ready to Implement: Yes/No
[If No, explain what's blocking or unclear]
```

## Integration with Worker Agent

The worker agent MUST complete re-anchoring as Phase 1:

```
Worker receives task
    ↓
Phase 1: Re-anchor (this skill)
    ├── Read task spec
    ├── Read epic context
    ├── Check git state
    ├── Check memory
    └── Validate starting point
    ↓
Phase 2: Implement (only after re-anchor)
    ↓
Phase 3: Verify
    ↓
Phase 4: Complete
```

## Anti-Patterns

### DON'T: Skip re-anchoring
```
❌ "I remember what this task needs..."
✓ "Let me read the spec to confirm..."
```

### DON'T: Assume git state
```
❌ "The file should be at src/components..."
✓ "Let me check: git status && ls src/components"
```

### DON'T: Proceed with uncertainty
```
❌ "I'll assume they meant X..."
✓ "The spec is unclear about X, returning for clarification"
```

### DON'T: Trust accumulated context
```
❌ "Earlier we decided to use Y..."
✓ "Let me verify the decision in the epic spec..."
```

## Benefits

1. **Drift Prevention**: Each task starts from verified truth
2. **Session Resilience**: Can resume after compaction/breaks
3. **Quality Assurance**: Catches misalignment early
4. **Clear Scope**: Implements exactly what's specified
5. **Audit Trail**: Documentation of what was understood

## Quality Checklist

Before proceeding to implementation:
- [ ] Task spec read and understood
- [ ] Epic context reviewed
- [ ] Git state verified
- [ ] Memory consulted (if enabled)
- [ ] Starting point validated
- [ ] No unresolved ambiguities
- [ ] Implementation plan clear
