---
skill: api-design-patterns
version: "1.0.0"
description: "REST, GraphQL, and tRPC API design principles and implementation patterns"
used-by: [api-architect, backend-engineer, database-architect]
---

# API Design Patterns

## REST API Design

### URL Structure Conventions
```
GET    /api/v1/resources          # List resources
GET    /api/v1/resources/:id      # Get single resource
POST   /api/v1/resources          # Create resource
PUT    /api/v1/resources/:id      # Replace resource
PATCH  /api/v1/resources/:id      # Partial update
DELETE /api/v1/resources/:id      # Delete resource
```

### Nested Resources
```
GET /api/v1/users/:userId/posts        # User's posts
GET /api/v1/posts/:postId/comments     # Post's comments
```

### Query Parameters
- Pagination: `?page=2&limit=20` or `?cursor=abc123`
- Filtering: `?status=active&category=tech`
- Sorting: `?sort=createdAt&order=desc`
- Fields: `?fields=id,title,author`

### Response Envelope Pattern
```typescript
interface ApiResponse<T> {
  success: boolean;
  data: T;
  meta?: {
    page: number;
    limit: number;
    total: number;
    hasMore: boolean;
  };
  error?: {
    code: string;
    message: string;
    details?: unknown;
  };
}
```

## GraphQL Design

### Schema-First Approach
1. Define types before resolvers
2. Use input types for mutations
3. Implement connection pattern for pagination

```graphql
type Query {
  user(id: ID!): User
  users(first: Int, after: String): UserConnection!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
}

type UserEdge {
  node: User!
  cursor: String!
}
```

### Resolver Pattern
```typescript
const resolvers = {
  Query: {
    user: (_, { id }, ctx) => ctx.dataSources.users.getById(id),
  },
  User: {
    posts: (parent, _, ctx) => ctx.dataSources.posts.getByUserId(parent.id),
  },
};
```

## tRPC Design

### Router Structure
```typescript
export const appRouter = router({
  user: router({
    getById: publicProcedure
      .input(z.object({ id: z.string() }))
      .query(({ input, ctx }) => ctx.db.user.findUnique({ where: { id: input.id } })),
    create: protectedProcedure
      .input(createUserSchema)
      .mutation(({ input, ctx }) => ctx.db.user.create({ data: input })),
  }),
});
```

### Procedure Types
- `publicProcedure`: No authentication required
- `protectedProcedure`: Requires authenticated user
- `adminProcedure`: Requires admin role

## Decision Criteria

| Factor | REST | GraphQL | tRPC |
|--------|------|---------|------|
| Multiple clients | Best | Good | Limited |
| Type safety | Manual | Good | Excellent |
| Caching | Simple | Complex | N/A |
| Learning curve | Low | Medium | Low |
| Overfetching | Common | Solved | Solved |

## Common Pitfalls

1. **Inconsistent naming**: Mix of camelCase and snake_case
2. **Missing versioning**: No `/v1/` prefix causes breaking changes
3. **N+1 queries**: Fetch related data inefficiently
4. **No rate limiting**: API abuse vulnerability
5. **Exposing internal IDs**: Use UUIDs or slugs for public APIs
6. **Missing pagination**: Returning unbounded lists
7. **Ignoring HTTP semantics**: Using POST for everything
