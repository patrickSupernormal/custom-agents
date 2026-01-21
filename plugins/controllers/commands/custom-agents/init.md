---
name: custom-agents:init
description: Initialize the task management system in current project
argument-hint: "[--memory] [--review]"
---

# Initialize Custom-Agents Task System

Initialize the `.tasks/` directory for task and epic management.

## What This Does

1. Creates `.tasks/` directory structure
2. Copies taskctl to `.tasks/bin/` for project-local usage
3. Optionally enables memory system (`--memory`)
4. Optionally enables review gating (`--review`)

## Step 0: Resolve Plugin Path

The plugin root is the parent of this command's directory. From this file's location, go up to find `scripts/` and `.claude-plugin/`.

Example: if this file is at `~/.claude/plugins/cache/.../custom-agents/2.2.0/plugins/controllers/commands/custom-agents/init.md`, then plugin root is `~/.claude/plugins/cache/.../custom-agents/2.2.0/plugins/controllers/`.

Store this as `PLUGIN_ROOT` for use in later steps.

## Step 1: Create Directory Structure

```bash
mkdir -p .tasks/epics .tasks/specs .tasks/tasks .tasks/bin
```

## Step 2: Copy Files

**IMPORTANT: Copy using absolute paths from PLUGIN_ROOT:**

```bash
# Copy taskctl CLI
cp "${PLUGIN_ROOT}/scripts/taskctl.py" .tasks/bin/taskctl.py
chmod +x .tasks/bin/taskctl.py

# Create wrapper script
cat > .tasks/bin/taskctl << 'EOF'
#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 "$DIR/taskctl.py" "$@"
EOF
chmod +x .tasks/bin/taskctl

# Copy worker protocol
cp "${PLUGIN_ROOT}/agents/worker.md" .tasks/worker.md
```

## Step 3: Create Config Files

Create `.tasks/meta.json`:
```json
{
  "schema_version": 1,
  "setup_version": "1.0.0"
}
```

Create `.tasks/config.json`:
```json
{
  "memory": {"enabled": false},
  "review": {"enabled": false}
}
```

## Step 4: Optional Features

**If `--memory` in arguments:**
```bash
.tasks/bin/taskctl memory init
```

**If `--review` in arguments:**
```bash
.tasks/bin/taskctl review init
```

## Step 5: Report to User

```
Custom-Agents initialized!

Created:
- .tasks/bin/taskctl (CLI tool)
- .tasks/bin/taskctl.py
- .tasks/worker.md (worker protocol)
- .tasks/epics/
- .tasks/specs/
- .tasks/tasks/

Configuration:
- Memory: <enabled|disabled>
- Review: <enabled|disabled>

Next steps:
- Run /custom-agents:plan <feature> to create your first epic
- Use .tasks/bin/taskctl --help for CLI usage
```

## Arguments

$ARGUMENTS
