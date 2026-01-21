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

```bash
# Find taskctl
TASKCTL="${CLAUDE_PLUGIN_ROOT}/plugins/controllers/scripts/taskctl"

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
