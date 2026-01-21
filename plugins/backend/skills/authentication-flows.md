---
skill: authentication-flows
version: "1.0.0"
description: "Auth.js, OAuth, JWT, and session-based authentication patterns"
used-by: [auth-security-engineer, backend-engineer, api-architect]
---

# Authentication Flows

## Auth.js (NextAuth) Setup

### Step 1: Install Dependencies
```bash
npm install next-auth @auth/prisma-adapter
```

### Step 2: Configure Auth Options
```typescript
// lib/auth.ts
import { NextAuthOptions } from "next-auth";
import { PrismaAdapter } from "@auth/prisma-adapter";
import GoogleProvider from "next-auth/providers/google";
import CredentialsProvider from "next-auth/providers/credentials";
import { prisma } from "@/lib/prisma";

export const authOptions: NextAuthOptions = {
  adapter: PrismaAdapter(prisma),
  session: { strategy: "jwt" },
  pages: {
    signIn: "/login",
    error: "/auth/error",
  },
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID!,
      clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    }),
    CredentialsProvider({
      name: "credentials",
      credentials: {
        email: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        if (!credentials?.email || !credentials?.password) return null;
        const user = await prisma.user.findUnique({
          where: { email: credentials.email },
        });
        if (!user || !user.hashedPassword) return null;
        const isValid = await bcrypt.compare(credentials.password, user.hashedPassword);
        if (!isValid) return null;
        return { id: user.id, email: user.email, name: user.name };
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        token.id = user.id;
        token.role = user.role;
      }
      return token;
    },
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.id as string;
        session.user.role = token.role as string;
      }
      return session;
    },
  },
};
```

### Step 3: Create API Route
```typescript
// app/api/auth/[...nextauth]/route.ts
import NextAuth from "next-auth";
import { authOptions } from "@/lib/auth";

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };
```

## Protected Route Patterns

### Server Component Protection
```typescript
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { redirect } from "next/navigation";

export default async function ProtectedPage() {
  const session = await getServerSession(authOptions);
  if (!session) redirect("/login");
  return <div>Welcome {session.user.name}</div>;
}
```

### API Route Protection
```typescript
import { getServerSession } from "next-auth";
import { authOptions } from "@/lib/auth";
import { NextResponse } from "next/server";

export async function GET() {
  const session = await getServerSession(authOptions);
  if (!session) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }
  // Protected logic here
}
```

### Middleware Protection
```typescript
// middleware.ts
import { withAuth } from "next-auth/middleware";

export default withAuth({
  pages: { signIn: "/login" },
});

export const config = {
  matcher: ["/dashboard/:path*", "/api/protected/:path*"],
};
```

## JWT Pattern (Manual)

```typescript
import { SignJWT, jwtVerify } from "jose";

const secret = new TextEncoder().encode(process.env.JWT_SECRET);

export async function signToken(payload: object) {
  return new SignJWT(payload)
    .setProtectedHeader({ alg: "HS256" })
    .setIssuedAt()
    .setExpirationTime("7d")
    .sign(secret);
}

export async function verifyToken(token: string) {
  try {
    const { payload } = await jwtVerify(token, secret);
    return payload;
  } catch {
    return null;
  }
}
```

## Role-Based Access Control

```typescript
type Role = "user" | "admin" | "superadmin";

const permissions: Record<Role, string[]> = {
  user: ["read:own", "write:own"],
  admin: ["read:all", "write:all", "delete:own"],
  superadmin: ["read:all", "write:all", "delete:all", "manage:users"],
};

function hasPermission(role: Role, permission: string): boolean {
  return permissions[role]?.includes(permission) ?? false;
}
```

## Decision Criteria

| Method | Use When |
|--------|----------|
| Session (DB) | High security, need revocation |
| JWT | Stateless, microservices |
| OAuth only | Social login, no passwords |
| Credentials | Email/password required |

## Common Pitfalls

1. **Storing JWT in localStorage**: XSS vulnerability
2. **No token refresh**: Poor UX with short expiry
3. **Missing CSRF protection**: Session fixation attacks
4. **Exposing user IDs**: Use session-based lookups
5. **No rate limiting on login**: Brute force vulnerability
6. **Plain text password comparison**: Always use bcrypt/argon2
7. **Missing secure cookie flags**: httpOnly, secure, sameSite
