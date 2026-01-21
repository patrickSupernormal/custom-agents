---
skill: component-architecture
version: "1.0.0"
description: "Patterns for building reusable, maintainable React components with proper composition and separation of concerns"
used-by:
  - "@react-engineer"
  - "@component-builder"
  - "@page-builder"
  - "@frontend-controller"
---

# Component Architecture Patterns

## Overview

This skill defines the standard patterns for building React components that are reusable, testable, and maintainable across projects.

## Component Classification

### 1. Primitive Components (Atoms)
- Single responsibility, no business logic
- Examples: Button, Input, Icon, Text, Box
- Accept style variants via props
- Forward refs for DOM access

### 2. Composite Components (Molecules)
- Combine 2-5 primitives
- Examples: FormField, Card, SearchInput
- May contain minimal local state
- No API calls or global state access

### 3. Feature Components (Organisms)
- Complete UI sections with logic
- Examples: Header, ProductCard, CommentThread
- Can connect to state management
- May fetch data (with loading/error states)

### 4. Page Components
- Route-level components
- Orchestrate features and layout
- Handle page-level data fetching
- Manage meta tags and SEO

## Standard Component Structure

```tsx
// ComponentName/index.tsx
export { ComponentName } from './ComponentName';
export type { ComponentNameProps } from './ComponentName.types';

// ComponentName/ComponentName.tsx
import { forwardRef } from 'react';
import { cn } from '@/lib/utils';
import type { ComponentNameProps } from './ComponentName.types';
import styles from './ComponentName.module.css';

export const ComponentName = forwardRef<HTMLDivElement, ComponentNameProps>(
  ({ className, variant = 'default', children, ...props }, ref) => {
    return (
      <div
        ref={ref}
        className={cn(styles.root, styles[variant], className)}
        {...props}
      >
        {children}
      </div>
    );
  }
);

ComponentName.displayName = 'ComponentName';

// ComponentName/ComponentName.types.ts
export interface ComponentNameProps {
  variant?: 'default' | 'primary' | 'secondary';
  className?: string;
  children?: React.ReactNode;
}
```

## Composition Patterns

### Compound Components
```tsx
const Card = ({ children }) => <div className="card">{children}</div>;
Card.Header = ({ children }) => <div className="card-header">{children}</div>;
Card.Body = ({ children }) => <div className="card-body">{children}</div>;
Card.Footer = ({ children }) => <div className="card-footer">{children}</div>;

// Usage
<Card>
  <Card.Header>Title</Card.Header>
  <Card.Body>Content</Card.Body>
</Card>
```

### Render Props
```tsx
<DataFetcher url="/api/users">
  {({ data, loading, error }) =>
    loading ? <Spinner /> : <UserList users={data} />
  }
</DataFetcher>
```

### Polymorphic Components
```tsx
interface BoxProps<T extends ElementType> {
  as?: T;
  children?: ReactNode;
}

function Box<T extends ElementType = 'div'>({
  as,
  children,
  ...props
}: BoxProps<T> & ComponentPropsWithoutRef<T>) {
  const Component = as || 'div';
  return <Component {...props}>{children}</Component>;
}
```

## Decision Criteria

| Question | If Yes | If No |
|----------|--------|-------|
| Used in 3+ places? | Extract to shared | Keep inline |
| Has complex state? | Consider hooks extraction | Keep in component |
| Needs testing isolation? | Separate logic from UI | Co-locate |
| Cross-feature usage? | Move to shared/components | Keep in feature |

## Common Pitfalls

1. **Prop Drilling** - Use composition or context instead of passing props through 5+ levels
2. **Mega Components** - Split when component exceeds 200 lines
3. **Premature Abstraction** - Wait for 3 uses before extracting
4. **Implicit Dependencies** - Make all dependencies explicit via props or imports
5. **Mixed Concerns** - Keep data fetching separate from presentation
6. **Missing Display Names** - Always set for forwardRef components (helps debugging)
7. **Over-memoization** - Only memo when you've measured performance issues
