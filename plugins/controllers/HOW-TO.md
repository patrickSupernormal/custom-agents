# Custom Agents Controller System - HOW-TO Guide

A comprehensive guide to using the task orchestration system for drift-free multi-track execution.

## Quick Start

```bash
# 1. Initialize the system in your project
/custom-agents:init

# 2. Plan a feature (creates epic + tasks)
/custom-agents:plan Build a user authentication system with login, registration, and password reset

# 3. Start working on tasks
/custom-agents:work ca-1-abc

# 4. Check progress anytime
/custom-agents:status
```

## Commands Overview

| Command | Purpose | Example |
|---------|---------|---------|
| `/custom-agents:init` | Initialize task system | `/custom-agents:init --memory --review` |
| `/custom-agents:plan` | Create epic from feature request | `/custom-agents:plan Add dark mode toggle` |
| `/custom-agents:work` | Execute tasks with re-anchoring | `/custom-agents:work ca-1-abc --yolo` |
| `/custom-agents:status` | Show system state and progress | `/custom-agents:status ca-1-abc` |
| `/custom-agents:next` | Get next actionable task | `/custom-agents:next --start` |

---

## 1. Initialization

### Basic Setup

```bash
/custom-agents:init
```

This creates:
```
.tasks/
├── config.json      # System configuration
├── epics/           # Epic definitions
├── tasks/           # Task definitions
├── specs/           # Detailed specifications
├── reviews/         # Review audit trail (if enabled)
└── memory/          # Learned patterns (if enabled)
```

### With Optional Features

```bash
# Enable memory system (learns from implementations)
/custom-agents:init --memory

# Enable review gating (QA before completion)
/custom-agents:init --review

# Enable both
/custom-agents:init --memory --review
```

### Configuration

After init, `.tasks/config.json` contains:

```json
{
  "version": "1.0.0",
  "memory": {
    "enabled": false
  },
  "review": {
    "enabled": false,
    "maxIterations": 3
  }
}
```

---

## 2. Planning Features

### Creating an Epic

```bash
/custom-agents:plan <feature description>
```

The planner will:

1. **Score complexity** using signals:
   - Multiple domains (frontend + backend): +2
   - Multiple deliverables: +2
   - Scope keywords (full, complete): +2
   - Sequential workflow: +1
   - Research + implement: +2
   - Quality gates mentioned: +1
   - Multi-page/feature: +2
   - End-to-end flow: +2

2. **Create an epic** with unique ID (e.g., `ca-1-abc`)

3. **Write specification** to `.tasks/specs/ca-1-abc.md`

4. **Decompose into tasks** based on complexity:
   - Score 3-4: 2-3 tasks
   - Score 5+: 5+ component-based tasks

5. **Set dependencies** between tasks

### Example Planning Session

```bash
/custom-agents:plan Build a todo app with categories, priorities, and local storage
```

Output:
```
## Epic Created: ca-1-xyz

**Title:** Todo App with Categories and Priorities
**Complexity Score:** 6 (COMPLEX)

### Tasks Created:
| ID | Title | Depends On |
|----|-------|------------|
| ca-1-xyz.1 | Project setup and dependencies | - |
| ca-1-xyz.2 | Design system tokens | ca-1-xyz.1 |
| ca-1-xyz.3 | UI components (Button, Input, Badge) | ca-1-xyz.2 |
| ca-1-xyz.4 | State management hooks | ca-1-xyz.1 |
| ca-1-xyz.5 | Todo feature components | ca-1-xyz.3, ca-1-xyz.4 |
| ca-1-xyz.6 | App integration | ca-1-xyz.5 |

### Dependency Graph:
ca-1-xyz.1 → ca-1-xyz.2 → ca-1-xyz.3 ─┐
    └────→ ca-1-xyz.4 ────────────────┴→ ca-1-xyz.5 → ca-1-xyz.6

**Next:** Run `/custom-agents:work ca-1-xyz` to start working
```

---

## 3. Executing Work

### Working on an Epic

```bash
/custom-agents:work <epic-id>
```

This finds the next ready task and spawns a worker agent.

### Working on a Specific Task

```bash
/custom-agents:work <task-id>
```

### YOLO Mode (Continuous Execution)

```bash
/custom-agents:work <epic-id> --yolo
```

YOLO mode runs through all tasks continuously without asking for confirmation:
- Automatically advances to next ready task after each completion
- Stops only when: all tasks done, critical error, or MAJOR_RETHINK verdict
- Progress reported after each task
- User can interrupt with Ctrl+C

**Use YOLO mode when:**
- You trust the plan and want hands-off execution
- Working on well-defined, lower-risk features
- Running overnight or during breaks

### Specialist Routing

The worker automatically selects a specialist context based on task content:

