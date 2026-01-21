# MVP Scaffolding Skill

```yaml
---
skill: mvp-scaffolding
version: 1.0.0
description: Rapid prototyping patterns for building MVPs quickly with production-ready foundations
used-by:
  - rapid-prototyper
  - fullstack-developer
  - nextjs-developer
tags:
  - scaffolding
  - mvp
  - prototyping
  - deployment
---
```

## Overview

This skill provides patterns and scripts for quickly scaffolding MVPs that can evolve into production applications. The focus is on speed without sacrificing the ability to iterate.

---

## 1. Stack Selection Matrix

### Decision Framework

| Project Type | Recommended Stack | Why |
|--------------|-------------------|-----|
| Landing page with forms | Astro + React islands | Fastest load, minimal JS |
| Dashboard/CRUD app | Next.js App Router + SQLite | Full-stack in one, simple data |
| API-first service | Hono + Bun + SQLite | Lightweight, fast iteration |
| Real-time features | Next.js + Convex or Supabase | Built-in subscriptions |
| Content site | Astro + MDX | Static generation, great DX |
| Mobile-first PWA | Next.js + Capacitor | One codebase, native feel |

### Quick Decision Tree

```
Need SEO?
  Yes -> Need interactivity?
    Heavy -> Next.js App Router
    Light -> Astro with React islands
  No -> SPA acceptable?
    Yes -> Vite + React
    No -> Next.js App Router

Need real-time?
  Yes -> Convex or Supabase
  No -> SQLite + Drizzle

Need auth?
  Social only -> Lucia or Better Auth
  Enterprise -> Auth.js v5
  Custom -> Roll with jose + cookies

Deployment target?
  Vercel -> Next.js (optimized)
  Edge -> Astro or Hono
  Self-hosted -> Docker + Railway/Fly.io
```

---

## 2. Quick Start Templates

### 2.1 Next.js MVP Starter

```bash
#!/bin/bash
# File: scaffold-nextjs-mvp.sh
# Usage: ./scaffold-nextjs-mvp.sh my-project

set -e

PROJECT_NAME=${1:-"mvp-app"}
echo "Creating Next.js MVP: $PROJECT_NAME"

# Create project with minimal prompts
bunx create-next-app@latest "$PROJECT_NAME" \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --src-dir \
  --import-alias "@/*" \
  --use-bun

cd "$PROJECT_NAME"

# Install MVP essentials
bun add drizzle-orm better-sqlite3 @libsql/client
bun add -d drizzle-kit @types/better-sqlite3

# Create project structure
mkdir -p src/{components,lib,db,actions,hooks}
mkdir -p src/components/{ui,forms,layout}

# Create database config
cat > src/db/index.ts << 'EOF'
import Database from "better-sqlite3";
import { drizzle } from "drizzle-orm/better-sqlite3";
import * as schema from "./schema";

const sqlite = new Database("local.db");
export const db = drizzle(sqlite, { schema });

// Enable WAL mode for better concurrent performance
sqlite.pragma("journal_mode = WAL");
EOF

# Create initial schema
cat > src/db/schema.ts << 'EOF'
import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";

export const users = sqliteTable("users", {
  id: text("id").primaryKey(),
  email: text("email").notNull().unique(),
  name: text("name"),
  createdAt: integer("created_at", { mode: "timestamp" })
    .$defaultFn(() => new Date()),
});

export const sessions = sqliteTable("sessions", {
  id: text("id").primaryKey(),
  userId: text("user_id")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" }),
  expiresAt: integer("expires_at", { mode: "timestamp" }).notNull(),
});

// Add your domain tables here
export const items = sqliteTable("items", {
  id: text("id").primaryKey(),
  userId: text("user_id").references(() => users.id),
  title: text("title").notNull(),
  content: text("content"),
  completed: integer("completed", { mode: "boolean" }).default(false),
  createdAt: integer("created_at", { mode: "timestamp" })
    .$defaultFn(() => new Date()),
  updatedAt: integer("updated_at", { mode: "timestamp" })
    .$defaultFn(() => new Date()),
});

export type User = typeof users.$inferSelect;
export type Session = typeof sessions.$inferSelect;
export type Item = typeof items.$inferSelect;
export type NewItem = typeof items.$inferInsert;
EOF

# Create drizzle config
cat > drizzle.config.ts << 'EOF'
import type { Config } from "drizzle-kit";

export default {
  schema: "./src/db/schema.ts",
  out: "./drizzle",
  dialect: "sqlite",
  dbCredentials: {
    url: "./local.db",
  },
} satisfies Config;
EOF

# Create utility functions
cat > src/lib/utils.ts << 'EOF'
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function generateId(): string {
  return crypto.randomUUID();
}

export function formatDate(date: Date): string {
  return new Intl.DateTimeFormat("en-US", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}
EOF

# Install clsx and tailwind-merge
bun add clsx tailwind-merge

# Create base UI components
cat > src/components/ui/button.tsx << 'EOF'
import { forwardRef, type ButtonHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

export interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "ghost" | "danger";
  size?: "sm" | "md" | "lg";
  loading?: boolean;
}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ className, variant = "primary", size = "md", loading, children, disabled, ...props }, ref) => {
    const baseStyles = "inline-flex items-center justify-center rounded-lg font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50";

    const variants = {
      primary: "bg-zinc-900 text-white hover:bg-zinc-800 focus-visible:ring-zinc-900",
      secondary: "bg-zinc-100 text-zinc-900 hover:bg-zinc-200 focus-visible:ring-zinc-500",
      ghost: "hover:bg-zinc-100 focus-visible:ring-zinc-500",
      danger: "bg-red-600 text-white hover:bg-red-700 focus-visible:ring-red-600",
    };

    const sizes = {
      sm: "h-8 px-3 text-sm",
      md: "h-10 px-4 text-sm",
      lg: "h-12 px-6 text-base",
    };

    return (
      <button
        ref={ref}
        className={cn(baseStyles, variants[variant], sizes[size], className)}
        disabled={disabled || loading}
        {...props}
      >
        {loading && (
          <svg className="mr-2 h-4 w-4 animate-spin" viewBox="0 0 24 24">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
          </svg>
        )}
        {children}
      </button>
    );
  }
);
Button.displayName = "Button";
EOF

cat > src/components/ui/input.tsx << 'EOF'
import { forwardRef, type InputHTMLAttributes } from "react";
import { cn } from "@/lib/utils";

export interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ className, error, ...props }, ref) => {
    return (
      <div className="w-full">
        <input
          ref={ref}
          className={cn(
            "flex h-10 w-full rounded-lg border border-zinc-300 bg-white px-3 py-2 text-sm placeholder:text-zinc-400 focus:outline-none focus:ring-2 focus:ring-zinc-900 focus:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50",
            error && "border-red-500 focus:ring-red-500",
            className
          )}
          {...props}
        />
        {error && <p className="mt-1 text-sm text-red-500">{error}</p>}
      </div>
    );
  }
);
Input.displayName = "Input";
EOF

# Create package.json scripts
cat > package.json.tmp << 'EOF'
{
  "scripts": {
    "dev": "next dev --turbo",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "db:generate": "drizzle-kit generate",
    "db:migrate": "drizzle-kit migrate",
    "db:push": "drizzle-kit push",
    "db:studio": "drizzle-kit studio"
  }
}
EOF

# Merge scripts into package.json
bun add -d json
bunx json -I -f package.json -e "this.scripts = { ...this.scripts, ...require('./package.json.tmp').scripts }"
rm package.json.tmp

# Add .gitignore entries
cat >> .gitignore << 'EOF'

# SQLite
*.db
*.db-journal
*.db-shm
*.db-wal

# Drizzle
drizzle/
EOF

# Initialize database
bun run db:push

echo "MVP scaffolded successfully!"
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  bun run dev"
```

### 2.2 Astro + React Islands Starter

