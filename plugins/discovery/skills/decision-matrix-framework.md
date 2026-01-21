---
skill: decision-matrix-framework
version: "1.0.0"
description: "Comprehensive frameworks for decision analysis, tradeoff evaluation, and data-driven recommendations"
used-by:
  - "@decision-analyst"
---

# Decision Matrix Framework

## Overview

Systematic methodology for evaluating tradeoffs, creating weighted decision matrices, and providing data-driven recommendations. This framework enables teams to make informed decisions by comparing alternatives objectively.

---

## 1. Decision Framework Selection

### Framework Selection Matrix
| Decision Type | Recommended Framework | When to Use |
|---------------|----------------------|-------------|
| Binary choice | Pros/Cons Analysis | Simple yes/no decisions |
| Multiple options | Weighted Scoring Matrix | 3-7 alternatives to compare |
| High stakes | Multi-Criteria Decision Analysis | Complex, consequential decisions |
| Resource allocation | Cost-Benefit Analysis | Budget/investment decisions |
| Uncertainty present | Risk-Adjusted Analysis | Outcomes are uncertain |
| Time-sensitive | Rapid Decision Framework | Need decision in < 1 hour |
| Stakeholder conflict | Consensus Building Matrix | Multiple decision-makers disagree |

### Decision Complexity Assessment
```
SIMPLE DECISIONS (Use Pros/Cons)
├── 2 options
├── Few criteria
├── Single decision-maker
└── Easily reversible

MODERATE DECISIONS (Use Weighted Matrix)
├── 3-5 options
├── 5-10 criteria
├── Small team consensus
└── Moderately reversible

COMPLEX DECISIONS (Use MCDA + Risk Analysis)
├── Many options or criteria
├── Multiple stakeholders
├── High stakes
└── Difficult to reverse
```

### Framework Selection Template
```markdown
## Decision Framework Selection

**Decision Statement**: [What are we deciding?]
**Timeline**: [When is decision needed?]
**Reversibility**: [Easy/Moderate/Difficult to undo]
**Stakes**: [Low/Medium/High impact]
**Stakeholders**: [Who needs to agree?]

**Recommended Framework**: [Based on above factors]
**Rationale**: [Why this framework fits]
```

---

## 2. Weighted Scoring Matrix

### Core Methodology
```
WEIGHTED SCORE = Sum of (Criterion Weight x Option Score)

Where:
- Weights sum to 100% (or use points like 1-10)
- Scores typically 1-5 or 1-10 scale
- Higher score = better performance
```

### Standard Weighted Matrix Template
```markdown
## Decision: [Decision Statement]

### Evaluation Criteria
| Criterion | Weight | Rationale for Weight |
|-----------|--------|---------------------|
| [Criterion 1] | [%] | [Why this weight] |
| [Criterion 2] | [%] | [Why this weight] |
| [Criterion 3] | [%] | [Why this weight] |
| **Total** | **100%** | |

### Scoring Guide
| Score | Meaning |
|-------|---------|
| 5 | Excellent - Exceeds requirements |
| 4 | Good - Fully meets requirements |
| 3 | Acceptable - Meets minimum requirements |
| 2 | Poor - Partially meets requirements |
| 1 | Unacceptable - Fails to meet requirements |

### Option Evaluation
| Criterion | Weight | Option A | Option B | Option C |
|-----------|--------|----------|----------|----------|
| [Criterion 1] | [%] | [1-5] | [1-5] | [1-5] |
| [Criterion 2] | [%] | [1-5] | [1-5] | [1-5] |
| [Criterion 3] | [%] | [1-5] | [1-5] | [1-5] |
| **Weighted Total** | | **[calc]** | **[calc]** | **[calc]** |

### Score Calculation
Option A: (W1 x S1) + (W2 x S2) + (W3 x S3) = [Total]
Option B: (W1 x S1) + (W2 x S2) + (W3 x S3) = [Total]
Option C: (W1 x S1) + (W2 x S2) + (W3 x S3) = [Total]
```

