---
skill: synthesis-patterns
version: "1.0.0"
description: "Combine outputs from multiple agents into coherent, actionable summaries"
used-by:
  - orchestrator
  - research-controller
  - planning-controller
  - discovery-controller
  - qa-controller
  - design-controller
---

# Synthesis Patterns Skill

## Purpose

Transform raw outputs from multiple specialist agents into coherent, actionable summaries that provide clear value to the user.

## Step-by-Step Procedure

### Step 1: Collect Agent Outputs

Gather all outputs, noting:
- Agent name and role
- Task that was assigned
- Raw output produced
- Files created/modified
- Status (complete, partial, failed)

### Step 2: Categorize Outputs

| Category | Examples | Treatment |
|----------|----------|-----------|
| **Artifacts** | Code files, configs | List paths, summarize purpose |
| **Analysis** | Audit results, research | Extract key findings |
| **Decisions** | Architecture choices | Document rationale |
| **Issues** | Errors, warnings | Prioritize by severity |
| **Recommendations** | Next steps, improvements | Organize by priority |

### Step 3: Identify Themes and Conflicts

- Look for **recurring themes** across outputs
- Flag **contradictions** between agents
- Note **gaps** where no agent addressed a need
- Highlight **synergies** where outputs complement each other

### Step 4: Apply Synthesis Template

Use the appropriate template based on context (see Patterns below).

### Step 5: Validate Synthesis

- [ ] All agent outputs represented
- [ ] No critical information lost
- [ ] Conflicts resolved or flagged
- [ ] Next steps are actionable
- [ ] User can understand without reading raw outputs

## Synthesis Patterns

### Pattern 1: Task Completion Summary

Use after: Implementation tasks complete

```markdown
## Task Complete: [Task Name]

### Summary
[2-3 sentence overview of what was accomplished]

### Deliverables
| Agent | Output | Location |
|-------|--------|----------|
| @react-engineer | Header component | /src/components/Header.tsx |
| @style-engineer | Header styles | /src/styles/header.css |

### Key Decisions
- [Decision 1]: [Rationale]
- [Decision 2]: [Rationale]

### Files Changed
- Created: [list]
- Modified: [list]

### Next Steps
1. [Immediate follow-up]
2. [Suggested enhancement]
```

### Pattern 2: Research Synthesis

Use after: Multiple research agents return findings

```markdown
## Research Complete: [Topic]

### Executive Summary
[1 paragraph distillation of all findings]

### Key Findings

#### From @web-researcher
- Finding 1
- Finding 2

#### From @documentation-researcher
- Finding 1
- Finding 2

### Comparative Analysis
| Aspect | Option A | Option B | Recommendation |
|--------|----------|----------|----------------|
| [Criteria 1] | [Value] | [Value] | [Choice] |

### Consensus Points
- [Point all sources agree on]

### Conflicts to Resolve
- [Contradiction between sources]

### Recommended Path Forward
[Synthesized recommendation with rationale]
```

### Pattern 3: Audit Consolidation

Use after: Multiple QA/audit agents complete

```markdown
## Quality Audit Complete

### Overall Score: [X/100]

### Summary by Category

#### Accessibility (@accessibility-auditor)
- Score: [X/100]
- Critical Issues: [count]
- Warnings: [count]

#### Performance (@performance-auditor)
- Score: [X/100]
- LCP: [value]
- FID: [value]

#### Security (@security-auditor)
- Score: [X/100]
- Vulnerabilities: [count]

### Priority Issues (Must Fix)
1. [Issue]: [Location] - [Impact]
2. [Issue]: [Location] - [Impact]

### Recommendations (Should Fix)
1. [Recommendation]
2. [Recommendation]

### Detailed Reports
- [Link to full accessibility report]
- [Link to full performance report]
```

### Pattern 4: Discovery Synthesis

Use after: Discovery phase agents complete

```markdown
## Discovery Complete: [Project Name]

### Project Overview
[Synthesized understanding of the project]

### Brand Analysis (from @brand-analyst)
- Primary Colors: [values]
- Typography: [fonts]
- Voice/Tone: [description]

### Content Structure (from @structure-analyst)
- Pages identified: [count]
- Components needed: [count]
- Content types: [list]

### Technical Requirements (from @figma-analyst)
- Design tokens: [count]
- Breakpoints: [list]
- Animations: [list]

### Synthesized Specifications
[Combined recommendations for implementation]

### Recommended Approach
1. [Phase 1]
2. [Phase 2]
3. [Phase 3]
```

### Pattern 5: Error Aggregation

Use when: Multiple agents encounter issues

```markdown
## Execution Issues Encountered

### Critical Failures
| Agent | Error | Impact | Resolution |
|-------|-------|--------|------------|
| @agent-1 | [error] | [impact] | [fix needed] |

### Warnings
- @agent-2: [warning message]
- @agent-3: [warning message]

### Partial Completions
- @agent-4: Completed 3/5 subtasks
  - Done: [list]
  - Remaining: [list]

### Recovery Plan
1. [Immediate action to resolve blockers]
2. [Retry strategy]
3. [Alternative approach if retry fails]
```

## Synthesis Techniques

### Technique 1: Hierarchical Summarization
```
Level 1: One-sentence overview
Level 2: Paragraph summary (3-5 sentences)
Level 3: Detailed findings by agent
Level 4: Raw outputs (linked, not included)
```

### Technique 2: Cross-Reference Matrix
When outputs overlap, create comparison:
```
| Aspect | Agent A Says | Agent B Says | Synthesis |
|--------|--------------|--------------|-----------|
```

### Technique 3: Priority Stacking
Order information by actionability:
1. Must act now (blockers, critical issues)
2. Should act soon (important findings)
3. Could act later (nice-to-haves)
4. For reference (context, background)

## Common Pitfalls

1. **Information overload**: Including too much raw detail
   - Fix: Summarize ruthlessly; link to details

2. **Lost attribution**: Not crediting which agent produced what
   - Fix: Always tag findings with source agent

3. **False consensus**: Assuming agreement when agents didn't address same topics
   - Fix: Note when findings are from single source

4. **Buried conflicts**: Hiding contradictions in prose
   - Fix: Call out conflicts explicitly in dedicated section

5. **Missing actionability**: Synthesis reads like report, not guidance
   - Fix: Always end with concrete next steps

## Quality Checklist

Before delivering synthesis:
- [ ] Executive summary captures essence
- [ ] All agent outputs represented
- [ ] Sources properly attributed
- [ ] Conflicts explicitly addressed
- [ ] Priorities clearly ordered
- [ ] Next steps are actionable
- [ ] User can act without reading raw outputs
