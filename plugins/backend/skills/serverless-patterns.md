---
skill: serverless-patterns
version: "1.0.0"
description: "Edge functions, Vercel, Cloudflare Workers, and serverless architecture patterns"
used-by: [backend-engineer, api-architect, performance-optimizer]
---

# Serverless Patterns

## Vercel Edge Functions

### Basic Edge Function
```typescript
// app/api/geo/route.ts
import { NextRequest, NextResponse } from 'next/server';

export const runtime = 'edge';

export async function GET(request: NextRequest) {
  const { geo } = request;
  return NextResponse.json({
    country: geo?.country ?? 'Unknown',
    city: geo?.city ?? 'Unknown',
    region: geo?.region ?? 'Unknown',
  });
}
```

### Edge Middleware
```typescript
// middleware.ts
import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';

export function middleware(request: NextRequest) {
  // A/B Testing
  const bucket = Math.random() < 0.5 ? 'a' : 'b';
  const response = NextResponse.next();
  response.cookies.set('ab-bucket', bucket);

  // Geolocation redirect
  const country = request.geo?.country;
  if (country === 'DE' && !request.nextUrl.pathname.startsWith('/de')) {
    return NextResponse.redirect(new URL('/de' + request.nextUrl.pathname, request.url));
  }

  return response;
}

export const config = {
  matcher: ['/((?!api|_next/static|favicon.ico).*)'],
};
```

## Cloudflare Workers

### Basic Worker
```typescript
// src/index.ts
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === '/api/hello') {
      return new Response(JSON.stringify({ message: 'Hello from Edge!' }), {
        headers: { 'Content-Type': 'application/json' },
      });
    }

    return new Response('Not Found', { status: 404 });
  },
};
```

### KV Storage Pattern
```typescript
export default {
  async fetch(request: Request, env: Env): Promise<Response> {
    const url = new URL(request.url);
    const key = url.pathname.slice(1);

    if (request.method === 'GET') {
      const value = await env.MY_KV.get(key);
      if (!value) return new Response('Not Found', { status: 404 });
      return new Response(value);
    }

    if (request.method === 'PUT') {
      const body = await request.text();
      await env.MY_KV.put(key, body, { expirationTtl: 3600 });
      return new Response('OK');
    }

    return new Response('Method Not Allowed', { status: 405 });
  },
};
```

## Vercel Serverless Functions

### Standard Function
```typescript
// app/api/posts/route.ts
import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const page = parseInt(searchParams.get('page') ?? '1');
  const limit = parseInt(searchParams.get('limit') ?? '10');

  const posts = await prisma.post.findMany({
    skip: (page - 1) * limit,
    take: limit,
    orderBy: { createdAt: 'desc' },
  });

  return NextResponse.json({ data: posts, page, limit });
}

export async function POST(request: Request) {
  const body = await request.json();
  const post = await prisma.post.create({ data: body });
  return NextResponse.json(post, { status: 201 });
}
```

### Background Jobs with Inngest
```typescript
// inngest/functions.ts
import { inngest } from './client';

export const sendWelcomeEmail = inngest.createFunction(
  { id: 'send-welcome-email' },
  { event: 'user/created' },
  async ({ event, step }) => {
    const user = event.data.user;

    await step.run('send-email', async () => {
      await resend.emails.send({
        from: 'hello@example.com',
        to: user.email,
        subject: 'Welcome!',
        html: '<p>Welcome to our platform!</p>',
      });
    });

    await step.sleep('wait-1-day', '1d');

    await step.run('send-followup', async () => {
      await resend.emails.send({
        from: 'hello@example.com',
        to: user.email,
        subject: 'How are you finding things?',
        html: '<p>Let us know if you need help!</p>',
      });
    });
  }
);
```

## Caching Patterns

### Edge Cache with Revalidation
```typescript
export async function GET() {
  const data = await fetch('https://api.example.com/data', {
    next: { revalidate: 60 }, // Revalidate every 60 seconds
  });
  return NextResponse.json(await data.json());
}
```

### On-Demand Revalidation
```typescript
// app/api/revalidate/route.ts
import { revalidatePath, revalidateTag } from 'next/cache';

export async function POST(request: Request) {
  const { path, tag, secret } = await request.json();

  if (secret !== process.env.REVALIDATION_SECRET) {
    return NextResponse.json({ error: 'Invalid secret' }, { status: 401 });
  }

  if (tag) revalidateTag(tag);
  if (path) revalidatePath(path);

  return NextResponse.json({ revalidated: true });
}
```

## Decision Criteria

| Runtime | Use When |
|---------|----------|
| Edge | Geolocation, A/B tests, auth checks, fast responses |
| Serverless | Database access, complex logic, third-party APIs |
| Background | Long-running tasks, scheduled jobs, webhooks |

## Common Pitfalls

1. **Cold starts**: Use edge for latency-critical paths
2. **Timeout limits**: 10s edge, 60s serverless (Vercel)
3. **No connection pooling**: Use Prisma Data Proxy or PlanetScale
4. **Large bundles**: Keep edge functions < 1MB
5. **Missing error handling**: Always wrap in try/catch
6. **Blocking operations**: Use streaming for large responses
7. **Ignoring limits**: 1MB request body, 4MB response
