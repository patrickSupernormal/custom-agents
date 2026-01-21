---
skill: multi-track-orchestration
version: "1.0.0"
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
---

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

### If SIMPLE Mode
Skip to direct routing using `task-routing.md`:
```
Main thread → Task(@specialist) → Synthesize
```

### If MODERATE/COMPLEX Mode
Continue to Phase 2: DECOMPOSE

## Phase 2: DECOMPOSE

### Purpose
Break the request into component-based tracks with dependencies mapped.

### Procedure

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

4. **Create Execution Plan**
   ```markdown
   ## Track Decomposition

   **Request:** [original request]
   **Domain:** [identified domain]
   **Tracks:** [count]

   ### Track List
   | # | Track | Component | Specialist | Depends On |
   |---|-------|-----------|------------|------------|
   | 1 | research | Market analysis | @web-researcher | - |
   | 2 | design-tokens | Color, typography | @css-architect | - |
   | 3 | layout | Page structure | @react-engineer | Track 2 |
   | 4 | components | UI elements | @react-engineer | Track 2, 3 |
   | 5 | api | Backend endpoints | @api-architect | Track 1 |

   ### Execution Waves
   - Wave 1 (parallel): Track 1, Track 2
   - Wave 2 (after Wave 1): Track 3, Track 5
   - Wave 3 (after Wave 2): Track 4
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
   ```
   for each wave in execution_plan:
       parallel_tracks = get_tracks_for_wave(wave)

       # Spawn all tracks in wave simultaneously
       for track in parallel_tracks:
           Task(@track.specialist, track.prompt)
           update_todo(track, status="in_progress")

       # Wait for wave completion
       wait_for_all(parallel_tracks)

       # Update state
       for track in parallel_tracks:
           update_todo(track, status="completed", output=result)
   ```

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
