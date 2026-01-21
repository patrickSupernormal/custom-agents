"""
State schema definitions for taskctl.

Provides JSON schemas and validation for:
- Epic metadata
- Task metadata
- Config settings
- Memory entries
"""

from typing import TypedDict, Optional, List, Literal
from datetime import datetime

# Type definitions for better IDE support

EpicStatus = Literal["planning", "ready", "in_progress", "blocked", "done", "cancelled"]
TaskStatus = Literal["pending", "in_progress", "blocked", "done", "cancelled"]
MemoryType = Literal["pitfall", "convention", "decision"]


class EpicSchema(TypedDict):
    id: str
    title: str
    status: EpicStatus
    created_at: str
    updated_at: str
    complexity_score: Optional[int]
    task_count: int
    tasks_done: int


class TaskSchema(TypedDict):
    id: str
    epic_id: str
    title: str
    status: TaskStatus
    created_at: str
    updated_at: str
    started_at: Optional[str]
    completed_at: Optional[str]
    depends_on: List[str]
    blocked_by: Optional[str]
    done_summary: Optional[str]


class ReviewConfigSchema(TypedDict, total=False):
    enabled: bool
    maxIterations: int  # Default 3


class ConfigSchema(TypedDict, total=False):
    memory: dict  # {"enabled": bool}
    review: ReviewConfigSchema  # {"enabled": bool, "maxIterations": int}
    planSync: dict  # {"enabled": bool}


class MetaSchema(TypedDict):
    schema_version: int
    setup_version: str
    created_at: str


# Schema version for migrations
SCHEMA_VERSION = 1
SETUP_VERSION = "1.0.0"

# Valid status values
EPIC_STATUSES: List[EpicStatus] = ["planning", "ready", "in_progress", "blocked", "done", "cancelled"]
TASK_STATUSES: List[TaskStatus] = ["pending", "in_progress", "blocked", "done", "cancelled"]
MEMORY_TYPES: List[MemoryType] = ["pitfall", "convention", "decision"]


def create_epic(id: str, title: str, complexity_score: Optional[int] = None) -> EpicSchema:
    """Create a new epic with default values."""
    now = datetime.utcnow().isoformat() + "Z"
    return {
        "id": id,
        "title": title,
        "status": "planning",
        "created_at": now,
        "updated_at": now,
        "complexity_score": complexity_score,
        "task_count": 0,
        "tasks_done": 0,
    }


def create_task(id: str, epic_id: str, title: str) -> TaskSchema:
    """Create a new task with default values."""
    now = datetime.utcnow().isoformat() + "Z"
    return {
        "id": id,
        "epic_id": epic_id,
        "title": title,
        "status": "pending",
        "created_at": now,
        "updated_at": now,
        "started_at": None,
        "completed_at": None,
        "depends_on": [],
        "blocked_by": None,
        "done_summary": None,
    }


def create_meta() -> MetaSchema:
    """Create metadata for new .tasks/ directory."""
    now = datetime.utcnow().isoformat() + "Z"
    return {
        "schema_version": SCHEMA_VERSION,
        "setup_version": SETUP_VERSION,
        "created_at": now,
    }


def create_default_config() -> ConfigSchema:
    """Create default configuration."""
    return {
        "memory": {"enabled": False},
        "review": {"enabled": False, "maxIterations": 3},
        "planSync": {"enabled": False},
    }


def validate_epic_status(status: str) -> bool:
    """Check if status is valid for epics."""
    return status in EPIC_STATUSES


def validate_task_status(status: str) -> bool:
    """Check if status is valid for tasks."""
    return status in TASK_STATUSES


def validate_memory_type(memory_type: str) -> bool:
    """Check if memory type is valid."""
    return memory_type in MEMORY_TYPES


def parse_task_id(task_id: str) -> tuple[str, int]:
    """
    Parse task ID into epic ID and task number.

    Args:
        task_id: Task ID like "ca-1-abc.2"

    Returns:
        Tuple of (epic_id, task_number) like ("ca-1-abc", 2)

    Raises:
        ValueError: If task ID format is invalid
    """
    if "." not in task_id:
        raise ValueError(f"Invalid task ID format: {task_id}")

    parts = task_id.rsplit(".", 1)
    if len(parts) != 2:
        raise ValueError(f"Invalid task ID format: {task_id}")

    epic_id, task_num_str = parts
    try:
        task_num = int(task_num_str)
    except ValueError:
        raise ValueError(f"Invalid task number in ID: {task_id}")

    return epic_id, task_num


def is_epic_id(id: str) -> bool:
    """Check if ID is an epic ID (no dot)."""
    return "." not in id and id.startswith("ca-")


def is_task_id(id: str) -> bool:
    """Check if ID is a task ID (has dot)."""
    return "." in id and id.startswith("ca-")
