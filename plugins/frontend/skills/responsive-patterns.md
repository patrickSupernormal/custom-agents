---
skill: responsive-patterns
version: "1.0.0"
description: "Mobile-first responsive design techniques using modern CSS and strategic breakpoints"
used-by:
  - "@react-engineer"
  - "@page-builder"
  - "@style-system-architect"
  - "@frontend-controller"
---

# Responsive Design Patterns

## Overview

This skill covers mobile-first responsive design using modern CSS features like container queries, fluid typography, and strategic breakpoint management.

## Breakpoint Strategy

### Standard Breakpoints
```css
/* Mobile-first breakpoints */
--bp-sm: 640px;   /* Large phones */
--bp-md: 768px;   /* Tablets */
--bp-lg: 1024px;  /* Small laptops */
--bp-xl: 1280px;  /* Desktops */
--bp-2xl: 1536px; /* Large screens */

/* Usage (mobile-first = min-width) */
@media (min-width: 768px) { /* md and up */ }
@media (min-width: 1024px) { /* lg and up */ }
```

### Tailwind Integration
```tsx
// Mobile-first classes
<div className="
  px-4 py-6           /* mobile default */
  md:px-8 md:py-12    /* tablet */
  lg:px-16 lg:py-20   /* desktop */
">
```

## Fluid Typography

### Clamp-Based Scaling
```css
/* Formula: clamp(min, preferred, max) */
/* Preferred = viewport-based calculation */

:root {
  --text-base: clamp(1rem, 0.9rem + 0.5vw, 1.125rem);
  --text-lg: clamp(1.125rem, 1rem + 0.75vw, 1.5rem);
  --text-xl: clamp(1.5rem, 1.2rem + 1.5vw, 2.5rem);
  --text-2xl: clamp(2rem, 1.5rem + 2.5vw, 4rem);
  --text-display: clamp(2.5rem, 2rem + 4vw, 6rem);
}

h1 { font-size: var(--text-display); }
h2 { font-size: var(--text-2xl); }
p { font-size: var(--text-base); }
```

## Container Queries

### Setup
```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

@container card (min-width: 400px) {
  .card {
    display: grid;
    grid-template-columns: 200px 1fr;
  }
}

@container card (min-width: 600px) {
  .card {
    grid-template-columns: 300px 1fr;
  }
}
```

### React Implementation
```tsx
function ResponsiveCard() {
  return (
    <div className="@container">
      <div className="
        flex flex-col
        @md:flex-row @md:gap-6
        @lg:gap-8
      ">
        <Image className="@md:w-1/3" />
        <Content className="@md:w-2/3" />
      </div>
    </div>
  );
}
```

## Layout Patterns

### Responsive Grid
```css
.auto-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(300px, 100%), 1fr));
  gap: var(--space-6);
}
```

### Flexible Sidebar
```css
.sidebar-layout {
  display: grid;
  grid-template-columns: 1fr;
}

@media (min-width: 1024px) {
  .sidebar-layout {
    grid-template-columns: 280px 1fr;
  }
}
```

### Stack to Row
```tsx
<div className="flex flex-col md:flex-row md:items-center gap-4">
  <Logo />
  <Navigation />
  <Actions />
</div>
```

## Responsive Images

### Picture Element
```tsx
<picture>
  <source
    media="(min-width: 1024px)"
    srcSet="/hero-desktop.webp"
    type="image/webp"
  />
  <source
    media="(min-width: 640px)"
    srcSet="/hero-tablet.webp"
    type="image/webp"
  />
  <img
    src="/hero-mobile.jpg"
    alt="Hero image"
    className="w-full h-auto"
  />
</picture>
```

### Next.js Image
```tsx
<Image
  src="/hero.jpg"
  alt="Hero"
  fill
  sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
  className="object-cover"
/>
```

## Touch-Friendly Targets

```css
/* Minimum 44x44px touch targets */
.touch-target {
  min-height: 44px;
  min-width: 44px;
  padding: 12px 16px;
}

/* Increase spacing on touch devices */
@media (pointer: coarse) {
  .nav-links {
    gap: 1rem;
  }

  .button {
    padding: 14px 24px;
  }
}
```

## Decision Criteria

| Scenario | Approach |
|----------|----------|
| Typography scaling | Use fluid clamp() |
| Component-level responsiveness | Container queries |
| Page layout changes | Media queries |
| Image optimization | Picture element + srcset |
| Hiding/showing elements | Prefer layout shifts over display:none |

## Testing Procedure

1. **Device Testing Order**
   - iPhone SE (375px) - smallest common viewport
   - iPhone 14 (390px)
   - iPad Mini (768px)
   - iPad Pro (1024px)
   - MacBook (1440px)
   - Large desktop (1920px)

2. **Orientation Testing**
   - Test landscape on tablets
   - Check modal/overlay behavior

3. **Content Testing**
   - Test with long text strings
   - Test with missing images
   - Test with minimal content

## Common Pitfalls

1. **Desktop-First CSS** - Always start mobile-first; it's easier to add than subtract
2. **Too Many Breakpoints** - 3-4 breakpoints suffice for most layouts
3. **Fixed Pixel Widths** - Use percentages, fr units, or clamp() instead
4. **Ignoring Orientation** - Landscape phones need different treatment
5. **Small Touch Targets** - Minimum 44x44px for tappable elements
6. **Overflow Issues** - Test with long words, large images at every breakpoint
7. **Hover-Only Interactions** - Always provide touch/focus alternatives
