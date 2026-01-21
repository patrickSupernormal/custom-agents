---
skill: wireframe-spec-templates
version: "1.0.0"
description: "Comprehensive wireframe documentation standards, ASCII patterns, and handoff-ready specification templates"
used-by: ["@wireframe-spec"]
---

# Wireframe Specification Templates

## Purpose
Provide standardized templates and patterns for creating detailed, unambiguous wireframe specifications that designers and developers can execute without guesswork. These specifications bridge the gap between conceptual design and implementation.

---

## 1. Wireframe Documentation Standards

### Document Structure
Every wireframe specification document follows this hierarchy:

```markdown
# Page Wireframe: [Page Name]
Version: [X.X] | Last Updated: [Date] | Status: [Draft/Review/Approved]

## Page Overview
- Purpose: [Why this page exists]
- Primary Goal: [What users should accomplish]
- Target Audience: [Who uses this page]
- Entry Points: [How users arrive here]
- Exit Points: [Where users go next]

## Layout Specifications
[ASCII wireframe with annotations]

## Section Details
[Section-by-section breakdown]

## Responsive Behavior
[Breakpoint specifications]

## Interaction States
[Hover, focus, active, error states]

## Accessibility Requirements
[A11y specifications]

## Content Requirements
[Placeholder content and constraints]

## Design Notes
[Guidance without over-prescription]
```

### Naming Conventions

| Element Type | Convention | Example |
|--------------|------------|---------|
| Pages | kebab-case | `user-profile-page` |
| Sections | PascalCase | `HeroSection`, `NavigationBar` |
| Components | PascalCase | `SearchInput`, `UserCard` |
| States | camelCase suffix | `buttonHover`, `inputError` |
| Breakpoints | t-shirt sizes | `xs`, `sm`, `md`, `lg`, `xl` |

### Version Control
```markdown
## Change History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2024-01-15 | [Name] | Initial specification |
| 1.1 | 2024-01-20 | [Name] | Added mobile breakpoints |
| 1.2 | 2024-01-25 | [Name] | Updated form validation states |
```

---

## 2. ASCII/Text-Based Wireframe Patterns

### Basic Container Elements

```
Full-Width Container
+------------------------------------------------------------------------+
|                                                                        |
+------------------------------------------------------------------------+

Constrained Container (max-width)
          +--------------------------------------------------+
          |                                                  |
          +--------------------------------------------------+

Split Container (50/50)
+----------------------------------+----------------------------------+
|                                  |                                  |
|            Left Panel            |           Right Panel            |
|                                  |                                  |
+----------------------------------+----------------------------------+

Asymmetric Split (2/3 - 1/3)
+----------------------------------------------+--------------------+
|                                              |                    |
|                 Main Content                 |      Sidebar       |
|                                              |                    |
+----------------------------------------------+--------------------+
```

### Navigation Patterns

```
Horizontal Navigation Bar
+------------------------------------------------------------------------+
| [Logo]     [Nav Item]  [Nav Item]  [Nav Item]           [Search] [CTA] |
+------------------------------------------------------------------------+

Horizontal Nav with Dropdown Indicator
+------------------------------------------------------------------------+
| [Logo]  Products v   Solutions v   Resources v   Company   [Get Demo]  |
+------------------------------------------------------------------------+

Mega Menu (expanded)
+------------------------------------------------------------------------+
| [Logo]  Products v   Solutions    Resources    Company     [Get Demo]  |
+--------+---------------------------------------------------------------+
|        |  Category A        Category B        Category C               |
|        |  - Item 1          - Item 1          - Item 1                 |
|        |  - Item 2          - Item 2          - Item 2                 |
|        |  - Item 3          - Item 3          - Item 3                 |
|        |                                                               |
|        |  [Featured Image]   Featured description text here            |
+--------+---------------------------------------------------------------+

Mobile Hamburger Menu (collapsed)
+------------------------------------------+
| [Logo]                          [=] Menu |
+------------------------------------------+

Mobile Menu (expanded)
+------------------------------------------+
| [Logo]                              [X]  |
+------------------------------------------+
| [Nav Item]                           >   |
+------------------------------------------+
| [Nav Item]                           >   |
+------------------------------------------+
| [Nav Item]                           >   |
+------------------------------------------+
| [CTA Button - Full Width]                |
+------------------------------------------+

Sidebar Navigation
+--------------------+--------------------------------------------+
| [Logo]             |                                            |
+--------------------+                                            |
| > Dashboard        |                                            |
| > Analytics        |           Main Content Area                |
|   - Overview       |                                            |
|   - Reports        |                                            |
| > Settings         |                                            |
| > Help             |                                            |
+--------------------+--------------------------------------------+
```

### Hero Section Patterns

```
Hero with CTA (Centered)
+------------------------------------------------------------------------+
|                                                                        |
|                         [Eyebrow Text]                                 |
|                                                                        |
|                    MAIN HEADLINE TEXT HERE                             |
|                                                                        |
|              Supporting description text that elaborates               |
|                   on the headline proposition.                         |
|                                                                        |
|                 [Primary CTA]    [Secondary CTA]                       |
|                                                                        |
+------------------------------------------------------------------------+

Hero with Image (Split Layout)
+-----------------------------------+------------------------------------+
|                                   |                                    |
|   [Eyebrow Text]                  |                                    |
|                                   |                                    |
|   MAIN HEADLINE                   |         +------------------+       |
|   TEXT HERE                       |         |                  |       |
|                                   |         |   Hero Image     |       |
|   Supporting description          |         |   or Video       |       |
|   text goes here with             |         |                  |       |
|   more details.                   |         +------------------+       |
|                                   |                                    |
|   [Primary CTA]  [Secondary]      |                                    |
|                                   |                                    |
+-----------------------------------+------------------------------------+

Hero with Background Image
+========================================================================+
||                                                                      ||
||  (Background Image/Video Layer)                                      ||
||                                                                      ||
||                    HEADLINE OVER IMAGE                               ||
||                                                                      ||
||              Description text with overlay treatment                 ||
||                                                                      ||
||                         [CTA Button]                                 ||
||                                                                      ||
+========================================================================+
```

### Card Patterns