```bash
#!/bin/bash
# File: scaffold-astro-mvp.sh
# Usage: ./scaffold-astro-mvp.sh my-landing

set -e

PROJECT_NAME=${1:-"landing-page"}
echo "Creating Astro MVP: $PROJECT_NAME"

# Create Astro project
bunx create-astro@latest "$PROJECT_NAME" \
  --template minimal \
  --install \
  --git \
  --typescript strict

cd "$PROJECT_NAME"

# Add integrations
bunx astro add react tailwind -y

# Create structure
mkdir -p src/{components,layouts,pages,styles,lib}
mkdir -p src/components/{ui,sections,forms}

# Create base layout
cat > src/layouts/Base.astro << 'EOF'
---
interface Props {
  title: string;
  description?: string;
}

const { title, description = "Built with Astro" } = Astro.props;
---

<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content={description} />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <title>{title}</title>
  </head>
  <body class="min-h-screen bg-white text-zinc-900 antialiased">
    <slot />
  </body>
</html>
EOF

# Create hero section (static)
cat > src/components/sections/Hero.astro << 'EOF'
---
interface Props {
  title: string;
  subtitle: string;
  ctaText: string;
  ctaHref: string;
}

const { title, subtitle, ctaText, ctaHref } = Astro.props;
---

<section class="relative overflow-hidden bg-gradient-to-b from-zinc-50 to-white py-24">
  <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
    <div class="mx-auto max-w-3xl text-center">
      <h1 class="text-4xl font-bold tracking-tight sm:text-6xl">
        {title}
      </h1>
      <p class="mt-6 text-lg leading-8 text-zinc-600">
        {subtitle}
      </p>
      <div class="mt-10">
        <a
          href={ctaHref}
          class="rounded-lg bg-zinc-900 px-6 py-3 text-sm font-semibold text-white shadow-sm hover:bg-zinc-800 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-zinc-900"
        >
          {ctaText}
        </a>
      </div>
    </div>
  </div>
</section>
EOF

# Create contact form (React island for interactivity)
cat > src/components/forms/ContactForm.tsx << 'EOF'
import { useState, type FormEvent } from "react";

interface FormState {
  status: "idle" | "loading" | "success" | "error";
  message: string;
}

export default function ContactForm() {
  const [state, setState] = useState<FormState>({ status: "idle", message: "" });

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setState({ status: "loading", message: "" });

    const formData = new FormData(e.currentTarget);

    try {
      const response = await fetch("/api/contact", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) throw new Error("Failed to submit");

      setState({ status: "success", message: "Thanks! We'll be in touch." });
      (e.target as HTMLFormElement).reset();
    } catch {
      setState({ status: "error", message: "Something went wrong. Please try again." });
    }
  }

  return (
    <form onSubmit={handleSubmit} className="mx-auto max-w-md space-y-4">
      <div>
        <label htmlFor="name" className="block text-sm font-medium text-zinc-700">
          Name
        </label>
        <input
          type="text"
          name="name"
          id="name"
          required
          className="mt-1 block w-full rounded-lg border border-zinc-300 px-3 py-2 shadow-sm focus:border-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500"
        />
      </div>

      <div>
        <label htmlFor="email" className="block text-sm font-medium text-zinc-700">
          Email
        </label>
        <input
          type="email"
          name="email"
          id="email"
          required
          className="mt-1 block w-full rounded-lg border border-zinc-300 px-3 py-2 shadow-sm focus:border-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500"
        />
      </div>

      <div>
        <label htmlFor="message" className="block text-sm font-medium text-zinc-700">
          Message
        </label>
        <textarea
          name="message"
          id="message"
          rows={4}
          required
          className="mt-1 block w-full rounded-lg border border-zinc-300 px-3 py-2 shadow-sm focus:border-zinc-500 focus:outline-none focus:ring-1 focus:ring-zinc-500"
        />
      </div>

      {state.message && (
        <p className={state.status === "error" ? "text-red-600" : "text-green-600"}>
          {state.message}
        </p>
      )}

      <button
        type="submit"
        disabled={state.status === "loading"}
        className="w-full rounded-lg bg-zinc-900 px-4 py-2 text-sm font-semibold text-white hover:bg-zinc-800 focus:outline-none focus:ring-2 focus:ring-zinc-500 focus:ring-offset-2 disabled:opacity-50"
      >
        {state.status === "loading" ? "Sending..." : "Send Message"}
      </button>
    </form>
  );
}
EOF

# Create API endpoint
cat > src/pages/api/contact.ts << 'EOF'
import type { APIRoute } from "astro";

export const POST: APIRoute = async ({ request }) => {
  const formData = await request.formData();
  const name = formData.get("name");
  const email = formData.get("email");
  const message = formData.get("message");

  // Validate
  if (!name || !email || !message) {
    return new Response(JSON.stringify({ error: "All fields required" }), {
      status: 400,
      headers: { "Content-Type": "application/json" },
    });
  }

  // TODO: Send to email service, database, or webhook
  console.log("Contact form submission:", { name, email, message });

  return new Response(JSON.stringify({ success: true }), {
    status: 200,
    headers: { "Content-Type": "application/json" },
  });
};
EOF

# Create index page
cat > src/pages/index.astro << 'EOF'
---
import Base from "../layouts/Base.astro";
import Hero from "../components/sections/Hero.astro";
import ContactForm from "../components/forms/ContactForm";
---

<Base title="My Landing Page" description="Welcome to our product">
  <Hero
    title="Build something amazing"
    subtitle="The fastest way to turn your ideas into reality. Start building today."
    ctaText="Get Started"
    ctaHref="#contact"
  />

  <section id="contact" class="py-24">
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
      <h2 class="text-center text-3xl font-bold">Get in Touch</h2>
      <p class="mx-auto mt-4 max-w-2xl text-center text-zinc-600">
        Have questions? We'd love to hear from you.
      </p>
      <div class="mt-12">
        <ContactForm client:visible />
      </div>
    </div>
  </section>
</Base>
EOF

# Enable SSR for API routes
cat > astro.config.mjs << 'EOF'
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';

export default defineConfig({
  integrations: [react(), tailwind()],
  output: 'hybrid',
});
EOF

echo "Astro MVP scaffolded!"
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  bun run dev"
```

### 2.3 API-Only Starter (Hono + Bun)

