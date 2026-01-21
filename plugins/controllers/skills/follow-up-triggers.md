---
skill: follow-up-triggers
version: "1.0.0"
description: "Rules for autonomous follow-up agent spawning after track completion"
used-by:
  - orchestrator
  - main-thread
---

# Follow-Up Triggers Skill

## Purpose

Define rules for automatically spawning quality and validation agents after primary tracks complete. Follow-up is fully autonomous with no user checkpoints required.

## Automatic Trigger Rules

### Code Creation Triggers

| Completed Action | Auto-Trigger | Condition | Priority |
|------------------|--------------|-----------|----------|
| Code file created | @test-engineer | No tests exist for file | HIGH |
| React component built | @accessibility-engineer | Always | HIGH |
| Page/route created | @accessibility-engineer | Always | HIGH |
| Form implemented | @test-engineer | Form validation exists | MEDIUM |
| CSS/styles added | @accessibility-engineer | Color contrast check | MEDIUM |

### API & Backend Triggers

| Completed Action | Auto-Trigger | Condition | Priority |
|------------------|--------------|-----------|----------|
| API endpoint created | @security-engineer | Always | HIGH |
| Auth-related code | @security-engineer | Always | CRITICAL |
| Database schema changed | @test-engineer | Migration created | HIGH |
| Public API created | @documentation-writer | Always | MEDIUM |
| Data handling logic | @security-engineer | PII or sensitive data | HIGH |

### Animation & Performance Triggers

| Completed Action | Auto-Trigger | Condition | Priority |
|------------------|--------------|-----------|----------|
| Animation added | @performance-engineer | Always | MEDIUM |
| Image handling | @performance-engineer | Multiple images or large files | MEDIUM |
| Data fetching added | @performance-engineer | API calls in render path | MEDIUM |
| Bundle changes | @performance-engineer | New dependencies added | LOW |

### Error & Quality Triggers

| Completed Action | Auto-Trigger | Condition | Priority |
|------------------|--------------|-----------|----------|
| Errors in agent output | @debugger | Always | CRITICAL |
| Build warnings | @debugger | Warnings affect functionality | HIGH |
| Type errors | @debugger | TypeScript errors present | HIGH |
| All tracks complete | @qa-auditor | Final synthesis pass | HIGH |

### Content & Documentation Triggers

| Completed Action | Auto-Trigger | Condition | Priority |
|------------------|--------------|-----------|----------|
| New feature built | @documentation-writer | Public-facing feature | LOW |
| Breaking changes | @documentation-writer | API changes | MEDIUM |
| Config changes | @documentation-writer | Environment or setup changes | LOW |

## Trigger Priority Execution

```
CRITICAL → Execute immediately, block other follow-ups
HIGH     → Execute in next follow-up wave
MEDIUM   → Queue for follow-up, execute if capacity
LOW      → Queue for end-of-task follow-up batch
```

## Step-by-Step Procedure

### Step 1: Monitor Track Completion

When a track completes, capture:
- Track type (what component was built)
- Files created/modified
- Agent output (success/errors/warnings)
- Deliverables produced

### Step 2: Match Against Trigger Rules

```
for each completed_track:
    for each trigger_rule:
        if trigger_rule.matches(completed_track):
            if trigger_rule.condition_met:
                add_to_follow_up_queue(trigger_rule.agent, trigger_rule.priority)
```

### Step 3: Deduplicate Triggers

If multiple triggers spawn the same agent, merge into single task:
```
// Before dedup:
- @accessibility-engineer (from component)
- @accessibility-engineer (from page)
- @accessibility-engineer (from styles)

// After dedup:
- @accessibility-engineer (comprehensive audit: component, page, styles)
```

### Step 4: Execute Follow-Up Queue

```
// Process by priority
while follow_up_queue not empty:
    critical_tasks = filter(queue, priority=CRITICAL)
    if critical_tasks:
        execute_immediately(critical_tasks)
        continue

    high_tasks = filter(queue, priority=HIGH)
    execute_parallel(high_tasks, max=3)

    medium_tasks = filter(queue, priority=MEDIUM)
    execute_parallel(medium_tasks, max=2)

    low_tasks = filter(queue, priority=LOW)
    batch_execute(low_tasks)
```