```
Basic Card
+------------------------+
| +--------------------+ |
| |   [Image/Media]    | |
| +--------------------+ |
|                        |
| Category Label         |
| Card Heading           |
| Description text that  |
| may wrap to multiple   |
| lines as needed.       |
|                        |
| [Link Text ->]         |
+------------------------+

Card Grid (3-up)
+------------------------+  +------------------------+  +------------------------+
| +--------------------+ |  | +--------------------+ |  | +--------------------+ |
| |      [Image]       | |  | |      [Image]       | |  | |      [Image]       | |
| +--------------------+ |  | +--------------------+ |  | +--------------------+ |
|                        |  |                        |  |                        |
| Card Title             |  | Card Title             |  | Card Title             |
| Short description      |  | Short description      |  | Short description      |
| text here.             |  | text here.             |  | text here.             |
|                        |  |                        |  |                        |
| [Learn More]           |  | [Learn More]           |  | [Learn More]           |
+------------------------+  +------------------------+  +------------------------+

Horizontal Card
+------------------------------------------------------------------------+
| +----------------+                                                     |
| |                |   Card Title Here                                   |
| |    [Image]     |                                                     |
| |                |   Description text that provides more context       |
| +----------------+   about this item. Can span multiple lines.         |
|                                                                        |
|                                               [Action Button]          |
+------------------------------------------------------------------------+

Pricing Card
+---------------------------+
|        PLAN NAME          |
|        $XX/month          |
+---------------------------+
|                           |
|   [check] Feature one     |
|   [check] Feature two     |
|   [check] Feature three   |
|   [x] Feature four        |
|   [x] Feature five        |
|                           |
| +------------------------+|
| |   [Select Plan]        ||
| +------------------------+|
+---------------------------+
```

### Form Patterns

```
Single Column Form
+--------------------------------------------+
|                                            |
|  Form Title                                |
|  Helper text describing the form purpose   |
|                                            |
|  Label *                                   |
|  +--------------------------------------+  |
|  | Placeholder text                     |  |
|  +--------------------------------------+  |
|                                            |
|  Label                                     |
|  +--------------------------------------+  |
|  | Placeholder text                     |  |
|  +--------------------------------------+  |
|  Helper text for this field               |
|                                            |
|  Label *                                   |
|  +--------------------------------------+  |
|  |                                    v |  |
|  +--------------------------------------+  |
|                                            |
|  [ ] I agree to the terms and conditions  |
|                                            |
|  +--------------------------------------+  |
|  |           [Submit Button]            |  |
|  +--------------------------------------+  |
|                                            |
+--------------------------------------------+

Two Column Form
+--------------------------------------------+
|                                            |
|  First Name *              Last Name *     |
|  +------------------+  +------------------+|
|  | First            |  | Last             ||
|  +------------------+  +------------------+|
|                                            |
|  Email *                                   |
|  +--------------------------------------+  |
|  | email@example.com                    |  |
|  +--------------------------------------+  |
|                                            |
|  City                    State     Zip     |
|  +--------------+ +--------+ +-----------+ |
|  | City         | | ST   v | | 00000     | |
|  +--------------+ +--------+ +-----------+ |
|                                            |
+--------------------------------------------+

Search Form with Filters
+------------------------------------------------------------------------+
| +----------------------------------------------------------------+     |
| | [Search Icon] Search...                                        |     |
| +----------------------------------------------------------------+     |
|                                                                        |
| Filters:  [Category v]  [Date Range v]  [Status v]  [Clear All]        |
+------------------------------------------------------------------------+

Login Form
+------------------------------------------+
|                                          |
|              [Logo/Icon]                 |
|                                          |
|           Welcome Back                   |
|    Sign in to your account               |
|                                          |
|  Email                                   |
|  +------------------------------------+  |
|  | email@example.com                  |  |
|  +------------------------------------+  |
|                                          |
|  Password                 Forgot?        |
|  +------------------------------------+  |
|  | ********                           |  |
|  +------------------------------------+  |
|                                          |
|  +------------------------------------+  |
|  |            Sign In                 |  |
|  +------------------------------------+  |
|                                          |
|  -------- Or continue with --------     |
|                                          |
|  [Google]  [GitHub]  [Microsoft]         |
|                                          |
|  Don't have an account? Sign up          |
|                                          |
+------------------------------------------+
```

### Data Display Patterns

```
Basic Table
+------------------------------------------------------------------------+
| Column A        | Column B        | Column C        | Actions          |
+------------------------------------------------------------------------+
| Cell content    | Cell content    | Cell content    | [Edit] [Delete]  |
+-----------------+-----------------+-----------------+------------------+
| Cell content    | Cell content    | Cell content    | [Edit] [Delete]  |
+-----------------+-----------------+-----------------+------------------+
| Cell content    | Cell content    | Cell content    | [Edit] [Delete]  |
+------------------------------------------------------------------------+
|                             [Load More]                                |
+------------------------------------------------------------------------+

Data Table with Selection
+------------------------------------------------------------------------+
| [ ] | Name          | Status    | Date       | Amount   | Actions      |
+------------------------------------------------------------------------+
| [ ] | Item Name     | Active    | 2024-01-15 | $125.00  | [...]        |
+-----+---------------+-----------+------------+----------+--------------+
| [x] | Item Name     | Pending   | 2024-01-14 | $250.00  | [...]        |
+-----+---------------+-----------+------------+----------+--------------+
| [ ] | Item Name     | Complete  | 2024-01-13 | $75.00   | [...]        |
+------------------------------------------------------------------------+
| Showing 1-10 of 156 results            [<] [1] [2] [3] ... [16] [>]    |
+------------------------------------------------------------------------+

List View
+------------------------------------------------------------------------+
| +------------------------------------------------------------------+   |
| | [Avatar]  Title or Name                           [Badge] [Menu] |   |
| |           Subtitle or description text                           |   |
| |           Meta info | More meta | Timestamp                      |   |
| +------------------------------------------------------------------+   |
|                                                                        |
| +------------------------------------------------------------------+   |
| | [Avatar]  Title or Name                           [Badge] [Menu] |   |
| |           Subtitle or description text                           |   |
| |           Meta info | More meta | Timestamp                      |   |
| +------------------------------------------------------------------+   |
+------------------------------------------------------------------------+
```

### Modal/Dialog Patterns

```
Standard Modal
                 +------------------------------------------+
                 | Modal Title                         [X]  |
                 +------------------------------------------+
                 |                                          |
                 |  Modal content goes here. This can       |
                 |  include text, forms, images, or any     |
                 |  other content as needed.                |
                 |                                          |
                 |                                          |
                 +------------------------------------------+
                 |              [Cancel]  [Confirm]         |
                 +------------------------------------------+

Confirmation Dialog
                 +------------------------------------------+
                 |  [Warning Icon]                          |
                 |                                          |
                 |  Delete this item?                       |
                 |                                          |
                 |  This action cannot be undone. The       |
                 |  item will be permanently removed.       |
                 |                                          |
                 |              [Cancel]  [Delete]          |
                 +------------------------------------------+

Full-Screen Modal (Mobile)
+------------------------------------------+
| [<- Back]    Modal Title           [X]   |
+------------------------------------------+
|                                          |
|  Full screen modal content area.         |
|                                          |
|  This pattern is used on mobile          |
|  devices where modals take over          |
|  the entire viewport.                    |
|                                          |
|                                          |
|                                          |
|                                          |
+------------------------------------------+
|  [Full-Width Action Button]              |
+------------------------------------------+
```

---

## 3. Component Annotation Methods

### Annotation Syntax

Use numbered callouts in ASCII wireframes with corresponding detail sections:

