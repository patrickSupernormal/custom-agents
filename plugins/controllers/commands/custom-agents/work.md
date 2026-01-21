---
name: custom-agents:work
description: Execute tasks from an epic with re-anchoring and optional review
argument-hint: "<epic-id or task-id>"
---

# Execute Work

Execute tasks from an epic or a specific task using the worker agent with re-anchoring.

## Prerequisites

- `.tasks/` must exist
- Epic/tasks must be created via `/custom-agents:plan`

## Process

### Step 1: Identify Work Unit

```bash
TASKCTL="${CLAUDE_PLUGIN_ROOT}/plugins/controllers/scripts/taskctl"

# If epic-id provided, find next ready task
if [[ "$ARGUMENTS" == ca-*-*.* ]]; then
    TASK_ID="$ARGUMENTS"
else
    # Get next ready task from epic
    TASK_ID=$($TASKCTL task ready --epic "$ARGUMENTS" | head -1)
fi
```

### Step 2: Start Task

```bash
$TASKCTL task start $TASK_ID
```

### Step 3: Spawn Worker

Spawn the `@worker` agent with task context:

```
Task(@worker, """
TASK_ID: <task-id>
EPIC_ID: <epic-id>
TASKCTL: ${CLAUDE_PLUGIN_ROOT}/plugins/controllers/scripts/taskctl
SPECIALIST_CONTEXT: <appropriate specialist based on task>

Execute task <task-id> following the worker protocol:
1. Re-anchor (read spec, epic, git state)
2. Implement per specification
3. Verify acceptance criteria
4. Commit changes
5. Mark done or request review
""")
```

### Step 4: Handle Result

**If worker returns successfully:**
- Task is marked done
- Report files changed
- Ask if user wants to continue with next task

**If worker requests review (review.enabled = true):**
- Spawn `@qa-auditor` for review
- Handle verdict (SHIP/NEEDS_WORK/MAJOR_RETHINK)
- Loop if NEEDS_WORK

**If worker is blocked:**
- Report blocker to user
- Suggest resolution

### Step 5: Continue or Complete

After task completion:
```bash
# Check for more ready tasks
NEXT=$($TASKCTL task ready --epic $EPIC_ID | head -1)
```

If more tasks ready, ask user if they want to continue.

## Target

$ARGUMENTS
