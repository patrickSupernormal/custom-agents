---
skill: scraping-strategies
version: "1.0.0"
description: "Comprehensive web scraping strategies including tool selection, content extraction, and best practices"
used-by: ["@site-scraper"]
---

# Scraping Strategies

## Purpose
Provide systematic approaches to web content extraction, covering tool selection, extraction patterns, dynamic content handling, and ethical considerations for reliable and responsible scraping.

---

## 1. Scraping Tool Selection

### Decision Matrix

| Scenario | Recommended Tool | Reason |
|----------|------------------|--------|
| Static HTML pages | `fetch` / `axios` | Fast, low overhead |
| Server-rendered content | `fetch` with headers | No JS needed |
| JavaScript-rendered SPAs | Playwright | Full browser engine |
| Complex interactions | Playwright | Click, scroll, type support |
| High-volume scraping | `fetch` + queue | Better rate control |
| Sites with anti-bot | Playwright + stealth | Browser fingerprint |
| PDF/document extraction | Specialized libraries | `pdf-parse`, `mammoth` |

### Tool Comparison

#### fetch / axios (Lightweight HTTP)
```javascript
// Best for: Static pages, APIs, server-rendered content
const response = await fetch('https://example.com/page', {
  headers: {
    'User-Agent': 'Mozilla/5.0 (compatible; CustomBot/1.0)',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'en-US,en;q=0.9'
  }
});
const html = await response.text();

// Pros: Fast, low memory, easy to parallelize
// Cons: No JS execution, no interaction
```

#### Playwright (Full Browser)
```javascript
// Best for: SPAs, dynamic content, interactions
import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
  viewport: { width: 1920, height: 1080 }
});
const page = await context.newPage();
await page.goto('https://example.com', { waitUntil: 'networkidle' });

// Pros: Full JS support, interactions, screenshots
// Cons: Slower, higher resource usage
```

#### Puppeteer (Chrome-specific)
```javascript
// Best for: Chrome-specific features, PDF generation
import puppeteer from 'puppeteer';

const browser = await puppeteer.launch({
  headless: 'new',
  args: ['--no-sandbox', '--disable-setuid-sandbox']
});
const page = await browser.newPage();
await page.goto('https://example.com');

// Similar to Playwright but Chrome-only
```

### When to Upgrade Tools

```
Start with fetch
    |
    v
[Page loads correctly?] --No--> Try Playwright
    |
   Yes
    |
    v
[Content visible in HTML?] --No--> Check for:
    |                               - AJAX calls (use fetch on API)
   Yes                              - JS rendering (use Playwright)
    |
    v
Extract with cheerio/DOM parser
```

---

## 2. Content Extraction Patterns

### HTML Parsing with Cheerio
```javascript
import * as cheerio from 'cheerio';

const $ = cheerio.load(html);

// Extract structured data
const articles = $('article').map((i, el) => ({
  title: $(el).find('h2').text().trim(),
  link: $(el).find('a').attr('href'),
  summary: $(el).find('.summary').text().trim(),
  date: $(el).find('time').attr('datetime'),
  author: $(el).find('.author').text().trim(),
  tags: $(el).find('.tag').map((i, t) => $(t).text()).get()
})).get();
```

### Playwright DOM Extraction
```javascript
// Extract using page.evaluate for complex structures
const data = await page.evaluate(() => {
  const items = document.querySelectorAll('.product-card');
  return Array.from(items).map(item => ({
    name: item.querySelector('.product-name')?.textContent?.trim(),
    price: item.querySelector('.price')?.textContent?.trim(),
    image: item.querySelector('img')?.src,
    rating: item.querySelector('.rating')?.getAttribute('data-rating'),
    reviews: item.querySelector('.review-count')?.textContent?.trim()
  }));
});
```

