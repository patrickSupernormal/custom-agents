---
skill: astro-islands-patterns
version: "1.0.0"
description: "Comprehensive patterns for Astro development including islands architecture, content collections, routing, and performance optimization"
used-by:
  - "@astro-developer"
  - "@frontend-controller"
  - "@performance-engineer"
---

# Astro Islands Patterns

## Overview

This skill covers production-ready patterns for building high-performance content sites with Astro, leveraging islands architecture for selective hydration, content collections for type-safe content management, and hybrid rendering for optimal performance.

## 1. Project Structure and Conventions

### Standard Astro Project Layout

```
src/
├── components/           # Reusable UI components
│   ├── astro/           # Pure Astro components (zero JS)
│   │   ├── Header.astro
│   │   ├── Footer.astro
│   │   └── Card.astro
│   ├── react/           # React islands (interactive)
│   │   ├── SearchDialog.tsx
│   │   └── ThemeToggle.tsx
│   └── ui/              # Shared UI primitives
│       ├── Button.astro
│       └── Badge.astro
├── content/             # Content collections
│   ├── blog/
│   │   ├── first-post.mdx
│   │   └── second-post.md
│   ├── docs/
│   │   └── getting-started.mdx
│   └── config.ts        # Collection schemas
├── layouts/             # Page layouts
│   ├── BaseLayout.astro
│   ├── BlogLayout.astro
│   └── DocsLayout.astro
├── pages/               # File-based routing
│   ├── index.astro
│   ├── about.astro
│   ├── blog/
│   │   ├── index.astro
│   │   └── [...slug].astro
│   └── api/
│       └── search.ts
├── styles/              # Global styles
│   └── global.css
└── lib/                 # Utilities
    ├── utils.ts
    └── constants.ts
public/                  # Static assets
├── fonts/
├── images/
└── favicon.svg
astro.config.mjs         # Astro configuration
```

### Configuration File (astro.config.mjs)

```typescript
import { defineConfig } from 'astro/config';
import tailwind from '@astrojs/tailwind';
import react from '@astrojs/react';
import mdx from '@astrojs/mdx';
import sitemap from '@astrojs/sitemap';
import vercel from '@astrojs/vercel';

export default defineConfig({
  site: 'https://example.com',
  output: 'hybrid', // 'static' | 'server' | 'hybrid'
  adapter: vercel(),

  integrations: [
    tailwind({
      applyBaseStyles: false,
    }),
    react(),
    mdx({
      syntaxHighlight: 'shiki',
      shikiConfig: {
        theme: 'github-dark',
      },
    }),
    sitemap(),
  ],

  vite: {
    ssr: {
      noExternal: ['@radix-ui/*'],
    },
  },

  image: {
    service: {
      entrypoint: 'astro/assets/services/sharp',
    },
    domains: ['cdn.example.com'],
  },

  markdown: {
    remarkPlugins: [],
    rehypePlugins: [],
  },
});
```

### TypeScript Configuration (tsconfig.json)

```json
{
  "extends": "astro/tsconfigs/strict",
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@layouts/*": ["src/layouts/*"],
      "@lib/*": ["src/lib/*"]
    }
  }
}
```

## 2. Islands Architecture (Client Directives)

### Client Directive Overview

| Directive | When to Use | JavaScript Loaded |
|-----------|-------------|-------------------|
| `client:load` | Critical interactivity needed immediately | On page load |
| `client:idle` | Lower priority, can wait for idle | On requestIdleCallback |
| `client:visible` | Below fold, only when scrolled into view | On IntersectionObserver |
| `client:media` | Only on certain screen sizes | On media query match |
| `client:only` | Client-only, no SSR | On page load, no SSR |

### client:load - Immediate Hydration

```astro
---
// For critical above-the-fold interactive elements
import SearchDialog from '@components/react/SearchDialog';
import MobileMenu from '@components/react/MobileMenu';
---

<!-- Navigation search - users expect immediate response -->
<SearchDialog client:load />

<!-- Mobile menu - critical for mobile users -->
<MobileMenu client:load />
```

### client:idle - Deferred Hydration

```astro
---
// For interactive elements that can wait
import NewsletterForm from '@components/react/NewsletterForm';
import FeedbackWidget from '@components/react/FeedbackWidget';
---

<!-- Newsletter form in footer - not immediately critical -->
<NewsletterForm client:idle />

<!-- Feedback widget - can wait for browser idle -->
<FeedbackWidget client:idle />
```

### client:visible - Lazy Hydration

```astro
---
// For below-fold content
import CommentSection from '@components/react/CommentSection';
import RelatedProducts from '@components/react/RelatedProducts';
import VideoPlayer from '@components/react/VideoPlayer';
---

<!-- Only hydrate when scrolled into view -->
<section class="mt-32">
  <CommentSection client:visible postId={post.id} />
</section>

<!-- Product carousel below fold -->
<RelatedProducts client:visible categoryId={category.id} />

<!-- Video player with custom root margin -->
<VideoPlayer
  client:visible={{
    rootMargin: '200px' // Start loading 200px before visible
  }}
  videoId={video.id}
/>
```

### client:media - Responsive Hydration

```astro
---
import MobileFilters from '@components/react/MobileFilters';
import DesktopFilters from '@components/react/DesktopFilters';
---

<!-- Only hydrate on mobile devices -->
<MobileFilters client:media="(max-width: 768px)" />

<!-- Only hydrate on desktop -->
<DesktopFilters client:media="(min-width: 769px)" />
```

### client:only - Skip SSR Entirely

```astro
---
// For components that cannot render on server
import ThreeScene from '@components/react/ThreeScene';
import MapComponent from '@components/react/MapComponent';
---

<!-- WebGL/Three.js - requires browser APIs -->
<ThreeScene client:only="react" />

<!-- Map with geolocation - browser-only APIs -->
<MapComponent client:only="react" />

<!-- Note: Must specify framework: "react" | "vue" | "svelte" | "solid" -->
```

### Mixed Framework Islands

```astro
---
// Combine different frameworks on same page
import ReactCounter from '@components/react/Counter';
import VueCounter from '@components/vue/Counter.vue';
import SvelteCounter from '@components/svelte/Counter.svelte';
---

<div class="counters">
  <!-- Each island hydrates independently -->
  <ReactCounter client:visible initialCount={0} />
  <VueCounter client:visible :initial-count="0" />
  <SvelteCounter client:visible initialCount={0} />
</div>
```

### Island Communication Pattern

```typescript
// src/lib/store.ts - Shared state with nanostores
import { atom, map } from 'nanostores';

// Simple atom for single values
export const isMenuOpen = atom(false);

// Map for complex state
export const cartItems = map<Record<string, CartItem>>({});

// Actions
export function addToCart(item: CartItem) {
  cartItems.setKey(item.id, item);
}

export function removeFromCart(id: string) {
  const items = cartItems.get();
  delete items[id];
  cartItems.set({ ...items });
}
```

```tsx
// src/components/react/CartButton.tsx
import { useStore } from '@nanostores/react';
import { cartItems, isMenuOpen } from '@lib/store';

export function CartButton() {
  const $cartItems = useStore(cartItems);
  const itemCount = Object.keys($cartItems).length;

  return (
    <button onClick={() => isMenuOpen.set(true)}>
      Cart ({itemCount})
    </button>
  );
}
```

