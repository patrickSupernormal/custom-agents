# Custom-Agents Plugin Upgrade Plan

## Executive Summary

This plan upgrades the custom-agents orchestration system by adopting key architectural patterns from flow-next while preserving your existing strengths (88 specialists, sophisticated complexity scoring, full SDLC coverage).

**Goal:** Achieve flow-next's context optimization and automation reliability without losing custom-agents' rich domain coverage.

---

## Key Features to Adopt

| Priority | Feature | Benefit |
|----------|---------|---------|
| **P0** | State Management CLI (`taskctl`) | Persistent task state across sessions |
| **P0** | Re-anchoring Pattern | Prevents drift in long-running tasks |
| **P1** | Context Isolation (worker subagent) | Fresh context per task, no accumulation |
| **P1** | Parallel Scout Pattern | 5x faster research phase |
| **P2** | Memory System | Learn from mistakes, persist patterns |
| **P2** | Token-Efficient Exploration | Signatures-only for large codebases |
| **P3** | Review Gating | Multi-model quality gates |
| **P3** | Guard Hooks | Enforce workflow rules |

---

## Phase 1: State Management Foundation (P0)

### 1.1 Create `taskctl` CLI

Create a lightweight Python CLI similar to flowctl but integrated with your complexity scoring.

**New Files:**
```
plugins/controllers/
├── scripts/
│   ├── taskctl              # Executable wrapper
│   ├── taskctl.py           # Main CLI (~600 lines)
│   └── state_schema.py      # JSON schema definitions
```

**`taskctl` Commands:**
```bash
# Epic management
taskctl epic create "Add OAuth login"      # Creates epic with ID
taskctl epic list                          # List all epics
taskctl epic show <id>                     # Show epic details
taskctl epic status <id> <status>          # Update status

# Task management
taskctl task create <epic-id> "Implement auth hook"  # Creates task
taskctl task list --epic <id>              # List tasks in epic
taskctl task show <id>                     # Show task with spec
taskctl task start <id>                    # Mark in-progress
taskctl task done <id>                     # Mark complete
taskctl task ready --epic <id>             # List ready tasks (deps resolved)

# State queries
taskctl next                               # Get next plannable/workable unit
taskctl cat <id>                           # Output full spec markdown

# Configuration
taskctl config get <key>                   # Get config value
taskctl config set <key> <value>           # Set config value
```

**State Directory Structure:**
```
.tasks/                                    # Project root
├── meta.json                              # Schema version, setup info
├── config.json                            # User preferences
├── epics/
│   └── <epic-id>.json                     # Epic metadata
├── specs/
│   └── <epic-id>.md                       # Epic specification
├── tasks/
│   ├── <epic-id>.<task-num>.json          # Task metadata
│   └── <epic-id>.<task-num>.md            # Task specification
└── memory/                                # Phase 2
    ├── pitfalls.md
    ├── conventions.md
    └── decisions.md
```

**ID Format:**
- Epic: `ca-N-xxx` (ca = custom-agents, N = sequence, xxx = collision suffix)
- Task: `ca-N-xxx.M` (M = task number within epic)

### 1.2 Update Orchestration Protocol

Modify `controllers/skills/multi-track-orchestration.md` to integrate taskctl:

**ASSESS Phase Addition:**
```markdown
## ASSESS Phase - Enhanced

After complexity scoring:
1. Check if `.tasks/` directory exists
2. If COMPLEX mode: Create epic via `taskctl epic create`
3. Store epic ID for DECOMPOSE phase
4. Log decision in epic spec
```

**DECOMPOSE Phase Addition:**
```markdown
## DECOMPOSE Phase - Enhanced

After identifying tracks:
1. Create task for each track via `taskctl task create`
2. Set dependencies in task metadata
3. Write task specifications to `.tasks/tasks/<id>.md`
4. Update TodoWrite with task IDs for user visibility
```

**EXECUTE Phase Addition:**
```markdown
## EXECUTE Phase - Enhanced

Before spawning each agent:
1. `taskctl task start <id>`
2. Include task ID and spec path in agent prompt

After agent completes:
1. `taskctl task done <id>`
2. Verify status via `taskctl task show <id>`
```

### 1.3 Deliverables

- [ ] `scripts/taskctl` (executable wrapper)
- [ ] `scripts/taskctl.py` (~600 lines)
- [ ] `scripts/state_schema.py` (JSON schemas)
- [ ] Updated `multi-track-orchestration.md`
- [ ] Updated `complexity-detection.md` (epic creation trigger)

---

## Phase 2: Re-anchoring & Context Isolation (P0-P1)