### Extraction Schema Template
```javascript
const extractionSchema = {
  // Page metadata
  meta: {
    title: 'title',
    description: 'meta[name="description"]@content',
    canonical: 'link[rel="canonical"]@href',
    ogImage: 'meta[property="og:image"]@content'
  },

  // Main content
  content: {
    headline: 'h1',
    subheadline: '.subtitle, .tagline',
    body: 'article, .content, main',
    publishDate: 'time@datetime, .date',
    author: '.author, [rel="author"]'
  },

  // Navigation structure
  navigation: {
    mainNav: 'nav a@href',
    breadcrumbs: '.breadcrumb a',
    footer: 'footer a@href'
  },

  // Media assets
  media: {
    images: 'img@src',
    videos: 'video source@src, iframe[src*="youtube"]@src',
    documents: 'a[href$=".pdf"]@href'
  }
};
```

---

## 3. Selector Strategies

### CSS Selectors (Preferred)
```javascript
// Element selectors
$('h1')                           // Tag name
$('.product-title')               // Class
$('#main-content')                // ID
$('[data-testid="price"]')        // Attribute

// Combinators
$('div.card > h2')                // Direct child
$('article p')                    // Descendant
$('h2 + p')                       // Adjacent sibling
$('h2 ~ p')                       // General sibling

// Pseudo-selectors
$('li:first-child')               // First element
$('li:nth-child(2)')              // Second element
$('li:last-child')                // Last element
$('p:contains("Price")')          // Contains text (cheerio)

// Attribute selectors
$('a[href^="https://"]')          // Starts with
$('a[href$=".pdf"]')              // Ends with
$('img[src*="product"]')          // Contains
$('input[type="email"]')          // Exact match
```

### XPath Selectors (Complex Cases)
```javascript
// Playwright XPath
const elements = await page.locator('xpath=//div[@class="product"]').all();

// Common XPath patterns
'//h1'                            // All h1 elements
'//div[@class="price"]'           // Div with exact class
'//div[contains(@class, "card")]' // Class contains
'//a[text()="Read More"]'         // Exact text match
'//a[contains(text(), "More")]'   // Text contains
'//table//tr[position()>1]'       // Skip header row
'//*[@data-price]/@data-price'    // Attribute value
'//div[@id="content"]//p[1]'      // First p in content div
'//preceding-sibling::h2'         // Previous sibling
'//following-sibling::p'          // Next sibling

// XPath functions
'//span[normalize-space()="Price"]'     // Trim whitespace
'//div[starts-with(@id, "product-")]'   // ID prefix
'//a[not(contains(@class, "hidden"))]'  // Negation
```

### Selector Robustness Ranking

| Priority | Selector Type | Example | Robustness |
|----------|--------------|---------|------------|
| 1 | Data attributes | `[data-testid="price"]` | Highest |
| 2 | Semantic HTML | `article`, `nav`, `main` | High |
| 3 | ARIA labels | `[aria-label="Add to cart"]` | High |
| 4 | ID (meaningful) | `#product-gallery` | Medium |
| 5 | Class (semantic) | `.product-price` | Medium |
| 6 | Class (utility) | `.text-lg.font-bold` | Low |
| 7 | Structure-based | `div > div > span` | Lowest |

### Building Resilient Selectors
```javascript
// Bad: Fragile structural selector
const price = $('div.container > div:nth-child(2) > span').text();

// Good: Multiple fallback selectors
const priceSelectors = [
  '[data-testid="product-price"]',
  '[itemprop="price"]',
  '.product-price',
  '.price-value',
  '#price'
];

function extractWithFallbacks($, selectors) {
  for (const selector of selectors) {
    const element = $(selector);
    if (element.length) {
      return element.text().trim();
    }
  }
  return null;
}

const price = extractWithFallbacks($, priceSelectors);
```

---

## 4. Handling Dynamic Content (SPAs)

### Wait Strategies
```javascript
// Wait for specific element
await page.waitForSelector('.product-list', { timeout: 10000 });

// Wait for network idle
await page.goto(url, { waitUntil: 'networkidle' });

// Wait for specific network request
await page.waitForResponse(
  response => response.url().includes('/api/products')
);

// Wait for function condition
await page.waitForFunction(() => {
  return document.querySelectorAll('.product').length > 0;
});

// Custom wait with retry
async function waitForContent(page, selector, maxWait = 30000) {
  const startTime = Date.now();
  while (Date.now() - startTime < maxWait) {
    const count = await page.locator(selector).count();
    if (count > 0) return true;
    await page.waitForTimeout(500);
  }
  throw new Error(`Timeout waiting for ${selector}`);
}
```

