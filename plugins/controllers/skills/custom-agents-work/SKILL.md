---
name: custom-agents-work
description: Execute tasks from an epic with worker subagents. Use when implementing a plan via /custom-agents:work.
---

# Custom Agents Work

Execute tasks systematically using worker subagents. Each task gets a fresh worker context.

**CRITICAL: This skill uses `.tasks/` for ALL task tracking. Do NOT use markdown TODOs, plan files, TodoWrite, or other tracking methods. All task state must be read and written via `taskctl`.**

**HARD REQUIREMENT: You MUST spawn a worker subagent for each task using the Task tool. NEVER implement tasks directly in the main thread.**

## Input

Full request: $ARGUMENTS

Accepts:
- Epic ID `ca-N-xxx` - work through all tasks (EPIC_MODE)
- Task ID `ca-N-xxx.M` - work on single task (SINGLE_TASK_MODE)
- `--yolo` flag - continuous mode without confirmation prompts

Examples:
- `/custom-agents:work ca-1-471`
- `/custom-agents:work ca-1-471.3`
- `/custom-agents:work ca-1-471 --yolo`

## Setup

**CRITICAL: taskctl is BUNDLED — NOT installed globally.** Always use the full path:

```bash
TASKCTL="${CLAUDE_PLUGIN_ROOT}/plugins/controllers/scripts/taskctl"
```

If CLAUDE_PLUGIN_ROOT is not set, use the marketplace path:
```bash
TASKCTL="/Users/patrickbrosnan/.claude/plugins/marketplaces/custom-agents/plugins/controllers/scripts/taskctl"
```

## Phase 1: Parse Input

```bash
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

## Phase 2: Validate

```bash
# Verify epic exists
$TASKCTL epic show $EPIC_ID

# Read spec for context
$TASKCTL cat $EPIC_ID
```

If epic not found, inform user and stop.

## Phase 3: Task Loop

**For each task**, you MUST spawn a worker subagent with fresh context.

### 3a. Find Next Task

```bash
TASK_ID=$($TASKCTL task ready --epic $EPIC_ID | head -1)
```

If no ready tasks, go to Phase 4 (Complete).

### 3b. Get Task Details

```bash
$TASKCTL task show $TASK_ID
TASK_TITLE=$($TASKCTL task show $TASK_ID --json | python3 -c "import sys,json; print(json.load(sys.stdin).get('title',''))")
```

### 3c. Determine Specialist Context

Based on task title, determine which specialist patterns the worker should follow:

| Task Contains | SPECIALIST_CONTEXT |
|--------------|-------------------|
| "setup", "init", "project", "dependencies" | nextjs-developer |
| "design", "tokens", "theme", "colors", "css" | css-architect |
| "component", "UI", "Button", "Input", "Badge" | ui-engineer |
| "hook", "state", "context", "store", "management" | react-engineer |
| "form", "validation" | react-engineer |
| "api", "endpoint", "fetch" | api-architect |
| "database", "schema", "query" | database-architect |
| "auth", "login", "session" | auth-engineer |
| "test", "spec" | test-engineer |
| "animation", "motion" | animation-engineer |
| default | react-engineer |

### 3d. Start Task

```bash
$TASKCTL task start $TASK_ID
```

### 3e. Spawn Worker (MANDATORY)

**YOU MUST USE THE TASK TOOL TO SPAWN A WORKER SUBAGENT.**

Do NOT skip this step. Do NOT implement directly.

Use the Task tool with `subagent_type: "general-purpose"`:

```
Task(
  description: "Worker: <task-title>",
  subagent_type: "general-purpose",
  prompt: """
You are the worker agent executing a task with strict re-anchoring protocol.

## Context
TASK_ID: <task-id>
EPIC_ID: <epic-id>
TASKCTL: <full-path-to-taskctl>
SPECIALIST_CONTEXT: <determined-specialist>

## Worker Protocol

### Phase 1: Re-Anchor (MANDATORY)
1. Read the epic spec: `$TASKCTL cat $EPIC_ID`
2. Read task details: `$TASKCTL task show $TASK_ID`
3. Check git status: `git status && git log -3 --oneline`

### Phase 2: Implement
Follow the SPECIALIST_CONTEXT patterns to implement:
- <task-title>

Implementation rules:
- Implement ONLY what the spec requires - no extras
- Follow existing patterns in the codebase
- Write production-ready code

### Phase 3: Verify
- Re-read acceptance criteria
- Run relevant tests if applicable
- Check for obvious issues

### Phase 4: Commit
```bash
git add -A
git commit -m "feat(<task-id>): <description>"
```

### Phase 5: Complete
```bash
$TASKCTL task done $TASK_ID
```

### Return Summary
Return a summary with:
- What was implemented
- Files changed
- Any issues encountered
"""
)
```

### 3f. Verify Completion

After worker returns, verify task completed:

```bash
$TASKCTL task show $TASK_ID --json
```

If status is not `done`, investigate and report issue.

### 3g. Loop Control

**SINGLE_TASK_MODE**: After task completes, go to Phase 4.

**EPIC_MODE + YOLO**: Automatically continue to 3a for next task.

**EPIC_MODE + Interactive**: Ask user "Continue with next task? (yes/no)"
- If yes: return to 3a
- If no: go to Phase 4

## Phase 4: Complete

When all tasks done or stopped:

```bash
# Show final status
$TASKCTL task list --epic $EPIC_ID
```

Report:
- Tasks completed
- Tasks remaining (if any)
- Any blocked tasks
- Suggest next steps

## Guardrails

- **NEVER implement tasks directly** - always spawn worker
- **NEVER use TodoWrite** - use taskctl
- **NEVER skip re-anchoring** - workers must read specs first
- **NEVER leave tasks half-done** - verify completion

## Anti-Patterns (VIOLATIONS)

```
WRONG: Main thread reads files, edits code, commits
RIGHT: Main thread spawns worker, worker does implementation

WRONG: Using TodoWrite for tracking
RIGHT: Using taskctl for all task state

WRONG: Skipping to next task without spawning worker
RIGHT: Every task gets its own worker subagent
```