```
+------------------------------------------------------------------------+
| [1]                                                                    |
+------------------------------------------------------------------------+
| [Logo] [2]     [3] Nav  Nav  Nav           [4] Search    [5] [CTA]    |
+------------------------------------------------------------------------+
|                                                                        |
|                            [6]                                         |
|                     HERO HEADLINE                                      |
|                                                                        |
|                   [7] Supporting text                                  |
|                                                                        |
|                [8] Primary    [9] Secondary                            |
|                                                                        |
+------------------------------------------------------------------------+

### Annotations

[1] STICKY HEADER
    - Behavior: Fixed on scroll after 100px
    - Height: 64px (desktop), 56px (mobile)
    - Background: White with shadow on scroll
    - Z-index: 100

[2] LOGO
    - Component: <Logo />
    - Size: 120x40px max
    - Link: Routes to homepage
    - Alt text required

[3] NAVIGATION ITEMS
    - Component: <NavItem />
    - Count: 4-6 items
    - Active state: Underline + bold
    - Includes dropdown indicator where applicable

[4] SEARCH
    - Component: <SearchInput />
    - Behavior: Expands on focus
    - Mobile: Icon only, opens overlay

[5] CTA BUTTON
    - Component: <Button variant="primary" />
    - Text: "Get Started" (max 15 chars)
    - Mobile: May hide below lg breakpoint

[6] HERO HEADLINE
    - Element: <h1>
    - Max characters: 60
    - Typography: Display Large

[7] SUPPORTING TEXT
    - Element: <p>
    - Max characters: 150
    - Typography: Body Large

[8] PRIMARY CTA
    - Component: <Button variant="primary" size="lg" />
    - Action: Routes to signup

[9] SECONDARY CTA
    - Component: <Button variant="outline" size="lg" />
    - Action: Opens demo modal
```

### Component Specification Format

```markdown
## Component: [ComponentName]

### Purpose
[What this component does and when to use it]

### Variants
| Variant | Description | Use When |
|---------|-------------|----------|
| primary | Bold, filled | Main actions |
| secondary | Outlined | Supporting actions |
| ghost | Text only | Tertiary actions |

### Props
| Prop | Type | Default | Required | Description |
|------|------|---------|----------|-------------|
| variant | string | "primary" | No | Visual style |
| size | "sm" \| "md" \| "lg" | "md" | No | Size preset |
| disabled | boolean | false | No | Disabled state |
| loading | boolean | false | No | Loading state |
| onClick | function | - | Yes | Click handler |

### Sizes
| Size | Height | Padding | Font Size |
|------|--------|---------|-----------|
| sm | 32px | 8px 12px | 14px |
| md | 40px | 10px 16px | 16px |
| lg | 48px | 12px 24px | 18px |

### States (see Section 5 for visuals)
- Default
- Hover
- Focus
- Active
- Disabled
- Loading
```

---

## 4. Responsive Breakpoint Documentation

### Standard Breakpoint Definitions

```markdown
## Breakpoint Definitions

| Name | Shorthand | Min Width | Target Devices |
|------|-----------|-----------|----------------|
| Extra Small | xs | 0px | Small phones |
| Small | sm | 640px | Large phones |
| Medium | md | 768px | Tablets portrait |
| Large | lg | 1024px | Tablets landscape, small laptops |
| Extra Large | xl | 1280px | Desktops |
| 2X Large | 2xl | 1536px | Large desktops |
```

### Responsive Behavior Matrix

```markdown
## Section: Hero

| Element | xs-sm | md | lg+ |
|---------|-------|-----|------|
| Layout | Stack (column) | Stack (column) | Split (row) |
| Headline | 32px | 40px | 56px |
| Image | Below text, 100% | Below text, 80% | Right side, 50% |
| CTA Buttons | Stack, full-width | Inline | Inline |
| Padding | 16px | 32px | 64px |
```

### Responsive Wireframe Examples

```
DESKTOP (lg+)
+----------------------------------+----------------------------------+
|                                  |         +------------------+     |
|   Headline Text Here             |         |                  |     |
|                                  |         |     [Image]      |     |
|   Description paragraph          |         |                  |     |
|                                  |         +------------------+     |
|   [Primary]  [Secondary]         |                                  |
+----------------------------------+----------------------------------+

TABLET (md)
+------------------------------------------------------------------------+
|                                                                        |
|                         Headline Text Here                             |
|                                                                        |
|                      Description paragraph                             |
|                                                                        |
|                    [Primary]  [Secondary]                              |
|                                                                        |
|                      +--------------------+                            |
|                      |                    |                            |
|                      |      [Image]       |                            |
|                      |                    |                            |
|                      +--------------------+                            |
|                                                                        |
+------------------------------------------------------------------------+

MOBILE (xs-sm)
+------------------------------------------+
|                                          |
|    Headline Text                         |
|    Here                                  |
|                                          |
|    Description paragraph that            |
|    wraps to multiple lines               |
|    on smaller screens.                   |
|                                          |
|    +----------------------------------+  |
|    |          [Primary CTA]          |  |
|    +----------------------------------+  |
|                                          |
|    +----------------------------------+  |
|    |         [Secondary CTA]         |  |
|    +----------------------------------+  |
|                                          |
|    +----------------------------------+  |
|    |                                  |  |
|    |           [Image]               |  |
|    |                                  |  |
|    +----------------------------------+  |
|                                          |
+------------------------------------------+
```

### Responsive Pattern Reference

| Pattern | Description | Use For |
|---------|-------------|---------|
| Stack | Column layout on small, row on large | Hero, feature sections |
| Collapse | Fewer columns on small | Card grids, galleries |
| Hide/Show | Elements appear/disappear | Navigation, secondary actions |
| Reorder | Elements change visual order | Media + text pairs |
| Resize | Same layout, scaled sizes | Typography, spacing |
| Transform | Complete layout change | Navigation (horizontal to hamburger) |

---

## 5. Interaction State Documentation

### State Specification Template

```markdown
## Component States: [ComponentName]

### Visual States Matrix

| State | Background | Border | Text | Icon | Shadow |
|-------|------------|--------|------|------|--------|
| Default | #FFFFFF | #E5E7EB | #374151 | #6B7280 | none |
| Hover | #F9FAFB | #D1D5DB | #111827 | #374151 | sm |
| Focus | #FFFFFF | #3B82F6 (2px) | #374151 | #6B7280 | ring |
| Active | #F3F4F6 | #9CA3AF | #111827 | #374151 | none |
| Disabled | #F9FAFB | #E5E7EB | #9CA3AF | #D1D5DB | none |
| Error | #FEF2F2 | #EF4444 | #374151 | #EF4444 | none |
| Success | #F0FDF4 | #22C55E | #374151 | #22C55E | none |
| Loading | #F9FAFB | #E5E7EB | #9CA3AF | spin | none |
```

### ASCII State Representations