```bash
#!/bin/bash
# File: scaffold-api-mvp.sh
# Usage: ./scaffold-api-mvp.sh my-api

set -e

PROJECT_NAME=${1:-"api-service"}
echo "Creating Hono API: $PROJECT_NAME"

mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# Initialize Bun project
bun init -y

# Install dependencies
bun add hono @hono/zod-validator zod drizzle-orm better-sqlite3
bun add -d @types/better-sqlite3 drizzle-kit

# Create structure
mkdir -p src/{routes,db,middleware,lib}

# Create database
cat > src/db/index.ts << 'EOF'
import Database from "better-sqlite3";
import { drizzle } from "drizzle-orm/better-sqlite3";
import * as schema from "./schema";

const sqlite = new Database("api.db");
sqlite.pragma("journal_mode = WAL");

export const db = drizzle(sqlite, { schema });
export { schema };
EOF

cat > src/db/schema.ts << 'EOF'
import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";

export const apiKeys = sqliteTable("api_keys", {
  id: text("id").primaryKey(),
  key: text("key").notNull().unique(),
  name: text("name").notNull(),
  createdAt: integer("created_at", { mode: "timestamp" }).$defaultFn(() => new Date()),
});

export const resources = sqliteTable("resources", {
  id: text("id").primaryKey(),
  name: text("name").notNull(),
  data: text("data", { mode: "json" }),
  createdAt: integer("created_at", { mode: "timestamp" }).$defaultFn(() => new Date()),
  updatedAt: integer("updated_at", { mode: "timestamp" }).$defaultFn(() => new Date()),
});

export type ApiKey = typeof apiKeys.$inferSelect;
export type Resource = typeof resources.$inferSelect;
export type NewResource = typeof resources.$inferInsert;
EOF

# Create middleware
cat > src/middleware/auth.ts << 'EOF'
import { createMiddleware } from "hono/factory";
import { HTTPException } from "hono/http-exception";
import { db, schema } from "../db";
import { eq } from "drizzle-orm";

export const apiKeyAuth = createMiddleware(async (c, next) => {
  const apiKey = c.req.header("X-API-Key");

  if (!apiKey) {
    throw new HTTPException(401, { message: "API key required" });
  }

  const keyRecord = await db.query.apiKeys.findFirst({
    where: eq(schema.apiKeys.key, apiKey),
  });

  if (!keyRecord) {
    throw new HTTPException(401, { message: "Invalid API key" });
  }

  c.set("apiKey", keyRecord);
  await next();
});
EOF

# Create routes
cat > src/routes/resources.ts << 'EOF'
import { Hono } from "hono";
import { zValidator } from "@hono/zod-validator";
import { z } from "zod";
import { db, schema } from "../db";
import { eq } from "drizzle-orm";

const resourceSchema = z.object({
  name: z.string().min(1).max(255),
  data: z.record(z.unknown()).optional(),
});

const resources = new Hono()
  .get("/", async (c) => {
    const items = await db.query.resources.findMany({
      orderBy: (resources, { desc }) => [desc(resources.createdAt)],
    });
    return c.json({ data: items });
  })
  .get("/:id", async (c) => {
    const id = c.req.param("id");
    const item = await db.query.resources.findFirst({
      where: eq(schema.resources.id, id),
    });

    if (!item) {
      return c.json({ error: "Not found" }, 404);
    }

    return c.json({ data: item });
  })
  .post("/", zValidator("json", resourceSchema), async (c) => {
    const body = c.req.valid("json");
    const id = crypto.randomUUID();

    await db.insert(schema.resources).values({
      id,
      name: body.name,
      data: body.data,
    });

    const item = await db.query.resources.findFirst({
      where: eq(schema.resources.id, id),
    });

    return c.json({ data: item }, 201);
  })
  .put("/:id", zValidator("json", resourceSchema), async (c) => {
    const id = c.req.param("id");
    const body = c.req.valid("json");

    await db.update(schema.resources)
      .set({ name: body.name, data: body.data, updatedAt: new Date() })
      .where(eq(schema.resources.id, id));

    const item = await db.query.resources.findFirst({
      where: eq(schema.resources.id, id),
    });

    if (!item) {
      return c.json({ error: "Not found" }, 404);
    }

    return c.json({ data: item });
  })
  .delete("/:id", async (c) => {
    const id = c.req.param("id");

    await db.delete(schema.resources)
      .where(eq(schema.resources.id, id));

    return c.json({ success: true });
  });

export default resources;
EOF

# Create main app
cat > src/index.ts << 'EOF'
import { Hono } from "hono";
import { cors } from "hono/cors";
import { logger } from "hono/logger";
import { prettyJSON } from "hono/pretty-json";
import { apiKeyAuth } from "./middleware/auth";
import resources from "./routes/resources";

const app = new Hono();

// Global middleware
app.use("*", logger());
app.use("*", prettyJSON());
app.use("*", cors({
  origin: ["http://localhost:3000"],
  allowMethods: ["GET", "POST", "PUT", "DELETE"],
  allowHeaders: ["Content-Type", "X-API-Key"],
}));

// Health check (no auth)
app.get("/health", (c) => c.json({ status: "ok", timestamp: new Date().toISOString() }));

// Protected routes
app.use("/api/*", apiKeyAuth);
app.route("/api/resources", resources);

// Error handling
app.onError((err, c) => {
  console.error(err);
  return c.json({ error: err.message }, 500);
});

// 404 handler
app.notFound((c) => c.json({ error: "Not found" }, 404));

export default {
  port: process.env.PORT || 3001,
  fetch: app.fetch,
};
EOF

# Create drizzle config
cat > drizzle.config.ts << 'EOF'
import type { Config } from "drizzle-kit";

export default {
  schema: "./src/db/schema.ts",
  out: "./drizzle",
  dialect: "sqlite",
  dbCredentials: {
    url: "./api.db",
  },
} satisfies Config;
EOF

# Update package.json
cat > package.json << 'EOF'
{
  "name": "api-service",
  "type": "module",
  "scripts": {
    "dev": "bun run --watch src/index.ts",
    "start": "bun run src/index.ts",
    "db:generate": "drizzle-kit generate",
    "db:migrate": "drizzle-kit migrate",
    "db:push": "drizzle-kit push",
    "db:studio": "drizzle-kit studio"
  }
}
EOF

# Create .gitignore
cat > .gitignore << 'EOF'
node_modules/
*.db
*.db-journal
*.db-shm
*.db-wal
drizzle/
.env
EOF

# Create seed script
cat > seed.ts << 'EOF'
import { db, schema } from "./src/db";

// Create a test API key
const apiKey = crypto.randomUUID();
await db.insert(schema.apiKeys).values({
  id: crypto.randomUUID(),
  key: apiKey,
  name: "Development Key",
});

console.log("Created API key:", apiKey);
console.log("Use with: curl -H 'X-API-Key: " + apiKey + "' http://localhost:3001/api/resources");
EOF

# Initialize database
bun run db:push
bun run seed.ts

echo "Hono API scaffolded!"
echo "Next steps:"
echo "  cd $PROJECT_NAME"
echo "  bun run dev"
```

---

## 3. Scaffolding Scripts

### 3.1 Component Generator

```bash
#!/bin/bash
# File: gen-component.sh
# Usage: ./gen-component.sh ComponentName [--form|--list|--card]

set -e

NAME=$1
TYPE=${2:-"--default"}
COMPONENTS_DIR="src/components"

if [ -z "$NAME" ]; then
  echo "Usage: ./gen-component.sh ComponentName [--form|--list|--card]"
  exit 1
fi

# Convert to kebab-case for filename
FILENAME=$(echo "$NAME" | sed 's/\([A-Z]\)/-\L\1/g' | sed 's/^-//')

case $TYPE in
  --form)
    cat > "$COMPONENTS_DIR/forms/$FILENAME.tsx" << EOF
"use client";

import { useActionState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface ${NAME}Props {
  onSubmit: (formData: FormData) => Promise<{ error?: string; success?: boolean }>;
}

export function ${NAME}({ onSubmit }: ${NAME}Props) {
  const [state, action, isPending] = useActionState(
    async (_prev: unknown, formData: FormData) => {
      return await onSubmit(formData);
    },
    { error: undefined, success: false }
  );

  return (
    <form action={action} className="space-y-4">
      <Input
        name="field"
        placeholder="Enter value"
        required
      />

      {state.error && (
        <p className="text-sm text-red-500">{state.error}</p>
      )}

      {state.success && (
        <p className="text-sm text-green-500">Success!</p>
      )}

      <Button type="submit" loading={isPending}>
        Submit
      </Button>
    </form>
  );
}
EOF
    echo "Created form component: $COMPONENTS_DIR/forms/$FILENAME.tsx"
    ;;

  --list)
    cat > "$COMPONENTS_DIR/$FILENAME.tsx" << EOF
interface ${NAME}Item {
  id: string;
  title: string;
  // Add more fields as needed
}

interface ${NAME}Props {
  items: ${NAME}Item[];
  onItemClick?: (item: ${NAME}Item) => void;
}

export function ${NAME}({ items, onItemClick }: ${NAME}Props) {
  if (items.length === 0) {
    return (
      <div className="py-12 text-center text-zinc-500">
        No items yet
      </div>
    );
  }

  return (
    <ul className="divide-y divide-zinc-200">
      {items.map((item) => (
        <li
          key={item.id}
          onClick={() => onItemClick?.(item)}
          className="flex items-center justify-between py-4 hover:bg-zinc-50 cursor-pointer"
        >
          <span>{item.title}</span>
        </li>
      ))}
    </ul>
  );
}
EOF
    echo "Created list component: $COMPONENTS_DIR/$FILENAME.tsx"
    ;;

  --card)
    cat > "$COMPONENTS_DIR/$FILENAME.tsx" << EOF
import { cn } from "@/lib/utils";
import type { ReactNode } from "react";

interface ${NAME}Props {
  title: string;
  description?: string;
  children?: ReactNode;
  className?: string;
}

export function ${NAME}({ title, description, children, className }: ${NAME}Props) {
  return (
    <div className={cn("rounded-lg border border-zinc-200 bg-white p-6 shadow-sm", className)}>
      <h3 className="text-lg font-semibold">{title}</h3>
      {description && (
        <p className="mt-1 text-sm text-zinc-500">{description}</p>
      )}
      {children && <div className="mt-4">{children}</div>}
    </div>
  );
}
EOF
    echo "Created card component: $COMPONENTS_DIR/$FILENAME.tsx"
    ;;

  *)
    cat > "$COMPONENTS_DIR/$FILENAME.tsx" << EOF
interface ${NAME}Props {
  // Add props here
}

export function ${NAME}({}: ${NAME}Props) {
  return (
    <div>
      {/* ${NAME} content */}
    </div>
  );
}
EOF
    echo "Created component: $COMPONENTS_DIR/$FILENAME.tsx"
    ;;
esac
```

### 3.2 Feature Generator (Full CRUD)

