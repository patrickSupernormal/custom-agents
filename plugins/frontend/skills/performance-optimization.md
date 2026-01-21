---
skill: performance-optimization
version: "1.0.0"
description: "Core Web Vitals optimization and bundle size reduction techniques"
used-by:
  - "@performance-engineer"
  - "@react-engineer"
  - "@qa-controller"
  - "@frontend-controller"
---

# Performance Optimization

## Overview

This skill covers techniques for optimizing Core Web Vitals (LCP, FID/INP, CLS) and reducing JavaScript bundle sizes for fast-loading web applications.

## Core Web Vitals Targets

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP (Largest Contentful Paint) | < 2.5s | 2.5s - 4s | > 4s |
| INP (Interaction to Next Paint) | < 200ms | 200ms - 500ms | > 500ms |
| CLS (Cumulative Layout Shift) | < 0.1 | 0.1 - 0.25 | > 0.25 |

## LCP Optimization

### Priority Loading
```tsx
// Mark hero image as priority
import Image from 'next/image';

<Image
  src="/hero.jpg"
  alt="Hero"
  priority
  fetchPriority="high"
  sizes="100vw"
/>
```

### Preload Critical Resources
```html
<head>
  <!-- Preload LCP image -->
  <link rel="preload" as="image" href="/hero.webp" />

  <!-- Preload critical font -->
  <link
    rel="preload"
    as="font"
    href="/fonts/inter.woff2"
    type="font/woff2"
    crossorigin
  />

  <!-- Preconnect to CDN -->
  <link rel="preconnect" href="https://cdn.example.com" />
</head>
```

### Optimize Server Response
```typescript
// Next.js - use ISR for cached responses
export async function generateStaticParams() {
  return [{ slug: 'home' }, { slug: 'about' }];
}

export const revalidate = 3600; // Revalidate every hour
```

## CLS Prevention

### Reserve Space for Images
```tsx
// Always provide dimensions
<Image
  src="/product.jpg"
  alt="Product"
  width={400}
  height={300}
  className="w-full h-auto"
/>

// Or use aspect ratio
<div className="aspect-video relative">
  <Image src="/video-thumb.jpg" fill alt="..." />
</div>
```

### Font Loading Strategy
```css
/* Use font-display: swap with fallback sizing */
@font-face {
  font-family: 'Inter';
  src: url('/fonts/inter.woff2') format('woff2');
  font-display: swap;
  size-adjust: 100%;
  ascent-override: 90%;
  descent-override: 20%;
}
```

### Skeleton Placeholders
```tsx
function ProductCard({ product, isLoading }) {
  if (isLoading) {
    return (
      <div className="animate-pulse">
        <div className="aspect-square bg-gray-200 rounded" />
        <div className="h-4 bg-gray-200 rounded mt-4 w-3/4" />
        <div className="h-4 bg-gray-200 rounded mt-2 w-1/2" />
      </div>
    );
  }
  return <ActualProductCard product={product} />;
}
```

## INP/Responsiveness

### Defer Non-Critical Work
```typescript
// Use requestIdleCallback for non-urgent tasks
function trackAnalytics(event: AnalyticsEvent) {
  if ('requestIdleCallback' in window) {
    requestIdleCallback(() => sendToAnalytics(event));
  } else {
    setTimeout(() => sendToAnalytics(event), 0);
  }
}
```

### Optimize Event Handlers
```typescript
// Debounce expensive handlers
import { useDebouncedCallback } from 'use-debounce';

function SearchInput() {
  const handleSearch = useDebouncedCallback((value: string) => {
    performSearch(value);
  }, 300);

  return <input onChange={(e) => handleSearch(e.target.value)} />;
}
```

### Use Transitions for Non-Urgent Updates
```typescript
import { useTransition } from 'react';

function FilteredList() {
  const [isPending, startTransition] = useTransition();

  const handleFilter = (filter: string) => {
    startTransition(() => {
      setFilter(filter); // Low priority update
    });
  };
}
```

## Bundle Optimization

### Code Splitting
```typescript
// Route-level splitting (automatic in Next.js)
// Component-level splitting
import dynamic from 'next/dynamic';

const HeavyChart = dynamic(() => import('./HeavyChart'), {
  loading: () => <ChartSkeleton />,
  ssr: false, // Skip SSR for client-only components
});
```

### Tree Shaking Imports
```typescript
// Bad - imports entire library
import _ from 'lodash';
_.debounce(fn, 300);

// Good - imports only what's needed
import debounce from 'lodash/debounce';
debounce(fn, 300);

// Best - use native or smaller alternative
const debounce = (fn, ms) => {
  let timeout;
  return (...args) => {
    clearTimeout(timeout);
    timeout = setTimeout(() => fn(...args), ms);
  };
};
```

### Analyze Bundle Size
```bash
# Next.js bundle analyzer
npm install @next/bundle-analyzer

# next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true',
});
module.exports = withBundleAnalyzer(nextConfig);

# Run analysis
ANALYZE=true npm run build
```

## Image Optimization

### Format Selection
```tsx
// Next.js handles format automatically
<Image src="/photo.jpg" alt="..." /> // Serves WebP/AVIF when supported

// Manual picture element
<picture>
  <source srcSet="/photo.avif" type="image/avif" />
  <source srcSet="/photo.webp" type="image/webp" />
  <img src="/photo.jpg" alt="..." />
</picture>
```

### Responsive Sizes
```tsx
<Image
  src="/hero.jpg"
  alt="Hero"
  fill
  sizes="
    (max-width: 640px) 100vw,
    (max-width: 1024px) 75vw,
    50vw
  "
/>
```

## Caching Strategy

```typescript
// next.config.js
module.exports = {
  async headers() {
    return [
      {
        source: '/_next/static/:path*',
        headers: [
          { key: 'Cache-Control', value: 'public, max-age=31536000, immutable' }
        ],
      },
      {
        source: '/images/:path*',
        headers: [
          { key: 'Cache-Control', value: 'public, max-age=86400, stale-while-revalidate=604800' }
        ],
      },
    ];
  },
};
```

## Measurement Tools

1. **Lighthouse** - Run in Chrome DevTools (Incognito mode)
2. **PageSpeed Insights** - Real user data from CrUX
3. **WebPageTest** - Detailed waterfall analysis
4. **Chrome DevTools Performance** - Runtime analysis

## Audit Procedure

1. Run Lighthouse audit (mobile, throttled)
2. Identify LCP element - optimize its loading
3. Check CLS sources in DevTools Performance panel
4. Profile interactions for INP issues
5. Analyze bundle with webpack-bundle-analyzer
6. Test on real devices (not just DevTools throttling)

## Common Pitfalls

1. **Unoptimized Images** - Always use next/image or optimize manually
2. **Render-Blocking Resources** - Defer non-critical CSS/JS
3. **Layout Shift from Ads** - Reserve space for dynamic content
4. **Hydration Mismatch** - Causes full re-render, hurting INP
5. **Over-fetching Data** - Only load what's needed for initial view
6. **No Caching Headers** - Configure proper cache-control
7. **Third-Party Script Bloat** - Audit and lazy-load analytics/chat widgets