| Task Type | Specialist |
|-----------|------------|
| Setup, dependencies | @nextjs-developer |
| Design tokens, theme | @css-architect |
| UI components | @ui-engineer |
| Hooks, state | @react-engineer |
| API, endpoints | @api-architect |
| Database, schema | @database-architect |
| Auth, login | @auth-engineer |
| Tests | @test-engineer |
| Animation | @animation-engineer |

### The Worker Protocol

When a worker is spawned, it follows this protocol:

#### Phase 1: Re-Anchor
- Read the epic spec
- Read the task spec
- Check git status
- Understand current state

#### Phase 2: Implement
- Follow the task specification exactly
- Use appropriate specialist patterns
- Make incremental, testable changes

#### Phase 3: Verify
- Check all acceptance criteria
- Run relevant tests
- Validate implementation

#### Phase 4: Review Loop (if enabled)
If `review.enabled = true`:
- Request review from @qa-auditor
- Handle verdict:
  - **SHIP ✅**: Proceed to completion
  - **NEEDS_WORK 🔧**: Apply fixes, re-submit
  - **MAJOR_RETHINK 🚨**: Escalate to user

#### Phase 5: Complete
- Commit changes with task ID
- Mark task as done
- Report completion

### Continuous Work Mode

After completing a task, you'll be asked:
```
Task ca-1-xyz.1 completed. Next ready task: ca-1-xyz.2
Continue with next task? (yes/no)
```

---

## 4. Checking Status

### Overall Status

```bash
/custom-agents:status
```

Output:
```
## Task System Status

### Configuration
- Memory: enabled
- Review: enabled (max 3 iterations)

### Epics
| ID | Title | Status | Progress |
|----|-------|--------|----------|
| ca-1-xyz | Todo App | in_progress | 2/6 tasks |
| ca-2-def | Auth System | pending | 0/4 tasks |

### Ready Tasks
- ca-1-xyz.3: UI components
- ca-2-def.1: Project setup

### Next Action
Run `/custom-agents:work ca-1-xyz.3` to continue
```

### Epic-Specific Status

```bash
/custom-agents:status ca-1-xyz
```

Output:
```
## Epic: ca-1-xyz - Todo App

### Tasks
| ID | Title | Status | Depends On |
|----|-------|--------|------------|
| ca-1-xyz.1 | Project setup | done | - |
| ca-1-xyz.2 | Design tokens | done | ca-1-xyz.1 |
| ca-1-xyz.3 | UI components | pending | ca-1-xyz.2 ✓ |
| ca-1-xyz.4 | State hooks | pending | ca-1-xyz.1 ✓ |
| ca-1-xyz.5 | Todo components | pending | ca-1-xyz.3, ca-1-xyz.4 |
| ca-1-xyz.6 | Integration | pending | ca-1-xyz.5 |

### Ready Now
- ca-1-xyz.3 (dependencies met)
- ca-1-xyz.4 (dependencies met)
```

---

## 5. Getting Next Task

### Find Next Actionable Task

```bash
/custom-agents:next
```

Output:
```
## Next Actionable Item

**ID:** ca-1-xyz.3
**Type:** task
**Title:** UI components (Button, Input, Badge)

- Epic: ca-1-xyz (Todo App)
- Dependencies: [all met]
- Status: pending (ready to start)

### Suggested Action:
Run `/custom-agents:work ca-1-xyz.3` to start working on this task.
```

### Auto-Start Next Task

```bash
/custom-agents:next --start
```

This automatically invokes `/custom-agents:work` on the next ready task.

---

## 6. Review Gating

When review is enabled, completed tasks go through QA before marking done.

### Verdict System

| Verdict | Meaning | Action |
|---------|---------|--------|
| **SHIP ✅** | Ready for production | Mark task done |
| **NEEDS_WORK 🔧** | Minor fixes needed | Apply fixes, re-review |
| **MAJOR_RETHINK 🚨** | Fundamental issues | Escalate to user |

### Review Flow

```
Worker completes task
        ↓
    QA Review
        ↓
   ┌────┴────┐
   │         │
SHIP    NEEDS_WORK
   │         │
   ↓         ↓
 Done    Fix Issues
            ↓
       Re-submit
            ↓
       QA Review
            ↓
          ...
```

### Review Commands (CLI)

```bash
# Initialize review for a task
taskctl review init <task-id>

# Log a review verdict
taskctl review log <task-id> <SHIP|NEEDS_WORK|MAJOR_RETHINK> --notes "..."

# Check review count
taskctl review count <task-id>

# List all reviews for a task
taskctl review list <task-id>

# Show specific review
taskctl review show <task-id> <iteration>
```

### Review Receipts

Reviews are logged to `.tasks/reviews/`:

