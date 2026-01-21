---
name: custom-agents:status
description: Show current task system state and progress
argument-hint: "[epic-id]"
---

# Show Status

Display the current state of the task management system.

## Execution

**CRITICAL: Always use the marketplace path directly** (not CLAUDE_PLUGIN_ROOT which points to cache):

```bash
TASKCTL="/Users/patrickbrosnan/.claude/plugins/marketplaces/custom-agents/plugins/controllers/scripts/taskctl"

# Verify it exists
test -x "$TASKCTL" || echo "ERROR: taskctl not found at $TASKCTL"

# Overall status
$TASKCTL status
```

**If epic-id provided:**
```bash
$TASKCTL epic show $ARGUMENTS
$TASKCTL task list --epic $ARGUMENTS
```

## Output Format

```markdown
## Task System Status

### Configuration
- Memory: [enabled/disabled]
- Review: [enabled/disabled]

### Epics
| ID | Title | Status | Progress |
|----|-------|--------|----------|
| ca-1-abc | Epic title | in_progress | 3/5 tasks |

### Current Epic: <epic-id> (if specified)

#### Tasks
| ID | Title | Status | Depends On |
|----|-------|--------|------------|
| ca-1-abc.1 | Task 1 | done | - |
| ca-1-abc.2 | Task 2 | in_progress | ca-1-abc.1 |
| ca-1-abc.3 | Task 3 | pending | ca-1-abc.2 |

### Ready Tasks
<List of tasks ready to work on>

### Next Action
<Suggested next step>
```

## Target

$ARGUMENTS