```
BUTTON STATES

Default:
+-------------------+
|    Button Text    |
+-------------------+

Hover:
+-------------------+
|////Button Text////|  (background fill change)
+-------------------+

Focus:
+=====================+
||   Button Text    ||  (visible focus ring)
+=====================+

Active/Pressed:
[-------------------]
[    Button Text    ]  (depressed appearance)
[-------------------]

Disabled:
+- - - - - - - - - -+
|    Button Text    |  (reduced opacity, no interaction)
+- - - - - - - - - -+

Loading:
+-------------------+
|    [spinner]      |  (text replaced with loader)
+-------------------+


INPUT FIELD STATES

Default:
+------------------------------------+
| Placeholder text                   |
+------------------------------------+

Focus:
+====================================+
| Cursor here_                       |  (highlight border)
+====================================+

Filled:
+------------------------------------+
| User entered value                 |
+------------------------------------+

Error:
+------------------------------------+  [!]
| Invalid input                      |  (red border)
+------------------------------------+
  Error message text here

Success:
+------------------------------------+  [check]
| Valid input                        |  (green border)
+------------------------------------+

Disabled:
+- - - - - - - - - - - - - - - - - -+
| Cannot edit                        |  (grayed out)
+- - - - - - - - - - - - - - - - - -+
```

### Interaction Flow Documentation

```markdown
## Interaction: Dropdown Menu

### Trigger
- Click on dropdown button
- Keyboard: Enter or Space when focused

### States Flow
1. CLOSED (default)
   - Arrow pointing down
   - Menu hidden

2. OPENING (transition)
   - Duration: 150ms
   - Animation: Fade + slide down

3. OPEN
   - Arrow pointing up
   - Menu visible
   - First item focused (keyboard)

4. ITEM HOVER
   - Background highlight on hovered item
   - Pointer cursor

5. ITEM SELECTED
   - Brief highlight feedback
   - Menu closes
   - Value updates

### Keyboard Navigation
| Key | Action |
|-----|--------|
| Enter/Space | Open menu (when closed), Select item (when open) |
| Escape | Close menu |
| Arrow Down | Move focus to next item |
| Arrow Up | Move focus to previous item |
| Home | Move focus to first item |
| End | Move focus to last item |
| Tab | Close menu, move focus to next element |
```

---

## 6. Accessibility Annotations

### Landmark Structure

```
+------------------------------------------------------------------------+
| <header role="banner">                                                 |
|   <nav role="navigation" aria-label="Main">                           |
|     [Logo] [Nav Items]                                                 |
|   </nav>                                                               |
+------------------------------------------------------------------------+
| <main role="main">                                                     |
|   +----------------------------------------------------+               |
|   | <section aria-labelledby="hero-heading">           |               |
|   |   <h1 id="hero-heading">...</h1>                   |               |
|   +----------------------------------------------------+               |
|                                                                        |
|   +------------------------------+-------------------------+           |
|   | <section aria-labelledby=    | <aside role="complementary">       |
|   |   "content-heading">         |   [Sidebar Content]    |           |
|   |   <h2 id="content-heading">  |                        |           |
|   +------------------------------+-------------------------+           |
+------------------------------------------------------------------------+
| <footer role="contentinfo">                                            |
|   [Footer Content]                                                     |
+------------------------------------------------------------------------+
```

### Heading Hierarchy Specification

```markdown
## Heading Structure

h1: Page Title (1 per page)
├── h2: Section A
│   ├── h3: Subsection A.1
│   └── h3: Subsection A.2
│       └── h4: Detail A.2.1
├── h2: Section B
│   ├── h3: Subsection B.1
│   └── h3: Subsection B.2
└── h2: Section C

### Heading Audit
| Level | Text | Element | Notes |
|-------|------|---------|-------|
| h1 | Welcome to [Site] | hero-heading | Required, single |
| h2 | Featured Products | featured-section | |
| h2 | Testimonials | testimonials-section | |
| h2 | Get Started | cta-section | |
```

### Focus Order Specification

```
+------------------------------------------------------------------------+
| [1] Skip Link (visible on focus)                                       |
+------------------------------------------------------------------------+
| [2] Logo    [3-6] Nav Items    [7] Search    [8] CTA                  |
+------------------------------------------------------------------------+
|                                                                        |
|    [9] Headline                                                        |
|    [10] Primary CTA    [11] Secondary CTA                              |
|                                                                        |
+------------------------------------------------------------------------+
|                                                                        |
|   [12] Card 1    [13] Card 2    [14] Card 3                           |
|                                                                        |
+------------------------------------------------------------------------+

### Focus Order Notes
- Tab order follows visual left-to-right, top-to-bottom flow
- Skip link appears first, visible only on focus
- Interactive elements only (no focus on headings/text)
- Modal focus traps when open
```

### ARIA Annotations

```markdown
## ARIA Requirements

### Navigation
```html
<nav aria-label="Main navigation">
<nav aria-label="Footer navigation">
<nav aria-label="Breadcrumb" aria-labelledby="breadcrumb-label">
```

### Interactive Elements
| Component | ARIA Attributes |
|-----------|-----------------|
| Dropdown | `aria-haspopup="listbox"`, `aria-expanded="true/false"` |
| Modal | `role="dialog"`, `aria-modal="true"`, `aria-labelledby` |
| Tab Panel | `role="tablist"`, `role="tab"`, `aria-selected`, `role="tabpanel"` |
| Accordion | `aria-expanded`, `aria-controls` |
| Alert | `role="alert"`, `aria-live="polite"` |
| Loading | `aria-busy="true"`, `aria-live="polite"` |

### Form Fields
| Requirement | Implementation |
|-------------|----------------|
| Labels | `<label for="">` or `aria-label` |
| Required | `aria-required="true"` + visual indicator |
| Errors | `aria-invalid="true"` + `aria-describedby` |
| Help text | `aria-describedby` linking to helper |
```

### Screen Reader Annotations

```
+--------------------------------------------+
|  [Image]                                   |
|  SR: "Product photo: Blue running shoe    |
|       on white background"                 |
+--------------------------------------------+
|  [Icon Button: Close]                      |
|  SR: "Close dialog"                        |
+--------------------------------------------+
|  Price: $99.99                             |
|  SR: "Price: ninety-nine dollars and      |
|       ninety-nine cents"                   |
+--------------------------------------------+
|  [Star Rating: 4.5/5]                      |
|  SR: "Rating: 4.5 out of 5 stars"         |
+--------------------------------------------+
```

---

## 7. Content Placeholder Conventions

### Text Placeholders

| Type | Convention | Example |
|------|------------|---------|
| Headlines | Descriptive with char count | `Headline (40 chars max)` |
| Body text | Lorem with word count | `[Lorem 50 words]` |
| User content | Realistic examples | `"John D." / "San Francisco, CA"` |
| Numbers | Realistic ranges | `$XX.XX` or `$99.99` |
| Dates | Format specification | `MMM DD, YYYY` or `Jan 15, 2024` |

### Character Count Specifications

