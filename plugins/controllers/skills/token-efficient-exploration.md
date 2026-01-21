---
skill: token-efficient-exploration
version: "1.0.0"
description: "Patterns for exploring large codebases without exhausting context window"
used-by:
  - repo-scout
  - context-scout
  - codebase-explorer
  - worker
  - all-agents
---

# Token-Efficient Exploration Skill

## Purpose

Explore codebases effectively while minimizing token consumption. Large codebases can easily exhaust context windows if explored naively. This skill provides patterns for maximum insight with minimum tokens.

## Core Principles

### 1. Breadth First, Depth Second
Discover WHAT exists and WHERE before reading HOW it works.

```
❌ Wrong: Read entire file to understand structure
✓ Right: Glob for files → Grep for patterns → Targeted read
```

### 2. Signatures Over Implementations
Extract WHAT things do (interfaces, exports) not HOW (function bodies).

```
❌ Wrong: Read full function implementation
✓ Right: Read function signature and return type
```

### 3. Summarize, Don't Quote
Return insights and patterns, not raw code blocks.

```
❌ Wrong: "Here's the full component:\n```tsx\n[200 lines]```"
✓ Right: "LoginForm at src/auth/LoginForm.tsx:23 uses react-hook-form with zod validation"
```

### 4. Stop Early When Pattern Clear
3-5 examples is enough to understand a pattern.

```
❌ Wrong: Find all 47 instances of the pattern
✓ Right: Find 3-5 representative examples, note "additional instances exist"
```

## Token Budget Guidelines

### Exploration Phase Budget

| Activity | Token Target | Strategy |
|----------|--------------|----------|
| Initial structure discovery | <500 | Glob only |
| Pattern search | <1000 | Grep with files_with_matches |
| Signature extraction | <2000 | Grep with limited context |
| Targeted reads | <1500 | Read with offset/limit |
| **Total exploration** | **<5000** | Stay under budget |

### Per-File Budget

| File Type | Read Strategy | Token Target |
|-----------|---------------|--------------|
| Config files | Full read | <200 |
| Type definitions | Full read | <500 |
| Component files | Signature + props only | <300 |
| Utility files | Export signatures only | <200 |
| Test files | Describe blocks only | <200 |

## Tool Usage Patterns

### Glob: Structure Discovery

Use Glob to understand file organization before reading anything:

```bash
# Understand project structure
Glob("src/**/*.ts")           # All TypeScript files
Glob("src/components/**/*")   # Component organization
Glob("**/*.test.ts")          # Test file locations
Glob("**/index.ts")           # Barrel exports
```

**Token cost:** ~1 token per file path returned

### Grep: Pattern Discovery

Use Grep to find patterns without reading full files:

```bash
# Find patterns (files_with_matches mode - lowest tokens)
Grep("export function use[A-Z]", glob: "**/*.ts", output_mode: "files_with_matches")
# Returns: List of file paths only

# Find patterns with context (content mode - more tokens)
Grep("interface.*Props", glob: "**/*.tsx", output_mode: "content", -A: 5)
# Returns: Matching lines + 5 lines after

# Count occurrences (count mode - minimal tokens)
Grep("useState", glob: "**/*.tsx", output_mode: "count")
# Returns: Count per file
```

**Output mode comparison:**
| Mode | Returns | Tokens | Use When |
|------|---------|--------|----------|
| `files_with_matches` | File paths | ~1/file | Finding where patterns exist |
| `count` | Counts | ~2/file | Gauging prevalence |
| `content` | Lines + context | ~50-200/match | Need actual code |

### Read: Targeted Extraction

Use Read with offset/limit for surgical precision:

```bash
# Read just imports and exports (top of file)
Read(file_path, limit: 30)

# Read specific function (found via Grep at line 45)
Read(file_path, offset: 45, limit: 25)

# Read type definitions (usually grouped)
Read(file_path, offset: 10, limit: 50)
```

**Never do:**
```bash
# ❌ Read entire large file
Read("src/components/BigComponent.tsx")  # Could be 500+ lines

# ✓ Read just what you need
Read("src/components/BigComponent.tsx", limit: 40)  # Imports + signature
```

## Extraction Patterns

### Pattern 1: Function Signatures

Extract what functions do without reading bodies:

```bash
# Find functions
Grep("export (async )?function \\w+", glob: "src/**/*.ts", output_mode: "content")

# Output: function signatures only
# export function validateUser(user: User): ValidationResult
# export async function fetchProfile(id: string): Promise<Profile>
```

### Pattern 2: Interface Definitions

Extract type structure without examples:

```bash
# Find interfaces with properties
Grep("(interface|type) [A-Z]\\w+ (=|\\{)", glob: "**/*.ts", output_mode: "content", -A: 10)

# Use head_limit to avoid too many results
Grep("interface", glob: "**/*.ts", output_mode: "content", -A: 8, head_limit: 50)
```

### Pattern 3: Component Props

Extract component API without implementation:

```bash
# Find Props types
Grep("Props = \\{|Props \\{|interface.*Props", glob: "**/*.tsx", output_mode: "content", -A: 10)

# Find component signatures
Grep("export (default )?(function|const) [A-Z]\\w+.*Props", glob: "**/*.tsx", output_mode: "content", -A: 2)
```

### Pattern 4: Export Structure

Understand module API without internals:

```bash
# Find all exports
Grep("^export", glob: "src/index.ts", output_mode: "content")

# Find barrel exports
Grep("export \\* from|export \\{", glob: "**/index.ts", output_mode: "content")
```

### Pattern 5: Hook Return Values

Understand hook API without implementation:

```bash
# Find return statements in hooks
Grep("return \\{", glob: "src/hooks/**/*.ts", output_mode: "content", -A: 5)
```

