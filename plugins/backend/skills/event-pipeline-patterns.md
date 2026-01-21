---
skill: event-pipeline-patterns
version: "1.0.0"
description: "Event-driven architectures, Inngest pipelines, analytics tracking, and webhook handling patterns"
used-by: [data-engineer, backend-engineer, api-architect]
---

# Event Pipeline Patterns

## Event Schema Design

### Event Envelope Structure
```typescript
// types/events.ts
import { z } from 'zod';

// Base envelope for all events
export const eventEnvelopeSchema = z.object({
  id: z.string().uuid(),
  type: z.string(),
  version: z.string().regex(/^\d+\.\d+\.\d+$/),
  timestamp: z.string().datetime(),
  source: z.string(),
  correlationId: z.string().uuid().optional(),
  metadata: z.object({
    environment: z.enum(['development', 'staging', 'production']),
    region: z.string().optional(),
    userAgent: z.string().optional(),
  }),
  data: z.unknown(),
});

export type EventEnvelope = z.infer<typeof eventEnvelopeSchema>;

// Factory for creating events
export function createEvent<T>(
  type: string,
  data: T,
  options?: Partial<Pick<EventEnvelope, 'correlationId' | 'metadata'>>
): EventEnvelope {
  return {
    id: crypto.randomUUID(),
    type,
    version: '1.0.0',
    timestamp: new Date().toISOString(),
    source: process.env.SERVICE_NAME ?? 'unknown',
    correlationId: options?.correlationId,
    metadata: {
      environment: (process.env.NODE_ENV as 'development' | 'staging' | 'production') ?? 'development',
      ...options?.metadata,
    },
    data,
  };
}
```

### Domain Event Types
```typescript
// events/user.events.ts
import { z } from 'zod';

export const userCreatedSchema = z.object({
  userId: z.string().uuid(),
  email: z.string().email(),
  name: z.string(),
  plan: z.enum(['free', 'pro', 'enterprise']),
  source: z.enum(['signup', 'invitation', 'migration']),
});

export const userUpdatedSchema = z.object({
  userId: z.string().uuid(),
  changes: z.record(z.unknown()),
  previousValues: z.record(z.unknown()),
});

export const userDeletedSchema = z.object({
  userId: z.string().uuid(),
  reason: z.string().optional(),
  deletedAt: z.string().datetime(),
});

// Event type registry
export const userEvents = {
  'user/created': userCreatedSchema,
  'user/updated': userUpdatedSchema,
  'user/deleted': userDeletedSchema,
} as const;

export type UserEventType = keyof typeof userEvents;
```

## Inngest Setup and Configuration

### Client Configuration
```typescript
// inngest/client.ts
import { Inngest, EventSchemas } from 'inngest';
import { z } from 'zod';

// Define event schemas for type safety
type Events = {
  'user/created': {
    data: {
      userId: string;
      email: string;
      name: string;
      plan: 'free' | 'pro' | 'enterprise';
    };
  };
  'order/placed': {
    data: {
      orderId: string;
      userId: string;
      items: Array<{ productId: string; quantity: number; price: number }>;
      total: number;
    };
  };
  'email/send': {
    data: {
      to: string;
      template: string;
      variables: Record<string, unknown>;
    };
  };
};

export const inngest = new Inngest({
  id: 'my-app',
  schemas: new EventSchemas().fromRecord<Events>(),
  middleware: [
    // Logging middleware
    {
      name: 'logging',
      init() {
        return {
          onFunctionRun({ fn, event }) {
            console.log(`[Inngest] Starting ${fn.name}`, { eventId: event.id });
            return {
              afterExecution({ error }) {
                if (error) {
                  console.error(`[Inngest] Failed ${fn.name}`, error);
                } else {
                  console.log(`[Inngest] Completed ${fn.name}`);
                }
              },
            };
          },
        };
      },
    },
  ],
});
```