```markdown
## Content Constraints

| Element | Min | Max | Optimal | Notes |
|---------|-----|-----|---------|-------|
| Page Title | 20 | 60 | 40-50 | SEO optimized |
| Hero Headline | 30 | 80 | 50-60 | Above the fold |
| Hero Subhead | 80 | 160 | 100-120 | Single paragraph |
| Card Title | 15 | 50 | 25-35 | 2 lines max |
| Card Description | 50 | 120 | 80-100 | 3 lines max |
| Button Text | 5 | 20 | 10-15 | Action verb + noun |
| Nav Item | 5 | 20 | 8-12 | Single word preferred |
| Meta Description | 120 | 160 | 150-155 | SEO |
```

### Image Placeholder Specifications

```
+--------------------------------+
|                                |
|    [IMAGE: Hero]               |
|    Aspect: 16:9                |
|    Min: 1200x675               |
|    Content: Product in use     |
|    Alt: Required, descriptive  |
|                                |
+--------------------------------+

+------------------+
|                  |
|  [AVATAR]        |
|  Size: 48x48     |
|  Shape: Circle   |
|  Fallback: Init  |
|                  |
+------------------+

+------------------+
|  [ICON]          |
|  Size: 24x24     |
|  Style: Outline  |
|  Color: Inherit  |
+------------------+
```

### Content Types Matrix

```markdown
## Content Type Specifications

| Content Type | Format | Source | Fallback |
|--------------|--------|--------|----------|
| User Avatar | Image/Initials | User upload | Generated initials |
| Product Image | JPG/WebP | CMS | Placeholder image |
| Icon | SVG | Icon library | Text label |
| Video | MP4/WebM | CDN | Poster image |
| Logo | SVG | Assets | Text fallback |
```

---

## 8. Grid and Spacing Documentation

### Grid System Specification

```markdown
## Grid System

### Base Grid
- Columns: 12
- Gutter: 24px (desktop), 16px (mobile)
- Margin: 64px (xl), 48px (lg), 32px (md), 16px (sm/xs)
- Max-width: 1280px

### Column Spans
| Element | xs | sm | md | lg | xl |
|---------|----|----|----|----|-----|
| Full-width | 12 | 12 | 12 | 12 | 12 |
| Hero Text | 12 | 12 | 12 | 6 | 6 |
| Hero Image | 12 | 12 | 12 | 6 | 6 |
| Card (grid) | 12 | 6 | 6 | 4 | 4 |
| Sidebar | 12 | 12 | 4 | 3 | 3 |
| Main Content | 12 | 12 | 8 | 9 | 9 |
```

### ASCII Grid Representation

```
12-COLUMN GRID (Desktop)
+--+--+--+--+--+--+--+--+--+--+--+--+
| 1| 2| 3| 4| 5| 6| 7| 8| 9|10|11|12|
+--+--+--+--+--+--+--+--+--+--+--+--+

COMMON LAYOUTS

Full Width (span 12)
+--------------------------------------------------+
|                                                  |
+--------------------------------------------------+

Two Columns (span 6 + 6)
+------------------------+------------------------+
|                        |                        |
+------------------------+------------------------+

Three Columns (span 4 + 4 + 4)
+---------------+----------------+----------------+
|               |                |                |
+---------------+----------------+----------------+

Content + Sidebar (span 8 + 4)
+----------------------------------+-------------+
|                                  |             |
+----------------------------------+-------------+

Asymmetric (span 7 + 5)
+----------------------------+-------------------+
|                            |                   |
+----------------------------+-------------------+
```

### Spacing Scale

```markdown
## Spacing Tokens

| Token | Value | Use For |
|-------|-------|---------|
| space-0 | 0px | Reset |
| space-1 | 4px | Tight grouping |
| space-2 | 8px | Related elements |
| space-3 | 12px | Form fields |
| space-4 | 16px | Default padding |
| space-5 | 24px | Section padding (mobile) |
| space-6 | 32px | Component gaps |
| space-8 | 48px | Section padding (tablet) |
| space-10 | 64px | Section padding (desktop) |
| space-12 | 96px | Large section breaks |
| space-16 | 128px | Hero padding |
```

### Spacing in Wireframes

```
SECTION SPACING

+------------------------------------------------------------------------+
|                              space-10 (64px)                           |
+------------------------------------------------------------------------+
|                                                                        |
|  Headline                                                              |
|                              space-4 (16px)                            |
|  Subheadline                                                           |
|                              space-6 (32px)                            |
|  +--------------------+  space-6  +--------------------+               |
|  |     Card 1         |<--------->|     Card 2         |               |
|  +--------------------+           +--------------------+               |
|                                                                        |
+------------------------------------------------------------------------+
|                              space-10 (64px)                           |
+------------------------------------------------------------------------+
```

---

## 9. Handoff-Ready Specification Format

### Complete Section Specification Template

```markdown
# Section: [Section Name]

## Overview
- **Purpose**: [Why this section exists]
- **Location**: [Where in page hierarchy]
- **Priority**: [P1-Critical, P2-Important, P3-Nice-to-have]

## Wireframe
```
[ASCII wireframe here]
```

## Grid & Layout
| Property | Value |
|----------|-------|
| Container | Constrained / Full-width |
| Max-width | 1280px |
| Columns | 12 |
| Column span | [specify per element] |
| Gutters | 24px |
| Padding (top/bottom) | 64px / 64px |

## Content Specifications
| Element | Type | Constraints | Required |
|---------|------|-------------|----------|
| Heading | h2 | 60 chars max | Yes |
| Description | p | 150 chars max | Yes |
| Image | img | 16:9, min 800px wide | Yes |
| CTA | button | 20 chars max | No |

## Components Used
| Component | Variant | Props |
|-----------|---------|-------|
| Button | primary, lg | onClick, children |
| Card | horizontal | image, title, description |

## Responsive Behavior
| Breakpoint | Behavior |
|------------|----------|
| xs-sm | Stack vertically, full-width elements |
| md | 2-column layout |
| lg+ | 3-column layout |

## Interaction States
| Element | Hover | Focus | Active |
|---------|-------|-------|--------|
| Card | Shadow increase, slight lift | Ring outline | Shadow decrease |
| CTA | Background darken | Ring outline | Scale 0.98 |

## Accessibility Requirements
| Requirement | Implementation |
|-------------|----------------|
| Landmark | <section aria-labelledby="[id]"> |
| Heading | h2 with unique id |
| Images | Alt text required |
| Focus order | Left to right, top to bottom |

## Design Notes
- [Any visual guidance without over-specifying]
- [Tone/feeling this section should convey]
- [References or inspirations if applicable]

## Implementation Notes
- [Technical considerations]
- [Performance requirements]
- [Third-party dependencies]
```

### Handoff Checklist

