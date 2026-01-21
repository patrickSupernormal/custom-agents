# Edge Workers Patterns

```yaml
---
skill: edge-workers-patterns
version: 1.0.0
used-by:
  - edge-developer
  - api-architect
  - backend-engineer
description: Production-ready patterns for Cloudflare Workers, Vercel Edge Functions, and edge-native storage solutions
---
```

## 1. Cloudflare Workers

### Project Setup with Wrangler

```toml
# wrangler.toml
name = "my-edge-api"
main = "src/index.ts"
compatibility_date = "2024-01-01"
compatibility_flags = ["nodejs_compat"]

[vars]
ENVIRONMENT = "production"
API_VERSION = "v1"

# KV Namespace bindings
[[kv_namespaces]]
binding = "CACHE"
id = "abc123"
preview_id = "def456"

[[kv_namespaces]]
binding = "SESSIONS"
id = "ghi789"

# D1 Database binding
[[d1_databases]]
binding = "DB"
database_name = "my-database"
database_id = "xyz123"

# R2 Bucket binding
[[r2_buckets]]
binding = "STORAGE"
bucket_name = "my-bucket"

# Durable Objects binding
[[durable_objects.bindings]]
name = "RATE_LIMITER"
class_name = "RateLimiter"

[[durable_objects.bindings]]
name = "WEBSOCKET_ROOM"
class_name = "WebSocketRoom"

[[migrations]]
tag = "v1"
new_classes = ["RateLimiter", "WebSocketRoom"]

# Environment-specific overrides
[env.staging]
vars = { ENVIRONMENT = "staging" }

[env.production]
routes = [
  { pattern = "api.example.com/*", zone_name = "example.com" }
]
```

### Basic Worker with Hono

```typescript
// src/index.ts
import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";
import { secureHeaders } from "hono/secure-headers";
import { timing } from "hono/timing";

// Environment type definition
interface Env {
  // KV Namespaces
  CACHE: KVNamespace;
  SESSIONS: KVNamespace;

  // D1 Database
  DB: D1Database;

  // R2 Bucket
  STORAGE: R2Bucket;

  // Durable Objects
  RATE_LIMITER: DurableObjectNamespace;
  WEBSOCKET_ROOM: DurableObjectNamespace;

  // Environment variables
  ENVIRONMENT: string;
  API_VERSION: string;
  JWT_SECRET: string;
}

// Variables passed through context
interface Variables {
  userId: string;
  requestId: string;
}

const app = new Hono<{ Bindings: Env; Variables: Variables }>();

// Middleware stack
app.use("*", timing());
app.use("*", logger());
app.use("*", secureHeaders());
app.use(
  "/api/*",
  cors({
    origin: ["https://example.com", "https://app.example.com"],
    allowMethods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allowHeaders: ["Content-Type", "Authorization", "X-Request-ID"],
    exposeHeaders: ["X-Request-ID", "X-Response-Time"],
    maxAge: 86400,
    credentials: true,
  })
);

// Request ID middleware
app.use("*", async (c, next) => {
  const requestId =
    c.req.header("X-Request-ID") || crypto.randomUUID();
  c.set("requestId", requestId);
  c.header("X-Request-ID", requestId);
  await next();
});

// Health check
app.get("/health", (c) => {
  return c.json({
    status: "healthy",
    environment: c.env.ENVIRONMENT,
    version: c.env.API_VERSION,
    timestamp: new Date().toISOString(),
  });
});

// API routes
const api = new Hono<{ Bindings: Env; Variables: Variables }>();

api.get("/users/:id", async (c) => {
  const userId = c.req.param("id");
  const user = await c.env.DB.prepare(
    "SELECT * FROM users WHERE id = ?"
  )
    .bind(userId)
    .first();

  if (!user) {
    return c.json({ error: "User not found" }, 404);
  }

  return c.json({ user });
});

app.route("/api/v1", api);

// 404 handler
app.notFound((c) => {
  return c.json(
    {
      error: "Not Found",
      path: c.req.path,
      requestId: c.get("requestId"),
    },
    404
  );
});

// Error handler
app.onError((err, c) => {
  console.error(`Error: ${err.message}`, {
    requestId: c.get("requestId"),
    stack: err.stack,
  });

  return c.json(
    {
      error: "Internal Server Error",
      message:
        c.env.ENVIRONMENT === "development" ? err.message : undefined,
      requestId: c.get("requestId"),
    },
    500
  );
});

export default app;
```

### itty-router Alternative

```typescript
// src/index.ts (using itty-router)
import {
  Router,
  IRequest,
  error,
  json,
  withParams,
} from "itty-router";

interface Env {
  CACHE: KVNamespace;
  DB: D1Database;
}

interface CFRequest extends IRequest {
  userId?: string;
}

const router = Router<CFRequest>();

// Middleware helper
const withAuth = async (request: CFRequest, env: Env) => {
  const token = request.headers.get("Authorization")?.replace(
    "Bearer ",
    ""
  );
  if (!token) {
    return error(401, "Unauthorized");
  }
  // Validate token and attach user
  request.userId = "user-123"; // From token validation
};

// Routes
router
  .all("*", withParams)
  .get("/api/items", withAuth, async (request, env: Env) => {
    const items = await env.DB.prepare("SELECT * FROM items").all();
    return json(items.results);
  })
  .get("/api/items/:id", withAuth, async (request, env: Env) => {
    const { id } = request.params;
    const item = await env.DB.prepare(
      "SELECT * FROM items WHERE id = ?"
    )
      .bind(id)
      .first();
    return item ? json(item) : error(404, "Not found");
  })
  .post("/api/items", withAuth, async (request, env: Env) => {
    const body = await request.json();
    const result = await env.DB.prepare(
      "INSERT INTO items (name, data) VALUES (?, ?) RETURNING *"
    )
      .bind(body.name, JSON.stringify(body.data))
      .first();
    return json(result, { status: 201 });
  })
  .all("*", () => error(404, "Not found"));

export default {
  fetch: (request: Request, env: Env, ctx: ExecutionContext) =>
    router.fetch(request, env, ctx).catch((err) => {
      console.error(err);
      return error(500, "Internal Server Error");
    }),
};
```

---

## 2. KV Storage

### KV CRUD Operations

```typescript
// src/kv/operations.ts
interface CacheOptions {
  ttl?: number; // seconds
  metadata?: Record<string, string>;
}

interface CachedItem<T> {
  data: T;
  cachedAt: number;
  expiresAt?: number;
}

export class KVCache {
  constructor(private kv: KVNamespace) {}

  // Create/Update with optional TTL
  async set<T>(
    key: string,
    value: T,
    options: CacheOptions = {}
  ): Promise<void> {
    const item: CachedItem<T> = {
      data: value,
      cachedAt: Date.now(),
      expiresAt: options.ttl
        ? Date.now() + options.ttl * 1000
        : undefined,
    };

    await this.kv.put(key, JSON.stringify(item), {
      expirationTtl: options.ttl,
      metadata: options.metadata,
    });
  }

  // Read with type safety
  async get<T>(key: string): Promise<T | null> {
    const raw = await this.kv.get(key, "text");
    if (!raw) return null;

    try {
      const item: CachedItem<T> = JSON.parse(raw);
      return item.data;
    } catch {
      return null;
    }
  }

  // Read with metadata
  async getWithMetadata<T>(
    key: string
  ): Promise<{ value: T | null; metadata: Record<string, string> | null }> {
    const result = await this.kv.getWithMetadata<Record<string, string>>(
      key,
      "text"
    );
    if (!result.value) {
      return { value: null, metadata: null };
    }

    try {
      const item: CachedItem<T> = JSON.parse(result.value);
      return { value: item.data, metadata: result.metadata };
    } catch {
      return { value: null, metadata: null };
    }
  }

  // Delete
  async delete(key: string): Promise<void> {
    await this.kv.delete(key);
  }

  // List keys with pagination
  async list(
    prefix?: string,
    limit: number = 1000
  ): Promise<{ keys: string[]; cursor?: string }> {
    const result = await this.kv.list({
      prefix,
      limit,
    });

    return {
      keys: result.keys.map((k) => k.name),
      cursor: result.list_complete ? undefined : result.cursor,
    };
  }

  // Batch delete by prefix
  async deleteByPrefix(prefix: string): Promise<number> {
    let deleted = 0;
    let cursor: string | undefined;

    do {
      const result = await this.kv.list({ prefix, cursor });
      await Promise.all(
        result.keys.map((key) => this.kv.delete(key.name))
      );
      deleted += result.keys.length;
      cursor = result.list_complete ? undefined : result.cursor;
    } while (cursor);

    return deleted;
  }
}
```

### Cache-Aside Pattern

```typescript
// src/kv/cache-aside.ts
type FetchFunction<T> = () => Promise<T>;

export class CacheAside {
  constructor(
    private kv: KVNamespace,
    private defaultTtl: number = 3600
  ) {}

  async getOrFetch<T>(
    key: string,
    fetchFn: FetchFunction<T>,
    ttl: number = this.defaultTtl
  ): Promise<T> {
    // Try cache first
    const cached = await this.kv.get<T>(key, "json");
    if (cached !== null) {
      return cached;
    }

    // Fetch fresh data
    const fresh = await fetchFn();

    // Store in cache (don't await to avoid blocking response)
    this.kv.put(key, JSON.stringify(fresh), { expirationTtl: ttl });

    return fresh;
  }

  // Stale-while-revalidate pattern
  async getStaleWhileRevalidate<T>(
    key: string,
    fetchFn: FetchFunction<T>,
    ttl: number = this.defaultTtl,
    staleTtl: number = ttl * 2,
    ctx: ExecutionContext
  ): Promise<T> {
    interface SWRItem<T> {
      data: T;
      staleAt: number;
      expiresAt: number;
    }

    const raw = await this.kv.get(key, "text");

    if (raw) {
      const item: SWRItem<T> = JSON.parse(raw);
      const now = Date.now();

      // Fresh data - return immediately
      if (now < item.staleAt) {
        return item.data;
      }

      // Stale but valid - return and revalidate in background
      if (now < item.expiresAt) {
        ctx.waitUntil(this.revalidate(key, fetchFn, ttl, staleTtl));
        return item.data;
      }
    }

    // No cache or expired - fetch fresh
    return this.fetchAndCache(key, fetchFn, ttl, staleTtl);
  }

  private async revalidate<T>(
    key: string,
    fetchFn: FetchFunction<T>,
    ttl: number,
    staleTtl: number
  ): Promise<void> {
    try {
      await this.fetchAndCache(key, fetchFn, ttl, staleTtl);
    } catch (error) {
      console.error(`Revalidation failed for ${key}:`, error);
    }
  }

  private async fetchAndCache<T>(
    key: string,
    fetchFn: FetchFunction<T>,
    ttl: number,
    staleTtl: number
  ): Promise<T> {
    const data = await fetchFn();
    const now = Date.now();

    const item = {
      data,
      staleAt: now + ttl * 1000,
      expiresAt: now + staleTtl * 1000,
    };

    await this.kv.put(key, JSON.stringify(item), {
      expirationTtl: staleTtl,
    });

    return data;
  }
}
```

