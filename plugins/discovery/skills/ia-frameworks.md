---
skill: ia-frameworks
version: "1.0.0"
description: "Information architecture frameworks for site structure, navigation, and user flow optimization"
used-by:
  - "@information-architect"
---

# Information Architecture Frameworks

## Overview

Comprehensive frameworks for creating intuitive, scalable website architectures. Covers site structure methodologies, navigation patterns, content taxonomy, user flows, and documentation standards.

---

## 1. Site Structure Methodologies

### Hierarchical Structure (Tree Model)
Best for: Content-heavy sites, corporate websites, documentation

```
Homepage (L0)
├── Category A (L1)
│   ├── Subcategory A1 (L2)
│   │   ├── Page A1a (L3)
│   │   └── Page A1b (L3)
│   └── Subcategory A2 (L2)
├── Category B (L1)
│   └── Subcategory B1 (L2)
└── Category C (L1)
```

**Rules**:
- Maximum 3-4 levels deep
- 7 +/- 2 items per level (Miller's Law)
- Clear parent-child relationships

### Flat Structure
Best for: Small sites, single-product apps, portfolios

```
Homepage
├── About
├── Services
├── Portfolio
├── Blog
└── Contact
```

**Rules**:
- All pages 1 click from home
- Maximum 10-12 pages
- Heavy cross-linking

### Hub and Spoke Structure
Best for: E-commerce, educational platforms, service sites

```
        ┌──────────┐
   ┌────┤   Hub    ├────┐
   │    │  (Home)  │    │
   │    └────┬─────┘    │
   │         │          │
   ▼         ▼          ▼
[Spoke 1] [Spoke 2] [Spoke 3]
   │         │          │
   └─────────┴──────────┘
        (Cross-links)
```

**Rules**:
- Hub contains navigation to all spokes
- Spokes link back to hub
- Spokes can cross-link to related spokes

### Matrix Structure
Best for: Research sites, data-heavy applications, filter-based browsing

```
           │ Topic A │ Topic B │ Topic C │
───────────┼─────────┼─────────┼─────────┤
Audience 1 │   X     │    X    │         │
Audience 2 │         │    X    │    X    │
Audience 3 │   X     │         │    X    │
```

**Rules**:
- Multiple entry points to same content
- Faceted navigation required
- Content tagged across dimensions

### Choosing a Structure

| Site Type | Recommended Structure | Reasoning |
|-----------|----------------------|-----------|
| Corporate | Hierarchical | Clear departments/services |
| E-commerce | Hub-and-Spoke | Product categories as spokes |
| Blog | Flat + Tags | Chronological + topical access |
| SaaS Product | Hierarchical + Flat | Features grouped, support flat |
| Portfolio | Flat | Quick access to work samples |
| Knowledge Base | Matrix | Multiple access dimensions |

---

## 2. Navigation Design Patterns

### Primary Navigation Patterns

**Horizontal Navigation Bar**
```
┌──────────────────────────────────────────────────────────────┐
│ [Logo]    Home   Products   Solutions   About   Contact  [CTA]│
└──────────────────────────────────────────────────────────────┘
```
Best for: 4-7 main items, desktop-first sites

**Mega Menu**
```
┌──────────────────────────────────────────────────────────────┐
│ [Logo]    Products ▼   Solutions   Resources   About         │
├──────────────────────────────────────────────────────────────┤
│ ┌────────────┬────────────┬────────────┬──────────────────┐ │
│ │ Category 1 │ Category 2 │ Category 3 │ Featured         │ │
│ │ - Item     │ - Item     │ - Item     │ [Image]          │ │
│ │ - Item     │ - Item     │ - Item     │ Promo content    │ │
│ │ - Item     │ - Item     │ - Item     │ [CTA Button]     │ │
│ └────────────┴────────────┴────────────┴──────────────────┘ │
└──────────────────────────────────────────────────────────────┘
```
Best for: Large sites, e-commerce, 20+ navigation items

**Vertical Sidebar Navigation**
```
┌─────────────────┬────────────────────────────────────────────┐
│ [Logo]          │                                            │
├─────────────────┤                                            │
│ Dashboard       │                                            │
│ > Projects      │              Content Area                  │
│   Analytics     │                                            │
│   Settings      │                                            │
│ ─────────────── │                                            │
│ Team            │                                            │
│ Integrations    │                                            │
└─────────────────┴────────────────────────────────────────────┘
```
Best for: Applications, dashboards, tools with deep hierarchy

### Secondary Navigation Patterns

**Tabs**
```
┌────────┬────────┬────────┬────────┐
│ Tab 1  │ Tab 2  │ Tab 3  │ Tab 4  │ ← Active tab highlighted
├────────┴────────┴────────┴────────┴─────────────────────────┐
│                                                              │
│                    Tab Content Area                          │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```
Use for: Related content views, settings sections, product details

**Pills/Segments**
```
┌───────────────────────────────────────────┐
│ [ All ] [ Active ] [ Completed ] [ Draft ]│
└───────────────────────────────────────────┘
```
Use for: Filtering content, view toggles, status-based navigation

**Stepped Navigation**
```
Step 1          Step 2          Step 3          Step 4
[====]──────────[====]──────────[    ]──────────[    ]
Account         Shipping        Payment         Review
```
Use for: Multi-step forms, onboarding, checkout flows

### Mobile Navigation Patterns

**Hamburger Menu**
```
┌─────────────────────────────────────┐
│ [===] [Logo]              [Search] │
└─────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│ Home                              > │
│ Products                          > │
│ Solutions                         > │
│ About                             > │
│ Contact                           > │
├─────────────────────────────────────┤
│ [Login]         [Get Started]      │
└─────────────────────────────────────┘
```

**Bottom Tab Bar**
```
┌─────────────────────────────────────┐
│                                     │
│           Content Area              │
│                                     │
├─────────────────────────────────────┤
│  [Home] [Search] [Add] [Inbox] [Me] │
└─────────────────────────────────────┘
```
Best for: Apps, mobile-first sites, frequent navigation

**Priority+ Navigation**
```
Desktop: [Home] [Products] [Solutions] [About] [Contact] [Support]

Mobile:  [Home] [Products] [Solutions] [...]
                                        │
                                        ▼
                              [About] [Contact] [Support]
```

### Navigation Design Rules

| Rule | Description |
|------|-------------|
| 7 +/- 2 | Maximum items in primary navigation |
| 3-click rule | Most content reachable in 3 clicks |
| Visible affordance | Make interactive elements obvious |
| Consistent placement | Same location across all pages |
| Current state | Show active/current page clearly |
| Descriptive labels | Use user language, not jargon |

---

## 3. Content Taxonomy Creation

### Taxonomy Types

**Flat Taxonomy**
```
Tags: design, development, marketing, sales, support
```
Use for: Blogs, articles, simple filtering

**Hierarchical Taxonomy**
```
Products
├── Electronics
│   ├── Phones
│   │   ├── Smartphones
│   │   └── Feature Phones
│   └── Computers
│       ├── Laptops
│       └── Desktops
└── Clothing
    ├── Men's
    └── Women's
```
Use for: E-commerce, documentation, structured content

**Faceted Taxonomy**
```
CONTENT TYPE           TOPIC              AUDIENCE
[ ] Article            [ ] Design         [ ] Beginner
[ ] Video              [ ] Development    [ ] Intermediate
[ ] Tutorial           [ ] Business       [ ] Advanced
[ ] Case Study         [ ] Marketing      [ ] Expert
```
Use for: Resource libraries, product catalogs, search-heavy sites

### Taxonomy Creation Process

**Step 1: Content Inventory**
```markdown
| Content ID | Title | Current Category | Content Type | Topics | Audience |
|------------|-------|------------------|--------------|--------|----------|
| C001 | Getting Started | Docs | Tutorial | Onboarding | Beginner |
| C002 | API Reference | Docs | Reference | API, Technical | Advanced |
```

**Step 2: Affinity Mapping**
```
Group 1: Learning Resources
├── Tutorials
├── Guides
├── Videos
└── Webinars

Group 2: Reference Materials
├── API Docs
├── Specifications
└── Changelogs

Group 3: Community
├── Case Studies
├── Community Posts
└── User Stories
```

**Step 3: Define Vocabulary**
```yaml
taxonomy:
  content_type:
    - label: "Tutorial"
      description: "Step-by-step learning content"
      slug: "tutorial"
    - label: "Reference"
      description: "Technical documentation"
      slug: "reference"

  topic:
    - label: "Getting Started"
      slug: "getting-started"
      children:
        - label: "Installation"
          slug: "installation"
        - label: "Configuration"
          slug: "configuration"
```

**Step 4: Governance Rules**
```markdown
## Taxonomy Governance

### Adding New Terms
1. Check if existing term covers the concept
2. Propose new term with definition and use cases
3. Review by content team
4. Add to controlled vocabulary

### Term Format
- Use sentence case: "Getting started" not "Getting Started"
- Use nouns, not verbs: "Installation" not "Installing"
- Avoid acronyms unless universal: "API" is OK, "WCAG" needs full form

### Hierarchy Rules
- Maximum 3 levels deep
- Parent terms should not be used on content (use children)
- Cross-reference related terms in different branches
```

---

## 4. User Flow Mapping

### Flow Notation System

```
[Rectangle] = Page/Screen
(Rounded)   = Action/Decision
<Diamond>   = Conditional/Branch
[  //  ]    = External System
───────>    = Flow Direction
- - - - >   = Optional/Alternative Path
```

### Common Flow Patterns

**Linear Flow**
```
[Landing] ──> [Signup] ──> [Onboarding] ──> [Dashboard]
```

**Branching Flow**
```
                    ┌──> [Free Trial] ──> [Dashboard]
[Pricing] ──> <Buy?>│
                    └──> [Checkout] ──> [Payment] ──> [Confirmation]
```

**Loop Flow**
```
[Product List] ──> [Product Detail] ──> (Add to Cart) ──┐
       ^                                                 │
       └─────────────── (Continue Shopping) ────────────┘
```

### User Flow Documentation Template

```markdown
## Flow: [Flow Name]

### Overview
- **Trigger**: What initiates this flow
- **Goal**: What user wants to accomplish
- **Success Criteria**: How we know flow succeeded

### Entry Points
1. Homepage CTA
2. Navigation menu
3. Direct URL

### Flow Diagram
[Insert visual flow diagram]

### Screen-by-Screen

#### Screen 1: [Name]
- **URL**: /page-path
- **Purpose**: What this screen accomplishes
- **Key Elements**:
  - Primary CTA: [Button text]
  - Form fields: [List fields]
  - Information displayed: [Key content]
- **Next Actions**:
  - Primary: [Where main CTA leads]
  - Secondary: [Alternative paths]
- **Edge Cases**:
  - Error state: [What happens on error]
  - Empty state: [What shows with no data]

### Exit Points
- **Success**: [Confirmation page, dashboard]
- **Abandonment**: [Where users might leave]
- **Error**: [Error page, retry option]

### Metrics
- Completion rate target: X%
- Time to complete target: X minutes
- Key drop-off points to monitor: [List]
```

### Critical Flows to Map

| Flow Type | Pages Involved | Priority |
|-----------|---------------|----------|
| Sign Up / Registration | 3-5 screens | Critical |
| Login / Authentication | 2-3 screens | Critical |
| Core Task Completion | 4-8 screens | Critical |
| Checkout / Purchase | 4-6 screens | Critical |
| Onboarding | 3-7 screens | High |
| Account Settings | 3-5 screens | Medium |
| Help / Support | 2-4 screens | Medium |
| Search / Browse | 2-3 screens | High |

---

## 5. Sitemap Documentation Formats

### Text-Based Sitemap

```markdown
# Site Map: [Project Name]
Version: 1.0 | Date: YYYY-MM-DD

## Level 0: Home
- / (Homepage)

## Level 1: Primary Sections
- /products (Products Landing)
- /solutions (Solutions Landing)
- /resources (Resources Hub)
- /company (Company Info)

## Level 2: Sub-Sections

### Products
- /products/product-a (Product A)
- /products/product-b (Product B)
- /products/pricing (Pricing)

### Solutions
- /solutions/enterprise (Enterprise)
- /solutions/small-business (Small Business)
- /solutions/by-industry (By Industry)
  - /solutions/by-industry/healthcare
  - /solutions/by-industry/finance
  - /solutions/by-industry/retail
```

### Visual Sitemap (ASCII)

```
                           ┌───────────────┐
                           │   HOMEPAGE    │
                           │      /        │
                           └───────┬───────┘
            ┌──────────────┬───────┴───────┬──────────────┐
            ▼              ▼               ▼              ▼
     ┌──────────┐   ┌──────────┐    ┌──────────┐   ┌──────────┐
     │ Products │   │Solutions │    │Resources │   │ Company  │
     │/products │   │/solutions│    │/resources│   │ /company │
     └────┬─────┘   └────┬─────┘    └────┬─────┘   └────┬─────┘
          │              │               │              │
    ┌─────┼─────┐   ┌────┼────┐     ┌────┼────┐    ┌────┼────┐
    ▼     ▼     ▼   ▼    ▼    ▼     ▼    ▼    ▼    ▼    ▼    ▼
  [A]   [B]  [$$]  [E]  [S]  [I]   [B]  [D]  [C]  [A]  [T]  [C]
```

### Annotated Sitemap Table

```markdown
| Page | URL | Template | Priority | Status | Notes |
|------|-----|----------|----------|--------|-------|
| Homepage | / | homepage | P1 | Design | Above fold hero |
| Products | /products | listing | P1 | Dev | 12 products |
| Product A | /products/a | product-detail | P1 | Design | Video needed |
| Pricing | /pricing | pricing | P1 | Design | 3 tiers |
| Blog | /blog | blog-listing | P2 | Backlog | Launch Month 2 |
| Contact | /contact | form | P1 | QA | Form integration |
```

### Sitemap with Page Attributes

```yaml
sitemap:
  - page: Homepage
    url: /
    template: homepage
    priority: P1
    content_owner: marketing
    seo:
      title: "Company Name - Tagline"
      meta_description: "..."
    children:
      - page: Products
        url: /products
        template: category-landing
        nav_label: "Products"
        show_in_nav: true
        children:
          - page: Product A
            url: /products/product-a
            template: product-detail
            dynamic: false
          - page: Product B
            url: /products/product-b
            template: product-detail
            dynamic: false
```

---

## 6. Card Sorting Analysis

### Card Sorting Types

| Type | Participants | Best For |
|------|--------------|----------|
| Open Sort | Create own categories | Discovery, new sites |
| Closed Sort | Sort into predefined categories | Validation, redesigns |
| Hybrid Sort | Predefined + can add categories | Refinement |

### Conducting Card Sorts

**Preparation**
```markdown
## Card Sort Plan

### Cards (Content Items)
1. Getting Started Guide
2. API Documentation
3. Video Tutorials
4. Pricing Information
5. Case Studies
6. Contact Support
7. Company Blog
8. Career Opportunities
... (30-60 cards typical)

### Participants
- Target: 15-30 participants
- Segments: [New users, Existing users, Specific roles]
- Recruitment method: [Email, User panel, Intercept]

### Instructions
"Please sort these cards into groups that make sense to you.
Give each group a name that describes the contents."
```

**Analysis Methods**

**1. Similarity Matrix**
```
           Card A  Card B  Card C  Card D
Card A       -       80%     20%     10%
Card B      80%       -      15%     25%
Card C      20%      15%      -      70%
Card D      10%      25%     70%       -

(Percentage = how often cards were grouped together)
```

**2. Dendrogram (Cluster Analysis)**
```
100% ─┬─────────────────────────────────────────────
      │
 80% ─┼───────┬───────────────────────────┐
      │       │                           │
 60% ─┼───┬───┤                       ┌───┴───┐
      │   │   │                       │       │
 40% ─┼───┤   ├───┬───┐           ┌───┤   ┌───┤
      │   │   │   │   │           │   │   │   │
  0% ─┴───┴───┴───┴───┴───────────┴───┴───┴───┴───
      A   B   C   D   E           F   G   H   I
```

**3. Category Agreement**

```markdown
## Category: "Learning Resources"

### Cards Consistently Placed Here (>70%)
- Getting Started Guide (92%)
- Video Tutorials (88%)
- Documentation (75%)

### Cards Sometimes Placed Here (40-70%)
- FAQ (55%)
- Webinars (48%)

### Cards Rarely Placed Here (<40%)
- Blog Posts (22%)
- Case Studies (18%)

### Common Alternative Names
- "Help & Support" (6 participants)
- "Learn" (4 participants)
- "Getting Started" (3 participants)
```

### Card Sort Output Template

```markdown
## Card Sort Analysis Report

### Study Overview
- Method: [Open/Closed/Hybrid]
- Participants: [N]
- Cards: [N]
- Completion rate: [%]

### Key Findings

#### Strong Agreements (>70% consistency)
| Cluster | Cards | Agreement | Suggested Label |
|---------|-------|-----------|-----------------|
| 1 | A, B, C | 85% | "Products" |
| 2 | D, E | 78% | "Support" |

#### Contested Items (<50% consistency)
| Card | Top Placements | Recommendation |
|------|----------------|----------------|
| FAQ | Support (40%), Learn (35%) | Place in both, or merge |

### Recommended Navigation Structure
[Based on findings]

### Participant Quotes
- "I expected X to be with Y because..."
- "I wasn't sure where Z belongs..."
```

---

## 7. Menu Structure Patterns

### Menu Depth Guidelines

| Menu Level | Content Type | Max Items |
|------------|--------------|-----------|
| Level 1 (Primary) | Core sections | 5-7 |
| Level 2 (Secondary) | Sub-sections | 5-8 per parent |
| Level 3 (Tertiary) | Specific pages | 8-10 per parent |
| Level 4+ | Avoid | Use different pattern |

### Menu Organization Patterns

**Task-Based**
```
What do you want to do?
├── Learn
│   ├── Tutorials
│   ├── Documentation
│   └── Webinars
├── Build
│   ├── Templates
│   ├── Components
│   └── APIs
└── Deploy
    ├── Hosting
    ├── CI/CD
    └── Monitoring
```

**Audience-Based**
```
I am a...
├── Developer
│   ├── API Docs
│   ├── SDKs
│   └── Code Examples
├── Designer
│   ├── Design System
│   ├── Templates
│   └── Assets
└── Business User
    ├── Pricing
    ├── Case Studies
    └── ROI Calculator
```

**Topic-Based**
```
Browse by topic
├── Security
│   ├── Authentication
│   ├── Encryption
│   └── Compliance
├── Performance
│   ├── Caching
│   ├── CDN
│   └── Optimization
└── Integration
    ├── APIs
    ├── Webhooks
    └── Third-party
```

### Utility Navigation Pattern

```
┌─────────────────────────────────────────────────────────────────┐
│ [Support] [Documentation] [Status] [Login]    [Language: EN ▼] │ ← Utility
├─────────────────────────────────────────────────────────────────┤
│ [Logo]  Products  Solutions  Pricing  Resources  Company       │ ← Primary
└─────────────────────────────────────────────────────────────────┘
```

### Footer Navigation Pattern

```
┌────────────────────────────────────────────────────────────────┐
│ Products        Resources        Company         Support       │
│ ─────────       ─────────        ───────         ───────       │
│ Product A       Blog             About           Help Center   │
│ Product B       Docs             Careers         Contact       │
│ Pricing         Webinars         Press           Status        │
│ Changelog       Case Studies     Partners        Trust         │
├────────────────────────────────────────────────────────────────┤
│ [Logo]                                   [Social] [Social]     │
│ Legal | Privacy | Terms | Sitemap        Copyright 2024        │
└────────────────────────────────────────────────────────────────┘
```

---

## 8. Breadcrumb Strategies

### Breadcrumb Types

**Location-Based (Hierarchical)**
```
Home > Products > Category > Subcategory > Current Page
```
Shows where page sits in site hierarchy.

**Path-Based (History)**
```
Home > Search Results > Product Page
```
Shows how user arrived at current page.

**Attribute-Based (Faceted)**
```
Home > Shoes > Men's > Size 10 > Running [x]
```
Shows applied filters, allows removal.

### Breadcrumb Implementation Patterns

**Standard Breadcrumb**
```
Home / Products / Widgets / Pro Widget
 ^       ^          ^          ^
Link    Link       Link     Current (not linked)
```

**Breadcrumb with Dropdown**
```
Home / Products / [Widgets ▼] / Pro Widget
                      │
                      ├── Gadgets
                      ├── Widgets ✓
                      └── Gizmos
```
Allows switching to sibling categories.

**Breadcrumb with Context**
```
Products (12,345) > Widgets (234) > Pro Widget
```
Shows item counts at each level.

### Breadcrumb Rules

| Rule | Description |
|------|-------------|
| Start with Home | Always include home link |
| Separator | Use "/" or ">" consistently |
| Current page | Display but don't link |
| Truncation | Use "..." for long paths (keep first and last 2) |
| Mobile | Consider hiding middle items |
| Schema markup | Include structured data for SEO |

### Breadcrumb Schema

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Products",
      "item": "https://example.com/products/"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Current Page"
    }
  ]
}
```

---

## 9. Search and Filtering IA

### Search Architecture Components

```
┌─────────────────────────────────────────────────────────────┐
│                      SEARCH INPUT                            │
│  ┌─────────────────────────────────────────────────────┐    │
│  │ [Q] Search products, articles, help...         [Go] │    │
│  └─────────────────────────────────────────────────────┘    │
│                                                              │
│  Recent: widget setup | api docs | pricing                   │
│  Popular: getting started | integration guide                │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    SEARCH RESULTS                            │
│                                                              │
│  Found 234 results for "widget"                              │
│                                                              │
│  ┌─────────────┐  ┌─────────────────────────────────────┐   │
│  │ FILTERS     │  │ RESULTS                              │   │
│  │             │  │                                      │   │
│  │ Type        │  │ [Product] Pro Widget                 │   │
│  │ [ ] Product │  │ The most advanced widget for...      │   │
│  │ [ ] Article │  │ /products/pro-widget                 │   │
│  │ [ ] Help    │  │                                      │   │
│  │             │  │ [Article] Widget Setup Guide         │   │
│  │ Category    │  │ Learn how to configure widgets...    │   │
│  │ [ ] Widgets │  │ /docs/widget-setup                   │   │
│  │ [ ] Gadgets │  │                                      │   │
│  │             │  │ [Help] Troubleshooting Widgets       │   │
│  │ Date        │  │ Common widget issues and fixes...    │   │
│  │ [Last year] │  │ /help/widget-troubleshooting         │   │
│  └─────────────┘  └─────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

