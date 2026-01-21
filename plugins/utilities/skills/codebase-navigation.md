---
skill: codebase-navigation
version: "1.0.0"
description: "Efficient techniques for exploring and understanding codebases of any size"
used-by: ["@code-explorer", "@architecture-analyzer", "@debugger", "@refactor-specialist"]
---

# Codebase Navigation Skill

## Overview
Systematic approach to exploring unfamiliar codebases efficiently, identifying key structures, and building mental models quickly.

## Step-by-Step Navigation Procedure

### Phase 1: Initial Reconnaissance (2-3 minutes)
1. **Check root structure**
   ```bash
   ls -la  # View all files including hidden
   ```

2. **Identify project type via config files**
   ```bash
   # Look for framework indicators
   ls package.json composer.json Gemfile requirements.txt go.mod Cargo.toml 2>/dev/null
   ```

3. **Read primary config**
   ```bash
   # JavaScript/TypeScript projects
   cat package.json | head -50

   # Check for monorepo structure
   ls packages/ apps/ libs/ 2>/dev/null
   ```

### Phase 2: Architecture Discovery (5-10 minutes)
1. **Map directory structure**
   ```bash
   # Get directory tree (depth 3)
   find . -type d -maxdepth 3 | grep -v node_modules | grep -v .git | head -50
   ```

2. **Identify entry points**
   - `src/index.*` or `src/main.*`
   - `app/` directory (Rails, Next.js)
   - `pages/` or `routes/` (routing)

3. **Find configuration layers**
   ```bash
   # Common config patterns
   ls -la *.config.* .*.rc .*.json tsconfig.json 2>/dev/null
   ```

### Phase 3: Code Pattern Analysis
1. **Locate type definitions** (TypeScript projects)
   ```bash
   find . -name "*.d.ts" -o -name "types.ts" -o -name "interfaces.ts" | head -20
   ```

2. **Find API boundaries**
   ```bash
   # Search for API routes
   find . -path "*/api/*" -name "*.ts" | head -20

   # Search for route definitions
   grep -r "router\." --include="*.ts" -l | head -10
   ```

3. **Identify shared utilities**
   ```bash
   ls src/utils/ src/lib/ src/helpers/ src/shared/ 2>/dev/null
   ```

## Decision Criteria

### When to Deep-Dive vs. Skim
| Scenario | Action |
|----------|--------|
| Bug in specific feature | Trace from entry point to affected code |
| General understanding | Map high-level structure first |
| Performance issue | Focus on data flow and async patterns |
| Adding new feature | Study similar existing features |

### File Priority Order
1. **README.md** - Project overview and setup
2. **package.json/config** - Dependencies and scripts
3. **Entry points** - Application flow
4. **Types/Interfaces** - Data structures
5. **Routes/API** - External boundaries

## Code Snippet Patterns

### Quick Component Location
```bash
# Find React components by name
grep -r "export.*function ComponentName" --include="*.tsx" -l

# Find by export pattern
grep -r "export default" --include="*.tsx" -l | xargs grep -l "ComponentName"
```

### Dependency Tracing
```bash
# Find all imports of a module
grep -r "from ['\"].*moduleName" --include="*.ts" --include="*.tsx"

# Find usage of a function
grep -r "functionName(" --include="*.ts" --include="*.tsx" | head -20
```

### Database Schema Discovery
```bash
# Prisma schemas
cat prisma/schema.prisma

# TypeORM entities
find . -name "*.entity.ts" | head -10

# Drizzle schemas
find . -name "schema.ts" -path "*/db/*"
```

## Common Pitfalls to Avoid

1. **Starting with tests** - Tests provide context but not architecture
2. **Ignoring .gitignore** - Reveals what's generated vs. source
3. **Skipping README** - Often contains critical context
4. **Deep-diving too early** - Map structure before details
5. **Missing environment files** - Check `.env.example` for required config
6. **Ignoring CI/CD configs** - `.github/workflows/` reveals build process

## Navigation Shortcuts

### By File Type
```bash
# All TypeScript files (excluding tests)
find . -name "*.ts" ! -name "*.test.ts" ! -name "*.spec.ts" | head -30

# Configuration files only
find . -maxdepth 2 -name "*.config.*" -o -name ".*rc" 2>/dev/null
```

### By Content Pattern
```bash
# Files with TODO comments
grep -r "TODO\|FIXME\|HACK" --include="*.ts" -l

# Files with error handling
grep -r "catch\|throw new" --include="*.ts" -l | head -10
```

## Mental Model Building

Create a quick architecture map:
```
Project: [name]
Type: [monorepo/single-app/library]
Framework: [next/express/fastify/etc]
Database: [prisma/drizzle/typeorm/none]
State: [redux/zustand/jotai/none]
Styling: [tailwind/styled/css-modules]
Testing: [jest/vitest/playwright]
```

## Output Format

When reporting navigation findings:
```markdown
## Codebase Overview

### Structure
- Type: [project type]
- Entry: [entry point path]
- Key dirs: [important directories]

### Key Files
1. [path] - [purpose]
2. [path] - [purpose]

### Dependencies (notable)
- [package]: [why it matters]

### Recommended Starting Points
- For [goal]: Start at [path]
```
