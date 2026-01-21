---
skill: testing-strategies
version: "1.0.0"
description: "Comprehensive testing approaches including unit, integration, and E2E testing methodologies"
used-by: ["@qa-controller", "@test-engineer", "@frontend-controller", "@backend-controller"]
---

# Testing Strategies

## Overview

This skill defines systematic testing approaches across the testing pyramid: unit tests at the base, integration tests in the middle, and E2E tests at the top.

---

## Step-by-Step Procedures

### 1. Unit Testing Setup

#### Framework Selection
- **React/Next.js**: Vitest + React Testing Library
- **Node.js/API**: Vitest or Jest
- **TypeScript**: ts-jest or vitest with TypeScript support

#### Configuration (vitest.config.ts)
```typescript
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./tests/setup.ts'],
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/', 'tests/'],
      thresholds: {
        statements: 80,
        branches: 80,
        functions: 80,
        lines: 80
      }
    }
  }
})
```

#### Unit Test Structure
```typescript
describe('ComponentName', () => {
  beforeEach(() => {
    // Setup
  })

  it('should render correctly with default props', () => {
    // Arrange
    const props = { title: 'Test' }

    // Act
    render(<Component {...props} />)

    // Assert
    expect(screen.getByText('Test')).toBeInTheDocument()
  })

  it('should handle user interactions', async () => {
    // Test user events
  })
})
```

### 2. Integration Testing

#### API Integration Tests
```typescript
import { createServer } from '../server'
import supertest from 'supertest'

describe('API Integration', () => {
  let app: Express
  let request: supertest.SuperTest<supertest.Test>

  beforeAll(async () => {
    app = await createServer()
    request = supertest(app)
  })

  it('POST /api/users creates user and returns 201', async () => {
    const response = await request
      .post('/api/users')
      .send({ email: 'test@example.com', name: 'Test User' })
      .expect(201)

    expect(response.body).toHaveProperty('id')
    expect(response.body.email).toBe('test@example.com')
  })
})
```

#### Database Integration
```typescript
import { PrismaClient } from '@prisma/client'
import { beforeEach, afterAll } from 'vitest'

const prisma = new PrismaClient()

beforeEach(async () => {
  // Clean database before each test
  await prisma.$executeRaw`TRUNCATE TABLE users CASCADE`
})

afterAll(async () => {
  await prisma.$disconnect()
})
```

### 3. E2E Testing with Playwright

#### Configuration (playwright.config.ts)
```typescript
import { defineConfig, devices } from '@playwright/test'

export default defineConfig({
  testDir: './e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure'
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'firefox', use: { ...devices['Desktop Firefox'] } },
    { name: 'webkit', use: { ...devices['Desktop Safari'] } },
    { name: 'mobile', use: { ...devices['iPhone 13'] } }
  ],
  webServer: {
    command: 'npm run dev',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI
  }
})
```

#### E2E Test Structure
```typescript
import { test, expect } from '@playwright/test'

test.describe('User Authentication Flow', () => {
  test('user can sign up and login', async ({ page }) => {
    await page.goto('/signup')
    await page.fill('[data-testid="email"]', 'new@example.com')
    await page.fill('[data-testid="password"]', 'SecurePass123!')
    await page.click('[data-testid="submit"]')

    await expect(page).toHaveURL('/dashboard')
    await expect(page.locator('h1')).toContainText('Welcome')
  })
})
```

---

## Decision Criteria

| Test Type | When to Use | Coverage Target |
|-----------|-------------|-----------------|
| Unit | Pure functions, components, utilities | 80%+ |
| Integration | API endpoints, database operations | Critical paths |
| E2E | User journeys, critical flows | Happy paths + edge cases |

### Testing Priority Matrix
1. **Critical**: Authentication, payments, data mutations
2. **High**: Core features, navigation, forms
3. **Medium**: UI components, non-critical features
4. **Low**: Static content, pure UI

---

## Common Pitfalls to Avoid

1. **Testing implementation details** - Test behavior, not internals
2. **Flaky E2E tests** - Use proper wait strategies, not arbitrary delays
3. **No test isolation** - Each test must be independent
4. **Over-mocking** - Mock external services only, not your own code
5. **Missing edge cases** - Test error states, empty states, boundaries
6. **Slow test suites** - Parallelize, use targeted test runs
7. **No CI integration** - Tests must run on every PR

---

## Validation Checklist

- [ ] Unit tests cover all utility functions
- [ ] Components have render and interaction tests
- [ ] API endpoints have integration tests
- [ ] Critical user flows have E2E coverage
- [ ] Tests run in CI on every PR
- [ ] Coverage thresholds are enforced
- [ ] Test data is properly isolated
- [ ] Flaky tests are identified and fixed