```bash
#!/bin/bash
# File: gen-feature.sh
# Usage: ./gen-feature.sh posts

set -e

FEATURE=$1
if [ -z "$FEATURE" ]; then
  echo "Usage: ./gen-feature.sh feature-name"
  exit 1
fi

# Convert to various cases
SINGULAR=$(echo "$FEATURE" | sed 's/s$//')
PASCAL=$(echo "$SINGULAR" | sed -r 's/(^|-)([a-z])/\U\2/g')
PASCAL_PLURAL=$(echo "$FEATURE" | sed -r 's/(^|-)([a-z])/\U\2/g')

echo "Generating feature: $FEATURE"
echo "  Singular: $SINGULAR"
echo "  Pascal: $PASCAL"
echo "  Pascal Plural: $PASCAL_PLURAL"

# Create directories
mkdir -p "src/app/$FEATURE"
mkdir -p "src/actions"
mkdir -p "src/components/$FEATURE"

# Add to schema
cat >> src/db/schema.ts << EOF

export const $FEATURE = sqliteTable("$FEATURE", {
  id: text("id").primaryKey(),
  title: text("title").notNull(),
  content: text("content"),
  createdAt: integer("created_at", { mode: "timestamp" }).\$defaultFn(() => new Date()),
  updatedAt: integer("updated_at", { mode: "timestamp" }).\$defaultFn(() => new Date()),
});

export type $PASCAL = typeof $FEATURE.\$inferSelect;
export type New$PASCAL = typeof $FEATURE.\$inferInsert;
EOF

# Create server actions
cat > "src/actions/$FEATURE.ts" << EOF
"use server";

import { db } from "@/db";
import { $FEATURE } from "@/db/schema";
import { eq } from "drizzle-orm";
import { revalidatePath } from "next/cache";

export async function get${PASCAL_PLURAL}() {
  return db.query.$FEATURE.findMany({
    orderBy: ($FEATURE, { desc }) => [desc($FEATURE.createdAt)],
  });
}

export async function get${PASCAL}(id: string) {
  return db.query.$FEATURE.findFirst({
    where: eq($FEATURE.id, id),
  });
}

export async function create${PASCAL}(formData: FormData) {
  const title = formData.get("title") as string;
  const content = formData.get("content") as string;

  if (!title) {
    return { error: "Title is required" };
  }

  const id = crypto.randomUUID();

  await db.insert($FEATURE).values({
    id,
    title,
    content,
  });

  revalidatePath("/$FEATURE");
  return { success: true, id };
}

export async function update${PASCAL}(id: string, formData: FormData) {
  const title = formData.get("title") as string;
  const content = formData.get("content") as string;

  if (!title) {
    return { error: "Title is required" };
  }

  await db.update($FEATURE)
    .set({ title, content, updatedAt: new Date() })
    .where(eq($FEATURE.id, id));

  revalidatePath("/$FEATURE");
  revalidatePath(\`/$FEATURE/\${id}\`);
  return { success: true };
}

export async function delete${PASCAL}(id: string) {
  await db.delete($FEATURE).where(eq($FEATURE.id, id));
  revalidatePath("/$FEATURE");
  return { success: true };
}
EOF

# Create list page
cat > "src/app/$FEATURE/page.tsx" << EOF
import Link from "next/link";
import { get${PASCAL_PLURAL} } from "@/actions/$FEATURE";
import { Button } from "@/components/ui/button";
import { ${PASCAL}List } from "@/components/$FEATURE/${SINGULAR}-list";

export default async function ${PASCAL_PLURAL}Page() {
  const items = await get${PASCAL_PLURAL}();

  return (
    <div className="mx-auto max-w-4xl py-8">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">${PASCAL_PLURAL}</h1>
        <Link href="/$FEATURE/new">
          <Button>Create New</Button>
        </Link>
      </div>
      <div className="mt-8">
        <${PASCAL}List items={items} />
      </div>
    </div>
  );
}
EOF

# Create new page
cat > "src/app/$FEATURE/new/page.tsx" << EOF
import { ${PASCAL}Form } from "@/components/$FEATURE/${SINGULAR}-form";
import { create${PASCAL} } from "@/actions/$FEATURE";

export default function New${PASCAL}Page() {
  return (
    <div className="mx-auto max-w-2xl py-8">
      <h1 className="text-2xl font-bold">Create ${PASCAL}</h1>
      <div className="mt-8">
        <${PASCAL}Form action={create${PASCAL}} />
      </div>
    </div>
  );
}
EOF

# Create detail page
cat > "src/app/$FEATURE/[id]/page.tsx" << EOF
import { notFound } from "next/navigation";
import { get${PASCAL} } from "@/actions/$FEATURE";
import { ${PASCAL}Detail } from "@/components/$FEATURE/${SINGULAR}-detail";

interface Props {
  params: Promise<{ id: string }>;
}

export default async function ${PASCAL}Page({ params }: Props) {
  const { id } = await params;
  const item = await get${PASCAL}(id);

  if (!item) {
    notFound();
  }

  return (
    <div className="mx-auto max-w-2xl py-8">
      <${PASCAL}Detail item={item} />
    </div>
  );
}
EOF

# Create list component
cat > "src/components/$FEATURE/${SINGULAR}-list.tsx" << EOF
import Link from "next/link";
import type { ${PASCAL} } from "@/db/schema";
import { formatDate } from "@/lib/utils";

interface ${PASCAL}ListProps {
  items: ${PASCAL}[];
}

export function ${PASCAL}List({ items }: ${PASCAL}ListProps) {
  if (items.length === 0) {
    return (
      <div className="py-12 text-center text-zinc-500">
        No ${FEATURE} yet. Create your first one!
      </div>
    );
  }

  return (
    <ul className="divide-y divide-zinc-200 rounded-lg border border-zinc-200">
      {items.map((item) => (
        <li key={item.id}>
          <Link
            href={\`/$FEATURE/\${item.id}\`}
            className="block px-4 py-4 hover:bg-zinc-50"
          >
            <h3 className="font-medium">{item.title}</h3>
            {item.createdAt && (
              <p className="mt-1 text-sm text-zinc-500">
                {formatDate(item.createdAt)}
              </p>
            )}
          </Link>
        </li>
      ))}
    </ul>
  );
}
EOF

# Create form component
cat > "src/components/$FEATURE/${SINGULAR}-form.tsx" << EOF
"use client";

import { useActionState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import type { ${PASCAL} } from "@/db/schema";

interface ${PASCAL}FormProps {
  action: (formData: FormData) => Promise<{ error?: string; success?: boolean; id?: string }>;
  initialData?: ${PASCAL};
}

export function ${PASCAL}Form({ action, initialData }: ${PASCAL}FormProps) {
  const router = useRouter();

  const [state, formAction, isPending] = useActionState(
    async (_prev: unknown, formData: FormData) => {
      const result = await action(formData);
      if (result.success && result.id) {
        router.push(\`/$FEATURE/\${result.id}\`);
      }
      return result;
    },
    { error: undefined }
  );

  return (
    <form action={formAction} className="space-y-4">
      <div>
        <label htmlFor="title" className="block text-sm font-medium">
          Title
        </label>
        <Input
          id="title"
          name="title"
          defaultValue={initialData?.title}
          required
          className="mt-1"
        />
      </div>

      <div>
        <label htmlFor="content" className="block text-sm font-medium">
          Content
        </label>
        <textarea
          id="content"
          name="content"
          defaultValue={initialData?.content ?? ""}
          rows={5}
          className="mt-1 w-full rounded-lg border border-zinc-300 px-3 py-2"
        />
      </div>

      {state.error && (
        <p className="text-sm text-red-500">{state.error}</p>
      )}

      <Button type="submit" loading={isPending}>
        {initialData ? "Update" : "Create"}
      </Button>
    </form>
  );
}
EOF

# Create detail component
cat > "src/components/$FEATURE/${SINGULAR}-detail.tsx" << EOF
"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { delete${PASCAL} } from "@/actions/$FEATURE";
import { formatDate } from "@/lib/utils";
import type { ${PASCAL} } from "@/db/schema";

interface ${PASCAL}DetailProps {
  item: ${PASCAL};
}

export function ${PASCAL}Detail({ item }: ${PASCAL}DetailProps) {
  const router = useRouter();

  async function handleDelete() {
    if (!confirm("Are you sure you want to delete this?")) return;
    await delete${PASCAL}(item.id);
    router.push("/$FEATURE");
  }

  return (
    <article>
      <div className="flex items-start justify-between">
        <div>
          <h1 className="text-2xl font-bold">{item.title}</h1>
          {item.createdAt && (
            <p className="mt-1 text-sm text-zinc-500">
              Created {formatDate(item.createdAt)}
            </p>
          )}
        </div>
        <div className="flex gap-2">
          <Link href={\`/$FEATURE/\${item.id}/edit\`}>
            <Button variant="secondary">Edit</Button>
          </Link>
          <Button variant="danger" onClick={handleDelete}>
            Delete
          </Button>
        </div>
      </div>

      {item.content && (
        <div className="prose mt-8">
          <p className="whitespace-pre-wrap">{item.content}</p>
        </div>
      )}
    </article>
  );
}
EOF

echo ""
echo "Feature $FEATURE generated!"
echo ""
echo "Next steps:"
echo "  1. Run: bun run db:push"
echo "  2. Add to schema index if needed"
echo "  3. Add navigation link"
```

