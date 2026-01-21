---
skill: stakeholder-extraction
version: "1.0.0"
description: "Processing kickoff materials, transcripts, and stakeholder input"
used-by:
  - "@kickoff-processor"
  - "@requirements-extractor"
  - "@discovery-controller"
---

# Stakeholder Extraction

## Overview

Systematic approach to extracting actionable requirements, insights, and context from kickoff meetings, client materials, transcripts, and stakeholder communications.

---

## Phase 1: Material Inventory

### Input Types
```
MEETING ARTIFACTS
├── Transcripts (Zoom, Teams, etc.)
├── Recording summaries
├── Meeting notes
└── Chat logs

DOCUMENTS
├── RFPs / Briefs
├── Brand guidelines
├── Existing site audits
├── Competitor lists
└── Content inventories

COMMUNICATIONS
├── Email threads
├── Slack conversations
├── Feedback documents
└── Revision requests

ASSETS
├── Logos and brand files
├── Content (copy, images)
├── Wireframes or mockups
└── Reference links
```

### Material Triage
| Priority | Type | Action |
|----------|------|--------|
| P1 | Direct requirements | Extract immediately |
| P2 | Context/background | Summarize key points |
| P3 | Reference material | Catalog for later |
| P4 | Nice-to-have | Note existence only |

---

## Phase 2: Extraction Framework

### Requirement Categories
```
EXPLICIT REQUIREMENTS (Directly stated)
├── "We need X"
├── "Must have Y"
├── "The site should Z"

IMPLICIT REQUIREMENTS (Inferred from context)
├── Industry standards
├── Competitor features mentioned positively
├── Problems described = solutions needed

CONSTRAINTS (Limitations stated)
├── Budget limits
├── Timeline deadlines
├── Technical restrictions
├── Brand requirements

PREFERENCES (Nice-to-haves)
├── "We like..."
├── "If possible..."
├── "Ideally..."
```

### Extraction Template
```markdown
## Extracted Requirement

**Source**: [Document/Transcript name, timestamp/page]
**Quote**: "[Exact words used]"
**Category**: Explicit/Implicit/Constraint/Preference
**Priority**: P1/P2/P3/P4

**Interpreted Requirement**:
[Clear, actionable statement]

**Confidence**: High/Medium/Low
**Needs Clarification**: Yes/No
**Clarification Question**: [If yes, what to ask]
```

---

## Phase 3: Transcript Processing

### Key Signals to Capture

**Priority Indicators**
- "Most important..." / "Critical..."
- "Must have..." / "Need to..."
- "Can't launch without..."
- "Non-negotiable..."

**Preference Indicators**
- "We like..." / "We prefer..."
- "It would be nice..." / "Ideally..."
- "If budget allows..." / "If time permits..."

**Concern Indicators**
- "Worried about..." / "Concerned that..."
- "Problem with current..." / "Pain point..."
- "Don't want..." / "Avoid..."

**Stakeholder Dynamics**
- Who speaks most? (Decision maker?)
- Who gets final word? (Approver?)
- Who asks technical questions? (Implementer?)

### Transcript Parsing Template
```markdown
## Transcript Analysis: [Meeting Name]

### Participants
| Name | Role | Influence Level | Key Concerns |
|------|------|-----------------|--------------|
| [X]  | [Y]  | High/Med/Low    | [Z]          |

### Timeline Extracted
| Timestamp | Speaker | Key Statement | Category |
|-----------|---------|---------------|----------|
| 00:05:23  | [Name]  | "[Quote]"     | Requirement |

### Themes Identified
1. [Theme] - Mentioned [N] times by [speakers]
2. [Theme] - Mentioned [N] times by [speakers]

### Action Items Mentioned
- [ ] [Action] - Owner: [Name]

### Unresolved Questions
- [Question needing follow-up]
```

---

## Phase 4: Synthesis

### Requirements Consolidation
```markdown
## Consolidated Requirements

### Must Have (P1)
| ID | Requirement | Source | Stakeholder |
|----|-------------|--------|-------------|
| R1 | [X]         | [Y]    | [Z]         |

### Should Have (P2)
| ID | Requirement | Source | Stakeholder |
|----|-------------|--------|-------------|

### Could Have (P3)
| ID | Requirement | Source | Stakeholder |

### Explicitly Excluded
| Item | Reason | Source |
|------|--------|--------|
```

### Conflict Resolution
When stakeholders disagree:
```
CONFLICT: [Description]
├── Stakeholder A says: [Position]
├── Stakeholder B says: [Position]
├── Resolution approach: [Escalate/Compromise/Defer]
└── Recommended action: [What to do]
```

---

## Phase 5: Validation

### Completeness Check
- [ ] All materials reviewed
- [ ] Key stakeholders' input captured
- [ ] Explicit requirements listed
- [ ] Implicit requirements inferred
- [ ] Constraints documented
- [ ] Preferences noted
- [ ] Conflicts identified

### Clarity Check
For each requirement ask:
- [ ] Is it specific enough to act on?
- [ ] Is success measurable?
- [ ] Is the priority clear?
- [ ] Is the source documented?

### Gaps Analysis
```markdown
## Information Gaps

### Critical (Blocking Progress)
1. [Missing information] - Need from: [Stakeholder]

### Important (Needed Soon)
1. [Missing information] - Need from: [Stakeholder]

### Nice to Have (Can Proceed Without)
1. [Missing information] - Would help with: [Area]
```

---

## Output Templates

### Discovery Summary
```markdown
## Stakeholder Discovery Summary

### Project Overview
[2-3 sentence project description from stakeholder perspective]

### Key Stakeholders
| Name | Role | Key Priorities |
|------|------|----------------|

### Core Requirements (P1)
1. [Requirement]
2. [Requirement]

### Secondary Requirements (P2)
1. [Requirement]

### Constraints
- Timeline: [X]
- Budget: [Y]
- Technical: [Z]

### Open Questions
1. [Question for stakeholder]

### Next Steps
1. [Action needed]
```

### Follow-Up Questions Template
```markdown
## Clarification Questions for [Stakeholder]

Based on our review of [materials], we have the following questions:

1. **[Topic]**: [Specific question]
   - Context: [Why we're asking]

2. **[Topic]**: [Specific question]
   - Context: [Why we're asking]

Please let us know at your earliest convenience.
```

---

## Common Pitfalls

| Pitfall | Prevention |
|---------|------------|
| Missing implicit requirements | Read between the lines |
| Over-relying on one stakeholder | Capture all voices |
| Assuming understanding | Document and confirm |
| Losing source attribution | Always cite sources |
| Ignoring concerns | Flag worries as requirements |
| Missing non-verbal cues | Note hesitation, emphasis |

---

## Quality Checklist

- [ ] All provided materials processed
- [ ] Requirements attributed to sources
- [ ] Priorities assigned
- [ ] Conflicts flagged
- [ ] Gaps identified
- [ ] Follow-up questions prepared
- [ ] Summary suitable for stakeholder review