### Example: Technology Selection
```markdown
## Decision: Select Frontend Framework

### Evaluation Criteria
| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| Performance | 25% | Core user experience factor |
| Developer Experience | 20% | Team productivity impact |
| Ecosystem/Community | 20% | Long-term support |
| Learning Curve | 15% | Time to productivity |
| Bundle Size | 10% | Mobile performance |
| TypeScript Support | 10% | Code quality |
| **Total** | **100%** | |

### Option Evaluation
| Criterion | Weight | React | Vue | Svelte |
|-----------|--------|-------|-----|--------|
| Performance | 25% | 4 | 4 | 5 |
| Developer Experience | 20% | 4 | 5 | 4 |
| Ecosystem/Community | 20% | 5 | 4 | 3 |
| Learning Curve | 15% | 3 | 4 | 4 |
| Bundle Size | 10% | 3 | 4 | 5 |
| TypeScript Support | 10% | 5 | 4 | 4 |
| **Weighted Total** | | **4.05** | **4.15** | **4.05** |
```

---

## 3. Trade-off Analysis Patterns

### Trade-off Identification Framework
```
TRADE-OFF TYPES
├── Performance vs Cost
├── Speed vs Quality
├── Flexibility vs Simplicity
├── Control vs Convenience
├── Short-term vs Long-term
├── Risk vs Reward
└── Scope vs Timeline
```

### Trade-off Matrix Template
```markdown
## Trade-off Analysis: [Decision]

### Trade-off Pairs Identified
| Trade-off | Option A Favors | Option B Favors |
|-----------|-----------------|-----------------|
| Speed vs Quality | Speed | Quality |
| Cost vs Features | Low Cost | More Features |
| Control vs Ease | More Control | Easier Setup |

### Trade-off Deep Dive
#### [Trade-off 1]: [Dimension A] vs [Dimension B]

**If we optimize for [Dimension A]:**
- Gain: [What we get]
- Lose: [What we sacrifice]
- Risk: [What could go wrong]

**If we optimize for [Dimension B]:**
- Gain: [What we get]
- Lose: [What we sacrifice]
- Risk: [What could go wrong]

**Recommendation**: Optimize for [choice] because [rationale]
```

### Trade-off Visualization
```
                    HIGH QUALITY
                         |
    Expensive but        |       Ideal Zone
    Excellent           |       (if achievable)
                         |
    ─────────────────────┼─────────────────────
    LOW COST             |             HIGH COST
                         |
    Budget Option        |       Overpaying
    (acceptable)         |       (avoid)
                         |
                    LOW QUALITY
```

### Trade-off Resolution Strategies
| Strategy | When to Use | Example |
|----------|-------------|---------|
| Prioritize | Clear winner exists | "Quality is non-negotiable" |
| Compromise | Both matter equally | "Medium quality, medium cost" |
| Sequence | Can address both over time | "MVP now, optimize later" |
| Innovate | Find third option | "Open source solves both" |
| Accept | Trade-off is inherent | "Document the limitation" |

---

## 4. Risk Assessment Frameworks

### Risk Identification Matrix
```markdown
## Risk Assessment: [Decision]

### Risk Categories
| Category | Description | Relevance |
|----------|-------------|-----------|
| Technical | Implementation challenges | [High/Med/Low] |
| Financial | Cost overruns, ROI failure | [High/Med/Low] |
| Operational | Process/workflow disruption | [High/Med/Low] |
| Strategic | Market/competitive impact | [High/Med/Low] |
| Compliance | Legal/regulatory issues | [High/Med/Low] |
| Reputational | Brand/trust damage | [High/Med/Low] |
```

### Risk Scoring Template
```markdown
### Risk Register
| Risk | Probability | Impact | Score | Mitigation |
|------|-------------|--------|-------|------------|
| [Risk 1] | [1-5] | [1-5] | [PxI] | [Strategy] |
| [Risk 2] | [1-5] | [1-5] | [PxI] | [Strategy] |

### Probability Scale
1 = Rare (< 10%)
2 = Unlikely (10-25%)
3 = Possible (25-50%)
4 = Likely (50-75%)
5 = Almost Certain (> 75%)

### Impact Scale
1 = Negligible (Minor inconvenience)
2 = Minor (Some disruption, easily recovered)
3 = Moderate (Significant effort to recover)
4 = Major (Serious damage, difficult recovery)
5 = Catastrophic (Existential threat)
```

