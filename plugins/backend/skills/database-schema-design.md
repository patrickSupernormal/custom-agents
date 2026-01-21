---
skill: database-schema-design
version: "1.0.0"
description: "Database schema patterns, normalization, indexes, and Prisma/Drizzle patterns"
used-by: [database-architect, backend-engineer, api-architect]
---

# Database Schema Design

## Schema Design Process

### Step 1: Identify Entities
- List all nouns from requirements
- Determine primary entities vs attributes
- Identify relationships between entities

### Step 2: Define Relationships
```
One-to-One:   User ←→ Profile
One-to-Many:  User ←→ Posts
Many-to-Many: Posts ←→ Tags (via PostTags)
```

### Step 3: Normalization Levels
- **1NF**: Atomic values, no repeating groups
- **2NF**: No partial dependencies on composite keys
- **3NF**: No transitive dependencies

## Prisma Schema Patterns

### Base Model Pattern
```prisma
model BaseEntity {
  id        String   @id @default(cuid())
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}
```

### User Model with Relations
```prisma
model User {
  id            String    @id @default(cuid())
  email         String    @unique
  emailVerified DateTime?
  name          String?
  image         String?
  accounts      Account[]
  sessions      Session[]
  posts         Post[]
  createdAt     DateTime  @default(now())
  updatedAt     DateTime  @updatedAt

  @@index([email])
}
```

### Many-to-Many Pattern
```prisma
model Post {
  id         String   @id @default(cuid())
  title      String
  content    String?
  published  Boolean  @default(false)
  author     User     @relation(fields: [authorId], references: [id])
  authorId   String
  tags       Tag[]
  categories Category[]

  @@index([authorId])
  @@index([published, createdAt])
}

model Tag {
  id    String @id @default(cuid())
  name  String @unique
  slug  String @unique
  posts Post[]
}
```

### Soft Delete Pattern
```prisma
model Document {
  id        String    @id @default(cuid())
  title     String
  deletedAt DateTime?

  @@index([deletedAt])
}
```

## Index Strategy

### When to Add Indexes
1. Foreign key columns (automatic in some DBs)
2. Columns in WHERE clauses
3. Columns in ORDER BY
4. Columns in JOIN conditions
5. Unique constraints

### Composite Index Order
```prisma
// Query: WHERE status = 'active' AND createdAt > date
@@index([status, createdAt])  // Correct order

// Query: WHERE authorId = x ORDER BY createdAt DESC
@@index([authorId, createdAt(sort: Desc)])
```

### Index Anti-Patterns
- Indexing low-cardinality columns alone (e.g., boolean)
- Too many indexes (slows writes)
- Unused indexes

## Drizzle Schema Patterns

```typescript
import { pgTable, text, timestamp, boolean, index } from 'drizzle-orm/pg-core';

export const users = pgTable('users', {
  id: text('id').primaryKey().$defaultFn(() => createId()),
  email: text('email').notNull().unique(),
  name: text('name'),
  createdAt: timestamp('created_at').defaultNow().notNull(),
  updatedAt: timestamp('updated_at').defaultNow().notNull(),
}, (table) => ({
  emailIdx: index('email_idx').on(table.email),
}));

export const posts = pgTable('posts', {
  id: text('id').primaryKey().$defaultFn(() => createId()),
  title: text('title').notNull(),
  published: boolean('published').default(false),
  authorId: text('author_id').references(() => users.id),
}, (table) => ({
  authorIdx: index('author_idx').on(table.authorId),
}));
```

## Decision Criteria

| Pattern | Use When |
|---------|----------|
| UUID/CUID | Distributed systems, public IDs |
| Auto-increment | Simple apps, internal IDs |
| Soft delete | Audit trails, recovery needed |
| Hard delete | GDPR compliance, storage limits |
| JSON column | Flexible schema, rarely queried |
| Separate table | Structured data, frequently queried |

## Common Pitfalls

1. **Missing indexes on foreign keys**: Slow JOIN operations
2. **Over-normalization**: Too many JOINs for simple queries
3. **Under-normalization**: Data inconsistency, update anomalies
4. **No cascade rules**: Orphaned records
5. **Using reserved words**: Column names like `order`, `user`
6. **Ignoring data types**: Using TEXT for everything
7. **No default timestamps**: Missing audit trail
