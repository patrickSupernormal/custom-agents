#!/bin/bash
#
# pre-edit-guard.sh - Enforce re-anchoring before file edits
#
# This hook runs before the Edit tool executes. It ensures that:
# 1. TASK_ID is set (worker has been properly initialized)
# 2. Task is in "in_progress" status (work has started)
#
# Environment variables expected:
#   TASK_ID  - The task being implemented
#   TASKCTL  - Path to taskctl CLI (optional, will try to find)
#
# Exit codes:
#   0 - Allow the edit to proceed
#   1 - Block the edit with error message
#
# Usage: This script is called by Claude Code's hook system.
#        Tool input is passed as JSON on stdin.

set -euo pipefail

# Read stdin (tool input JSON) but we don't need it for this check
# cat > /dev/null

# Skip guard if not in worker context (no TASK_ID means orchestrator/direct use)
if [[ -z "${TASK_ID:-}" ]]; then
    # Not in worker context - allow edit
    # This permits direct edits when not using the task system
    exit 0
fi

# Find taskctl
TASKCTL="${TASKCTL:-}"
if [[ -z "$TASKCTL" ]]; then
    # Try common locations
    if [[ -x "./.claude/plugins/marketplaces/custom-agents/plugins/controllers/scripts/taskctl" ]]; then
        TASKCTL="./.claude/plugins/marketplaces/custom-agents/plugins/controllers/scripts/taskctl"
    elif command -v taskctl &> /dev/null; then
        TASKCTL="taskctl"
    else
        # Can't find taskctl, allow the edit but warn
        echo "Warning: taskctl not found, skipping task state check" >&2
        exit 0
    fi
fi

# Find .tasks directory by walking up from cwd
find_tasks_dir() {
    local dir="$PWD"
    while [[ "$dir" != "/" ]]; do
        if [[ -d "$dir/.tasks" ]]; then
            echo "$dir/.tasks"
            return 0
        fi
        dir=$(dirname "$dir")
    done
    return 1
}

TASKS_DIR=$(find_tasks_dir 2>/dev/null || echo "")
if [[ -z "$TASKS_DIR" ]]; then
    # No task system initialized, allow edit
    exit 0
fi

# Verify task exists and check status
# Use eval to handle TASKCTL that may contain spaces (e.g., "python3 /path/to/script")
TASK_STATUS=$(eval "$TASKCTL" task show "$TASK_ID" --json 2>/dev/null | python3 -c "import sys, json; print(json.load(sys.stdin).get('status', 'unknown'))" 2>/dev/null || echo "unknown")

case "$TASK_STATUS" in
    "in_progress")
        # Task is properly started, allow edit
        exit 0
        ;;
    "pending")
        echo "ERROR: Task $TASK_ID is pending. Start it first with: taskctl task start $TASK_ID" >&2
        exit 1
        ;;
    "blocked")
        echo "ERROR: Task $TASK_ID is blocked. Resolve blocker before editing." >&2
        exit 1
        ;;
    "done"|"cancelled")
        echo "ERROR: Task $TASK_ID is already $TASK_STATUS. Cannot edit completed tasks." >&2
        exit 1
        ;;
    "unknown")
        # Task not found or error - allow edit but warn
        echo "Warning: Could not verify task $TASK_ID status" >&2
        exit 0
        ;;
    *)
        # Unknown status - allow but warn
        echo "Warning: Task $TASK_ID has unexpected status: $TASK_STATUS" >&2
        exit 0
        ;;
esac