### 2.1 Create Worker Agent

Add a new agent that handles task execution with fresh context:

**New File:** `plugins/controllers/agents/worker.md`

```markdown
---
name: worker
version: "1.0.0"
description: "Task implementation agent with fresh context per task"
tools: [Read, Write, Edit, Glob, Grep, Bash]
disallowedTools: [Task]  # Cannot spawn subagents
model: inherit
color: "#3B82F6"
---

# Worker

You are a task implementation specialist. You receive a single task specification and implement it with laser focus.

## Phase 1: Re-anchor (MANDATORY)

Before any implementation:

1. **Read Task Spec**
   ```bash
   $TASKCTL cat $TASK_ID
   ```

2. **Read Epic Context**
   ```bash
   $TASKCTL epic show $EPIC_ID
   $TASKCTL cat $EPIC_ID
   ```

3. **Check Git State**
   ```bash
   git status
   git log -5 --oneline
   ```

4. **Parse Acceptance Criteria**
   Extract AC from task spec, verify completability.

## Phase 2: Implement

Execute the task per specification:
- Follow existing patterns from re-anchor phase
- Implement ONLY what spec requires
- No scope creep or "improvements"

## Phase 3: Verify

Before declaring done:
- Run relevant tests if they exist
- Verify acceptance criteria met
- Commit with clear message

## Phase 4: Complete

```bash
$TASKCTL task done $TASK_ID
```

Return summary of:
- Files created/modified
- Tests run
- Any blockers for downstream tasks
```

### 2.2 Update Agent Spawning Pattern

Modify how main thread spawns specialists:

**Current Pattern:**
```
Task(@react-engineer, "Build the login form...")
```

**New Pattern:**
```
Task(@worker, """
TASK_ID: ca-1-abc.2
EPIC_ID: ca-1-abc
TASKCTL: $CLAUDE_PLUGIN_ROOT/plugins/controllers/scripts/taskctl
SPECIALIST_CONTEXT: react-engineer

You are acting as @react-engineer for this task.
[Include react-engineer.md content or reference]

Re-anchor and implement task ca-1-abc.2.
""")
```

### 2.3 Re-anchor Skill

**New File:** `plugins/controllers/skills/re-anchoring.md`

```markdown
---
skill: re-anchoring
version: "1.0.0"
description: "Pattern for context re-synchronization before task execution"
used-by:
  - worker
  - all-specialists
---

# Re-anchoring Pattern

## Purpose

Prevent context drift by re-reading source-of-truth before every task.

## Mandatory Steps

### Step 1: Read Task Specification
- Execute: `taskctl cat <task-id>`
- Parse: acceptance criteria, constraints, dependencies

### Step 2: Read Epic Context
- Execute: `taskctl cat <epic-id>`
- Parse: overall goal, decisions made, related tasks

### Step 3: Check Repository State
- Execute: `git status` (modified files)
- Execute: `git log -5 --oneline` (recent commits)
- Verify: current branch matches expected

### Step 4: Validate Starting Point
- Compare: spec requirements vs current state
- Identify: what's already done vs what remains
- Flag: any conflicts or ambiguities

## When to Re-anchor

- Start of every task
- After any interruption (compaction, user pause)
- When context feels stale or uncertain
- Before claiming task completion

## Anti-Patterns

- Starting implementation without reading spec
- Assuming previous context is still valid
- Skipping git status check
- Proceeding with stale understanding
```

### 2.4 Deliverables

- [ ] `plugins/controllers/agents/worker.md`
- [ ] `plugins/controllers/skills/re-anchoring.md`
- [ ] Updated agent spawn pattern in `multi-track-orchestration.md`
- [ ] Updated `task-routing.md` (SIMPLE mode uses worker too)

---

## Phase 3: Parallel Scout Pattern (P1)

### 3.1 Create Scout Agents

Transform research-oriented agents into parallel scouts:

**New/Updated Files:**
```
plugins/discovery/agents/
├── repo-scout.md       # Fast pattern discovery (grep/glob)
├── context-scout.md    # Deep discovery (structure-aware)
├── practice-scout.md   # Best practices research
├── docs-scout.md       # Framework documentation
├── memory-scout.md     # Persistent learning retrieval
```

