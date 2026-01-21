#!/usr/bin/env python3
"""
taskctl - Task state management CLI for custom-agents orchestration system.

A zero-dependency CLI tool (stdlib only) for managing epics and tasks
stored in a .tasks/ directory. Integrates with the complexity scoring system.

Usage:
    taskctl init                              Initialize .tasks/ directory
    taskctl status                            Show current state summary
    taskctl epic create "<title>"             Create epic
    taskctl epic list [--status <s>]          List epics
    taskctl epic show <id> [--json]           Show epic details
    taskctl epic cat <id>                     Output spec markdown
    taskctl epic set-status <id> <status>     Update epic status
    taskctl epic delete <id>                  Delete epic and tasks
    taskctl task create <epic-id> "<title>"   Create task
    taskctl task list --epic <id>             List tasks in epic
    taskctl task show <id> [--json]           Show task details
    taskctl task cat <id>                     Output spec markdown
    taskctl task start <id>                   Start task
    taskctl task done <id> [--summary "<s>"]  Complete task
    taskctl task block <id> --reason "<r>"    Block task
    taskctl task set-status <id> <status>     Update task status
    taskctl task set-depends <id> <deps...>   Set dependencies
    taskctl task ready --epic <id>            List ready tasks
    taskctl task delete <id>                  Delete task
    taskctl next                              Get next actionable unit
    taskctl cat <id>                          Smart cat (epic or task)
    taskctl config get <key>                  Get config value
    taskctl config set <key> <value>          Set config value
    taskctl config list                       List all config
    taskctl memory init                       Initialize memory directory
    taskctl memory add --type <t> "<content>" Add memory entry
    taskctl memory list [--type <t>]          List memory entries
    taskctl review init                       Initialize review system
    taskctl review log <id> --verdict <v>     Log review verdict
    taskctl review count <id>                 Count review iterations
    taskctl review list <id>                  List reviews for task
    taskctl review show <id> [--iteration N]  Show review details
"""

import argparse
import json
import os
import secrets
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# Constants
SCHEMA_VERSION = 1
SETUP_VERSION = "1.0.0"
TASKS_DIR = ".tasks"

EPIC_STATUSES = ["planning", "ready", "in_progress", "blocked", "done", "cancelled"]
TASK_STATUSES = ["pending", "in_progress", "blocked", "done", "cancelled"]
MEMORY_TYPES = ["pitfall", "convention", "decision"]
REVIEW_VERDICTS = ["SHIP", "NEEDS_WORK", "MAJOR_RETHINK"]


def now_iso() -> str:
    """Return current UTC time in ISO 8601 format."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def generate_id_suffix() -> str:
    """Generate a 3-character random alphanumeric suffix."""
    return secrets.token_hex(2)[:3]


def find_tasks_root() -> Optional[Path]:
    """Find .tasks/ directory in current working directory only.

    Unlike git which walks up to find .git/, we require .tasks/ to be
    in the current directory. This prevents confusion when running from
    different directories.
    """
    tasks_dir = Path.cwd() / TASKS_DIR
    if tasks_dir.is_dir():
        return tasks_dir
    return None


def require_tasks_root() -> Path:
    """Get tasks root or exit with error."""
    root = find_tasks_root()
    if root is None:
        error("Not in a taskctl project. Run 'taskctl init' first.")
    return root


def msg(text: str) -> None:
    """Print message to stderr."""
    print(text, file=sys.stderr)


def out(text: str) -> None:
    """Print data to stdout."""
    print(text)


def error(text: str, code: int = 1) -> None:
    """Print error and exit."""
    print(f"Error: {text}", file=sys.stderr)
    sys.exit(code)


def read_json(path: Path) -> Dict[str, Any]:
    """Read and parse JSON file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        error(f"File not found: {path}")
    except json.JSONDecodeError as e:
        error(f"Invalid JSON in {path}: {e}")


def write_json(path: Path, data: Dict[str, Any]) -> None:
    """Write data as JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
        f.write("\n")


def read_text(path: Path) -> str:
    """Read text file."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        error(f"File not found: {path}")


