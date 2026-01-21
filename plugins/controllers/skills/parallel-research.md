---
skill: parallel-research
version: "1.0.0"
description: "Orchestrate parallel scout execution for comprehensive research before planning"
used-by:
  - orchestrator
  - planning-phase
  - decompose-phase
requires:
  - repo-scout
  - context-scout
  - practice-scout
  - docs-scout
  - memory-scout
---

# Parallel Research Skill

## Purpose

Gather comprehensive context before planning by running multiple specialized scouts concurrently. This front-loads research to ensure the DECOMPOSE phase has all necessary information.

## When to Use

- **MODERATE/COMPLEX mode** - Before creating tracks in DECOMPOSE phase
- **New feature implementation** - When building something without existing patterns
- **Technology integration** - When adding new libraries or frameworks
- **Unfamiliar codebase areas** - When working in unknown territory

## Scout Roster

| Scout | Purpose | Tools | When to Use |
|-------|---------|-------|-------------|
| `@repo-scout` | Existing patterns in codebase | Grep, Glob, Read | Always |
| `@context-scout` | Type definitions and signatures | Grep, Glob, Read | When types matter |
| `@practice-scout` | Industry best practices | Web, Grep | New features |
| `@docs-scout` | Framework documentation | Web, Read | External integrations |
| `@memory-scout` | Previous learnings | Read, Grep | If memory enabled |

## Execution Pattern

### Step 1: Determine Scout Selection

Based on the task, select which scouts to spawn:

```markdown
## Scout Selection for: [Topic]

| Scout | Include | Reason |
|-------|---------|--------|
| repo-scout | Yes | Always check existing patterns |
| context-scout | [Yes/No] | [Types needed / Simple implementation] |
| practice-scout | [Yes/No] | [New feature / Familiar territory] |
| docs-scout | [Yes/No] | [Uses external lib / Internal only] |
| memory-scout | [Yes/No] | [Memory enabled / Not configured] |
```

### Step 2: Spawn All Scouts in Parallel

**CRITICAL:** Spawn all selected scouts in a SINGLE message to maximize parallelization.

```
# In ONE Tool call block, spawn all scouts:

Task(@repo-scout, """
  ## Research Topic: [topic]

  Find existing patterns for:
  - [specific pattern 1]
  - [specific pattern 2]

  Focus areas:
  - File structure and naming
  - Import patterns
  - Test patterns

  Return: Patterns summary with file:line references
""")

Task(@context-scout, """
  ## Research Topic: [topic]

  Extract signatures for:
  - Related types and interfaces
  - Component props
  - Hook return types

  Return: Type definitions and module relationships
""")

Task(@practice-scout, """
  ## Research Topic: [topic]

  Research best practices for:
  - [specific practice area]
  - Security considerations
  - Performance implications

  Tech stack: [framework, libraries]

  Return: Recommendations with sources
""")

Task(@docs-scout, """
  ## Research Topic: [topic]

  Find documentation for:
  - [specific API/feature]
  - Configuration options
  - Migration notes (if version differs)

  Installed versions: [from package.json]

  Return: API reference and examples
""")

Task(@memory-scout, """
  ## Research Topic: [topic]

  Search memory for:
  - Pitfalls related to [topic]
  - Conventions for [domain]
  - Relevant architectural decisions

  Return: Applicable learnings and warnings
""")
```

### Step 3: Collect and Synthesize Results

All scouts return within ~30 seconds. Combine findings:

