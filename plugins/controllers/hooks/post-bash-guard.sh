#!/bin/bash
#
# post-bash-guard.sh - Monitor and log bash commands in task context
#
# This hook runs after Bash tool executes. It can:
# 1. Log significant commands for audit trail
# 2. Detect potential issues (failed builds, test failures)
# 3. Update task metadata if needed
#
# Environment variables expected:
#   TASK_ID  - The task being implemented (optional)
#   EPIC_ID  - The parent epic (optional)
#   TASKCTL  - Path to taskctl CLI (optional)
#
# The hook receives the tool result on stdin as JSON with format:
#   { "stdout": "...", "stderr": "...", "exitCode": N }
#
# Exit codes:
#   0 - Always allow (this is post-execution, can't block)
#   Non-zero exit doesn't block but may log warnings

set -euo pipefail

# Skip if not in task context
if [[ -z "${TASK_ID:-}" ]]; then
    exit 0
fi

# Read the tool result from stdin
RESULT=$(cat)

# Extract exit code from result (if available)
EXIT_CODE=$(echo "$RESULT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('exitCode', 0))
except:
    print(0)
" 2>/dev/null || echo "0")

# If command failed, we might want to log or warn
if [[ "$EXIT_CODE" != "0" ]]; then
    # Check for common failure patterns
    STDERR=$(echo "$RESULT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(data.get('stderr', ''))
except:
    print('')
" 2>/dev/null || echo "")

    # Detect test failures
    if echo "$STDERR" | grep -qi "test.*fail\|failed.*test\|FAIL:"; then
        echo "Note: Test failure detected in task $TASK_ID context" >&2
    fi

    # Detect build failures
    if echo "$STDERR" | grep -qi "build.*fail\|compilation.*error\|error.*compil"; then
        echo "Note: Build failure detected in task $TASK_ID context" >&2
    fi

    # Detect TypeScript errors
    if echo "$STDERR" | grep -qi "error TS\|typescript.*error"; then
        echo "Note: TypeScript error detected in task $TASK_ID context" >&2
    fi
fi

# Always exit 0 - post hooks shouldn't block
exit 0
