---
skill: performance-profiling
version: "1.0.0"
description: "Performance optimization through Lighthouse audits, bundle analysis, and systematic profiling"
used-by: ["@performance-engineer", "@devops-controller", "@frontend-controller", "@qa-controller"]
---

# Performance Profiling

## Overview

This skill covers systematic performance profiling and optimization, including Lighthouse audits, bundle analysis, runtime profiling, and Core Web Vitals optimization.

---

## Step-by-Step Procedures

### 1. Lighthouse Audit Setup

#### CLI Automation
```bash
# Install Lighthouse
npm install -g lighthouse

# Run audit with JSON output
lighthouse https://example.com \
  --output=json \
  --output-path=./lighthouse-report.json \
  --chrome-flags="--headless"

# Run specific categories
lighthouse https://example.com \
  --only-categories=performance,accessibility,best-practices,seo
```

#### CI Integration
```yaml
# .github/workflows/lighthouse.yml
name: Lighthouse CI
on: [push]

jobs:
  lighthouse:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci && npm run build

      - name: Run Lighthouse
        uses: treosh/lighthouse-ci-action@v10
        with:
          urls: |
            http://localhost:3000
            http://localhost:3000/about
          budgetPath: ./lighthouse-budget.json
          uploadArtifacts: true
          temporaryPublicStorage: true
```

#### Performance Budget
```json
// lighthouse-budget.json
[
  {
    "path": "/*",
    "timings": [
      { "metric": "first-contentful-paint", "budget": 1500 },
      { "metric": "largest-contentful-paint", "budget": 2500 },
      { "metric": "cumulative-layout-shift", "budget": 0.1 },
      { "metric": "total-blocking-time", "budget": 300 }
    ],
    "resourceSizes": [
      { "resourceType": "script", "budget": 300 },
      { "resourceType": "total", "budget": 500 }
    ]
  }
]
```

### 2. Bundle Analysis

#### Next.js Bundle Analyzer Setup
```javascript
// next.config.js
const withBundleAnalyzer = require('@next/bundle-analyzer')({
  enabled: process.env.ANALYZE === 'true'
})

module.exports = withBundleAnalyzer({
  // your config
})
```

```bash
# Run bundle analysis
ANALYZE=true npm run build
```

#### Bundle Size Monitoring
```typescript
// scripts/check-bundle-size.ts
import { readFileSync, readdirSync } from 'fs'
import { join } from 'path'

const MAX_BUNDLE_SIZE = 300 * 1024 // 300KB

function checkBundleSizes(buildDir: string) {
  const jsFiles = readdirSync(join(buildDir, 'static/chunks'))
    .filter(f => f.endsWith('.js'))

  const issues: string[] = []

  for (const file of jsFiles) {
    const filePath = join(buildDir, 'static/chunks', file)
    const stats = readFileSync(filePath)

    if (stats.length > MAX_BUNDLE_SIZE) {
      issues.push(`${file}: ${(stats.length / 1024).toFixed(2)}KB exceeds limit`)
    }
  }

  if (issues.length > 0) {
    console.error('Bundle size violations:')
    issues.forEach(i => console.error(`  - ${i}`))
    process.exit(1)
  }

  console.log('All bundles within size limits')
}

checkBundleSizes('.next')
```

### 3. Runtime Profiling

#### React Profiler Integration
```typescript
import { Profiler, ProfilerOnRenderCallback } from 'react'

const onRenderCallback: ProfilerOnRenderCallback = (
  id,
  phase,
  actualDuration,
  baseDuration,
  startTime,
  commitTime
) => {
  // Log slow renders
  if (actualDuration > 16) { // > 1 frame at 60fps
    console.warn(`Slow render: ${id}`, {
      phase,
      actualDuration: `${actualDuration.toFixed(2)}ms`,
      baseDuration: `${baseDuration.toFixed(2)}ms`
    })
  }
}

export function ProfiledComponent({ children }: { children: React.ReactNode }) {
  return (
    <Profiler id="App" onRender={onRenderCallback}>
      {children}
    </Profiler>
  )
}
```