### Session Management with KV

```typescript
// src/kv/sessions.ts
import { nanoid } from "nanoid";

interface Session {
  id: string;
  userId: string;
  createdAt: number;
  expiresAt: number;
  data: Record<string, unknown>;
}

export class SessionManager {
  private readonly SESSION_TTL = 86400; // 24 hours
  private readonly PREFIX = "session:";

  constructor(private kv: KVNamespace) {}

  async create(
    userId: string,
    data: Record<string, unknown> = {}
  ): Promise<Session> {
    const session: Session = {
      id: nanoid(32),
      userId,
      createdAt: Date.now(),
      expiresAt: Date.now() + this.SESSION_TTL * 1000,
      data,
    };

    await this.kv.put(
      `${this.PREFIX}${session.id}`,
      JSON.stringify(session),
      { expirationTtl: this.SESSION_TTL }
    );

    // Index by user for session listing
    const userSessions = await this.getUserSessions(userId);
    userSessions.push(session.id);
    await this.kv.put(
      `user-sessions:${userId}`,
      JSON.stringify(userSessions),
      { expirationTtl: this.SESSION_TTL }
    );

    return session;
  }

  async get(sessionId: string): Promise<Session | null> {
    const raw = await this.kv.get(`${this.PREFIX}${sessionId}`, "text");
    if (!raw) return null;

    const session: Session = JSON.parse(raw);

    // Check expiration
    if (Date.now() > session.expiresAt) {
      await this.delete(sessionId);
      return null;
    }

    return session;
  }

  async refresh(sessionId: string): Promise<Session | null> {
    const session = await this.get(sessionId);
    if (!session) return null;

    session.expiresAt = Date.now() + this.SESSION_TTL * 1000;

    await this.kv.put(
      `${this.PREFIX}${sessionId}`,
      JSON.stringify(session),
      { expirationTtl: this.SESSION_TTL }
    );

    return session;
  }

  async delete(sessionId: string): Promise<void> {
    const session = await this.get(sessionId);
    if (session) {
      // Remove from user index
      const userSessions = await this.getUserSessions(session.userId);
      const filtered = userSessions.filter((id) => id !== sessionId);
      await this.kv.put(
        `user-sessions:${session.userId}`,
        JSON.stringify(filtered)
      );
    }
    await this.kv.delete(`${this.PREFIX}${sessionId}`);
  }

  async deleteAllForUser(userId: string): Promise<void> {
    const sessionIds = await this.getUserSessions(userId);
    await Promise.all(
      sessionIds.map((id) => this.kv.delete(`${this.PREFIX}${id}`))
    );
    await this.kv.delete(`user-sessions:${userId}`);
  }

  private async getUserSessions(userId: string): Promise<string[]> {
    const raw = await this.kv.get(`user-sessions:${userId}`, "text");
    return raw ? JSON.parse(raw) : [];
  }
}
```

---

## 3. Durable Objects

### Rate Limiter with Sliding Window

```typescript
// src/durable-objects/rate-limiter.ts
interface RateLimitConfig {
  maxRequests: number;
  windowMs: number;
}

interface RateLimitResult {
  allowed: boolean;
  remaining: number;
  resetAt: number;
  retryAfter?: number;
}

export class RateLimiter implements DurableObject {
  private requests: number[] = [];
  private config: RateLimitConfig = {
    maxRequests: 100,
    windowMs: 60000, // 1 minute
  };

  constructor(
    private state: DurableObjectState,
    private env: unknown
  ) {
    // Restore state on initialization
    this.state.blockConcurrencyWhile(async () => {
      const stored = await this.state.storage.get<number[]>("requests");
      if (stored) {
        this.requests = stored;
      }
    });
  }

  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);

    switch (url.pathname) {
      case "/check":
        return this.handleCheck();
      case "/configure":
        return this.handleConfigure(request);
      case "/reset":
        return this.handleReset();
      default:
        return new Response("Not Found", { status: 404 });
    }
  }

  private async handleCheck(): Promise<Response> {
    const now = Date.now();
    const windowStart = now - this.config.windowMs;

    // Remove expired requests
    this.requests = this.requests.filter((ts) => ts > windowStart);

    const result: RateLimitResult = {
      allowed: this.requests.length < this.config.maxRequests,
      remaining: Math.max(
        0,
        this.config.maxRequests - this.requests.length
      ),
      resetAt: windowStart + this.config.windowMs,
    };

    if (result.allowed) {
      this.requests.push(now);
      await this.state.storage.put("requests", this.requests);
    } else {
      // Calculate retry-after based on oldest request
      const oldestInWindow = this.requests[0];
      result.retryAfter = Math.ceil(
        (oldestInWindow + this.config.windowMs - now) / 1000
      );
    }

    return new Response(JSON.stringify(result), {
      headers: {
        "Content-Type": "application/json",
        "X-RateLimit-Limit": String(this.config.maxRequests),
        "X-RateLimit-Remaining": String(result.remaining),
        "X-RateLimit-Reset": String(Math.floor(result.resetAt / 1000)),
      },
    });
  }

  private async handleConfigure(request: Request): Promise<Response> {
    const config = await request.json<Partial<RateLimitConfig>>();

    if (config.maxRequests) {
      this.config.maxRequests = config.maxRequests;
    }
    if (config.windowMs) {
      this.config.windowMs = config.windowMs;
    }

    await this.state.storage.put("config", this.config);

    return new Response(JSON.stringify(this.config), {
      headers: { "Content-Type": "application/json" },
    });
  }

  private async handleReset(): Promise<Response> {
    this.requests = [];
    await this.state.storage.put("requests", this.requests);
    return new Response("OK");
  }
}

// Usage in Worker
export async function checkRateLimit(
  env: { RATE_LIMITER: DurableObjectNamespace },
  identifier: string
): Promise<RateLimitResult> {
  const id = env.RATE_LIMITER.idFromName(identifier);
  const stub = env.RATE_LIMITER.get(id);
  const response = await stub.fetch("http://internal/check");
  return response.json();
}
```

### WebSocket Room with Durable Objects

```typescript
// src/durable-objects/websocket-room.ts
interface Message {
  type: "message" | "join" | "leave" | "presence";
  userId: string;
  content?: string;
  timestamp: number;
}

interface RoomState {
  messages: Message[];
  maxMessages: number;
}

export class WebSocketRoom implements DurableObject {
  private sessions: Map<WebSocket, { userId: string; joinedAt: number }> =
    new Map();
  private state: RoomState = {
    messages: [],
    maxMessages: 100,
  };

  constructor(
    private durableState: DurableObjectState,
    private env: unknown
  ) {
    this.durableState.blockConcurrencyWhile(async () => {
      const stored =
        await this.durableState.storage.get<Message[]>("messages");
      if (stored) {
        this.state.messages = stored;
      }
    });
  }

  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/websocket") {
      return this.handleWebSocket(request);
    }

    if (url.pathname === "/messages") {
      return new Response(JSON.stringify(this.state.messages), {
        headers: { "Content-Type": "application/json" },
      });
    }

    if (url.pathname === "/presence") {
      const users = Array.from(this.sessions.values()).map(
        (s) => s.userId
      );
      return new Response(JSON.stringify({ users, count: users.length }), {
        headers: { "Content-Type": "application/json" },
      });
    }

    return new Response("Not Found", { status: 404 });
  }

  private handleWebSocket(request: Request): Response {
    const upgradeHeader = request.headers.get("Upgrade");
    if (upgradeHeader !== "websocket") {
      return new Response("Expected WebSocket", { status: 426 });
    }

    const url = new URL(request.url);
    const userId = url.searchParams.get("userId");
    if (!userId) {
      return new Response("Missing userId", { status: 400 });
    }

    const pair = new WebSocketPair();
    const [client, server] = Object.values(pair);

    this.handleSession(server, userId);

    return new Response(null, {
      status: 101,
      webSocket: client,
    });
  }

  private handleSession(ws: WebSocket, userId: string): void {
    // Accept the WebSocket connection
    ws.accept();

    // Store session
    this.sessions.set(ws, { userId, joinedAt: Date.now() });

    // Send recent messages
    ws.send(
      JSON.stringify({
        type: "history",
        messages: this.state.messages.slice(-50),
      })
    );

    // Broadcast join
    this.broadcast({
      type: "join",
      userId,
      timestamp: Date.now(),
    });

    // Handle incoming messages
    ws.addEventListener("message", async (event) => {
      try {
        const data = JSON.parse(event.data as string);

        if (data.type === "message" && data.content) {
          const message: Message = {
            type: "message",
            userId,
            content: data.content,
            timestamp: Date.now(),
          };

          // Store message
          this.state.messages.push(message);
          if (this.state.messages.length > this.state.maxMessages) {
            this.state.messages = this.state.messages.slice(
              -this.state.maxMessages
            );
          }
          await this.durableState.storage.put(
            "messages",
            this.state.messages
          );

          // Broadcast to all
          this.broadcast(message);
        }

        if (data.type === "ping") {
          ws.send(JSON.stringify({ type: "pong", timestamp: Date.now() }));
        }
      } catch (error) {
        console.error("Message handling error:", error);
      }
    });

    // Handle close
    ws.addEventListener("close", () => {
      this.sessions.delete(ws);
      this.broadcast({
        type: "leave",
        userId,
        timestamp: Date.now(),
      });
    });

    // Handle errors
    ws.addEventListener("error", (event) => {
      console.error("WebSocket error:", event);
      this.sessions.delete(ws);
    });
  }

  private broadcast(message: Message): void {
    const data = JSON.stringify(message);

    for (const [ws] of this.sessions) {
      try {
        ws.send(data);
      } catch {
        // Remove dead connections
        this.sessions.delete(ws);
      }
    }
  }
}

// Worker entry point for WebSocket connections
export async function handleWebSocketUpgrade(
  request: Request,
  env: { WEBSOCKET_ROOM: DurableObjectNamespace },
  roomId: string
): Promise<Response> {
  const id = env.WEBSOCKET_ROOM.idFromName(roomId);
  const room = env.WEBSOCKET_ROOM.get(id);

  const url = new URL(request.url);
  return room.fetch(
    new Request(`http://internal/websocket?${url.searchParams}`, {
      headers: request.headers,
    })
  );
}
```

### Durable Object Alarms

```typescript
// src/durable-objects/scheduled-task.ts
interface ScheduledTask {
  id: string;
  action: string;
  payload: unknown;
  scheduledFor: number;
  createdAt: number;
}

