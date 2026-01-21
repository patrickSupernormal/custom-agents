---
skill: rapid-prototyping
version: "1.0.0"
description: "Quick MVP development patterns for validating ideas with minimal code"
used-by: ["@prototype-builder", "@full-stack-engineer", "@startup-advisor", "@product-developer"]
---

# Rapid Prototyping Skill

## Overview
Patterns and techniques for building functional prototypes quickly, focusing on core value demonstration over production quality.

## Prototyping Philosophy

### Core Principles
1. **Working > Perfect** - Ship something testable
2. **Fake what you can** - Mock expensive features
3. **Steal patterns** - Use existing templates/boilerplates
4. **Delete later** - Technical debt is acceptable

### Time Budget Guidelines
| Prototype Type | Time Budget | Fidelity |
|---------------|-------------|----------|
| UI mockup | 2-4 hours | Visual only |
| Clickable prototype | 4-8 hours | Navigation works |
| Functional MVP | 1-2 days | Core feature works |
| Testable product | 3-5 days | Happy path complete |

## Quick Start Templates

### Next.js Full-Stack (Fastest Path)
```bash
npx create-next-app@latest my-prototype --typescript --tailwind --app
cd my-prototype
npm install @auth/nextjs prisma @prisma/client
npx prisma init --datasource-provider sqlite
```

### Express API (Backend Only)
```bash
mkdir api-prototype && cd api-prototype
npm init -y
npm install express cors dotenv
npm install -D typescript @types/express @types/node ts-node nodemon
npx tsc --init
```

### Static Site (No Backend)
```bash
npm create vite@latest static-prototype -- --template react-ts
cd static-prototype
npm install
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p
```

## Step-by-Step MVP Procedure

### Phase 1: Scope Definition (30 minutes)
1. **Define the ONE core feature**
   ```markdown
   Core value: [What problem does this solve?]
   Core action: [What ONE thing must users do?]
   Success metric: [How do we know it works?]
   ```

2. **List what to fake**
   - Authentication? Use hardcoded user
   - Payments? Show success message
   - Email? Log to console
   - AI features? Use placeholder responses

3. **Draw 3 screens max**
   - Entry point (landing/login)
   - Core action screen
   - Success/result screen

### Phase 2: Scaffold (1-2 hours)
```bash
# 1. Create project
npx create-next-app@latest mvp --typescript --tailwind --app

# 2. Add essential deps only
npm install zod react-hook-form  # Forms
npm install zustand              # State (if needed)

# 3. Create route structure
mkdir -p app/(auth) app/(dashboard) app/api
```

### Phase 3: Build Core Loop (2-4 hours)
Focus only on:
1. Data input (form/upload/selection)
2. Processing (real or faked)
3. Output display (results/confirmation)

```typescript
// Minimal working form
'use client';
import { useState } from 'react';

export default function CoreFeature() {
  const [result, setResult] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setLoading(true);

    const formData = new FormData(e.currentTarget);
    // Fake processing delay
    await new Promise(r => setTimeout(r, 1000));

    // Fake result - replace with real logic later
    setResult(`Processed: ${formData.get('input')}`);
    setLoading(false);
  }

  return (
    <div className="max-w-md mx-auto p-4">
      <form onSubmit={handleSubmit} className="space-y-4">
        <input
          name="input"
          placeholder="Enter something..."
          className="w-full p-2 border rounded"
          required
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full p-2 bg-blue-500 text-white rounded disabled:opacity-50"
        >
          {loading ? 'Processing...' : 'Submit'}
        </button>
      </form>

      {result && (
        <div className="mt-4 p-4 bg-green-100 rounded">
          {result}
        </div>
      )}
    </div>
  );
}
```

### Phase 4: Polish Minimal UI (1-2 hours)
```typescript
// Quick layout wrapper
function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-4xl mx-auto p-4">
          <h1 className="text-xl font-bold">Prototype Name</h1>
        </div>
      </header>
      <main className="max-w-4xl mx-auto p-4">
        {children}
      </main>
    </div>
  );
}
```

## Faking Patterns

### Fake Authentication
```typescript
// lib/fake-auth.ts
const FAKE_USER = {
  id: '1',
  name: 'Test User',
  email: 'test@example.com',
};

export function useAuth() {
  return {
    user: FAKE_USER,
    login: async () => FAKE_USER,
    logout: async () => {},
    isAuthenticated: true,
  };
}
```

### Fake Database
```typescript
// lib/fake-db.ts
let items: Item[] = [
  { id: '1', name: 'Sample Item', createdAt: new Date() },
];

export const db = {
  items: {
    findMany: async () => items,
    create: async (data: Omit<Item, 'id'>) => {
      const item = { ...data, id: crypto.randomUUID() };
      items.push(item);
      return item;
    },
    delete: async (id: string) => {
      items = items.filter(i => i.id !== id);
    },
  },
};
```

### Fake API Response
```typescript
// app/api/analyze/route.ts
export async function POST(request: Request) {
  const { input } = await request.json();

  // Simulate processing delay
  await new Promise(r => setTimeout(r, 2000));

  // Return fake but realistic response
  return Response.json({
    success: true,
    result: {
      score: Math.random() * 100,
      summary: `Analysis of "${input}" complete.`,
      recommendations: [
        'Consider improving X',
        'Opportunity in Y area',
      ],
    },
  });
}
```

## Decision Criteria

### Build vs. Fake
| Feature | Prototype | Why |
|---------|-----------|-----|
| Core value feature | Build | Must prove concept |
| Authentication | Fake | Not differentiating |
| Payments | Fake | Complex, add later |
| Email/notifications | Log to console | Prove without sending |
| File uploads | Local storage | Avoid cloud setup |
| Search | Simple filter | Full-text later |

### Framework Selection
| Need | Use | Time Saved |
|------|-----|------------|
| Full-stack web | Next.js | 2+ hours |
| API only | Express/Hono | 1 hour |
| Static + forms | Vite + Formspree | 30 min |
| Mobile concept | React Native Expo | 1 hour |
| CLI tool | Node.js + Commander | 30 min |

## Common Pitfalls to Avoid

1. **Premature optimization** - Don't add caching, queues, etc.
2. **Perfect styling** - Use Tailwind defaults or shadcn/ui
3. **Edge cases** - Handle happy path only
4. **Full auth flow** - Fake it until you need real users
5. **Database migrations** - SQLite file is fine
6. **CI/CD** - Manual deploy is acceptable
7. **Tests** - Manual testing is faster for prototypes

## Deployment Shortcuts

### Vercel (Fastest)
```bash
npm install -g vercel
vercel  # Follow prompts, done in 2 minutes
```

### Netlify (Static)
```bash
npm run build
npx netlify-cli deploy --prod
```

### Railway (With Database)
```bash
# Link repo to Railway dashboard
# Add Postgres plugin
# Deploy automatically
```

## Output Checklist

Before demo/testing:
- [ ] Core feature works end-to-end
- [ ] No console errors on main flow
- [ ] Mobile-responsive (basic)
- [ ] Loading states shown
- [ ] Error messages display (even if generic)
- [ ] Deployed to shareable URL

## Prototype Handoff Template
```markdown
## Prototype: [Name]

### Purpose
[One sentence on what this validates]

### Live URL
[Deployed link]

### Test Instructions
1. [Step to test core feature]
2. [Expected outcome]

### What's Real
- [Feature that actually works]

### What's Faked
- Auth: Hardcoded user
- Data: In-memory, resets on refresh
- [Other faked features]

### Next Steps to Production
1. [ ] Replace fake auth with [provider]
2. [ ] Add real database
3. [ ] Implement [deferred feature]
```