---

## 4. MVP Feature Patterns

### 4.1 Simple Auth with Cookies (No Library)

```typescript
// File: src/lib/auth.ts
import { cookies } from "next/headers";
import { db } from "@/db";
import { users, sessions } from "@/db/schema";
import { eq } from "drizzle-orm";

const SESSION_COOKIE = "session_id";
const SESSION_DURATION = 7 * 24 * 60 * 60 * 1000; // 7 days

export async function hashPassword(password: string): Promise<string> {
  return await Bun.password.hash(password, "bcrypt");
}

export async function verifyPassword(password: string, hash: string): Promise<boolean> {
  return await Bun.password.verify(password, hash);
}

export async function createSession(userId: string): Promise<string> {
  const sessionId = crypto.randomUUID();
  const expiresAt = new Date(Date.now() + SESSION_DURATION);

  await db.insert(sessions).values({
    id: sessionId,
    userId,
    expiresAt,
  });

  const cookieStore = await cookies();
  cookieStore.set(SESSION_COOKIE, sessionId, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    expires: expiresAt,
    path: "/",
  });

  return sessionId;
}

export async function getSession() {
  const cookieStore = await cookies();
  const sessionId = cookieStore.get(SESSION_COOKIE)?.value;

  if (!sessionId) return null;

  const session = await db.query.sessions.findFirst({
    where: eq(sessions.id, sessionId),
    with: { user: true },
  });

  if (!session || session.expiresAt < new Date()) {
    if (session) {
      await db.delete(sessions).where(eq(sessions.id, sessionId));
    }
    return null;
  }

  return session;
}

export async function logout() {
  const cookieStore = await cookies();
  const sessionId = cookieStore.get(SESSION_COOKIE)?.value;

  if (sessionId) {
    await db.delete(sessions).where(eq(sessions.id, sessionId));
    cookieStore.delete(SESSION_COOKIE);
  }
}

export async function requireAuth() {
  const session = await getSession();
  if (!session) {
    throw new Error("Unauthorized");
  }
  return session;
}
```

```typescript
// File: src/actions/auth.ts
"use server";

import { redirect } from "next/navigation";
import { db } from "@/db";
import { users } from "@/db/schema";
import { eq } from "drizzle-orm";
import { createSession, hashPassword, verifyPassword, logout as logoutSession } from "@/lib/auth";

export async function signup(formData: FormData) {
  const email = formData.get("email") as string;
  const password = formData.get("password") as string;
  const name = formData.get("name") as string;

  if (!email || !password) {
    return { error: "Email and password are required" };
  }

  const existing = await db.query.users.findFirst({
    where: eq(users.email, email.toLowerCase()),
  });

  if (existing) {
    return { error: "Email already registered" };
  }

  const hashedPassword = await hashPassword(password);
  const userId = crypto.randomUUID();

  await db.insert(users).values({
    id: userId,
    email: email.toLowerCase(),
    name,
    passwordHash: hashedPassword,
  });

  await createSession(userId);
  redirect("/dashboard");
}

export async function login(formData: FormData) {
  const email = formData.get("email") as string;
  const password = formData.get("password") as string;

  if (!email || !password) {
    return { error: "Email and password are required" };
  }

  const user = await db.query.users.findFirst({
    where: eq(users.email, email.toLowerCase()),
  });

  if (!user || !user.passwordHash) {
    return { error: "Invalid credentials" };
  }

  const valid = await verifyPassword(password, user.passwordHash);

  if (!valid) {
    return { error: "Invalid credentials" };
  }

  await createSession(user.id);
  redirect("/dashboard");
}

export async function logout() {
  await logoutSession();
  redirect("/login");
}
```

### 4.2 Data Fetching Patterns

```typescript
// File: src/lib/fetcher.ts

// SWR fetcher
export const fetcher = async <T>(url: string): Promise<T> => {
  const res = await fetch(url);
  if (!res.ok) {
    const error = new Error("An error occurred while fetching the data.");
    throw error;
  }
  return res.json();
};

// Server-side data fetching with error handling
export async function fetchData<T>(
  fetcher: () => Promise<T>,
  options?: { revalidate?: number }
): Promise<{ data: T | null; error: string | null }> {
  try {
    const data = await fetcher();
    return { data, error: null };
  } catch (e) {
    console.error("Fetch error:", e);
    return { data: null, error: "Failed to fetch data" };
  }
}

// Mutation helper with optimistic updates
export async function mutate<T, R>(
  action: (data: T) => Promise<R>,
  data: T,
  options?: {
    onSuccess?: (result: R) => void;
    onError?: (error: Error) => void;
  }
): Promise<R | null> {
  try {
    const result = await action(data);
    options?.onSuccess?.(result);
    return result;
  } catch (e) {
    const error = e instanceof Error ? e : new Error("Unknown error");
    options?.onError?.(error);
    return null;
  }
}
```

```typescript
// File: src/hooks/use-data.ts
"use client";

import useSWR, { type SWRConfiguration } from "swr";
import useSWRMutation from "swr/mutation";
import { fetcher } from "@/lib/fetcher";

// Generic data hook
export function useData<T>(key: string | null, config?: SWRConfiguration<T>) {
  return useSWR<T>(key, fetcher, {
    revalidateOnFocus: false,
    ...config,
  });
}

// Mutation hook
export function useMutation<T, R>(
  key: string,
  mutator: (key: string, { arg }: { arg: T }) => Promise<R>
) {
  return useSWRMutation(key, mutator);
}

// Example: Posts hook
export function usePosts() {
  return useData<{ data: Post[] }>("/api/posts");
}

export function useCreatePost() {
  return useMutation("/api/posts", async (url, { arg }: { arg: NewPost }) => {
    const res = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(arg),
    });
    return res.json();
  });
}
```

### 4.3 Form Handling with Server Actions

```typescript
// File: src/components/forms/server-form.tsx
"use client";

import { useActionState } from "react";
import { useFormStatus } from "react-dom";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface FormState {
  error?: string;
  success?: boolean;
  fieldErrors?: Record<string, string>;
}

interface ServerFormProps {
  action: (prevState: FormState, formData: FormData) => Promise<FormState>;
  children?: React.ReactNode;
}

function SubmitButton({ children }: { children: React.ReactNode }) {
  const { pending } = useFormStatus();
  return (
    <Button type="submit" loading={pending}>
      {children}
    </Button>
  );
}

export function ServerForm({ action, children }: ServerFormProps) {
  const [state, formAction] = useActionState(action, {});

  return (
    <form action={formAction} className="space-y-4">
      {children}

      {state.error && (
        <div className="rounded-lg bg-red-50 p-3 text-sm text-red-600">
          {state.error}
        </div>
      )}

      {state.success && (
        <div className="rounded-lg bg-green-50 p-3 text-sm text-green-600">
          Success!
        </div>
      )}

      <SubmitButton>Submit</SubmitButton>
    </form>
  );
}

// Field with error display
interface FormFieldProps {
  name: string;
  label: string;
  type?: string;
  error?: string;
  required?: boolean;
}

export function FormField({ name, label, type = "text", error, required }: FormFieldProps) {
  return (
    <div>
      <label htmlFor={name} className="block text-sm font-medium text-zinc-700">
        {label}
        {required && <span className="text-red-500 ml-1">*</span>}
      </label>
      <Input
        id={name}
        name={name}
        type={type}
        required={required}
        error={error}
        className="mt-1"
      />
    </div>
  );
}
```

