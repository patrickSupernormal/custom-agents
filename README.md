# Custom Agents

Custom orchestration agents and skills for Claude Code development workflow.

## Architecture

Claude Code uses a **2-tier architecture**:
- **Main Thread (Orchestrator)**: Routes tasks to specialists, never implements directly
- **Specialist Agents**: Perform actual implementation work

There are no intermediate "controller" agents - subagents cannot spawn other subagents.

## Plugins

| Plugin | Agents | Description |
|--------|--------|-------------|
| **controllers** | 0 | Orchestration skills (no agents - main thread uses skills directly) |
| **frontend** | 15+ | Frontend/UI development specialists |
| **backend** | 15+ | Backend/API development specialists |
| **creative** | 12+ | Design, content, and creative specialists |
| **discovery** | 12+ | Research, planning, and analysis specialists |
| **devops** | 10+ | DevOps, testing, and quality specialists |
| **utilities** | 15+ | Cross-cutting utility specialists |

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

### Orchestration Skills

| Skill | Purpose |
|-------|---------|
| `complexity-detection` | Score requests to determine SIMPLE vs COMPLEX mode |
| `track-templates` | Component-based decomposition templates by domain |
| `multi-track-orchestration` | Full 5-phase orchestration for complex tasks |
| `follow-up-triggers` | Rules for autonomous quality agent spawning |
| `task-routing` | Direct routing for simple, single-agent tasks |
| `parallel-execution` | Determine when/how to parallelize agents |
| `dependency-management` | Track blocking vs non-blocking dependencies |
| `synthesis-patterns` | Combine multi-agent outputs into summaries |
| `error-escalation` | Handle failures and escalation paths |

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
Track 3: @animation-engineer
```

**Correct:**
```
Track 1: layout-structure → @react-engineer
Track 2: design-tokens → @css-architect
Track 3: animations → @animation-engineer
Track 4: api-integration → @api-architect
```

## Installation

```bash
/plugins install <github-username>/custom-agents
```

## Usage

The orchestrator automatically:
1. Assesses request complexity
2. Routes simple tasks directly to specialists
3. Decomposes complex tasks into parallel tracks
4. Spawns follow-up agents for quality assurance
5. Synthesizes results into actionable summaries

No manual intervention required - the system is fully autonomous.

## Directory Structure

```
plugins/
├── controllers/
│   ├── agents/          # (empty - main thread orchestrates directly)
│   └── skills/          # Orchestration skills
│       ├── complexity-detection.md
│       ├── track-templates.md
│       ├── multi-track-orchestration.md
│       ├── follow-up-triggers.md
│       ├── task-routing.md
│       ├── parallel-execution.md
│       ├── dependency-management.md
│       ├── synthesis-patterns.md
│       └── error-escalation.md
├── frontend/
│   ├── agents/          # Frontend specialists
│   └── skills/          # Frontend-specific skills
├── backend/
│   ├── agents/          # Backend specialists
│   └── skills/          # Backend-specific skills
├── creative/
│   ├── agents/          # Creative specialists
│   └── plugin.json
├── discovery/
│   ├── agents/          # Research/planning specialists
│   └── plugin.json
├── devops/
│   ├── agents/          # DevOps/QA specialists
│   └── plugin.json
└── utilities/
    └── agents/          # Cross-cutting specialists
```