export class ScheduledTaskRunner implements DurableObject {
  private tasks: Map<string, ScheduledTask> = new Map();

  constructor(
    private state: DurableObjectState,
    private env: { WEBHOOK_URL: string }
  ) {
    this.state.blockConcurrencyWhile(async () => {
      const stored = await this.state.storage.list<ScheduledTask>();
      for (const [key, task] of stored) {
        if (key.startsWith("task:")) {
          this.tasks.set(task.id, task);
        }
      }
      // Set alarm for next task
      await this.scheduleNextAlarm();
    });
  }

  async fetch(request: Request): Promise<Response> {
    const url = new URL(request.url);

    switch (url.pathname) {
      case "/schedule":
        return this.handleSchedule(request);
      case "/cancel":
        return this.handleCancel(request);
      case "/list":
        return this.handleList();
      default:
        return new Response("Not Found", { status: 404 });
    }
  }

  async alarm(): Promise<void> {
    const now = Date.now();

    // Find and execute due tasks
    for (const [id, task] of this.tasks) {
      if (task.scheduledFor <= now) {
        await this.executeTask(task);
        this.tasks.delete(id);
        await this.state.storage.delete(`task:${id}`);
      }
    }

    // Schedule next alarm
    await this.scheduleNextAlarm();
  }

  private async handleSchedule(request: Request): Promise<Response> {
    const body = await request.json<{
      action: string;
      payload: unknown;
      delayMs: number;
    }>();

    const task: ScheduledTask = {
      id: crypto.randomUUID(),
      action: body.action,
      payload: body.payload,
      scheduledFor: Date.now() + body.delayMs,
      createdAt: Date.now(),
    };

    this.tasks.set(task.id, task);
    await this.state.storage.put(`task:${task.id}`, task);
    await this.scheduleNextAlarm();

    return new Response(JSON.stringify(task), {
      status: 201,
      headers: { "Content-Type": "application/json" },
    });
  }

  private async handleCancel(request: Request): Promise<Response> {
    const { taskId } = await request.json<{ taskId: string }>();

    if (!this.tasks.has(taskId)) {
      return new Response("Task not found", { status: 404 });
    }

    this.tasks.delete(taskId);
    await this.state.storage.delete(`task:${taskId}`);
    await this.scheduleNextAlarm();

    return new Response("Cancelled");
  }

  private handleList(): Response {
    const tasks = Array.from(this.tasks.values()).sort(
      (a, b) => a.scheduledFor - b.scheduledFor
    );
    return new Response(JSON.stringify(tasks), {
      headers: { "Content-Type": "application/json" },
    });
  }

  private async scheduleNextAlarm(): Promise<void> {
    if (this.tasks.size === 0) {
      await this.state.storage.deleteAlarm();
      return;
    }

    const nextTask = Array.from(this.tasks.values()).reduce((a, b) =>
      a.scheduledFor < b.scheduledFor ? a : b
    );

    await this.state.storage.setAlarm(nextTask.scheduledFor);
  }

  private async executeTask(task: ScheduledTask): Promise<void> {
    try {
      await fetch(this.env.WEBHOOK_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          taskId: task.id,
          action: task.action,
          payload: task.payload,
          executedAt: Date.now(),
        }),
      });
    } catch (error) {
      console.error(`Task ${task.id} execution failed:`, error);
      // Optionally reschedule or move to dead letter queue
    }
  }
}
```

---

## 4. R2 Object Storage

### Upload and Download Operations

```typescript
// src/r2/storage.ts
interface UploadOptions {
  contentType?: string;
  customMetadata?: Record<string, string>;
  httpMetadata?: R2HTTPMetadata;
}

interface PresignedUrlOptions {
  expiresIn: number; // seconds
  contentType?: string;
}

export class ObjectStorage {
  constructor(private bucket: R2Bucket) {}

  // Direct upload
  async upload(
    key: string,
    data: ReadableStream | ArrayBuffer | string,
    options: UploadOptions = {}
  ): Promise<R2Object> {
    return this.bucket.put(key, data, {
      httpMetadata: {
        contentType: options.contentType || "application/octet-stream",
        ...options.httpMetadata,
      },
      customMetadata: options.customMetadata,
    });
  }

  // Multipart upload for large files
  async uploadMultipart(
    key: string,
    stream: ReadableStream<Uint8Array>,
    options: UploadOptions = {}
  ): Promise<R2Object> {
    const multipart = await this.bucket.createMultipartUpload(key, {
      httpMetadata: {
        contentType: options.contentType || "application/octet-stream",
        ...options.httpMetadata,
      },
      customMetadata: options.customMetadata,
    });

    const parts: R2UploadedPart[] = [];
    let partNumber = 1;
    const reader = stream.getReader();
    let buffer = new Uint8Array(0);
    const PART_SIZE = 10 * 1024 * 1024; // 10MB parts

    try {
      while (true) {
        const { done, value } = await reader.read();

        if (value) {
          // Combine with existing buffer
          const newBuffer = new Uint8Array(buffer.length + value.length);
          newBuffer.set(buffer);
          newBuffer.set(value, buffer.length);
          buffer = newBuffer;
        }

        // Upload parts when buffer reaches threshold or stream ends
        while (buffer.length >= PART_SIZE || (done && buffer.length > 0)) {
          const chunk = buffer.slice(0, PART_SIZE);
          buffer = buffer.slice(PART_SIZE);

          const part = await multipart.uploadPart(partNumber, chunk);
          parts.push(part);
          partNumber++;

          if (done && buffer.length === 0) break;
        }

        if (done) break;
      }

      return multipart.complete(parts);
    } catch (error) {
      await multipart.abort();
      throw error;
    }
  }

  // Download as stream
  async download(key: string): Promise<R2ObjectBody | null> {
    return this.bucket.get(key);
  }

  // Download with range support
  async downloadRange(
    key: string,
    start: number,
    end: number
  ): Promise<R2ObjectBody | null> {
    return this.bucket.get(key, {
      range: { offset: start, length: end - start + 1 },
    });
  }

  // Get object metadata only
  async head(key: string): Promise<R2Object | null> {
    return this.bucket.head(key);
  }

  // Delete object
  async delete(key: string): Promise<void> {
    await this.bucket.delete(key);
  }

  // Delete multiple objects
  async deleteMany(keys: string[]): Promise<void> {
    await this.bucket.delete(keys);
  }

  // List objects with pagination
  async list(options: {
    prefix?: string;
    limit?: number;
    cursor?: string;
    delimiter?: string;
  }): Promise<R2Objects> {
    return this.bucket.list(options);
  }

  // Copy object
  async copy(sourceKey: string, destKey: string): Promise<R2Object> {
    const source = await this.bucket.get(sourceKey);
    if (!source) {
      throw new Error(`Source object not found: ${sourceKey}`);
    }

    return this.bucket.put(destKey, source.body, {
      httpMetadata: source.httpMetadata,
      customMetadata: source.customMetadata,
    });
  }
}
```

### Presigned URLs with Workers

```typescript
// src/r2/presigned.ts
import { AwsClient } from "aws4fetch";

interface R2Credentials {
  accessKeyId: string;
  secretAccessKey: string;
  accountId: string;
  bucketName: string;
}

export class PresignedUrlGenerator {
  private aws: AwsClient;
  private bucketUrl: string;

  constructor(private credentials: R2Credentials) {
    this.aws = new AwsClient({
      accessKeyId: credentials.accessKeyId,
      secretAccessKey: credentials.secretAccessKey,
      service: "s3",
      region: "auto",
    });
    this.bucketUrl = `https://${credentials.accountId}.r2.cloudflarestorage.com/${credentials.bucketName}`;
  }

  // Generate presigned URL for download
  async getDownloadUrl(
    key: string,
    expiresIn: number = 3600
  ): Promise<string> {
    const url = new URL(`${this.bucketUrl}/${encodeURIComponent(key)}`);
    url.searchParams.set("X-Amz-Expires", String(expiresIn));

    const signed = await this.aws.sign(
      new Request(url.toString(), { method: "GET" }),
      { aws: { signQuery: true } }
    );

    return signed.url;
  }

  // Generate presigned URL for upload
  async getUploadUrl(
    key: string,
    contentType: string,
    expiresIn: number = 3600
  ): Promise<{ url: string; fields: Record<string, string> }> {
    const url = new URL(`${this.bucketUrl}/${encodeURIComponent(key)}`);
    url.searchParams.set("X-Amz-Expires", String(expiresIn));

    const signed = await this.aws.sign(
      new Request(url.toString(), {
        method: "PUT",
        headers: { "Content-Type": contentType },
      }),
      { aws: { signQuery: true } }
    );

    return {
      url: signed.url,
      fields: { "Content-Type": contentType },
    };
  }
}

// File upload handler
export async function handleFileUpload(
  request: Request,
  env: {
    STORAGE: R2Bucket;
    R2_ACCESS_KEY_ID: string;
    R2_SECRET_ACCESS_KEY: string;
    ACCOUNT_ID: string;
  }
): Promise<Response> {
  const formData = await request.formData();
  const file = formData.get("file") as File | null;

  if (!file) {
    return new Response(JSON.stringify({ error: "No file provided" }), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }

  // Validate file
  const maxSize = 100 * 1024 * 1024; // 100MB
  if (file.size > maxSize) {
    return new Response(JSON.stringify({ error: "File too large" }), {
      status: 413,
      headers: { "Content-Type": "application/json" },
    });
  }

  const allowedTypes = ["image/jpeg", "image/png", "image/webp", "application/pdf"];
  if (!allowedTypes.includes(file.type)) {
    return new Response(JSON.stringify({ error: "Invalid file type" }), {
      status: 415,
      headers: { "Content-Type": "application/json" },
    });
  }

  // Generate unique key
  const ext = file.name.split(".").pop() || "bin";
  const key = `uploads/${Date.now()}-${crypto.randomUUID()}.${ext}`;

  // Upload to R2
  const storage = new ObjectStorage(env.STORAGE);
  await storage.upload(key, file.stream(), {
    contentType: file.type,
    customMetadata: {
      originalName: file.name,
      uploadedAt: new Date().toISOString(),
    },
  });

  // Generate download URL
  const presigner = new PresignedUrlGenerator({
    accessKeyId: env.R2_ACCESS_KEY_ID,
    secretAccessKey: env.R2_SECRET_ACCESS_KEY,
    accountId: env.ACCOUNT_ID,
    bucketName: "my-bucket",
  });

  const downloadUrl = await presigner.getDownloadUrl(key, 86400);

  return new Response(
    JSON.stringify({
      key,
      downloadUrl,
      size: file.size,
      contentType: file.type,
    }),
    {
      status: 201,
      headers: { "Content-Type": "application/json" },
    }
  );
}
```

---

## 5. D1 Database

### Schema and Migrations

```typescript
// migrations/0001_initial.sql
-- Users table
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  password_hash TEXT NOT NULL,
  created_at INTEGER DEFAULT (unixepoch()),
  updated_at INTEGER DEFAULT (unixepoch())
);