---

## 5. Deployment Shortcuts

### 5.1 Vercel Deployment

```bash
#!/bin/bash
# File: deploy-vercel.sh
# Usage: ./deploy-vercel.sh [--prod]

set -e

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
  echo "Installing Vercel CLI..."
  bun add -g vercel
fi

# Build check
echo "Running build..."
bun run build

if [ "$1" = "--prod" ]; then
  echo "Deploying to production..."
  vercel --prod
else
  echo "Deploying preview..."
  vercel
fi
```

```json
// vercel.json - Optimal Next.js config
{
  "framework": "nextjs",
  "regions": ["iad1"],
  "env": {
    "DATABASE_URL": "@database-url"
  },
  "headers": [
    {
      "source": "/api/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "no-store" }
      ]
    }
  ]
}
```

### 5.2 Railway Deployment

```bash
#!/bin/bash
# File: deploy-railway.sh
# Usage: ./deploy-railway.sh

set -e

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
  echo "Installing Railway CLI..."
  brew install railway
fi

# Login if needed
railway whoami || railway login

# Initialize if no project exists
if [ ! -f "railway.toml" ]; then
  echo "Initializing Railway project..."
  railway init
fi

# Deploy
echo "Deploying to Railway..."
railway up
```

```toml
# railway.toml
[build]
builder = "nixpacks"
buildCommand = "bun install && bun run build"

[deploy]
startCommand = "bun run start"
healthcheckPath = "/api/health"
healthcheckTimeout = 100
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 3

[[services]]
name = "web"
port = 3000
```

### 5.3 Docker Deployment

```dockerfile
# Dockerfile - Multi-stage Bun build
FROM oven/bun:1 AS base
WORKDIR /app

# Install dependencies
FROM base AS deps
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile

# Build application
FROM base AS builder
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED=1
RUN bun run build

# Production image
FROM base AS runner
WORKDIR /app
ENV NODE_ENV=production
ENV NEXT_TELEMETRY_DISABLED=1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs
EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["bun", "server.js"]
```

```yaml
# docker-compose.yml - Local development with SQLite
version: "3.8"

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_URL=file:./data/app.db
      - NODE_ENV=production

  # Optional: Add when ready for Postgres
  # db:
  #   image: postgres:16-alpine
  #   environment:
  #     POSTGRES_USER: app
  #     POSTGRES_PASSWORD: secret
  #     POSTGRES_DB: app
  #   volumes:
  #     - postgres_data:/var/lib/postgresql/data
  #   ports:
  #     - "5432:5432"

# volumes:
#   postgres_data:
```

```bash
#!/bin/bash
# File: docker-deploy.sh
# Usage: ./docker-deploy.sh

set -e

IMAGE_NAME="mvp-app"
TAG="latest"

# Build
echo "Building Docker image..."
docker build -t "$IMAGE_NAME:$TAG" .

# Run locally
echo "Running container..."
docker run -d \
  --name "$IMAGE_NAME" \
  -p 3000:3000 \
  -v "$(pwd)/data:/app/data" \
  "$IMAGE_NAME:$TAG"

echo "App running at http://localhost:3000"
```

---

## 6. MVP Checklist by Day

### Day 1: Foundation

```markdown
## Day 1 Checklist

### Morning (Setup)
- [ ] Scaffold project with appropriate template
- [ ] Configure Tailwind with design tokens
- [ ] Set up SQLite + Drizzle
- [ ] Create initial schema
- [ ] Add basic auth (if needed)

### Afternoon (Core)
- [ ] Build primary data model
- [ ] Create CRUD actions
- [ ] Build list view
- [ ] Build create form
- [ ] Build detail view

### Evening (Polish)
- [ ] Add loading states
- [ ] Add error handling
- [ ] Test happy path
- [ ] Deploy preview
```

### Day 2: Features

```markdown
## Day 2 Checklist

### Morning (Features)
- [ ] Add secondary features
- [ ] Implement search/filter
- [ ] Add sorting
- [ ] Build dashboard/home

### Afternoon (UX)
- [ ] Add empty states
- [ ] Add success feedback
- [ ] Improve form validation
- [ ] Add navigation

### Evening (Quality)
- [ ] Mobile responsiveness
- [ ] Basic accessibility
- [ ] Performance check
- [ ] Deploy production
```

### Day 3: Launch

```markdown
## Day 3 Checklist

### Morning (Final)
- [ ] Fix critical bugs
- [ ] Add analytics (Vercel/Plausible)
- [ ] Set up error monitoring
- [ ] Final content review

### Afternoon (Launch)
- [ ] Production deploy
- [ ] DNS/domain setup
- [ ] Test all flows
- [ ] Share with users

### Post-Launch
- [ ] Monitor errors
- [ ] Gather feedback
- [ ] Document shortcuts taken
- [ ] Plan v2 improvements
```

---

## 7. Anti-Patterns to Avoid

### 7.1 Premature Optimization

```typescript
// BAD: Over-engineering from day 1
interface Repository<T> {
  findAll(): Promise<T[]>;
  findById(id: string): Promise<T | null>;
  create(data: Partial<T>): Promise<T>;
  update(id: string, data: Partial<T>): Promise<T>;
  delete(id: string): Promise<void>;
}

class PostRepository implements Repository<Post> {
  // 100 lines of abstraction...
}

// GOOD: Direct and simple
export async function getPosts() {
  return db.query.posts.findMany();
}

export async function createPost(data: NewPost) {
  return db.insert(posts).values(data).returning();
}
```

### 7.2 Wrong Database Choice

```typescript
// BAD: Starting with Postgres + Prisma for a simple app
// - Requires external service
// - Slower local development
// - More configuration

// GOOD: Start with SQLite
// - Zero configuration
// - Instant local development
// - Easy to migrate later
import Database from "better-sqlite3";
import { drizzle } from "drizzle-orm/better-sqlite3";

const sqlite = new Database("app.db");
export const db = drizzle(sqlite);
```

### 7.3 Premature Auth Complexity

```typescript
// BAD: Full OAuth + multiple providers day 1
import NextAuth from "next-auth";
import GitHub from "next-auth/providers/github";
import Google from "next-auth/providers/google";
import Credentials from "next-auth/providers/credentials";
// ... 200 lines of config

// GOOD: Simple cookie auth for MVP
export async function login(email: string, password: string) {
  const user = await verifyCredentials(email, password);
  if (!user) return { error: "Invalid credentials" };

  const session = await createSession(user.id);
  cookies().set("session", session.id, { httpOnly: true });

  return { success: true };
}
```

### 7.4 Unnecessary State Management

```typescript
// BAD: Redux/Zustand for simple state
import { create } from "zustand";

const useStore = create((set) => ({
  user: null,
  posts: [],
  loading: false,
  setUser: (user) => set({ user }),
  setPosts: (posts) => set({ posts }),
  setLoading: (loading) => set({ loading }),
}));

// GOOD: React state + server components
// Most state lives on the server
export default async function PostsPage() {
  const posts = await getPosts(); // Server fetch
  return <PostList posts={posts} />;
}

// Client state only when needed
function PostForm() {
  const [isPending, startTransition] = useTransition();
  // ...
}
```

### 7.5 Over-Componentization

```typescript
// BAD: Component for everything
<Container>
  <Section>
    <Card>
      <CardHeader>
        <CardTitle>
          <Text variant="heading">Title</Text>
        </CardTitle>
      </CardHeader>
      <CardBody>
        <Paragraph>Content</Paragraph>
      </CardBody>
    </Card>
  </Section>
</Container>

// GOOD: Just enough abstraction
<div className="mx-auto max-w-4xl py-8">
  <Card title="Title">
    <p>Content</p>
  </Card>
</div>
```

---

## 8. SQLite-First Patterns

### 8.1 Schema Design

