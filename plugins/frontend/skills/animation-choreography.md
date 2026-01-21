---
skill: animation-choreography
version: "1.0.0"
description: "GSAP and Framer Motion patterns for creating polished, performant UI animations"
used-by:
  - "@animation-engineer"
  - "@react-engineer"
  - "@page-builder"
  - "@frontend-controller"
---

# Animation Choreography

## Overview

This skill covers creating smooth, purposeful animations using GSAP (GreenSock) and Framer Motion. Focus is on performance, accessibility, and meaningful motion.

## Animation Principles

1. **Purpose** - Every animation should serve UX (feedback, orientation, delight)
2. **Performance** - Animate only transform and opacity when possible
3. **Timing** - Fast enough to feel responsive (150-300ms for micro-interactions)
4. **Easing** - Use natural easing curves, avoid linear
5. **Accessibility** - Respect `prefers-reduced-motion`

## GSAP Patterns

### Basic Timeline
```typescript
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';

function HeroSection() {
  const container = useRef<HTMLDivElement>(null);

  useGSAP(() => {
    const tl = gsap.timeline({ defaults: { ease: 'power3.out' } });

    tl.from('.hero-title', { y: 100, opacity: 0, duration: 0.8 })
      .from('.hero-subtitle', { y: 50, opacity: 0, duration: 0.6 }, '-=0.4')
      .from('.hero-cta', { scale: 0.9, opacity: 0, duration: 0.4 }, '-=0.2');
  }, { scope: container });

  return <div ref={container}>...</div>;
}
```

### Scroll-Triggered Animations
```typescript
import { ScrollTrigger } from 'gsap/ScrollTrigger';
gsap.registerPlugin(ScrollTrigger);

useGSAP(() => {
  gsap.from('.feature-card', {
    scrollTrigger: {
      trigger: '.features-section',
      start: 'top 80%',
      toggleActions: 'play none none reverse',
    },
    y: 60,
    opacity: 0,
    duration: 0.8,
    stagger: 0.15,
  });
}, { scope: container });
```

### Stagger Patterns
```typescript
// Grid reveal
gsap.from('.grid-item', {
  opacity: 0,
  y: 40,
  duration: 0.6,
  stagger: {
    each: 0.1,
    from: 'start', // 'end', 'center', 'edges', 'random'
    grid: [4, 3],  // for grid layouts
  },
});
```

## Framer Motion Patterns

### Component Variants
```tsx
import { motion, Variants } from 'framer-motion';

const cardVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: {
    opacity: 1,
    y: 0,
    transition: { duration: 0.4, ease: [0.25, 0.1, 0.25, 1] }
  },
  hover: {
    y: -8,
    boxShadow: '0 20px 40px rgba(0,0,0,0.1)',
    transition: { duration: 0.2 }
  },
};

function Card({ children }) {
  return (
    <motion.div
      variants={cardVariants}
      initial="hidden"
      animate="visible"
      whileHover="hover"
    >
      {children}
    </motion.div>
  );
}
```

### Staggered Children
```tsx
const containerVariants: Variants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1, delayChildren: 0.2 }
  }
};

const itemVariants: Variants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
};

function List({ items }) {
  return (
    <motion.ul variants={containerVariants} initial="hidden" animate="visible">
      {items.map(item => (
        <motion.li key={item.id} variants={itemVariants}>
          {item.name}
        </motion.li>
      ))}
    </motion.ul>
  );
}
```

### Layout Animations
```tsx
<motion.div layout layoutId="shared-element">
  {isExpanded ? <ExpandedView /> : <CollapsedView />}
</motion.div>
```

### Exit Animations (AnimatePresence)
```tsx
<AnimatePresence mode="wait">
  {isVisible && (
    <motion.div
      key="modal"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
    >
      <Modal />
    </motion.div>
  )}
</AnimatePresence>
```

## Timing Reference

| Interaction Type | Duration | Easing |
|------------------|----------|--------|
| Button feedback | 100-150ms | ease-out |
| Tooltip/popover | 150-200ms | ease-out |
| Modal open | 200-300ms | ease-out |
| Modal close | 150-200ms | ease-in |
| Page transition | 300-400ms | ease-in-out |
| Complex sequence | 600-1000ms | custom |

## Accessibility Implementation

```typescript
// Check for reduced motion preference
const prefersReducedMotion = window.matchMedia(
  '(prefers-reduced-motion: reduce)'
).matches;

// GSAP approach
gsap.config({
  autoSleep: 60,
  force3D: true,
});

if (prefersReducedMotion) {
  gsap.globalTimeline.timeScale(20); // Instant animations
}

// Framer Motion approach
const motionConfig = {
  transition: prefersReducedMotion
    ? { duration: 0 }
    : { duration: 0.4 }
};
```

## Performance Guidelines

1. **GPU-Accelerated Properties Only**
   - `transform` (translate, scale, rotate)
   - `opacity`
   - Avoid: `width`, `height`, `top`, `left`, `margin`, `padding`

2. **Will-Change Sparingly**
   ```css
   .will-animate { will-change: transform, opacity; }
   ```

3. **Debounce Scroll Handlers**
   - Use GSAP ScrollTrigger (handles this automatically)
   - Or implement requestAnimationFrame throttling

## Common Pitfalls

1. **Animating Layout Properties** - Causes expensive reflows; use transform instead
2. **Too Many Simultaneous Animations** - Limit to 3-5 concurrent animations
3. **Ignoring Reduced Motion** - Always implement accessibility fallbacks
4. **Overly Long Durations** - Keep interactions snappy; reserve long animations for cinematic moments
5. **No Exit Animations** - Elements should animate out, not just disappear
6. **Conflicting Animation Libraries** - Pick one library per project when possible