CREATE INDEX idx_users_email ON users(email);

-- Posts table
CREATE TABLE IF NOT EXISTS posts (
  id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  slug TEXT UNIQUE NOT NULL,
  content TEXT NOT NULL,
  published INTEGER DEFAULT 0,
  created_at INTEGER DEFAULT (unixepoch()),
  updated_at INTEGER DEFAULT (unixepoch())
);

CREATE INDEX idx_posts_user_id ON posts(user_id);
CREATE INDEX idx_posts_slug ON posts(slug);
CREATE INDEX idx_posts_published ON posts(published);

-- Comments table
CREATE TABLE IF NOT EXISTS comments (
  id TEXT PRIMARY KEY DEFAULT (lower(hex(randomblob(16)))),
  post_id TEXT NOT NULL REFERENCES posts(id) ON DELETE CASCADE,
  user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  created_at INTEGER DEFAULT (unixepoch())
);

CREATE INDEX idx_comments_post_id ON comments(post_id);

-- Trigger for updated_at
CREATE TRIGGER update_users_timestamp
  AFTER UPDATE ON users
BEGIN
  UPDATE users SET updated_at = unixepoch() WHERE id = NEW.id;
END;

CREATE TRIGGER update_posts_timestamp
  AFTER UPDATE ON posts
BEGIN
  UPDATE posts SET updated_at = unixepoch() WHERE id = NEW.id;
END;
```

### Type-Safe Database Layer

```typescript
// src/db/types.ts
interface User {
  id: string;
  email: string;
  name: string;
  password_hash: string;
  created_at: number;
  updated_at: number;
}

interface Post {
  id: string;
  user_id: string;
  title: string;
  slug: string;
  content: string;
  published: number;
  created_at: number;
  updated_at: number;
}

interface Comment {
  id: string;
  post_id: string;
  user_id: string;
  content: string;
  created_at: number;
}

// src/db/repository.ts
export class Database {
  constructor(private db: D1Database) {}

  // Users
  async createUser(data: {
    email: string;
    name: string;
    passwordHash: string;
  }): Promise<User> {
    const result = await this.db
      .prepare(
        `INSERT INTO users (email, name, password_hash)
         VALUES (?, ?, ?)
         RETURNING *`
      )
      .bind(data.email, data.name, data.passwordHash)
      .first<User>();

    if (!result) {
      throw new Error("Failed to create user");
    }
    return result;
  }

  async getUserById(id: string): Promise<User | null> {
    return this.db
      .prepare("SELECT * FROM users WHERE id = ?")
      .bind(id)
      .first<User>();
  }

  async getUserByEmail(email: string): Promise<User | null> {
    return this.db
      .prepare("SELECT * FROM users WHERE email = ?")
      .bind(email)
      .first<User>();
  }

  // Posts
  async createPost(data: {
    userId: string;
    title: string;
    slug: string;
    content: string;
  }): Promise<Post> {
    const result = await this.db
      .prepare(
        `INSERT INTO posts (user_id, title, slug, content)
         VALUES (?, ?, ?, ?)
         RETURNING *`
      )
      .bind(data.userId, data.title, data.slug, data.content)
      .first<Post>();

    if (!result) {
      throw new Error("Failed to create post");
    }
    return result;
  }

  async getPostBySlug(slug: string): Promise<Post | null> {
    return this.db
      .prepare("SELECT * FROM posts WHERE slug = ?")
      .bind(slug)
      .first<Post>();
  }

  async getPublishedPosts(
    limit: number = 10,
    offset: number = 0
  ): Promise<Post[]> {
    const result = await this.db
      .prepare(
        `SELECT * FROM posts
         WHERE published = 1
         ORDER BY created_at DESC
         LIMIT ? OFFSET ?`
      )
      .bind(limit, offset)
      .all<Post>();

    return result.results;
  }

  async getPostsByUser(
    userId: string,
    includeUnpublished: boolean = false
  ): Promise<Post[]> {
    const query = includeUnpublished
      ? "SELECT * FROM posts WHERE user_id = ? ORDER BY created_at DESC"
      : "SELECT * FROM posts WHERE user_id = ? AND published = 1 ORDER BY created_at DESC";

    const result = await this.db
      .prepare(query)
      .bind(userId)
      .all<Post>();

    return result.results;
  }

  async updatePost(
    id: string,
    data: Partial<Pick<Post, "title" | "content" | "published">>
  ): Promise<Post | null> {
    const updates: string[] = [];
    const values: unknown[] = [];

    if (data.title !== undefined) {
      updates.push("title = ?");
      values.push(data.title);
    }
    if (data.content !== undefined) {
      updates.push("content = ?");
      values.push(data.content);
    }
    if (data.published !== undefined) {
      updates.push("published = ?");
      values.push(data.published);
    }

    if (updates.length === 0) {
      return this.getPostById(id);
    }

    values.push(id);

    return this.db
      .prepare(
        `UPDATE posts SET ${updates.join(", ")} WHERE id = ? RETURNING *`
      )
      .bind(...values)
      .first<Post>();
  }

  async getPostById(id: string): Promise<Post | null> {
    return this.db
      .prepare("SELECT * FROM posts WHERE id = ?")
      .bind(id)
      .first<Post>();
  }

  async deletePost(id: string): Promise<boolean> {
    const result = await this.db
      .prepare("DELETE FROM posts WHERE id = ?")
      .bind(id)
      .run();

    return result.meta.changes > 0;
  }

  // Comments with joins
  async getCommentsForPost(postId: string): Promise<
    Array<
      Comment & {
        user_name: string;
        user_email: string;
      }
    >
  > {
    const result = await this.db
      .prepare(
        `SELECT c.*, u.name as user_name, u.email as user_email
         FROM comments c
         JOIN users u ON c.user_id = u.id
         WHERE c.post_id = ?
         ORDER BY c.created_at ASC`
      )
      .bind(postId)
      .all();

    return result.results as Array<
      Comment & { user_name: string; user_email: string }
    >;
  }

  // Batch operations
  async batchInsert<T>(
    table: string,
    columns: string[],
    rows: T[][]
  ): Promise<void> {
    const placeholders = columns.map(() => "?").join(", ");
    const stmt = this.db.prepare(
      `INSERT INTO ${table} (${columns.join(", ")}) VALUES (${placeholders})`
    );

    const batch = rows.map((row) => stmt.bind(...row));
    await this.db.batch(batch);
  }

  // Transaction-like pattern (D1 batch)
  async transferOwnership(
    postId: string,
    fromUserId: string,
    toUserId: string
  ): Promise<void> {
    const statements = [
      this.db
        .prepare("UPDATE posts SET user_id = ? WHERE id = ? AND user_id = ?")
        .bind(toUserId, postId, fromUserId),
      this.db
        .prepare(
          `INSERT INTO audit_log (action, entity_type, entity_id, from_user, to_user)
           VALUES ('transfer', 'post', ?, ?, ?)`
        )
        .bind(postId, fromUserId, toUserId),
    ];

    await this.db.batch(statements);
  }

  // Full-text search (SQLite FTS5)
  async searchPosts(query: string, limit: number = 10): Promise<Post[]> {
    // Requires FTS5 virtual table setup
    const result = await this.db
      .prepare(
        `SELECT posts.* FROM posts
         JOIN posts_fts ON posts.id = posts_fts.id
         WHERE posts_fts MATCH ?
         ORDER BY rank
         LIMIT ?`
      )
      .bind(query, limit)
      .all<Post>();

    return result.results;
  }
}
```

### Migration Runner

```typescript
// src/db/migrate.ts
interface Migration {
  version: number;
  name: string;
  up: string;
  down?: string;
}

export class MigrationRunner {
  constructor(private db: D1Database) {}

  async initialize(): Promise<void> {
    await this.db
      .prepare(
        `CREATE TABLE IF NOT EXISTS _migrations (
          version INTEGER PRIMARY KEY,
          name TEXT NOT NULL,
          applied_at INTEGER DEFAULT (unixepoch())
        )`
      )
      .run();
  }

  async getAppliedVersions(): Promise<number[]> {
    const result = await this.db
      .prepare("SELECT version FROM _migrations ORDER BY version")
      .all<{ version: number }>();
    return result.results.map((r) => r.version);
  }

  async migrate(migrations: Migration[]): Promise<string[]> {
    await this.initialize();

    const applied = await this.getAppliedVersions();
    const pending = migrations
      .filter((m) => !applied.includes(m.version))
      .sort((a, b) => a.version - b.version);

    const results: string[] = [];

    for (const migration of pending) {
      try {
        // Execute migration
        await this.db.exec(migration.up);

        // Record migration
        await this.db
          .prepare(
            "INSERT INTO _migrations (version, name) VALUES (?, ?)"
          )
          .bind(migration.version, migration.name)
          .run();

        results.push(`Applied: ${migration.version} - ${migration.name}`);
      } catch (error) {
        results.push(
          `Failed: ${migration.version} - ${migration.name}: ${error}`
        );
        throw error;
      }
    }

    if (results.length === 0) {
      results.push("No pending migrations");
    }

    return results;
  }

  async rollback(migrations: Migration[], steps: number = 1): Promise<string[]> {
    const applied = await this.getAppliedVersions();
    const toRollback = applied.slice(-steps).reverse();

    const results: string[] = [];

    for (const version of toRollback) {
      const migration = migrations.find((m) => m.version === version);
      if (!migration?.down) {
        results.push(`Skip: ${version} - no down migration`);
        continue;
      }

      try {
        await this.db.exec(migration.down);
        await this.db
          .prepare("DELETE FROM _migrations WHERE version = ?")
          .bind(version)
          .run();

        results.push(`Rolled back: ${version} - ${migration.name}`);
      } catch (error) {
        results.push(`Failed: ${version} - ${error}`);
        throw error;
      }
    }

    return results;
  }
}
```

---

## 6. Vercel Edge Functions

### Edge Middleware

```typescript
// middleware.ts
import { NextResponse, type NextRequest } from "next/server";