### Infinite Scroll Handling
```javascript
async function scrapeInfiniteScroll(page, itemSelector, maxItems = 100) {
  const items = new Set();
  let previousHeight = 0;
  let noNewContentCount = 0;

  while (items.size < maxItems && noNewContentCount < 3) {
    // Extract current items
    const currentItems = await page.evaluate((selector) => {
      return Array.from(document.querySelectorAll(selector))
        .map(el => el.outerHTML);
    }, itemSelector);

    const previousSize = items.size;
    currentItems.forEach(item => items.add(item));

    // Check if new content loaded
    if (items.size === previousSize) {
      noNewContentCount++;
    } else {
      noNewContentCount = 0;
    }

    // Scroll to bottom
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(2000);

    // Check for "Load More" button
    const loadMoreButton = await page.$('button:has-text("Load More")');
    if (loadMoreButton) {
      await loadMoreButton.click();
      await page.waitForTimeout(2000);
    }
  }

  return Array.from(items);
}
```

### Handling Lazy-Loaded Images
```javascript
async function loadLazyImages(page) {
  // Scroll through page to trigger lazy loading
  await page.evaluate(async () => {
    const distance = 300;
    const delay = 100;

    while (document.scrollingElement.scrollTop + window.innerHeight
           < document.scrollingElement.scrollHeight) {
      document.scrollingElement.scrollBy(0, distance);
      await new Promise(resolve => setTimeout(resolve, delay));
    }

    // Scroll back to top
    document.scrollingElement.scrollTop = 0;
  });

  // Wait for images to load
  await page.waitForFunction(() => {
    const images = document.querySelectorAll('img[data-src], img[loading="lazy"]');
    return Array.from(images).every(img => img.complete);
  });
}

// Extract actual image sources
const images = await page.evaluate(() => {
  return Array.from(document.querySelectorAll('img')).map(img => ({
    src: img.src || img.dataset.src,
    alt: img.alt,
    width: img.naturalWidth,
    height: img.naturalHeight
  }));
});
```

### SPA Route Navigation
```javascript
async function scrapeSpARoutes(page, routes) {
  const results = {};

  for (const route of routes) {
    // Use client-side navigation when possible
    await page.evaluate((path) => {
      window.history.pushState({}, '', path);
      window.dispatchEvent(new PopStateEvent('popstate'));
    }, route);

    // Or navigate directly
    await page.goto(`https://example.com${route}`, {
      waitUntil: 'networkidle'
    });

    // Wait for route-specific content
    await page.waitForSelector('[data-page-loaded="true"]', { timeout: 10000 });

    results[route] = await extractPageData(page);
  }

  return results;
}
```

---

## 5. Rate Limiting and Politeness

### Request Throttling
```javascript
class RateLimiter {
  constructor(requestsPerSecond = 1) {
    this.minDelay = 1000 / requestsPerSecond;
    this.lastRequest = 0;
  }

  async wait() {
    const now = Date.now();
    const elapsed = now - this.lastRequest;
    if (elapsed < this.minDelay) {
      await new Promise(resolve =>
        setTimeout(resolve, this.minDelay - elapsed)
      );
    }
    this.lastRequest = Date.now();
  }
}

// Usage
const limiter = new RateLimiter(2); // 2 requests per second

async function scrapeWithRateLimit(urls) {
  const results = [];
  for (const url of urls) {
    await limiter.wait();
    const data = await scrapePage(url);
    results.push(data);
  }
  return results;
}
```

### Respectful Crawling Patterns
```javascript
const scrapingConfig = {
  // Timing
  requestDelay: 2000,           // ms between requests
  randomDelay: [1000, 3000],    // Random range for human-like behavior
  maxConcurrent: 2,             // Parallel requests limit

  // Respect robots.txt
  respectRobotsTxt: true,

  // Headers
  headers: {
    'User-Agent': 'CustomBot/1.0 (+https://yoursite.com/bot-info)',
    'Accept': 'text/html',
    'Accept-Language': 'en-US,en;q=0.9'
  },

  // Backoff on errors
  retryDelays: [1000, 5000, 30000, 60000],

  // Honor server hints
  respectCrawlDelay: true,
  respectRetryAfter: true
};