```astro
---
import CartButton from '@components/react/CartButton';
import CartDrawer from '@components/react/CartDrawer';
---

<!-- Both components share state via nanostores -->
<CartButton client:load />
<CartDrawer client:idle />
```

## 3. Content Collections

### Collection Schema Definition

```typescript
// src/content/config.ts
import { defineCollection, z, reference } from 'astro:content';

// Blog collection with full metadata
const blogCollection = defineCollection({
  type: 'content',
  schema: ({ image }) => z.object({
    title: z.string().max(100),
    description: z.string().max(200),
    publishDate: z.coerce.date(),
    updatedDate: z.coerce.date().optional(),
    author: reference('authors'), // Reference another collection
    category: z.enum(['tutorial', 'guide', 'news', 'opinion']),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().default(false),

    // Image with automatic optimization
    coverImage: image().refine((img) => img.width >= 1200, {
      message: 'Cover image must be at least 1200px wide',
    }),
    coverImageAlt: z.string(),

    // SEO overrides
    seo: z.object({
      title: z.string().optional(),
      description: z.string().optional(),
      canonical: z.string().url().optional(),
    }).optional(),
  }),
});

// Authors collection (data only, no content)
const authorsCollection = defineCollection({
  type: 'data',
  schema: ({ image }) => z.object({
    name: z.string(),
    email: z.string().email(),
    bio: z.string(),
    avatar: image(),
    social: z.object({
      twitter: z.string().url().optional(),
      github: z.string().url().optional(),
      linkedin: z.string().url().optional(),
    }).optional(),
  }),
});

// Documentation collection with sidebar ordering
const docsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    sidebar: z.object({
      order: z.number(),
      label: z.string().optional(),
      badge: z.enum(['new', 'updated', 'deprecated']).optional(),
    }),
    prev: z.string().optional(),
    next: z.string().optional(),
  }),
});

// Products collection (e-commerce)
const productsCollection = defineCollection({
  type: 'data',
  schema: ({ image }) => z.object({
    name: z.string(),
    sku: z.string(),
    price: z.number().positive(),
    salePrice: z.number().positive().optional(),
    description: z.string(),
    images: z.array(image()),
    category: z.string(),
    variants: z.array(z.object({
      name: z.string(),
      options: z.array(z.string()),
    })).optional(),
    inStock: z.boolean().default(true),
    featured: z.boolean().default(false),
  }),
});

export const collections = {
  blog: blogCollection,
  authors: authorsCollection,
  docs: docsCollection,
  products: productsCollection,
};
```

### Querying Collections

```astro
---
// src/pages/blog/index.astro
import { getCollection, getEntry } from 'astro:content';
import BlogLayout from '@layouts/BlogLayout.astro';
import BlogCard from '@components/astro/BlogCard.astro';

// Get all published posts, sorted by date
const posts = await getCollection('blog', ({ data }) => {
  return import.meta.env.PROD ? !data.draft : true;
});

const sortedPosts = posts.sort(
  (a, b) => b.data.publishDate.valueOf() - a.data.publishDate.valueOf()
);

// Get posts by category
const tutorials = await getCollection('blog', ({ data }) => {
  return data.category === 'tutorial' && !data.draft;
});

// Get posts by tag
const typescriptPosts = await getCollection('blog', ({ data }) => {
  return data.tags.includes('typescript');
});

// Get featured products
const featuredProducts = await getCollection('products', ({ data }) => {
  return data.featured && data.inStock;
});
---

<BlogLayout title="Blog">
  <section class="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
    {sortedPosts.map((post) => (
      <BlogCard post={post} />
    ))}
  </section>
</BlogLayout>
```

### Rendering Collection Entries

```astro
---
// src/pages/blog/[...slug].astro
import { getCollection, getEntry, type CollectionEntry } from 'astro:content';
import BlogLayout from '@layouts/BlogLayout.astro';
import TableOfContents from '@components/astro/TableOfContents.astro';
import AuthorCard from '@components/astro/AuthorCard.astro';

export async function getStaticPaths() {
  const posts = await getCollection('blog');
  return posts.map((post) => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

type Props = {
  post: CollectionEntry<'blog'>;
};

const { post } = Astro.props;

// Resolve author reference
const author = await getEntry(post.data.author);

// Render content with components and headings
const { Content, headings } = await post.render();

// Get related posts by category
const relatedPosts = await getCollection('blog', ({ data, slug }) => {
  return data.category === post.data.category &&
         slug !== post.slug &&
         !data.draft;
});
---

<BlogLayout
  title={post.data.seo?.title || post.data.title}
  description={post.data.seo?.description || post.data.description}
  image={post.data.coverImage}
>
  <article class="prose prose-lg mx-auto">
    <header>
      <h1>{post.data.title}</h1>
      <div class="flex items-center gap-4">
        <AuthorCard author={author} />
        <time datetime={post.data.publishDate.toISOString()}>
          {post.data.publishDate.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
          })}
        </time>
      </div>
    </header>

    {headings.length > 0 && (
      <aside class="toc">
        <TableOfContents headings={headings} />
      </aside>
    )}

    <Content />
  </article>

  {relatedPosts.length > 0 && (
    <section class="mt-16">
      <h2>Related Posts</h2>
      <div class="grid gap-4 md:grid-cols-3">
        {relatedPosts.slice(0, 3).map((related) => (
          <a href={`/blog/${related.slug}`}>{related.data.title}</a>
        ))}
      </div>
    </section>
  )}
</BlogLayout>
```

### MDX Components

```typescript
// src/content/blog/advanced-post.mdx
---
title: "Building with Astro"
description: "Learn advanced Astro patterns"
publishDate: 2024-01-15
author: john-doe
category: tutorial
tags: ['astro', 'typescript']
coverImage: ./images/astro-cover.png
coverImageAlt: "Astro logo with code"
---

import Callout from '@components/mdx/Callout.astro';
import CodeBlock from '@components/mdx/CodeBlock.astro';
import VideoEmbed from '@components/react/VideoEmbed';

# Getting Started

<Callout type="info">
  This guide assumes familiarity with JavaScript and basic web concepts.
</Callout>

Here's a code example:

<CodeBlock lang="typescript" filename="example.ts">
{`const greeting = "Hello, Astro!";
console.log(greeting);`}
</CodeBlock>

## Video Tutorial

<VideoEmbed client:visible videoId="abc123" />
```

```astro
// src/components/mdx/Callout.astro
---
interface Props {
  type?: 'info' | 'warning' | 'error' | 'success';
}

const { type = 'info' } = Astro.props;

const styles = {
  info: 'bg-blue-50 border-blue-500 text-blue-900',
  warning: 'bg-yellow-50 border-yellow-500 text-yellow-900',
  error: 'bg-red-50 border-red-500 text-red-900',
  success: 'bg-green-50 border-green-500 text-green-900',
};

const icons = {
  info: 'i',
  warning: '!',
  error: 'x',
  success: '✓',
};
---

<aside class={`border-l-4 p-4 my-6 rounded-r ${styles[type]}`} role="note">
  <div class="flex items-start gap-3">
    <span class="font-bold">{icons[type]}</span>
    <div class="prose-sm">
      <slot />
    </div>
  </div>
</aside>
```

