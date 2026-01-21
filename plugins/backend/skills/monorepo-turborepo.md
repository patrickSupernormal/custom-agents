---
skill: monorepo-turborepo
version: "1.0.0"
description: "Turborepo and pnpm workspace architecture for scalable monorepo development"
used-by: [monorepo-architect, devops-engineer, platform-engineer]
---

# Monorepo Architecture with Turborepo

## Overview

This skill covers production-ready monorepo setup using Turborepo for build orchestration and pnpm workspaces for package management. Includes project structure, configuration, task pipelines, and CI/CD optimization.

---

## 1. Project Structure

### Standard Monorepo Layout

```
my-monorepo/
├── apps/
│   ├── web/                    # Next.js web application
│   │   ├── package.json
│   │   ├── next.config.js
│   │   └── src/
│   ├── docs/                   # Documentation site
│   │   ├── package.json
│   │   └── src/
│   └── api/                    # Backend API service
│       ├── package.json
│       └── src/
├── packages/
│   ├── ui/                     # Shared React components
│   │   ├── package.json
│   │   ├── src/
│   │   └── tsconfig.json
│   ├── utils/                  # Shared utilities
│   │   ├── package.json
│   │   └── src/
│   ├── config-eslint/          # Shared ESLint configuration
│   │   ├── package.json
│   │   └── index.js
│   ├── config-typescript/      # Shared TypeScript configuration
│   │   ├── package.json
│   │   ├── base.json
│   │   ├── nextjs.json
│   │   └── react-library.json
│   └── database/               # Database client and schemas
│       ├── package.json
│       └── src/
├── turbo.json
├── pnpm-workspace.yaml
├── package.json
└── .npmrc
```

### Directory Conventions

| Directory | Purpose | Examples |
|-----------|---------|----------|
| `apps/` | Deployable applications | web, api, mobile, admin |
| `packages/` | Shared internal packages | ui, utils, config, types |
| `tooling/` | Development tools (optional) | scripts, generators |

---

## 2. Configuration Files

### Root package.json

```json
{
  "name": "my-monorepo",
  "private": true,
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev",
    "lint": "turbo run lint",
    "test": "turbo run test",
    "typecheck": "turbo run typecheck",
    "clean": "turbo run clean && rm -rf node_modules",
    "format": "prettier --write \"**/*.{ts,tsx,js,jsx,json,md}\""
  },
  "devDependencies": {
    "prettier": "^3.2.0",
    "turbo": "^2.3.0"
  },
  "packageManager": "pnpm@9.15.0",
  "engines": {
    "node": ">=20"
  }
}
```

### pnpm-workspace.yaml

```yaml
packages:
  - "apps/*"
  - "packages/*"
  - "tooling/*"
```

### .npmrc

```ini
# Use workspace protocol for internal packages
link-workspace-packages=true

# Hoist dependencies to root (recommended)
shamefully-hoist=true

# Strict peer dependencies
strict-peer-dependencies=false

# Auto-install peers
auto-install-peers=true
```

### turbo.json (Comprehensive)

```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalDependencies": [
    ".env",
    ".env.local"
  ],
  "globalEnv": [
    "NODE_ENV",
    "VERCEL_ENV"
  ],
  "ui": "tui",
  "tasks": {
    "build": {
      "dependsOn": ["^build"],
      "inputs": ["$TURBO_DEFAULT$", ".env*"],
      "outputs": [
        ".next/**",
        "!.next/cache/**",
        "dist/**",
        "build/**"
      ]
    },
    "dev": {
      "cache": false,
      "persistent": true
    },
    "lint": {
      "dependsOn": ["^build"],
      "inputs": ["$TURBO_DEFAULT$", ".eslintrc*", "eslint.config.*"]
    },
    "typecheck": {
      "dependsOn": ["^build"],
      "inputs": ["$TURBO_DEFAULT$", "tsconfig.json"]
    },
    "test": {
      "dependsOn": ["^build"],
      "inputs": ["$TURBO_DEFAULT$", "**/*.test.{ts,tsx}"],
      "outputs": ["coverage/**"]
    },
    "test:watch": {
      "cache": false,
      "persistent": true
    },
    "clean": {
      "cache": false
    },
    "db:generate": {
      "cache": false
    },
    "db:push": {
      "cache": false
    }
  }
}
```

---

## 3. Package Patterns

### Internal Package (No Build Step)

Recommended for most internal packages. Uses TypeScript paths for direct source imports.

