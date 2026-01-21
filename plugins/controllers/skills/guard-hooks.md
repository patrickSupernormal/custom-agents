---
skill: guard-hooks
version: "1.0.0"
description: "Workflow enforcement hooks that validate task state before tool execution"
used-by:
  - worker
  - orchestrator
  - all-agents
requires:
  - taskctl
---

# Guard Hooks Skill

## Purpose

Enforce workflow rules by intercepting tool calls. Guard hooks ensure that:
- Workers have properly re-anchored before editing files
- Tasks are in the correct state before modifications
- Build/test failures are detected and logged

## How Hooks Work

Claude Code supports hooks that run before (PreToolUse) and after (PostToolUse) tool execution:

```
┌─────────────────────────────────────────────────────────────────┐
│                         HOOK FLOW                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│   Agent calls Edit tool                                          │
│         │                                                        │
│         ▼                                                        │
│   PreToolUse hook runs                                           │
│         │                                                        │
│    ┌────┴────┐                                                   │
│    ▼         ▼                                                   │
│  Exit 0    Exit 1+                                               │
│    │         │                                                   │
│    ▼         ▼                                                   │
│  Tool     Tool BLOCKED                                           │
│  executes  (error shown)                                         │
│    │                                                             │
│    ▼                                                             │
│  PostToolUse hook runs                                           │
│    │                                                             │
│    ▼                                                             │
│  Result returned to agent                                        │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Available Guards

### pre-edit-guard.sh

**Triggers:** Before `Edit` tool execution

**Checks:**
1. Is `TASK_ID` environment variable set?
2. Is the task in `in_progress` status?

**Blocks when:**
- Task is `pending` (must start first)
- Task is `blocked` (must resolve blocker)
- Task is `done` or `cancelled` (can't edit completed tasks)

**Allows when:**
- No `TASK_ID` set (not in worker context)
- Task is `in_progress`
- No `.tasks/` directory (task system not initialized)

### pre-write-guard.sh

**Triggers:** Before `Write` tool execution

**Checks:** Same as pre-edit-guard.sh

**Purpose:** Prevents creating new files without proper task context

### post-bash-guard.sh

**Triggers:** After `Bash` tool execution

**Detects:**
- Test failures (grep for "test fail" patterns)
- Build failures (grep for "build fail" patterns)
- TypeScript errors (grep for "error TS" patterns)

**Purpose:** Logs warnings when commands fail, helping catch issues early

## Installation

### Option 1: Project-Level Hooks

Add to your project's `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/custom-agents/plugins/controllers/hooks/pre-edit-guard.sh"
          }
        ]
      },
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/custom-agents/plugins/controllers/hooks/pre-write-guard.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/custom-agents/plugins/controllers/hooks/post-bash-guard.sh"
          }
        ]
      }
    ]
  }
}
```

### Option 2: Global Hooks

Add to `~/.claude/settings.json` for all projects.

### Option 3: Selective Activation

Only enable specific hooks:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/pre-edit-guard.sh"
          }
        ]
      }
    ]
  }
}
```

## Environment Variables

Guards expect these environment variables (set by worker spawn):

| Variable | Required | Description |
|----------|----------|-------------|
| `TASK_ID` | No | Current task ID (e.g., ca-1-abc.2) |
| `EPIC_ID` | No | Parent epic ID (e.g., ca-1-abc) |
| `TASKCTL` | No | Path to taskctl CLI |

**If `TASK_ID` is not set, guards allow the operation** - this permits direct tool use outside the task system.

## Hook Behavior by Context

| Context | TASK_ID | Guard Behavior |
|---------|---------|----------------|
| Orchestrator | Not set | Allow (no task context) |
| Worker | Set | Check task status |
| Direct user | Not set | Allow (no task context) |
| Specialist agent | Depends | Check if set by spawner |

## Error Messages

### "Task is pending"
```
ERROR: Task ca-1-abc.2 is pending. Start it first with: taskctl task start ca-1-abc.2
```
**Fix:** Run `taskctl task start <task-id>` before implementing

### "Task is blocked"
```
ERROR: Task ca-1-abc.2 is blocked. Resolve blocker before editing.
```
**Fix:** Check blocker with `taskctl task show <task-id>` and resolve

### "Task is already done"
```
ERROR: Task ca-1-abc.2 is already done. Cannot edit completed tasks.
```
**Fix:** Create a new task for additional changes

## Customizing Guards

### Adding New Checks

Edit the guard scripts to add custom validation:

```bash
# Example: Block edits to certain directories
FILE_PATH=$(echo "$INPUT" | jq -r '.file_path // ""')
if [[ "$FILE_PATH" == *"/node_modules/"* ]]; then
    echo "ERROR: Cannot edit files in node_modules" >&2
    exit 1
fi
```

### Creating New Guards

1. Create script in `plugins/controllers/hooks/`
2. Make it executable: `chmod +x script.sh`
3. Add to hooks.json or settings.json
4. Script receives tool input as JSON on stdin
5. Exit 0 to allow, non-zero to block

### Guard Template

```bash
#!/bin/bash
set -euo pipefail

# Read tool input
INPUT=$(cat)

# Your validation logic here
# ...

# Allow
exit 0

# Or block
# echo "ERROR: Reason" >&2
# exit 1
```

## Integration with Task System

### Worker Spawn with Guards

When spawning a worker, set environment variables:

```markdown
Task(@worker, """
TASK_ID: ca-1-abc.2
EPIC_ID: ca-1-abc
TASKCTL: $PLUGIN_ROOT/plugins/controllers/scripts/taskctl

Implement the task...
""")
```

The guards will then validate task state before allowing edits.

### Guard + Review Flow

```
Worker starts task
    │
    ▼
taskctl task start ca-1-abc.2
    │
    ▼
Guard checks: status = in_progress ✓
    │
    ▼
Worker edits files (guards allow)
    │
    ▼
Worker commits
    │
    ▼
QA Review → SHIP
    │
    ▼
taskctl task done ca-1-abc.2
    │
    ▼
Guard checks: status = done ✗
    │
    ▼
Further edits blocked
```

## Troubleshooting

### Guard Not Running

1. Check hook is in settings.json
2. Verify script is executable: `chmod +x script.sh`
3. Test script directly: `echo '{}' | ./script.sh`

### Guard Always Blocking

1. Check if TASK_ID is set correctly
2. Verify task status: `taskctl task show <id>`
3. Start task if pending: `taskctl task start <id>`

### Guard Always Allowing

1. Ensure TASK_ID environment variable is passed to worker
2. Check .tasks/ directory exists
3. Verify taskctl is findable

## Disabling Guards

### Temporarily

Unset TASK_ID in the session:
```bash
unset TASK_ID
```

### Permanently

Remove hooks from settings.json

### Per-Project

Use project `.claude/settings.json` without hooks while global has them

## Anti-Patterns

1. **Bypassing guards by unsetting TASK_ID**
   - If you need to edit outside task context, do it intentionally

2. **Adding blocking post-hooks**
   - Post-hooks run after execution, blocking is pointless

3. **Guards that call external APIs**
   - Hooks should be fast and offline-capable

4. **Overly strict guards**
   - Allow reasonable flexibility, block obvious violations

## Files Reference

```
plugins/controllers/hooks/
├── hooks.json           # Reference configuration
├── pre-edit-guard.sh    # Validates before Edit
├── pre-write-guard.sh   # Validates before Write
└── post-bash-guard.sh   # Monitors after Bash
```
