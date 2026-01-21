---
skill: memory-management
version: "1.0.0"
description: "Patterns for using the persistent memory system to learn from experience"
used-by:
  - orchestrator
  - worker
  - follow-up-triggers
requires:
  - taskctl CLI
---

# Memory Management Skill

## Purpose

Leverage the persistent memory system to learn from past experiences, avoid repeated mistakes, and maintain consistency across sessions. Memory survives context compaction and session boundaries.

## Memory System Overview

### Storage Location
```
.tasks/memory/
├── pitfalls.md      # Mistakes to avoid
├── conventions.md   # Patterns to follow
└── decisions.md     # Choices already made
```

### Memory Types

| Type | Purpose | When to Capture |
|------|---------|-----------------|
| **Pitfall** | Mistakes and gotchas | After fixing unexpected bugs, failed reviews |
| **Convention** | Patterns and standards | When establishing new patterns |
| **Decision** | Architectural choices | When making trade-offs |

## Setup

### Enable Memory System

```bash
# Initialize memory (creates .tasks/memory/ directory)
taskctl memory init

# Enable memory in config
taskctl config set memory.enabled true

# Verify
taskctl config get memory.enabled
```

### Check Memory Status

```bash
# List all memory
taskctl memory list

# List by type
taskctl memory list --type pitfall
taskctl memory list --type convention
taskctl memory list --type decision
```

## Adding Memories

### Command Syntax

```bash
taskctl memory add --type <pitfall|convention|decision> "<content>"
```

### Pitfall Examples

```bash
# Bug fix learning
taskctl memory add --type pitfall "useState with objects needs spread operator for updates - direct mutation doesn't trigger re-render"

# Build issue
taskctl memory add --type pitfall "Next.js 14 requires 'use client' directive for components using hooks in App Router"

# Security issue
taskctl memory add --type pitfall "Never log request bodies in production - may contain sensitive data like passwords"
```

### Convention Examples

```bash
# Naming convention
taskctl memory add --type convention "All custom hooks must start with 'use' prefix and be in src/hooks/ directory"

# Code pattern
taskctl memory add --type convention "API error responses follow { error: string, code: number } shape"

# File structure
taskctl memory add --type convention "Feature components go in src/features/[feature]/components/"
```

### Decision Examples

```bash
# Technology choice
taskctl memory add --type decision "Chose Zustand over Redux - simpler API, smaller bundle, sufficient for our state needs"

# Architecture choice
taskctl memory add --type decision "Using tRPC instead of REST - type safety across client/server, better DX"

# Pattern choice
taskctl memory add --type decision "Opted for server components by default, 'use client' only when needed for interactivity"
```

## Reading Memory

### In Re-anchor Phase

Before implementing, check memory for relevant learnings:

```bash
# Check all memory types
taskctl memory list --type pitfall
taskctl memory list --type convention
taskctl memory list --type decision

# Or use memory-scout agent for intelligent filtering
Task(@memory-scout, "Search memory for: [topic]")
```

### Search Patterns

```bash
# Search within memory files
Grep("auth|login", ".tasks/memory/*.md", output_mode: "content")

# Search specific type
Grep("[topic]", ".tasks/memory/pitfalls.md", output_mode: "content", -B: 2, -A: 5)
```

## When to Capture

### Automatic Capture (via follow-up-triggers)

| Event | Memory Type | Example |
|-------|-------------|---------|
| @debugger fixes non-obvious bug | Pitfall | "Array.map with async needs Promise.all wrapper" |
| Review verdict: NEEDS_WORK | Pitfall | "Missing null check on API response" |
| @qa-auditor recommends pattern | Convention | "All forms must use react-hook-form with zod validation" |
| Architecture choice during DECOMPOSE | Decision | "Using edge runtime for API routes requiring low latency" |

### Manual Capture

Encourage team members to add memories when:
- They discover something unexpected
- They establish a new pattern
- They make a significant decision
- They fix a bug that others might encounter

## Memory in Worker Agent

### Re-anchor with Memory

```markdown
## Worker Phase 1: Re-anchor

1. Read task spec
2. Read epic context
3. Check git state
4. **Check memory (if enabled)**
   ```bash
   # Check if memory is available
   taskctl config get memory.enabled

   # If true, read relevant entries
   taskctl memory list --type pitfall
   taskctl memory list --type convention
   ```
5. Validate starting point
```

### Apply Memory During Implementation

```markdown
## Worker Phase 2: Implement

When implementing, apply memory:

1. **Check pitfalls before writing code**
   - "Am I about to make a mistake we've seen before?"
   - Reference: `.tasks/memory/pitfalls.md`

2. **Follow conventions**
   - "Does this follow our established patterns?"
   - Reference: `.tasks/memory/conventions.md`

3. **Respect decisions**
   - "Am I contradicting a previous decision?"
   - Reference: `.tasks/memory/decisions.md`
```

### Capture Memory After Implementation

```markdown
## Worker Phase 4: Complete

Before returning:

If non-obvious issue was resolved:
  taskctl memory add --type pitfall "[description of issue and solution]"

If new pattern was established:
  taskctl memory add --type convention "[description of pattern]"

If significant decision was made:
  taskctl memory add --type decision "[decision and rationale]"
```

## Memory File Format

### pitfalls.md
```markdown
# Pitfalls

Known issues and gotchas to avoid.

## 2026-01-21T10:30:00Z

useState with objects needs spread operator for updates - direct mutation doesn't trigger re-render

## 2026-01-21T11:45:00Z

Next.js 14 requires 'use client' directive for components using hooks in App Router
```

### conventions.md
```markdown
# Conventions

Project conventions and patterns.

## 2026-01-21T10:30:00Z

All custom hooks must start with 'use' prefix and be in src/hooks/ directory

## 2026-01-21T11:45:00Z

API error responses follow { error: string, code: number } shape
```

### decisions.md
```markdown
# Decisions

Architectural and design decisions.

## 2026-01-21T10:30:00Z

Chose Zustand over Redux - simpler API, smaller bundle, sufficient for our state needs

## 2026-01-21T11:45:00Z

Using tRPC instead of REST - type safety across client/server, better DX
```

## Best Practices

### Writing Good Memory Entries

1. **Be Specific**
   - Bad: "Forms are tricky"
   - Good: "react-hook-form requires mode: 'onChange' for real-time validation display"

2. **Include Context**
   - Bad: "Use edge runtime"
   - Good: "Use edge runtime for auth API routes - reduces cold start latency for login flows"

3. **Explain the Why**
   - Bad: "Don't use Redux"
   - Good: "Chose Zustand over Redux - simpler API, smaller bundle, sufficient for our current state complexity"

### Maintaining Memory

1. **Regular Review**: Periodically review memories for relevance
2. **Deduplication**: Combine similar entries
3. **Archiving**: Move outdated entries to archive section
4. **Tagging**: Use consistent tags (#auth, #forms, #api) for searchability

## Integration Points

### With Parallel Research
```
Task(@memory-scout, "Search memory for: [topic]")
```

### With Worker Re-anchor
```bash
# Phase 1 includes memory check
taskctl memory list --type pitfall
taskctl memory list --type convention
```

### With Follow-up Triggers
```bash
# After @debugger fixes issue
taskctl memory add --type pitfall "[issue description]"
```

## Quality Checklist

- [ ] Memory system initialized (`taskctl memory init`)
- [ ] Memory enabled in config
- [ ] Relevant pitfalls captured after bug fixes
- [ ] Conventions documented when patterns established
- [ ] Decisions recorded with rationale
- [ ] Memory checked during re-anchor phase
- [ ] Entries are specific and actionable