**packages/ui/package.json**
```json
{
  "name": "@repo/ui",
  "version": "0.0.0",
  "private": true,
  "exports": {
    ".": {
      "types": "./src/index.ts",
      "default": "./src/index.ts"
    },
    "./button": {
      "types": "./src/button.tsx",
      "default": "./src/button.tsx"
    },
    "./card": {
      "types": "./src/card.tsx",
      "default": "./src/card.tsx"
    }
  },
  "scripts": {
    "lint": "eslint src/",
    "typecheck": "tsc --noEmit"
  },
  "peerDependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0"
  },
  "devDependencies": {
    "@repo/config-eslint": "workspace:*",
    "@repo/config-typescript": "workspace:*",
    "@types/react": "^18.2.0",
    "eslint": "^9.0.0",
    "typescript": "^5.3.0"
  }
}
```

### Internal Package (With Build Step)

For packages that need compilation (e.g., publishing externally).

**packages/utils/package.json**
```json
{
  "name": "@repo/utils",
  "version": "0.0.0",
  "private": true,
  "main": "./dist/index.js",
  "module": "./dist/index.mjs",
  "types": "./dist/index.d.ts",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.mjs",
      "require": "./dist/index.js"
    }
  },
  "scripts": {
    "build": "tsup src/index.ts --format cjs,esm --dts",
    "dev": "tsup src/index.ts --format cjs,esm --dts --watch",
    "lint": "eslint src/",
    "typecheck": "tsc --noEmit",
    "clean": "rm -rf dist"
  },
  "devDependencies": {
    "@repo/config-typescript": "workspace:*",
    "tsup": "^8.0.0",
    "typescript": "^5.3.0"
  }
}
```

### Shared ESLint Configuration

**packages/config-eslint/package.json**
```json
{
  "name": "@repo/config-eslint",
  "version": "0.0.0",
  "private": true,
  "main": "./index.js",
  "exports": {
    ".": "./index.js",
    "./next": "./next.js",
    "./react": "./react.js",
    "./typescript": "./typescript.js"
  },
  "dependencies": {
    "@typescript-eslint/eslint-plugin": "^7.0.0",
    "@typescript-eslint/parser": "^7.0.0",
    "eslint-config-next": "^14.0.0",
    "eslint-config-prettier": "^9.0.0",
    "eslint-plugin-react": "^7.33.0",
    "eslint-plugin-react-hooks": "^4.6.0"
  }
}
```

**packages/config-eslint/index.js**
```javascript
/** @type {import('eslint').Linter.Config} */
module.exports = {
  extends: ['eslint:recommended', 'prettier'],
  env: {
    node: true,
    es2022: true,
  },
  parserOptions: {
    ecmaVersion: 'latest',
    sourceType: 'module',
  },
  ignorePatterns: [
    'node_modules',
    'dist',
    '.next',
    'coverage',
  ],
};
```

**packages/config-eslint/next.js**
```javascript
const baseConfig = require('./index');

/** @type {import('eslint').Linter.Config} */
module.exports = {
  ...baseConfig,
  extends: [
    ...baseConfig.extends,
    'next/core-web-vitals',
  ],
  rules: {
    '@next/next/no-html-link-for-pages': 'off',
  },
};
```

### Shared TypeScript Configuration

**packages/config-typescript/base.json**
```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "compilerOptions": {
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "moduleResolution": "bundler",
    "module": "ESNext",
    "target": "ES2022",
    "lib": ["ES2022"],
    "resolveJsonModule": true,
    "isolatedModules": true,
    "noEmit": true,
    "declaration": true,
    "declarationMap": true,
    "incremental": true
  },
  "exclude": ["node_modules", "dist", ".next", "coverage"]
}
```

**packages/config-typescript/nextjs.json**
```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "extends": "./base.json",
  "compilerOptions": {
    "lib": ["DOM", "DOM.Iterable", "ES2022"],
    "jsx": "preserve",
    "plugins": [{ "name": "next" }],
    "allowJs": true,
    "noEmit": true
  }
}
```

**packages/config-typescript/react-library.json**
```json
{
  "$schema": "https://json.schemastore.org/tsconfig",
  "extends": "./base.json",
  "compilerOptions": {
    "lib": ["DOM", "DOM.Iterable", "ES2022"],
    "jsx": "react-jsx"
  }
}
```

---

## 4. Task Pipelines

### Understanding dependsOn

```json
{
  "tasks": {
    "build": {
      "dependsOn": ["^build"]
    }
  }
}
```

| Syntax | Meaning |
|--------|---------|
| `^build` | Run `build` in all dependencies FIRST |
| `build` | Run `build` in same package (self-reference) |
| `lint` | Run `lint` task in same package |
| `@repo/ui#build` | Run `build` specifically in @repo/ui |

