---
skill: multi-track-orchestration
version: "2.0.0"
description: "5-phase orchestration system for complex tasks: ASSESS → DECOMPOSE → EXECUTE → SYNTHESIZE → FOLLOW-UP"
used-by:
  - orchestrator
  - main-thread
requires:
  - complexity-detection
  - track-templates
  - follow-up-triggers
  - parallel-execution
  - dependency-management
  - synthesis-patterns
  - re-anchoring
---

# State Management Integration

## taskctl CLI

The orchestration system uses `taskctl` for persistent state management across sessions.

**Location:** `/Users/patrickbrosnan/.claude/plugins/marketplaces/custom-agents/plugins/controllers/scripts/taskctl`

**CRITICAL:** Always use this direct marketplace path. The `CLAUDE_PLUGIN_ROOT` variable often points to a cache directory that doesn't contain the scripts.

### Key Commands
```bash
# Initialize (first time only)
taskctl init

# Epic management (ASSESS/DECOMPOSE phases)
taskctl epic create "<title>"           # Returns epic ID (ca-N-xxx)
taskctl epic set-status <id> <status>   # planning|ready|in_progress|done

# Task management (EXECUTE phase)
taskctl task create <epic-id> "<title>" # Returns task ID (ca-N-xxx.M)
taskctl task set-depends <id> <deps...> # Set dependencies
taskctl task start <id>                 # Mark in_progress
taskctl task done <id> --summary "..."  # Mark completed

# Queries
taskctl next                            # Get next actionable unit
taskctl task ready --epic <id>          # List ready tasks (deps resolved)
taskctl cat <id>                        # Output spec for re-anchoring
```

### State Directory
```
.tasks/
├── meta.json           # Schema version
├── config.json         # User preferences
├── epics/<id>.json     # Epic metadata
├── specs/<id>.md       # Epic specification
├── tasks/<id>.json     # Task metadata
└── tasks/<id>.md       # Task specification
```

# Multi-Track Orchestration Skill

## Purpose

Orchestrate complex, multi-component tasks through a structured 5-phase system that decomposes work into parallel tracks and ensures autonomous completion with quality follow-up.

## 5-Phase Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│  PHASE 1: ASSESS                                                     │
│  Parse intent → Calculate complexity → Determine orchestration mode  │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │ SIMPLE?  → Direct   │
                    │          routing    │
                    └──────────┬──────────┘
                               │ MODERATE/COMPLEX
