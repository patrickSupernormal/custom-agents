---
skill: security-audit-checklist
version: "1.0.0"
description: "Comprehensive security audit procedures covering OWASP Top 10 and automated security scanning"
used-by: ["@security-auditor", "@devops-controller", "@qa-controller"]
---

# Security Audit Checklist

## Overview

This skill provides a systematic approach to security auditing, covering OWASP Top 10 vulnerabilities, automated scanning tools, and security best practices for web applications.

---

## Step-by-Step Procedures

### 1. Dependency Security Audit

#### NPM Audit
```bash
# Run security audit
npm audit

# Auto-fix where possible
npm audit fix

# Force fix (may include breaking changes)
npm audit fix --force

# Generate detailed report
npm audit --json > audit-report.json
```

#### GitHub Dependabot Configuration
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10
    labels:
      - "dependencies"
      - "security"
    commit-message:
      prefix: "chore(deps):"
```

### 2. OWASP Top 10 Checklist

#### A01: Broken Access Control
```typescript
// Verify authorization on every request
export async function authorizeRequest(
  req: Request,
  requiredRole: Role
): Promise<boolean> {
  const session = await getSession(req)

  if (!session?.user) {
    throw new UnauthorizedError('Authentication required')
  }

  if (!hasRole(session.user, requiredRole)) {
    throw new ForbiddenError('Insufficient permissions')
  }

  return true
}

// Always verify resource ownership
export async function getResource(id: string, userId: string) {
  const resource = await db.resource.findUnique({ where: { id } })

  if (resource?.ownerId !== userId) {
    throw new ForbiddenError('Access denied')
  }

  return resource
}
```

#### A02: Cryptographic Failures
```typescript
// Use strong hashing for passwords
import { hash, verify } from '@node-rs/argon2'

async function hashPassword(password: string): Promise<string> {
  return hash(password, {
    memoryCost: 65536,
    timeCost: 3,
    parallelism: 4
  })
}

// Never store sensitive data unencrypted
// Use environment variables for secrets
const apiKey = process.env.API_KEY // Not in code
```

#### A03: Injection Prevention
```typescript
// Use parameterized queries (Prisma does this automatically)
const user = await prisma.user.findUnique({
  where: { email: userInput } // Safe - parameterized
})

// Sanitize HTML output
import DOMPurify from 'isomorphic-dompurify'

function sanitizeHTML(dirty: string): string {
  return DOMPurify.sanitize(dirty, {
    ALLOWED_TAGS: ['b', 'i', 'em', 'strong', 'a'],
    ALLOWED_ATTR: ['href']
  })
}
```

#### A04: Insecure Design
- [ ] Implement rate limiting on all endpoints
- [ ] Use CAPTCHA for public forms
- [ ] Implement account lockout after failed attempts
- [ ] Design for least privilege

#### A05: Security Misconfiguration
```typescript
// next.config.js security headers
const securityHeaders = [
  { key: 'X-DNS-Prefetch-Control', value: 'on' },
  { key: 'Strict-Transport-Security', value: 'max-age=63072000; includeSubDomains' },
  { key: 'X-Frame-Options', value: 'SAMEORIGIN' },
  { key: 'X-Content-Type-Options', value: 'nosniff' },
  { key: 'Referrer-Policy', value: 'strict-origin-when-cross-origin' },
  { key: 'Permissions-Policy', value: 'camera=(), microphone=(), geolocation=()' },
  {
    key: 'Content-Security-Policy',
    value: `
      default-src 'self';
      script-src 'self' 'unsafe-eval' 'unsafe-inline';
      style-src 'self' 'unsafe-inline';
      img-src 'self' blob: data:;
      font-src 'self';
      connect-src 'self' https://api.example.com;
    `.replace(/\s+/g, ' ').trim()
  }
]
```

#### A06: Vulnerable Components
```bash
# Check for known vulnerabilities
npx snyk test

# Continuous monitoring
npx snyk monitor
```

#### A07: Authentication Failures
```typescript
// Implement secure session management
import { getIronSession } from 'iron-session'

const sessionOptions = {
  password: process.env.SESSION_SECRET!,
  cookieName: 'session',
  cookieOptions: {
    secure: process.env.NODE_ENV === 'production',
    httpOnly: true,
    sameSite: 'lax' as const,
    maxAge: 60 * 60 * 24 * 7 // 1 week
  }
}
```

#### A08: Software and Data Integrity
```typescript
// Verify webhook signatures
import crypto from 'crypto'

function verifyWebhookSignature(
  payload: string,
  signature: string,
  secret: string
): boolean {
  const expected = crypto
    .createHmac('sha256', secret)
    .update(payload)
    .digest('hex')

  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expected)
  )
}
```

#### A09: Logging and Monitoring
```typescript
// Security event logging
const securityLogger = pino({
  level: 'info',
  redact: ['password', 'token', 'authorization']
})

function logSecurityEvent(event: SecurityEvent) {
  securityLogger.info({
    type: event.type,
    userId: event.userId,
    ip: event.ip,
    userAgent: event.userAgent,
    timestamp: new Date().toISOString()
  })
}
```

#### A10: Server-Side Request Forgery (SSRF)
```typescript
// Validate and sanitize URLs
function isAllowedUrl(url: string): boolean {
  const allowedHosts = ['api.trusted.com', 'cdn.trusted.com']

  try {
    const parsed = new URL(url)
    return allowedHosts.includes(parsed.host)
  } catch {
    return false
  }
}
```

### 3. Automated Security Scanning

#### GitHub CodeQL Setup
```yaml
# .github/workflows/codeql.yml
name: CodeQL Analysis
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 0'

jobs:
  analyze:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: javascript-typescript
      - uses: github/codeql-action/analyze@v3
```

---

## Decision Criteria

| Finding Severity | Action Required | Timeline |
|------------------|-----------------|----------|
| Critical | Immediate fix, consider rollback | < 24 hours |
| High | Priority fix | < 1 week |
| Medium | Scheduled fix | < 1 month |
| Low | Track for future | Next quarter |

---

## Common Pitfalls to Avoid

1. **Secrets in code** - Use environment variables exclusively
2. **Missing rate limiting** - All public endpoints need limits
3. **Overly permissive CORS** - Never use `*` in production
4. **Console logging secrets** - Redact sensitive data in logs
5. **Direct SQL queries** - Always use parameterized queries
6. **Trusting client input** - Validate everything server-side
7. **Ignoring audit warnings** - Address all high/critical findings

---

## Validation Checklist

- [ ] npm audit shows no high/critical vulnerabilities
- [ ] All OWASP Top 10 items addressed
- [ ] Security headers configured
- [ ] Rate limiting implemented
- [ ] Input validation on all endpoints
- [ ] Authentication/authorization verified
- [ ] Secrets properly managed
- [ ] Logging excludes sensitive data
- [ ] CodeQL or similar scanning enabled
- [ ] Dependency updates automated