**Scout Agent Template:**
```markdown
---
name: repo-scout
version: "1.0.0"
description: "Fast pattern discovery via grep/glob"
tools: [Read, Grep, Glob, Bash]
disallowedTools: [Task, Write, Edit]  # Read-only exploration
model: opus
color: "#22C55E"
---

# Repo Scout

Fast pattern discovery specialist. Find relevant code patterns without reading full files.

## Mission

Given a topic/feature, discover:
1. Existing implementations of similar patterns
2. File locations and naming conventions
3. Import patterns and dependencies
4. Test patterns for the domain

## Approach

1. **Grep First**: Use Grep to find keyword matches
2. **Glob for Structure**: Use Glob to understand file organization
3. **Targeted Reads**: Only read specific sections, not full files
4. **Summarize Patterns**: Return distilled findings, not raw content

## Output Format

```markdown
## Findings: [Topic]

### Existing Patterns
- Pattern 1: `path/to/file.ts:45` - description
- Pattern 2: `path/to/other.ts:120` - description

### File Structure
- Components: `src/components/[feature]/`
- Hooks: `src/hooks/use[Feature].ts`
- Tests: `__tests__/[feature].test.ts`

### Dependencies
- Internal: `@/lib/utils`, `@/hooks/useAuth`
- External: `react-query`, `zod`

### Recommendations
- Follow pattern from [existing file]
- Use existing [utility/hook]
```
```

### 3.2 Parallel Research Skill

**New File:** `plugins/controllers/skills/parallel-research.md`

```markdown
---
skill: parallel-research
version: "1.0.0"
description: "Orchestrate parallel scout execution for research phase"
used-by:
  - orchestrator
  - planning-phase
---

# Parallel Research Pattern

## Purpose

Gather comprehensive context before planning by running multiple scouts concurrently.

## Scout Roster

| Scout | Purpose | When to Use |
|-------|---------|-------------|
| repo-scout | Existing patterns in codebase | Always |
| practice-scout | Industry best practices | New features |
| docs-scout | Framework/library docs | External integrations |
| github-scout | Cross-repo examples | Novel implementations |
| memory-scout | Previous learnings | If memory enabled |

## Execution

### Step 1: Spawn All Relevant Scouts (Single Message)

```
# In single Task tool message, spawn parallel:
Task(@repo-scout, "Find patterns for: [topic]")
Task(@practice-scout, "Research best practices for: [topic]")
Task(@docs-scout, "Gather docs for: [frameworks used]")
Task(@github-scout, "Find examples of: [topic]")
Task(@memory-scout, "Retrieve learnings about: [topic]")  # if enabled
```

### Step 2: Collect Results

All scouts return within ~30 seconds. Collect findings.

### Step 3: Synthesize

Combine scout outputs into unified research summary:
- Patterns to follow
- Patterns to avoid
- Dependencies to use
- Gaps in existing codebase

## Output to Planning Phase

```markdown
## Research Summary: [Topic]

### From Codebase (repo-scout)
[Distilled findings]

### From Best Practices (practice-scout)
[Distilled findings]

### From Documentation (docs-scout)
[Distilled findings]

### From Examples (github-scout)
[Distilled findings]

### From Memory (memory-scout)
[Distilled findings]

### Synthesis
[Combined recommendations]
```
```

### 3.3 Deliverables

- [ ] `plugins/discovery/agents/repo-scout.md`
- [ ] `plugins/discovery/agents/context-scout.md`
- [ ] `plugins/discovery/agents/practice-scout.md`
- [ ] `plugins/discovery/agents/docs-scout.md`
- [ ] `plugins/discovery/agents/memory-scout.md`
- [ ] `plugins/controllers/skills/parallel-research.md`
- [ ] Update DECOMPOSE phase to include research step

---

## Phase 4: Memory System (P2)

### 4.1 Memory Structure

Extend `.tasks/` with memory directory:

```
.tasks/memory/
├── pitfalls.md        # Lessons from failures
├── conventions.md     # Project-specific patterns
└── decisions.md       # Architectural choices
```

### 4.2 Memory Management Commands

Add to `taskctl.py`:

```bash
# Initialize memory
taskctl memory init

# Add entries
taskctl memory add --type pitfall "Don't use useState for form state, use react-hook-form"
taskctl memory add --type convention "All API routes use /api/v1/ prefix"
taskctl memory add --type decision "Chose Zustand over Redux for simplicity"

# Query memory
taskctl memory list --type pitfall
taskctl memory search "form state"

# Auto-capture from reviews
taskctl memory capture --from review-output.md
```

### 4.3 Memory Scout Agent

**New File:** `plugins/discovery/agents/memory-scout.md`