// Add random delay for human-like behavior
async function humanDelay(min = 1000, max = 3000) {
  const delay = Math.floor(Math.random() * (max - min + 1)) + min;
  await new Promise(resolve => setTimeout(resolve, delay));
}
```

### Robots.txt Parsing
```javascript
import robotsParser from 'robots-parser';

async function checkRobotsTxt(url) {
  const robotsUrl = new URL('/robots.txt', url).href;
  const response = await fetch(robotsUrl);
  const robotsTxt = await response.text();

  const robots = robotsParser(robotsUrl, robotsTxt);

  return {
    isAllowed: robots.isAllowed(url, 'CustomBot'),
    crawlDelay: robots.getCrawlDelay('CustomBot'),
    sitemaps: robots.getSitemaps()
  };
}

// Respect crawl-delay
async function scrapeWithRobotsTxt(baseUrl, paths) {
  const robotsInfo = await checkRobotsTxt(baseUrl);
  const delay = (robotsInfo.crawlDelay || 1) * 1000;

  for (const path of paths) {
    const url = new URL(path, baseUrl).href;

    if (!robotsInfo.isAllowed) {
      console.log(`Skipping disallowed: ${url}`);
      continue;
    }

    await scrapePage(url);
    await new Promise(resolve => setTimeout(resolve, delay));
  }
}
```

---

## 6. Authentication Handling

### Session-Based Authentication
```javascript
async function scrapeWithSession(page, loginUrl, credentials) {
  // Navigate to login page
  await page.goto(loginUrl);

  // Fill login form
  await page.fill('input[name="email"]', credentials.email);
  await page.fill('input[name="password"]', credentials.password);

  // Submit and wait for navigation
  await Promise.all([
    page.waitForNavigation({ waitUntil: 'networkidle' }),
    page.click('button[type="submit"]')
  ]);

  // Verify login success
  const isLoggedIn = await page.locator('.user-menu').isVisible();
  if (!isLoggedIn) {
    throw new Error('Login failed');
  }

  // Session cookies are now stored in context
  // Continue scraping authenticated pages
  return page;
}

// Save and reuse session
async function saveSession(context, path) {
  const cookies = await context.cookies();
  const storage = await context.storageState();
  await fs.writeFile(path, JSON.stringify({ cookies, storage }));
}

async function loadSession(browser, path) {
  const { storage } = JSON.parse(await fs.readFile(path));
  return browser.newContext({ storageState: storage });
}
```

### API Token Authentication
```javascript
async function scrapeWithToken(apiUrl, token) {
  const response = await fetch(apiUrl, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  });

  if (response.status === 401) {
    // Token expired, refresh
    const newToken = await refreshToken();
    return scrapeWithToken(apiUrl, newToken);
  }

  return response.json();
}