### Basic Inngest Function
```typescript
// inngest/functions/user-welcome.ts
import { inngest } from '../client';
import { resend } from '@/lib/resend';
import { prisma } from '@/lib/prisma';

export const sendWelcomeEmail = inngest.createFunction(
  {
    id: 'send-welcome-email',
    retries: 3,
    onFailure: async ({ event, error }) => {
      await prisma.failedEvent.create({
        data: {
          eventId: event.id,
          eventType: 'user/created',
          error: error.message,
          payload: JSON.stringify(event.data),
        },
      });
    },
  },
  { event: 'user/created' },
  async ({ event, step }) => {
    const { userId, email, name } = event.data;

    // Step 1: Send welcome email
    const emailResult = await step.run('send-welcome-email', async () => {
      const response = await resend.emails.send({
        from: 'welcome@example.com',
        to: email,
        subject: `Welcome, ${name}!`,
        html: `<h1>Welcome to our platform!</h1>`,
      });
      return { emailId: response.id };
    });

    // Step 2: Update user record
    await step.run('update-user-welcome-sent', async () => {
      await prisma.user.update({
        where: { id: userId },
        data: { welcomeEmailSentAt: new Date() },
      });
    });

    // Step 3: Wait before sending follow-up
    await step.sleep('wait-for-followup', '3 days');

    // Step 4: Send follow-up email
    await step.run('send-followup-email', async () => {
      await resend.emails.send({
        from: 'team@example.com',
        to: email,
        subject: 'How are you finding things?',
        html: `<p>Hi ${name}, let us know if you need help!</p>`,
      });
    });

    return { emailId: emailResult.emailId, completed: true };
  }
);
```

## Fan-Out and Parallel Execution

### Fan-Out Pattern
```typescript
// inngest/functions/order-processing.ts
import { inngest } from '../client';

export const processOrder = inngest.createFunction(
  { id: 'process-order' },
  { event: 'order/placed' },
  async ({ event, step }) => {
    const { orderId, userId, items, total } = event.data;

    // Fan-out: Process multiple items in parallel
    const inventoryResults = await step.run('check-inventory', async () => {
      const checks = items.map(async (item) => {
        const response = await fetch(`${process.env.INVENTORY_API}/check`, {
          method: 'POST',
          body: JSON.stringify({ productId: item.productId, quantity: item.quantity }),
        });
        return response.json();
      });
      return Promise.all(checks);
    });

    // Validate all items are available
    const allAvailable = inventoryResults.every((r) => r.available);
    if (!allAvailable) {
      await step.sendEvent('order-failed', {
        name: 'order/failed',
        data: { orderId, reason: 'inventory_unavailable' },
      });
      return { status: 'failed', reason: 'inventory_unavailable' };
    }

    // Fan-out: Trigger parallel workflows
    await step.sendEvent('fan-out-order-tasks', [
      { name: 'order/fulfill', data: { orderId, items } },
      { name: 'order/notify-warehouse', data: { orderId, items } },
      { name: 'payment/charge', data: { orderId, userId, amount: total } },
      { name: 'analytics/track', data: { event: 'order_placed', orderId, userId, total } },
    ]);

    return { status: 'processing', orderId };
  }
);
```

### Parallel Step Execution
```typescript
// inngest/functions/data-aggregation.ts
import { inngest } from '../client';

export const aggregateUserData = inngest.createFunction(
  { id: 'aggregate-user-data' },
  { event: 'user/data-export-requested' },
  async ({ event, step }) => {
    const { userId } = event.data;

    // Execute multiple data fetches in parallel
    const [profile, orders, activity, preferences] = await Promise.all([
      step.run('fetch-profile', () => fetchUserProfile(userId)),
      step.run('fetch-orders', () => fetchUserOrders(userId)),
      step.run('fetch-activity', () => fetchUserActivity(userId)),
      step.run('fetch-preferences', () => fetchUserPreferences(userId)),
    ]);

    // Combine results
    const exportData = await step.run('combine-data', async () => ({
      profile,
      orders,
      activity,
      preferences,
      exportedAt: new Date().toISOString(),
    }));

    // Upload to storage
    const downloadUrl = await step.run('upload-export', async () => {
      const blob = new Blob([JSON.stringify(exportData)], { type: 'application/json' });
      return uploadToStorage(`exports/${userId}/${Date.now()}.json`, blob);
    });

    return { downloadUrl };
  }
);
```

