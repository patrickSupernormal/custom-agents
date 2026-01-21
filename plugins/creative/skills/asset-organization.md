---
skill: asset-organization
version: "1.0.0"
description: "Managing, collecting, and organizing visual and brand assets systematically"
used-by: [asset-manager, brand-guardian, project-manager, designer]
---

# Asset Organization

## Purpose
Establish systematic processes for collecting, organizing, naming, and managing visual assets to ensure efficient workflows and brand consistency.

## Step-by-Step Procedure

### Step 1: Asset Collection

#### Asset Request Template
```markdown
# Asset Request: [Project Name]

**Requested by**: [Name]
**Deadline**: [Date]
**Project context**: [Brief description]

## Required Assets

### Brand Assets
- [ ] Logo files (SVG, PNG, all variations)
- [ ] Brand colors (hex codes, RGB, CMYK)
- [ ] Typography files (font files or names)
- [ ] Brand guidelines document

### Visual Assets
- [ ] Photography (specify subjects needed)
- [ ] Icons (specify style/set)
- [ ] Illustrations (specify style)
- [ ] Videos/animations

### Content Assets
- [ ] Existing copy/messaging
- [ ] Approved taglines
- [ ] Boilerplate content
- [ ] Legal/compliance copy

### Technical Assets
- [ ] Favicon files
- [ ] Social media templates
- [ ] Email templates
- [ ] Presentation templates

## File Delivery
**Preferred method**: [Dropbox/Drive/Email]
**Contact**: [Email]

## Questions
[Any clarifying questions about assets]
```

### Step 2: Folder Structure

#### Standard Project Structure
```
/[Project Name]
├── /00_Admin
│   ├── /Briefs
│   ├── /Contracts
│   └── /Meeting_Notes
├── /01_Brand_Assets
│   ├── /Logo
│   │   ├── /Primary
│   │   ├── /Secondary
│   │   └── /Favicon
│   ├── /Colors
│   ├── /Typography
│   └── /Guidelines
├── /02_Photography
│   ├── /Raw
│   ├── /Edited
│   └── /Web_Optimized
├── /03_Graphics
│   ├── /Icons
│   ├── /Illustrations
│   └── /Patterns
├── /04_Video
│   ├── /Source
│   ├── /Edits
│   └── /Finals
├── /05_Copy
│   ├── /Drafts
│   ├── /Approved
│   └── /Translations
├── /06_Deliverables
│   ├── /Working_Files
│   ├── /Exports
│   └── /Archive
└── /07_Reference
    ├── /Inspiration
    ├── /Competitive
    └── /Research
```

### Step 3: File Naming Conventions

#### Naming Formula
```
[project]_[asset-type]_[descriptor]_[version]_[date].[ext]

Examples:
acme_logo_primary_v1_20240115.svg
acme_hero_homepage_v2_20240120.jpg
acme_icon_arrow-right_v1_20240115.svg
```

#### Naming Rules
| Element | Format | Example |
|---------|--------|---------|
| Project | Lowercase, hyphenated | acme-corp |
| Asset type | Lowercase | logo, icon, photo |
| Descriptor | Lowercase, hyphenated | hero-homepage |
| Version | v + number | v1, v2, v12 |
| Date | YYYYMMDD | 20240115 |
| Extension | Lowercase | .svg, .png, .jpg |

#### Status Prefixes (Optional)
```
DRAFT_ - Work in progress
REVIEW_ - Awaiting approval
APPROVED_ - Client approved
FINAL_ - Ready for use
ARCHIVE_ - Superseded version
```

### Step 4: Image Specifications

#### Web Image Standards
| Use Case | Format | Max Width | Max Size | Notes |
|----------|--------|-----------|----------|-------|
| Hero images | WebP/JPEG | 1920px | 200KB | Compress 80% |
| Content images | WebP/JPEG | 1200px | 100KB | Compress 85% |
| Thumbnails | WebP/JPEG | 400px | 30KB | Compress 80% |
| Icons | SVG | N/A | 5KB | Optimize paths |
| Logos | SVG | N/A | 10KB | Preserve vectors |
| Social | PNG/JPEG | Per platform | 1MB | Platform specific |