```markdown
## Specification Completeness Checklist

### Structure
- [ ] Page purpose and goals documented
- [ ] User entry/exit points identified
- [ ] Section hierarchy defined
- [ ] All sections have ASCII wireframes

### Visual
- [ ] Grid system specified
- [ ] Spacing tokens identified
- [ ] All breakpoints documented
- [ ] Component variants specified

### Content
- [ ] All text constraints defined
- [ ] Image specifications complete
- [ ] Placeholder content provided
- [ ] Character counts specified

### Interaction
- [ ] All states documented
- [ ] Transitions/animations noted
- [ ] Error states defined
- [ ] Loading states defined

### Accessibility
- [ ] Heading hierarchy mapped
- [ ] Landmarks identified
- [ ] Focus order specified
- [ ] ARIA requirements listed
- [ ] Screen reader text documented

### Technical
- [ ] Components mapped to design system
- [ ] Props/variants specified
- [ ] Responsive behavior defined
- [ ] Performance considerations noted
```

---

## 10. Common Page Wireframe Templates

### Homepage Template

```
+========================================================================+
| HEADER                                                                 |
| [Logo]  [Nav] [Nav] [Nav] [Nav]                    [Search] [CTA]     |
+========================================================================+

+------------------------------------------------------------------------+
| HERO SECTION                                                           |
+-----------------------------------+------------------------------------+
|                                   |                                    |
|   [Eyebrow]                       |       +--------------------+       |
|                                   |       |                    |       |
|   Main Headline                   |       |    Hero Image      |       |
|   Goes Here                       |       |    or Video        |       |
|                                   |       |                    |       |
|   Supporting subheadline that     |       +--------------------+       |
|   explains the value prop.        |                                    |
|                                   |                                    |
|   [Primary CTA]  [Secondary]      |                                    |
|                                   |                                    |
+-----------------------------------+------------------------------------+

+------------------------------------------------------------------------+
| SOCIAL PROOF / LOGOS                                                   |
| "Trusted by leading companies"                                         |
| [Logo] [Logo] [Logo] [Logo] [Logo] [Logo]                             |
+------------------------------------------------------------------------+

+------------------------------------------------------------------------+
| FEATURES SECTION                                                       |
|                                                                        |
|                    Section Headline                                    |
|                    Section subheadline                                 |
|                                                                        |
| +----------------------+ +----------------------+ +----------------------+
| |       [Icon]         | |       [Icon]         | |       [Icon]         |
| |                      | |                      | |                      |
| | Feature Title        | | Feature Title        | | Feature Title        |
| |                      | |                      | |                      |
| | Description text     | | Description text     | | Description text     |
| | goes here.           | | goes here.           | | goes here.           |
| |                      | |                      | |                      |
| | [Learn more ->]      | | [Learn more ->]      | | [Learn more ->]      |
| +----------------------+ +----------------------+ +----------------------+
|                                                                        |
+------------------------------------------------------------------------+

+------------------------------------------------------------------------+
| HOW IT WORKS / PROCESS                                                 |
|                                                                        |
|              How It Works                                              |
|                                                                        |
| +----------+           +----------+           +----------+             |
| |    1     |  ------>  |    2     |  ------>  |    3     |             |
| +----------+           +----------+           +----------+             |
|   Step One               Step Two              Step Three              |
|   Description            Description            Description            |
|                                                                        |
+------------------------------------------------------------------------+

+------------------------------------------------------------------------+
| TESTIMONIALS                                                           |
|                                                                        |
|                    What Our Customers Say                              |
|                                                                        |
| +------------------------------------------------------------------+   |
| |                                                                  |   |
| |   "Quote text from customer that highlights key benefits         |   |
| |    and builds trust with potential buyers."                      |   |
| |                                                                  |   |
| |   [Avatar]  Customer Name                                        |   |
| |             Title, Company                                       |   |
| |                                                                  |   |
| +------------------------------------------------------------------+   |
|                                                                        |
|                         [ o ] [ o ] [ o ]                              |
|                          (carousel dots)                               |
+------------------------------------------------------------------------+

+------------------------------------------------------------------------+
| CTA SECTION                                                            |
|                                                                        |
|                    Ready to Get Started?                               |
|                                                                        |
|              Take the next step with a compelling CTA                  |
|                                                                        |
|                      [Primary CTA Button]                              |
|                                                                        |
+------------------------------------------------------------------------+

+========================================================================+
| FOOTER                                                                 |
|                                                                        |
| [Logo]             Products    Resources    Company    Legal           |
|                    Link        Link         Link       Link            |
| Brief company      Link        Link         Link       Link            |
| description.       Link        Link         Link       Link            |
|                                                                        |
| [Social] [Social] [Social]                                             |
|                                                                        |
| (c) 2024 Company Name. All rights reserved.  [Privacy] [Terms]         |
+========================================================================+
```

### Product/Feature Page Template

```
+========================================================================+
| HEADER (consistent with homepage)                                      |
+========================================================================+

+------------------------------------------------------------------------+
| BREADCRUMB                                                             |
| Home > Products > [Product Name]                                       |
+------------------------------------------------------------------------+

+------------------------------------------------------------------------+
| PRODUCT HERO                                                           |
+-----------------------------------+------------------------------------+
|                                   |                                    |
|   [Category Badge]                |       +--------------------+       |
|                                   |       |                    |       |
|   Product Name                    |       |  Product Image/    |       |
|                                   |       |  Screenshot/       |       |
|   Brief description that          |       |  Video             |       |
|   explains the product and        |       |                    |       |
|   its main benefit.               |       +--------------------+       |
|                                   |                                    |
|   [Start Free Trial] [See Demo]   |                                    |
|                                   |                                    |
+-----------------------------------+------------------------------------+

+------------------------------------------------------------------------+
| KEY BENEFITS BAR                                                       |
|                                                                        |
| [Icon] Benefit 1  |  [Icon] Benefit 2  |  [Icon] Benefit 3            |
|                                                                        |
+------------------------------------------------------------------------+

+------------------------------------------------------------------------+
| FEATURE DETAILS (Alternating Layout)                                   |
|                                                                        |
+-----------------------------------+------------------------------------+
| +-----------------------------+   |                                    |
| |                             |   |   Feature Headline                 |
| |    [Feature Screenshot]     |   |                                    |
| |                             |   |   Detailed description of this     |
| +-----------------------------+   |   feature and how it helps users   |
|                                   |   accomplish their goals.          |
|                                   |                                    |
|                                   |   - Bullet point benefit           |
|                                   |   - Bullet point benefit           |
|                                   |   - Bullet point benefit           |
+-----------------------------------+------------------------------------+

+------------------------------------+-----------------------------------+
|                                    | +-----------------------------+   |
|   Feature Headline                 | |                             |   |
|                                    | |    [Feature Screenshot]     |   |
|   Detailed description of this     | |                             |   |
|   feature and how it helps users   | +-----------------------------+   |
|   accomplish their goals.          |                                   |
|                                    |                                   |
|   - Bullet point benefit           |                                   |
|   - Bullet point benefit           |                                   |
+------------------------------------+-----------------------------------+

+------------------------------------------------------------------------+
| COMPARISON TABLE (if applicable)                                       |
|                                                                        |
|              Compare Plans                                             |
|                                                                        |
| +----------------------------------------------------------------+     |
| | Feature        | Free      | Pro       | Enterprise             |     |
| +----------------------------------------------------------------+     |
| | Feature 1      | [check]   | [check]   | [check]                |     |
| | Feature 2      | [x]       | [check]   | [check]                |     |
| | Feature 3      | [x]       | [x]       | [check]                |     |
| | Price          | $0        | $29/mo    | Custom                 |     |
| +----------------------------------------------------------------+     |
|                                                                        |
+------------------------------------------------------------------------+

+------------------------------------------------------------------------+
| INTEGRATION / ECOSYSTEM                                                |
|                                                                        |
|              Works with your favorite tools                            |
|                                                                        |
| [App] [App] [App] [App] [App] [App] [App] [App]                       |
|                                                                        |
|                   [See all integrations ->]                            |
+------------------------------------------------------------------------+

+------------------------------------------------------------------------+
| FAQ SECTION                                                            |
|                                                                        |
|              Frequently Asked Questions                                |
|                                                                        |
| +------------------------------------------------------------------+   |
| | [+] Question text goes here?                                     |   |
| +------------------------------------------------------------------+   |
| | [-] Question text goes here?                                     |   |
| |     Answer text that expands when the question is clicked.       |   |
| |     Can contain multiple paragraphs if needed.                   |   |
| +------------------------------------------------------------------+   |
| | [+] Question text goes here?                                     |   |
| +------------------------------------------------------------------+   |
|                                                                        |
+------------------------------------------------------------------------+

+------------------------------------------------------------------------+
| BOTTOM CTA                                                             |
|                                                                        |
|              Ready to try [Product Name]?                              |
|                 Start your free trial today                            |
|                                                                        |
|              [Start Free Trial]  [Talk to Sales]                       |
+------------------------------------------------------------------------+

+========================================================================+
| FOOTER                                                                 |
+========================================================================+
```

