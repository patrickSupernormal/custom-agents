---
skill: design-token-implementation
version: "1.0.0"
description: "Converting design specifications into structured code tokens for consistent styling"
used-by:
  - "@design-token-engineer"
  - "@style-system-architect"
  - "@frontend-controller"
  - "@setup-dev-foundation"
---

# Design Token Implementation

## Overview

Design tokens are the atomic values that define a design system: colors, typography, spacing, shadows, and more. This skill covers extracting tokens from design specs and implementing them in code.

## Token Categories

### 1. Color Tokens
```css
/* primitives (raw values) */
--color-blue-500: #3b82f6;
--color-gray-900: #111827;

/* semantic (purpose-based) */
--color-primary: var(--color-blue-500);
--color-text-primary: var(--color-gray-900);
--color-background: var(--color-white);

/* component-specific */
--button-bg-primary: var(--color-primary);
--button-text-primary: var(--color-white);
```

### 2. Typography Tokens
```css
/* Font families */
--font-sans: 'Inter', system-ui, sans-serif;
--font-mono: 'JetBrains Mono', monospace;

/* Font sizes (using fluid scaling) */
--text-xs: clamp(0.75rem, 0.7rem + 0.25vw, 0.875rem);
--text-sm: clamp(0.875rem, 0.8rem + 0.35vw, 1rem);
--text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
--text-lg: clamp(1.125rem, 1rem + 0.6vw, 1.25rem);
--text-xl: clamp(1.25rem, 1.1rem + 0.75vw, 1.5rem);

/* Line heights */
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.75;

/* Font weights */
--font-normal: 400;
--font-medium: 500;
--font-semibold: 600;
--font-bold: 700;
```

### 3. Spacing Tokens
```css
/* Base unit: 4px */
--space-1: 0.25rem;  /* 4px */
--space-2: 0.5rem;   /* 8px */
--space-3: 0.75rem;  /* 12px */
--space-4: 1rem;     /* 16px */
--space-6: 1.5rem;   /* 24px */
--space-8: 2rem;     /* 32px */
--space-12: 3rem;    /* 48px */
--space-16: 4rem;    /* 64px */
--space-24: 6rem;    /* 96px */
```

### 4. Shadow Tokens
```css
--shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
--shadow-md: 0 4px 6px -1px rgb(0 0 0 / 0.1);
--shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1);
--shadow-xl: 0 20px 25px -5px rgb(0 0 0 / 0.1);
```

### 5. Animation Tokens
```css
--duration-fast: 150ms;
--duration-normal: 300ms;
--duration-slow: 500ms;

--ease-in: cubic-bezier(0.4, 0, 1, 1);
--ease-out: cubic-bezier(0, 0, 0.2, 1);
--ease-in-out: cubic-bezier(0.4, 0, 0.2, 1);
--ease-bounce: cubic-bezier(0.68, -0.55, 0.265, 1.55);
```

## Implementation Procedure

### Step 1: Extract from Design Specs
1. Open design file (Figma/Sketch)
2. Locate the design system/styles panel
3. Export color styles, text styles, effects
4. Document any undocumented values in use

### Step 2: Create Token Structure
```
src/
  styles/
    tokens/
      colors.css
      typography.css
      spacing.css
      shadows.css
      animations.css
      index.css      # imports all token files
    globals.css      # imports tokens + base styles
```

### Step 3: Implement Dark Mode
```css
:root {
  --color-bg: var(--color-white);
  --color-text: var(--color-gray-900);
}

[data-theme="dark"] {
  --color-bg: var(--color-gray-900);
  --color-text: var(--color-gray-100);
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --color-bg: var(--color-gray-900);
    --color-text: var(--color-gray-100);
  }
}
```

### Step 4: TypeScript Integration
```typescript
// tokens.ts
export const colors = {
  primary: 'var(--color-primary)',
  secondary: 'var(--color-secondary)',
} as const;

export const spacing = {
  1: 'var(--space-1)',
  2: 'var(--space-2)',
  // ...
} as const;

// Type-safe token access
type ColorToken = keyof typeof colors;
type SpacingToken = keyof typeof spacing;
```

## Decision Criteria

| Scenario | Approach |
|----------|----------|
| Value used once | Inline, no token |
| Value used 2-3 times | Consider token |
| Value used 4+ times | Definitely token |
| Brand colors | Always token |
| Spacing | Always token |
| One-off animation | Inline is fine |

## Common Pitfalls

1. **Too Many Tokens** - Not every value needs a token; creates maintenance burden
2. **Inconsistent Naming** - Use consistent prefixes: `color-`, `text-`, `space-`
3. **Missing Semantic Layer** - Always add semantic tokens between primitives and components
4. **Hard-coded Values** - Audit regularly for magic numbers that should be tokens
5. **No Dark Mode Plan** - Design token architecture with themes in mind from the start
6. **Forgetting Fallbacks** - Always provide fallback values for CSS custom properties