export const config = {
  matcher: [
    // Match all paths except static files
    "/((?!_next/static|_next/image|favicon.ico|public/).*)",
  ],
};

// Rate limiting state (in-memory for single region)
const rateLimitMap = new Map<string, { count: number; resetAt: number }>();

export async function middleware(request: NextRequest) {
  const response = NextResponse.next();
  const startTime = Date.now();

  // Add request ID
  const requestId = crypto.randomUUID();
  response.headers.set("X-Request-ID", requestId);

  // Rate limiting
  const ip = request.ip || request.headers.get("x-forwarded-for") || "unknown";
  const rateLimitResult = checkRateLimit(ip, 100, 60000);

  if (!rateLimitResult.allowed) {
    return new NextResponse(
      JSON.stringify({
        error: "Too Many Requests",
        retryAfter: rateLimitResult.retryAfter,
      }),
      {
        status: 429,
        headers: {
          "Content-Type": "application/json",
          "Retry-After": String(rateLimitResult.retryAfter),
          "X-RateLimit-Limit": "100",
          "X-RateLimit-Remaining": "0",
        },
      }
    );
  }

  response.headers.set(
    "X-RateLimit-Remaining",
    String(rateLimitResult.remaining)
  );

  // Geolocation-based routing
  const country = request.geo?.country || "US";
  const city = request.geo?.city || "Unknown";

  response.headers.set("X-Geo-Country", country);
  response.headers.set("X-Geo-City", city);

  // Bot detection
  const userAgent = request.headers.get("user-agent") || "";
  if (isBot(userAgent)) {
    response.headers.set("X-Bot-Detected", "true");
    // Could redirect to cached version or block
  }

  // A/B testing
  let variant = request.cookies.get("ab-variant")?.value;
  if (!variant) {
    variant = Math.random() < 0.5 ? "control" : "experiment";
    response.cookies.set("ab-variant", variant, {
      maxAge: 60 * 60 * 24 * 30, // 30 days
      httpOnly: true,
      sameSite: "lax",
    });
  }
  response.headers.set("X-AB-Variant", variant);

  // Authentication check for protected routes
  if (request.nextUrl.pathname.startsWith("/dashboard")) {
    const token = request.cookies.get("auth-token")?.value;
    if (!token) {
      const loginUrl = new URL("/login", request.url);
      loginUrl.searchParams.set("redirect", request.nextUrl.pathname);
      return NextResponse.redirect(loginUrl);
    }

    // Verify token (lightweight check at edge)
    const isValid = await verifyTokenAtEdge(token);
    if (!isValid) {
      return NextResponse.redirect(new URL("/login", request.url));
    }
  }

  // Response timing
  response.headers.set("X-Response-Time", `${Date.now() - startTime}ms`);

  return response;
}

function checkRateLimit(
  key: string,
  maxRequests: number,
  windowMs: number
): { allowed: boolean; remaining: number; retryAfter?: number } {
  const now = Date.now();
  const record = rateLimitMap.get(key);

  if (!record || now > record.resetAt) {
    rateLimitMap.set(key, { count: 1, resetAt: now + windowMs });
    return { allowed: true, remaining: maxRequests - 1 };
  }

  if (record.count >= maxRequests) {
    return {
      allowed: false,
      remaining: 0,
      retryAfter: Math.ceil((record.resetAt - now) / 1000),
    };
  }

  record.count++;
  return { allowed: true, remaining: maxRequests - record.count };
}

function isBot(userAgent: string): boolean {
  const botPatterns = [
    /bot/i,
    /crawler/i,
    /spider/i,
    /scraper/i,
    /headless/i,
    /puppeteer/i,
    /playwright/i,
  ];
  return botPatterns.some((pattern) => pattern.test(userAgent));
}

async function verifyTokenAtEdge(token: string): Promise<boolean> {
  try {
    // Lightweight JWT verification
    const [, payload] = token.split(".");
    if (!payload) return false;

    const decoded = JSON.parse(atob(payload));
    return decoded.exp > Date.now() / 1000;
  } catch {
    return false;
  }
}
```

### Edge API Routes

```typescript
// app/api/edge/route.ts
import { NextRequest, NextResponse } from "next/server";

export const runtime = "edge";
export const preferredRegion = ["iad1", "sfo1", "fra1"]; // US East, US West, Frankfurt

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url);
  const query = searchParams.get("q");

  // Access geo data
  const geo = request.geo;
  const country = geo?.country || "unknown";
  const region = geo?.region || "unknown";

  // Fetch from origin with caching
  const cacheKey = `search:${query}:${country}`;

  // Using fetch with cache control
  const response = await fetch(
    `https://api.origin.com/search?q=${encodeURIComponent(query || "")}`,
    {
      headers: {
        "X-Country": country,
        "X-Region": region,
      },
      next: {
        revalidate: 60, // Cache for 60 seconds
        tags: [`search-${query}`],
      },
    }
  );

  const data = await response.json();

  return NextResponse.json(data, {
    headers: {
      "Cache-Control": "public, s-maxage=60, stale-while-revalidate=300",
      "CDN-Cache-Control": "public, max-age=60",
      "Vercel-CDN-Cache-Control": "public, max-age=3600",
    },
  });
}

export async function POST(request: NextRequest) {
  const body = await request.json();

  // Validate at edge
  if (!body.email || !isValidEmail(body.email)) {
    return NextResponse.json(
      { error: "Invalid email" },
      { status: 400 }
    );
  }

  // Forward to origin
  const response = await fetch("https://api.origin.com/subscribe", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Forwarded-For": request.ip || "",
    },
    body: JSON.stringify(body),
  });

  const result = await response.json();

  return NextResponse.json(result, {
    status: response.status,
  });
}