```json
{
  "type": "impl_review",
  "task_id": "ca-1-xyz.3",
  "epic_id": "ca-1-xyz",
  "verdict": "NEEDS_WORK",
  "reviewer": "qa-auditor",
  "timestamp": "2024-01-15T10:30:00Z",
  "notes": "Button component missing focus styles",
  "iteration": 1
}
```

---

## 7. Memory System

When memory is enabled, the system learns from implementations.

### What Gets Stored

- Code patterns that worked
- Solutions to common problems
- Project-specific conventions
- Performance optimizations

### Memory Location

```
.tasks/memory/
├── patterns/       # Reusable code patterns
├── solutions/      # Problem-solution pairs
└── conventions/    # Project conventions
```

### Using Memory

Memory scouts automatically:
1. Check memory before implementing
2. Extract patterns after successful implementations
3. Update memory with new learnings

---

## 8. Guard Hooks

Guard hooks enforce workflow rules automatically.

### Available Guards

| Hook | Trigger | Enforcement |
|------|---------|-------------|
| `pre-edit-guard` | Before Edit tool | Task must be in_progress |
| `pre-write-guard` | Before Write tool | Task must be in_progress |
| `post-bash-guard` | After Bash tool | Detects test/build failures |

### How Guards Work

```
Agent tries to edit file
        ↓
  pre-edit-guard.sh
        ↓
   Check TASK_ID set?
        ↓
   Task in_progress?
        ↓
    ┌────┴────┐
   Yes        No
    │         │
    ↓         ↓
 Allow     Block with
 Edit      error message
```

### Installing Hooks

Add to your Claude Code settings (`.claude/settings.json`):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit",
        "hooks": [{
          "type": "command",
          "command": "$CLAUDE_PLUGIN_ROOT/plugins/controllers/hooks/pre-edit-guard.sh"
        }]
      },
      {
        "matcher": "Write",
        "hooks": [{
          "type": "command",
          "command": "$CLAUDE_PLUGIN_ROOT/plugins/controllers/hooks/pre-write-guard.sh"
        }]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{
          "type": "command",
          "command": "$CLAUDE_PLUGIN_ROOT/plugins/controllers/hooks/post-bash-guard.sh"
        }]
      }
    ]
  }
}
```

---

## 9. Best Practices

### Planning

- **Be specific** in feature descriptions
- **Include acceptance criteria** when possible
- **Mention quality requirements** (tests, accessibility)

### Working

- **Let re-anchoring happen** - don't skip reading specs
- **Follow the protocol** - don't jump ahead
- **Commit incrementally** - one task = one commit

### Reviewing

- **Enable review for complex features**
- **Set reasonable maxIterations** (default: 3)
- **Check review history** when debugging

### Status Checks

- **Check status regularly** during long sessions
- **Use epic-specific status** for focused view
- **Use /next** when unsure what to do

---

## 10. Troubleshooting

### "No .tasks directory found"

Run `/custom-agents:init` first.

### "Task not found"

Check the task ID format: `ca-<epic-num>-<hash>.<task-num>`

### "Dependencies not met"

Use `/custom-agents:status <epic-id>` to see dependency graph.

### "Review loop exceeded max iterations"

The task has been reviewed too many times. Options:
1. Increase `maxIterations` in config
2. Manually mark task done
3. Re-plan the task

### Guard hook blocking edits

Ensure:
1. `TASK_ID` environment variable is set
2. Task is started (`taskctl task start <id>`)
3. Task status is `in_progress`

---

## 11. CLI Reference

### Epic Commands

```bash
taskctl epic create "<title>"        # Create new epic
taskctl epic list                    # List all epics
taskctl epic show <epic-id>          # Show epic details
taskctl epic set-status <id> <status> # Update epic status
```

### Task Commands

```bash
taskctl task create <epic-id> "<title>"  # Create task
taskctl task list [--epic <id>]          # List tasks
taskctl task show <task-id>              # Show task details
taskctl task start <task-id>             # Mark in_progress
taskctl task done <task-id>              # Mark completed
taskctl task block <task-id> "<reason>"  # Mark blocked
taskctl task ready [--epic <id>]         # List ready tasks
taskctl task set-depends <id> <dep-id>   # Add dependency
```

### Config Commands

```bash
taskctl config get <key>             # Get config value
taskctl config set <key> <value>     # Set config value
```

### Review Commands

```bash
taskctl review init <task-id>        # Initialize review
taskctl review log <id> <verdict>    # Log verdict
taskctl review count <task-id>       # Count reviews
taskctl review list <task-id>        # List all reviews
taskctl review show <id> <iteration> # Show specific review
```

### Status Commands

```bash
taskctl status                       # Overall status
taskctl next                         # Next actionable item
```

---

## Version

**Plugin:** controllers v2.2.0
**Features:** State management, worker agent, re-anchoring, parallel scouts, memory system, review gating, guard hooks