### Risk Heat Map
```
IMPACT
  5 |  5 | 10 | 15 | 20 | 25 |  <- Catastrophic
  4 |  4 |  8 | 12 | 16 | 20 |  <- Major
  3 |  3 |  6 |  9 | 12 | 15 |  <- Moderate
  2 |  2 |  4 |  6 |  8 | 10 |  <- Minor
  1 |  1 |  2 |  3 |  4 |  5 |  <- Negligible
    +----+----+----+----+----+
       1    2    3    4    5    PROBABILITY

Risk Zones:
- Green (1-4): Accept/Monitor
- Yellow (5-9): Mitigate
- Orange (10-14): Active Management
- Red (15-25): Avoid/Transfer
```

### Risk-Adjusted Decision Framework
```markdown
## Risk-Adjusted Comparison

| Option | Base Score | Risk Score | Adjusted Score |
|--------|------------|------------|----------------|
| Option A | [weighted] | [risk penalty] | [base - risk] |
| Option B | [weighted] | [risk penalty] | [base - risk] |

Risk Penalty Calculation:
- Sum of (Risk Score / 25) for all identified risks
- Higher risk = higher penalty
- Subtract from base score
```

---

## 5. Cost-Benefit Analysis Templates

### Standard CBA Template
```markdown
## Cost-Benefit Analysis: [Decision]

### Costs
| Cost Category | One-Time | Recurring (Annual) | 5-Year Total |
|---------------|----------|-------------------|--------------|
| Implementation | $X | - | $X |
| Licensing/Fees | - | $X | $5X |
| Training | $X | $X | $X + $5X |
| Maintenance | - | $X | $5X |
| Opportunity Cost | $X | - | $X |
| **Total Costs** | **$X** | **$X** | **$X** |

### Benefits
| Benefit Category | One-Time | Recurring (Annual) | 5-Year Total |
|------------------|----------|-------------------|--------------|
| Revenue Increase | - | $X | $5X |
| Cost Savings | - | $X | $5X |
| Productivity Gain | - | $X | $5X |
| Risk Reduction | $X | $X | $X |
| **Total Benefits** | **$X** | **$X** | **$X** |

### Summary Metrics
| Metric | Value | Interpretation |
|--------|-------|----------------|
| Net Present Value (NPV) | $X | Positive = Good investment |
| Return on Investment (ROI) | X% | Higher = Better return |
| Payback Period | X months | Shorter = Faster return |
| Benefit-Cost Ratio | X:1 | > 1 = Benefits exceed costs |
```

### Simplified CBA for Quick Decisions
```markdown
## Quick Cost-Benefit: [Decision]

### Costs (Estimate)
- Direct costs: $[X]
- Time investment: [X] hours @ $[rate] = $[X]
- Hidden costs: $[X]
- **Total**: $[X]

### Benefits (Estimate)
- Primary benefit: $[X] or [qualitative]
- Secondary benefits: $[X] or [qualitative]
- **Total**: $[X]

### Verdict
- **Quantifiable ROI**: [X]% or [not quantifiable]
- **Qualitative assessment**: [Worth it / Not worth it / Uncertain]
- **Recommendation**: [Proceed / Do not proceed / Need more data]
```

### Intangible Benefits Framework
```markdown
### Intangible Benefits Assessment
| Benefit | Importance (1-5) | Confidence (1-5) | Weighted Value |
|---------|------------------|------------------|----------------|
| Brand perception | [X] | [X] | [calc] |
| Employee morale | [X] | [X] | [calc] |
| Customer satisfaction | [X] | [X] | [calc] |
| Strategic positioning | [X] | [X] | [calc] |
| Innovation capability | [X] | [X] | [calc] |

Note: Include intangible benefits in qualitative assessment,
not in financial calculations.
```

---

## 6. Pros/Cons Structuring

### Enhanced Pros/Cons Template
```markdown
## Pros/Cons Analysis: [Option]

### Pros
| Pro | Impact | Confidence | Weighted |
|-----|--------|------------|----------|
| [Pro 1] | [H/M/L] | [H/M/L] | [calc] |
| [Pro 2] | [H/M/L] | [H/M/L] | [calc] |
| [Pro 3] | [H/M/L] | [H/M/L] | [calc] |

### Cons
| Con | Impact | Confidence | Mitigable? |
|-----|--------|------------|------------|
| [Con 1] | [H/M/L] | [H/M/L] | [Y/N/Partial] |
| [Con 2] | [H/M/L] | [H/M/L] | [Y/N/Partial] |
| [Con 3] | [H/M/L] | [H/M/L] | [Y/N/Partial] |

### Summary
- **Pro count**: [X] ([Y] high-impact)
- **Con count**: [X] ([Y] high-impact, [Z] mitigable)
- **Net assessment**: [Favorable / Unfavorable / Neutral]
```

