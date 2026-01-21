---
skill: debugging-methodology
version: "1.0.0"
description: "Systematic debugging procedures for identifying and resolving issues efficiently"
used-by: ["@debugger", "@devops-controller", "@frontend-controller", "@backend-controller"]
---

# Debugging Methodology

## Overview

A systematic approach to debugging that minimizes time-to-resolution through structured investigation, proper tooling, and documented resolution patterns.

---

## Step-by-Step Procedures

### 1. Issue Triage (5-10 minutes)

#### Gather Context
1. **Reproduce the issue** - Confirm you can replicate it
2. **Identify scope** - Single user, all users, specific conditions?
3. **Check recent changes** - Review git log for recent deploys
4. **Review error logs** - Check application and server logs
5. **Note environment** - Production, staging, local? Browser? Device?

#### Severity Classification
| Level | Criteria | Response Time |
|-------|----------|---------------|
| P0 | System down, data loss | Immediate |
| P1 | Major feature broken | < 4 hours |
| P2 | Feature degraded | < 24 hours |
| P3 | Minor issue | Next sprint |

### 2. Systematic Investigation

#### Frontend Debugging

```typescript
// Enable verbose logging temporarily
const DEBUG = process.env.NODE_ENV === 'development'

function debugLog(context: string, data: unknown) {
  if (DEBUG) {
    console.group(`[DEBUG] ${context}`)
    console.log(JSON.stringify(data, null, 2))
    console.trace()
    console.groupEnd()
  }
}
```

#### Browser DevTools Checklist
1. **Console** - Check for errors, warnings, failed requests
2. **Network** - Verify API responses, check timing, inspect payloads
3. **Elements** - Inspect DOM state, computed styles
4. **Application** - Check localStorage, cookies, service workers
5. **Performance** - Profile if performance-related
6. **Sources** - Set breakpoints, step through code

#### Backend Debugging

```typescript
// Structured logging for debugging
import pino from 'pino'

const logger = pino({
  level: process.env.LOG_LEVEL || 'info',
  transport: {
    target: 'pino-pretty',
    options: { colorize: true }
  }
})

// Log request context
app.use((req, res, next) => {
  req.requestId = crypto.randomUUID()
  logger.info({
    requestId: req.requestId,
    method: req.method,
    url: req.url,
    userAgent: req.headers['user-agent']
  }, 'Incoming request')
  next()
})
```

### 3. Isolation Techniques

#### Binary Search Debugging
1. Identify the last known working state
2. Find the midpoint between working and broken
3. Test at midpoint
4. Narrow down to the breaking change

#### Git Bisect for Regression
```bash
git bisect start
git bisect bad HEAD
git bisect good v1.2.0
# Git will checkout commits for you to test
# Mark each as good or bad until found
git bisect reset
```

#### Environment Isolation
```bash
# Create isolated test environment
docker-compose -f docker-compose.debug.yml up

# Test with minimal dependencies
npm run dev -- --no-cache

# Clear all caches
rm -rf .next node_modules/.cache
npm run build
```

### 4. Common Issue Patterns

#### Memory Leaks
```typescript
// Detect memory leaks in Node.js
import v8 from 'v8'

function checkMemory() {
  const heap = v8.getHeapStatistics()
  console.log({
    totalHeap: `${(heap.total_heap_size / 1024 / 1024).toFixed(2)} MB`,
    usedHeap: `${(heap.used_heap_size / 1024 / 1024).toFixed(2)} MB`,
    heapLimit: `${(heap.heap_size_limit / 1024 / 1024).toFixed(2)} MB`
  })
}
```

#### Race Conditions
```typescript
// Add request deduplication
const pendingRequests = new Map<string, Promise<unknown>>()

async function deduplicatedFetch(key: string, fetcher: () => Promise<unknown>) {
  if (pendingRequests.has(key)) {
    return pendingRequests.get(key)
  }

  const promise = fetcher().finally(() => {
    pendingRequests.delete(key)
  })

  pendingRequests.set(key, promise)
  return promise
}
```

#### Hydration Mismatches (React/Next.js)
```typescript
// Suppress hydration warnings for dynamic content
const [mounted, setMounted] = useState(false)

useEffect(() => {
  setMounted(true)
}, [])

if (!mounted) return null // or skeleton
```

---

## Tool Configurations

### VS Code Debug Configuration
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Next.js",
      "type": "node",
      "request": "launch",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "skipFiles": ["<node_internals>/**"],
      "console": "integratedTerminal"
    },
    {
      "name": "Debug Jest Tests",
      "type": "node",
      "request": "launch",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "test", "--", "--runInBand"],
      "console": "integratedTerminal"
    }
  ]
}
```

---

## Decision Criteria

| Symptom | First Check | Tool |
|---------|-------------|------|
| Page not loading | Network tab, console | DevTools |
| Slow performance | Performance tab | Lighthouse |
| API errors | Network response | curl/Postman |
| Memory issues | Heap snapshot | Chrome Memory |
| Build failures | Build logs | Terminal |

---

## Common Pitfalls to Avoid

1. **Changing multiple things at once** - One change, test, repeat
2. **Not reproducing locally first** - Always reproduce before debugging
3. **Ignoring error messages** - Read the full stack trace
4. **Debugging production directly** - Use staging or local reproduction
5. **No documentation** - Document the fix for future reference
6. **Skipping root cause** - Fix the cause, not just symptoms
7. **Not checking recent deploys** - Most bugs are from recent changes

---

## Resolution Documentation Template

```markdown
## Bug Report: [Issue Title]

### Summary
Brief description of the issue

### Root Cause
Technical explanation of why it happened

### Resolution
What was changed to fix it

### Prevention
How to prevent similar issues

### Related Files
- path/to/affected/file.ts

### Commits
- abc1234 - Fix: description
```