## Scheduled Jobs (Cron)

### Daily Reports
```typescript
// inngest/functions/scheduled-reports.ts
import { inngest } from '../client';

export const dailyMetricsReport = inngest.createFunction(
  {
    id: 'daily-metrics-report',
    concurrency: 1, // Ensure only one runs at a time
  },
  { cron: '0 8 * * *' }, // Every day at 8 AM UTC
  async ({ step }) => {
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const dateStr = yesterday.toISOString().split('T')[0];

    // Gather metrics
    const metrics = await step.run('gather-metrics', async () => {
      const [users, orders, revenue] = await Promise.all([
        prisma.user.count({ where: { createdAt: { gte: yesterday } } }),
        prisma.order.count({ where: { createdAt: { gte: yesterday } } }),
        prisma.order.aggregate({
          where: { createdAt: { gte: yesterday } },
          _sum: { total: true },
        }),
      ]);
      return { newUsers: users, orders, revenue: revenue._sum.total ?? 0 };
    });

    // Store in database
    await step.run('store-metrics', async () => {
      await prisma.dailyMetrics.create({
        data: { date: dateStr, ...metrics },
      });
    });

    // Send to Slack
    await step.run('notify-slack', async () => {
      await fetch(process.env.SLACK_WEBHOOK_URL!, {
        method: 'POST',
        body: JSON.stringify({
          text: `Daily Metrics for ${dateStr}:\n- New Users: ${metrics.newUsers}\n- Orders: ${metrics.orders}\n- Revenue: $${metrics.revenue}`,
        }),
      });
    });

    return metrics;
  }
);

// Cleanup old data weekly
export const weeklyCleanup = inngest.createFunction(
  { id: 'weekly-cleanup' },
  { cron: '0 2 * * 0' }, // Sunday at 2 AM UTC
  async ({ step }) => {
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

    const deleted = await step.run('cleanup-old-sessions', async () => {
      const result = await prisma.session.deleteMany({
        where: { expiresAt: { lt: thirtyDaysAgo } },
      });
      return result.count;
    });

    return { deletedSessions: deleted };
  }
);
```

## Debouncing and Batching

### Debounce Pattern
```typescript
// inngest/functions/search-index.ts
import { inngest } from '../client';

// Debounce search index updates - wait for activity to settle
export const updateSearchIndex = inngest.createFunction(
  {
    id: 'update-search-index',
    debounce: {
      key: 'event.data.entityType',
      period: '5s', // Wait 5 seconds for more events
    },
  },
  { event: 'search/reindex-requested' },
  async ({ event, step, events }) => {
    // events contains all debounced events
    const entityType = event.data.entityType;
    const entityIds = [...new Set(events.map((e) => e.data.entityId))];

    await step.run('batch-reindex', async () => {
      const entities = await prisma[entityType].findMany({
        where: { id: { in: entityIds } },
      });

      await searchClient.index(entityType).updateDocuments(entities);
    });

    return { indexed: entityIds.length, entityType };
  }
);
```

### Batching with Concurrency Control
```typescript
// inngest/functions/notification-batch.ts
import { inngest } from '../client';

export const batchNotifications = inngest.createFunction(
  {
    id: 'batch-notifications',
    batchEvents: {
      maxSize: 100, // Process up to 100 events at once
      timeout: '10s', // Or after 10 seconds, whichever comes first
    },
    concurrency: {
      limit: 5, // Max 5 concurrent executions
    },
  },
  { event: 'notification/send' },
  async ({ events, step }) => {
    // Group notifications by user
    const byUser = events.reduce(
      (acc, event) => {
        const userId = event.data.userId;
        if (!acc[userId]) acc[userId] = [];
        acc[userId].push(event.data);
        return acc;
      },
      {} as Record<string, Array<{ userId: string; message: string; channel: string }>>
    );

    // Send batched notifications
    const results = await step.run('send-batch', async () => {
      const sends = Object.entries(byUser).map(async ([userId, notifications]) => {
        // Combine notifications for same user
        const combined = {
          userId,
          messages: notifications.map((n) => n.message),
          channels: [...new Set(notifications.map((n) => n.channel))],
        };
        return sendBatchedNotification(combined);
      });
      return Promise.all(sends);
    });

    return { processed: events.length, users: Object.keys(byUser).length };
  }
);
```