### Comparative Pros/Cons
```markdown
## Side-by-Side Comparison

### Option A: [Name]
| Pros | Cons |
|------|------|
| + [Pro 1] | - [Con 1] |
| + [Pro 2] | - [Con 2] |
| + [Pro 3] | - [Con 3] |

### Option B: [Name]
| Pros | Cons |
|------|------|
| + [Pro 1] | - [Con 1] |
| + [Pro 2] | - [Con 2] |
| + [Pro 3] | - [Con 3] |

### Differentiating Factors
- Option A is better when: [conditions]
- Option B is better when: [conditions]
```

### Structured Argumentation
```markdown
### Arguments For [Option]
1. **[Argument]**
   - Evidence: [Supporting data]
   - Counterargument: [Opposing view]
   - Rebuttal: [Why argument still holds]

2. **[Argument]**
   - Evidence: [Supporting data]
   - Counterargument: [Opposing view]
   - Rebuttal: [Why argument still holds]

### Arguments Against [Option]
1. **[Argument]**
   - Evidence: [Supporting data]
   - Counterargument: [Opposing view]
   - Rebuttal: [Why argument still holds]
```

---

## 7. Multi-Criteria Decision Analysis (MCDA)

### MCDA Process
```
MCDA WORKFLOW
├── 1. Define objectives
├── 2. Identify criteria (from objectives)
├── 3. Weight criteria (stakeholder input)
├── 4. Identify alternatives
├── 5. Score alternatives against criteria
├── 6. Calculate weighted scores
├── 7. Sensitivity analysis
└── 8. Document and recommend
```

### Complete MCDA Template
```markdown
## Multi-Criteria Decision Analysis: [Decision]

### 1. Objectives
| Objective | Description | Priority |
|-----------|-------------|----------|
| [Obj 1] | [What we want to achieve] | [Critical/Important/Nice] |
| [Obj 2] | [What we want to achieve] | [Critical/Important/Nice] |

### 2. Criteria Derived from Objectives
| Objective | Criteria | Measurable Indicator |
|-----------|----------|---------------------|
| [Obj 1] | [Criterion 1a] | [How to measure] |
| [Obj 1] | [Criterion 1b] | [How to measure] |
| [Obj 2] | [Criterion 2a] | [How to measure] |

### 3. Criteria Weighting
Method: [Pairwise comparison / Direct assignment / Swing weights]

| Criterion | Raw Weight | Normalized Weight |
|-----------|------------|-------------------|
| [Criterion 1] | [X] | [X%] |
| [Criterion 2] | [X] | [X%] |
| **Total** | | **100%** |

### 4. Alternatives
| Alternative | Description | Source |
|-------------|-------------|--------|
| [Alt A] | [Brief description] | [How identified] |
| [Alt B] | [Brief description] | [How identified] |
| [Alt C] | [Brief description] | [How identified] |

### 5. Performance Matrix
| Criterion | Weight | Alt A | Alt B | Alt C |
|-----------|--------|-------|-------|-------|
| [Crit 1] | [X%] | [score/value] | [score/value] | [score/value] |
| [Crit 2] | [X%] | [score/value] | [score/value] | [score/value] |
| [Crit 3] | [X%] | [score/value] | [score/value] | [score/value] |

### 6. Weighted Scores
| Alternative | Weighted Score | Rank |
|-------------|---------------|------|
| [Alt A] | [X.XX] | [1/2/3] |
| [Alt B] | [X.XX] | [1/2/3] |
| [Alt C] | [X.XX] | [1/2/3] |

### 7. Sensitivity Analysis
How do results change if weights shift?

| Scenario | Weight Change | New Winner | Stability |
|----------|--------------|------------|-----------|
| [Crit 1] +20% | [X% -> Y%] | [Alt X] | [Stable/Unstable] |
| [Crit 2] +20% | [X% -> Y%] | [Alt X] | [Stable/Unstable] |

### 8. Recommendation
**Recommended Alternative**: [Name]
**Confidence Level**: [High/Medium/Low]
**Key Factors**: [Top 2-3 deciding criteria]
```