```markdown
---
name: memory-scout
version: "1.0.0"
description: "Retrieve relevant persistent learnings"
tools: [Read, Grep, Glob]
disallowedTools: [Task, Write, Edit, Bash]
model: opus
color: "#A855F7"
---

# Memory Scout

Retrieve relevant learnings from project memory.

## Mission

Given a topic, find:
1. Related pitfalls to avoid
2. Established conventions to follow
3. Relevant architectural decisions

## Process

1. Read `.tasks/memory/pitfalls.md`
2. Read `.tasks/memory/conventions.md`
3. Read `.tasks/memory/decisions.md`
4. Filter for relevance to current topic
5. Return applicable learnings

## Output Format

```markdown
## Relevant Memory: [Topic]

### Pitfalls to Avoid
- [Pitfall 1]: [Context and why]
- [Pitfall 2]: [Context and why]

### Conventions to Follow
- [Convention 1]
- [Convention 2]

### Relevant Decisions
- [Decision 1]: [Rationale]
```
```

### 4.4 Auto-Capture from Follow-ups

Update `follow-up-triggers.md` to capture learnings:

```markdown
## Memory Capture Triggers

When @debugger fixes an issue:
- If fix was non-obvious: `taskctl memory add --type pitfall "[description]"`

When @qa-auditor finds issues:
- Pattern-based issues: `taskctl memory add --type convention "[pattern]"`

When architectural change made:
- `taskctl memory add --type decision "[decision and rationale]"`
```

### 4.5 Deliverables

- [ ] Memory commands in `taskctl.py`
- [ ] `plugins/discovery/agents/memory-scout.md`
- [ ] Memory capture rules in `follow-up-triggers.md`
- [ ] Memory integration in worker re-anchor phase

---

## Phase 5: Token-Efficient Exploration (P2)

### 5.1 Structure-Aware Exploration Skill

**New File:** `plugins/controllers/skills/token-efficient-exploration.md`

```markdown
---
skill: token-efficient-exploration
version: "1.0.0"
description: "Patterns for exploring large codebases without exhausting context"
---

# Token-Efficient Exploration

## Principle

Explore breadth first (Grep/Glob), depth second (targeted Read).

## Strategies

### Strategy 1: Grep for Patterns
```bash
# Find all exports of a type
Grep("export (interface|type|class) Auth", glob: "**/*.ts")

# Find all usages
Grep("useAuth|AuthContext|authService", glob: "**/*.{ts,tsx}")
```

### Strategy 2: Glob for Structure
```bash
# Understand file organization
Glob("src/**/*.ts")
Glob("src/components/**/*.tsx")
```

### Strategy 3: Targeted Reads
Instead of reading entire files, read specific line ranges:
```
Read(file_path, offset: 45, limit: 30)  # Just the relevant function
```

### Strategy 4: Signature Extraction
When exploring unfamiliar code, extract signatures only:
```javascript
// Instead of full file, extract:
export function useAuth(): AuthState
export const AuthProvider: FC<AuthProviderProps>
interface AuthState { user: User | null; login: () => void }
```

## Anti-Patterns

- Reading entire files when only function signature needed
- Using Read for exploration (use Grep first)
- Accumulating full file contents in context
- Not using offset/limit for large files
```

### 5.2 Update Scout Agents

Add token-efficiency rules to all scout agents:

```markdown
## Token Budget Rules

1. **Never read full files for exploration**
   - Use Grep to find relevant sections
   - Use Read with offset/limit for specific sections

2. **Summarize, don't quote**
   - Return patterns found, not raw code
   - Include file:line references for specifics

3. **Stop early if pattern clear**
   - Don't exhaustively search after finding 3-5 examples
   - Mention "additional instances exist" if truncating
```

### 5.3 Deliverables

- [ ] `plugins/controllers/skills/token-efficient-exploration.md`
- [ ] Token budget rules added to all scout agents
- [ ] Exploration patterns in `repo-scout.md`

---

## Phase 6: Review Gating (P3)

### 6.1 Quality Auditor Enhancement

Update `plugins/devops/agents/qa-auditor.md` with review gating:

```markdown
## Review Verdict System

After reviewing, output one of:

### SHIP
Implementation meets all criteria. Proceed to next task.

### NEEDS_WORK
Minor issues found. List specific fixes required.
Worker will fix and re-submit for review.

### MAJOR_RETHINK
Fundamental problems. Escalate to user.
Do not proceed without human decision.
```

### 6.2 Review Loop in Worker

Update worker agent to handle review outcomes:

```markdown
## Phase 3: Review Loop

If REVIEW_MODE enabled:

1. Commit implementation
2. Invoke review (via main thread)
3. Parse verdict:
   - SHIP → proceed to completion
   - NEEDS_WORK → apply fixes, re-commit, re-review
   - MAJOR_RETHINK → return to main thread with escalation

Maximum review iterations: 3
After 3 NEEDS_WORK: escalate as MAJOR_RETHINK
```

