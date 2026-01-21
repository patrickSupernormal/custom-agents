---
skill: seo-optimization
version: "1.0.0"
description: "On-page SEO best practices for content and technical optimization"
used-by: [seo-specialist, content-strategist, copywriter, technical-seo-auditor]
---

# SEO Optimization

## Purpose
Optimize content for search engine visibility while maintaining quality user experience and brand voice integrity.

## Step-by-Step Procedure

### Step 1: Keyword Research & Selection
1. **Identify seed keywords** - Core terms related to topic
2. **Expand with tools** - Use keyword research tools for variations
3. **Analyze intent** - Categorize as informational, commercial, or transactional
4. **Assess difficulty** - Balance volume against competition
5. **Select primary + secondary** - 1 primary, 3-5 secondary per page

#### Keyword Selection Criteria
| Factor | Consideration |
|--------|---------------|
| Relevance | Does it match content purpose? |
| Volume | Minimum 100 monthly searches (varies by niche) |
| Difficulty | KD < 40 for new sites, < 60 for established |
| Intent match | Commercial for product pages, informational for blogs |
| Trend | Stable or growing, not declining |

### Step 2: On-Page Optimization

#### Title Tag
```
Formula: Primary Keyword | Brand Differentiator - Brand Name
Length: 50-60 characters
Example: "Content Strategy Guide | Free Template - BrandName"
```

#### Meta Description
```
Formula: [Value proposition] + [Primary keyword naturally] + [CTA]
Length: 150-160 characters
Example: "Learn proven content strategy frameworks with our step-by-step guide. Includes free templates. Start planning smarter content today."
```

#### URL Structure
```
Pattern: /category/primary-keyword
Rules:
- Lowercase only
- Hyphens between words
- No stop words (the, and, or)
- Max 60 characters
- Include primary keyword

Good: /guides/content-strategy-framework
Bad: /blog/2024/01/the-ultimate-guide-to-content-strategy-for-beginners
```

#### Heading Structure
```
H1: Include primary keyword (1 per page, within first 100 words)
H2: Include secondary keywords naturally
H3: Semantic variations and related terms
```

### Step 3: Content Optimization

#### Keyword Placement Checklist
- [ ] Primary keyword in H1
- [ ] Primary keyword in first 100 words
- [ ] Primary keyword in at least one H2
- [ ] Primary keyword in meta title
- [ ] Primary keyword in URL
- [ ] Secondary keywords in H2s and body
- [ ] Natural keyword density (1-2% max)

#### Content Structure for SEO
```markdown
[H1: Primary Keyword + Modifier]

[Intro paragraph - hook + primary keyword + what they'll learn]

[H2: Secondary Keyword 1]
[300-500 words of valuable content]

[H2: Secondary Keyword 2]
[300-500 words of valuable content]

[H2: FAQ or Summary - includes question keywords]
[Structured data opportunity]

[CTA section]
```

### Step 4: Technical On-Page Elements

#### Image Optimization
```
File name: primary-keyword-descriptive-name.webp
Alt text: Descriptive text including keyword where natural
Size: < 100KB for standard images, < 200KB for heroes
Format: WebP with JPEG fallback
```

#### Internal Linking
- Minimum 3-5 internal links per 1000 words
- Anchor text varies (exact match, partial, branded)
- Link to related pillar and cluster content
- No orphan pages (every page linked from at least one other)

#### Schema Markup Priorities
| Content Type | Schema Type |
|--------------|-------------|
| Articles | Article, BlogPosting |
| Products | Product, Offer |
| FAQ pages | FAQPage |
| How-to guides | HowTo |
| Local business | LocalBusiness |
| Events | Event |

### Step 5: Content Quality Signals

#### E-E-A-T Optimization
- **Experience**: First-hand knowledge, case studies, examples
- **Expertise**: Author credentials, detailed explanations
- **Authoritativeness**: Citations, external links to sources
- **Trustworthiness**: Accurate info, clear attribution, transparency

#### User Experience Factors
- Reading level appropriate for audience (aim for grade 8-10)
- Short paragraphs (2-4 sentences)
- Bullet points for scannable content
- Visual breaks every 300 words
- Mobile-optimized formatting

## Templates

### SEO Content Checklist
```markdown
## Pre-Writing
- [ ] Primary keyword selected
- [ ] Search intent analyzed
- [ ] Competitor content reviewed
- [ ] Outline includes keyword placement

## Writing
- [ ] H1 includes primary keyword
- [ ] First 100 words include keyword
- [ ] H2s include secondary keywords
- [ ] Natural keyword density
- [ ] Internal links added (3-5 minimum)
- [ ] External authoritative links (1-2)

## Post-Writing
- [ ] Title tag optimized (50-60 chars)
- [ ] Meta description compelling (150-160 chars)
- [ ] URL clean and keyword-rich
- [ ] Images optimized (alt text, file size)
- [ ] Schema markup added
- [ ] Mobile preview checked
```

## Decision Criteria

### When to prioritize keywords:
- **High priority**: Product pages, pillar content, high-intent pages
- **Medium priority**: Blog posts, support content
- **Lower priority**: Legal pages, internal tools

### When to skip SEO optimization:
- Gated content (not indexable)
- Temporary campaign pages (short lifespan)
- Internal-only documentation

## Common Pitfalls

1. **Keyword stuffing** - Forcing keywords ruins readability
2. **Ignoring intent** - Ranking for wrong search intent wastes traffic
3. **Duplicate content** - Similar pages competing against each other
4. **Thin content** - Short pages without substantial value
5. **Over-optimization** - Exact match anchors look spammy
6. **Neglecting updates** - Stale content loses rankings over time
7. **Mobile afterthought** - Most searches are mobile-first
8. **Slow page speed** - Technical issues undermine content quality
9. **Missing internal links** - Orphan pages can't rank well
10. **Title tag neglect** - Generic titles kill click-through rates