## 4. Component Patterns

### Props and TypeScript

```astro
---
// src/components/astro/Button.astro
interface Props {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost';
  size?: 'sm' | 'md' | 'lg';
  href?: string;
  disabled?: boolean;
  class?: string;
  'aria-label'?: string;
}

const {
  variant = 'primary',
  size = 'md',
  href,
  disabled = false,
  class: className,
  'aria-label': ariaLabel,
  ...rest
} = Astro.props;

const Tag = href ? 'a' : 'button';

const baseStyles = 'inline-flex items-center justify-center font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50';

const variantStyles = {
  primary: 'bg-blue-600 text-white hover:bg-blue-700 focus-visible:ring-blue-500',
  secondary: 'bg-gray-100 text-gray-900 hover:bg-gray-200 focus-visible:ring-gray-500',
  outline: 'border border-gray-300 bg-transparent hover:bg-gray-100 focus-visible:ring-gray-500',
  ghost: 'bg-transparent hover:bg-gray-100 focus-visible:ring-gray-500',
};

const sizeStyles = {
  sm: 'h-8 px-3 text-sm rounded',
  md: 'h-10 px-4 text-base rounded-md',
  lg: 'h-12 px-6 text-lg rounded-lg',
};
---

<Tag
  href={href}
  disabled={disabled}
  aria-label={ariaLabel}
  class:list={[baseStyles, variantStyles[variant], sizeStyles[size], className]}
  {...rest}
>
  <slot />
</Tag>
```

### Slots and Composition

```astro
---
// src/components/astro/Card.astro
interface Props {
  class?: string;
}

const { class: className } = Astro.props;

// Check which slots are provided
const hasHeader = Astro.slots.has('header');
const hasFooter = Astro.slots.has('footer');
const hasMedia = Astro.slots.has('media');
---

<article class:list={['bg-white rounded-lg shadow-md overflow-hidden', className]}>
  {hasMedia && (
    <div class="aspect-video relative">
      <slot name="media" />
    </div>
  )}

  {hasHeader && (
    <header class="px-6 pt-6">
      <slot name="header" />
    </header>
  )}

  <div class="px-6 py-4">
    <slot />
  </div>

  {hasFooter && (
    <footer class="px-6 pb-6 pt-2 border-t border-gray-100">
      <slot name="footer" />
    </footer>
  )}
</article>
```

```astro
---
// Usage example
import Card from '@components/astro/Card.astro';
import Button from '@components/astro/Button.astro';
import { Image } from 'astro:assets';
import productImage from '@assets/product.jpg';
---

<Card>
  <Image
    slot="media"
    src={productImage}
    alt="Product"
    class="object-cover w-full h-full"
  />

  <Fragment slot="header">
    <h3 class="text-xl font-semibold">Product Name</h3>
    <p class="text-gray-500">$99.00</p>
  </Fragment>

  <p>Product description goes here.</p>

  <div slot="footer" class="flex gap-2">
    <Button variant="primary">Add to Cart</Button>
    <Button variant="outline">View Details</Button>
  </div>
</Card>
```

### Compound Component Pattern

```astro
---
// src/components/astro/Tabs/Tabs.astro
interface Props {
  defaultValue: string;
}

const { defaultValue } = Astro.props;
const id = `tabs-${Math.random().toString(36).slice(2)}`;
---

<div data-tabs data-default-value={defaultValue} id={id}>
  <slot />
</div>

<script>
  class TabGroup {
    container: HTMLElement;
    tabs: HTMLElement[];
    panels: HTMLElement[];
    activeValue: string;

    constructor(container: HTMLElement) {
      this.container = container;
      this.tabs = [...container.querySelectorAll('[data-tab-trigger]')] as HTMLElement[];
      this.panels = [...container.querySelectorAll('[data-tab-content]')] as HTMLElement[];
      this.activeValue = container.dataset.defaultValue || '';

      this.init();
    }

    init() {
      this.tabs.forEach(tab => {
        tab.addEventListener('click', () => this.activate(tab.dataset.value!));
      });
      this.activate(this.activeValue);
    }

    activate(value: string) {
      this.activeValue = value;

      this.tabs.forEach(tab => {
        const isActive = tab.dataset.value === value;
        tab.setAttribute('aria-selected', String(isActive));
        tab.setAttribute('tabindex', isActive ? '0' : '-1');
      });

      this.panels.forEach(panel => {
        const isActive = panel.dataset.value === value;
        panel.hidden = !isActive;
      });
    }
  }

  document.querySelectorAll('[data-tabs]').forEach(container => {
    new TabGroup(container as HTMLElement);
  });
</script>
```

```astro
---
// src/components/astro/Tabs/TabList.astro
interface Props {
  'aria-label': string;
}

const { 'aria-label': ariaLabel } = Astro.props;
---

<div role="tablist" aria-label={ariaLabel} class="flex border-b">
  <slot />
</div>
```

```astro
---
// src/components/astro/Tabs/Tab.astro
interface Props {
  value: string;
}

const { value } = Astro.props;
---

<button
  role="tab"
  data-tab-trigger
  data-value={value}
  aria-selected="false"
  class="px-4 py-2 text-sm font-medium border-b-2 border-transparent hover:border-gray-300 aria-selected:border-blue-500 aria-selected:text-blue-600"
>
  <slot />
</button>
```

```astro
---
// src/components/astro/Tabs/TabPanel.astro
interface Props {
  value: string;
}

const { value } = Astro.props;
---

<div
  role="tabpanel"
  data-tab-content
  data-value={value}
  hidden
  class="py-4"
>
  <slot />
</div>
```

### Higher-Order Component Pattern

```astro
---
// src/components/astro/WithAuth.astro
// Wrapper component for protected content
interface Props {
  fallback?: string;
}

const { fallback = '/login' } = Astro.props;

// Check auth in middleware or here
const session = Astro.locals.session;
const isAuthenticated = !!session?.user;

if (!isAuthenticated) {
  return Astro.redirect(fallback);
}
---

<slot user={session.user} />
```

```astro
---
// Usage
import WithAuth from '@components/astro/WithAuth.astro';
---

<WithAuth>
  {(props) => (
    <div>
      <h1>Welcome, {props.user.name}</h1>
      <p>This is protected content.</p>
    </div>
  )}
</WithAuth>
```

## 5. Data Fetching

### Build-Time Data Fetching