### Filter Types

| Filter Type | UI Pattern | Best For |
|-------------|------------|----------|
| Checkbox | Multi-select | Categories, tags |
| Radio | Single-select | Mutually exclusive options |
| Range Slider | Min-max | Price, date, numeric |
| Toggle | On/off | Boolean attributes |
| Dropdown | Select one | Long lists, secondary filters |
| Search within filter | Type-ahead | Many options (brands, locations) |

### Filter Organization

```markdown
## Filter Panel Structure

### Primary Filters (Always Visible)
- Category (highest impact on results)
- Price range (for e-commerce)
- Content type (for resource sites)

### Secondary Filters (Collapsible)
- Brand/Author
- Date range
- Ratings
- Specific attributes

### Applied Filters (Chip Display)
[Category: Widgets ×] [Price: $0-$100 ×] [Clear All]
```

### Search Results Design

**Result Card Components**
```markdown
┌────────────────────────────────────────────────────────┐
│ [Content Type Badge]                                    │
│ **Title with keyword highlighted**                      │
│ Description excerpt with **keyword** in context...      │
│                                                         │
│ Breadcrumb: Products > Category > Subcategory           │
│ Meta: Date | Author | Reading time                      │
└────────────────────────────────────────────────────────┘
```

**Zero Results State**
```markdown
## No results found for "xyz123"

### Suggestions
- Check your spelling
- Try more general terms
- Remove some filters

### Popular Searches
- Getting started
- API documentation
- Pricing

### Browse Categories
[Products] [Resources] [Help]
```

