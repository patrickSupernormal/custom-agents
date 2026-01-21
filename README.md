# Custom Agents

Custom orchestration agents and skills for Claude Code development workflow.

## Quick Start

```bash
# Initialize task system in your project
/custom-agents:init

# Plan a feature (creates epic + tasks)
/custom-agents:plan Build a user authentication system

# Start working on tasks
/custom-agents:work ca-1-abc

# Check progress
/custom-agents:status
```

## Architecture

Claude Code uses a **2-tier architecture**:
- **Main Thread (Orchestrator)**: Routes tasks to specialists, never implements directly
- **Specialist Agents**: Perform actual implementation work

There are no intermediate "controller" agents - subagents cannot spawn other subagents.

## Slash Commands

| Command | Description |
|---------|-------------|
| `/custom-agents:init` | Initialize task system with optional `--memory` and `--review` flags |
| `/custom-agents:plan` | Create epic with decomposed tasks from a feature request |
| `/custom-agents:work` | Execute tasks using worker agent with re-anchoring |
| `/custom-agents:status` | Show system state and progress |
| `/custom-agents:next` | Get next actionable task (with optional `--start`) |

## Plugins

| Plugin | Agents | Description |
|--------|--------|-------------|
| **controllers** | 1 | Orchestration system with taskctl, worker agent, and skills |
| **frontend** | 15+ | Frontend/UI development specialists |
| **backend** | 15+ | Backend/API development specialists |
| **creative** | 12+ | Design, content, and creative specialists |
| **discovery** | 17+ | Research, planning, analysis, and scout specialists |
| **devops** | 10+ | DevOps, testing, and quality specialists |
| **utilities** | 15+ | Cross-cutting utility specialists |

## Controllers Plugin (v2.2.0)

The controllers plugin provides a complete task orchestration system:

### Features

| Feature | Description |
|---------|-------------|
| **taskctl CLI** | Epic/task state management with dependencies |
| **Worker Agent** | Re-anchoring protocol for drift-free execution |
| **Review Gating** | QA verdicts (SHIP/NEEDS_WORK/MAJOR_RETHINK) |
| **Guard Hooks** | Workflow enforcement via PreToolUse/PostToolUse |
| **Parallel Scouts** | Token-efficient codebase exploration |
| **Memory System** | Pattern learning from implementations |

### Task Lifecycle

```
/custom-agents:init     →  Create .tasks/ directory
        ↓
/custom-agents:plan     →  Epic + decomposed tasks
        ↓
/custom-agents:work     →  Worker executes with re-anchoring
        ↓
    [Review Loop]       →  QA verdict (if enabled)
        ↓
/custom-agents:status   →  Track progress
```

### Worker Protocol

The worker agent follows a strict re-anchoring protocol:

1. **Re-Anchor**: Read epic spec, task spec, git state
2. **Implement**: Follow specification exactly
3. **Verify**: Check acceptance criteria
4. **Review**: Submit for QA (if enabled)
5. **Complete**: Commit and mark done

## Orchestration System

### 5-Phase Multi-Track Orchestration

For complex tasks, the system uses a sophisticated 5-phase approach:

```
ASSESS → DECOMPOSE → EXECUTE → SYNTHESIZE → FOLLOW-UP
```

1. **ASSESS**: Detect complexity, determine orchestration mode
2. **DECOMPOSE**: Break into component-based tracks
3. **EXECUTE**: Spawn agents per track in parallel waves
4. **SYNTHESIZE**: Combine outputs into cohesive deliverables
5. **FOLLOW-UP**: Auto-spawn quality agents until complete

### Complexity Modes

| Mode | Score | Action |
|------|-------|--------|
| SIMPLE | 0-2 | Direct single-agent routing |
| MODERATE | 3-4 | 2-3 parallel tracks |
| COMPLEX | 5+ | Full multi-track orchestration |

### Key Principle: Component-Based Decomposition

Decomposition is based on **WHAT is needed**, not WHO builds it.

**Wrong:**
```
Track 1: @page-builder
Track 2: @css-architect
```

**Correct:**
```
Track 1: layout-structure → @react-engineer
Track 2: design-tokens → @css-architect
Track 3: api-integration → @api-architect
```

## Installation

```bash
/plugins install <github-username>/custom-agents
```

## Documentation

See `plugins/controllers/HOW-TO.md` for comprehensive usage guide.

## Directory Structure

```
plugins/
├── controllers/
│   ├── agents/
│   │   └── worker.md           # Re-anchoring worker agent
│   ├── commands/
│   │   └── custom-agents/      # Slash commands
│   │       ├── init.md
│   │       ├── plan.md
│   │       ├── work.md
│   │       ├── status.md
│   │       └── next.md
│   ├── hooks/
│   │   ├── hooks.json          # Hook configuration reference
│   │   ├── pre-edit-guard.sh
│   │   ├── pre-write-guard.sh
│   │   └── post-bash-guard.sh
│   ├── scripts/
│   │   ├── taskctl             # CLI entry point
│   │   ├── taskctl.py          # Task management CLI
│   │   └── state_schema.py     # State type definitions
│   ├── skills/
│   │   ├── complexity-detection.md
│   │   ├── multi-track-orchestration.md
│   │   ├── re-anchoring.md
│   │   ├── review-gating.md
│   │   ├── guard-hooks.md
│   │   ├── memory-management.md
│   │   ├── parallel-research.md
│   │   └── ...
│   ├── plugin.json
│   └── HOW-TO.md               # Comprehensive guide
├── frontend/
│   ├── agents/                 # Frontend specialists
│   └── skills/
├── backend/
│   ├── agents/                 # Backend specialists
│   └── skills/
├── creative/
│   ├── agents/                 # Creative specialists
│   └── skills/
├── discovery/
│   ├── agents/                 # Research/planning + scout specialists
│   └── skills/
├── devops/
│   ├── agents/                 # DevOps/QA specialists
│   └── skills/
└── utilities/
    ├── agents/                 # Cross-cutting specialists
    └── skills/
```

## Version

**controllers**: v2.2.0