## Exploration Workflows

### Workflow 1: New Codebase Survey

```
Step 1: Structure (Glob)
├── Glob("src/**/*.ts") → Understand file count and organization
├── Glob("**/index.ts") → Find entry points
└── Glob("*.config.*") → Find configuration

Step 2: Key Files (Read limited)
├── Read("package.json", limit: 50) → Dependencies
├── Read("tsconfig.json", limit: 30) → TypeScript config
└── Read("src/index.ts", limit: 40) → Main exports

Step 3: Pattern Discovery (Grep)
├── Grep("export.*from", output_mode: "files_with_matches") → Module structure
├── Grep("interface|type", output_mode: "count") → Type density
└── Grep("use[A-Z]", output_mode: "files_with_matches") → Custom hooks

Total tokens: ~2000-3000
```

### Workflow 2: Feature Investigation

```
Step 1: Find Feature Files (Glob)
├── Glob("**/*auth*") → Auth-related files
├── Glob("**/*login*") → Login-specific files
└── Glob("**/*session*") → Session handling

Step 2: Understand Structure (Grep)
├── Grep("export", glob: "**/auth/**", output_mode: "content", head_limit: 30)
├── Grep("interface.*Auth|type.*Auth", output_mode: "content", -A: 10)
└── Grep("useAuth|useSession", output_mode: "files_with_matches")

Step 3: Key Signatures (Read limited)
├── Read("src/hooks/useAuth.ts", limit: 40) → Hook signature
├── Read("src/types/auth.ts", limit: 60) → Type definitions
└── Read("src/lib/auth.ts", limit: 30) → Utility exports

Total tokens: ~1500-2500
```

### Workflow 3: Dependency Tracing

```
Step 1: Find Usages (Grep)
├── Grep("import.*from ['\"]@/lib/auth", output_mode: "files_with_matches")
└── Note file count

Step 2: Sample Usages (Grep with context)
├── Grep("useAuth", glob: "src/components/**", output_mode: "content", -B: 2, -A: 5, head_limit: 20)
└── Understand usage patterns from 3-5 examples

Step 3: Trace Chain (targeted reads)
├── If needed, read specific integration points
└── Use offset/limit for surgical reads

Total tokens: ~1000-2000
```

## Anti-Patterns

### Anti-Pattern 1: Reading for Exploration

```
❌ Wrong:
Read("src/components/Dashboard.tsx")  # 400 lines
Read("src/components/Header.tsx")     # 150 lines
Read("src/components/Sidebar.tsx")    # 200 lines
# Total: 750 lines = ~3000+ tokens just to explore

✓ Right:
Glob("src/components/**/*.tsx")       # File list: ~50 tokens
Grep("export", glob: "src/components/**", output_mode: "content", head_limit: 30)
# Pattern understanding: ~300 tokens
```

### Anti-Pattern 2: Full File Reads for Types

```
❌ Wrong:
Read("src/types/index.ts")  # Entire 500-line type file

✓ Right:
Grep("export (interface|type)", glob: "src/types/**", output_mode: "content", -A: 8, head_limit: 50)
# Just the type signatures: ~400 tokens
```

### Anti-Pattern 3: Exhaustive Pattern Search

```
❌ Wrong:
Grep("useState", glob: "**/*.tsx", output_mode: "content", -A: 10)
# Could return 100+ matches with context = 5000+ tokens

✓ Right:
Grep("useState", glob: "**/*.tsx", output_mode: "count")  # See prevalence
Grep("useState", glob: "**/*.tsx", output_mode: "content", -A: 3, head_limit: 15)
# Sample of pattern: ~300 tokens
```

### Anti-Pattern 4: Raw Code in Output

```
❌ Wrong output:
"Here's the auth hook:
```typescript
export function useAuth() {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)
  // ... 50 more lines
}
```"

✓ Right output:
"useAuth hook at src/hooks/useAuth.ts:5
- Returns: { user: User | null, loading: boolean, login, logout }
- Uses: useState, useEffect, AuthContext
- Pattern: Standard auth state with async login/logout"
```

## Output Format Guidelines

### Summarize Patterns

```markdown
## Exploration: [Topic]

### Files Found
- 12 files matching `*auth*`
- Primary: `src/lib/auth.ts`, `src/hooks/useAuth.ts`
- Components: `src/components/auth/` (5 files)

### Patterns Identified
1. **Auth State**: Managed via `useAuth` hook returning `{ user, login, logout }`
2. **Protected Routes**: Use `withAuth` HOC pattern
3. **API Calls**: All go through `src/lib/api/auth.ts`

### Key Signatures
- `useAuth(): { user: User | null, login: (creds) => Promise<void>, logout: () => void }`
- `withAuth<P>(Component): FC<P>` - HOC for protected routes
- `validateToken(token: string): Promise<boolean>`

### Recommendations
- Follow existing `useAuth` pattern for auth state
- Use `withAuth` for new protected routes
- Auth API calls through `src/lib/api/auth.ts`
```

### Reference Specific Locations

Always include file:line references for follow-up:

```markdown
### Key Locations
- Auth hook: `src/hooks/useAuth.ts:5`
- Auth types: `src/types/auth.ts:12`
- Login component: `src/components/auth/LoginForm.tsx:23`
- Auth API: `src/lib/api/auth.ts:45`
```

## Quality Checklist

Before returning exploration results:
- [ ] Used Glob before Grep
- [ ] Used Grep before Read
- [ ] Read with offset/limit, not full files
- [ ] Stayed under ~5000 token budget
- [ ] Summarized patterns, not quoted code
- [ ] Included file:line references
- [ ] Stopped after 3-5 examples per pattern
- [ ] Output is actionable, not just informational