### Faceted Navigation Matrix

```markdown
## Facet Definition: [Content Type]

| Facet Value | Display Name | Count | Sort Order |
|-------------|--------------|-------|------------|
| product | Products | Dynamic | 1 |
| article | Articles | Dynamic | 2 |
| video | Videos | Dynamic | 3 |
| help | Help & Support | Dynamic | 4 |

### Behavior Rules
- Show facet only if count > 0
- Sort by relevance within facet
- Allow multi-select (OR logic)
- Cross-facet filtering uses AND logic
```

---

## 10. IA Documentation Templates

### Complete IA Document Structure

```markdown
# Information Architecture: [Project Name]
Version: [X.X] | Last Updated: [Date] | Author: [Name]

---

## 1. Executive Summary
[2-3 paragraphs summarizing key IA decisions]

## 2. User Analysis

### 2.1 Primary User Types
| User Type | Goals | Mental Model | Priority |
|-----------|-------|--------------|----------|
| [Type A] | [Goals] | [How they think] | P1 |

### 2.2 User Journey Context
- Where users come from (entry points)
- What they're trying to accomplish
- How they expect information organized

## 3. Content Inventory Summary

### 3.1 Content Types
| Type | Count | Template | Owner |
|------|-------|----------|-------|
| [Type] | [N] | [Template] | [Team] |

### 3.2 Content Relationships
[Diagram showing how content types relate]

## 4. Site Structure

### 4.1 Structure Type
[Hierarchical/Flat/Hub-Spoke/Matrix] - [Rationale]

### 4.2 Sitemap
[Visual sitemap with all pages]

### 4.3 URL Structure
| Pattern | Example | Notes |
|---------|---------|-------|
| /[category]/[slug] | /products/widget-pro | Product pages |

## 5. Navigation System

### 5.1 Navigation Components
- Primary Navigation: [Pattern + items]
- Secondary Navigation: [Pattern + items]
- Utility Navigation: [Pattern + items]
- Mobile Navigation: [Pattern]

### 5.2 Navigation Specifications
[Detailed specs for each nav component]

## 6. Page Templates

### 6.1 Template Inventory
| Template | Used For | Key Components |
|----------|----------|----------------|
| homepage | Home | Hero, features, social proof |
| category | Category landing | Intro, card grid, filters |

### 6.2 Template Wireframes
[Low-fidelity wireframes for each template]

## 7. User Flows

### 7.1 Critical Flows
[Flow diagrams for key user journeys]

### 7.2 Flow Specifications
[Detailed specs for each flow]

## 8. Search & Filtering

### 8.1 Search Strategy
- Search scope: [What's searchable]
- Results display: [How results appear]
- Filters available: [Filter list]

### 8.2 Filter Specifications
[Detailed filter definitions]

## 9. Cross-Linking Strategy

### 9.1 Related Content Rules
| From Page Type | Link To | Placement | Logic |
|---------------|---------|-----------|-------|
| Product | Related products | Below content | Tag match |

### 9.2 Internal Linking Guidelines
[Rules for content creators]

## 10. Governance

### 10.1 Taxonomy Management
[Rules for adding/changing taxonomy]

### 10.2 Content Lifecycle
[Rules for content creation, review, archival]

---

## Appendices

### A. Sitemap (Full Detail)
### B. Content Inventory
### C. Card Sort Results
### D. User Research Findings
```