### Task Configuration Options

```json
{
  "tasks": {
    "build": {
      "dependsOn": ["^build", "codegen"],
      "inputs": [
        "$TURBO_DEFAULT$",
        ".env*",
        "!.env.local"
      ],
      "outputs": [
        "dist/**",
        ".next/**",
        "!.next/cache/**"
      ],
      "env": ["DATABASE_URL", "API_KEY"],
      "passThroughEnv": ["CI", "VERCEL"],
      "outputLogs": "new-only"
    },
    "dev": {
      "cache": false,
      "persistent": true,
      "dependsOn": ["^build"]
    },
    "test": {
      "dependsOn": ["build"],
      "inputs": ["src/**", "tests/**"],
      "outputs": ["coverage/**"],
      "outputLogs": "full"
    }
  }
}
```

### Inputs and Outputs Explained

**Inputs** - Files that affect task output (for cache invalidation):
- `$TURBO_DEFAULT$` - All files tracked by git
- `src/**/*.ts` - Specific file patterns
- `!**/*.test.ts` - Exclude patterns (with !)
- `.env*` - Environment files

**Outputs** - Files produced by task (for caching):
- `dist/**` - Build output directory
- `.next/**` - Next.js build output
- `!.next/cache/**` - Exclude Next.js cache

---

## 5. Filtered Runs

### Filter Syntax Reference

```bash
# Run in specific package
pnpm turbo run build --filter=@repo/web

# Run in package and its dependencies
pnpm turbo run build --filter=@repo/web...

# Run in package and its dependents
pnpm turbo run build --filter=...@repo/ui

# Run in package, dependencies, AND dependents
pnpm turbo run build --filter=...@repo/ui...

# Run in all packages in apps/
pnpm turbo run build --filter="./apps/*"

# Run in packages changed since main
pnpm turbo run build --filter="[main]"

# Run in packages changed in last commit
pnpm turbo run build --filter="[HEAD^1]"

# Combine filters
pnpm turbo run build --filter="@repo/web" --filter="@repo/api"

# Exclude packages
pnpm turbo run build --filter="!@repo/docs"
```

### Common Filter Patterns

| Use Case | Command |
|----------|---------|
| Build single app | `turbo run build --filter=@repo/web` |
| Build app with deps | `turbo run build --filter=@repo/web...` |
| Test changed packages | `turbo run test --filter="[main]"` |
| Lint all apps | `turbo run lint --filter="./apps/*"` |
| Build everything except docs | `turbo run build --filter="!@repo/docs"` |

---

## 6. Shared Code Patterns

### Importing Internal Packages

**apps/web/package.json**
```json
{
  "name": "@repo/web",
  "dependencies": {
    "@repo/ui": "workspace:*",
    "@repo/utils": "workspace:*",
    "@repo/database": "workspace:*"
  }
}
```

### TypeScript Path Configuration

**apps/web/tsconfig.json**
```json
{
  "extends": "@repo/config-typescript/nextjs.json",
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@repo/ui": ["../../packages/ui/src"],
      "@repo/ui/*": ["../../packages/ui/src/*"],
      "@repo/utils": ["../../packages/utils/src"],
      "@repo/utils/*": ["../../packages/utils/src/*"]
    }
  },
  "include": [
    "next-env.d.ts",
    "**/*.ts",
    "**/*.tsx",
    "../../packages/ui/src/**/*.ts",
    "../../packages/ui/src/**/*.tsx"
  ],
  "exclude": ["node_modules"]
}
```

### Next.js Transpilation

**apps/web/next.config.js**
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  transpilePackages: ['@repo/ui', '@repo/utils'],
  experimental: {
    // Enable external packages optimization
    optimizePackageImports: ['@repo/ui'],
  },
};

module.exports = nextConfig;
```

### Usage in Application Code

```typescript
// apps/web/src/app/page.tsx
import { Button, Card } from '@repo/ui';
import { formatDate, cn } from '@repo/utils';
import { db } from '@repo/database';

