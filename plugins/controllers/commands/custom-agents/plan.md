---
name: custom-agents:plan
description: Create an epic with decomposed tasks from a feature request
argument-hint: "<feature description>"
---

# Plan a Feature Epic

Create a structured epic with decomposed tasks from a user's feature request.

## Prerequisites

- `.tasks/` must exist (run `/custom-agents:init` first)

## Process

### Step 1: Score Complexity

Evaluate the request using the complexity scoring matrix:

| Signal | Points |
|--------|--------|
| Multiple domains (frontend + backend) | +2 |
| Multiple deliverables | +2 |
| Scope keywords (full, complete, entire) | +2 |
| Sequential workflow | +1 |
| Research + implement | +2 |
| Quality gates mentioned | +1 |
| Multi-page/multi-feature | +2 |
| End-to-end flow | +2 |

### Step 2: Create Epic

```bash
TASKCTL="${CLAUDE_PLUGIN_ROOT}/plugins/controllers/scripts/taskctl"
EPIC_ID=$($TASKCTL epic create "<title from request>")
```

### Step 3: Write Epic Specification

Write to `.tasks/specs/<epic-id>.md`:

```markdown
# <Epic Title>

## Overview
<1-2 sentence summary>

## Goals
- <Goal 1>
- <Goal 2>

## Requirements
<Extracted from user request>

## Constraints
<Any limitations or requirements>

## Acceptance Criteria
- [ ] <Criterion 1>
- [ ] <Criterion 2>
```

### Step 4: Decompose into Tasks

Based on complexity score:
- **Score 3-4**: 2-3 tasks
- **Score 5+**: 5+ tasks (component-based decomposition)

For each task:
```bash
TASK_ID=$($TASKCTL task create $EPIC_ID "<task title>")
```

Write task spec to `.tasks/tasks/<task-id>.md`:

```markdown
# <Task Title>

## Objective
<What this task accomplishes>

## Acceptance Criteria
- [ ] <Specific criterion>
- [ ] <Specific criterion>

## Implementation Notes
<Any guidance for the implementer>
```

### Step 5: Set Dependencies

```bash
$TASKCTL task set-depends <task-id> <dependency-task-id>
```

### Step 6: Report to User

Output summary:
- Epic ID and title
- List of tasks with IDs
- Dependency graph
- Suggest running `/custom-agents:work <epic-id>` to start

## User Request

$ARGUMENTS