### Step 5: Handle Follow-Up Results

- If follow-up finds issues → spawn @debugger
- If follow-up completes clean → mark track as verified
- If follow-up fails → escalate to synthesis

## Trigger Detection Patterns

### File Type Detection

```markdown
| File Pattern | Triggers |
|--------------|----------|
| `*.tsx`, `*.jsx` | @accessibility-engineer, @test-engineer |
| `*.ts` (API routes) | @security-engineer, @test-engineer |
| `*.css`, `*.scss` | @accessibility-engineer (contrast) |
| `schema.ts`, `*.prisma` | @test-engineer (migrations) |
| `*.test.*`, `*.spec.*` | None (already tests) |
```

### Code Pattern Detection

```markdown
| Code Pattern | Triggers |
|--------------|----------|
| `useEffect`, `fetch`, `axios` | @performance-engineer |
| `password`, `token`, `auth` | @security-engineer |
| `form`, `input`, `submit` | @accessibility-engineer, @test-engineer |
| `animation`, `transition`, `gsap` | @performance-engineer |
| `<img`, `Image` | @accessibility-engineer (alt), @performance-engineer |
```

### Output Pattern Detection

```markdown
| Output Pattern | Triggers |
|----------------|----------|
| Contains "error" | @debugger (CRITICAL) |
| Contains "warning" | @debugger (HIGH) |
| Contains "TODO" | Log for follow-up |
| Contains "FIXME" | @debugger (MEDIUM) |
| Build failed | @debugger (CRITICAL) |
```

## Follow-Up Task Templates

### @test-engineer Follow-Up
```markdown
## Follow-Up: Test Coverage

**Trigger:** New code created without tests
**Files:** [list of files needing tests]

### Task
Write tests for the newly created code:
- Unit tests for functions/utilities
- Component tests for React components
- Integration tests for API endpoints

### Deliverables
- Test files created
- All tests passing
- Coverage report
```

### @accessibility-engineer Follow-Up
```markdown
## Follow-Up: Accessibility Audit

**Trigger:** UI components created
**Files:** [list of component files]

### Task
Audit new UI for accessibility:
- Keyboard navigation
- Screen reader compatibility
- Color contrast
- Focus management
- ARIA attributes

### Deliverables
- Issues identified
- Fixes applied
- Audit report
```

### @security-engineer Follow-Up
```markdown
## Follow-Up: Security Review

**Trigger:** Auth/API code created
**Files:** [list of security-sensitive files]

### Task
Review code for security vulnerabilities:
- Input validation
- Authentication flows
- Authorization checks
- Data exposure risks
- OWASP top 10

### Deliverables
- Vulnerabilities identified
- Fixes applied
- Security report
```

### @performance-engineer Follow-Up
```markdown
## Follow-Up: Performance Check

**Trigger:** Animation/data fetching added
**Files:** [list of files with perf implications]

### Task
Audit for performance issues:
- Animation performance (60fps)
- Bundle size impact
- Data fetching efficiency
- Render optimization

### Deliverables
- Performance metrics
- Optimizations applied
- Performance report
```

### @debugger Follow-Up
```markdown
## Follow-Up: Error Resolution

**Trigger:** Errors in agent output
**Errors:** [list of errors]

### Task
Investigate and fix errors:
- Identify root cause
- Apply fix
- Verify resolution
- Prevent regression

### Deliverables
- Errors resolved
- Fix explanation
- Prevention strategy
```

## Autonomous Behavior Rules

1. **No User Checkpoints**: Follow-ups execute automatically
2. **Self-Healing**: If follow-up finds issues, spawn fix agents
3. **Completion Required**: Task not done until all follow-ups pass
4. **Escalation Path**: Critical issues surface to synthesis phase
5. **Parallel Execution**: Non-conflicting follow-ups run simultaneously

## Quality Checklist

- [ ] All track completions monitored
- [ ] Trigger rules matched
- [ ] Priorities assigned correctly
- [ ] Follow-ups deduplicated
- [ ] Queue executed by priority
- [ ] Results handled appropriately
- [ ] No manual intervention required
