---
name: custom-agents:init
description: Initialize the task management system in current project
argument-hint: "[--memory] [--review]"
---

# Initialize Custom-Agents Task System

Initialize the `.tasks/` directory for task and epic management.

## What This Does

1. Creates `.tasks/` directory structure
2. Optionally enables memory system (`--memory`)
3. Optionally enables review gating (`--review`)

## Execution

**CRITICAL: Always use the marketplace path directly** (not CLAUDE_PLUGIN_ROOT which points to cache):

```bash
TASKCTL="/Users/patrickbrosnan/.claude/plugins/marketplaces/custom-agents/plugins/controllers/scripts/taskctl"

# Verify it exists
test -x "$TASKCTL" || echo "ERROR: taskctl not found at $TASKCTL"

# Initialize
$TASKCTL init
```

**If `--memory` argument provided:**
```bash
$TASKCTL memory init
```

**If `--review` argument provided:**
```bash
$TASKCTL review init
```

## After Initialization

Report to user:
- `.tasks/` directory created
- Which optional features were enabled
- Suggest running `/custom-agents:plan` to create first epic

## Arguments

$ARGUMENTS
