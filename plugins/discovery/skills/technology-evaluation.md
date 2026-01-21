---
skill: technology-evaluation
version: "1.0.0"
description: "Framework for evaluating tools, frameworks, and services"
used-by:
  - "@tech-stack-advisor"
  - "@web-researcher"
  - "@discovery-controller"
---

# Technology Evaluation

## Overview

Structured approach to evaluating and recommending technologies, frameworks, libraries, and services based on project requirements and constraints.

---

## Phase 1: Requirements Gathering

### Requirement Categories
```
FUNCTIONAL REQUIREMENTS
├── What must it do?
├── What integrations needed?
└── What scale must it handle?

NON-FUNCTIONAL REQUIREMENTS
├── Performance expectations
├── Security requirements
└── Compliance needs

CONSTRAINTS
├── Budget (one-time and recurring)
├── Timeline
├── Team expertise
└── Existing infrastructure
```

### Weighted Criteria Template
| Criterion | Weight | Description |
|-----------|--------|-------------|
| Functionality | [1-5] | Meets feature requirements |
| Performance | [1-5] | Speed, scalability |
| Developer Experience | [1-5] | Learning curve, docs |
| Community/Support | [1-5] | Active development, help |
| Cost | [1-5] | Total cost of ownership |
| Security | [1-5] | Vulnerabilities, compliance |
| Longevity | [1-5] | Future viability |

---

## Phase 2: Candidate Identification

### Discovery Strategy
1. **Official sources**: Documentation, official comparisons
2. **Community consensus**: Stack Overflow, Reddit, HN
3. **Expert recommendations**: Tech blogs, conference talks
4. **Similar projects**: What do peers use?

### Candidate Shortlist
```markdown
## Candidates for [Technology Need]

### Tier 1: Strong Contenders (Evaluate Deeply)
1. [Technology A] - [One-line reason]
2. [Technology B] - [One-line reason]
3. [Technology C] - [One-line reason]

### Tier 2: Worth Considering (Evaluate if Tier 1 fails)
4. [Technology D] - [One-line reason]

### Ruled Out (Document why)
- [Technology X] - [Disqualifying reason]
```

---

## Phase 3: Deep Evaluation

### Evaluation Template (Per Candidate)
```markdown
## [Technology Name]

### Overview
- **Type**: [Framework/Library/Service/Platform]
- **License**: [MIT/Apache/Proprietary/etc]
- **Pricing**: [Free/Freemium/Paid - details]
- **Maturity**: [Beta/Stable/Mature/Legacy]

### Strengths
1. [Strength with evidence]
2. [Strength with evidence]
3. [Strength with evidence]

### Weaknesses
1. [Weakness with evidence]
2. [Weakness with evidence]

### Fit Assessment
| Criterion | Score (1-5) | Notes |
|-----------|-------------|-------|
| Functionality | | |
| Performance | | |
| Developer Experience | | |
| Community/Support | | |
| Cost | | |
| Security | | |
| Longevity | | |
| **Weighted Total** | | |

### Risk Factors
- [Potential risk and mitigation]

### Team Readiness
- Current expertise: [None/Some/Strong]
- Learning investment: [Low/Medium/High]
```

---

## Phase 4: Comparison Matrix

### Side-by-Side Comparison
```
| Factor            | Option A | Option B | Option C |
|-------------------|----------|----------|----------|
| License           |          |          |          |
| Cost (Year 1)     |          |          |          |
| Cost (Ongoing)    |          |          |          |
| Learning Curve    |          |          |          |
| Performance       |          |          |          |
| Community Size    |          |          |          |
| Last Release      |          |          |          |
| GitHub Stars      |          |          |          |
| Known Issues      |          |          |          |
| Migration Path    |          |          |          |
| **Weighted Score**|          |          |          |
```

### Trade-off Analysis
```
OPTION A: Best for [use case]
├── Choose if: [condition]
└── Avoid if: [condition]

OPTION B: Best for [use case]
├── Choose if: [condition]
└── Avoid if: [condition]
```

---

## Phase 5: Recommendation

### Decision Framework
```
1. ELIMINATE: Remove options that fail must-have requirements
2. RANK: Score remaining options on weighted criteria
3. VALIDATE: Check top choice against constraints
4. RISK ASSESS: Consider failure scenarios
5. RECOMMEND: Provide clear recommendation with rationale
```

### Recommendation Template
```markdown
## Technology Recommendation: [Category]

### Recommendation: [Technology Name]
**Confidence Level**: High/Medium/Low

### Rationale
[2-3 sentences explaining why this is the best choice]

### Key Deciding Factors
1. [Factor and why it mattered]
2. [Factor and why it mattered]

### Trade-offs Accepted
- [What we're giving up by choosing this]

### Implementation Considerations
- [Setup complexity]
- [Learning requirements]
- [Integration points]

### Fallback Option
If [Technology Name] doesn't work out, consider [Alternative] because [reason].

### Next Steps
1. [Immediate action]
2. [Short-term action]
```

---

## Common Pitfalls

| Pitfall | Prevention |
|---------|------------|
| Hype-driven selection | Focus on requirements, not buzz |
| Ignoring team skills | Factor in learning investment |
| Underestimating costs | Include hidden and ongoing costs |
| Over-engineering | Match complexity to actual needs |
| Ignoring exit strategy | Consider lock-in and migration |
| Recency bias | Proven tech often beats new |

---

## Red Flags to Watch

- No updates in 12+ months
- Declining GitHub activity
- Few Stack Overflow answers
- Company/maintainer instability
- Unclear licensing
- Poor documentation
- No migration path

---

## Quality Checklist

- [ ] Requirements clearly defined and weighted
- [ ] 3+ candidates evaluated
- [ ] Objective criteria used
- [ ] Costs fully calculated (TCO)
- [ ] Team capability considered
- [ ] Risks identified
- [ ] Clear recommendation provided
- [ ] Fallback option identified
