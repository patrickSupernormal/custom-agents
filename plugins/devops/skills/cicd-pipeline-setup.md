---
skill: cicd-pipeline-setup
version: "1.0.0"
description: "Setup and configure CI/CD pipelines using GitHub Actions and Vercel deployment workflows"
used-by: ["@devops-controller", "@deployment-engineer", "@infrastructure-specialist"]
---

# CI/CD Pipeline Setup

## Overview

This skill covers the complete setup of continuous integration and deployment pipelines, focusing on GitHub Actions for CI and Vercel for deployment.

---

## Step-by-Step Procedures

### 1. GitHub Actions Workflow Setup

#### Initial Configuration
1. Create `.github/workflows/` directory in repository root
2. Define workflow files based on project needs:
   - `ci.yml` - Continuous integration (lint, test, build)
   - `deploy-preview.yml` - Preview deployments for PRs
   - `deploy-production.yml` - Production deployments

#### Standard CI Workflow Template
```yaml
name: CI
on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run lint

  test:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run test:ci

  build:
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-artifact@v4
        with:
          name: build
          path: .next/
```

### 2. Vercel Deployment Configuration

#### Project Setup
1. Install Vercel CLI: `npm i -g vercel`
2. Link project: `vercel link`
3. Configure `vercel.json` in project root

#### Vercel Configuration Template
```json
{
  "buildCommand": "npm run build",
  "outputDirectory": ".next",
  "framework": "nextjs",
  "regions": ["iad1"],
  "env": {
    "NODE_ENV": "production"
  },
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" }
      ]
    }
  ]
}
```

### 3. Environment Variable Management

#### GitHub Secrets Setup
1. Navigate to Repository → Settings → Secrets
2. Add required secrets:
   - `VERCEL_TOKEN` - Vercel API token
   - `VERCEL_ORG_ID` - Organization ID
   - `VERCEL_PROJECT_ID` - Project ID
   - Application-specific secrets (API keys, etc.)

#### Environment Separation
- `production` - Main branch deployments
- `preview` - PR preview deployments
- `development` - Local development

---

## Decision Criteria

| Scenario | Recommendation |
|----------|----------------|
| Simple static site | Vercel auto-deploy only |
| Complex build with tests | Full GitHub Actions + Vercel |
| Monorepo | Turborepo + selective builds |
| Multiple environments | Branch-based deployment rules |

---

## Common Pitfalls to Avoid

1. **Missing cache configuration** - Always cache node_modules and .next
2. **Incorrect secret scoping** - Use environment-specific secrets
3. **No build artifact preservation** - Upload artifacts for debugging
4. **Ignoring preview deploys** - Enable for every PR
5. **Hardcoded environment values** - Use GitHub Secrets exclusively
6. **No timeout limits** - Set job timeouts to prevent runaway builds
7. **Missing status checks** - Require CI to pass before merge

---

## Validation Checklist

- [ ] Workflows trigger on correct branches
- [ ] All secrets are configured in GitHub
- [ ] Build artifacts are preserved
- [ ] Preview deployments work for PRs
- [ ] Production deploys only from main
- [ ] Environment variables are correctly scoped
- [ ] Cache is properly configured
- [ ] Status checks are required for merges
