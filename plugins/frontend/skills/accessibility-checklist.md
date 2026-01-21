---
skill: accessibility-checklist
version: "1.0.0"
description: "WCAG compliance verification procedures for ensuring accessible web interfaces"
used-by:
  - "@accessibility-auditor"
  - "@qa-controller"
  - "@react-engineer"
  - "@page-builder"
---

# Accessibility Checklist

## Overview

This skill provides procedures for verifying WCAG 2.1 AA compliance. Use this checklist during development and QA to ensure accessible experiences for all users.

## Quick Audit Procedure

### 1. Keyboard Navigation Test (5 min)
- [ ] Tab through entire page - logical order?
- [ ] All interactive elements focusable?
- [ ] Focus visible on all elements?
- [ ] No keyboard traps?
- [ ] Skip links present?
- [ ] Escape closes modals/dropdowns?

### 2. Screen Reader Test (10 min)
- [ ] Page has descriptive `<title>`
- [ ] Headings form logical hierarchy (h1 > h2 > h3)
- [ ] Images have alt text
- [ ] Form inputs have labels
- [ ] Buttons have accessible names
- [ ] ARIA landmarks present (main, nav, aside)
- [ ] Dynamic content announces changes

### 3. Visual Test (5 min)
- [ ] Color contrast passes (4.5:1 text, 3:1 UI)
- [ ] Information not conveyed by color alone
- [ ] Text resizes to 200% without breaking
- [ ] Focus indicators visible
- [ ] Animations respect reduced motion

## Semantic HTML Requirements

### Document Structure
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>Page Title - Site Name</title>
  <meta name="description" content="...">
</head>
<body>
  <a href="#main" class="skip-link">Skip to content</a>
  <header role="banner">...</header>
  <nav role="navigation" aria-label="Main">...</nav>
  <main id="main" role="main">...</main>
  <aside role="complementary">...</aside>
  <footer role="contentinfo">...</footer>
</body>
</html>
```

### Heading Hierarchy
```html
<!-- Correct -->
<h1>Page Title</h1>
  <h2>Section</h2>
    <h3>Subsection</h3>
  <h2>Another Section</h2>

<!-- Incorrect - skipped level -->
<h1>Page Title</h1>
  <h3>Subsection</h3> <!-- Missing h2 -->
```

## Form Accessibility

### Input Labels
```tsx
// Always associate labels with inputs
<div>
  <label htmlFor="email">Email address</label>
  <input
    id="email"
    type="email"
    aria-describedby="email-hint email-error"
  />
  <p id="email-hint">We'll never share your email</p>
  {error && <p id="email-error" role="alert">{error}</p>}
</div>
```

### Error Handling
```tsx
<form aria-describedby="form-errors">
  {errors.length > 0 && (
    <div id="form-errors" role="alert" aria-live="polite">
      <p>Please fix the following errors:</p>
      <ul>
        {errors.map(e => <li key={e.field}>{e.message}</li>)}
      </ul>
    </div>
  )}
</form>
```

### Required Fields
```tsx
<label htmlFor="name">
  Name <span aria-hidden="true">*</span>
  <span className="sr-only">(required)</span>
</label>
<input id="name" required aria-required="true" />
```

## Interactive Elements

### Buttons vs Links
```tsx
// Button = actions (submit, toggle, open modal)
<button onClick={handleSubmit}>Submit</button>

// Link = navigation (goes to URL)
<a href="/about">About Us</a>

// Never use div/span as buttons without proper ARIA
<div
  role="button"
  tabIndex={0}
  onClick={handler}
  onKeyDown={(e) => e.key === 'Enter' && handler()}
>
  Click me
</div>
```

### Icon Buttons
```tsx
// With visible text - hide icon from AT
<button>
  <Icon aria-hidden="true" />
  <span>Close</span>
</button>

// Icon only - provide accessible name
<button aria-label="Close dialog">
  <Icon aria-hidden="true" />
</button>
```

## ARIA Patterns

### Live Regions
```tsx
// Polite - waits for user to finish
<div aria-live="polite" aria-atomic="true">
  {statusMessage}
</div>

// Assertive - interrupts immediately (use sparingly)
<div role="alert" aria-live="assertive">
  {errorMessage}
</div>
```

### Modal Dialog
```tsx
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-description"
>
  <h2 id="modal-title">Confirm Action</h2>
  <p id="modal-description">Are you sure?</p>
  <button>Confirm</button>
  <button>Cancel</button>
</div>
```

### Tabs
```tsx
<div role="tablist" aria-label="Content tabs">
  <button
    role="tab"
    aria-selected={activeTab === 0}
    aria-controls="panel-0"
    id="tab-0"
  >
    Tab 1
  </button>
</div>
<div
  role="tabpanel"
  id="panel-0"
  aria-labelledby="tab-0"
  hidden={activeTab !== 0}
>
  Panel content
</div>
```

## Color & Contrast

### Minimum Ratios
| Element | Ratio Required |
|---------|---------------|
| Normal text (<18px) | 4.5:1 |
| Large text (>18px bold or >24px) | 3:1 |
| UI components & graphics | 3:1 |
| Focus indicators | 3:1 |

### Testing Tools
- Browser DevTools (Accessibility panel)
- WebAIM Contrast Checker
- Stark (Figma plugin)
- axe DevTools extension

## Focus Management

### Skip Link
```css
.skip-link {
  position: absolute;
  left: -9999px;
}

.skip-link:focus {
  left: 50%;
  transform: translateX(-50%);
  top: 1rem;
  z-index: 9999;
}
```

### Focus Trap (Modals)
```tsx
import { FocusTrap } from 'focus-trap-react';

<FocusTrap>
  <dialog>
    {/* Focus stays within dialog */}
  </dialog>
</FocusTrap>
```

## Common Pitfalls

1. **Missing Alt Text** - Every image needs alt (empty alt="" for decorative)
2. **Poor Focus Visibility** - Default outlines removed without replacement
3. **Auto-Playing Media** - Provide pause controls, respect reduced motion
4. **Form Without Labels** - Placeholders are not labels
5. **Click-Only Handlers** - Add keyboard handlers for custom controls
6. **Color-Only Information** - Add icons, text, or patterns
7. **Missing Page Language** - Always set `<html lang="en">`
8. **Inaccessible Custom Components** - Use established patterns or test thoroughly