#### Server-Side Timing
```typescript
// Measure API endpoint performance
import { performance } from 'perf_hooks'

export function withTiming<T>(
  fn: () => Promise<T>,
  label: string
): Promise<T> {
  const start = performance.now()

  return fn().finally(() => {
    const duration = performance.now() - start
    console.log(`[PERF] ${label}: ${duration.toFixed(2)}ms`)
  })
}

// Usage
const data = await withTiming(
  () => db.users.findMany(),
  'Database query'
)
```

### 4. Core Web Vitals Optimization

#### LCP (Largest Contentful Paint)
```typescript
// Prioritize critical resources
import Image from 'next/image'

export function HeroImage() {
  return (
    <Image
      src="/hero.jpg"
      alt="Hero"
      width={1200}
      height={600}
      priority // Preload this image
      sizes="100vw"
    />
  )
}
```

#### CLS (Cumulative Layout Shift)
```css
/* Reserve space for images */
.image-container {
  aspect-ratio: 16 / 9;
  width: 100%;
}

/* Reserve space for dynamic content */
.skeleton {
  min-height: 200px;
  background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}
```

#### INP (Interaction to Next Paint)
```typescript
// Defer non-critical work
import { startTransition } from 'react'

function handleClick() {
  // Immediate feedback
  setIsLoading(true)

  // Defer expensive update
  startTransition(() => {
    setExpensiveState(computeExpensiveValue())
  })
}

// Use web workers for heavy computation
const worker = new Worker('/workers/compute.js')
worker.postMessage(data)
worker.onmessage = (e) => setResult(e.data)
```

### 5. Performance Monitoring

#### Real User Monitoring (RUM)
```typescript
// Report Web Vitals to analytics
import { onCLS, onINP, onLCP, onFCP, onTTFB } from 'web-vitals'

function sendToAnalytics(metric: Metric) {
  const body = JSON.stringify({
    name: metric.name,
    value: metric.value,
    rating: metric.rating,
    delta: metric.delta,
    id: metric.id
  })

  navigator.sendBeacon('/api/vitals', body)
}

onCLS(sendToAnalytics)
onINP(sendToAnalytics)
onLCP(sendToAnalytics)
onFCP(sendToAnalytics)
onTTFB(sendToAnalytics)
```

---

## Decision Criteria

| Metric | Good | Needs Improvement | Poor |
|--------|------|-------------------|------|
| LCP | < 2.5s | 2.5s - 4s | > 4s |
| INP | < 200ms | 200ms - 500ms | > 500ms |
| CLS | < 0.1 | 0.1 - 0.25 | > 0.25 |
| FCP | < 1.8s | 1.8s - 3s | > 3s |
| TTFB | < 800ms | 800ms - 1800ms | > 1800ms |

---

## Common Pitfalls to Avoid

1. **No image optimization** - Always use next/image or optimized formats
2. **Blocking third-party scripts** - Load analytics/ads asynchronously
3. **Large JavaScript bundles** - Code split aggressively
4. **No caching strategy** - Implement proper cache headers
5. **Unoptimized fonts** - Use font-display: swap, preload critical fonts
6. **Missing preconnect** - Preconnect to critical third-party origins
7. **Measuring only in dev** - Production builds behave differently

---

## Validation Checklist

- [ ] Lighthouse score > 90 for performance
- [ ] All Core Web Vitals in "Good" range
- [ ] Bundle size within budget
- [ ] Images optimized and lazy-loaded
- [ ] Fonts optimized with proper loading strategy
- [ ] Third-party scripts loaded asynchronously
- [ ] Cache headers properly configured
- [ ] RUM collecting real user data
- [ ] Performance regression tests in CI
- [ ] No layout shifts on page load