function isValidEmail(email: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```

### Edge Config Integration

```typescript
// lib/edge-config.ts
import { get, getAll, has } from "@vercel/edge-config";

interface FeatureFlags {
  newCheckoutFlow: boolean;
  darkModeDefault: boolean;
  maintenanceMode: boolean;
  apiRateLimit: number;
}

interface EdgeConfigData {
  features: FeatureFlags;
  allowedOrigins: string[];
  blockedIPs: string[];
}

export async function getFeatureFlags(): Promise<FeatureFlags> {
  const flags = await get<FeatureFlags>("features");
  return (
    flags || {
      newCheckoutFlow: false,
      darkModeDefault: false,
      maintenanceMode: false,
      apiRateLimit: 100,
    }
  );
}

export async function isIPBlocked(ip: string): Promise<boolean> {
  const blockedIPs = await get<string[]>("blockedIPs");
  return blockedIPs?.includes(ip) || false;
}

export async function getAllConfig(): Promise<EdgeConfigData | undefined> {
  return getAll<EdgeConfigData>();
}

// Usage in middleware
import { getFeatureFlags, isIPBlocked } from "@/lib/edge-config";

export async function middleware(request: NextRequest) {
  const ip = request.ip || "";

  // Check IP blocklist
  if (await isIPBlocked(ip)) {
    return new NextResponse("Forbidden", { status: 403 });
  }

  // Check maintenance mode
  const flags = await getFeatureFlags();
  if (flags.maintenanceMode) {
    return NextResponse.rewrite(new URL("/maintenance", request.url));
  }

  return NextResponse.next();
}
```

---

## 7. Common Patterns

### CORS Handler

```typescript
// src/middleware/cors.ts
interface CorsOptions {
  origins: string[] | "*";
  methods?: string[];
  headers?: string[];
  exposeHeaders?: string[];
  maxAge?: number;
  credentials?: boolean;
}

export function createCorsHandler(options: CorsOptions) {
  const {
    origins,
    methods = ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    headers = ["Content-Type", "Authorization"],
    exposeHeaders = [],
    maxAge = 86400,
    credentials = true,
  } = options;

  function isOriginAllowed(origin: string): boolean {
    if (origins === "*") return true;
    return origins.includes(origin);
  }

  function getCorsHeaders(origin: string): Headers {
    const corsHeaders = new Headers();

    if (isOriginAllowed(origin)) {
      corsHeaders.set(
        "Access-Control-Allow-Origin",
        origins === "*" ? "*" : origin
      );
    }

    corsHeaders.set("Access-Control-Allow-Methods", methods.join(", "));
    corsHeaders.set("Access-Control-Allow-Headers", headers.join(", "));
    corsHeaders.set("Access-Control-Max-Age", String(maxAge));

    if (exposeHeaders.length > 0) {
      corsHeaders.set(
        "Access-Control-Expose-Headers",
        exposeHeaders.join(", ")
      );
    }

    if (credentials && origins !== "*") {
      corsHeaders.set("Access-Control-Allow-Credentials", "true");
    }

    return corsHeaders;
  }

  return {
    handlePreflight(request: Request): Response {
      const origin = request.headers.get("Origin") || "";
      const corsHeaders = getCorsHeaders(origin);

      return new Response(null, {
        status: 204,
        headers: corsHeaders,
      });
    },

    addCorsHeaders(response: Response, origin: string): Response {
      const corsHeaders = getCorsHeaders(origin);
      const newResponse = new Response(response.body, response);

      for (const [key, value] of corsHeaders.entries()) {
        newResponse.headers.set(key, value);
      }

      return newResponse;
    },
  };
}

// Usage
const cors = createCorsHandler({
  origins: ["https://app.example.com", "https://example.com"],
  credentials: true,
});

export default {
  async fetch(request: Request): Promise<Response> {
    const origin = request.headers.get("Origin") || "";

    // Handle preflight
    if (request.method === "OPTIONS") {
      return cors.handlePreflight(request);
    }

    // Process request
    const response = await handleRequest(request);

    // Add CORS headers
    return cors.addCorsHeaders(response, origin);
  },
};
```

### Rate Limiting Middleware

```typescript
// src/middleware/rate-limit.ts
interface RateLimitOptions {
  maxRequests: number;
  windowMs: number;
  keyGenerator?: (request: Request) => string;
  handler?: (request: Request) => Response;
}

// In-memory rate limiter (for single instance)
class InMemoryRateLimiter {
  private windows: Map<string, { count: number; resetAt: number }> =
    new Map();

  check(key: string, max: number, windowMs: number): {
    allowed: boolean;
    remaining: number;
    resetAt: number;
  } {
    const now = Date.now();
    const record = this.windows.get(key);

    // Cleanup old entries periodically
    if (this.windows.size > 10000) {
      this.cleanup(now);
    }

    if (!record || now > record.resetAt) {
      this.windows.set(key, { count: 1, resetAt: now + windowMs });
      return { allowed: true, remaining: max - 1, resetAt: now + windowMs };
    }

    if (record.count >= max) {
      return { allowed: false, remaining: 0, resetAt: record.resetAt };
    }

    record.count++;
    return {
      allowed: true,
      remaining: max - record.count,
      resetAt: record.resetAt,
    };
  }

  private cleanup(now: number): void {
    for (const [key, record] of this.windows.entries()) {
      if (now > record.resetAt) {
        this.windows.delete(key);
      }
    }
  }
}

// Durable Object rate limiter (distributed)
export async function checkRateLimitDO(
  env: { RATE_LIMITER: DurableObjectNamespace },
  key: string
): Promise<{ allowed: boolean; remaining: number; resetAt: number }> {
  const id = env.RATE_LIMITER.idFromName(key);
  const stub = env.RATE_LIMITER.get(id);
  const response = await stub.fetch("http://internal/check");
  return response.json();
}

// KV-based rate limiter (eventually consistent)
export async function checkRateLimitKV(
  kv: KVNamespace,
  key: string,
  max: number,
  windowMs: number
): Promise<{ allowed: boolean; remaining: number; resetAt: number }> {
  const now = Date.now();
  const windowKey = `ratelimit:${key}:${Math.floor(now / windowMs)}`;

  const current = parseInt((await kv.get(windowKey)) || "0", 10);

  if (current >= max) {
    return {
      allowed: false,
      remaining: 0,
      resetAt: Math.ceil(now / windowMs) * windowMs,
    };
  }

  // Increment (fire and forget for performance)
  kv.put(windowKey, String(current + 1), {
    expirationTtl: Math.ceil(windowMs / 1000),
  });

  return {
    allowed: true,
    remaining: max - current - 1,
    resetAt: Math.ceil(now / windowMs) * windowMs,
  };
}

// Middleware factory
export function createRateLimiter(options: RateLimitOptions) {
  const limiter = new InMemoryRateLimiter();

  const keyGenerator =
    options.keyGenerator ||
    ((req: Request) => req.headers.get("CF-Connecting-IP") || "unknown");

  const handler =
    options.handler ||
    ((req: Request) =>
      new Response(JSON.stringify({ error: "Too Many Requests" }), {
        status: 429,
        headers: { "Content-Type": "application/json" },
      }));

  return async function rateLimitMiddleware(
    request: Request,
    next: () => Promise<Response>
  ): Promise<Response> {
    const key = keyGenerator(request);
    const result = limiter.check(
      key,
      options.maxRequests,
      options.windowMs
    );

    if (!result.allowed) {
      const response = handler(request);
      response.headers.set(
        "Retry-After",
        String(Math.ceil((result.resetAt - Date.now()) / 1000))
      );
      return response;
    }

    const response = await next();

    // Add rate limit headers
    response.headers.set(
      "X-RateLimit-Limit",
      String(options.maxRequests)
    );
    response.headers.set(
      "X-RateLimit-Remaining",
      String(result.remaining)
    );
    response.headers.set(
      "X-RateLimit-Reset",
      String(Math.floor(result.resetAt / 1000))
    );

    return response;
  };
}
```

### JWT Authentication

```typescript
// src/auth/jwt.ts
interface JWTPayload {
  sub: string;
  iat: number;
  exp: number;
  [key: string]: unknown;
}

export class JWTAuth {
  constructor(private secret: string) {}

  async sign(
    payload: Omit<JWTPayload, "iat" | "exp">,
    expiresIn: number = 3600
  ): Promise<string> {
    const header = { alg: "HS256", typ: "JWT" };
    const now = Math.floor(Date.now() / 1000);

    const fullPayload: JWTPayload = {
      ...payload,
      iat: now,
      exp: now + expiresIn,
    };

    const encodedHeader = this.base64UrlEncode(JSON.stringify(header));
    const encodedPayload = this.base64UrlEncode(
      JSON.stringify(fullPayload)
    );
    const signature = await this.createSignature(
      `${encodedHeader}.${encodedPayload}`
    );

    return `${encodedHeader}.${encodedPayload}.${signature}`;
  }

  async verify(token: string): Promise<JWTPayload | null> {
    try {
      const [encodedHeader, encodedPayload, signature] = token.split(".");
      if (!encodedHeader || !encodedPayload || !signature) {
        return null;
      }

      // Verify signature
      const expectedSignature = await this.createSignature(
        `${encodedHeader}.${encodedPayload}`
      );
      if (signature !== expectedSignature) {
        return null;
      }

      // Decode payload
      const payload: JWTPayload = JSON.parse(
        this.base64UrlDecode(encodedPayload)
      );

      // Check expiration
      if (payload.exp < Math.floor(Date.now() / 1000)) {
        return null;
      }

      return payload;
    } catch {
      return null;
    }
  }

  private async createSignature(data: string): Promise<string> {
    const encoder = new TextEncoder();
    const key = await crypto.subtle.importKey(
      "raw",
      encoder.encode(this.secret),
      { name: "HMAC", hash: "SHA-256" },
      false,
      ["sign"]
    );

    const signature = await crypto.subtle.sign(
      "HMAC",
      key,
      encoder.encode(data)
    );

    return this.base64UrlEncode(
      String.fromCharCode(...new Uint8Array(signature))
    );
  }

  private base64UrlEncode(str: string): string {
    return btoa(str).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  }

  private base64UrlDecode(str: string): string {
    const padded = str + "=".repeat((4 - (str.length % 4)) % 4);
    return atob(padded.replace(/-/g, "+").replace(/_/g, "/"));
  }
}

// Auth middleware
export function createAuthMiddleware(jwt: JWTAuth) {
  return async function authMiddleware(
    request: Request,
    next: () => Promise<Response>
  ): Promise<Response> {
    const authHeader = request.headers.get("Authorization");
    if (!authHeader?.startsWith("Bearer ")) {
      return new Response(
        JSON.stringify({ error: "Missing authorization header" }),
        { status: 401, headers: { "Content-Type": "application/json" } }
      );
    }

    const token = authHeader.slice(7);
    const payload = await jwt.verify(token);

    if (!payload) {
      return new Response(
        JSON.stringify({ error: "Invalid or expired token" }),
        { status: 401, headers: { "Content-Type": "application/json" } }
      );
    }

    // Attach user to request (via headers for Workers)
    const modifiedRequest = new Request(request, {
      headers: new Headers(request.headers),
    });
    modifiedRequest.headers.set("X-User-ID", payload.sub);
    modifiedRequest.headers.set("X-User-Data", JSON.stringify(payload));

    return next();
  };
}
```

### A/B Testing

```typescript
// src/ab/testing.ts
interface Experiment {
  id: string;
  name: string;
  variants: {
    id: string;
    weight: number; // 0-100
  }[];
  startDate?: Date;
  endDate?: Date;
}

interface Assignment {
  experimentId: string;
  variantId: string;
  assignedAt: number;
}

export class ABTestingService {
  constructor(private kv: KVNamespace) {}

  async getAssignment(
    userId: string,
    experiment: Experiment
  ): Promise<Assignment> {
    // Check for existing assignment
    const key = `ab:${experiment.id}:${userId}`;
    const existing = await this.kv.get<Assignment>(key, "json");

    if (existing) {
      return existing;
    }

    // Check if experiment is active
    const now = Date.now();
    if (experiment.startDate && experiment.startDate.getTime() > now) {
      return this.createAssignment(
        experiment.id,
        experiment.variants[0].id
      );
    }
    if (experiment.endDate && experiment.endDate.getTime() < now) {
      return this.createAssignment(
        experiment.id,
        experiment.variants[0].id
      );
    }

    // Assign variant based on weights
    const variantId = this.selectVariant(experiment.variants, userId);
    const assignment = this.createAssignment(experiment.id, variantId);

    // Store assignment
    await this.kv.put(key, JSON.stringify(assignment), {
      expirationTtl: 60 * 60 * 24 * 30, // 30 days
    });

    return assignment;
  }

  private selectVariant(
    variants: Experiment["variants"],
    userId: string
  ): string {
    // Deterministic assignment based on user ID hash
    const hash = this.hashString(userId);
    const bucket = hash % 100;

    let cumulative = 0;
    for (const variant of variants) {
      cumulative += variant.weight;
      if (bucket < cumulative) {
        return variant.id;
      }
    }

    return variants[variants.length - 1].id;
  }

  private hashString(str: string): number {
    let hash = 0;
    for (let i = 0; i < str.length; i++) {
      const char = str.charCodeAt(i);
      hash = (hash << 5) - hash + char;
      hash = hash & hash;
    }
    return Math.abs(hash);
  }

  private createAssignment(
    experimentId: string,
    variantId: string
  ): Assignment {
    return {
      experimentId,
      variantId,
      assignedAt: Date.now(),
    };
  }

  // Track conversion
  async trackConversion(
    userId: string,
    experimentId: string,
    metric: string
  ): Promise<void> {
    const key = `ab:conversion:${experimentId}:${metric}`;
    const assignment = await this.kv.get<Assignment>(
      `ab:${experimentId}:${userId}`,
      "json"
    );

    if (!assignment) return;

    // Increment conversion counter for variant
    const counterKey = `${key}:${assignment.variantId}`;
    const current = parseInt((await this.kv.get(counterKey)) || "0", 10);
    await this.kv.put(counterKey, String(current + 1));
  }
}

// Edge middleware for A/B testing
export function createABMiddleware(
  experiments: Experiment[],
  kv: KVNamespace
) {
  const abService = new ABTestingService(kv);

  return async function abMiddleware(
    request: Request,
    next: () => Promise<Response>
  ): Promise<Response> {
    // Get or create user ID
    const cookies = parseCookies(request.headers.get("Cookie") || "");
    let userId = cookies["user_id"];
    const isNewUser = !userId;

    if (!userId) {
      userId = crypto.randomUUID();
    }

    // Get assignments for all experiments
    const assignments: Record<string, string> = {};
    for (const experiment of experiments) {
      const assignment = await abService.getAssignment(userId, experiment);
      assignments[experiment.id] = assignment.variantId;
    }

    // Add to request headers
    const modifiedRequest = new Request(request, {
      headers: new Headers(request.headers),
    });
    modifiedRequest.headers.set(
      "X-AB-Assignments",
      JSON.stringify(assignments)
    );

    const response = await next();

    // Set user ID cookie if new
    if (isNewUser) {
      const newResponse = new Response(response.body, response);
      newResponse.headers.append(
        "Set-Cookie",
        `user_id=${userId}; Path=/; Max-Age=31536000; HttpOnly; SameSite=Lax`
      );
      return newResponse;
    }

    return response;
  };
}

function parseCookies(cookieHeader: string): Record<string, string> {
  return Object.fromEntries(
    cookieHeader.split(";").map((c) => {
      const [key, ...val] = c.trim().split("=");
      return [key, val.join("=")];
    })
  );
}
```

---

## 8. Performance Optimization

### Bundle Size Optimization

```typescript
// wrangler.toml
# Use esbuild for smaller bundles
[build]
command = "esbuild src/index.ts --bundle --minify --format=esm --outfile=dist/index.js"

# Or use custom build with tree shaking
[build]
command = "npm run build"
```

```typescript
// esbuild.config.js
const esbuild = require("esbuild");

esbuild.build({
  entryPoints: ["src/index.ts"],
  bundle: true,
  minify: true,
  format: "esm",
  target: "es2022",
  outfile: "dist/index.js",
  treeShaking: true,
  // Exclude node built-ins that aren't needed
  external: [],
  // Define constants for dead code elimination
  define: {
    "process.env.NODE_ENV": '"production"',
  },
  // Analyze bundle size
  metafile: true,
}).then((result) => {
  // Output bundle analysis
  const text = esbuild.analyzeMetafileSync(result.metafile);
  console.log(text);
});
```

### Streaming Responses

```typescript
// src/streaming.ts
export function streamResponse(
  generator: AsyncGenerator<string>,
  headers: Record<string, string> = {}
): Response {
  const encoder = new TextEncoder();

  const stream = new ReadableStream({
    async start(controller) {
      try {
        for await (const chunk of generator) {
          controller.enqueue(encoder.encode(chunk));
        }
        controller.close();
      } catch (error) {
        controller.error(error);
      }
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
      Connection: "keep-alive",
      ...headers,
    },
  });
}

// Server-Sent Events
export function createSSEStream(): {
  stream: ReadableStream;
  send: (event: string, data: unknown) => void;
  close: () => void;
} {
  const encoder = new TextEncoder();
  let controller: ReadableStreamDefaultController;

  const stream = new ReadableStream({
    start(c) {
      controller = c;
    },
  });

  return {
    stream,
    send(event: string, data: unknown) {
      const message = `event: ${event}\ndata: ${JSON.stringify(data)}\n\n`;
      controller.enqueue(encoder.encode(message));
    },
    close() {
      controller.close();
    },
  };
}

// Usage
app.get("/stream", async (c) => {
  const sse = createSSEStream();

  // Start background task
  c.executionCtx.waitUntil(
    (async () => {
      for (let i = 0; i < 10; i++) {
        await sleep(1000);
        sse.send("update", { count: i });
      }
      sse.close();
    })()
  );

  return new Response(sse.stream, {
    headers: {
      "Content-Type": "text/event-stream",
      "Cache-Control": "no-cache",
    },
  });
});
```

### Smart Caching

```typescript
// src/cache/smart-cache.ts
interface CacheStrategy {
  ttl: number;
  staleWhileRevalidate?: number;
  tags?: string[];
}

const CACHE_STRATEGIES: Record<string, CacheStrategy> = {
  static: { ttl: 86400, staleWhileRevalidate: 604800 }, // 1 day, 1 week SWR
  dynamic: { ttl: 60, staleWhileRevalidate: 300 }, // 1 min, 5 min SWR
  user: { ttl: 0 }, // No caching
  api: { ttl: 10, staleWhileRevalidate: 60 }, // 10 sec, 1 min SWR
};

export function getCacheHeaders(strategy: keyof typeof CACHE_STRATEGIES): Headers {
  const config = CACHE_STRATEGIES[strategy];
  const headers = new Headers();

  if (config.ttl === 0) {
    headers.set(
      "Cache-Control",
      "private, no-cache, no-store, must-revalidate"
    );
    return headers;
  }

  let cacheControl = `public, max-age=${config.ttl}`;

  if (config.staleWhileRevalidate) {
    cacheControl += `, stale-while-revalidate=${config.staleWhileRevalidate}`;
  }

  headers.set("Cache-Control", cacheControl);

  // Cloudflare specific
  headers.set("CDN-Cache-Control", `max-age=${config.ttl}`);

  return headers;
}

// Cache API usage
export async function withCache<T>(
  request: Request,
  cacheKey: string,
  ttl: number,
  fetcher: () => Promise<T>
): Promise<Response> {
  const cache = caches.default;

  // Create cache request
  const cacheRequest = new Request(
    `https://cache.internal/${cacheKey}`,
    { method: "GET" }
  );

  // Check cache
  const cached = await cache.match(cacheRequest);
  if (cached) {
    // Add cache status header
    const response = new Response(cached.body, cached);
    response.headers.set("X-Cache", "HIT");
    return response;
  }

  // Fetch fresh data
  const data = await fetcher();
  const response = new Response(JSON.stringify(data), {
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": `public, max-age=${ttl}`,
      "X-Cache": "MISS",
    },
  });

  // Store in cache (don't await)
  cache.put(cacheRequest, response.clone());

  return response;
}