def write_text(path: Path, content: str) -> None:
    """Write text file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def get_next_epic_number(root: Path) -> int:
    """Get the next epic sequence number."""
    epics_dir = root / "epics"
    if not epics_dir.exists():
        return 1
    max_num = 0
    for f in epics_dir.glob("ca-*.json"):
        try:
            # Extract number from ca-N-xxx.json
            parts = f.stem.split("-")
            if len(parts) >= 2:
                num = int(parts[1])
                max_num = max(max_num, num)
        except (ValueError, IndexError):
            continue
    return max_num + 1


def get_next_task_number(root: Path, epic_id: str) -> int:
    """Get the next task number for an epic."""
    tasks_dir = root / "tasks"
    if not tasks_dir.exists():
        return 1
    max_num = 0
    for f in tasks_dir.glob(f"{epic_id}.*.json"):
        try:
            # Extract task number from ca-N-xxx.M.json
            parts = f.stem.rsplit(".", 1)
            if len(parts) == 2:
                num = int(parts[1])
                max_num = max(max_num, num)
        except (ValueError, IndexError):
            continue
    return max_num + 1


def parse_id(id_str: str) -> tuple:
    """Parse an ID to determine if it's an epic or task.

    Returns: (type, epic_id, task_num) where type is 'epic' or 'task'
    """
    if "." in id_str:
        parts = id_str.rsplit(".", 1)
        return ("task", parts[0], int(parts[1]))
    return ("epic", id_str, None)


def get_config(root: Path) -> Dict[str, Any]:
    """Get configuration dictionary."""
    config_path = root / "config.json"
    if config_path.exists():
        return read_json(config_path)
    return {}


def set_config(root: Path, config: Dict[str, Any]) -> None:
    """Save configuration dictionary."""
    write_json(root / "config.json", config)


def get_nested_value(d: Dict, key: str) -> Any:
    """Get value using dot notation."""
    keys = key.split(".")
    for k in keys:
        if isinstance(d, dict) and k in d:
            d = d[k]
        else:
            return None
    return d


def set_nested_value(d: Dict, key: str, value: Any) -> None:
    """Set value using dot notation."""
    keys = key.split(".")
    for k in keys[:-1]:
        if k not in d:
            d[k] = {}
        d = d[k]
    # Try to parse value as JSON for complex types
    try:
        parsed = json.loads(value)
        d[keys[-1]] = parsed
    except (json.JSONDecodeError, TypeError):
        # Handle boolean strings
        if value.lower() == "true":
            d[keys[-1]] = True
        elif value.lower() == "false":
            d[keys[-1]] = False
        else:
            d[keys[-1]] = value


# ============================================================================
# Command: init
# ============================================================================

def cmd_init(args: argparse.Namespace) -> None:
    """Initialize .tasks/ directory structure.

    Idempotent - returns success if already exists.
    """
    tasks_dir = Path.cwd() / TASKS_DIR

    if tasks_dir.exists():
        # Already initialized - this is fine
        msg(f"{TASKS_DIR}/ already exists in {Path.cwd()}")
        return

    # Create directory structure
    tasks_dir.mkdir()
    (tasks_dir / "epics").mkdir()
    (tasks_dir / "specs").mkdir()
    (tasks_dir / "tasks").mkdir()

    # Create meta.json
    write_json(tasks_dir / "meta.json", {
        "schema_version": SCHEMA_VERSION,
        "setup_version": SETUP_VERSION
    })

    # Create default config.json
    write_json(tasks_dir / "config.json", {
        "memory": {"enabled": False},
        "review": {"enabled": False}
    })

    msg(f"Initialized {TASKS_DIR}/ directory in {Path.cwd()}")


def cmd_detect(args: argparse.Namespace) -> None:
    """Check if .tasks/ exists in current directory.

    Returns JSON with exists, valid, and path information.
    """
    tasks_dir = Path.cwd() / TASKS_DIR
    exists = tasks_dir.is_dir()

    result = {
        "success": True,
        "exists": exists,
        "valid": False,
        "path": str(tasks_dir) if exists else None,
        "cwd": str(Path.cwd())
    }

    if exists:
        # Check if it's valid (has required subdirs)
        required = ["epics", "specs", "tasks"]
        result["valid"] = all((tasks_dir / d).is_dir() for d in required)

    if args.json:
        print(json.dumps(result))
    else:
        if exists and result["valid"]:
            msg(f"Found valid {TASKS_DIR}/ at {tasks_dir}")
        elif exists:
            msg(f"Found {TASKS_DIR}/ at {tasks_dir} but it's invalid (missing subdirs)")
        else:
            msg(f"No {TASKS_DIR}/ in current directory ({Path.cwd()})")


# ============================================================================
# Command: status
# ============================================================================

def cmd_status(args: argparse.Namespace) -> None:
    """Show current state summary."""
    root = require_tasks_root()

    # Count epics by status
    epic_counts = {s: 0 for s in EPIC_STATUSES}
    epics_dir = root / "epics"
    total_epics = 0

    if epics_dir.exists():
        for f in epics_dir.glob("ca-*.json"):
            epic = read_json(f)
            status = epic.get("status", "planning")
            epic_counts[status] = epic_counts.get(status, 0) + 1
            total_epics += 1

    # Count tasks by status
    task_counts = {s: 0 for s in TASK_STATUSES}
    tasks_dir = root / "tasks"
    total_tasks = 0

    if tasks_dir.exists():
        for f in tasks_dir.glob("ca-*.json"):
            task = read_json(f)
            status = task.get("status", "pending")
            task_counts[status] = task_counts.get(status, 0) + 1
            total_tasks += 1

    # Output summary
    out(f"Project: {root.parent.name}")
    out(f"Tasks root: {root}")
    out("")
    out(f"Epics ({total_epics} total):")
    for status in EPIC_STATUSES:
        if epic_counts[status] > 0:
            out(f"  {status}: {epic_counts[status]}")

    out("")
    out(f"Tasks ({total_tasks} total):")
    for status in TASK_STATUSES:
        if task_counts[status] > 0:
            out(f"  {status}: {task_counts[status]}")


# ============================================================================
# Command: epic
# ============================================================================

def cmd_epic_create(args: argparse.Namespace) -> None:
    """Create a new epic."""
    root = require_tasks_root()

    # Generate ID
    num = get_next_epic_number(root)
    suffix = generate_id_suffix()
    epic_id = f"ca-{num}-{suffix}"

    # Create epic metadata
    epic_data = {
        "id": epic_id,
        "title": args.title,
        "status": "planning",
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "complexity_score": None,
        "task_count": 0,
        "tasks_done": 0
    }

    write_json(root / "epics" / f"{epic_id}.json", epic_data)

    # Create empty spec file
    spec_content = f"# {args.title}\n\n## Overview\n\n## Requirements\n\n## Acceptance Criteria\n"
    write_text(root / "specs" / f"{epic_id}.md", spec_content)

    out(epic_id)


def cmd_epic_list(args: argparse.Namespace) -> None:
    """List epics."""
    root = require_tasks_root()
    epics_dir = root / "epics"

    if not epics_dir.exists():
        return

    epics = []
    for f in sorted(epics_dir.glob("ca-*.json")):
        epic = read_json(f)
        if args.status and epic.get("status") != args.status:
            continue
        epics.append(epic)

    for epic in epics:
        status = epic.get("status", "planning")
        title = epic.get("title", "")
        done = epic.get("tasks_done", 0)
        total = epic.get("task_count", 0)
        out(f"{epic['id']} [{status}] ({done}/{total}) {title}")


def cmd_epic_show(args: argparse.Namespace) -> None:
    """Show epic details."""
    root = require_tasks_root()
    epic_path = root / "epics" / f"{args.id}.json"

    if not epic_path.exists():
        error(f"Epic not found: {args.id}")

    epic = read_json(epic_path)

    if args.json:
        out(json.dumps(epic, indent=2))
    else:
        out(f"ID: {epic['id']}")
        out(f"Title: {epic['title']}")
        out(f"Status: {epic['status']}")
        out(f"Complexity: {epic.get('complexity_score', 'Not set')}")
        out(f"Tasks: {epic.get('tasks_done', 0)}/{epic.get('task_count', 0)} done")
        out(f"Created: {epic['created_at']}")
        out(f"Updated: {epic['updated_at']}")


def cmd_epic_cat(args: argparse.Namespace) -> None:
    """Output epic spec markdown to stdout."""
    root = require_tasks_root()
    spec_path = root / "specs" / f"{args.id}.md"

    if not spec_path.exists():
        error(f"Epic spec not found: {args.id}")

    out(read_text(spec_path).rstrip())


def cmd_epic_set_status(args: argparse.Namespace) -> None:
    """Update epic status."""
    root = require_tasks_root()

    if args.status not in EPIC_STATUSES:
        error(f"Invalid status. Must be one of: {', '.join(EPIC_STATUSES)}")

    epic_path = root / "epics" / f"{args.id}.json"
    if not epic_path.exists():
        error(f"Epic not found: {args.id}")

    epic = read_json(epic_path)
    epic["status"] = args.status
    epic["updated_at"] = now_iso()
    write_json(epic_path, epic)

    msg(f"Status updated: {args.id} -> {args.status}")


def cmd_epic_delete(args: argparse.Namespace) -> None:
    """Delete epic and all its tasks."""
    root = require_tasks_root()

    epic_path = root / "epics" / f"{args.id}.json"
    if not epic_path.exists():
        error(f"Epic not found: {args.id}")

    # Delete epic files
    epic_path.unlink()
    spec_path = root / "specs" / f"{args.id}.md"
    if spec_path.exists():
        spec_path.unlink()

    # Delete all tasks for this epic
    tasks_dir = root / "tasks"
    if tasks_dir.exists():
        for f in tasks_dir.glob(f"{args.id}.*.json"):
            f.unlink()
        for f in tasks_dir.glob(f"{args.id}.*.md"):
            f.unlink()

    msg(f"Deleted: {args.id}")


# ============================================================================
# Command: task
# ============================================================================

def update_epic_task_counts(root: Path, epic_id: str) -> None:
    """Update task counts in epic metadata."""
    epic_path = root / "epics" / f"{epic_id}.json"
    if not epic_path.exists():
        return

    epic = read_json(epic_path)
    tasks_dir = root / "tasks"

    total = 0
    done = 0

    if tasks_dir.exists():
        for f in tasks_dir.glob(f"{epic_id}.*.json"):
            task = read_json(f)
            total += 1
            if task.get("status") == "done":
                done += 1

    epic["task_count"] = total
    epic["tasks_done"] = done
    epic["updated_at"] = now_iso()
    write_json(epic_path, epic)


def cmd_task_create(args: argparse.Namespace) -> None:
    """Create a new task."""
    root = require_tasks_root()

    # Verify epic exists
    epic_path = root / "epics" / f"{args.epic_id}.json"
    if not epic_path.exists():
        error(f"Epic not found: {args.epic_id}")

    # Generate task ID
    task_num = get_next_task_number(root, args.epic_id)
    task_id = f"{args.epic_id}.{task_num}"

    # Create task metadata
    task_data = {
        "id": task_id,
        "epic_id": args.epic_id,
        "title": args.title,
        "status": "pending",
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "started_at": None,
        "completed_at": None,
        "depends_on": [],
        "blocked_by": None,
        "done_summary": None
    }

    write_json(root / "tasks" / f"{task_id}.json", task_data)

    # Create empty spec file
    spec_content = f"# {args.title}\n\n## Description\n\n## Implementation Notes\n"
    write_text(root / "tasks" / f"{task_id}.md", spec_content)

    # Update epic counts
    update_epic_task_counts(root, args.epic_id)

    out(task_id)


def cmd_task_list(args: argparse.Namespace) -> None:
    """List tasks in an epic."""
    root = require_tasks_root()

    if not args.epic:
        error("--epic is required")

    tasks_dir = root / "tasks"
    if not tasks_dir.exists():
        return

    tasks = []
    for f in sorted(tasks_dir.glob(f"{args.epic}.*.json")):
        task = read_json(f)
        if args.status and task.get("status") != args.status:
            continue
        tasks.append(task)

    for task in tasks:
        status = task.get("status", "pending")
        title = task.get("title", "")
        deps = task.get("depends_on", [])
        deps_str = f" (deps: {', '.join(deps)})" if deps else ""
        out(f"{task['id']} [{status}]{deps_str} {title}")


def cmd_task_show(args: argparse.Namespace) -> None:
    """Show task details."""
    root = require_tasks_root()
    task_path = root / "tasks" / f"{args.id}.json"

    if not task_path.exists():
        error(f"Task not found: {args.id}")

    task = read_json(task_path)

    if args.json:
        out(json.dumps(task, indent=2))
    else:
        out(f"ID: {task['id']}")
        out(f"Epic: {task['epic_id']}")
        out(f"Title: {task['title']}")
        out(f"Status: {task['status']}")
        deps = task.get("depends_on", [])
        out(f"Dependencies: {', '.join(deps) if deps else 'None'}")
        if task.get("blocked_by"):
            out(f"Blocked by: {task['blocked_by']}")
        out(f"Created: {task['created_at']}")
        out(f"Updated: {task['updated_at']}")
        if task.get("started_at"):
            out(f"Started: {task['started_at']}")
        if task.get("completed_at"):
            out(f"Completed: {task['completed_at']}")
        if task.get("done_summary"):
            out(f"Summary: {task['done_summary']}")


def cmd_task_cat(args: argparse.Namespace) -> None:
    """Output task spec markdown to stdout."""
    root = require_tasks_root()
    spec_path = root / "tasks" / f"{args.id}.md"

    if not spec_path.exists():
        error(f"Task spec not found: {args.id}")

    out(read_text(spec_path).rstrip())


def cmd_task_start(args: argparse.Namespace) -> None:
    """Start a task (set status to in_progress)."""
    root = require_tasks_root()
    task_path = root / "tasks" / f"{args.id}.json"

    if not task_path.exists():
        error(f"Task not found: {args.id}")

    task = read_json(task_path)
    task["status"] = "in_progress"
    task["started_at"] = now_iso()
    task["updated_at"] = now_iso()
    write_json(task_path, task)

    msg(f"Started: {args.id}")


def cmd_task_done(args: argparse.Namespace) -> None:
    """Complete a task."""
    root = require_tasks_root()
    task_path = root / "tasks" / f"{args.id}.json"

    if not task_path.exists():
        error(f"Task not found: {args.id}")

    task = read_json(task_path)
    task["status"] = "done"
    task["completed_at"] = now_iso()
    task["updated_at"] = now_iso()
    if args.summary:
        task["done_summary"] = args.summary
    write_json(task_path, task)

    # Update epic counts
    update_epic_task_counts(root, task["epic_id"])

    msg(f"Completed: {args.id}")


def cmd_task_block(args: argparse.Namespace) -> None:
    """Block a task."""
    root = require_tasks_root()
    task_path = root / "tasks" / f"{args.id}.json"

    if not task_path.exists():
        error(f"Task not found: {args.id}")

    if not args.reason:
        error("--reason is required")

    task = read_json(task_path)
    task["status"] = "blocked"
    task["blocked_by"] = args.reason
    task["updated_at"] = now_iso()
    write_json(task_path, task)

    msg(f"Blocked: {args.id}")


def cmd_task_set_status(args: argparse.Namespace) -> None:
    """Update task status."""
    root = require_tasks_root()

    if args.status not in TASK_STATUSES:
        error(f"Invalid status. Must be one of: {', '.join(TASK_STATUSES)}")

    task_path = root / "tasks" / f"{args.id}.json"
    if not task_path.exists():
        error(f"Task not found: {args.id}")

    task = read_json(task_path)
    task["status"] = args.status
    task["updated_at"] = now_iso()
    write_json(task_path, task)

    # Update epic counts
    update_epic_task_counts(root, task["epic_id"])

    msg(f"Status updated: {args.id} -> {args.status}")


def cmd_task_set_depends(args: argparse.Namespace) -> None:
    """Set task dependencies."""
    root = require_tasks_root()
    task_path = root / "tasks" / f"{args.id}.json"

    if not task_path.exists():
        error(f"Task not found: {args.id}")

    # Verify all dependencies exist
    for dep_id in args.deps:
        dep_path = root / "tasks" / f"{dep_id}.json"
        if not dep_path.exists():
            error(f"Dependency not found: {dep_id}")

    task = read_json(task_path)
    task["depends_on"] = args.deps
    task["updated_at"] = now_iso()
    write_json(task_path, task)

    msg(f"Dependencies set for {args.id}")


def cmd_task_ready(args: argparse.Namespace) -> None:
    """List tasks ready to start (dependencies resolved)."""
    root = require_tasks_root()

    if not args.epic:
        error("--epic is required")

    tasks_dir = root / "tasks"
    if not tasks_dir.exists():
        return

    # Load all tasks for this epic
    tasks = {}
    for f in tasks_dir.glob(f"{args.epic}.*.json"):
        task = read_json(f)
        tasks[task["id"]] = task

    # Find tasks that are pending and have all deps done
    ready = []
    for task_id, task in tasks.items():
        if task["status"] != "pending":
            continue

        deps_resolved = True
        for dep_id in task.get("depends_on", []):
            dep_task = tasks.get(dep_id)
            if not dep_task or dep_task["status"] != "done":
                deps_resolved = False
                break

        if deps_resolved:
            ready.append(task_id)

    for task_id in sorted(ready):
        out(task_id)


def cmd_task_delete(args: argparse.Namespace) -> None:
    """Delete a task."""
    root = require_tasks_root()
    task_path = root / "tasks" / f"{args.id}.json"

    if not task_path.exists():
        error(f"Task not found: {args.id}")

    task = read_json(task_path)
    epic_id = task["epic_id"]

    # Delete task files
    task_path.unlink()
    spec_path = root / "tasks" / f"{args.id}.md"
    if spec_path.exists():
        spec_path.unlink()

    # Update epic counts
    update_epic_task_counts(root, epic_id)

    msg(f"Deleted: {args.id}")


# ============================================================================
# Command: next
# ============================================================================

def cmd_next(args: argparse.Namespace) -> None:
    """Get next actionable unit (task or epic needing planning)."""
    root = require_tasks_root()

    # First, check for in_progress tasks
    tasks_dir = root / "tasks"
    if tasks_dir.exists():
        for f in sorted(tasks_dir.glob("ca-*.json")):
            task = read_json(f)
            if task["status"] == "in_progress":
                out(f"{task['id']} (in_progress)")
                return

    # Next, check for ready tasks across all epics
    epics_dir = root / "epics"
    if epics_dir.exists():
        for epic_file in sorted(epics_dir.glob("ca-*.json")):
            epic = read_json(epic_file)
            if epic["status"] not in ["ready", "in_progress"]:
                continue

            epic_id = epic["id"]

            # Load all tasks for this epic
            tasks = {}
            if tasks_dir.exists():
                for f in tasks_dir.glob(f"{epic_id}.*.json"):
                    task = read_json(f)
                    tasks[task["id"]] = task

            # Find ready tasks
            for task_id in sorted(tasks.keys()):
                task = tasks[task_id]
                if task["status"] != "pending":
                    continue

                deps_resolved = True
                for dep_id in task.get("depends_on", []):
                    dep_task = tasks.get(dep_id)
                    if not dep_task or dep_task["status"] != "done":
                        deps_resolved = False
                        break

                if deps_resolved:
                    out(f"{task_id} (ready)")
                    return

    # Finally, check for epics needing planning
    if epics_dir.exists():
        for f in sorted(epics_dir.glob("ca-*.json")):
            epic = read_json(f)
            if epic["status"] == "planning":
                out(f"{epic['id']} (needs_planning)")
                return

    msg("No actionable items")


# ============================================================================
# Command: cat (smart)
# ============================================================================

def cmd_cat(args: argparse.Namespace) -> None:
    """Smart cat - works for both epic and task IDs."""
    root = require_tasks_root()

    id_type, epic_id, task_num = parse_id(args.id)

    if id_type == "task":
        spec_path = root / "tasks" / f"{args.id}.md"
    else:
        spec_path = root / "specs" / f"{args.id}.md"

    if not spec_path.exists():
        error(f"Spec not found: {args.id}")

    out(read_text(spec_path).rstrip())


# ============================================================================
# Command: config
# ============================================================================

def cmd_config_get(args: argparse.Namespace) -> None:
    """Get config value."""
    root = require_tasks_root()
    config = get_config(root)
    value = get_nested_value(config, args.key)

    if value is None:
        error(f"Config key not found: {args.key}")

    if isinstance(value, (dict, list)):
        out(json.dumps(value, indent=2))
    else:
        out(str(value))


def cmd_config_set(args: argparse.Namespace) -> None:
    """Set config value."""
    root = require_tasks_root()
    config = get_config(root)
    set_nested_value(config, args.key, args.value)
    set_config(root, config)

    msg(f"Set {args.key} = {args.value}")


def cmd_config_list(args: argparse.Namespace) -> None:
    """List all config."""
    root = require_tasks_root()
    config = get_config(root)
    out(json.dumps(config, indent=2))


# ============================================================================
# Command: memory
# ============================================================================

def cmd_memory_init(args: argparse.Namespace) -> None:
    """Initialize memory directory."""
    root = require_tasks_root()
    memory_dir = root / "memory"

    if memory_dir.exists():
        error("Memory directory already exists")

    memory_dir.mkdir()

    # Create initial files
    write_text(memory_dir / "pitfalls.md", "# Pitfalls\n\nKnown issues and gotchas to avoid.\n\n")
    write_text(memory_dir / "conventions.md", "# Conventions\n\nProject conventions and patterns.\n\n")
    write_text(memory_dir / "decisions.md", "# Decisions\n\nArchitectural and design decisions.\n\n")

    # Enable memory in config
    config = get_config(root)
    if "memory" not in config:
        config["memory"] = {}
    config["memory"]["enabled"] = True
    set_config(root, config)

    msg("Initialized memory directory")


def cmd_memory_add(args: argparse.Namespace) -> None:
    """Add memory entry."""
    root = require_tasks_root()
    memory_dir = root / "memory"

    if not memory_dir.exists():
        error("Memory not initialized. Run 'taskctl memory init' first.")

    if args.type not in MEMORY_TYPES:
        error(f"Invalid type. Must be one of: {', '.join(MEMORY_TYPES)}")

    # Map type to file
    type_files = {
        "pitfall": "pitfalls.md",
        "convention": "conventions.md",
        "decision": "decisions.md"
    }

    file_path = memory_dir / type_files[args.type]

    # Append entry with timestamp
    timestamp = now_iso()
    entry = f"\n## {timestamp}\n\n{args.content}\n"

    with open(file_path, "a", encoding="utf-8") as f:
        f.write(entry)

    msg(f"Added {args.type} entry")


def cmd_memory_list(args: argparse.Namespace) -> None:
    """List memory entries."""
    root = require_tasks_root()
    memory_dir = root / "memory"

    if not memory_dir.exists():
        error("Memory not initialized. Run 'taskctl memory init' first.")

    type_files = {
        "pitfall": "pitfalls.md",
        "convention": "conventions.md",
        "decision": "decisions.md"
    }

    if args.type:
        if args.type not in MEMORY_TYPES:
            error(f"Invalid type. Must be one of: {', '.join(MEMORY_TYPES)}")
        files = [(args.type, type_files[args.type])]
    else:
        files = list(type_files.items())

    for mem_type, filename in files:
        file_path = memory_dir / filename
        if file_path.exists():
            out(f"=== {mem_type.upper()}S ===")
            out(read_text(file_path).rstrip())
            out("")


# ============================================================================
# Command: review
# ============================================================================

def cmd_review_init(args: argparse.Namespace) -> None:
    """Initialize review system."""
    root = require_tasks_root()
    reviews_dir = root / "reviews"

    if reviews_dir.exists():
        error("Reviews directory already exists")

    reviews_dir.mkdir()

    # Enable review in config
    config = get_config(root)
    if "review" not in config:
        config["review"] = {}
    config["review"]["enabled"] = True
    config["review"]["maxIterations"] = 3
    set_config(root, config)

    msg("Initialized review system")


def cmd_review_log(args: argparse.Namespace) -> None:
    """Log a review verdict."""
    root = require_tasks_root()
    reviews_dir = root / "reviews"

    if not reviews_dir.exists():
        error("Review system not initialized. Run 'taskctl review init' first.")

    # Validate verdict
    verdict = args.verdict.upper()
    if verdict not in REVIEW_VERDICTS:
        error(f"Invalid verdict. Must be one of: {', '.join(REVIEW_VERDICTS)}")

    # Validate task ID
    id_type, epic_id, task_num = parse_id(args.task_id)
    if id_type != "task":
        error(f"Expected task ID, got epic ID: {args.task_id}")

    # Create review receipt
    timestamp = now_iso()
    receipt = {
        "type": "impl_review",
        "task_id": args.task_id,
        "epic_id": epic_id,
        "verdict": verdict,
        "reviewer": "qa-auditor",
        "timestamp": timestamp,
        "notes": args.notes or "",
        "iteration": get_review_iteration(root, args.task_id)
    }

    # Save receipt with timestamp in filename
    safe_ts = timestamp.replace(":", "-").replace("T", "_").replace("Z", "")
    receipt_file = reviews_dir / f"{args.task_id}-{safe_ts}.json"
    write_json(receipt_file, receipt)

    msg(f"Logged review: {args.task_id} → {verdict}")

    # If SHIP, capture in memory if enabled
    if verdict == "SHIP":
        config = get_config(root)
        if config.get("memory", {}).get("enabled", False):
            msg("Task approved - consider capturing any learnings with 'taskctl memory add'")


def cmd_review_count(args: argparse.Namespace) -> None:
    """Count review iterations for a task."""
    root = require_tasks_root()
    reviews_dir = root / "reviews"

    if not reviews_dir.exists():
        out("0")
        return

    count = get_review_iteration(root, args.task_id)
    out(str(count))


def cmd_review_list(args: argparse.Namespace) -> None:
    """List reviews for a task."""
    root = require_tasks_root()
    reviews_dir = root / "reviews"

    if not reviews_dir.exists():
        error("Review system not initialized. Run 'taskctl review init' first.")

    # Find all reviews for this task
    pattern = f"{args.task_id}-*.json"
    reviews = sorted(reviews_dir.glob(pattern))

    if not reviews:
        msg(f"No reviews found for {args.task_id}")
        return

    for review_file in reviews:
        review = read_json(review_file)
        out(f"[{review['iteration']}] {review['timestamp']} - {review['verdict']}")
        if review.get('notes'):
            out(f"    {review['notes'][:80]}...")


def cmd_review_show(args: argparse.Namespace) -> None:
    """Show review details."""
    root = require_tasks_root()
    reviews_dir = root / "reviews"

    if not reviews_dir.exists():
        error("Review system not initialized. Run 'taskctl review init' first.")

    # Find latest review for this task
    pattern = f"{args.task_id}-*.json"
    reviews = sorted(reviews_dir.glob(pattern))

    if not reviews:
        error(f"No reviews found for {args.task_id}")

    # Get latest or specified iteration
    if args.iteration:
        target_iter = int(args.iteration)
        review_file = None
        for rf in reviews:
            review = read_json(rf)
            if review.get('iteration') == target_iter:
                review_file = rf
                break
        if not review_file:
            error(f"Review iteration {target_iter} not found for {args.task_id}")
    else:
        review_file = reviews[-1]  # Latest

    review = read_json(review_file)

    if args.json:
        out(json.dumps(review, indent=2))
    else:
        out(f"Task: {review['task_id']}")
        out(f"Verdict: {review['verdict']}")
        out(f"Iteration: {review['iteration']}")
        out(f"Timestamp: {review['timestamp']}")
        out(f"Reviewer: {review['reviewer']}")
        if review.get('notes'):
            out(f"Notes: {review['notes']}")


def get_review_iteration(root: Path, task_id: str) -> int:
    """Get the current review iteration count for a task."""
    reviews_dir = root / "reviews"
    if not reviews_dir.exists():
        return 1

    pattern = f"{task_id}-*.json"
    reviews = list(reviews_dir.glob(pattern))
    return len(reviews) + 1


# ============================================================================
# Main CLI Setup
# ============================================================================

def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="taskctl",
        description="Task state management CLI for custom-agents orchestration"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # init
    subparsers.add_parser("init", help="Initialize .tasks/ directory")

    # detect
    detect_parser = subparsers.add_parser("detect", help="Check if .tasks/ exists")
    detect_parser.add_argument("--json", action="store_true", help="Output as JSON")

    # status
    subparsers.add_parser("status", help="Show current state summary")

    # epic
    epic_parser = subparsers.add_parser("epic", help="Epic management")
    epic_subs = epic_parser.add_subparsers(dest="epic_command")

    epic_create = epic_subs.add_parser("create", help="Create epic")
    epic_create.add_argument("title", help="Epic title")

    epic_list = epic_subs.add_parser("list", help="List epics")
    epic_list.add_argument("--status", help="Filter by status")

    epic_show = epic_subs.add_parser("show", help="Show epic details")
    epic_show.add_argument("id", help="Epic ID")
    epic_show.add_argument("--json", action="store_true", help="Output as JSON")

    epic_cat = epic_subs.add_parser("cat", help="Output spec markdown")
    epic_cat.add_argument("id", help="Epic ID")

    epic_set_status = epic_subs.add_parser("set-status", help="Update epic status")
    epic_set_status.add_argument("id", help="Epic ID")
    epic_set_status.add_argument("status", help="New status")

    epic_delete = epic_subs.add_parser("delete", help="Delete epic")
    epic_delete.add_argument("id", help="Epic ID")

    # task
    task_parser = subparsers.add_parser("task", help="Task management")
    task_subs = task_parser.add_subparsers(dest="task_command")

    task_create = task_subs.add_parser("create", help="Create task")
    task_create.add_argument("epic_id", help="Epic ID")
    task_create.add_argument("title", help="Task title")

    task_list = task_subs.add_parser("list", help="List tasks")
    task_list.add_argument("--epic", help="Epic ID (required)")
    task_list.add_argument("--status", help="Filter by status")

    task_show = task_subs.add_parser("show", help="Show task details")
    task_show.add_argument("id", help="Task ID")
    task_show.add_argument("--json", action="store_true", help="Output as JSON")

    task_cat = task_subs.add_parser("cat", help="Output spec markdown")
    task_cat.add_argument("id", help="Task ID")

    task_start = task_subs.add_parser("start", help="Start task")
    task_start.add_argument("id", help="Task ID")

    task_done = task_subs.add_parser("done", help="Complete task")
    task_done.add_argument("id", help="Task ID")
    task_done.add_argument("--summary", help="Completion summary")

    task_block = task_subs.add_parser("block", help="Block task")
    task_block.add_argument("id", help="Task ID")
    task_block.add_argument("--reason", help="Block reason (required)")

    task_set_status = task_subs.add_parser("set-status", help="Update task status")
    task_set_status.add_argument("id", help="Task ID")
    task_set_status.add_argument("status", help="New status")

    task_set_depends = task_subs.add_parser("set-depends", help="Set dependencies")
    task_set_depends.add_argument("id", help="Task ID")
    task_set_depends.add_argument("deps", nargs="+", help="Dependency task IDs")

    task_ready = task_subs.add_parser("ready", help="List ready tasks")
    task_ready.add_argument("--epic", help="Epic ID (required)")

    task_delete = task_subs.add_parser("delete", help="Delete task")
    task_delete.add_argument("id", help="Task ID")

    # next
    subparsers.add_parser("next", help="Get next actionable unit")

    # cat (smart)
    cat_parser = subparsers.add_parser("cat", help="Smart cat for epic or task")
    cat_parser.add_argument("id", help="Epic or Task ID")

    # config
    config_parser = subparsers.add_parser("config", help="Configuration management")
    config_subs = config_parser.add_subparsers(dest="config_command")

    config_get = config_subs.add_parser("get", help="Get config value")
    config_get.add_argument("key", help="Config key (dot notation)")

    config_set = config_subs.add_parser("set", help="Set config value")
    config_set.add_argument("key", help="Config key (dot notation)")
    config_set.add_argument("value", help="Config value")

    config_subs.add_parser("list", help="List all config")

    # memory
    memory_parser = subparsers.add_parser("memory", help="Memory management")
    memory_subs = memory_parser.add_subparsers(dest="memory_command")

    memory_subs.add_parser("init", help="Initialize memory directory")

    memory_add = memory_subs.add_parser("add", help="Add memory entry")
    memory_add.add_argument("--type", required=True, help="Memory type")
    memory_add.add_argument("content", help="Memory content")

    memory_list = memory_subs.add_parser("list", help="List memory entries")
    memory_list.add_argument("--type", help="Filter by type")

    # review
    review_parser = subparsers.add_parser("review", help="Review management")
    review_subs = review_parser.add_subparsers(dest="review_command")

    review_subs.add_parser("init", help="Initialize review system")

    review_log = review_subs.add_parser("log", help="Log a review verdict")
    review_log.add_argument("task_id", help="Task ID")
    review_log.add_argument("--verdict", required=True, help="Verdict (SHIP, NEEDS_WORK, MAJOR_RETHINK)")
    review_log.add_argument("--notes", help="Review notes")

    review_count = review_subs.add_parser("count", help="Count review iterations")
    review_count.add_argument("task_id", help="Task ID")

    review_list = review_subs.add_parser("list", help="List reviews for a task")
    review_list.add_argument("task_id", help="Task ID")

    review_show = review_subs.add_parser("show", help="Show review details")
    review_show.add_argument("task_id", help="Task ID")
    review_show.add_argument("--iteration", help="Specific iteration number")
    review_show.add_argument("--json", action="store_true", help="Output as JSON")

    # Parse and route
    args = parser.parse_args()

    if args.command is None:
        parser.print_help()
        sys.exit(0)

    # Route to handlers
    if args.command == "init":
        cmd_init(args)
    elif args.command == "detect":
        cmd_detect(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "epic":
        if args.epic_command == "create":
            cmd_epic_create(args)
        elif args.epic_command == "list":
            cmd_epic_list(args)
        elif args.epic_command == "show":
            cmd_epic_show(args)
        elif args.epic_command == "cat":
            cmd_epic_cat(args)
        elif args.epic_command == "set-status":
            cmd_epic_set_status(args)
        elif args.epic_command == "delete":
            cmd_epic_delete(args)
        else:
            epic_parser.print_help()
    elif args.command == "task":
        if args.task_command == "create":
            cmd_task_create(args)
        elif args.task_command == "list":
            cmd_task_list(args)
        elif args.task_command == "show":
            cmd_task_show(args)
        elif args.task_command == "cat":
            cmd_task_cat(args)
        elif args.task_command == "start":
            cmd_task_start(args)
        elif args.task_command == "done":
            cmd_task_done(args)
        elif args.task_command == "block":
            cmd_task_block(args)
        elif args.task_command == "set-status":
            cmd_task_set_status(args)
        elif args.task_command == "set-depends":
            cmd_task_set_depends(args)
        elif args.task_command == "ready":
            cmd_task_ready(args)
        elif args.task_command == "delete":
            cmd_task_delete(args)
        else:
            task_parser.print_help()
    elif args.command == "next":
        cmd_next(args)
    elif args.command == "cat":
        cmd_cat(args)
    elif args.command == "config":
        if args.config_command == "get":
            cmd_config_get(args)
        elif args.config_command == "set":
            cmd_config_set(args)
        elif args.config_command == "list":
            cmd_config_list(args)
        else:
            config_parser.print_help()
    elif args.command == "memory":
        if args.memory_command == "init":
            cmd_memory_init(args)
        elif args.memory_command == "add":
            cmd_memory_add(args)
        elif args.memory_command == "list":
            cmd_memory_list(args)
        else:
            memory_parser.print_help()
    elif args.command == "review":
        if args.review_command == "init":
            cmd_review_init(args)
        elif args.review_command == "log":
            cmd_review_log(args)
        elif args.review_command == "count":
            cmd_review_count(args)
        elif args.review_command == "list":
            cmd_review_list(args)
        elif args.review_command == "show":
            cmd_review_show(args)
        else:
            review_parser.print_help()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