## Webhook Handling

### Signature Verification
```typescript
// lib/webhooks/verify.ts
import crypto from 'crypto';

export function verifyStripeSignature(
  payload: string,
  signature: string,
  secret: string
): boolean {
  const elements = signature.split(',');
  const timestamp = elements.find((e) => e.startsWith('t='))?.slice(2);
  const v1Signature = elements.find((e) => e.startsWith('v1='))?.slice(3);

  if (!timestamp || !v1Signature) return false;

  const signedPayload = `${timestamp}.${payload}`;
  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(signedPayload)
    .digest('hex');

  return crypto.timingSafeEqual(
    Buffer.from(v1Signature),
    Buffer.from(expectedSignature)
  );
}

export function verifyGitHubSignature(
  payload: string,
  signature: string,
  secret: string
): boolean {
  const expected = `sha256=${crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex')}`;

  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expected)
  );
}
```

### Idempotent Webhook Handler
```typescript
// app/api/webhooks/stripe/route.ts
import { NextRequest, NextResponse } from 'next/server';
import { verifyStripeSignature } from '@/lib/webhooks/verify';
import { inngest } from '@/inngest/client';
import { prisma } from '@/lib/prisma';

export async function POST(request: NextRequest) {
  const payload = await request.text();
  const signature = request.headers.get('stripe-signature');

  if (!signature) {
    return NextResponse.json({ error: 'Missing signature' }, { status: 400 });
  }

  // Verify signature
  if (!verifyStripeSignature(payload, signature, process.env.STRIPE_WEBHOOK_SECRET!)) {
    return NextResponse.json({ error: 'Invalid signature' }, { status: 401 });
  }

  const event = JSON.parse(payload);

  // Idempotency check - prevent duplicate processing
  const existing = await prisma.processedWebhook.findUnique({
    where: { eventId: event.id },
  });

  if (existing) {
    return NextResponse.json({ status: 'already_processed' });
  }

  // Mark as processing (with TTL for cleanup)
  await prisma.processedWebhook.create({
    data: {
      eventId: event.id,
      type: event.type,
      processedAt: new Date(),
    },
  });

  // Route to Inngest for processing
  try {
    await inngest.send({
      name: `stripe/${event.type}`,
      data: event.data.object,
      id: event.id, // Use Stripe event ID for Inngest idempotency
    });

    return NextResponse.json({ status: 'accepted' });
  } catch (error) {
    // Remove idempotency record on failure so retry can work
    await prisma.processedWebhook.delete({ where: { eventId: event.id } });
    throw error;
  }
}
```

### Webhook Event Router
```typescript
// inngest/functions/stripe-webhooks.ts
import { inngest } from '../client';

// Payment succeeded
export const handlePaymentSucceeded = inngest.createFunction(
  { id: 'stripe-payment-succeeded' },
  { event: 'stripe/payment_intent.succeeded' },
  async ({ event, step }) => {
    const paymentIntent = event.data;

    await step.run('update-order', async () => {
      await prisma.order.update({
        where: { paymentIntentId: paymentIntent.id },
        data: { status: 'paid', paidAt: new Date() },
      });
    });

    await step.sendEvent('notify-user', {
      name: 'email/send',
      data: {
        to: paymentIntent.receipt_email,
        template: 'payment-confirmation',
        variables: { amount: paymentIntent.amount / 100 },
      },
    });
  }
);