```markdown
## Research Synthesis: [Topic]

### From Codebase (repo-scout)
**Existing Patterns:**
- [Pattern 1]: Found in `file.ts:23`
- [Pattern 2]: Found in `other.ts:45`

**File Structure:**
- Components: `src/components/[feature]/`
- Hooks: `src/hooks/use[Feature].ts`

**Naming Conventions:**
- [Convention 1]
- [Convention 2]

### From Types (context-scout)
**Key Interfaces:**
```typescript
interface RelevantType {
  // extracted signature
}
```

**Component Signatures:**
- `ComponentName(props: Props): JSX.Element`

### From Best Practices (practice-scout)
**Recommendations:**
1. [Practice 1] - [rationale]
2. [Practice 2] - [rationale]

**Pitfalls to Avoid:**
- [Anti-pattern 1]
- [Anti-pattern 2]

**Security Considerations:**
- [Security note]

### From Documentation (docs-scout)
**API Reference:**
- `function(): ReturnType` - [description]

**Configuration:**
```typescript
// recommended config
```

### From Memory (memory-scout)
**Previous Pitfalls:**
- [Pitfall]: [how to avoid]

**Conventions to Follow:**
- [Convention]: [requirement]

**Relevant Decisions:**
- [Decision]: [what it means for this task]

---

## Synthesis: Implementation Guidance

### Must Do
1. [Required action from research]
2. [Required action from research]

### Should Do
1. [Recommended action]
2. [Recommended action]

### Must Avoid
1. [Anti-pattern from research]
2. [Anti-pattern from research]

### Open Questions
- [Anything needing clarification]
```

## Scout Selection Guidelines

### Always Include
- **repo-scout** - Existing patterns are always relevant

### Include for New Features
- **practice-scout** - Industry best practices
- **docs-scout** - If using external libraries

### Include for Complex Types
- **context-scout** - When types and interfaces matter

### Include if Configured
- **memory-scout** - Only if `.tasks/memory/` exists

## Timing Expectations

| Scout | Typical Duration | Token Usage |
|-------|------------------|-------------|
| repo-scout | 5-15 seconds | Low (Grep/Glob) |
| context-scout | 10-20 seconds | Medium (targeted reads) |
| practice-scout | 15-30 seconds | Medium (web search) |
| docs-scout | 15-30 seconds | Medium (web fetch) |
| memory-scout | 5-10 seconds | Low (file reads) |

**Total parallel research:** ~30 seconds (scouts run concurrently)

## Token Efficiency

**Reference:** Each scout has its own token budget. See `token-efficient-exploration.md` for patterns.

### Combined Token Budget

| Scout | Target | Max |
|-------|--------|-----|
| repo-scout | 1000 | 2000 |
| context-scout | 1200 | 2500 |
| practice-scout | 1300 | 2500 |
| docs-scout | 1500 | 3000 |
| memory-scout | 550 | 1100 |
| **Total (all scouts)** | **5550** | **11100** |

### Efficiency Rules

1. **Scout selection reduces total cost**
   - Don't spawn all 5 scouts for every task
   - repo-scout is mandatory; others are selective
   - See "Scout Selection Guidelines" above

2. **Scouts are parallel, not sequential**
   - Token budgets don't compound across time
   - All scouts work simultaneously
   - Total cost = sum of selected scouts

3. **Synthesis should be compact**
   - Summarize findings, don't paste scout outputs
   - Focus on actionable guidance
   - Reference file:line for details

4. **Diminishing returns threshold**
   - If 3 scouts found nothing relevant, stop
   - Don't search harder when context is clear
   - Greenfield projects need practice-scout, not more searching

## Integration with Orchestration

### In DECOMPOSE Phase

Before creating tracks:

```markdown
## Phase 2: DECOMPOSE

### Step 0: Parallel Research (NEW)
If task involves implementation:
1. Run parallel research with relevant scouts
2. Wait for all scouts to complete
3. Synthesize findings
4. Use synthesis to inform track decomposition

### Step 1: Identify Request Domain
[existing steps continue...]
```

### Research Output Feeds Track Creation

```
Research Synthesis
       ↓
Patterns found → Inform component structure
Best practices → Inform quality requirements
Type signatures → Inform interface design
Memory pitfalls → Inform constraints
       ↓
Track Decomposition (with full context)
```

## Error Handling

### If Scout Fails
- Continue with other scouts
- Note missing information in synthesis
- Flag as potential risk for DECOMPOSE

### If No Patterns Found
- Note that this may be greenfield
- Rely more heavily on practice-scout
- Document as new territory

### If Memory Empty
- Skip memory-scout results
- Note to capture learnings after implementation

## Quality Checklist

Before proceeding to DECOMPOSE:
- [ ] All selected scouts completed
- [ ] Findings synthesized into single document
- [ ] Existing patterns identified
- [ ] Best practices documented
- [ ] Pitfalls flagged
- [ ] Open questions listed
- [ ] Implementation guidance clear