┌──────────────────────────────▼──────────────────────────────────────┐
│  PHASE 2: DECOMPOSE                                                  │
│  Identify components → Create tracks → Map dependencies              │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────────┐
│  PHASE 3: EXECUTE                                                    │
│  Spawn agents per track → Track via TodoWrite → Respect dependencies │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────────┐
│  PHASE 4: SYNTHESIZE                                                 │
│  Combine outputs → Detect emergent tasks → Create summary            │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────────┐
│  PHASE 5: FOLLOW-UP                                                  │
│  Auto-spawn quality agents → Continue until complete                 │
└─────────────────────────────────────────────────────────────────────┘
```

## Phase 1: ASSESS

### Purpose
Determine whether to use simple routing or full multi-track orchestration.

### Procedure

1. **Parse User Intent**
   - Extract action verbs, domains, constraints
   - Identify implicit needs (research before building)
   - Note any explicit agent requests

2. **Calculate Complexity Score**
   Use `complexity-detection.md` skill:
   ```
   Score 0-2  → SIMPLE (direct routing)
   Score 3-4  → MODERATE (2-3 tracks)
   Score 5+   → COMPLEX (full orchestration)
   ```

3. **Check Overrides**
   - Force SIMPLE: single verb+noun, explicit @agent, small scope
   - Force COMPLEX: /discover, /deploy, multi-page, end-to-end

4. **Output Decision**
   ```markdown
   ## Assessment Complete

   **Mode:** [SIMPLE/MODERATE/COMPLEX]
   **Reasoning:** [brief explanation]
   **Next Phase:** [DECOMPOSE or Direct Routing]
   ```

5. **Create Epic for Persistent State** (MODERATE/COMPLEX only)
   ```bash
   # Ensure .tasks/ exists
   taskctl init  # Safe to run multiple times

   # Create epic to track this orchestration
   EPIC_ID=$(taskctl epic create "[Brief task description]")
   # Example: EPIC_ID=ca-1-f7k

   # Store complexity score in epic
   # (done automatically via spec markdown)
   ```

### If SIMPLE Mode
Skip to direct routing using `task-routing.md`:
```
Main thread → Task(@specialist) → Synthesize
```
Note: SIMPLE mode does NOT create an epic (overhead not justified).

### If MODERATE/COMPLEX Mode
Continue to Phase 2: DECOMPOSE with created EPIC_ID

## Phase 2: DECOMPOSE

### Purpose
Break the request into component-based tracks with dependencies mapped.

### Procedure

0. **Parallel Research (for implementation tasks)**

   Before decomposing, gather context using the `parallel-research.md` skill:

   ```
   # Spawn scouts in parallel (SINGLE message)
   Task(@repo-scout, "Find patterns for: [topic]")
   Task(@context-scout, "Extract signatures for: [topic]")
   Task(@practice-scout, "Research best practices for: [topic]")
   Task(@docs-scout, "Find documentation for: [frameworks]")
   Task(@memory-scout, "Search memory for: [topic]")  # if memory.enabled
   ```

   **Scout Selection Guide:**
   | Scout | When to Include |
   |-------|-----------------|
   | repo-scout | Always (existing patterns) |
   | context-scout | When types/interfaces matter |
   | practice-scout | New features, security-sensitive |
   | docs-scout | External library integration |
   | memory-scout | If `.tasks/memory/` exists |

   **Wait for all scouts to complete, then synthesize:**
   - Patterns to follow
   - Pitfalls to avoid
   - Best practices to apply
   - Types to use

   This research informs the track decomposition below.

1. **Identify Request Domain**
   - Development (building)
   - Research (understanding)
   - Discovery (project kickoff)
   - Design (specification)
   - Strategy (planning)
   - Quality (auditing)
   - Learning (education)

2. **Apply Track Templates**
   Use `track-templates.md` to identify all required components:
   ```
   for each checklist_item in domain_checklist:
       if required:
           create_track(component_type, purpose, specialist)
   ```

3. **Map Dependencies**
   Use `dependency-management.md`:
   - Identify which tracks can parallelize
   - Identify blocking dependencies
   - Determine critical path

4. **Create Tasks in State System**
   ```bash
   # For each track identified, create a task
   TASK1=$(taskctl task create $EPIC_ID "Market analysis research")
   TASK2=$(taskctl task create $EPIC_ID "Design tokens - color, typography")
   TASK3=$(taskctl task create $EPIC_ID "Page layout structure")
   TASK4=$(taskctl task create $EPIC_ID "UI component implementation")
   TASK5=$(taskctl task create $EPIC_ID "API endpoints")

   # Set dependencies
   taskctl task set-depends $TASK3 $TASK2    # layout depends on tokens
   taskctl task set-depends $TASK4 $TASK2 $TASK3  # components depend on tokens + layout
   ```

5. **Create Execution Plan**
   ```markdown
   ## Track Decomposition

   **Request:** [original request]
   **Domain:** [identified domain]
   **Epic:** [EPIC_ID]
   **Tracks:** [count]

   ### Track List
   | # | Task ID | Component | Specialist | Depends On |
   |---|---------|-----------|------------|------------|
   | 1 | ca-1-f7k.1 | Market analysis | @web-researcher | - |
   | 2 | ca-1-f7k.2 | Design tokens | @css-architect | - |
   | 3 | ca-1-f7k.3 | Page structure | @react-engineer | .2 |
   | 4 | ca-1-f7k.4 | UI elements | @react-engineer | .2, .3 |
   | 5 | ca-1-f7k.5 | Backend endpoints | @api-architect | .1 |

   ### Execution Waves
   - Wave 1 (parallel): .1, .2
   - Wave 2 (after Wave 1): .3, .5
   - Wave 3 (after Wave 2): .4
   ```

6. **Update Epic Status**
   ```bash
   taskctl epic set-status $EPIC_ID ready
   ```

## Phase 3: EXECUTE

### Purpose
Spawn agents for each track, respecting dependencies and tracking progress.

### Procedure

1. **Initialize TodoWrite State**
   ```markdown
   ## Orchestration: [task-name]

   **Phase:** EXECUTE
   **Total Tracks:** [count]
   **Current Wave:** 1

   | Track | Status | Agent | Wave | Output |
   |-------|--------|-------|------|--------|
   | research | pending | @web-researcher | 1 | - |
   | design-tokens | pending | @css-architect | 1 | - |
   | layout | blocked | @react-engineer | 2 | - |
   ```

2. **Execute Wave by Wave**

   **IMPORTANT:** Use the `@worker` agent for all task execution. The worker provides:
   - Fresh context per task (no accumulated drift)
   - Mandatory re-anchoring before implementation
   - Consistent completion patterns

   ```
   for each wave in execution_plan:
       parallel_tracks = get_tracks_for_wave(wave)

       # Mark tasks as started and spawn worker agents
       for track in parallel_tracks:
           taskctl task start $TASK_ID

           # Spawn worker with specialist context
           Task(@worker, """
             ## Task Configuration
             TASK_ID: $TASK_ID
             EPIC_ID: $EPIC_ID
             TASKCTL: /Users/patrickbrosnan/.claude/plugins/marketplaces/custom-agents/plugins/controllers/scripts/taskctl
             SPECIALIST_CONTEXT: $track.specialist

             ## Specialist Role
             You are acting as @$track.specialist for this task.
             Apply the patterns, conventions, and expertise of that role.

             ## Instructions
             1. Complete Phase 1 (Re-anchor) - read spec, epic, git state
             2. Complete Phase 2 (Implement) - follow spec exactly
             3. Complete Phase 3 (Verify) - check criteria, commit
             4. Complete Phase 4 (Complete) - mark done, return summary

             Begin with re-anchoring: taskctl cat $TASK_ID
           """)
           update_todo(track, status="in_progress")

       # Wait for wave completion
       wait_for_all(parallel_tracks)

       # Worker marks task done internally; verify and update orchestrator state
       for track in parallel_tracks:
           # Verify task is done
           taskctl task show $TASK_ID  # Confirm status=done
           update_todo(track, status="completed", output=worker_summary)
   ```

   **Worker vs Direct Specialist:**
   | Approach | Context | Re-anchor | Completion |
   |----------|---------|-----------|------------|
   | `@worker` (recommended) | Fresh per task | Mandatory | Consistent |
   | `@specialist` (legacy) | Accumulated | Optional | Variable |

3. **Handle Track Failures**
   - If track fails → spawn @debugger
   - If critical failure → pause and assess
   - If recoverable → retry with adjusted approach

4. **Respect Concurrency Limits**
   Use `parallel-execution.md`:
   - Max 3-5 parallel agents
   - No file write conflicts
   - Domain separation where possible

## Phase 4: SYNTHESIZE

### Purpose
Combine all track outputs into cohesive deliverables and detect emergent tasks.

### Procedure

1. **Gather All Outputs**
   ```
   outputs = []
   for track in completed_tracks:
       outputs.append({
           track: track.name,
           agent: track.agent,
           deliverables: track.output,
           files_changed: track.files
       })
   ```

2. **Use Synthesis Patterns**
   Apply `synthesis-patterns.md`:
   ```markdown
   ## Task Complete

   ### Summary
   [2-3 sentence overview of what was accomplished]

   ### Results by Track
   | Track | Deliverables | Files |
   |-------|--------------|-------|
   | research | Market analysis report | docs/analysis.md |
   | design-tokens | Token system | tokens.css |
   | layout | Page structure | pages/index.tsx |

   ### Key Decisions Made
   - [Decision 1 and rationale]
   - [Decision 2 and rationale]

   ### Files Changed
   - [full list of files created/modified]
   ```

3. **Detect Emergent Tasks**
   Look for:
   - TODOs in agent outputs
   - Unresolved dependencies
   - Integration gaps
   - Quality concerns mentioned

4. **Queue Emergent Tasks**
   If emergent tasks found:
   ```
   for task in emergent_tasks:
       add_to_follow_up_queue(task)
   ```

## Phase 5: FOLLOW-UP

### Purpose
Automatically spawn quality and validation agents to ensure complete, production-ready output.

### Procedure

1. **Apply Follow-Up Triggers**
   Use `follow-up-triggers.md`:
   ```
   for track in completed_tracks:
       triggers = match_triggers(track)
       for trigger in triggers:
           if trigger.condition_met:
               queue_follow_up(trigger.agent, trigger.priority)
   ```

2. **Execute Follow-Up Queue**
   ```
   # Process by priority
   CRITICAL → Execute immediately
   HIGH     → Execute in next wave
   MEDIUM   → Queue for capacity
   LOW      → Batch at end
   ```

3. **Handle Follow-Up Results**
   - Issues found → spawn @debugger
   - Clean pass → mark verified
   - New emergent tasks → queue for follow-up

4. **Loop Until Complete**
   ```
   while follow_up_queue not empty OR emergent_tasks exist:
       execute_follow_ups()
       handle_results()
       check_for_new_emergent_tasks()
   ```

5. **Final Verification**
   - All tracks completed
   - All follow-ups passed
   - No critical issues remaining
   - Final synthesis delivered

6. **Mark Epic Complete**
   ```bash
   # Verify all tasks done
   taskctl task list --epic $EPIC_ID --status done

   # Mark epic as done
   taskctl epic set-status $EPIC_ID done

   # Final status
   taskctl status
   ```

## State Tracking via TodoWrite

### Orchestration State Template

```markdown
## Orchestration: [task-name]