// Subscription events
export const handleSubscriptionUpdated = inngest.createFunction(
  { id: 'stripe-subscription-updated' },
  { event: 'stripe/customer.subscription.updated' },
  async ({ event, step }) => {
    const subscription = event.data;

    await step.run('sync-subscription', async () => {
      await prisma.subscription.upsert({
        where: { stripeSubscriptionId: subscription.id },
        update: {
          status: subscription.status,
          currentPeriodEnd: new Date(subscription.current_period_end * 1000),
          cancelAtPeriodEnd: subscription.cancel_at_period_end,
        },
        create: {
          stripeSubscriptionId: subscription.id,
          stripeCustomerId: subscription.customer,
          status: subscription.status,
          currentPeriodEnd: new Date(subscription.current_period_end * 1000),
        },
      });
    });
  }
);
```

## Analytics Event Tracking

### Segment Integration
```typescript
// lib/analytics/segment.ts
import { Analytics } from '@segment/analytics-node';

const analytics = new Analytics({
  writeKey: process.env.SEGMENT_WRITE_KEY!,
  flushAt: 20, // Batch size
  flushInterval: 10000, // Flush every 10s
});

export interface TrackEvent {
  userId?: string;
  anonymousId?: string;
  event: string;
  properties?: Record<string, unknown>;
  context?: Record<string, unknown>;
  timestamp?: Date;
}

export function track(event: TrackEvent): void {
  if (!event.userId && !event.anonymousId) {
    console.warn('Track event missing userId or anonymousId');
    return;
  }

  analytics.track({
    userId: event.userId,
    anonymousId: event.anonymousId,
    event: event.event,
    properties: event.properties,
    context: {
      ...event.context,
      library: { name: 'my-app', version: '1.0.0' },
    },
    timestamp: event.timestamp ?? new Date(),
  });
}

export function identify(userId: string, traits: Record<string, unknown>): void {
  analytics.identify({ userId, traits });
}

export function page(
  userId: string,
  name: string,
  properties?: Record<string, unknown>
): void {
  analytics.page({ userId, name, properties });
}

// Graceful shutdown
export async function closeAnalytics(): Promise<void> {
  await analytics.closeAndFlush();
}
```

### PostHog Integration
```typescript
// lib/analytics/posthog.ts
import { PostHog } from 'posthog-node';

const posthog = new PostHog(process.env.POSTHOG_API_KEY!, {
  host: process.env.POSTHOG_HOST ?? 'https://app.posthog.com',
  flushAt: 20,
  flushInterval: 10000,
});

export function capture(
  distinctId: string,
  event: string,
  properties?: Record<string, unknown>
): void {
  posthog.capture({
    distinctId,
    event,
    properties: {
      ...properties,
      $lib: 'my-app',
      $lib_version: '1.0.0',
    },
  });
}

export function identifyUser(
  distinctId: string,
  properties: Record<string, unknown>
): void {
  posthog.identify({ distinctId, properties });
}

export function capturePageview(
  distinctId: string,
  url: string,
  properties?: Record<string, unknown>
): void {
  posthog.capture({
    distinctId,
    event: '$pageview',
    properties: { $current_url: url, ...properties },
  });
}

// Feature flags
export async function getFeatureFlag(
  distinctId: string,
  flagKey: string
): Promise<boolean | string | undefined> {
  return posthog.getFeatureFlag(flagKey, distinctId);
}

export async function closePostHog(): Promise<void> {
  await posthog.shutdown();
}
```

### Server-Side Analytics Middleware
```typescript
// middleware/analytics.ts
import { NextRequest, NextResponse } from 'next/server';
import { track } from '@/lib/analytics/segment';