// OAuth flow for API access
async function getOAuthToken(page, oauthConfig) {
  const { authUrl, clientId, redirectUri, scope } = oauthConfig;

  const authUrlFull = `${authUrl}?client_id=${clientId}&redirect_uri=${redirectUri}&scope=${scope}&response_type=code`;

  await page.goto(authUrlFull);

  // Handle OAuth consent
  await page.click('button:has-text("Allow")');

  // Capture redirect with code
  const redirectedUrl = page.url();
  const code = new URL(redirectedUrl).searchParams.get('code');

  // Exchange code for token
  const tokenResponse = await fetch(oauthConfig.tokenUrl, {
    method: 'POST',
    body: new URLSearchParams({
      code,
      client_id: clientId,
      client_secret: oauthConfig.clientSecret,
      redirect_uri: redirectUri,
      grant_type: 'authorization_code'
    })
  });

  return tokenResponse.json();
}
```

### Cookie Management
```javascript
async function manageCookies(context) {
  // Get all cookies
  const cookies = await context.cookies();

  // Set specific cookies
  await context.addCookies([
    {
      name: 'session_id',
      value: 'abc123',
      domain: '.example.com',
      path: '/',
      httpOnly: true,
      secure: true,
      sameSite: 'Lax'
    }
  ]);

  // Clear specific cookies
  await context.clearCookies({ name: 'tracking_cookie' });

  // Export cookies for later use
  return cookies.filter(c => !c.name.includes('tracking'));
}
```

---

## 7. Data Structuring from Scraped Content

### Normalization Utilities
```javascript
const normalizers = {
  // Price normalization
  price(text) {
    if (!text) return null;
    const cleaned = text.replace(/[^0-9.,]/g, '');
    const normalized = cleaned.replace(',', '.');
    return parseFloat(normalized) || null;
  },

  // Date normalization
  date(text) {
    if (!text) return null;
    const parsed = new Date(text);
    return isNaN(parsed) ? null : parsed.toISOString();
  },

  // Text cleaning
  text(text) {
    if (!text) return null;
    return text
      .replace(/\s+/g, ' ')
      .replace(/[\n\r\t]/g, ' ')
      .trim();
  },

  // URL normalization
  url(url, baseUrl) {
    if (!url) return null;
    try {
      return new URL(url, baseUrl).href;
    } catch {
      return null;
    }
  },

  // Array from comma-separated
  tags(text) {
    if (!text) return [];
    return text.split(',').map(t => t.trim()).filter(Boolean);
  }
};
```

### Schema Validation
```javascript
import Joi from 'joi';

const productSchema = Joi.object({
  name: Joi.string().required().min(1).max(500),
  price: Joi.number().positive().allow(null),
  currency: Joi.string().length(3).default('USD'),
  description: Joi.string().max(10000).allow(null),
  images: Joi.array().items(Joi.string().uri()),
  url: Joi.string().uri().required(),
  sku: Joi.string().allow(null),
  inStock: Joi.boolean().default(true),
  rating: Joi.number().min(0).max(5).allow(null),
  reviewCount: Joi.number().integer().min(0).default(0),
  categories: Joi.array().items(Joi.string()),
  scrapedAt: Joi.date().iso().default(Date.now)
});

function validateAndClean(data) {
  const { error, value } = productSchema.validate(data, {
    stripUnknown: true,
    abortEarly: false
  });

  if (error) {
    console.warn('Validation errors:', error.details);
  }

  return value;
}
```

### Output Formats
```javascript
// JSON output
function toJSON(data, pretty = true) {
  return JSON.stringify(data, null, pretty ? 2 : 0);
}

// CSV output
function toCSV(data, columns) {
  const header = columns.join(',');
  const rows = data.map(item =>
    columns.map(col => {
      const value = item[col];
      if (value === null || value === undefined) return '';
      if (typeof value === 'string' && (value.includes(',') || value.includes('"'))) {
        return `"${value.replace(/"/g, '""')}"`;
      }
      return value;
    }).join(',')
  );
  return [header, ...rows].join('\n');
}

// Structured extraction report
function generateReport(results) {
  return {
    metadata: {
      scrapedAt: new Date().toISOString(),
      totalPages: results.pages.length,
      successCount: results.pages.filter(p => p.success).length,
      errorCount: results.pages.filter(p => !p.success).length,
      duration: results.duration
    },
    summary: {
      contentTypes: countBy(results.pages, 'contentType'),
      avgLoadTime: average(results.pages.map(p => p.loadTime)),
      totalItems: sum(results.pages.map(p => p.items?.length || 0))
    },
    pages: results.pages,
    errors: results.pages.filter(p => p.error).map(p => ({
      url: p.url,
      error: p.error
    }))
  };
}
```

---

## 8. Error Handling and Retries

### Retry Logic with Exponential Backoff
```javascript
async function scrapeWithRetry(url, options = {}) {
  const {
    maxRetries = 3,
    baseDelay = 1000,
    maxDelay = 30000,
    retryableErrors = [408, 429, 500, 502, 503, 504]
  } = options;

  let lastError;

  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      const response = await fetch(url, options.fetchOptions);

      if (!response.ok) {
        if (retryableErrors.includes(response.status)) {
          throw new RetryableError(`HTTP ${response.status}`, response.status);
        }
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.text();

    } catch (error) {
      lastError = error;

      if (attempt < maxRetries && isRetryable(error)) {
        const delay = Math.min(baseDelay * Math.pow(2, attempt), maxDelay);

        // Check for Retry-After header
        if (error.retryAfter) {
          await sleep(error.retryAfter * 1000);
        } else {
          // Add jitter to prevent thundering herd
          const jitter = Math.random() * 1000;
          await sleep(delay + jitter);
        }

        console.log(`Retry ${attempt + 1}/${maxRetries} for ${url}`);
        continue;
      }

      throw error;
    }
  }

  throw lastError;
}

