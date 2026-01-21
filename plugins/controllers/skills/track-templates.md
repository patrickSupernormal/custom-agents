---
skill: track-templates
version: "1.0.0"
description: "Component-based track templates for multi-track orchestration - decompose by WHAT is needed, not WHO builds it"
used-by:
  - orchestrator
  - main-thread
---

# Track Templates Skill

## Core Principle

**Decomposition is based on TASK COMPONENTS, not agent specialization.**

Wrong approach: `1 page = 1 @page-builder = 1 track`

Correct approach: Analyze what the task REQUIRES, create one track per component, then assign the appropriate specialist.

## Component Track Types

| Track Type | Purpose | Typical Specialists |
|------------|---------|---------------------|
| `research` | Information gathering before implementation | @web-researcher, Explore, @codebase-explorer |
| `design-tokens` | Design system, colors, typography, spacing | @css-architect, @design-spec-foundation |
| `layout-structure` | HTML structure, grid systems, responsive layout | @react-engineer, @css-architect |
| `components` | Reusable UI components | @react-engineer, @ui-engineer |
| `animations` | Motion, scroll effects, transitions | @animation-engineer |
| `forms` | Form logic, validation, submission handling | @react-engineer |
| `api-integration` | API endpoints, data fetching, handlers | @api-architect, @node-engineer |
| `database` | Schema design, migrations, queries | @database-architect |
| `auth` | Authentication flows, protected routes | @auth-engineer |
| `state-management` | Client state, data flow, caching | @react-engineer |
| `content` | Copy, content structure, CMS setup | @copywriter, @content-strategist, @cms-architect |
| `quality` | Testing, accessibility, performance, security | @test-engineer, @accessibility-engineer, etc. |

## Domain-Specific Decomposition Templates

### DEVELOPMENT Decomposition

For implementation requests, analyze what building REQUIRES:

```markdown
## Decomposition Checklist

- [ ] Design tokens/styling needed?
- [ ] Layout/structure work?
- [ ] Components to build?
- [ ] Animations/interactions?
- [ ] Forms with validation?
- [ ] API endpoints?
- [ ] Database schema?
- [ ] Auth flows?
- [ ] State management?
- [ ] Content/copy?
```

**Example:** "Build contact page with form"
```
Tracks:
├── layout-structure → @react-engineer (page layout, responsive grid)
├── components → @react-engineer (form inputs, buttons)
├── forms → @react-engineer (validation logic, submission)
├── api-integration → @api-architect (form submission endpoint)
├── animations → @animation-engineer (form transitions, feedback)
└── styling → @css-architect (form styles, states)
```

### RESEARCH Decomposition

For understanding/analysis requests:

```markdown
## Decomposition Checklist

- [ ] Web/external sources needed?
- [ ] Codebase exploration needed?
- [ ] Documentation review?
- [ ] Competitive analysis?
- [ ] Technical evaluation?
- [ ] User/market research?
```

**Example:** "Research authentication options for our app"
```
Tracks:
├── web-research → @web-researcher (auth providers, best practices)
├── codebase-analysis → @codebase-explorer (current auth patterns)
├── competitive-analysis → @competitor-analyst (competitor auth implementations)
├── tech-evaluation → @technology-evaluator (compare Auth.js vs Clerk vs custom)
└── security-review → @security-engineer (security implications)
```

### DISCOVERY Decomposition

For project kickoff/understanding:

```markdown
## Decomposition Checklist

- [ ] Brand/visual identity analysis?
- [ ] Content inventory?
- [ ] Competitor landscape?
- [ ] Technical constraints?
- [ ] User needs?
- [ ] Business goals?
```

**Example:** "Run discovery for new client project"
```
Tracks:
├── site-audit → @site-scraper (existing site analysis)
├── competitor-research → @competitor-analyst (market positioning)
├── content-analysis → @content-strategist (content needs)
├── technical-assessment → @technology-evaluator (tech stack options)
├── brand-analysis → @brand-strategist (brand positioning)
└── kickoff-synthesis → @kickoff-processor (if transcript provided)
```

### DESIGN Decomposition

For design/specification requests:

```markdown
## Decomposition Checklist

- [ ] Brand/identity work?
- [ ] Design tokens?
- [ ] Component patterns?
- [ ] Page layouts?
- [ ] Motion language?
- [ ] Content structure?
```

**Example:** "Create design system for new project"
```
Tracks:
├── brand-direction → @design-director (aesthetic direction)
├── token-system → @design-spec-foundation (colors, typography, spacing)
├── component-specs → @ui-engineer (component patterns)
├── motion-system → @animation-engineer (motion principles)
├── content-framework → @content-strategist (content structure)
└── wireframes → @wireframe-spec (layout patterns)
```

### STRATEGY Decomposition

For planning/strategy requests:

```markdown
## Decomposition Checklist

- [ ] Market positioning needed?
- [ ] Content planning?
- [ ] Technical approach?
- [ ] Project scope?
- [ ] Information architecture?
- [ ] SEO considerations?
```