export function analyticsMiddleware(request: NextRequest): NextResponse {
  const response = NextResponse.next();

  // Get or create anonymous ID
  let anonymousId = request.cookies.get('ajs_anonymous_id')?.value;
  if (!anonymousId) {
    anonymousId = crypto.randomUUID();
    response.cookies.set('ajs_anonymous_id', anonymousId, {
      maxAge: 365 * 24 * 60 * 60, // 1 year
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
    });
  }

  // Track pageview
  track({
    anonymousId,
    event: 'Page Viewed',
    properties: {
      path: request.nextUrl.pathname,
      url: request.url,
      referrer: request.headers.get('referer'),
      userAgent: request.headers.get('user-agent'),
    },
  });

  return response;
}
```

## Event Batching for Performance

### Batch Event Processor
```typescript
// lib/events/batch-processor.ts
interface BatchConfig {
  maxSize: number;
  maxWaitMs: number;
  onFlush: (events: unknown[]) => Promise<void>;
}

export class BatchProcessor<T> {
  private batch: T[] = [];
  private timer: NodeJS.Timeout | null = null;
  private config: BatchConfig;

  constructor(config: BatchConfig) {
    this.config = config;
  }

  add(event: T): void {
    this.batch.push(event);

    if (this.batch.length >= this.config.maxSize) {
      this.flush();
    } else if (!this.timer) {
      this.timer = setTimeout(() => this.flush(), this.config.maxWaitMs);
    }
  }

  async flush(): Promise<void> {
    if (this.timer) {
      clearTimeout(this.timer);
      this.timer = null;
    }

    if (this.batch.length === 0) return;

    const events = this.batch;
    this.batch = [];

    try {
      await this.config.onFlush(events);
    } catch (error) {
      console.error('Batch flush failed:', error);
      // Re-add events for retry
      this.batch = [...events, ...this.batch];
    }
  }

  async close(): Promise<void> {
    await this.flush();
  }
}

// Usage
const analyticsProcessor = new BatchProcessor<TrackEvent>({
  maxSize: 100,
  maxWaitMs: 5000,
  onFlush: async (events) => {
    await fetch('/api/analytics/batch', {
      method: 'POST',
      body: JSON.stringify({ events }),
    });
  },
});
```

### Inngest Batch Event Handler
```typescript
// app/api/inngest/route.ts
import { serve } from 'inngest/next';
import { inngest } from '@/inngest/client';

// Batch analytics events
export const batchAnalytics = inngest.createFunction(
  {
    id: 'batch-analytics',
    batchEvents: {
      maxSize: 500,
      timeout: '30s',
    },
  },
  { event: 'analytics/track' },
  async ({ events, step }) => {
    // Transform events for warehouse
    const transformed = events.map((e) => ({
      event_id: e.id,
      event_type: e.data.event,
      user_id: e.data.userId,
      properties: e.data.properties,
      timestamp: e.ts,
    }));

    // Bulk insert to data warehouse
    await step.run('insert-to-warehouse', async () => {
      await bigquery
        .dataset('analytics')
        .table('events')
        .insert(transformed);
    });

    return { inserted: transformed.length };
  }
);
```

## Dead Letter Queue and Error Handling

### DLQ Implementation
```typescript
// lib/events/dlq.ts
import { prisma } from '@/lib/prisma';

interface DeadLetter {
  eventId: string;
  eventType: string;
  payload: unknown;
  error: string;
  attempts: number;
  lastAttemptAt: Date;
}

export async function moveToDeadLetterQueue(
  event: { id: string; type: string; data: unknown },
  error: Error,
  attempts: number
): Promise<void> {
  await prisma.deadLetterQueue.create({
    data: {
      eventId: event.id,
      eventType: event.type,
      payload: JSON.stringify(event.data),
      error: error.message,
      stackTrace: error.stack,
      attempts,
      lastAttemptAt: new Date(),
    },
  });
}

export async function reprocessDeadLetter(dlqId: string): Promise<void> {
  const item = await prisma.deadLetterQueue.findUnique({
    where: { id: dlqId },
  });

  if (!item) throw new Error('DLQ item not found');

  // Re-send to Inngest
  await inngest.send({
    name: item.eventType,
    data: JSON.parse(item.payload),
    id: `${item.eventId}-retry-${Date.now()}`,
  });

  // Mark as reprocessed
  await prisma.deadLetterQueue.update({
    where: { id: dlqId },
    data: { reprocessedAt: new Date() },
  });
}