```astro
---
// src/pages/products/index.astro
// Data fetched at build time, cached in static HTML

// Simple fetch
const response = await fetch('https://api.example.com/products');
const products = await response.json();

// With error handling
async function fetchProducts() {
  try {
    const res = await fetch('https://api.example.com/products', {
      headers: {
        'Authorization': `Bearer ${import.meta.env.API_KEY}`,
      },
    });

    if (!res.ok) {
      throw new Error(`HTTP ${res.status}`);
    }

    return await res.json();
  } catch (error) {
    console.error('Failed to fetch products:', error);
    return [];
  }
}

const products = await fetchProducts();

// Parallel fetching for better performance
const [productsRes, categoriesRes, featuredRes] = await Promise.all([
  fetch('https://api.example.com/products'),
  fetch('https://api.example.com/categories'),
  fetch('https://api.example.com/featured'),
]);

const [products, categories, featured] = await Promise.all([
  productsRes.json(),
  categoriesRes.json(),
  featuredRes.json(),
]);
---

<Layout title="Products">
  {products.length === 0 ? (
    <p>No products available.</p>
  ) : (
    <ul>
      {products.map((product) => (
        <li>{product.name} - ${product.price}</li>
      ))}
    </ul>
  )}
</Layout>
```

### Server-Side Data Fetching (SSR)

```astro
---
// src/pages/dashboard.astro
// Enable SSR for this page
export const prerender = false;

import { getSession } from '@lib/auth';

const session = await getSession(Astro.cookies);

if (!session) {
  return Astro.redirect('/login');
}

// Fetch user-specific data on each request
const userData = await fetch(`https://api.example.com/users/${session.userId}`, {
  headers: {
    'Authorization': `Bearer ${session.token}`,
  },
}).then(r => r.json());

// Cache for short period with custom headers
Astro.response.headers.set('Cache-Control', 'private, max-age=60');
---

<Layout title="Dashboard">
  <h1>Welcome back, {userData.name}</h1>
</Layout>
```

### API Routes

```typescript
// src/pages/api/search.ts
import type { APIRoute } from 'astro';

