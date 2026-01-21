---
skill: cms-content-modeling
version: "1.0.0"
description: "Sanity and Payload CMS schema design principles and content modeling"
used-by: [cms-integration-engineer, backend-engineer, content-migration-specialist]
---

# CMS Content Modeling

## Content Modeling Process

### Step 1: Content Audit
1. List all content types from design
2. Identify reusable content blocks
3. Map relationships between content
4. Define required vs optional fields

### Step 2: Schema Structure
```
Document Types (standalone)
├── page
├── post
├── author
└── settings

Object Types (embedded)
├── seo
├── portableText
└── cta
```

## Sanity Schema Patterns

### Document Type
```typescript
// schemas/documents/post.ts
import { defineType, defineField } from 'sanity';

export default defineType({
  name: 'post',
  title: 'Blog Post',
  type: 'document',
  fields: [
    defineField({
      name: 'title',
      title: 'Title',
      type: 'string',
      validation: (Rule) => Rule.required().max(100),
    }),
    defineField({
      name: 'slug',
      title: 'Slug',
      type: 'slug',
      options: { source: 'title', maxLength: 96 },
      validation: (Rule) => Rule.required(),
    }),
    defineField({
      name: 'author',
      title: 'Author',
      type: 'reference',
      to: [{ type: 'author' }],
    }),
    defineField({
      name: 'mainImage',
      title: 'Main Image',
      type: 'image',
      options: { hotspot: true },
      fields: [
        { name: 'alt', type: 'string', title: 'Alt Text' },
      ],
    }),
    defineField({
      name: 'body',
      title: 'Body',
      type: 'blockContent',
    }),
    defineField({
      name: 'seo',
      title: 'SEO',
      type: 'seo',
    }),
  ],
  preview: {
    select: { title: 'title', author: 'author.name', media: 'mainImage' },
    prepare({ title, author, media }) {
      return { title, subtitle: author, media };
    },
  },
});
```

### Reusable Block Content
```typescript
// schemas/objects/blockContent.ts
export default defineType({
  name: 'blockContent',
  title: 'Block Content',
  type: 'array',
  of: [
    { type: 'block', styles: [
      { title: 'Normal', value: 'normal' },
      { title: 'H2', value: 'h2' },
      { title: 'H3', value: 'h3' },
      { title: 'Quote', value: 'blockquote' },
    ]},
    { type: 'image', options: { hotspot: true } },
    { type: 'code' },
    { type: 'callout' },
  ],
});
```

### SEO Object
```typescript
export default defineType({
  name: 'seo',
  title: 'SEO',
  type: 'object',
  fields: [
    { name: 'metaTitle', type: 'string', title: 'Meta Title' },
    { name: 'metaDescription', type: 'text', title: 'Meta Description', rows: 3 },
    { name: 'ogImage', type: 'image', title: 'OG Image' },
    { name: 'noIndex', type: 'boolean', title: 'No Index' },
  ],
});
```

## Payload CMS Patterns

### Collection Config
```typescript
// collections/Posts.ts
import { CollectionConfig } from 'payload/types';

export const Posts: CollectionConfig = {
  slug: 'posts',
  admin: { useAsTitle: 'title' },
  access: {
    read: () => true,
    create: ({ req: { user } }) => !!user,
    update: ({ req: { user } }) => !!user,
    delete: ({ req: { user } }) => user?.role === 'admin',
  },
  fields: [
    { name: 'title', type: 'text', required: true },
    { name: 'slug', type: 'text', unique: true, admin: { position: 'sidebar' } },
    { name: 'author', type: 'relationship', relationTo: 'users' },
    { name: 'featuredImage', type: 'upload', relationTo: 'media' },
    { name: 'content', type: 'richText' },
    { name: 'status', type: 'select', options: ['draft', 'published'], defaultValue: 'draft' },
    { name: 'publishedAt', type: 'date', admin: { position: 'sidebar' } },
  ],
  hooks: {
    beforeChange: [
      ({ data, operation }) => {
        if (operation === 'create' && !data.slug) {
          data.slug = slugify(data.title);
        }
        return data;
      },
    ],
  },
};
```

## GROQ Query Patterns (Sanity)

```groq
// Fetch posts with author
*[_type == "post" && defined(slug.current)] | order(publishedAt desc) {
  _id,
  title,
  "slug": slug.current,
  publishedAt,
  mainImage { asset-> { url } },
  "author": author-> { name, image },
  "excerpt": pt::text(body)[0...200]
}

// Fetch single post by slug
*[_type == "post" && slug.current == $slug][0] {
  ...,
  "author": author-> { name, bio, image },
  body[] {
    ...,
    _type == "image" => { ..., asset-> { url, metadata } }
  }
}
```

## Decision Criteria

| Pattern | Use When |
|---------|----------|
| Reference | Content reused across documents |
| Embedded object | Content specific to one document |
| Array of blocks | Flexible page building |
| Select field | Fixed set of options |
| Slug field | URL-friendly identifiers |

## Common Pitfalls

1. **Deep nesting**: Hard to query, slow performance
2. **Missing validation**: Invalid data in production
3. **No preview config**: Poor editor experience
4. **Hardcoded slugs**: Broken links when renamed
5. **Missing alt text**: Accessibility issues
6. **Over-referencing**: Query complexity explosion
7. **No draft workflow**: Accidental publishes