// Scheduled DLQ cleanup
export const cleanupDeadLetterQueue = inngest.createFunction(
  { id: 'cleanup-dlq' },
  { cron: '0 0 * * 0' }, // Weekly
  async ({ step }) => {
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

    const deleted = await step.run('delete-old-dlq', async () => {
      const result = await prisma.deadLetterQueue.deleteMany({
        where: {
          OR: [
            { reprocessedAt: { not: null } }, // Already reprocessed
            { lastAttemptAt: { lt: thirtyDaysAgo } }, // Too old
          ],
        },
      });
      return result.count;
    });

    return { deleted };
  }
);
```

### Comprehensive Error Handler
```typescript
// inngest/functions/with-error-handling.ts
import { inngest } from '../client';
import { moveToDeadLetterQueue } from '@/lib/events/dlq';

export const processWithErrorHandling = inngest.createFunction(
  {
    id: 'process-with-error-handling',
    retries: 5,
    onFailure: async ({ event, error, attempt }) => {
      // Log to monitoring
      console.error(`Event ${event.id} failed after ${attempt} attempts`, error);

      // Move to DLQ after all retries exhausted
      await moveToDeadLetterQueue(
        { id: event.id, type: event.name, data: event.data },
        error,
        attempt
      );

      // Alert on-call
      await fetch(process.env.PAGERDUTY_WEBHOOK!, {
        method: 'POST',
        body: JSON.stringify({
          event_action: 'trigger',
          payload: {
            summary: `Event processing failed: ${event.name}`,
            severity: 'error',
            source: 'inngest',
            custom_details: { eventId: event.id, error: error.message },
          },
        }),
      });
    },
  },
  { event: 'critical/process' },
  async ({ event, step }) => {
    // Wrap each step with error context
    const result = await step.run('main-process', async () => {
      try {
        return await processCriticalEvent(event.data);
      } catch (error) {
        // Add context to error
        const enrichedError = new Error(
          `Failed processing event ${event.id}: ${error.message}`
        );
        enrichedError.cause = error;
        throw enrichedError;
      }
    });

    return result;
  }
);
```

## Retry Strategies

### Exponential Backoff Configuration
```typescript
// inngest/functions/with-retries.ts
import { inngest } from '../client';

// Basic retry with exponential backoff
export const basicRetry = inngest.createFunction(
  {
    id: 'basic-retry',
    retries: 5, // 5 retries with exponential backoff
    // Default: 1s, 2s, 4s, 8s, 16s
  },
  { event: 'task/process' },
  async ({ event, step }) => {
    await step.run('process', async () => {
      const response = await fetch(process.env.EXTERNAL_API!);
      if (!response.ok) throw new Error(`API error: ${response.status}`);
      return response.json();
    });
  }
);

// Custom retry backoff
export const customRetry = inngest.createFunction(
  {
    id: 'custom-retry',
    retries: 10,
    backoff: {
      type: 'exponential',
      delay: '1s', // Initial delay
      maxDelay: '1h', // Max delay between retries
      factor: 2, // Multiply by 2 each retry
    },
  },
  { event: 'external/sync' },
  async ({ event, step }) => {
    // Implementation
  }
);
```

### Conditional Retry Logic
```typescript
// inngest/functions/smart-retry.ts
import { inngest } from '../client';

class RetryableError extends Error {
  constructor(
    message: string,
    public readonly retryAfter?: number
  ) {
    super(message);
    this.name = 'RetryableError';
  }
}

class NonRetryableError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'NonRetryableError';
  }
}