#### Social Media Dimensions
| Platform | Image Type | Dimensions |
|----------|------------|------------|
| Facebook | Post | 1200 x 630 |
| Instagram | Feed | 1080 x 1080 |
| Instagram | Story | 1080 x 1920 |
| LinkedIn | Post | 1200 x 627 |
| Twitter/X | Post | 1200 x 675 |
| YouTube | Thumbnail | 1280 x 720 |

### Step 5: Asset Inventory

#### Asset Inventory Spreadsheet
```markdown
| Asset ID | File Name | Type | Location | Version | Status | Owner | Expires |
|----------|-----------|------|----------|---------|--------|-------|---------|
| A001 | acme_logo_primary | Logo | /Brand/Logo | v3 | Active | Jane | Never |
| A002 | hero_homepage | Photo | /Photos/Heroes | v2 | Active | Stock | 2025-01 |
```

#### Tracking Fields
- **Asset ID**: Unique identifier
- **File Name**: Following naming convention
- **Type**: Logo, photo, icon, video, etc.
- **Location**: Folder path
- **Version**: Current version number
- **Status**: Active, Archive, Expired, Pending
- **Owner**: Creator or license holder
- **Expires**: License expiration (if applicable)
- **Usage Rights**: Restrictions or permissions
- **Tags**: Searchable keywords

### Step 6: Quality Control

#### Pre-Upload Checklist
- [ ] Correct file format for use case
- [ ] Optimized file size
- [ ] Proper color space (sRGB for web)
- [ ] Named according to convention
- [ ] Placed in correct folder
- [ ] Metadata stripped (privacy)
- [ ] Version number updated
- [ ] Previous version archived

#### Image Quality Checks
- [ ] Resolution appropriate for use
- [ ] No visible compression artifacts
- [ ] Colors match brand guidelines
- [ ] No watermarks or placeholder text
- [ ] Properly cropped and aligned
- [ ] Transparent background where needed

## Templates

### Asset Handoff Checklist
```markdown
# Asset Handoff: [Project Name]

## Delivered Assets
- [ ] All logo variations (SVG, PNG @1x, @2x)
- [ ] Color palette file
- [ ] Font files or licensing info
- [ ] Photography (web-optimized)
- [ ] Icons (SVG format)
- [ ] Favicon package

## Documentation Included
- [ ] Asset inventory spreadsheet
- [ ] Naming convention guide
- [ ] Usage guidelines
- [ ] License information

## Access Provided
- [ ] Shared drive access
- [ ] DAM system credentials
- [ ] Stock library login

## Training Completed
- [ ] Folder structure walkthrough
- [ ] Naming convention training
- [ ] Version control process
```

## Decision Criteria

### When to update vs. create new:
- **Update**: Minor revision, same context
- **New version**: Significant change, same asset
- **New asset**: Different purpose or context

### Format selection:
| Need | Format |
|------|--------|
| Logos, icons | SVG (vector) |
| Photos | WebP or JPEG |
| Graphics with transparency | PNG or WebP |
| Print materials | PDF, TIFF, EPS |
| Animation | GIF, MP4, Lottie |

### Archiving criteria:
- Superseded by new version
- No longer brand-compliant
- License expired
- Project completed (working files)

## Common Pitfalls

1. **No naming convention** - Files become unsearchable chaos
2. **Flat folder structure** - Everything dumped in one place
3. **Missing versions** - Overwriting instead of versioning
4. **Unoptimized files** - Huge images slowing everything down
5. **License ignorance** - Using expired or wrong-rights assets
6. **No single source of truth** - Assets scattered across platforms
7. **Stale inventory** - Documentation doesn't match reality
8. **Missing originals** - Only having flattened/exported files
9. **Inconsistent formats** - Mixed file types for same asset type
10. **No backup** - Single copy of irreplaceable assets