```typescript
// File: src/db/schema.ts
import { sqliteTable, text, integer, real, blob } from "drizzle-orm/sqlite-core";

// Use text for IDs (UUIDs work great)
export const users = sqliteTable("users", {
  id: text("id").primaryKey().$defaultFn(() => crypto.randomUUID()),
  email: text("email").notNull().unique(),
  name: text("name"),
  // Store timestamps as integers (Unix epoch)
  createdAt: integer("created_at", { mode: "timestamp" })
    .$defaultFn(() => new Date()),
});

// JSON stored as text
export const settings = sqliteTable("settings", {
  id: text("id").primaryKey(),
  userId: text("user_id").references(() => users.id),
  // JSON mode auto-serializes
  preferences: text("preferences", { mode: "json" }).$type<{
    theme: "light" | "dark";
    notifications: boolean;
  }>(),
});

// Full-text search ready
export const posts = sqliteTable("posts", {
  id: text("id").primaryKey(),
  title: text("title").notNull(),
  content: text("content"),
  // Create index for common queries
  authorId: text("author_id").references(() => users.id),
});
```

### 8.2 Query Patterns

```typescript
// File: src/db/queries.ts
import { db } from ".";
import { posts, users } from "./schema";
import { eq, like, desc, and, sql } from "drizzle-orm";

// Simple queries
export const getPostById = (id: string) =>
  db.query.posts.findFirst({
    where: eq(posts.id, id),
    with: { author: true },
  });

// Filtered list with pagination
export const getPosts = async (options: {
  search?: string;
  authorId?: string;
  page?: number;
  limit?: number;
}) => {
  const { search, authorId, page = 1, limit = 20 } = options;
  const offset = (page - 1) * limit;

  const conditions = [];
  if (search) {
    conditions.push(like(posts.title, `%${search}%`));
  }
  if (authorId) {
    conditions.push(eq(posts.authorId, authorId));
  }

  return db.query.posts.findMany({
    where: conditions.length > 0 ? and(...conditions) : undefined,
    orderBy: [desc(posts.createdAt)],
    limit,
    offset,
    with: { author: true },
  });
};

// Aggregations
export const getPostStats = async (authorId: string) => {
  const result = await db
    .select({
      total: sql<number>`count(*)`,
      thisMonth: sql<number>`sum(case when created_at > unixepoch('now', '-30 days') then 1 else 0 end)`,
    })
    .from(posts)
    .where(eq(posts.authorId, authorId));

  return result[0];
};
```

### 8.3 Migration to Postgres

```typescript
// When ready to scale, migration is straightforward

// 1. Update drizzle config
// drizzle.config.ts
export default {
  schema: "./src/db/schema.ts",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
};

// 2. Update schema (minimal changes)
// Change imports
import { pgTable, text, timestamp, jsonb } from "drizzle-orm/pg-core";

// 3. Update connection
import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";

const client = postgres(process.env.DATABASE_URL!);
export const db = drizzle(client);

// 4. Run migration
// bun run db:push
```

---

## 9. Server Actions for Forms

### 9.1 Action Patterns

```typescript
// File: src/actions/items.ts
"use server";

import { revalidatePath } from "next/cache";
import { redirect } from "next/navigation";
import { db } from "@/db";
import { items } from "@/db/schema";
import { eq } from "drizzle-orm";
import { z } from "zod";

// Validation schema
const ItemSchema = z.object({
  title: z.string().min(1, "Title is required").max(255),
  content: z.string().optional(),
});

// Type-safe action result
type ActionResult =
  | { success: true; data?: unknown }
  | { success: false; error: string; fieldErrors?: Record<string, string[]> };

// Create with validation
export async function createItem(formData: FormData): Promise<ActionResult> {
  const raw = {
    title: formData.get("title"),
    content: formData.get("content"),
  };

  const parsed = ItemSchema.safeParse(raw);

  if (!parsed.success) {
    return {
      success: false,
      error: "Validation failed",
      fieldErrors: parsed.error.flatten().fieldErrors,
    };
  }

  try {
    const id = crypto.randomUUID();
    await db.insert(items).values({
      id,
      ...parsed.data,
    });

    revalidatePath("/items");
    return { success: true, data: { id } };
  } catch (e) {
    console.error("Create item error:", e);
    return { success: false, error: "Failed to create item" };
  }
}

// Update
export async function updateItem(id: string, formData: FormData): Promise<ActionResult> {
  const raw = {
    title: formData.get("title"),
    content: formData.get("content"),
  };

  const parsed = ItemSchema.safeParse(raw);

  if (!parsed.success) {
    return {
      success: false,
      error: "Validation failed",
      fieldErrors: parsed.error.flatten().fieldErrors,
    };
  }

  try {
    await db.update(items)
      .set({ ...parsed.data, updatedAt: new Date() })
      .where(eq(items.id, id));

    revalidatePath("/items");
    revalidatePath(`/items/${id}`);
    return { success: true };
  } catch (e) {
    console.error("Update item error:", e);
    return { success: false, error: "Failed to update item" };
  }
}

// Delete with redirect
export async function deleteItem(id: string): Promise<void> {
  await db.delete(items).where(eq(items.id, id));
  revalidatePath("/items");
  redirect("/items");
}
```

### 9.2 Form Component with Actions

```typescript
// File: src/components/forms/item-form.tsx
"use client";

import { useActionState } from "react";
import { useEffect, useRef } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface FormState {
  success?: boolean;
  error?: string;
  fieldErrors?: Record<string, string[]>;
}

interface ItemFormProps {
  action: (formData: FormData) => Promise<FormState>;
  initialData?: {
    title: string;
    content?: string | null;
  };
  submitLabel?: string;
  onSuccess?: () => void;
}

export function ItemForm({
  action,
  initialData,
  submitLabel = "Save",
  onSuccess
}: ItemFormProps) {
  const formRef = useRef<HTMLFormElement>(null);

  const [state, formAction, isPending] = useActionState(
    async (_: FormState, formData: FormData) => {
      const result = await action(formData);
      return result;
    },
    {}
  );

  // Handle success
  useEffect(() => {
    if (state.success) {
      formRef.current?.reset();
      onSuccess?.();
    }
  }, [state.success, onSuccess]);

  return (
    <form ref={formRef} action={formAction} className="space-y-4">
      <div>
        <label htmlFor="title" className="block text-sm font-medium">
          Title <span className="text-red-500">*</span>
        </label>
        <Input
          id="title"
          name="title"
          defaultValue={initialData?.title}
          error={state.fieldErrors?.title?.[0]}
          className="mt-1"
        />
      </div>

      <div>
        <label htmlFor="content" className="block text-sm font-medium">
          Content
        </label>
        <textarea
          id="content"
          name="content"
          defaultValue={initialData?.content ?? ""}
          rows={4}
          className="mt-1 w-full rounded-lg border border-zinc-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-zinc-500"
        />
        {state.fieldErrors?.content && (
          <p className="mt-1 text-sm text-red-500">
            {state.fieldErrors.content[0]}
          </p>
        )}
      </div>

      {state.error && !state.fieldErrors && (
        <div className="rounded-lg bg-red-50 p-3 text-sm text-red-600">
          {state.error}
        </div>
      )}

      {state.success && (
        <div className="rounded-lg bg-green-50 p-3 text-sm text-green-600">
          Saved successfully!
        </div>
      )}

      <Button type="submit" loading={isPending}>
        {submitLabel}
      </Button>
    </form>
  );
}
```

---

## 10. Minimal Viable Auth

### 10.1 Cookie-Based Session Auth

```typescript
// File: src/db/schema.ts (auth tables)
import { sqliteTable, text, integer } from "drizzle-orm/sqlite-core";

export const users = sqliteTable("users", {
  id: text("id").primaryKey(),
  email: text("email").notNull().unique(),
  passwordHash: text("password_hash").notNull(),
  name: text("name"),
  createdAt: integer("created_at", { mode: "timestamp" })
    .$defaultFn(() => new Date()),
});

export const sessions = sqliteTable("sessions", {
  id: text("id").primaryKey(),
  userId: text("user_id")
    .notNull()
    .references(() => users.id, { onDelete: "cascade" }),
  expiresAt: integer("expires_at", { mode: "timestamp" }).notNull(),
});
```

