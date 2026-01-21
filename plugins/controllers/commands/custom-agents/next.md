---
name: custom-agents:next
description: Get and optionally start the next actionable task
argument-hint: "[--start]"
---

# Get Next Task

Find the next actionable task and optionally start working on it.

## Execution

**CRITICAL: Always use the marketplace path directly** (not CLAUDE_PLUGIN_ROOT which points to cache):

```bash
TASKCTL="/Users/patrickbrosnan/.claude/plugins/marketplaces/custom-agents/plugins/controllers/scripts/taskctl"

# Verify it exists
test -x "$TASKCTL" || echo "ERROR: taskctl not found at $TASKCTL"

# Get next actionable item
NEXT=$($TASKCTL next)
```

## Output

```markdown
## Next Actionable Item

**ID:** <task-id or epic-id>
**Type:** <task or epic needing planning>
**Title:** <title>

### If Task:
- Epic: <parent epic>
- Dependencies: [all met]
- Status: pending (ready to start)

### Suggested Action:
Run `/custom-agents:work <id>` to start working on this task.
```

**If `--start` argument provided:**

Automatically invoke `/custom-agents:work <task-id>` to begin work.

## Arguments

$ARGUMENTS
