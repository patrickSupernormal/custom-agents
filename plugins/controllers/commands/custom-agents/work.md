---
name: custom-agents:work
description: Execute tasks from an epic with re-anchoring and optional review
argument-hint: "<epic-id or task-id> [--yolo]"
---

# Execute Work

Execute tasks from an epic or a specific task using the worker agent with re-anchoring.

## Prerequisites

- `.tasks/` must exist
- Epic/tasks must be created via `/custom-agents:plan`

## Arguments

- `<epic-id>` (e.g., `ca-1-471`) - Execute all tasks in epic (EPIC_MODE)
- `<task-id>` (e.g., `ca-1-471.2`) - Execute single task (SINGLE_TASK_MODE)
- `--yolo` - Continuous mode: run all tasks without stopping for confirmation

## Process

### Step 1: Parse Arguments & Mode

```bash
TASKCTL="${CLAUDE_PLUGIN_ROOT}/plugins/controllers/scripts/taskctl"

# Check for --yolo flag
YOLO_MODE=false
if [[ "$ARGUMENTS" == *"--yolo"* ]]; then
    YOLO_MODE=true
fi

# Extract ID (remove flags)
TARGET_ID=$(echo "$ARGUMENTS" | sed 's/--yolo//g' | xargs)

# Determine mode
if [[ "$TARGET_ID" == ca-*-*.* ]]; then
    MODE="SINGLE_TASK"
    TASK_ID="$TARGET_ID"
    EPIC_ID=$(echo "$TARGET_ID" | sed 's/\.[0-9]*$//')
else
    MODE="EPIC"
    EPIC_ID="$TARGET_ID"
fi
```

### Step 2: Task Loop

**EPIC_MODE**: Loop through all ready tasks until none remain.
**SINGLE_TASK_MODE**: Execute only the specified task, then stop.

```
while true:
    1. Find next ready task (or use specified task in SINGLE_TASK_MODE)
    2. Start task
    3. Determine specialist context from task title
    4. Spawn worker with specialist context
    5. Verify completion
    6. If SINGLE_TASK_MODE: break
    7. If EPIC_MODE + YOLO: continue to next task
    8. If EPIC_MODE + !YOLO: ask user to continue
```

### Step 3: Specialist Routing

Determine `SPECIALIST_CONTEXT` based on task title/content:

| Task Contains | Specialist |
|--------------|------------|
| "setup", "init", "project", "dependencies" | nextjs-developer |
| "design", "tokens", "theme", "colors" | css-architect |
| "component", "UI", "Button", "Input" | ui-engineer |
| "hook", "state", "context", "store" | react-engineer |
| "form", "validation" | react-engineer |
| "api", "endpoint", "fetch" | api-architect |
| "database", "schema", "query" | database-architect |
| "auth", "login", "session" | auth-engineer |
| "test", "spec" | test-engineer |
| "animation", "motion" | animation-engineer |
| default | react-engineer |

### Step 4: Spawn Worker

For each task, spawn the `@worker` agent:

```
Task(@worker, """
TASK_ID: <task-id>
EPIC_ID: <epic-id>
TASKCTL: ${CLAUDE_PLUGIN_ROOT}/plugins/controllers/scripts/taskctl
SPECIALIST_CONTEXT: <determined from routing>

Execute this task following your worker protocol phases exactly.
""")
```

**Worker responsibilities:**
- Re-anchor (read spec, epic, git state)
- Implement per specification using specialist patterns
- Verify acceptance criteria
- Commit changes
- Mark done via taskctl

### Step 5: Handle Result

**If worker returns successfully:**
- Verify task status is `done`
- Log files changed

**If worker requests review (review.enabled = true):**
- Spawn `@qa-auditor` for review
- Handle verdict:
  - SHIP ✅ → continue
  - NEEDS_WORK 🔧 → worker fixes, re-review
  - MAJOR_RETHINK 🚨 → stop, report to user

**If worker is blocked:**
- Report blocker
- In YOLO mode: skip to next task
- In interactive mode: ask user

### Step 6: Loop Control

**SINGLE_TASK_MODE:**
- After task completes, stop and report

**EPIC_MODE + YOLO:**
- Automatically continue to next ready task
- Stop only when:
  - No more ready tasks
  - MAJOR_RETHINK verdict
  - Unrecoverable error
- Report progress after each task

**EPIC_MODE + Interactive:**
- After each task, ask: "Continue with next task? (yes/no)"
- Stop if user says no

### Step 7: Completion

When all tasks done or stopped:
- Show epic progress summary
- List any blocked/pending tasks
- Suggest next steps

## YOLO Mode Notes

When `--yolo` is specified:
- No confirmation prompts between tasks
- Runs until all tasks complete or critical error
- Progress reported after each task
- User can interrupt with Ctrl+C

## Target

$ARGUMENTS