### Quick Reference Card

```markdown
## IA Quick Reference: [Project]

### Navigation
PRIMARY: Home | Products | Solutions | Resources | Company
UTILITY: Support | Docs | Login
MOBILE: Hamburger + bottom bar for key actions

### URL Patterns
/                       Homepage
/products/              Products listing
/products/[slug]/       Product detail
/solutions/[slug]/      Solution page
/resources/             Resources hub
/resources/[type]/      Filtered resources
/blog/[year]/[slug]/    Blog post

### Breadcrumbs
Always: Home > Section > Subsection > Page
Truncate at 4 levels on mobile

### Search
Scope: Products, Resources, Help
Filters: Type, Category, Date
Results: Title, excerpt, breadcrumb, meta

### Key Flows
1. Product discovery: Home > Products > Detail > CTA
2. Support: Any page > Help > Article > Contact
3. Conversion: Home > Pricing > Signup > Onboard
```

---

## Quality Checklist

### IA Completeness
- [ ] User types and mental models defined
- [ ] Content inventory completed
- [ ] Site structure methodology chosen and documented
- [ ] Full sitemap with all pages
- [ ] URL conventions defined
- [ ] All navigation components specified
- [ ] Page templates identified
- [ ] Critical user flows mapped
- [ ] Search and filtering strategy defined
- [ ] Cross-linking rules established

### IA Quality
- [ ] Navigation follows 7 +/- 2 rule
- [ ] 3-click rule validated for key content
- [ ] Consistent labeling throughout
- [ ] Mobile navigation considered
- [ ] Breadcrumbs specified
- [ ] Search handles zero results
- [ ] Taxonomy is controlled and documented

### Stakeholder Alignment
- [ ] Business goals reflected in IA
- [ ] SEO requirements addressed
- [ ] Content team can execute
- [ ] Technical team can implement
- [ ] Governance plan in place

---

## Common Pitfalls

| Pitfall | Prevention |
|---------|------------|
| Org-chart navigation | Use user mental models, not internal structure |
| Too deep hierarchy | Keep to 3-4 levels maximum |
| Inconsistent labels | Create controlled vocabulary |
| Missing mobile strategy | Design mobile nav first, then desktop |
| No governance plan | Define taxonomy management upfront |
| Ignoring search | Search is navigation for many users |
| Static thinking | Plan for content growth and change |
