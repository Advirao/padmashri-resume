---
description: Design system and visual decisions for padmashri.org and resume.padmashri.org
---

# Design System — padmashri.org

## Design Inspiration

The visual identity is inspired by **Anthropic's website** (`anthropic.com`):

- Warm ivory/cream background palette
- Dark near-black slate for text (high contrast, editorial feel)
- Serif display headings mixed with clean sans-serif body text
- Minimal, generous whitespace with a newspaper/editorial quality
- Subtle borders instead of heavy shadows

---

## Color Palette

| Token            | Hex                  | Usage                                                       |
| ---------------- | -------------------- | ----------------------------------------------------------- |
| `--ivory-light`  | `#faf9f5`            | Page background, hero background                            |
| `--ivory-medium` | `#f0eee6`            | Section alternating backgrounds, card backgrounds           |
| `--ivory-dark`   | `#e8e6dc`            | Hover states on ivory surfaces                              |
| `--oat`          | `#e3dacc`            | Decorative accents                                          |
| `--slate-dark`   | `#141413`            | Primary text, buttons, nav logo, footer background          |
| `--slate-medium` | `#3d3d3a`            | Body text, job bullets, blog post body                      |
| `--slate-light`  | `#5e5d59`            | Subtext, secondary labels, nav links                        |
| `--cloud-medium` | `#b0aea5`            | Section labels, job numbers, date text                      |
| `--clay`         | `#d97757`            | Accent color: blog tags, job roles, hover highlights, links |
| `--accent`       | `#c6613f`            | Darker clay variant, education grade badges                 |
| `--manilla`      | `#ebdbbc`            | Education grade badge background                            |
| `--kraft`        | `#d4a27f`            | Certification card icons                                    |
| `--border`       | `rgba(20,20,19,0.1)` | All dividers and card borders                               |

### Section Background Alternation (Resume)

```
Hero           → --ivory-light
About          → --ivory-medium
Experience     → --ivory-light
Education      → --ivory-medium
Certifications → --slate-dark  (contrast dark band)
Contact        → --ivory-medium
Blog Preview   → --ivory-light
Footer         → --slate-dark
```

---

## Typography

| Role               | Font             | Fallback          |
| ------------------ | ---------------- | ----------------- |
| Display / Headings | Playfair Display | Georgia, serif    |
| Body / UI          | Inter            | Arial, sans-serif |

### Type Scale

| Concept       | CSS value                    | Used for                  |
| ------------- | ---------------------------- | ------------------------- |
| Hero title    | `clamp(4rem, 10vw, 9rem)`    | Resume hero name          |
| Blog hero     | `clamp(3.5rem, 8vw, 7.5rem)` | "Padmashri Writes." hero  |
| Section title | `clamp(2.2rem, 4vw, 3.5rem)` | H2 section headings       |
| Blog post h1  | `clamp(2.2rem, 5vw, 3.6rem)` | Blog post title           |
| Blog section  | `1.6rem`                     | Day 1 / Day 2 headings    |
| Body          | `1rem–1.05rem`               | Paragraphs, bullets       |
| Label / Tag   | `0.75–0.85rem`               | Blog tags, section labels |

---

## Layout & Spacing

- **Container max width:** `89.5rem` (matching Anthropic's `--site--width`)
- **Horizontal padding:** `clamp(1.5rem, 4vw, 5rem)` — fluid gutters
- **Spacing scale:** `--sp-1` (0.25rem) → `--sp-12` (10rem)
- **Section padding:** `clamp(5rem, 10vh, 8rem)` vertical

---

## Components

### Navigation

- Fixed, `backdrop-filter: blur(12px)` frosted glass on ivory
- Border-bottom appears only after scroll (`scrolled` class via JS)
- Logo: `PR` monogram in Playfair Display (serif)
- Links: thin underline animation on hover (`::after` scaleX trick)

**Resume site nav:** About · Experience · Education · Certifications · Contact + "Get in Touch" CTA  
**Blog site nav:** All Posts only (clean, minimal)  
**Blog post nav:** All Posts + Back to Blog breadcrumb

### Hero Section (Resume)

- Stats row: 3 numbers with vertical dividers
- Scroll indicator: animated bouncing text + gradient line
- Parallax: background text drifts on scroll (JS)
- Entrance animation: elements stagger in with 100ms delay
- **CTA Icon Buttons** (in order):
  - **Exp** (dark filled) → scrolls to `#experience`
  - **Email** (outline) → opens mailto
  - **LinkedIn** (outline) → opens LinkedIn in new tab
  - **Resume** (outline) → downloads `padmashri_resume.pdf`

### Blog Hero ("Padmashri Writes.")

- Giant decorative watermark text "Journal" in outline stroke
- `min-height: 60vh`
- Stats row: Posts Published · Destinations Covered · Year Started

### Blog Cards

- Rounded cards (`border-radius: 14px`) on ivory-medium background
- Hover: `translateY(-6px)` + `box-shadow`
- Clay-colored tags (`blog-card-tag`), location pills (`blog-loc`)
- Featured card spans full grid width with two-column internal grid
- Coming Soon card: dashed border, reduced opacity

### Blog Post Page

- Layout: main article + sticky sidebar TOC (240px)
- Sidebar: Table of Contents + trip stats
- Section headings have clay left-border `::before` accent (48px wide)
- Pull quotes: `blog-highlight` class with left clay border
- Back to top floating button (appears after 400px scroll)
- TOC active link tracking via `IntersectionObserver`

### Job Experience Accordion (Resume)

- `max-height` transition (not `height: auto`)
- `collapsed` class → `max-height: 0; overflow: hidden`
- Full header row is clickable, not just the `+` button
- Tech tags displayed above bullet points

---

## Responsive Breakpoints

| Breakpoint | Changes                                                                             |
| ---------- | ----------------------------------------------------------------------------------- |
| `≤ 900px`  | Blog grid → 1 col; nav links hidden → hamburger; sidebar TOC becomes top bar        |
| `≤ 600px`  | All grids stack; hero font scales down; blog post layout collapses to single column |

---

## PDF Content Extraction Strategy

For both resume and blog PDFs:

1. Use `PyMuPDF (fitz)` with `page.get_text()` for extraction
2. For multi-column PDFs: use `page.get_text('dict')` + sort blocks by `(y, x)` coordinates
3. Always write output to a file, not stdout (terminal truncates)
4. `publish_blog.py` handles blog PDF extraction automatically