export default async function HomePage() {
  const posts = await db.post.findMany();

  return (
    <main>
      {posts.map((post) => (
        <Card key={post.id}>
          <h2>{post.title}</h2>
          <p>{formatDate(post.createdAt)}</p>
          <Button variant="primary">Read More</Button>
        </Card>
      ))}
    </main>
  );
}
```

---

## 7. Environment Variables

### turbo.json Environment Configuration

```json
{
  "globalEnv": [
    "NODE_ENV",
    "CI",
    "VERCEL_ENV"
  ],
  "globalDependencies": [
    ".env"
  ],
  "tasks": {
    "build": {
      "env": [
        "DATABASE_URL",
        "NEXT_PUBLIC_API_URL"
      ],
      "passThroughEnv": [
        "AWS_ACCESS_KEY_ID",
        "AWS_SECRET_ACCESS_KEY"
      ]
    }
  }
}
```

### Environment Variable Types

| Configuration | Purpose | Cache Impact |
|---------------|---------|--------------|
| `globalEnv` | Variables affecting all tasks | Invalidates all caches |
| `env` (per task) | Variables for specific task | Invalidates that task's cache |
| `passThroughEnv` | Variables passed but not cached | No cache impact |
| `globalDependencies` | Files affecting all tasks | Invalidates all caches |

### Environment File Structure

```
my-monorepo/
├── .env                  # Shared defaults (committed)
├── .env.local            # Local overrides (gitignored)
├── apps/
│   └── web/
│       ├── .env          # App-specific defaults
│       └── .env.local    # App-specific local overrides
```

### Root .env Example

```bash
# .env (committed - no secrets)
NODE_ENV=development
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### App-Specific .env

```bash
# apps/web/.env.local (gitignored)
DATABASE_URL="postgresql://..."
NEXT_PUBLIC_API_URL="http://localhost:4000"
```

---

## 8. CI/CD Patterns

### GitHub Actions with Turborepo

**.github/workflows/ci.yml**
```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
  TURBO_TEAM: ${{ vars.TURBO_TEAM }}

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 2

      - name: Setup pnpm
        uses: pnpm/action-setup@v3
        with:
          version: 9

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build
        run: pnpm turbo run build

      - name: Lint
        run: pnpm turbo run lint

      - name: Type Check
        run: pnpm turbo run typecheck

      - name: Test
        run: pnpm turbo run test

  # Optimized: Only build affected packages on PRs
  build-affected:
    if: github.event_name == 'pull_request'
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Setup pnpm
        uses: pnpm/action-setup@v3
        with:
          version: 9

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'

      - name: Install dependencies
        run: pnpm install --frozen-lockfile

      - name: Build affected packages
        run: pnpm turbo run build --filter="[origin/main]"
```

### Remote Caching Setup

```yaml
# Add to workflow env section
env:
  TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
  TURBO_TEAM: ${{ vars.TURBO_TEAM }}
  TURBO_REMOTE_ONLY: true
```

**Vercel Remote Cache (Recommended)**
```bash
# Login to Vercel (one-time setup)
npx turbo login

# Link to remote cache
npx turbo link
```

### Parallel Job Matrix

```yaml
jobs:
  lint-and-typecheck:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        task: [lint, typecheck]
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm turbo run ${{ matrix.task }}
    env:
      TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
      TURBO_TEAM: ${{ vars.TURBO_TEAM }}

  test:
    needs: lint-and-typecheck
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v3
        with:
          version: 9
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'pnpm'
      - run: pnpm install --frozen-lockfile
      - run: pnpm turbo run test
    env:
      TURBO_TOKEN: ${{ secrets.TURBO_TOKEN }}
      TURBO_TEAM: ${{ vars.TURBO_TEAM }}
```

### Deploy Preview per App

```yaml
name: Deploy Preview

on:
  pull_request:
    branches: [main]

jobs:
  detect-changes:
    runs-on: ubuntu-latest
    outputs:
      web: ${{ steps.filter.outputs.web }}
      docs: ${{ steps.filter.outputs.docs }}
    steps:
      - uses: actions/checkout@v4
      - uses: dorny/paths-filter@v3
        id: filter
        with:
          filters: |
            web:
              - 'apps/web/**'
              - 'packages/ui/**'
              - 'packages/utils/**'
            docs:
              - 'apps/docs/**'
              - 'packages/ui/**'

  deploy-web-preview:
    needs: detect-changes
    if: needs.detect-changes.outputs.web == 'true'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: amondnet/vercel-action@v25
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID_WEB }}
          working-directory: ./apps/web
```

---

## 9. Common Commands Reference

### Development

```bash
# Start all apps in dev mode
pnpm dev

# Start specific app
pnpm turbo run dev --filter=@repo/web

# Start app and watch dependencies
pnpm turbo run dev --filter=@repo/web...
```

### Building

```bash
# Build all packages
pnpm build

# Build specific package
pnpm turbo run build --filter=@repo/web

# Build with dependencies
pnpm turbo run build --filter=@repo/web...

# Build only changed packages
pnpm turbo run build --filter="[main]"

# Build with verbose output
pnpm turbo run build --output-logs=full

# Build without cache
pnpm turbo run build --force
```