function isRetryable(error) {
  return error instanceof RetryableError ||
         error.code === 'ECONNRESET' ||
         error.code === 'ETIMEDOUT' ||
         error.code === 'ENOTFOUND';
}
```

### Comprehensive Error Handling
```javascript
class ScrapingError extends Error {
  constructor(message, url, type, details = {}) {
    super(message);
    this.name = 'ScrapingError';
    this.url = url;
    this.type = type;
    this.details = details;
    this.timestamp = new Date().toISOString();
  }
}

async function safeScrape(page, url, extractors) {
  const result = {
    url,
    success: false,
    data: null,
    errors: [],
    warnings: [],
    timing: {}
  };

  const startTime = Date.now();

  try {
    // Navigation with timeout
    result.timing.navigationStart = Date.now();
    await page.goto(url, {
      timeout: 30000,
      waitUntil: 'domcontentloaded'
    });
    result.timing.navigationEnd = Date.now();

    // Check for error pages
    const title = await page.title();
    if (title.match(/404|not found|error/i)) {
      throw new ScrapingError('Page not found', url, 'NOT_FOUND');
    }

    // Check for blocks/captchas
    const isBlocked = await page.locator('[class*="captcha"], [id*="captcha"]').count();
    if (isBlocked > 0) {
      throw new ScrapingError('Blocked by captcha', url, 'BLOCKED');
    }

    // Run extractors with individual error handling
    result.data = {};
    for (const [key, extractor] of Object.entries(extractors)) {
      try {
        result.data[key] = await extractor(page);
      } catch (extractError) {
        result.warnings.push({
          field: key,
          error: extractError.message
        });
        result.data[key] = null;
      }
    }

    result.success = true;

  } catch (error) {
    result.errors.push({
      type: error.type || 'UNKNOWN',
      message: error.message,
      stack: error.stack
    });

    // Capture screenshot for debugging
    try {
      const screenshot = await page.screenshot({ fullPage: true });
      result.debugScreenshot = screenshot.toString('base64');
    } catch {}

  } finally {
    result.timing.total = Date.now() - startTime;
  }

  return result;
}
```

### Circuit Breaker Pattern
```javascript
class CircuitBreaker {
  constructor(options = {}) {
    this.failureThreshold = options.failureThreshold || 5;
    this.resetTimeout = options.resetTimeout || 60000;
    this.state = 'CLOSED';
    this.failures = 0;
    this.lastFailure = null;
  }

  async execute(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() - this.lastFailure > this.resetTimeout) {
        this.state = 'HALF_OPEN';
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }

    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (error) {
      this.onFailure();
      throw error;
    }
  }

  onSuccess() {
    this.failures = 0;
    this.state = 'CLOSED';
  }

  onFailure() {
    this.failures++;
    this.lastFailure = Date.now();

    if (this.failures >= this.failureThreshold) {
      this.state = 'OPEN';
    }
  }
}

// Usage per domain
const breakers = new Map();