```typescript
// File: src/lib/auth.ts
import { cookies } from "next/headers";
import { cache } from "react";
import { db } from "@/db";
import { users, sessions } from "@/db/schema";
import { eq } from "drizzle-orm";

const SESSION_COOKIE = "sid";
const SESSION_DURATION_MS = 7 * 24 * 60 * 60 * 1000; // 7 days

// Password hashing (Bun native)
export async function hash(password: string): Promise<string> {
  return Bun.password.hash(password, {
    algorithm: "bcrypt",
    cost: 10,
  });
}

export async function verify(password: string, hash: string): Promise<boolean> {
  return Bun.password.verify(password, hash);
}

// Session management
export async function createSession(userId: string): Promise<string> {
  const sessionId = crypto.randomUUID();
  const expiresAt = new Date(Date.now() + SESSION_DURATION_MS);

  await db.insert(sessions).values({
    id: sessionId,
    userId,
    expiresAt,
  });

  const cookieStore = await cookies();
  cookieStore.set(SESSION_COOKIE, sessionId, {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax",
    expires: expiresAt,
    path: "/",
  });

  return sessionId;
}

// Cached session getter (deduplicated per request)
export const getSession = cache(async () => {
  const cookieStore = await cookies();
  const sessionId = cookieStore.get(SESSION_COOKIE)?.value;

  if (!sessionId) return null;

  const session = await db.query.sessions.findFirst({
    where: eq(sessions.id, sessionId),
  });

  if (!session) return null;

  // Check expiration
  if (session.expiresAt < new Date()) {
    await db.delete(sessions).where(eq(sessions.id, sessionId));
    cookieStore.delete(SESSION_COOKIE);
    return null;
  }

  // Get user
  const user = await db.query.users.findFirst({
    where: eq(users.id, session.userId),
    columns: {
      id: true,
      email: true,
      name: true,
    },
  });

  return user ? { ...session, user } : null;
});

export async function destroySession(): Promise<void> {
  const cookieStore = await cookies();
  const sessionId = cookieStore.get(SESSION_COOKIE)?.value;

  if (sessionId) {
    await db.delete(sessions).where(eq(sessions.id, sessionId));
    cookieStore.delete(SESSION_COOKIE);
  }
}

// Auth guard for server components
export async function requireAuth() {
  const session = await getSession();
  if (!session) {
    const { redirect } = await import("next/navigation");
    redirect("/login");
  }
  return session;
}
```

```typescript
// File: src/actions/auth.ts
"use server";

import { redirect } from "next/navigation";
import { db } from "@/db";
import { users } from "@/db/schema";
import { eq } from "drizzle-orm";
import { hash, verify, createSession, destroySession } from "@/lib/auth";
import { z } from "zod";

const SignupSchema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(8, "Password must be at least 8 characters"),
  name: z.string().min(1, "Name is required"),
});

const LoginSchema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(1, "Password is required"),
});

export async function signup(formData: FormData) {
  const raw = {
    email: formData.get("email"),
    password: formData.get("password"),
    name: formData.get("name"),
  };

  const parsed = SignupSchema.safeParse(raw);
  if (!parsed.success) {
    return { error: parsed.error.errors[0].message };
  }

  const { email, password, name } = parsed.data;

  // Check existing
  const existing = await db.query.users.findFirst({
    where: eq(users.email, email.toLowerCase()),
  });

  if (existing) {
    return { error: "Email already registered" };
  }

  // Create user
  const id = crypto.randomUUID();
  const passwordHash = await hash(password);

  await db.insert(users).values({
    id,
    email: email.toLowerCase(),
    passwordHash,
    name,
  });

  await createSession(id);
  redirect("/dashboard");
}

export async function login(formData: FormData) {
  const raw = {
    email: formData.get("email"),
    password: formData.get("password"),
  };

  const parsed = LoginSchema.safeParse(raw);
  if (!parsed.success) {
    return { error: parsed.error.errors[0].message };
  }

  const { email, password } = parsed.data;

  const user = await db.query.users.findFirst({
    where: eq(users.email, email.toLowerCase()),
  });

  if (!user) {
    return { error: "Invalid credentials" };
  }

  const valid = await verify(password, user.passwordHash);
  if (!valid) {
    return { error: "Invalid credentials" };
  }

  await createSession(user.id);
  redirect("/dashboard");
}

export async function logout() {
  await destroySession();
  redirect("/login");
}
```

### 10.2 Auth UI Components

```typescript
// File: src/app/(auth)/login/page.tsx
import { LoginForm } from "@/components/auth/login-form";

export default function LoginPage() {
  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="w-full max-w-sm space-y-6">
        <div className="text-center">
          <h1 className="text-2xl font-bold">Welcome back</h1>
          <p className="mt-2 text-zinc-600">Sign in to your account</p>
        </div>
        <LoginForm />
      </div>
    </div>
  );
}
```

```typescript
// File: src/components/auth/login-form.tsx
"use client";

import { useActionState } from "react";
import Link from "next/link";
import { login } from "@/actions/auth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function LoginForm() {
  const [state, action, isPending] = useActionState(
    async (_: { error?: string }, formData: FormData) => {
      return await login(formData);
    },
    {}
  );

  return (
    <form action={action} className="space-y-4">
      <div>
        <label htmlFor="email" className="block text-sm font-medium">
          Email
        </label>
        <Input
          id="email"
          name="email"
          type="email"
          autoComplete="email"
          required
          className="mt-1"
        />
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium">
          Password
        </label>
        <Input
          id="password"
          name="password"
          type="password"
          autoComplete="current-password"
          required
          className="mt-1"
        />
      </div>

      {state.error && (
        <div className="rounded-lg bg-red-50 p-3 text-sm text-red-600">
          {state.error}
        </div>
      )}

      <Button type="submit" loading={isPending} className="w-full">
        Sign in
      </Button>

      <p className="text-center text-sm text-zinc-600">
        Don't have an account?{" "}
        <Link href="/signup" className="font-medium text-zinc-900 hover:underline">
          Sign up
        </Link>
      </p>
    </form>
  );
}
```

### 10.3 Protected Routes

```typescript
// File: src/app/(protected)/layout.tsx
import { requireAuth } from "@/lib/auth";
import { Navbar } from "@/components/layout/navbar";

export default async function ProtectedLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const session = await requireAuth();

  return (
    <div className="min-h-screen">
      <Navbar user={session.user} />
      <main className="mx-auto max-w-7xl px-4 py-8">{children}</main>
    </div>
  );
}
```

```typescript
// File: src/middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

const publicPaths = ["/", "/login", "/signup"];

export function middleware(request: NextRequest) {
  const sessionCookie = request.cookies.get("sid");
  const isPublicPath = publicPaths.some(
    (path) => request.nextUrl.pathname === path
  );

  // Redirect to login if accessing protected route without session
  if (!sessionCookie && !isPublicPath) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  // Redirect to dashboard if accessing auth pages with session
  if (sessionCookie && (request.nextUrl.pathname === "/login" || request.nextUrl.pathname === "/signup")) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
```

---

## Quick Reference

### Commands Cheatsheet

```bash
# Project setup
./scaffold-nextjs-mvp.sh my-app    # Next.js MVP
./scaffold-astro-mvp.sh my-site    # Astro landing
./scaffold-api-mvp.sh my-api       # Hono API

# Feature generation
./gen-component.sh Card --card     # Generate card component
./gen-component.sh ContactForm --form  # Generate form
./gen-feature.sh posts             # Full CRUD feature

# Database
bun run db:push                    # Push schema changes
bun run db:studio                  # Open Drizzle Studio

# Deploy
./deploy-vercel.sh --prod          # Deploy to Vercel
./deploy-railway.sh                # Deploy to Railway
docker compose up -d               # Docker local

# Development
bun run dev                        # Start dev server
bun run build                      # Build for production
```

### File Structure Template

```
src/
├── app/
│   ├── (auth)/
│   │   ├── login/page.tsx
│   │   └── signup/page.tsx
│   ├── (protected)/
│   │   ├── dashboard/page.tsx
│   │   └── layout.tsx
│   ├── api/
│   │   └── health/route.ts
│   ├── layout.tsx
│   └── page.tsx
├── actions/
│   ├── auth.ts
│   └── [feature].ts
├── components/
│   ├── ui/
│   │   ├── button.tsx
│   │   └── input.tsx
│   ├── forms/
│   ├── layout/
│   └── [feature]/
├── db/
│   ├── index.ts
│   └── schema.ts
├── lib/
│   ├── auth.ts
│   └── utils.ts
└── hooks/
```

### Tech Stack Summary

| Layer | MVP Choice | Scale-Up Path |
|-------|------------|---------------|
| Framework | Next.js App Router | Same |
| Styling | Tailwind CSS | Same |
| Database | SQLite + Drizzle | Postgres + Drizzle |
| Auth | Cookie sessions | Auth.js or Lucia |
| Deployment | Vercel | Same or self-host |
| Forms | Server Actions | Same |
| Validation | Zod | Same |