// Conditional caching based on response
export function shouldCache(response: Response): boolean {
  // Don't cache errors
  if (!response.ok) return false;

  // Don't cache if explicitly disabled
  const cacheControl = response.headers.get("Cache-Control");
  if (cacheControl?.includes("no-store")) return false;

  // Don't cache if response is too large
  const contentLength = response.headers.get("Content-Length");
  if (contentLength && parseInt(contentLength) > 25 * 1024 * 1024) {
    return false; // > 25MB
  }

  return true;
}
```

### Cold Start Optimization

```typescript
// src/optimization/cold-start.ts

// 1. Lazy initialization
let dbInstance: Database | null = null;

function getDb(env: Env): Database {
  if (!dbInstance) {
    dbInstance = new Database(env.DB);
  }
  return dbInstance;
}

// 2. Avoid top-level async
// BAD: Top-level await causes cold start delay
// const config = await fetchConfig();

// GOOD: Lazy load on first request
let configPromise: Promise<Config> | null = null;

async function getConfig(env: Env): Promise<Config> {
  if (!configPromise) {
    configPromise = fetchConfig(env);
  }
  return configPromise;
}

// 3. Minimize dependencies
// Use native APIs instead of large libraries when possible

// Instead of lodash
const pick = <T extends object, K extends keyof T>(
  obj: T,
  keys: K[]
): Pick<T, K> => {
  return keys.reduce((acc, key) => {
    if (key in obj) acc[key] = obj[key];
    return acc;
  }, {} as Pick<T, K>);
};

// Instead of moment/dayjs for simple formatting
const formatDate = (date: Date): string => {
  return date.toISOString().split("T")[0];
};

// 4. Precompute at build time
// Generate route tables, regex patterns at build time

const ROUTE_PATTERNS = [
  { pattern: /^\/api\/users\/([^/]+)$/, handler: "getUser" },
  { pattern: /^\/api\/posts$/, handler: "listPosts" },
  { pattern: /^\/api\/posts\/([^/]+)$/, handler: "getPost" },
] as const;

// 5. Use smaller alternatives
// - date-fns instead of moment
// - superjson instead of full serialization libs
// - itty-router instead of express-like frameworks
```

---

## 9. Security Patterns

### Request Validation

```typescript
// src/validation/schema.ts
type Validator<T> = (value: unknown) => { valid: true; data: T } | { valid: false; errors: string[] };

// Simple schema validation without external deps
export const validators = {
  string(
    options: { minLength?: number; maxLength?: number; pattern?: RegExp } = {}
  ): Validator<string> {
    return (value) => {
      const errors: string[] = [];

      if (typeof value !== "string") {
        return { valid: false, errors: ["Must be a string"] };
      }

      if (options.minLength && value.length < options.minLength) {
        errors.push(`Must be at least ${options.minLength} characters`);
      }

      if (options.maxLength && value.length > options.maxLength) {
        errors.push(`Must be at most ${options.maxLength} characters`);
      }

      if (options.pattern && !options.pattern.test(value)) {
        errors.push("Invalid format");
      }

      return errors.length
        ? { valid: false, errors }
        : { valid: true, data: value };
    };
  },

  email(): Validator<string> {
    return validators.string({
      pattern: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    });
  },

  number(
    options: { min?: number; max?: number; integer?: boolean } = {}
  ): Validator<number> {
    return (value) => {
      const errors: string[] = [];
      const num = typeof value === "string" ? parseFloat(value) : value;

      if (typeof num !== "number" || isNaN(num)) {
        return { valid: false, errors: ["Must be a number"] };
      }

      if (options.integer && !Number.isInteger(num)) {
        errors.push("Must be an integer");
      }

      if (options.min !== undefined && num < options.min) {
        errors.push(`Must be at least ${options.min}`);
      }

      if (options.max !== undefined && num > options.max) {
        errors.push(`Must be at most ${options.max}`);
      }

      return errors.length
        ? { valid: false, errors }
        : { valid: true, data: num };
    };
  },

  object<T extends Record<string, Validator<unknown>>>(
    schema: T
  ): Validator<{ [K in keyof T]: T[K] extends Validator<infer U> ? U : never }> {
    return (value) => {
      if (typeof value !== "object" || value === null) {
        return { valid: false, errors: ["Must be an object"] };
      }

      const errors: string[] = [];
      const result: Record<string, unknown> = {};

      for (const [key, validator] of Object.entries(schema)) {
        const fieldResult = validator((value as Record<string, unknown>)[key]);

        if (!fieldResult.valid) {
          errors.push(
            ...fieldResult.errors.map((e) => `${key}: ${e}`)
          );
        } else {
          result[key] = fieldResult.data;
        }
      }

      return errors.length
        ? { valid: false, errors }
        : { valid: true, data: result as { [K in keyof T]: T[K] extends Validator<infer U> ? U : never } };
    };
  },

  array<T>(itemValidator: Validator<T>): Validator<T[]> {
    return (value) => {
      if (!Array.isArray(value)) {
        return { valid: false, errors: ["Must be an array"] };
      }

      const errors: string[] = [];
      const result: T[] = [];

      value.forEach((item, index) => {
        const itemResult = itemValidator(item);
        if (!itemResult.valid) {
          errors.push(
            ...itemResult.errors.map((e) => `[${index}]: ${e}`)
          );
        } else {
          result.push(itemResult.data);
        }
      });

      return errors.length
        ? { valid: false, errors }
        : { valid: true, data: result };
    };
  },
};

