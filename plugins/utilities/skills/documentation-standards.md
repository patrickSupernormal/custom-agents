---
skill: documentation-standards
version: "1.0.0"
description: "Best practices for creating clear, maintainable technical documentation"
used-by: ["@documentation-writer", "@api-designer", "@architecture-analyzer", "@onboarding-specialist"]
---

# Documentation Standards Skill

## Overview
Standards and patterns for producing consistent, useful technical documentation across different contexts and audiences.

## Documentation Hierarchy

### Level 1: README (Entry Point)
```markdown
# Project Name

One-line description of what this does.

## Quick Start
\`\`\`bash
npm install
npm run dev
\`\`\`

## Overview
2-3 paragraphs explaining the project's purpose and architecture.

## Documentation
- [Setup Guide](./docs/setup.md)
- [API Reference](./docs/api.md)
- [Contributing](./CONTRIBUTING.md)

## License
MIT
```

### Level 2: Setup/Installation Guide
```markdown
# Setup Guide

## Prerequisites
- Node.js 18+
- PostgreSQL 14+
- Redis (optional, for caching)

## Installation

1. Clone the repository
   \`\`\`bash
   git clone https://github.com/org/project.git
   cd project
   \`\`\`

2. Install dependencies
   \`\`\`bash
   npm install
   \`\`\`

3. Configure environment
   \`\`\`bash
   cp .env.example .env
   # Edit .env with your values
   \`\`\`

4. Initialize database
   \`\`\`bash
   npm run db:migrate
   npm run db:seed  # Optional: sample data
   \`\`\`

## Verification
\`\`\`bash
npm test        # Run test suite
npm run dev     # Start development server
# Visit http://localhost:3000
\`\`\`

## Troubleshooting
| Issue | Solution |
|-------|----------|
| Port 3000 in use | Set `PORT=3001` in .env |
| Database connection failed | Check PostgreSQL is running |
```

### Level 3: API Reference
```markdown
# API Reference

## Authentication
All endpoints require Bearer token authentication.
\`\`\`
Authorization: Bearer <token>
\`\`\`

## Endpoints

### Users

#### GET /api/users
List all users with pagination.

**Query Parameters:**
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| page | number | 1 | Page number |
| limit | number | 20 | Items per page |
| search | string | - | Filter by name/email |

**Response:**
\`\`\`json
{
  "data": [
    { "id": "uuid", "name": "string", "email": "string" }
  ],
  "meta": {
    "total": 100,
    "page": 1,
    "limit": 20
  }
}
\`\`\`

**Example:**
\`\`\`bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://api.example.com/api/users?page=1&limit=10"
\`\`\`
```

## Step-by-Step Writing Procedure

### Phase 1: Audience Analysis
1. **Identify reader level**
   - Beginner: Needs context and explanations
   - Intermediate: Wants efficient steps
   - Expert: Needs reference material only

2. **Determine documentation type**
   - Tutorial: Learning-oriented
   - How-to: Task-oriented
   - Reference: Information-oriented
   - Explanation: Understanding-oriented

### Phase 2: Structure Planning
1. Start with an outline
2. Use progressive disclosure (overview -> details)
3. Group related content
4. Plan code examples

### Phase 3: Writing
1. **Lead with the outcome** - What will the reader achieve?
2. **Use active voice** - "Run the command" not "The command should be run"
3. **One idea per paragraph**
4. **Code examples for every concept**

### Phase 4: Review Checklist
- [ ] All code examples tested and working
- [ ] Links verified
- [ ] Prerequisites listed
- [ ] Error states documented
- [ ] No assumed knowledge without explanation

## Code Documentation Patterns

### Function Documentation (JSDoc)
```typescript
/**
 * Calculates the total price including tax and discounts.
 *
 * @param items - Array of cart items with price and quantity
 * @param taxRate - Tax rate as decimal (e.g., 0.08 for 8%)
 * @param discountCode - Optional discount code to apply
 * @returns Total price in cents
 * @throws {InvalidDiscountError} When discount code is invalid
 *
 * @example
 * const total = calculateTotal(
 *   [{ price: 1000, quantity: 2 }],
 *   0.08,
 *   'SAVE10'
 * );
 * // Returns: 1944 (2000 - 10% + 8% tax)
 */
function calculateTotal(
  items: CartItem[],
  taxRate: number,
  discountCode?: string
): number {
  // Implementation
}
```

### Component Documentation
```typescript
/**
 * Button component with multiple variants and states.
 *
 * @example
 * // Primary button
 * <Button variant="primary" onClick={handleClick}>
 *   Submit
 * </Button>
 *
 * @example
 * // Loading state
 * <Button loading disabled>
 *   Processing...
 * </Button>
 */
interface ButtonProps {
  /** Visual style variant */
  variant?: 'primary' | 'secondary' | 'ghost';
  /** Disables interaction */
  disabled?: boolean;
  /** Shows loading spinner */
  loading?: boolean;
  /** Click handler */
  onClick?: () => void;
  children: React.ReactNode;
}
```

## Decision Criteria

### When to Document
| Scenario | Document? | Type |
|----------|-----------|------|
| Public API | Yes | Reference + Examples |
| Internal utility | Maybe | JSDoc only |
| Complex algorithm | Yes | Explanation + Comments |
| Standard CRUD | No | Self-documenting code |
| Breaking change | Yes | Migration guide |

### Documentation Placement
| Content | Location |
|---------|----------|
| Project overview | README.md |
| API reference | docs/api/ or inline |
| Architecture decisions | docs/adr/ |
| Setup instructions | docs/setup.md |
| Contribution guidelines | CONTRIBUTING.md |

## Common Pitfalls to Avoid

1. **Documenting the obvious** - Don't explain `getUserById(id)` returns a user
2. **Outdated examples** - Always test code snippets
3. **Missing prerequisites** - State required knowledge upfront
4. **Wall of text** - Use headings, lists, and code blocks
5. **Passive voice** - "Run `npm install`" not "npm install should be run"
6. **No error documentation** - Show what can go wrong
7. **Buried information** - Put critical info first

## Templates

### ADR (Architecture Decision Record)
```markdown
# ADR-001: Use PostgreSQL for primary database

## Status
Accepted

## Context
We need a database that supports complex queries and ACID transactions.

## Decision
Use PostgreSQL 14+ as the primary database.

## Consequences
- **Positive:** Strong query capabilities, mature ecosystem
- **Negative:** More complex than SQLite for development
- **Mitigation:** Docker Compose for local development
```

### Changelog Entry
```markdown
## [1.2.0] - 2024-01-15

### Added
- User profile avatars (#123)
- Export to CSV functionality (#145)

### Changed
- Improved search performance by 40%

### Fixed
- Login redirect loop on expired sessions (#156)

### Deprecated
- `getUserByEmail()` - use `findUser({ email })` instead
```

## Quality Metrics

Good documentation should:
- Answer "what does this do?" in the first paragraph
- Be searchable (use clear headings)
- Include working code examples
- Be current (last updated date visible)
- Link to related resources