### Dashboard/App Page Template

```
+========================================================================+
| TOP BAR                                                                |
| [Logo]        [Global Search]                   [Notif] [Help] [User]  |
+========================================================================+

+--------------------+---------------------------------------------------+
| SIDEBAR            | MAIN CONTENT AREA                                 |
|                    |                                                   |
| [Dashboard]        | PAGE HEADER                                       |
| [Analytics]        | Dashboard                    [Date Range] [Export]|
| [Projects]         |                                                   |
|   > Project A      +---------------------------------------------------+
|   > Project B      |                                                   |
| [Team]             | METRIC CARDS                                      |
| [Settings]         | +------------+ +------------+ +------------+      |
|                    | | [Icon]     | | [Icon]     | | [Icon]     |      |
| -----------        | |            | |            | |            |      |
|                    | | Metric A   | | Metric B   | | Metric C   |      |
| [Collapse <]       | | 12,345     | | $45,678    | | 89.2%      |      |
|                    | | +12.5%     | | -3.2%      | | +5.1%      |      |
|                    | +------------+ +------------+ +------------+      |
|                    |                                                   |
|                    +---------------------------------------------------+
|                    |                                                   |
|                    | MAIN CHART                                        |
|                    | +-----------------------------------------------+ |
|                    | |                                               | |
|                    | |     /\                                        | |
|                    | |    /  \      /\                               | |
|                    | |   /    \    /  \     /\                       | |
|                    | |  /      \  /    \   /  \                      | |
|                    | | /        \/      \ /    \___                  | |
|                    | |                                               | |
|                    | +-----------------------------------------------+ |
|                    | Jan  Feb  Mar  Apr  May  Jun  Jul  Aug          |
|                    |                                                   |
|                    +---------------------------------------------------+
|                    |                                                   |
|                    | DATA TABLE                                        |
|                    | +-----------------------------------------------+ |
|                    | | [Search]                          [Filter] v | |
|                    | +-----------------------------------------------+ |
|                    | | [ ] | Name     | Status  | Date    | Actions | |
|                    | +-----------------------------------------------+ |
|                    | | [ ] | Item 1   | Active  | Jan 15  | [...]   | |
|                    | | [ ] | Item 2   | Pending | Jan 14  | [...]   | |
|                    | | [ ] | Item 3   | Done    | Jan 13  | [...]   | |
|                    | +-----------------------------------------------+ |
|                    | | Page 1 of 10              [<] [1] [2] [3] [>]| |
|                    | +-----------------------------------------------+ |
|                    |                                                   |
+--------------------+---------------------------------------------------+
```

### Blog/Article Page Template

```
+========================================================================+
| HEADER                                                                 |
+========================================================================+

+------------------------------------------------------------------------+
| BREADCRUMB                                                             |
| Home > Blog > [Category] > [Article Title]                            |
+------------------------------------------------------------------------+

+---------------------------------------------------+--------------------+
| ARTICLE CONTENT                                   | SIDEBAR            |
|                                                   |                    |
| [Category Badge]                                  | AUTHOR             |
|                                                   | +----------------+ |
| Article Headline That Can                         | | [Avatar]       | |
| Span Multiple Lines                               | | Author Name    | |
|                                                   | | Brief bio      | |
| [Avatar] Author Name  |  Jan 15, 2024  |  8 min  | +----------------+ |
|                                                   |                    |
| +-----------------------------------------------+ | TABLE OF CONTENTS |
| |                                               | | +----------------+ |
| |              [Hero Image]                     | | | > Section 1    | |
| |                                               | | | > Section 2    | |
| +-----------------------------------------------+ | | > Section 3    | |
|                                                   | | > Section 4    | |
| Intro paragraph that hooks the reader and         | +----------------+ |
| provides context for the article. This should     |                    |
| be compelling and set expectations.               | NEWSLETTER         |
|                                                   | +----------------+ |
| ## Section Heading                                | | Subscribe for  | |
|                                                   | | weekly updates | |
| Body text paragraph that provides the main        | |                | |
| content. Can include multiple paragraphs,         | | [Email input]  | |
| lists, and other formatting as needed.            | | [Subscribe]    | |
|                                                   | +----------------+ |
| - Bullet point one                                |                    |
| - Bullet point two                                | RELATED POSTS      |
| - Bullet point three                              | +----------------+ |
|                                                   | | [Thumb] Title  | |
| > Blockquote text that highlights an              | +----------------+ |
| > important point or quote from a source.         | | [Thumb] Title  | |
|                                                   | +----------------+ |
| ## Another Section                                | | [Thumb] Title  | |
|                                                   | +----------------+ |
| More content with a code block:                   |                    |
|                                                   |                    |
| +-----------------------------------------------+ |                    |
| | code example {                                | |                    |
| |   property: value;                            | |                    |
| | }                                             | |                    |
| +-----------------------------------------------+ |                    |
|                                                   |                    |
| ## Conclusion                                     |                    |
|                                                   |                    |
| Summary paragraph that wraps up the article       |                    |
| and may include a call to action.                 |                    |
|                                                   |                    |
+---------------------------------------------------+--------------------+

+------------------------------------------------------------------------+
| SHARE & TAGS                                                           |
|                                                                        |
| Share: [Twitter] [LinkedIn] [Facebook] [Copy Link]                    |
|                                                                        |
| Tags: [Tag 1] [Tag 2] [Tag 3]                                         |
+------------------------------------------------------------------------+

+------------------------------------------------------------------------+
| AUTHOR BIO (expanded)                                                  |
|                                                                        |
| +------------------------------------------------------------------+   |
| | [Large Avatar]                                                   |   |
| |                                                                  |   |
| | About the Author                                                 |   |
| |                                                                  |   |
| | Author Name                                                      |   |
| | Full bio paragraph that describes the author's background,       |   |
| | expertise, and credentials. Links to social profiles.            |   |
| |                                                                  |   |
| | [Twitter] [LinkedIn] [Website]                                   |   |
| +------------------------------------------------------------------+   |
+------------------------------------------------------------------------+

+------------------------------------------------------------------------+
| RELATED ARTICLES                                                       |
|                                                                        |
|              You might also like                                       |
|                                                                        |
| +----------------------+ +----------------------+ +----------------------+
| | [Image]              | | [Image]              | | [Image]              |
| |                      | |                      | |                      |
| | Article Title        | | Article Title        | | Article Title        |
| |                      | |                      | |                      |
| | Brief excerpt...     | | Brief excerpt...     | | Brief excerpt...     |
| |                      | |                      | |                      |
| | [Read more ->]       | | [Read more ->]       | | [Read more ->]       |
| +----------------------+ +----------------------+ +----------------------+
+------------------------------------------------------------------------+

+------------------------------------------------------------------------+
| COMMENTS (if applicable)                                               |
|                                                                        |
| Comments (23)                                                          |
|                                                                        |
| +------------------------------------------------------------------+   |
| | [Avatar] User Name                              2 hours ago      |   |
| |                                                                  |   |
| | Comment text goes here. Can span multiple lines as needed.       |   |
| |                                                                  |   |
| | [Reply] [Like (5)]                                               |   |
| +------------------------------------------------------------------+   |
|                                                                        |
| +------------------------------------------------------------------+   |
| | [Your Avatar]                                                    |   |
| |                                                                  |   |
| | +--------------------------------------------------------------+ |   |
| | | Add a comment...                                             | |   |
| | +--------------------------------------------------------------+ |   |
| |                                               [Post Comment]     |   |
| +------------------------------------------------------------------+   |
+------------------------------------------------------------------------+

+========================================================================+
| FOOTER                                                                 |
+========================================================================+
```