// Usage
const createUserSchema = validators.object({
  email: validators.email(),
  name: validators.string({ minLength: 1, maxLength: 100 }),
  age: validators.number({ min: 0, max: 150, integer: true }),
});

export function validateRequest<T>(
  validator: Validator<T>,
  data: unknown
): T {
  const result = validator(data);

  if (!result.valid) {
    throw new ValidationError(result.errors);
  }

  return result.data;
}

export class ValidationError extends Error {
  constructor(public errors: string[]) {
    super(`Validation failed: ${errors.join(", ")}`);
    this.name = "ValidationError";
  }
}
```

### Request Signing

```typescript
// src/security/signing.ts
export class RequestSigner {
  constructor(private secret: string) {}

  async sign(payload: unknown, timestamp: number = Date.now()): Promise<string> {
    const message = `${timestamp}.${JSON.stringify(payload)}`;
    const signature = await this.createHmac(message);
    return `t=${timestamp},s=${signature}`;
  }

  async verify(
    payload: unknown,
    signatureHeader: string,
    maxAge: number = 300000 // 5 minutes
  ): Promise<boolean> {
    const parts = Object.fromEntries(
      signatureHeader.split(",").map((p) => p.split("="))
    );

    const timestamp = parseInt(parts.t, 10);
    const signature = parts.s;

    if (!timestamp || !signature) {
      return false;
    }

    // Check timestamp
    if (Date.now() - timestamp > maxAge) {
      return false;
    }

    // Verify signature
    const message = `${timestamp}.${JSON.stringify(payload)}`;
    const expectedSignature = await this.createHmac(message);

    return this.timingSafeEqual(signature, expectedSignature);
  }

  private async createHmac(message: string): Promise<string> {
    const encoder = new TextEncoder();
    const key = await crypto.subtle.importKey(
      "raw",
      encoder.encode(this.secret),
      { name: "HMAC", hash: "SHA-256" },
      false,
      ["sign"]
    );

    const signature = await crypto.subtle.sign(
      "HMAC",
      key,
      encoder.encode(message)
    );

    return Array.from(new Uint8Array(signature))
      .map((b) => b.toString(16).padStart(2, "0"))
      .join("");
  }

  private timingSafeEqual(a: string, b: string): boolean {
    if (a.length !== b.length) {
      return false;
    }

    let result = 0;
    for (let i = 0; i < a.length; i++) {
      result |= a.charCodeAt(i) ^ b.charCodeAt(i);
    }

    return result === 0;
  }
}

// Webhook verification middleware
export function createWebhookVerifier(secret: string) {
  const signer = new RequestSigner(secret);

  return async function verifyWebhook(
    request: Request,
    next: () => Promise<Response>
  ): Promise<Response> {
    const signature = request.headers.get("X-Signature");

    if (!signature) {
      return new Response(
        JSON.stringify({ error: "Missing signature" }),
        { status: 401 }
      );
    }

    const body = await request.clone().json();
    const isValid = await signer.verify(body, signature);

    if (!isValid) {
      return new Response(
        JSON.stringify({ error: "Invalid signature" }),
        { status: 401 }
      );
    }

    return next();
  };
}
```

### Content Security Policy

```typescript
// src/security/csp.ts
interface CSPDirectives {
  defaultSrc?: string[];
  scriptSrc?: string[];
  styleSrc?: string[];
  imgSrc?: string[];
  fontSrc?: string[];
  connectSrc?: string[];
  frameSrc?: string[];
  objectSrc?: string[];
  mediaSrc?: string[];
  workerSrc?: string[];
  reportUri?: string;
  reportTo?: string;
}

export function buildCSP(directives: CSPDirectives): string {
  const parts: string[] = [];

  if (directives.defaultSrc) {
    parts.push(`default-src ${directives.defaultSrc.join(" ")}`);
  }
  if (directives.scriptSrc) {
    parts.push(`script-src ${directives.scriptSrc.join(" ")}`);
  }
  if (directives.styleSrc) {
    parts.push(`style-src ${directives.styleSrc.join(" ")}`);
  }
  if (directives.imgSrc) {
    parts.push(`img-src ${directives.imgSrc.join(" ")}`);
  }
  if (directives.fontSrc) {
    parts.push(`font-src ${directives.fontSrc.join(" ")}`);
  }
  if (directives.connectSrc) {
    parts.push(`connect-src ${directives.connectSrc.join(" ")}`);
  }
  if (directives.frameSrc) {
    parts.push(`frame-src ${directives.frameSrc.join(" ")}`);
  }
  if (directives.objectSrc) {
    parts.push(`object-src ${directives.objectSrc.join(" ")}`);
  }
  if (directives.mediaSrc) {
    parts.push(`media-src ${directives.mediaSrc.join(" ")}`);
  }
  if (directives.workerSrc) {
    parts.push(`worker-src ${directives.workerSrc.join(" ")}`);
  }
  if (directives.reportUri) {
    parts.push(`report-uri ${directives.reportUri}`);
  }
  if (directives.reportTo) {
    parts.push(`report-to ${directives.reportTo}`);
  }

  return parts.join("; ");
}

// Security headers middleware
export function securityHeaders(): (
  response: Response
) => Response {
  const csp = buildCSP({
    defaultSrc: ["'self'"],
    scriptSrc: ["'self'", "'unsafe-inline'"],
    styleSrc: ["'self'", "'unsafe-inline'"],
    imgSrc: ["'self'", "data:", "https:"],
    fontSrc: ["'self'"],
    connectSrc: ["'self'", "https://api.example.com"],
    frameSrc: ["'none'"],
    objectSrc: ["'none'"],
  });

  return (response: Response): Response => {
    const newResponse = new Response(response.body, response);

    newResponse.headers.set("Content-Security-Policy", csp);
    newResponse.headers.set("X-Content-Type-Options", "nosniff");
    newResponse.headers.set("X-Frame-Options", "DENY");
    newResponse.headers.set("X-XSS-Protection", "1; mode=block");
    newResponse.headers.set(
      "Strict-Transport-Security",
      "max-age=31536000; includeSubDomains"
    );
    newResponse.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
    newResponse.headers.set(
      "Permissions-Policy",
      "camera=(), microphone=(), geolocation=()"
    );

    return newResponse;
  };
}
```

---

## 10. Platform Limits Reference

### Cloudflare Workers Limits

| Resource | Free | Paid |
|----------|------|------|
| Requests/day | 100,000 | Unlimited |
| CPU time/request | 10ms | 50ms (default), up to 30s |
| Memory | 128MB | 128MB |
| Script size | 1MB | 10MB (after compression) |
| Environment variables | 64 | 64 |
| KV reads/day | 100,000 | 10M+ |
| KV writes/day | 1,000 | 1M+ |
| KV value size | 25MB | 25MB |
| D1 database size | 500MB | 2GB+ |
| D1 rows read/day | 5M | 50B+ |
| R2 storage | 10GB | Unlimited |
| Durable Objects | N/A | Unlimited |

### Vercel Edge Functions Limits

| Resource | Hobby | Pro |
|----------|-------|-----|
| Execution time | 25s | 25s |
| Memory | 128MB | 128MB |
| Payload size | 4MB | 4MB |
| Concurrent executions | 1,000 | 1,000+ |
| Edge Config reads | 100K/month | 1M+/month |
| Edge Config size | 8KB | 512KB |

### Best Practices for Limits

```typescript
// 1. Handle timeouts gracefully
export async function withTimeout<T>(
  promise: Promise<T>,
  ms: number,
  fallback?: T
): Promise<T> {
  const timeout = new Promise<never>((_, reject) =>
    setTimeout(() => reject(new Error("Timeout")), ms)
  );

  try {
    return await Promise.race([promise, timeout]);
  } catch (error) {
    if (fallback !== undefined) return fallback;
    throw error;
  }
}

// 2. Chunk large operations
export async function processInChunks<T, R>(
  items: T[],
  processor: (item: T) => Promise<R>,
  chunkSize: number = 100
): Promise<R[]> {
  const results: R[] = [];

  for (let i = 0; i < items.length; i += chunkSize) {
    const chunk = items.slice(i, i + chunkSize);
    const chunkResults = await Promise.all(chunk.map(processor));
    results.push(...chunkResults);
  }

  return results;
}

// 3. Monitor CPU time (Cloudflare specific)
export function checkCpuTime(startTime: number, maxMs: number): void {
  const elapsed = Date.now() - startTime;
  if (elapsed > maxMs * 0.8) {
    throw new Error(`Approaching CPU limit: ${elapsed}ms`);
  }
}

// 4. Compress large responses
export async function compressResponse(
  response: Response
): Promise<Response> {
  const body = await response.arrayBuffer();

  // Only compress if > 1KB
  if (body.byteLength < 1024) {
    return response;
  }

  const compressed = await compress(body);

  return new Response(compressed, {
    headers: {
      ...Object.fromEntries(response.headers),
      "Content-Encoding": "gzip",
    },
  });
}

async function compress(data: ArrayBuffer): Promise<ArrayBuffer> {
  const stream = new ReadableStream({
    start(controller) {
      controller.enqueue(new Uint8Array(data));
      controller.close();
    },
  });

  const compressed = stream.pipeThrough(new CompressionStream("gzip"));
  const reader = compressed.getReader();
  const chunks: Uint8Array[] = [];

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    chunks.push(value);
  }

  const totalLength = chunks.reduce((sum, chunk) => sum + chunk.length, 0);
  const result = new Uint8Array(totalLength);
  let offset = 0;

  for (const chunk of chunks) {
    result.set(chunk, offset);
    offset += chunk.length;
  }

  return result.buffer;
}
```

---

## Quick Reference Commands

```bash
# Cloudflare Workers
wrangler init my-worker          # Create new worker
wrangler dev                     # Local development
wrangler deploy                  # Deploy to production
wrangler deploy --env staging    # Deploy to staging
wrangler tail                    # Stream logs
wrangler kv:namespace create X   # Create KV namespace
wrangler d1 create my-db         # Create D1 database
wrangler d1 execute my-db --file schema.sql  # Run migrations
wrangler r2 bucket create X      # Create R2 bucket

# Vercel Edge
vercel dev                       # Local development
vercel deploy                    # Deploy preview
vercel deploy --prod             # Deploy production
vercel env pull                  # Pull environment variables
```