### 6.3 Receipt System

Add review receipts for audit trail:

```
.tasks/reviews/
└── <task-id>-<timestamp>.json
```

```json
{
  "type": "impl_review",
  "task_id": "ca-1-abc.2",
  "verdict": "SHIP",
  "reviewer": "qa-auditor",
  "timestamp": "2026-01-21T10:30:00Z",
  "notes": "All acceptance criteria met"
}
```

### 6.4 Deliverables

- [ ] Verdict system in `qa-auditor.md`
- [ ] Review loop in `worker.md`
- [ ] Receipt logging in `taskctl.py`
- [ ] Review config in `.tasks/config.json`

---

## Phase 7: Guard Hooks (P3)

### 7.1 Hook Configuration

**New File:** `plugins/controllers/hooks/hooks.json`

```json
{
  "description": "Workflow enforcement hooks",
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "$PLUGIN_ROOT/scripts/hooks/pre-edit-guard.sh"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "$PLUGIN_ROOT/scripts/hooks/post-bash-guard.sh"
          }
        ]
      }
    ]
  }
}
```

### 7.2 Guard Scripts

**pre-edit-guard.sh:**
```bash
#!/bin/bash
# Ensure worker has re-anchored before editing

if [ -z "$TASK_ID" ]; then
  echo "ERROR: No TASK_ID set. Worker must re-anchor before editing."
  exit 1
fi

# Check if task is in-progress
STATUS=$(taskctl task show $TASK_ID --json | jq -r '.status')
if [ "$STATUS" != "in_progress" ]; then
  echo "ERROR: Task $TASK_ID is not in-progress. Run: taskctl task start $TASK_ID"
  exit 1
fi

exit 0
```

### 7.3 Deliverables

- [ ] `plugins/controllers/hooks/hooks.json`
- [ ] `plugins/controllers/scripts/hooks/pre-edit-guard.sh`
- [ ] `plugins/controllers/scripts/hooks/post-bash-guard.sh`

---

## Implementation Timeline

| Phase | Priority | Effort | Dependencies |
|-------|----------|--------|--------------|
| **Phase 1: State Management** | P0 | 2-3 days | None |
| **Phase 2: Re-anchoring** | P0-P1 | 1-2 days | Phase 1 |
| **Phase 3: Parallel Scouts** | P1 | 1-2 days | None |
| **Phase 4: Memory System** | P2 | 1-2 days | Phase 1 |
| **Phase 5: Token Efficiency** | P2 | 1 day | Phase 3 |
| **Phase 6: Review Gating** | P3 | 1-2 days | Phase 1, 2 |
| **Phase 7: Guard Hooks** | P3 | 1 day | Phase 1 |

**Total Estimated Effort: 8-14 days**

---

## Migration Strategy

### Step 1: Parallel Installation
Install new features alongside existing system. Don't break current workflow.

### Step 2: Opt-In Activation
Add config flag to enable new features:
```json
{
  "stateManagement": { "enabled": false },
  "reAnchoring": { "enabled": false },
  "parallelScouts": { "enabled": false },
  "memory": { "enabled": false },
  "reviewGating": { "enabled": false }
}
```

### Step 3: Gradual Rollout
Enable one feature at a time:
1. State Management first (foundation)
2. Re-anchoring second (quality improvement)
3. Parallel Scouts third (speed improvement)
4. Others as needed

### Step 4: Remove Opt-Out
Once stable, make new patterns default.

---

## What to Preserve

Your custom-agents system has advantages over flow-next:

1. **88 Specialized Agents** - Keep all of them
2. **Complexity Scoring** - Superior to flow-next's simple epic model
3. **Domain Coverage** - Full SDLC coverage (frontend, backend, devops, creative, etc.)
4. **Follow-Up Triggers** - More comprehensive than flow-next's review-only gates
5. **Synthesis Patterns** - Well-defined output combination rules

The upgrade enhances these strengths with flow-next's reliability patterns.

---

## Success Metrics

After upgrade, measure:

1. **Context Drift** - Tasks complete per spec vs requiring clarification
2. **Session Continuity** - Can resume tasks after compaction
3. **Research Speed** - Time to complete DECOMPOSE phase
4. **Error Recovery** - Tasks fixed on first @debugger pass
5. **Memory Utilization** - Pitfalls avoided on subsequent tasks

---

## Next Steps

1. Review this plan
2. Decide on Phase 1 implementation approach
3. Create branch for upgrade work
4. Implement Phase 1 (taskctl CLI)
5. Test with real project before proceeding to Phase 2