export const GET: APIRoute = async ({ request, url }) => {
  const query = url.searchParams.get('q');

  if (!query || query.length < 2) {
    return new Response(JSON.stringify({ error: 'Query too short' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  try {
    const results = await searchDatabase(query);

    return new Response(JSON.stringify({ results }), {
      status: 200,
      headers: {
        'Content-Type': 'application/json',
        'Cache-Control': 'public, max-age=300',
      },
    });
  } catch (error) {
    return new Response(JSON.stringify({ error: 'Search failed' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    });
  }
};

export const POST: APIRoute = async ({ request }) => {
  const body = await request.json();

  // Validate input
  if (!body.email || !body.message) {
    return new Response(JSON.stringify({ error: 'Missing fields' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  // Process submission
  await saveContact(body);

  return new Response(JSON.stringify({ success: true }), {
    status: 201,
    headers: { 'Content-Type': 'application/json' },
  });
};
```

### Data Loading in React Islands

```tsx
// src/components/react/ProductSearch.tsx
import { useState, useTransition } from 'react';

interface Product {
  id: string;
  name: string;
  price: number;
}

interface Props {
  initialProducts: Product[];
}

export function ProductSearch({ initialProducts }: Props) {
  const [products, setProducts] = useState(initialProducts);
  const [query, setQuery] = useState('');
  const [isPending, startTransition] = useTransition();

  const handleSearch = async (searchQuery: string) => {
    setQuery(searchQuery);

    if (searchQuery.length < 2) {
      setProducts(initialProducts);
      return;
    }

    startTransition(async () => {
      const response = await fetch(`/api/search?q=${encodeURIComponent(searchQuery)}`);
      const data = await response.json();
      setProducts(data.results);
    });
  };

  return (
    <div>
      <input
        type="search"
        value={query}
        onChange={(e) => handleSearch(e.target.value)}
        placeholder="Search products..."
        className="w-full px-4 py-2 border rounded"
      />

      {isPending && <div className="text-sm text-gray-500">Searching...</div>}

      <ul className="mt-4 space-y-2">
        {products.map((product) => (
          <li key={product.id}>
            {product.name} - ${product.price}
          </li>
        ))}
      </ul>
    </div>
  );
}
```

```astro
---
// Usage - pass initial data from Astro
import { ProductSearch } from '@components/react/ProductSearch';

const initialProducts = await fetch('https://api.example.com/products')
  .then(r => r.json());
---

<ProductSearch client:load initialProducts={initialProducts} />
```

## 6. Routing

### Dynamic Routes

```astro
---
// src/pages/blog/[slug].astro
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('blog');

  return posts.map((post) => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content } = await post.render();
---

<article>
  <h1>{post.data.title}</h1>
  <Content />
</article>
```

### Catch-All Routes

```astro
---
// src/pages/docs/[...path].astro
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const docs = await getCollection('docs');

  return docs.map((doc) => ({
    // doc.slug might be "getting-started" or "api/reference/methods"
    params: { path: doc.slug },
    props: { doc },
  }));
}

const { doc } = Astro.props;
---

<DocsLayout>
  <h1>{doc.data.title}</h1>
</DocsLayout>
```

### Nested Dynamic Routes

```astro
---
// src/pages/[category]/[product].astro
import { getCollection } from 'astro:content';

export async function getStaticPaths() {
  const products = await getCollection('products');

  return products.map((product) => ({
    params: {
      category: product.data.category.toLowerCase(),
      product: product.id,
    },
    props: { product },
  }));
}

const { product } = Astro.props;
// URL: /electronics/iphone-15
---

<ProductLayout>
  <h1>{product.data.name}</h1>
</ProductLayout>
```

### Pagination

```astro
---
// src/pages/blog/page/[page].astro
import { getCollection } from 'astro:content';
import type { GetStaticPaths, Page } from 'astro';
import Pagination from '@components/astro/Pagination.astro';

export const getStaticPaths = (async ({ paginate }) => {
  const posts = await getCollection('blog', ({ data }) => !data.draft);
  const sortedPosts = posts.sort(
    (a, b) => b.data.publishDate.valueOf() - a.data.publishDate.valueOf()
  );

  return paginate(sortedPosts, { pageSize: 10 });
}) satisfies GetStaticPaths;

interface Props {
  page: Page;
}

const { page } = Astro.props;
---

<Layout title={`Blog - Page ${page.currentPage}`}>
  <ul>
    {page.data.map((post) => (
      <li>
        <a href={`/blog/${post.slug}`}>{post.data.title}</a>
      </li>
    ))}
  </ul>

  <Pagination
    currentPage={page.currentPage}
    totalPages={page.lastPage}
    prevUrl={page.url.prev}
    nextUrl={page.url.next}
  />
</Layout>
```

```astro
---
// src/components/astro/Pagination.astro
interface Props {
  currentPage: number;
  totalPages: number;
  prevUrl?: string;
  nextUrl?: string;
}

const { currentPage, totalPages, prevUrl, nextUrl } = Astro.props;
---

<nav aria-label="Pagination" class="flex items-center justify-between">
  {prevUrl ? (
    <a href={prevUrl} class="px-4 py-2 border rounded hover:bg-gray-100">
      Previous
    </a>
  ) : (
    <span class="px-4 py-2 border rounded opacity-50 cursor-not-allowed">
      Previous
    </span>
  )}

  <span class="text-sm text-gray-600">
    Page {currentPage} of {totalPages}
  </span>

  {nextUrl ? (
    <a href={nextUrl} class="px-4 py-2 border rounded hover:bg-gray-100">
      Next
    </a>
  ) : (
    <span class="px-4 py-2 border rounded opacity-50 cursor-not-allowed">
      Next
    </span>
  )}
</nav>
```

### Server Endpoints for Dynamic API

```typescript
// src/pages/api/posts/[id].ts
import type { APIRoute } from 'astro';
import { getEntry } from 'astro:content';

export const prerender = false;

export const GET: APIRoute = async ({ params }) => {
  const post = await getEntry('blog', params.id!);

  if (!post) {
    return new Response(JSON.stringify({ error: 'Post not found' }), {
      status: 404,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  return new Response(JSON.stringify(post.data), {
    status: 200,
    headers: { 'Content-Type': 'application/json' },
  });
};

export const DELETE: APIRoute = async ({ params, locals }) => {
  // Check authentication
  if (!locals.user?.isAdmin) {
    return new Response(JSON.stringify({ error: 'Unauthorized' }), {
      status: 403,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  await deletePost(params.id!);

  return new Response(null, { status: 204 });
};
```

## 7. View Transitions

### Basic Setup

```astro
---
// src/layouts/BaseLayout.astro
import { ViewTransitions } from 'astro:transitions';
---

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{title}</title>
    <ViewTransitions />
  </head>
  <body>
    <slot />
  </body>
</html>
```

### Named Transitions

```astro
---
// src/pages/blog/index.astro - List page
import { Image } from 'astro:assets';
---

{posts.map((post) => (
  <article>
    <Image
      src={post.data.coverImage}
      alt={post.data.coverImageAlt}
      transition:name={`post-image-${post.slug}`}
      class="aspect-video object-cover"
    />
    <h2 transition:name={`post-title-${post.slug}`}>
      <a href={`/blog/${post.slug}`}>{post.data.title}</a>
    </h2>
  </article>
))}
```

```astro
---
// src/pages/blog/[slug].astro - Detail page
import { Image } from 'astro:assets';

const { post } = Astro.props;
---

<article>
  <Image
    src={post.data.coverImage}
    alt={post.data.coverImageAlt}
    transition:name={`post-image-${post.slug}`}
    class="w-full aspect-video object-cover"
  />
  <h1 transition:name={`post-title-${post.slug}`}>
    {post.data.title}
  </h1>
</article>
```

### Transition Animations

```astro
---
// Custom transition animations
---

<header transition:animate="none">
  <!-- Header persists without animation -->
</header>

<main transition:animate="slide">
  <!-- Slides in from right on forward nav, left on back -->
</main>

<aside transition:animate="fade">
  <!-- Simple fade in/out -->
</aside>

<!-- Custom animation -->
<div transition:animate={{
  old: {
    name: 'fadeOut',
    duration: '0.2s',
    easing: 'ease-out',
  },
  new: {
    name: 'fadeIn',
    duration: '0.3s',
    easing: 'ease-in',
    delay: '0.1s',
  },
}}>
  Custom animated content
</div>

<style is:global>
  @keyframes fadeOut {
    from { opacity: 1; transform: scale(1); }
    to { opacity: 0; transform: scale(0.95); }
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: scale(1.05); }
    to { opacity: 1; transform: scale(1); }
  }
</style>
```

### Persisting State Across Transitions

```astro
---
// Elements with transition:persist maintain state
import AudioPlayer from '@components/react/AudioPlayer';
import VideoPlayer from '@components/react/VideoPlayer';
---

<!-- Audio player continues playing during navigation -->
<div transition:persist="media-player">
  <AudioPlayer client:load />
</div>

<!-- Video maintains playback position -->
<VideoPlayer
  client:load
  transition:persist="video-player"
  videoId={videoId}
/>
```

### Transition Events

```astro
---
// Handle transition lifecycle
---

<script>
  document.addEventListener('astro:before-preparation', (event) => {
    // Before new page is fetched
    console.log('Navigating from:', event.from);
    console.log('Navigating to:', event.to);
  });

  document.addEventListener('astro:after-preparation', (event) => {
    // After new page is fetched but before swap
    console.log('New document ready');
  });

  document.addEventListener('astro:before-swap', (event) => {
    // Right before DOM swap - modify newDocument if needed
    const theme = localStorage.getItem('theme');
    event.newDocument.documentElement.dataset.theme = theme;
  });

  document.addEventListener('astro:after-swap', () => {
    // After DOM swap - reinitialize scripts
    initializeAnalytics();
    initializeThirdPartyWidgets();
  });

  document.addEventListener('astro:page-load', () => {
    // Page fully loaded (works for both initial and subsequent)
    console.log('Page loaded');
  });
</script>
```

### Fallback for Non-Supporting Browsers

```astro
---
import { ViewTransitions } from 'astro:transitions';
---

<head>
  <ViewTransitions fallback="animate" />
  <!-- Options: "animate" | "swap" | "none" -->
</head>
```

## 8. Integrations

### Tailwind CSS Setup

```javascript
// tailwind.config.mjs
import defaultTheme from 'tailwindcss/defaultTheme';

/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter Variable', ...defaultTheme.fontFamily.sans],
      },
      colors: {
        brand: {
          50: '#f0f9ff',
          100: '#e0f2fe',
          500: '#0ea5e9',
          600: '#0284c7',
          700: '#0369a1',
        },
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            a: {
              color: theme('colors.brand.600'),
              '&:hover': {
                color: theme('colors.brand.700'),
              },
            },
          },
        },
      }),
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
    require('@tailwindcss/forms'),
    require('@tailwindcss/aspect-ratio'),
  ],
};
```

```css
/* src/styles/global.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --color-background: 255 255 255;
    --color-foreground: 15 23 42;
  }

  .dark {
    --color-background: 15 23 42;
    --color-foreground: 248 250 252;
  }

  html {
    scroll-behavior: smooth;
  }

  body {
    @apply bg-white text-slate-900 dark:bg-slate-900 dark:text-slate-50;
  }
}

@layer components {
  .prose-custom {
    @apply prose prose-slate dark:prose-invert max-w-none;
  }
}
```

### React Integration with Shadcn/UI

```typescript
// src/components/react/Dialog.tsx
import * as React from 'react';
import * as DialogPrimitive from '@radix-ui/react-dialog';
import { X } from 'lucide-react';
import { cn } from '@lib/utils';

const Dialog = DialogPrimitive.Root;
const DialogTrigger = DialogPrimitive.Trigger;
const DialogPortal = DialogPrimitive.Portal;

const DialogOverlay = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Overlay>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Overlay>
>(({ className, ...props }, ref) => (
  <DialogPrimitive.Overlay
    ref={ref}
    className={cn(
      'fixed inset-0 z-50 bg-black/80 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0',
      className
    )}
    {...props}
  />
));
DialogOverlay.displayName = DialogPrimitive.Overlay.displayName;

const DialogContent = React.forwardRef<
  React.ElementRef<typeof DialogPrimitive.Content>,
  React.ComponentPropsWithoutRef<typeof DialogPrimitive.Content>
>(({ className, children, ...props }, ref) => (
  <DialogPortal>
    <DialogOverlay />
    <DialogPrimitive.Content
      ref={ref}
      className={cn(
        'fixed left-[50%] top-[50%] z-50 grid w-full max-w-lg translate-x-[-50%] translate-y-[-50%] gap-4 border bg-white p-6 shadow-lg duration-200 data-[state=open]:animate-in data-[state=closed]:animate-out data-[state=closed]:fade-out-0 data-[state=open]:fade-in-0 data-[state=closed]:zoom-out-95 data-[state=open]:zoom-in-95 data-[state=closed]:slide-out-to-left-1/2 data-[state=closed]:slide-out-to-top-[48%] data-[state=open]:slide-in-from-left-1/2 data-[state=open]:slide-in-from-top-[48%] sm:rounded-lg',
        className
      )}
      {...props}
    >
      {children}
      <DialogPrimitive.Close className="absolute right-4 top-4 rounded-sm opacity-70 ring-offset-white transition-opacity hover:opacity-100 focus:outline-none focus:ring-2 focus:ring-slate-950 focus:ring-offset-2 disabled:pointer-events-none data-[state=open]:bg-slate-100 data-[state=open]:text-slate-500">
        <X className="h-4 w-4" />
        <span className="sr-only">Close</span>
      </DialogPrimitive.Close>
    </DialogPrimitive.Content>
  </DialogPortal>
));
DialogContent.displayName = DialogPrimitive.Content.displayName;

export { Dialog, DialogTrigger, DialogContent };
```

### Image Optimization

```astro
---
// src/components/astro/OptimizedImage.astro
import { Image, getImage } from 'astro:assets';
import type { ImageMetadata } from 'astro';

interface Props {
  src: ImageMetadata | string;
  alt: string;
  widths?: number[];
  sizes?: string;
  class?: string;
  loading?: 'lazy' | 'eager';
  priority?: boolean;
}

const {
  src,
  alt,
  widths = [400, 800, 1200, 1600],
  sizes = '(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw',
  class: className,
  loading = 'lazy',
  priority = false,
} = Astro.props;

// For remote images, use getImage for more control
const isRemote = typeof src === 'string';

if (isRemote) {
  const optimizedImage = await getImage({
    src,
    width: 1200,
    format: 'webp',
  });
}
---

{isRemote ? (
  <img
    src={optimizedImage.src}
    alt={alt}
    width={optimizedImage.attributes.width}
    height={optimizedImage.attributes.height}
    class={className}
    loading={priority ? 'eager' : loading}
    decoding={priority ? 'sync' : 'async'}
  />
) : (
  <Image
    src={src}
    alt={alt}
    widths={widths}
    sizes={sizes}
    class={className}
    loading={priority ? 'eager' : loading}
    decoding={priority ? 'sync' : 'async'}
    format="webp"
    quality={80}
  />
)}
```

```astro
---
// Usage examples
import { Image } from 'astro:assets';
import heroImage from '@assets/hero.jpg';
import OptimizedImage from '@components/astro/OptimizedImage.astro';
---

<!-- Local image with automatic optimization -->
<Image
  src={heroImage}
  alt="Hero banner"
  widths={[640, 1280, 1920]}
  sizes="100vw"
  loading="eager"
  format="webp"
  quality={85}
/>

<!-- Remote image -->
<Image
  src="https://cdn.example.com/image.jpg"
  alt="Remote image"
  width={800}
  height={600}
  inferSize
/>

<!-- With picture element for art direction -->
<picture>
  <source
    media="(max-width: 768px)"
    srcset={mobileImage.src}
  />
  <Image
    src={desktopImage}
    alt="Responsive image"
    class="w-full"
  />
</picture>
```

## 9. Performance and SEO Patterns

### SEO Component

```astro
---
// src/components/astro/SEO.astro
interface Props {
  title: string;
  description: string;
  image?: string;
  article?: {
    publishedTime: Date;
    modifiedTime?: Date;
    author: string;
    tags?: string[];
  };
  canonical?: string;
  noindex?: boolean;
}

const {
  title,
  description,
  image = '/og-default.png',
  article,
  canonical,
  noindex = false,
} = Astro.props;

const siteUrl = Astro.site?.toString() || 'https://example.com';
const currentUrl = new URL(Astro.url.pathname, siteUrl).toString();
const canonicalUrl = canonical || currentUrl;
const ogImage = new URL(image, siteUrl).toString();
---

<!-- Primary Meta Tags -->
<title>{title}</title>
<meta name="title" content={title} />
<meta name="description" content={description} />
<link rel="canonical" href={canonicalUrl} />

{noindex && <meta name="robots" content="noindex, nofollow" />}

<!-- Open Graph / Facebook -->
<meta property="og:type" content={article ? 'article' : 'website'} />
<meta property="og:url" content={currentUrl} />
<meta property="og:title" content={title} />
<meta property="og:description" content={description} />
<meta property="og:image" content={ogImage} />
<meta property="og:site_name" content="Site Name" />

{article && (
  <>
    <meta property="article:published_time" content={article.publishedTime.toISOString()} />
    {article.modifiedTime && (
      <meta property="article:modified_time" content={article.modifiedTime.toISOString()} />
    )}
    <meta property="article:author" content={article.author} />
    {article.tags?.map((tag) => (
      <meta property="article:tag" content={tag} />
    ))}
  </>
)}

<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image" />
<meta property="twitter:url" content={currentUrl} />
<meta property="twitter:title" content={title} />
<meta property="twitter:description" content={description} />
<meta property="twitter:image" content={ogImage} />
```

### Structured Data

```astro
---
// src/components/astro/StructuredData.astro
interface Props {
  type: 'Article' | 'Product' | 'Organization' | 'BreadcrumbList' | 'FAQ';
  data: Record<string, any>;
}

const { type, data } = Astro.props;

function generateSchema(type: string, data: Record<string, any>) {
  const baseSchema = {
    '@context': 'https://schema.org',
    '@type': type,
  };

  switch (type) {
    case 'Article':
      return {
        ...baseSchema,
        headline: data.title,
        description: data.description,
        image: data.image,
        datePublished: data.publishDate,
        dateModified: data.modifiedDate || data.publishDate,
        author: {
          '@type': 'Person',
          name: data.author,
        },
        publisher: {
          '@type': 'Organization',
          name: 'Site Name',
          logo: {
            '@type': 'ImageObject',
            url: 'https://example.com/logo.png',
          },
        },
      };

    case 'Product':
      return {
        ...baseSchema,
        name: data.name,
        description: data.description,
        image: data.images,
        sku: data.sku,
        brand: {
          '@type': 'Brand',
          name: data.brand,
        },
        offers: {
          '@type': 'Offer',
          price: data.price,
          priceCurrency: 'USD',
          availability: data.inStock
            ? 'https://schema.org/InStock'
            : 'https://schema.org/OutOfStock',
        },
      };

    case 'BreadcrumbList':
      return {
        ...baseSchema,
        itemListElement: data.items.map((item, index) => ({
          '@type': 'ListItem',
          position: index + 1,
          name: item.name,
          item: item.url,
        })),
      };

    default:
      return { ...baseSchema, ...data };
  }
}

const schema = generateSchema(type, data);
---

<script type="application/ld+json" set:html={JSON.stringify(schema)} />
```

### Performance Optimizations

```astro
---
// src/layouts/BaseLayout.astro
import { ViewTransitions } from 'astro:transitions';
import SEO from '@components/astro/SEO.astro';

interface Props {
  title: string;
  description: string;
}

const { title, description } = Astro.props;
---

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <SEO title={title} description={description} />

    <!-- Preconnect to critical third-party origins -->
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />

    <!-- Preload critical fonts -->
    <link
      rel="preload"
      href="/fonts/inter-var.woff2"
      as="font"
      type="font/woff2"
      crossorigin
    />

    <!-- Inline critical CSS -->
    <style is:inline>
      /* Critical above-the-fold styles */
      :root {
        --color-bg: #fff;
        --color-text: #1a1a1a;
      }
      body {
        margin: 0;
        font-family: 'Inter', system-ui, sans-serif;
        background: var(--color-bg);
        color: var(--color-text);
      }
    </style>

    <!-- Defer non-critical CSS -->
    <link
      rel="stylesheet"
      href="/styles/main.css"
      media="print"
      onload="this.media='all'"
    />

    <ViewTransitions />
  </head>
  <body>
    <slot />

    <!-- Defer analytics -->
    <script>
      if ('requestIdleCallback' in window) {
        requestIdleCallback(() => {
          // Load analytics
        });
      }
    </script>
  </body>
</html>
```

### RSS Feed Generation

```typescript
// src/pages/rss.xml.ts
import rss from '@astrojs/rss';
import { getCollection } from 'astro:content';
import type { APIContext } from 'astro';
import sanitizeHtml from 'sanitize-html';
import MarkdownIt from 'markdown-it';

const parser = new MarkdownIt();

export async function GET(context: APIContext) {
  const posts = await getCollection('blog', ({ data }) => !data.draft);

  const sortedPosts = posts.sort(
    (a, b) => b.data.publishDate.valueOf() - a.data.publishDate.valueOf()
  );

  return rss({
    title: 'My Blog',
    description: 'A blog about web development',
    site: context.site!,
    items: sortedPosts.map((post) => ({
      title: post.data.title,
      pubDate: post.data.publishDate,
      description: post.data.description,
      link: `/blog/${post.slug}/`,
      content: sanitizeHtml(parser.render(post.body), {
        allowedTags: sanitizeHtml.defaults.allowedTags.concat(['img']),
      }),
      categories: post.data.tags,
      author: post.data.author.id,
    })),
    customData: `<language>en-us</language>`,
  });
}
```

### Sitemap Configuration

```javascript
// astro.config.mjs
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://example.com',
  integrations: [
    sitemap({
      filter: (page) => !page.includes('/admin/'),
      changefreq: 'weekly',
      priority: 0.7,
      lastmod: new Date(),
      customPages: [
        'https://example.com/external-page',
      ],
      serialize(item) {
        // Customize individual entries
        if (item.url.includes('/blog/')) {
          item.changefreq = 'daily';
          item.priority = 0.9;
        }
        return item;
      },
    }),
  ],
});
```

## 10. Common Site Patterns

### Blog Site Structure

```astro
---
// src/pages/blog/index.astro
import { getCollection } from 'astro:content';
import BaseLayout from '@layouts/BaseLayout.astro';
import BlogCard from '@components/astro/BlogCard.astro';
import CategoryNav from '@components/astro/CategoryNav.astro';

const posts = await getCollection('blog', ({ data }) => !data.draft);
const sortedPosts = posts.sort(
  (a, b) => b.data.publishDate.valueOf() - a.data.publishDate.valueOf()
);

const categories = [...new Set(posts.map((p) => p.data.category))];
---

<BaseLayout title="Blog" description="Latest articles and tutorials">
  <main class="container mx-auto px-4 py-12">
    <header class="mb-12">
      <h1 class="text-4xl font-bold mb-4">Blog</h1>
      <CategoryNav categories={categories} />
    </header>

    <div class="grid gap-8 md:grid-cols-2 lg:grid-cols-3">
      {sortedPosts.map((post) => (
        <BlogCard post={post} />
      ))}
    </div>
  </main>
</BaseLayout>
```

```astro
---
// src/components/astro/BlogCard.astro
import { Image } from 'astro:assets';
import type { CollectionEntry } from 'astro:content';

interface Props {
  post: CollectionEntry<'blog'>;
}

const { post } = Astro.props;
const { title, description, publishDate, coverImage, coverImageAlt, category } = post.data;
---

<article class="group">
  <a href={`/blog/${post.slug}`} class="block">
    <div class="aspect-video overflow-hidden rounded-lg mb-4">
      <Image
        src={coverImage}
        alt={coverImageAlt}
        class="w-full h-full object-cover transition-transform group-hover:scale-105"
        widths={[400, 800]}
        sizes="(max-width: 768px) 100vw, 400px"
        transition:name={`post-image-${post.slug}`}
      />
    </div>

    <div class="space-y-2">
      <span class="text-sm text-blue-600 font-medium uppercase tracking-wide">
        {category}
      </span>

      <h2
        class="text-xl font-semibold group-hover:text-blue-600 transition-colors"
        transition:name={`post-title-${post.slug}`}
      >
        {title}
      </h2>

      <p class="text-gray-600 line-clamp-2">{description}</p>

      <time class="text-sm text-gray-500" datetime={publishDate.toISOString()}>
        {publishDate.toLocaleDateString('en-US', {
          year: 'numeric',
          month: 'long',
          day: 'numeric',
        })}
      </time>
    </div>
  </a>
</article>
```

### Documentation Site Structure

```astro
---
// src/layouts/DocsLayout.astro
import { getCollection } from 'astro:content';
import BaseLayout from './BaseLayout.astro';
import DocsSidebar from '@components/astro/DocsSidebar.astro';
import TableOfContents from '@components/astro/TableOfContents.astro';
import DocsPagination from '@components/astro/DocsPagination.astro';
import type { CollectionEntry } from 'astro:content';

interface Props {
  doc: CollectionEntry<'docs'>;
  headings: { depth: number; slug: string; text: string }[];
}

const { doc, headings } = Astro.props;

// Get all docs for sidebar
const allDocs = await getCollection('docs');
const sortedDocs = allDocs.sort((a, b) => a.data.sidebar.order - b.data.sidebar.order);

// Group by category (first segment of slug)
const groupedDocs = sortedDocs.reduce((acc, doc) => {
  const category = doc.slug.split('/')[0] || 'Getting Started';
  if (!acc[category]) acc[category] = [];
  acc[category].push(doc);
  return acc;
}, {} as Record<string, typeof sortedDocs>);
---

<BaseLayout title={doc.data.title} description={doc.data.description}>
  <div class="flex min-h-screen">
    <!-- Sidebar -->
    <aside class="hidden lg:block w-64 border-r bg-gray-50 p-6">
      <DocsSidebar groups={groupedDocs} currentSlug={doc.slug} />
    </aside>

    <!-- Main content -->
    <main class="flex-1 max-w-3xl px-8 py-12">
      <article class="prose prose-slate max-w-none">
        <h1>{doc.data.title}</h1>
        <slot />
      </article>

      <DocsPagination
        prev={doc.data.prev}
        next={doc.data.next}
        allDocs={sortedDocs}
      />
    </main>

    <!-- Table of Contents -->
    <aside class="hidden xl:block w-64 p-6">
      <TableOfContents headings={headings} />
    </aside>
  </div>
</BaseLayout>
```

```astro
---
// src/components/astro/DocsSidebar.astro
import type { CollectionEntry } from 'astro:content';

interface Props {
  groups: Record<string, CollectionEntry<'docs'>[]>;
  currentSlug: string;
}

const { groups, currentSlug } = Astro.props;
---

<nav aria-label="Documentation navigation">
  {Object.entries(groups).map(([category, docs]) => (
    <div class="mb-6">
      <h3 class="font-semibold text-sm uppercase tracking-wide text-gray-500 mb-3">
        {category.replace(/-/g, ' ')}
      </h3>
      <ul class="space-y-1">
        {docs.map((doc) => (
          <li>
            <a
              href={`/docs/${doc.slug}`}
              class:list={[
                'block px-3 py-2 rounded-md text-sm transition-colors',
                currentSlug === doc.slug
                  ? 'bg-blue-100 text-blue-700 font-medium'
                  : 'text-gray-700 hover:bg-gray-100',
              ]}
              aria-current={currentSlug === doc.slug ? 'page' : undefined}
            >
              {doc.data.sidebar.label || doc.data.title}
              {doc.data.sidebar.badge && (
                <span class="ml-2 px-1.5 py-0.5 text-xs rounded bg-green-100 text-green-700">
                  {doc.data.sidebar.badge}
                </span>
              )}
            </a>
          </li>
        ))}
      </ul>
    </div>
  ))}
</nav>
```

### Marketing/Landing Page Pattern

```astro
---
// src/pages/index.astro
import BaseLayout from '@layouts/BaseLayout.astro';
import Hero from '@components/astro/Hero.astro';
import Features from '@components/astro/Features.astro';
import Testimonials from '@components/astro/Testimonials.astro';
import Pricing from '@components/astro/Pricing.astro';
import FAQ from '@components/astro/FAQ.astro';
import CTA from '@components/astro/CTA.astro';
import NewsletterForm from '@components/react/NewsletterForm';

const features = [
  {
    icon: 'rocket',
    title: 'Lightning Fast',
    description: 'Built for performance with zero JavaScript by default.',
  },
  {
    icon: 'puzzle',
    title: 'Component Islands',
    description: 'Use React, Vue, or Svelte only where you need interactivity.',
  },
  {
    icon: 'document',
    title: 'Content Collections',
    description: 'Type-safe content management with automatic validation.',
  },
];

const testimonials = await fetch('https://api.example.com/testimonials').then(r => r.json());
const pricing = await fetch('https://api.example.com/pricing').then(r => r.json());
---

<BaseLayout
  title="Astro - Build faster websites"
  description="The web framework for content-driven websites"
>
  <Hero
    title="Build faster websites with Astro"
    subtitle="The web framework for content-driven websites. Ship zero JavaScript by default."
    primaryCTA={{ text: 'Get Started', href: '/docs' }}
    secondaryCTA={{ text: 'View on GitHub', href: 'https://github.com' }}
  />

  <Features
    title="Why Astro?"
    features={features}
  />

  <Testimonials
    title="Loved by developers"
    testimonials={testimonials}
  />

  <Pricing
    title="Simple pricing"
    plans={pricing}
  />

  <FAQ title="Frequently asked questions" />

  <CTA
    title="Ready to get started?"
    description="Join thousands of developers building with Astro."
  >
    <NewsletterForm client:visible />
  </CTA>
</BaseLayout>
```

```astro
---
// src/components/astro/Hero.astro
import { Image } from 'astro:assets';
import Button from './Button.astro';
import heroImage from '@assets/hero-illustration.svg';

interface Props {
  title: string;
  subtitle: string;
  primaryCTA: { text: string; href: string };
  secondaryCTA?: { text: string; href: string };
}

const { title, subtitle, primaryCTA, secondaryCTA } = Astro.props;
---

<section class="relative overflow-hidden bg-gradient-to-b from-blue-50 to-white py-24 sm:py-32">
  <div class="container mx-auto px-4">
    <div class="grid lg:grid-cols-2 gap-12 items-center">
      <div class="max-w-2xl">
        <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold tracking-tight text-gray-900">
          {title}
        </h1>
        <p class="mt-6 text-xl text-gray-600">
          {subtitle}
        </p>
        <div class="mt-10 flex flex-wrap gap-4">
          <Button href={primaryCTA.href} variant="primary" size="lg">
            {primaryCTA.text}
          </Button>
          {secondaryCTA && (
            <Button href={secondaryCTA.href} variant="outline" size="lg">
              {secondaryCTA.text}
            </Button>
          )}
        </div>
      </div>

      <div class="relative lg:ml-auto">
        <Image
          src={heroImage}
          alt=""
          class="w-full max-w-lg"
          loading="eager"
        />
      </div>
    </div>
  </div>

  <!-- Decorative background -->
  <div class="absolute inset-0 -z-10 overflow-hidden">
    <div class="absolute -top-1/2 -right-1/4 w-96 h-96 bg-blue-100 rounded-full blur-3xl opacity-50" />
    <div class="absolute -bottom-1/2 -left-1/4 w-96 h-96 bg-purple-100 rounded-full blur-3xl opacity-50" />
  </div>
</section>
```

## Decision Matrix

### When to Use Astro

| Use Case | Astro Fit | Reason |
|----------|-----------|--------|
| Marketing sites | Excellent | Zero JS by default, fast LCP |
| Blogs | Excellent | Content collections, MDX support |
| Documentation | Excellent | File-based routing, easy navigation |
| E-commerce (content) | Good | Product pages can be static |
| E-commerce (interactive) | Moderate | May need many islands |
| Dashboards | Poor | Heavy interactivity needs SPA |
| Real-time apps | Poor | Better suited for SPA frameworks |

### Client Directive Decision Tree

```
Is the component interactive?
├── No → Use Astro component (zero JS)
└── Yes → Does user need it immediately?
    ├── Yes → client:load
    └── No → Is it below the fold?
        ├── Yes → client:visible
        └── No → Can it wait for idle?
            ├── Yes → client:idle
            └── No → client:load
```

### SSR vs SSG Decision

| Scenario | Rendering Mode | Reason |
|----------|---------------|--------|
| Public blog posts | SSG | Content rarely changes |
| Product pages | SSG with ISR | Periodic updates |
| User dashboard | SSR | Personalized content |
| Search results | SSR | Dynamic queries |
| Landing pages | SSG | Maximum performance |
| API routes | Server | Dynamic responses |

## Common Pitfalls

1. **Over-hydrating** - Using `client:load` everywhere defeats the purpose of islands
2. **Missing `prerender` exports** - SSR pages need explicit `export const prerender = false`
3. **Ignoring TypeScript** - Content collections require typed schemas for full benefits
4. **Large islands** - Keep interactive components small and focused
5. **Not using content collections** - Manual file handling loses type safety
6. **Blocking resources** - Preload critical assets, defer non-essential JS
7. **Missing image optimization** - Always use `astro:assets` Image component
8. **No view transition names** - Animating elements need unique `transition:name`