### Pairwise Comparison Method
```markdown
### Pairwise Comparison for Weights

Compare each criterion pair: Which is more important?
Scale: 1 = Equal, 3 = Moderate, 5 = Strong, 7 = Very Strong, 9 = Extreme

|           | Crit A | Crit B | Crit C | Crit D |
|-----------|--------|--------|--------|--------|
| Crit A    | 1      | [1-9]  | [1-9]  | [1-9]  |
| Crit B    | [1/X]  | 1      | [1-9]  | [1-9]  |
| Crit C    | [1/X]  | [1/X]  | 1      | [1-9]  |
| Crit D    | [1/X]  | [1/X]  | [1/X]  | 1      |

Row Sum -> Normalize -> Weights
```

---

## 8. Stakeholder Alignment Methods

### Stakeholder Mapping for Decisions
```markdown
## Stakeholder Analysis: [Decision]

### Stakeholder Register
| Stakeholder | Role | Interest | Influence | Position |
|-------------|------|----------|-----------|----------|
| [Name/Group] | [Role] | [H/M/L] | [H/M/L] | [Supportive/Neutral/Resistant] |

### Influence-Interest Matrix
```
INFLUENCE
  High |  Keep       |  Manage    |
       |  Satisfied  |  Closely   |
       +-------------+------------+
  Low  |  Monitor    |  Keep      |
       |             |  Informed  |
       +-------------+------------+
            Low          High      INTEREST
```

### Stakeholder Concerns Matrix
| Stakeholder | Primary Concern | Option A Impact | Option B Impact |
|-------------|-----------------|-----------------|-----------------|
| [Stakeholder 1] | [Their priority] | [+/-/neutral] | [+/-/neutral] |
| [Stakeholder 2] | [Their priority] | [+/-/neutral] | [+/-/neutral] |
```

### Consensus Building Template
```markdown
## Consensus Building: [Decision]

### Current Positions
| Stakeholder | Preferred Option | Rationale | Flexibility |
|-------------|-----------------|-----------|-------------|
| [Name] | [Option X] | [Why] | [High/Med/Low] |

### Points of Agreement
- [Area where all agree]
- [Area where all agree]

### Points of Disagreement
| Issue | Position A | Position B | Path to Resolution |
|-------|------------|------------|-------------------|
| [Issue] | [View] | [View] | [Compromise/Vote/Defer] |

### Proposed Resolution Path
1. [Step to build consensus]
2. [Step to build consensus]
3. [Final decision mechanism]
```

### RACI for Decision Making
```markdown
### Decision RACI
| Activity | [Person 1] | [Person 2] | [Person 3] |
|----------|------------|------------|------------|
| Gather requirements | R | C | I |
| Evaluate options | R | A | C |
| Make recommendation | R | A | I |
| Approve decision | I | A | C |
| Implement decision | R | A | I |

R = Responsible, A = Accountable, C = Consulted, I = Informed
```

---

## 9. Recommendation Formatting

### Standard Recommendation Structure
```markdown
## Decision Recommendation: [Topic]

### Executive Summary
**Recommendation**: [Clear statement of recommended option]
**Confidence Level**: [High/Medium/Low] ([X]% confidence)
**Decision Type**: [Reversible/Partially Reversible/Irreversible]

### Context
[2-3 sentences on why this decision is needed now]

### Options Considered
1. **[Option A]**: [One-line description] - [Recommended/Not Recommended]
2. **[Option B]**: [One-line description] - [Recommended/Not Recommended]
3. **[Option C]**: [One-line description] - [Recommended/Not Recommended]

### Recommendation Rationale
**Primary Factors:**
1. [Most important reason with evidence]
2. [Second reason with evidence]
3. [Third reason with evidence]

**Trade-offs Accepted:**
- [What we are sacrificing by choosing this option]

**Risks Acknowledged:**
- [Key risk and mitigation plan]

### Implementation Considerations
| Aspect | Details |
|--------|---------|
| Timeline | [Expected duration] |
| Resources | [What's needed] |
| Dependencies | [What must happen first] |
| Success Metrics | [How to measure success] |

### Fallback Plan
If [recommended option] fails or circumstances change:
- **Trigger**: [What would cause us to reconsider]
- **Alternative**: [Backup option]
- **Switching cost**: [Effort to change course]

### Decision Required
- **Decision maker(s)**: [Who decides]
- **Deadline**: [When decision is needed]
- **Next steps if approved**: [Immediate actions]
```