**Example:** "Develop content strategy for marketing site"
```
Tracks:
├── audience-research → @web-researcher (target audience insights)
├── competitor-content → @competitor-analyst (content gaps/opportunities)
├── content-planning → @content-strategist (content pillars, calendar)
├── site-architecture → @information-architect (site structure)
├── seo-strategy → @seo-optimizer (keyword strategy)
└── messaging-framework → @brand-strategist (voice, tone, messaging)
```

### QA/QUALITY Decomposition

For quality assurance requests:

```markdown
## Decomposition Checklist

- [ ] Unit tests needed?
- [ ] Integration tests?
- [ ] Accessibility audit?
- [ ] Performance audit?
- [ ] Security audit?
- [ ] Code review?
```

**Example:** "Run full QA on the new feature"
```
Tracks:
├── unit-tests → @test-engineer
├── integration-tests → @test-engineer
├── accessibility-audit → @accessibility-engineer
├── performance-audit → @performance-engineer
├── security-audit → @security-engineer
└── code-review → @qa-auditor
```

### LEARNING Decomposition

For educational/tutorial requests:

```markdown
## Decomposition Checklist

- [ ] Concept explanation needed?
- [ ] Code examples?
- [ ] Hands-on tutorial?
- [ ] Documentation review?
- [ ] Best practices?
- [ ] Common pitfalls?
```

**Example:** "Learn how to implement OAuth in Next.js"
```
Tracks:
├── concept-research → @web-researcher (OAuth fundamentals)
├── docs-synthesis → @documentation-synthesizer (Next.js auth docs)
├── codebase-patterns → @codebase-explorer (existing OAuth implementations)
├── tutorial-creation → @tutorial-engineer (step-by-step guide)
└── best-practices → @security-engineer (security considerations)
```

## Track Dependency Patterns

### Independent Tracks (can parallelize)

```
[Track A] ─────────────────►
[Track B] ─────────────────►
[Track C] ─────────────────►
```
All run simultaneously, no dependencies.

### Sequential Tracks (must serialize)

```
[Track A] ──► [Track B] ──► [Track C]
```
Each depends on previous output.

### Mixed Dependencies

```
[Track A: research] ─────────┐
                              ├──► [Track D: implementation]
[Track B: design-tokens] ────┘

[Track C: content] ──────────────► [Track E: integration]
```

### Common Dependency Patterns

| Pattern | Dependencies |
|---------|-------------|
| Foundation → Build | design-tokens BLOCKS components, layout |
| Research → Implement | research BLOCKS implementation tracks |
| Schema → API | database BLOCKS api-integration |
| Build → Test | components BLOCKS quality |
| Content → Design | content-strategy BLOCKS design work |

## Decomposition Process

### Step 1: Identify Request Domain

What type of request is this?
- Development (building)
- Research (understanding)
- Discovery (project kickoff)
- Design (specification)
- Strategy (planning)
- Quality (auditing)
- Learning (education)

### Step 2: Run Domain Checklist

Use the appropriate checklist above to identify all required components.

### Step 3: Create Track List

For each checked item, create a track with:
- Track name (component type)
- Purpose (what it delivers)
- Specialist (who executes)

### Step 4: Map Dependencies

- Which tracks can run in parallel?
- Which tracks block others?
- What's the critical path?

### Step 5: Output Track Plan

```markdown
## Track Decomposition

**Request:** [original request]
**Domain:** [identified domain]

### Tracks
| # | Track | Purpose | Specialist | Depends On |
|---|-------|---------|------------|------------|
| 1 | [name] | [purpose] | @agent | - |
| 2 | [name] | [purpose] | @agent | Track 1 |
| 3 | [name] | [purpose] | @agent | - |

### Execution Waves
- Wave 1 (parallel): Track 1, Track 3
- Wave 2 (after Wave 1): Track 2, Track 4
```

## Anti-Patterns to Avoid

### Wrong: Agent-Based Decomposition
```
Track 1: @react-engineer
Track 2: @css-architect
Track 3: @animation-engineer
```
This doesn't capture WHAT needs building.

### Right: Component-Based Decomposition
```
Track 1: layout-structure → @react-engineer
Track 2: styling-system → @css-architect
Track 3: animations → @animation-engineer
```
This captures the component AND assigns the specialist.

### Wrong: Page-Based Decomposition
```
Track 1: Build homepage
Track 2: Build about page
Track 3: Build contact page
```
Misses shared components and creates duplication.

### Right: Component-Based for Multi-Page
```
Track 1: design-tokens (shared) → @css-architect
Track 2: layout-structure (shared) → @react-engineer
Track 3: homepage-hero → @animation-engineer
Track 4: homepage-newsletter → @react-engineer + @api-architect
Track 5: about-team-grid → @react-engineer
Track 6: contact-form → @react-engineer + @api-architect
```
Identifies shared vs unique, avoids duplication.

## Quality Checklist

- [ ] Identified correct domain
- [ ] Ran appropriate checklist
- [ ] Each track has clear component purpose
- [ ] Specialists assigned to tracks (not tracks to specialists)
- [ ] Dependencies mapped
- [ ] Shared components identified (for multi-page)
- [ ] No agent-based or page-based decomposition
