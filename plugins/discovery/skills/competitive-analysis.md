---
skill: competitive-analysis
version: "1.0.0"
description: "Systematic competitor analysis for design and strategy insights"
used-by:
  - "@competitor-analyst"
  - "@market-researcher"
  - "@discovery-controller"
---

# Competitive Analysis

## Overview

Framework for analyzing competitor websites, products, and strategies to inform design decisions and identify market opportunities.

---

## Phase 1: Competitor Identification

### Competitor Categories
```
DIRECT COMPETITORS (Same product, same market)
├── Primary: Top 3-5 direct competitors
└── Secondary: Emerging or niche players

INDIRECT COMPETITORS (Different product, same need)
├── Alternative solutions
└── Adjacent market players

ASPIRATIONAL (Best-in-class, any industry)
├── UX/UI leaders
└── Feature innovators
```

### Selection Criteria
| Factor | Weight | Evaluation |
|--------|--------|------------|
| Market overlap | High | Same target audience? |
| Feature parity | High | Solving same problems? |
| Market position | Medium | Leader, challenger, niche? |
| Design quality | Medium | Worth learning from? |

---

## Phase 2: Analysis Framework

### Site Audit Template

For each competitor, capture:

```markdown
## [Competitor Name]
**URL**:
**Category**: Direct / Indirect / Aspirational

### First Impressions (30 seconds)
- Value proposition clarity: /5
- Visual design quality: /5
- Trust signals present: Y/N
- Primary CTA: [what is it?]

### Navigation & Information Architecture
- Main nav items: [list]
- Depth of hierarchy: [shallow/medium/deep]
- Search functionality: Y/N
- Mobile navigation: [pattern used]

### Content Strategy
- Tone of voice: [formal/casual/technical]
- Content types: [blog/case studies/videos/etc]
- Update frequency: [active/stale]
- SEO focus keywords: [inferred topics]

### Key Features
1. [Feature] - [how it works]
2. [Feature] - [how it works]

### Strengths
- [Strength 1]
- [Strength 2]

### Weaknesses
- [Weakness 1]
- [Weakness 2]

### Unique Elements
- [Something they do that others don't]
```

---

## Phase 3: Comparative Analysis

### Feature Matrix Template
```
| Feature          | Us | Comp A | Comp B | Comp C |
|------------------|:--:|:------:|:------:|:------:|
| Feature 1        | -  | ✓      | ✓      | -      |
| Feature 2        | -  | ✓      | -      | ✓      |
| Feature 3        | -  | -      | ✓      | ✓      |
```

### Positioning Map
Plot competitors on 2x2 matrix:
```
                    HIGH PRICE
                        │
    Premium Niche       │       Premium Leader
                        │
    ────────────────────┼────────────────────
    LOW FEATURES        │       HIGH FEATURES
                        │
    Budget Option       │       Value Leader
                        │
                    LOW PRICE
```

---

## Phase 4: Pattern Extraction

### Design Patterns to Capture
- **Hero sections**: Layout, messaging, imagery
- **Navigation**: Patterns, mega menus, mobile
- **Social proof**: Testimonials, logos, stats
- **CTAs**: Placement, copy, styling
- **Forms**: Fields, validation, progress
- **Pricing pages**: Structure, comparison tables

### Innovation Identification
```
STANDARD PATTERNS (Industry norms)
└── [Pattern everyone uses]

DIFFERENTIATORS (Unique approaches)
└── [What one competitor does differently]

GAPS (Nobody does this)
└── [Opportunity areas]
```

---

## Phase 5: Strategic Synthesis

### Opportunity Framework
```
1. TABLE STAKES: Must have to compete
   └── [Features/elements everyone has]

2. DIFFERENTIATORS: Ways to stand out
   └── [Unique approaches we could take]

3. FIRST MOVER: Untapped opportunities
   └── [Things nobody is doing]
```

### Output Template
```markdown
## Competitive Analysis Summary

### Market Landscape
[2-3 sentence overview of competitive environment]

### Key Competitors
| Competitor | Positioning | Main Strength | Main Weakness |
|------------|-------------|---------------|---------------|
| A          | Premium     | UX quality    | High price    |
| B          | Value       | Features      | Dated design  |

### Critical Insights
1. [Insight with strategic implication]
2. [Insight with strategic implication]

### Recommended Approach
[How findings should influence our strategy]
```

---

## Common Pitfalls

| Pitfall | Prevention |
|---------|------------|
| Copy competitors blindly | Understand WHY they made choices |
| Analyze too many | Focus on 5-7 most relevant |
| Surface-level review | Dig into user flows, not just homepages |
| Ignore indirect competitors | Include alternative solutions |
| Static analysis | Note what's working, not just what exists |

---

## Quality Checklist

- [ ] 3-5 direct competitors analyzed
- [ ] 1-2 aspirational examples included
- [ ] Screenshots captured for key patterns
- [ ] Feature matrix completed
- [ ] Opportunities identified
- [ ] Strategic recommendations provided