export const smartRetry = inngest.createFunction(
  {
    id: 'smart-retry',
    retries: 5,
  },
  { event: 'api/call' },
  async ({ event, step, attempt }) => {
    return await step.run('call-api', async () => {
      try {
        const response = await fetch(event.data.url, {
          method: event.data.method,
          body: JSON.stringify(event.data.body),
        });

        if (response.ok) {
          return response.json();
        }

        // Handle specific status codes
        switch (response.status) {
          case 429: // Rate limited
            const retryAfter = parseInt(response.headers.get('Retry-After') ?? '60');
            throw new RetryableError('Rate limited', retryAfter);

          case 400:
          case 401:
          case 403:
          case 404:
            // Client errors - don't retry
            throw new NonRetryableError(`Client error: ${response.status}`);

          case 500:
          case 502:
          case 503:
          case 504:
            // Server errors - retry
            throw new RetryableError(`Server error: ${response.status}`);

          default:
            throw new Error(`Unexpected status: ${response.status}`);
        }
      } catch (error) {
        if (error instanceof NonRetryableError) {
          // Log and don't retry
          console.error('Non-retryable error:', error.message);
          return { error: error.message, retried: false };
        }

        if (error instanceof RetryableError && error.retryAfter) {
          // Use step.sleep for rate limit backoff
          await step.sleep('rate-limit-wait', `${error.retryAfter}s`);
        }

        throw error; // Will trigger retry
      }
    });
  }
);
```

### Circuit Breaker Pattern
```typescript
// lib/circuit-breaker.ts
interface CircuitState {
  failures: number;
  lastFailure: number;
  state: 'closed' | 'open' | 'half-open';
}

const circuits = new Map<string, CircuitState>();

const FAILURE_THRESHOLD = 5;
const RESET_TIMEOUT = 60000; // 1 minute

export function getCircuitState(key: string): CircuitState {
  if (!circuits.has(key)) {
    circuits.set(key, { failures: 0, lastFailure: 0, state: 'closed' });
  }
  return circuits.get(key)!;
}

export function recordSuccess(key: string): void {
  const state = getCircuitState(key);
  state.failures = 0;
  state.state = 'closed';
}

export function recordFailure(key: string): void {
  const state = getCircuitState(key);
  state.failures++;
  state.lastFailure = Date.now();

  if (state.failures >= FAILURE_THRESHOLD) {
    state.state = 'open';
  }
}

export function canExecute(key: string): boolean {
  const state = getCircuitState(key);

  if (state.state === 'closed') return true;

  if (state.state === 'open') {
    if (Date.now() - state.lastFailure > RESET_TIMEOUT) {
      state.state = 'half-open';
      return true;
    }
    return false;
  }

  return true; // half-open allows one request
}

// Usage in Inngest function
export const withCircuitBreaker = inngest.createFunction(
  { id: 'with-circuit-breaker' },
  { event: 'external/request' },
  async ({ event, step }) => {
    const circuitKey = `external-api-${event.data.endpoint}`;

    if (!canExecute(circuitKey)) {
      throw new Error('Circuit breaker open - service unavailable');
    }

    try {
      const result = await step.run('call-external', async () => {
        const response = await fetch(event.data.endpoint);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
      });

      recordSuccess(circuitKey);
      return result;
    } catch (error) {
      recordFailure(circuitKey);
      throw error;
    }
  }
);
```

## Decision Criteria

| Pattern | Use When |
|---------|----------|
| Fan-out | Multiple independent tasks from single event |
| Debounce | High-frequency updates that can be batched |
| Batch | Processing many similar events efficiently |
| Cron | Scheduled maintenance or reporting |
| Circuit breaker | Protecting against failing dependencies |
| DLQ | Handling events that exhaust retries |

## Common Pitfalls

1. **Missing idempotency**: Always use event IDs for deduplication
2. **No signature verification**: Webhooks must be verified
3. **Unbounded retries**: Set reasonable retry limits
4. **Missing DLQ**: Events disappear after max retries
5. **No batching**: Overwhelming downstream systems
6. **Ignoring backpressure**: Respect rate limits
7. **Missing monitoring**: Add alerts for failures
8. **Synchronous processing**: Use async for I/O operations
9. **No correlation IDs**: Tracing becomes impossible
10. **Hardcoded timeouts**: Make configurable per environment