### Testing and Linting

```bash
# Run all tests
pnpm test

# Run tests for specific package
pnpm turbo run test --filter=@repo/utils

# Run tests in watch mode
pnpm turbo run test:watch --filter=@repo/utils

# Lint all packages
pnpm lint

# Lint changed packages only
pnpm turbo run lint --filter="[main]"

# Type check all packages
pnpm turbo run typecheck
```

### Package Management

```bash
# Add dependency to specific package
pnpm add lodash --filter=@repo/utils

# Add dev dependency to specific package
pnpm add -D vitest --filter=@repo/utils

# Add workspace dependency
pnpm add @repo/ui --filter=@repo/web --workspace

# Update all dependencies
pnpm update -r

# Remove dependency from package
pnpm remove lodash --filter=@repo/utils

# Install all dependencies
pnpm install

# Clean install (remove lockfile)
pnpm install --force
```

### Turborepo Utilities

```bash
# View dependency graph
pnpm turbo run build --graph

# Generate SVG dependency graph
pnpm turbo run build --graph=graph.svg

# View what would run (dry run)
pnpm turbo run build --dry-run

# Prune monorepo for deployment
pnpm turbo prune @repo/web --docker

# Clear local cache
pnpm turbo run build --force
rm -rf .turbo
```

---

## 10. Performance Tips

### Cache Optimization

1. **Specify precise inputs and outputs**
```json
{
  "tasks": {
    "build": {
      "inputs": ["src/**", "package.json", "tsconfig.json"],
      "outputs": ["dist/**"]
    }
  }
}
```

2. **Exclude test files from build inputs**
```json
{
  "tasks": {
    "build": {
      "inputs": ["$TURBO_DEFAULT$", "!**/*.test.ts", "!**/*.spec.ts"]
    }
  }
}
```

3. **Use remote caching**
```bash
# Enable remote cache
npx turbo login
npx turbo link
```

### Build Performance

1. **Use internal packages without build steps**
   - Point exports directly to source files
   - Let consuming app handle transpilation

2. **Parallelize independent tasks**
   - Ensure tasks without dependencies run in parallel
   - Use task graph to identify bottlenecks

3. **Optimize TypeScript compilation**
```json
{
  "compilerOptions": {
    "incremental": true,
    "tsBuildInfoFile": ".tsbuildinfo"
  }
}
```

### CI Performance

1. **Use pnpm for faster installs**
```yaml
- uses: pnpm/action-setup@v3
  with:
    version: 9
```

2. **Enable dependency caching**
```yaml
- uses: actions/setup-node@v4
  with:
    node-version: 20
    cache: 'pnpm'
```

3. **Filter to affected packages**
```yaml
- run: pnpm turbo run build --filter="[origin/main]"
```

4. **Use shallow clone for PRs**
```yaml
- uses: actions/checkout@v4
  with:
    fetch-depth: 2  # Or 0 for full history with filter
```

### Memory and Resource Management

1. **Limit parallel tasks**
```bash
pnpm turbo run build --concurrency=50%
```

2. **Set Node.js memory limits**
```bash
NODE_OPTIONS="--max-old-space-size=4096" pnpm turbo run build
```

---

## Decision Criteria

| Scenario | Recommendation |
|----------|----------------|
| Small team, few packages | Internal packages without build |
| Publishing to npm | Packages with build step (tsup) |
| Many dependent packages | Remote caching essential |
| Frequent PRs | Affected-only builds in CI |
| Multiple apps | Separate Vercel projects per app |

---

## Common Pitfalls

1. **Circular dependencies** - Use `turbo run build --graph` to detect
2. **Missing transpilePackages** - Next.js needs explicit config for workspace packages
3. **Overly broad inputs** - Causes unnecessary cache invalidation
4. **Missing outputs** - Task results not cached properly
5. **env vs globalEnv confusion** - Use globalEnv sparingly
6. **Not using workspace:* protocol** - Leads to version mismatches
7. **Forgetting --filter on large monorepos** - Full builds are slow
8. **No remote caching in CI** - Repeated builds waste time

---

## Validation Checklist

- [ ] pnpm-workspace.yaml includes all package directories
- [ ] turbo.json has proper task configuration
- [ ] All internal packages use workspace:* protocol
- [ ] TypeScript paths configured in consuming apps
- [ ] next.config.js has transpilePackages for workspace packages
- [ ] CI uses remote caching
- [ ] Affected-only builds enabled for PRs
- [ ] Environment variables properly configured
- [ ] Task inputs/outputs precisely specified
- [ ] No circular dependencies in package graph
