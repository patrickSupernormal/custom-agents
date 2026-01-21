---
skill: data-validation
version: "1.0.0"
description: "Zod, validation schemas, and data sanitization patterns"
used-by: [backend-engineer, api-architect, form-specialist]
---

# Data Validation Patterns

## Zod Schema Fundamentals

### Basic Types
```typescript
import { z } from 'zod';

// Primitives
const stringSchema = z.string();
const numberSchema = z.number();
const booleanSchema = z.boolean();
const dateSchema = z.date();

// With constraints
const emailSchema = z.string().email();
const urlSchema = z.string().url();
const uuidSchema = z.string().uuid();
const minMaxSchema = z.string().min(1).max(100);
const positiveSchema = z.number().positive();
const intSchema = z.number().int();
```

### Object Schemas
```typescript
const userSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().positive().optional(),
  role: z.enum(['user', 'admin', 'superadmin']).default('user'),
  createdAt: z.date().default(() => new Date()),
});

type User = z.infer<typeof userSchema>;
```

### Array and Union Schemas
```typescript
const tagsSchema = z.array(z.string()).min(1).max(10);

const responseSchema = z.discriminatedUnion('status', [
  z.object({ status: z.literal('success'), data: z.unknown() }),
  z.object({ status: z.literal('error'), error: z.string() }),
]);
```

## API Validation Patterns

### Request Validation
```typescript
// schemas/api.ts
export const createPostSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.string().min(1),
  slug: z.string().regex(/^[a-z0-9-]+$/),
  published: z.boolean().default(false),
  tags: z.array(z.string()).optional(),
});

export const updatePostSchema = createPostSchema.partial();

export const postIdSchema = z.object({
  id: z.string().uuid(),
});
```

### Route Handler with Validation
```typescript
// app/api/posts/route.ts
import { NextResponse } from 'next/server';
import { createPostSchema } from '@/schemas/api';

export async function POST(request: Request) {
  try {
    const body = await request.json();
    const validated = createPostSchema.parse(body);

    const post = await prisma.post.create({ data: validated });
    return NextResponse.json(post, { status: 201 });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: 'Validation failed', details: error.errors },
        { status: 400 }
      );
    }
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
```

## Form Validation Patterns

### React Hook Form Integration
```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const formSchema = z.object({
  email: z.string().email('Invalid email address'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string(),
}).refine((data) => data.password === data.confirmPassword, {
  message: 'Passwords do not match',
  path: ['confirmPassword'],
});

function SignupForm() {
  const { register, handleSubmit, formState: { errors } } = useForm({
    resolver: zodResolver(formSchema),
  });

  const onSubmit = (data) => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}
      {/* ... */}
    </form>
  );
}
```

## Advanced Patterns

### Custom Refinements
```typescript
const passwordSchema = z.string()
  .min(8)
  .refine((val) => /[A-Z]/.test(val), 'Must contain uppercase')
  .refine((val) => /[a-z]/.test(val), 'Must contain lowercase')
  .refine((val) => /[0-9]/.test(val), 'Must contain number')
  .refine((val) => /[^A-Za-z0-9]/.test(val), 'Must contain special char');
```

### Transform and Preprocess
```typescript
const sanitizedStringSchema = z.string()
  .transform((val) => val.trim().toLowerCase());

const dateFromStringSchema = z.preprocess(
  (val) => (typeof val === 'string' ? new Date(val) : val),
  z.date()
);

const numericStringSchema = z.preprocess(
  (val) => (typeof val === 'string' ? parseInt(val, 10) : val),
  z.number().int().positive()
);
```

### Reusable Schema Compositions
```typescript
const timestampFields = {
  createdAt: z.date().default(() => new Date()),
  updatedAt: z.date().default(() => new Date()),
};

const baseDocumentSchema = z.object({
  id: z.string().uuid(),
  ...timestampFields,
});

const postSchema = baseDocumentSchema.extend({
  title: z.string(),
  content: z.string(),
});
```

## Environment Validation

```typescript
// env.ts
const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  NEXTAUTH_SECRET: z.string().min(32),
  NEXTAUTH_URL: z.string().url(),
  NODE_ENV: z.enum(['development', 'production', 'test']),
  SMTP_HOST: z.string().optional(),
  SMTP_PORT: z.string().transform(Number).optional(),
});

export const env = envSchema.parse(process.env);
```

## Decision Criteria

| Pattern | Use When |
|---------|----------|
| `.parse()` | Throw on invalid data |
| `.safeParse()` | Handle errors gracefully |
| `.partial()` | Update operations |
| `.pick()/.omit()` | Subset of fields |
| `.refine()` | Cross-field validation |
| `.transform()` | Data normalization |

## Common Pitfalls

1. **Not using safeParse**: Unhandled exceptions in API routes
2. **Duplicating schemas**: Keep single source of truth
3. **Missing error messages**: Poor user experience
4. **Over-validating**: Trust already-validated internal data
5. **Ignoring transform order**: Validate then transform
6. **No environment validation**: Runtime crashes from missing env vars
7. **Circular dependencies**: Schemas importing each other