function getBreakerForDomain(url) {
  const domain = new URL(url).hostname;
  if (!breakers.has(domain)) {
    breakers.set(domain, new CircuitBreaker());
  }
  return breakers.get(domain);
}
```

---

## 9. Legal and Ethical Considerations

### Compliance Checklist

| Consideration | Check | Action |
|---------------|-------|--------|
| Terms of Service | Read site ToS | Verify scraping is permitted |
| robots.txt | Parse and respect | Skip disallowed paths |
| Rate limiting | Implement delays | Minimum 1 request/second |
| Data protection | Check regulations | GDPR, CCPA compliance |
| Copyright | Assess content type | Fair use evaluation |
| Authentication bypass | Never circumvent | Only scrape public data |
| Personal data | Minimize collection | Anonymize if necessary |

### Ethical Scraping Principles
```javascript
const ethicalScrapingConfig = {
  // Always identify your bot
  userAgent: 'YourCompanyBot/1.0 (+https://yourcompany.com/bot; contact@yourcompany.com)',

  // Provide opt-out mechanism
  robotsTxtCompliance: true,

  // Rate limit to prevent server impact
  requestsPerSecond: 1,
  maxConcurrent: 2,

  // Respect server capacity
  backoffOnError: true,
  respectRetryAfter: true,

  // Only collect necessary data
  dataMinimization: true,

  // Don't store sensitive information
  excludePatterns: [
    /password/i,
    /credit.?card/i,
    /ssn/i,
    /social.?security/i
  ],

  // Provide contact for complaints
  contactEmail: 'scraping@yourcompany.com'
};
```

### Data Handling Best Practices
```javascript
// Anonymize personal data
function anonymizeData(data) {
  return {
    ...data,
    email: data.email ? hashEmail(data.email) : null,
    phone: data.phone ? maskPhone(data.phone) : null,
    name: data.name ? 'User' : null,
    ip: null // Never store
  };
}

// Retention policy
const dataRetention = {
  rawHtml: '7 days',      // Delete raw captures quickly
  extractedData: '90 days', // Keep processed data longer
  aggregatedStats: 'indefinite' // Anonymous aggregates OK
};

