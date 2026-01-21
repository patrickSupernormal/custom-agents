---
name: custom-agents-work
description: Execute tasks from an epic with worker subagents. Use when implementing a plan via /custom-agents:work.
---

# Custom Agents Work

Execute tasks systematically. Focus on finishing.

**IMPORTANT**: This skill uses `.tasks/` for ALL task tracking. Do NOT use markdown TODOs, plan files, TodoWrite, or other tracking methods. All task state must be read and written via `taskctl`.

**Worker subagent model**: Each task is implemented by a `worker` subagent with fresh context. This prevents context bleed between tasks. The main conversation handles task selection and looping; worker handles implementation, commits, and completion.

## Input

Full request: $ARGUMENTS

Accepts:
- Epic ID `ca-N-xxx` - work through all tasks (EPIC_MODE)
- Task ID `ca-N-xxx.M` - work on single task (SINGLE_TASK_MODE)
- `--yolo` flag - continuous mode without confirmation prompts

## Setup

**CRITICAL: Always use the marketplace path directly.** The `CLAUDE_PLUGIN_ROOT` variable often points to a cache directory that doesn't contain the scripts.

```bash
# Always use this path - it's the source of truth
TASKCTL="/Users/patrickbrosnan/.claude/plugins/marketplaces/custom-agents/plugins/controllers/scripts/taskctl"

# Verify it exists
test -x "$TASKCTL" || echo "ERROR: taskctl not found at $TASKCTL"
```

## Workflow

Read the phases below and execute each in order.

---

## Phase 0: Validate

```bash
pwd
$TASKCTL detect --json
```

If `.tasks/` not found in current directory, stop and inform user to `cd` to project root or run `/custom-agents:init`.

## Phase 1: Parse Input

```bash
# Determine mode from input
# ca-1-471.3 = SINGLE_TASK_MODE (specific task)
# ca-1-471 = EPIC_MODE (all tasks)
# --yolo = continuous without prompts
```

## Phase 2: Validate Epic

```bash
$TASKCTL epic show <EPIC_ID>
$TASKCTL cat <EPIC_ID>
```

If epic not found, stop.

## Phase 3: Task Loop

### 3a. Find Next Task

```bash
$TASKCTL task ready --epic <EPIC_ID>
```

If no ready tasks, go to Phase 4.

### 3b. Start Task

```bash
$TASKCTL task start <TASK_ID>
```

### 3c. Spawn Worker

**YOU MUST USE THE TASK TOOL HERE.**

Spawn a worker subagent. Pass config values only - the worker reads `worker.md` for implementation phases.

```
Task(
  subagent_type: "general-purpose",
  description: "Worker: implement <TASK_TITLE>",
  prompt: """
Implement custom-agents task.

TASK_ID: <task-id>
EPIC_ID: <epic-id>
TASKCTL: <full-path-to-taskctl>

Read the worker protocol at:
/Users/patrickbrosnan/.claude/plugins/marketplaces/custom-agents/plugins/controllers/agents/worker.md

Follow the phases in worker.md exactly. Do not skip re-anchoring.
"""
)
```

**DO NOT put implementation details in the prompt.** Worker reads worker.md.

### 3d. Verify Completion

After worker returns:

```bash
$TASKCTL task show <TASK_ID> --json
```

If status is not `done`, investigate.

### 3e. Loop Control

**SINGLE_TASK_MODE**: Go to Phase 4.

**EPIC_MODE + YOLO**: Return to 3a automatically.

**EPIC_MODE + Interactive**: Ask user "Continue? (yes/no)"

## Phase 4: Complete

```bash
$TASKCTL task list --epic <EPIC_ID>
```

Report:
- Tasks completed
- Tasks remaining
- Suggest next steps

---

## Guardrails

- **Never implement directly** - always spawn worker
- **Never use TodoWrite** - use taskctl
- **Never skip worker spawn** - every task gets its own worker
- **Never put implementation details in worker prompt** - worker reads worker.md