**Phase:** [ASSESS/DECOMPOSE/EXECUTE/SYNTHESIZE/FOLLOW-UP]
**Mode:** [SIMPLE/MODERATE/COMPLEX]
**Progress:** [X/Y tracks complete]

### Tracks
| # | Track | Status | Agent | Output |
|---|-------|--------|-------|--------|
| 1 | [name] | [status] | @agent | [summary] |

### Follow-Up Queue
| Priority | Agent | Trigger | Status |
|----------|-------|---------|--------|
| HIGH | @accessibility-engineer | Component built | pending |

### Emergent Tasks
- [ ] [Task description]

### Blockers
- [Any blocking issues]
```

### Status Values

- `pending` - Not yet started
- `blocked` - Waiting on dependency
- `in_progress` - Currently executing
- `completed` - Finished successfully
- `failed` - Error occurred
- `verified` - Passed follow-up checks

## Key Principles

1. **No Artificial Concurrency Limits**
   Spawn as many agents as the task requires (within practical limits of 3-5).

2. **Blocking Dependencies Must Complete**
   Never start a track that depends on incomplete tracks.

3. **Main Thread Never Implements**
   Orchestrator routes, specialists implement.

4. **Follow-Up is Fully Autonomous**
   No user checkpoints during follow-up phase.

5. **TodoWrite Tracks All State**
   Every phase transition and track status update is recorded.

6. **Component-Based Decomposition**
   Decompose by WHAT is needed, not WHO builds it.

## Quality Checklist

- [ ] Phase 1: Complexity assessed, mode determined
- [ ] Phase 2: All components identified, dependencies mapped
- [ ] Phase 3: Tracks executed respecting waves
- [ ] Phase 4: Outputs synthesized, emergent tasks detected
- [ ] Phase 5: Follow-ups completed, verification passed
- [ ] State tracked throughout via TodoWrite
- [ ] No manual intervention required (autonomous completion)