### Confidence Level Guidelines
| Level | Criteria | Use When |
|-------|----------|----------|
| **High** (>80%) | Clear winner, robust analysis, low risk | Data is strong, stakeholders aligned |
| **Medium** (50-80%) | Leading option, some uncertainty | Trade-offs are close, some unknowns |
| **Low** (<50%) | Slight preference, significant uncertainty | Data is limited, high-stakes gamble |

### Recommendation Presentation Format
```markdown
## TL;DR
- **Choose**: [Option]
- **Because**: [One sentence]
- **Risk**: [One sentence]
- **Next step**: [One action]

---

[Full analysis below]
```

---

## 10. Decision Documentation Templates

### Decision Record Template (Lightweight)
```markdown
# Decision Record: [DR-XXXX]

**Date**: [YYYY-MM-DD]
**Decision Maker(s)**: [Names]
**Status**: [Proposed/Accepted/Superseded/Deprecated]

## Context
[What situation prompted this decision?]

## Decision
[What was decided?]

## Rationale
[Why was this option chosen over alternatives?]

## Consequences
[What are the implications of this decision?]

## Alternatives Considered
1. [Alternative 1] - Rejected because [reason]
2. [Alternative 2] - Rejected because [reason]
```

### Architecture Decision Record (ADR) Format
```markdown
# ADR-[NUMBER]: [Short Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## Context
[Describe the issue that motivates this decision]

## Decision
[Describe the change being proposed/decided]

## Consequences

### Positive
- [Benefit 1]
- [Benefit 2]

### Negative
- [Drawback 1]
- [Drawback 2]

### Neutral
- [Implication that is neither good nor bad]

## Alternatives Considered

### [Alternative 1]
- Pros: [list]
- Cons: [list]
- Reason rejected: [why]

### [Alternative 2]
- Pros: [list]
- Cons: [list]
- Reason rejected: [why]

## References
- [Link to relevant documentation]
- [Link to discussion thread]
```

### Decision Log Template
```markdown
## Decision Log: [Project/Team]

| ID | Date | Decision | Owner | Status | Review Date |
|----|------|----------|-------|--------|-------------|
| D001 | YYYY-MM-DD | [Brief description] | [Name] | Active | YYYY-MM-DD |
| D002 | YYYY-MM-DD | [Brief description] | [Name] | Active | YYYY-MM-DD |
```

### Post-Decision Review Template
```markdown
# Post-Decision Review: [Decision Title]

**Original Decision Date**: [YYYY-MM-DD]
**Review Date**: [YYYY-MM-DD]
**Reviewer**: [Name]

## Original Decision
[What was decided]

## Expected Outcomes
- [What we expected to happen]

## Actual Outcomes
- [What actually happened]

## Variance Analysis
| Expected | Actual | Variance | Explanation |
|----------|--------|----------|-------------|
| [X] | [Y] | [+/-Z] | [Why different] |

## Lessons Learned
1. [What we learned]
2. [What we would do differently]

## Decision Validation
- **Outcome**: [Successful/Partially Successful/Unsuccessful]
- **Would we make same decision again?**: [Yes/No/Modified]
- **Recommended changes**: [None/Adjustments needed]
```

---

## Quick Reference: Framework Selection Guide

```
START
  │
  ├─ Is it a simple yes/no?
  │   └─ YES → Use Pros/Cons Analysis
  │
  ├─ Are there 3+ options to compare?
  │   └─ YES → Use Weighted Scoring Matrix
  │
  ├─ Is it high-stakes or complex?
  │   └─ YES → Use full MCDA
  │
  ├─ Is budget/ROI the primary concern?
  │   └─ YES → Use Cost-Benefit Analysis
  │
  ├─ Is there significant uncertainty?
  │   └─ YES → Add Risk Assessment layer
  │
  └─ Do multiple stakeholders need to agree?
      └─ YES → Add Stakeholder Alignment process
```

---

## Quality Checklist

- [ ] Decision statement is clear and specific
- [ ] All viable options have been identified
- [ ] Evaluation criteria are weighted appropriately
- [ ] Scores are based on evidence, not assumptions
- [ ] Trade-offs are explicitly acknowledged
- [ ] Risks are identified and assessed
- [ ] Costs and benefits are quantified where possible
- [ ] Stakeholder concerns are addressed
- [ ] Recommendation includes confidence level
- [ ] Fallback option is identified
- [ ] Decision is documented for future reference
- [ ] Review triggers are defined
