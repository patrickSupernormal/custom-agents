---
skill: error-escalation
version: "1.0.0"
description: "Determine when to escalate issues and how to handle agent failures gracefully"
used-by:
  - orchestrator
  - frontend-controller
  - backend-controller
  - qa-controller
  - devops-controller
  - all-specialist-agents
---

# Error Escalation Skill

## Purpose

Provide a consistent framework for handling errors, determining when human intervention is needed, and gracefully recovering from agent failures.

## Step-by-Step Procedure

### Step 1: Classify Error Severity

| Severity | Criteria | Response |
|----------|----------|----------|
| **CRITICAL** | Blocks all progress; data loss risk; security issue | Immediate escalation |
| **HIGH** | Blocks current task; no workaround; affects deliverable | Escalate within 1 attempt |
| **MEDIUM** | Delays task; workaround exists; partial impact | Retry then escalate |
| **LOW** | Minor inconvenience; doesn't block; cosmetic | Log and continue |

### Step 2: Attempt Recovery

Before escalating, try recovery based on error type:

```
Error Type: FILE_NOT_FOUND
├── Check path spelling
├── Verify directory exists
├── Search for similar filenames
└── Ask user for correct path

Error Type: PERMISSION_DENIED
├── Check file permissions
├── Verify user has access
└── Escalate if system-level issue

Error Type: AGENT_TIMEOUT
├── Check task complexity
├── Break into smaller subtasks
├── Retry with simpler scope
└── Escalate if repeated timeout

Error Type: INVALID_OUTPUT
├── Review agent instructions
├── Clarify requirements
├── Retry with explicit constraints
└── Escalate if quality remains poor
```

### Step 3: Document Error Context

Before escalating, capture:
```yaml
error_report:
  timestamp: [when it occurred]
  agent: [which agent failed]
  task: [what was being attempted]
  error_type: [classification]
  error_message: [exact error text]
  context:
    - files_involved: [list]
    - dependencies: [list]
    - previous_attempts: [count]
  recovery_attempts:
    - attempt_1: [what was tried, result]
    - attempt_2: [what was tried, result]
  impact:
    - blocked_tasks: [list]
    - affected_deliverables: [list]
```

### Step 4: Escalation Decision Tree

```
Is there a security or data loss risk?
├── YES → ESCALATE IMMEDIATELY
└── NO → Have you tried recovery?
          ├── NO → Attempt recovery first
          └── YES → Did recovery work?
                    ├── YES → Continue
                    └── NO → Is this blocking critical path?
                              ├── YES → ESCALATE
                              └── NO → Can you work around it?
                                        ├── YES → Continue with workaround, log issue
                                        └── NO → ESCALATE
```

### Step 5: Escalate Appropriately

| Escalation Target | When to Use |
|-------------------|-------------|
| **User** | Requires human decision; ambiguous requirements; access needed |
| **Higher Controller** | Cross-domain issue; resource conflict; priority decision |
| **Original Orchestrator** | Task cannot be completed; need to re-route |
| **External System** | Infrastructure issue; third-party service failure |

## Escalation Templates

### Template 1: User Escalation

```markdown
## Action Required: [Brief Issue Title]

### What Happened
[1-2 sentence description of the error]

### What I Tried
1. [Recovery attempt 1]
2. [Recovery attempt 2]

### Why I Need Your Help
[Explain what decision or action requires human input]

### Options
1. **[Option A]**: [description and tradeoff]
2. **[Option B]**: [description and tradeoff]
3. **[Option C]**: Provide different guidance

### Impact If Not Resolved
- [Blocked task 1]
- [Blocked task 2]
```

### Template 2: Controller Escalation

```markdown
## Controller Escalation: [Error Type]

### Agent: @[agent-name]
### Task: [task description]
### Severity: [CRITICAL/HIGH/MEDIUM]

### Error Details
```
[Error message or stack trace]
```

### Context
- Task was part of: [larger workflow]
- Dependencies: [what this was blocking]
- Files involved: [list]

### Recovery Attempts
| Attempt | Action | Result |
|---------|--------|--------|
| 1 | [action] | [result] |
| 2 | [action] | [result] |

### Recommended Resolution
[What the controller should do]

### Alternative Paths
1. [Alternative approach]
2. [Fallback option]
```

### Template 3: Graceful Degradation Notice

```markdown
## Proceeding with Limitations

### Issue Encountered
[Description of non-blocking issue]

### Impact
- [What won't work as expected]
- [Reduced functionality]

### Workaround Applied
[What was done to continue]

### To Fully Resolve
[What would fix it properly - for later]

### Continuing with: [next task]
```

## Error Recovery Patterns

### Pattern 1: Retry with Backoff
```
Attempt 1: Immediate retry
Attempt 2: Wait 5 seconds, retry
Attempt 3: Wait 15 seconds, retry with simplified scope
Attempt 4: Escalate
```

### Pattern 2: Fallback Chain
```
Primary approach failed
├── Try fallback approach A
│   ├── Success → Continue
│   └── Fail → Try fallback approach B
│             ├── Success → Continue (degraded)
│             └── Fail → Escalate
```

### Pattern 3: Isolation and Continue
```
Task A failed
├── Isolate Task A
├── Mark as blocked
├── Continue with independent Task B, C, D
└── Revisit Task A after other progress
```

### Pattern 4: Scope Reduction
```
Full task failed
├── Reduce scope by 50%
├── Retry reduced scope
│   ├── Success → Report partial completion
│   └── Fail → Reduce scope again or escalate
```

## Common Error Scenarios

### Scenario 1: Agent Produces Invalid Output
```
Detection: Output doesn't match expected format/quality
Recovery:
1. Clarify requirements in task prompt
2. Provide explicit examples of expected output
3. Retry with stricter constraints
4. If still failing, try different agent or approach
Escalation trigger: 3 failed attempts
```

### Scenario 2: File Conflict
```
Detection: Two agents trying to modify same file
Recovery:
1. Serialize the operations
2. Merge changes if compatible
3. Ask user to resolve if incompatible
Escalation trigger: Incompatible changes detected
```

### Scenario 3: Missing Dependency
```
Detection: Required input not available
Recovery:
1. Check if dependency task completed
2. Wait and poll for completion
3. Route task to create missing dependency
Escalation trigger: Circular dependency or missing task
```

### Scenario 4: External Service Failure
```
Detection: API timeout, service unavailable
Recovery:
1. Retry with exponential backoff
2. Check service status
3. Use cached data if available
Escalation trigger: Service down for extended period
```

## Common Pitfalls

1. **Silent failures**: Not reporting errors to maintain "progress"
   - Fix: Always surface errors, even if continuing

2. **Over-escalation**: Escalating every minor issue
   - Fix: Follow severity classification; attempt recovery first

3. **Under-escalation**: Spinning on unsolvable problems
   - Fix: Set clear retry limits; escalate after threshold

4. **Lost context**: Escalating without enough information
   - Fix: Always include full error report with recovery attempts

5. **Cascading failures**: One error causing chain of failures
   - Fix: Isolate failing tasks; continue independent work

## Escalation Checklist

Before escalating:
- [ ] Error severity classified
- [ ] Recovery attempts documented
- [ ] Context fully captured
- [ ] Impact assessed
- [ ] Options identified
- [ ] Escalation template completed
- [ ] Correct escalation target identified