// Data deletion on request
async function handleDeletionRequest(identifier) {
  await database.delete('scraped_data', { source_url: identifier });
  await cache.invalidate(`scrape:${identifier}`);
  console.log(`Deleted data for: ${identifier}`);
}
```

---

## 10. Common Scraping Patterns by Site Type

### E-commerce Product Pages
```javascript
const ecommerceExtractor = {
  async extract(page) {
    return {
      product: {
        name: await page.textContent('[itemprop="name"], .product-title, h1'),
        price: await extractPrice(page),
        currency: await page.getAttribute('[itemprop="priceCurrency"]', 'content'),
        sku: await page.getAttribute('[itemprop="sku"]', 'content'),
        description: await page.textContent('[itemprop="description"], .product-description'),
        images: await page.$$eval('.product-images img', imgs =>
          imgs.map(img => img.src || img.dataset.src)
        ),
        rating: await page.textContent('[itemprop="ratingValue"]'),
        reviewCount: await page.textContent('[itemprop="reviewCount"]'),
        availability: await page.textContent('[itemprop="availability"]'),
        brand: await page.textContent('[itemprop="brand"]'),
        categories: await page.$$eval('.breadcrumb a', links =>
          links.map(a => a.textContent.trim())
        )
      },
      variants: await extractVariants(page),
      relatedProducts: await extractRelatedProducts(page)
    };
  }
};
```

### News/Article Pages
```javascript
const articleExtractor = {
  async extract(page) {
    return {
      article: {
        headline: await page.textContent('h1, [itemprop="headline"]'),
        subheadline: await page.textContent('.subtitle, .dek, [itemprop="alternativeHeadline"]'),
        author: await page.textContent('[rel="author"], .author-name, [itemprop="author"]'),
        publishDate: await page.getAttribute('time, [itemprop="datePublished"]', 'datetime'),
        modifiedDate: await page.getAttribute('[itemprop="dateModified"]', 'datetime'),
        body: await page.innerHTML('article, .article-body, [itemprop="articleBody"]'),
        summary: await page.textContent('.summary, .excerpt, [itemprop="description"]'),
        images: await extractArticleImages(page),
        tags: await page.$$eval('.tags a, [rel="tag"]', tags =>
          tags.map(t => t.textContent.trim())
        ),
        section: await page.textContent('[itemprop="articleSection"]'),
        wordCount: await countWords(page)
      },
      metadata: {
        ogImage: await page.getAttribute('meta[property="og:image"]', 'content'),
        twitterCard: await page.getAttribute('meta[name="twitter:card"]', 'content'),
        canonical: await page.getAttribute('link[rel="canonical"]', 'href')
      }
    };
  }
};
```

### Directory/Listing Pages
```javascript
const listingExtractor = {
  async extractAll(page, paginationSelector = '.pagination a') {
    const allItems = [];
    let currentPage = 1;

    while (true) {
      // Extract items from current page
      const items = await page.$$eval('.listing-item', cards =>
        cards.map(card => ({
          title: card.querySelector('.title')?.textContent?.trim(),
          url: card.querySelector('a')?.href,
          description: card.querySelector('.description')?.textContent?.trim(),
          location: card.querySelector('.location')?.textContent?.trim(),
          price: card.querySelector('.price')?.textContent?.trim(),
          image: card.querySelector('img')?.src,
          rating: card.querySelector('.rating')?.textContent?.trim(),
          metadata: Object.fromEntries(
            Array.from(card.querySelectorAll('[data-field]'))
              .map(el => [el.dataset.field, el.textContent.trim()])
          )
        }))
      );

      allItems.push(...items);

      // Check for next page
      const nextButton = await page.$(`${paginationSelector}:has-text("Next")`);
      if (!nextButton) break;

      await nextButton.click();
      await page.waitForLoadState('networkidle');
      currentPage++;

      // Safety limit
      if (currentPage > 100) break;
    }

    return allItems;
  }
};
```

### Social Media Profiles
```javascript
const socialProfileExtractor = {
  async extract(page, platform) {
    const extractors = {
      twitter: {
        username: '@[data-testid="UserName"]',
        displayName: '[data-testid="UserName"] span:first-child',
        bio: '[data-testid="UserDescription"]',
        location: '[data-testid="UserLocation"]',
        website: '[data-testid="UserUrl"] a',
        joinDate: '[data-testid="UserJoinDate"]',
        followers: '[href$="/followers"] span',
        following: '[href$="/following"] span'
      },
      linkedin: {
        name: '.text-heading-xlarge',
        headline: '.text-body-medium',
        location: '.text-body-small:has(.t-black--light)',
        connections: '.t-bold:has-text("connections")',
        about: '#about ~ .display-flex .full-width'
      }
    };

    const selectors = extractors[platform];
    if (!selectors) throw new Error(`Unknown platform: ${platform}`);

    const profile = {};
    for (const [field, selector] of Object.entries(selectors)) {
      try {
        profile[field] = await page.textContent(selector);
      } catch {
        profile[field] = null;
      }
    }

    return profile;
  }
};
```

### API Response Scraping
```javascript
const apiScraper = {
  async interceptAndExtract(page, apiPattern) {
    const apiResponses = [];

    // Set up request interception
    await page.route(apiPattern, async route => {
      const response = await route.fetch();
      const json = await response.json();
      apiResponses.push({
        url: route.request().url(),
        method: route.request().method(),
        data: json,
        timestamp: Date.now()
      });
      await route.fulfill({ response });
    });

    // Navigate and trigger API calls
    await page.goto(url);
    await page.waitForLoadState('networkidle');

    return apiResponses;
  },

  // Direct API scraping when endpoints are known
  async scrapeApi(endpoint, params = {}) {
    const url = new URL(endpoint);
    Object.entries(params).forEach(([k, v]) => url.searchParams.set(k, v));

    const response = await fetch(url, {
      headers: {
        'Accept': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      }
    });

    return response.json();
  }
};
```

---

## Quality Checklist

Before completing any scraping task:

- [ ] Tool selection matches site complexity
- [ ] Selectors use robust patterns (data attributes > structure)
- [ ] Dynamic content properly waited for
- [ ] Rate limiting implemented
- [ ] robots.txt respected
- [ ] Error handling covers all failure modes
- [ ] Retries use exponential backoff
- [ ] Data validated against schema
- [ ] Personal data handled appropriately
- [ ] Output format matches requirements
- [ ] Logging captures debugging information