### Contact/Form Page Template

```
+========================================================================+
| HEADER                                                                 |
+========================================================================+

+------------------------------------------------------------------------+
| PAGE HERO                                                              |
|                                                                        |
|                         Get in Touch                                   |
|                                                                        |
|              We'd love to hear from you. Send us a message             |
|              and we'll respond as soon as possible.                    |
|                                                                        |
+------------------------------------------------------------------------+

+------------------------------------------------------------------------+
| CONTACT OPTIONS                                                        |
|                                                                        |
| +--------------------+ +--------------------+ +--------------------+    |
| |      [Icon]        | |      [Icon]        | |      [Icon]        |    |
| |                    | |                    | |                    |    |
| |      Email         | |      Phone         | |      Office        |    |
| |  hello@company.com | |  +1 (555) 123-4567 | |  123 Main Street   |    |
| |                    | |  Mon-Fri 9am-5pm   | |  City, ST 12345    |    |
| +--------------------+ +--------------------+ +--------------------+    |
|                                                                        |
+------------------------------------------------------------------------+

+-----------------------------------+------------------------------------+
| CONTACT FORM                      | MAP / ADDITIONAL INFO              |
|                                   |                                    |
| Send us a message                 | +--------------------------------+ |
|                                   | |                                | |
| Full Name *                       | |         [Map Embed]            | |
| +-------------------------------+ | |                                | |
| | Your name                     | | |                                | |
| +-------------------------------+ | +--------------------------------+ |
|                                   |                                    |
| Email *                           | Office Hours                       |
| +-------------------------------+ |                                    |
| | your@email.com                | | Monday - Friday                   |
| +-------------------------------+ | 9:00 AM - 5:00 PM EST             |
|                                   |                                    |
| Phone                             | Saturday - Sunday                  |
| +-------------------------------+ | Closed                             |
| | (555) 123-4567                | |                                    |
| +-------------------------------+ | ---------------------------------- |
|                                   |                                    |
| Subject *                         | Follow Us                          |
| +-------------------------------+ |                                    |
| | Select a topic              v | | [Twitter] [LinkedIn] [Instagram]  |
| +-------------------------------+ |                                    |
|                                   |                                    |
| Message *                         |                                    |
| +-------------------------------+ |                                    |
| |                               | |                                    |
| |                               | |                                    |
| |                               | |                                    |
| |                               | |                                    |
| +-------------------------------+ |                                    |
|                                   |                                    |
| [ ] I agree to the privacy policy |                                    |
|                                   |                                    |
| +-------------------------------+ |                                    |
| |       [Send Message]          | |                                    |
| +-------------------------------+ |                                    |
|                                   |                                    |
+-----------------------------------+------------------------------------+

+------------------------------------------------------------------------+
| FAQ SECTION                                                            |
|                                                                        |
|                    Frequently Asked Questions                          |
|                                                                        |
| +------------------------------------------------------------------+   |
| | [+] How quickly will I receive a response?                       |   |
| +------------------------------------------------------------------+   |
| | [+] What information should I include?                           |   |
| +------------------------------------------------------------------+   |
| | [+] Can I schedule a call instead?                               |   |
| +------------------------------------------------------------------+   |
|                                                                        |
+------------------------------------------------------------------------+

+========================================================================+
| FOOTER                                                                 |
+========================================================================+
```

---

## Common Pitfalls

1. **Over-specification** - Prescribing exact pixels/colors instead of using tokens
2. **Missing states** - Documenting only default appearance
3. **Ignoring mobile** - Creating desktop-first without responsive specs
4. **Inconsistent naming** - Using different conventions across sections
5. **No accessibility** - Skipping ARIA and focus order documentation
6. **Vague content** - Using "Lorem ipsum" without character constraints
7. **Missing interactions** - Documenting static layouts without behaviors
8. **No component mapping** - Not linking wireframes to design system
9. **Skipping handoff details** - Missing implementation notes
10. **Version chaos** - No change history or version tracking

---

## Quality Checklist

Before marking a wireframe specification complete:

- [ ] ASCII wireframe provided for each section
- [ ] All breakpoints documented with behavior changes
- [ ] Component annotations with numbered callouts
- [ ] Interaction states for all interactive elements
- [ ] Heading hierarchy mapped (h1-h4)
- [ ] Focus order specified for keyboard navigation
- [ ] ARIA landmarks and attributes noted
- [ ] Content constraints (character counts) defined
- [ ] Grid columns and spacing tokens identified
- [ ] Handoff notes for implementation
- [ ] Version number and change history
- [ ] All sections reviewed for completeness
