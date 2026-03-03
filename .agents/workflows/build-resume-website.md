---
description: How to build a modern resume website from a PDF using Anthropic-inspired styling
---

# Workflow: Build Resume Website from PDF

## Overview

This workflow converts a PDF resume into a beautiful, scrollable single-page website using vanilla HTML/CSS/JS with an Anthropic-inspired design system. The site also includes a separate blog section (`padmashri.org`) for personal journals.

---

## Step 1 — Read Reference Files

```
1a. View refernce style.png — note colors, fonts, spacing, section layout
1b. Read style.txt — extract CSS custom property names for colors, type scale, spacing tokens
1c. Note: background=#faf9f5, text=#141413, accent=#d97757, fonts: Playfair Display + Inter
```

---

## Step 2 — Extract PDF Content

PDFs with multi-column layouts require structured extraction:

```bash
pip install pymupdf
```

```python
import fitz

doc = fitz.open('resume.pdf')
with open('resume_content.txt', 'w', encoding='utf-8') as out:
    for page_num, page in enumerate(doc):
        out.write(f'=== PAGE {page_num+1} ===\n')
        d = page.get_text('dict')
        for b in sorted(d['blocks'], key=lambda x: (round(x['bbox'][1]/10), x['bbox'][0])):
            if b['type'] == 0:
                for line in b['lines']:
                    text = ''.join(span['text'] for span in line['spans'])
                    if text.strip():
                        out.write(f"x={line['bbox'][0]:.0f} y={line['bbox'][1]:.0f} | {text.strip()}\n")
```

> Always write to a file, not stdout — terminal output gets truncated.

**Organize extracted content into sections:** Name + Contact · Summary · Experience · Education · Certifications

---

## Step 3 — Create Design Tokens in CSS

```css
:root {
  --ivory-light: #faf9f5;
  --ivory-medium: #f0eee6;
  --slate-dark: #141413;
  --slate-medium: #3d3d3a;
  --slate-light: #5e5d59;
  --clay: #d97757;
  --border: rgba(20, 20, 19, 0.1);
  --font-serif: "Playfair Display", Georgia, serif;
  --font-sans: "Inter", Arial, sans-serif;
  --sp-4: 1rem;
  --sp-5: 1.5rem;
  --sp-6: 2rem; /* ... */
  --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

---

## Step 4 — Build HTML Structure (Resume)

```
<nav>                  — Fixed, frosted glass, scroll-aware
<header#hero>          — Full-viewport hero with name, subtitle, stats, CTA icons
<section#about>        — Summary paragraph + skill chips
<section#experience>   — Job accordion cards
<section#education>    — 3-column card grid
<section#certifications> — Dark-background cert list
<section#contact>      — Contact details
<footer>               — Logo + copyright + quick nav
```

Every `<section>` must have a matching `id` for anchor navigation.

---

## Step 5 — Hero CTA Icon Buttons

Pattern: `.btn-icon-wrap > a.btn-icon + span.btn-icon-label`

- **Exp** (`btn-icon--dark`) → scrolls to `#experience`
- **Email** (`btn-icon--outline`) → `mailto:` link
- **LinkedIn** (`btn-icon--outline`) → LinkedIn in new tab
- **Resume** (`btn-icon--outline`) → `href="padmashri_resume.pdf" download="Padmashri_R_Resume.pdf"`

---

## Step 6 — Job Accordion

```css
.job-details {
  max-height: 2000px;
  transition: max-height 0.5s;
}
.job-details.collapsed {
  max-height: 0;
  overflow: hidden;
}
```

Each job: number badge · company (H3 serif) · role (clay color) · date · toggle (+/−) · tech tags + bullets

---

## Step 7 — JavaScript Interactivity

```
a) Nav scroll effect   → toggle 'scrolled' class
b) Hamburger menu      → toggle 'open' class on nav links
c) Scroll reveal       → IntersectionObserver on .reveal elements
d) Accordion toggle    → toggle 'collapsed' class + aria-expanded
e) Active nav tracking → IntersectionObserver on sections
f) Hero entrance anim  → requestAnimationFrame double-call for stagger
g) Parallax (optional) → translate hero bg text on scroll
```

---

## Step 8 — Blog Integration

### Adding a blog post (automated)

```bash
python publish_blog.py "My Journal.pdf"
python publish_blog.py "Travel Notes.docx"
```

The script:

1. Extracts text from PDF or Word
2. Detects sections/headings
3. Generates `blogs/<slug>.html` with full styling + TOC sidebar
4. Adds a card to `blog-only.html`
5. Opens Chrome for review

### Blog page structure

```
blog-only.html          — Blog landing page (padmashri.org)
  Hero: "Padmashri Writes."
  Posts grid: featured card (full width) + regular cards

blogs/<slug>.html       — Individual blog post
  Nav: All Posts only
  Hero: title + metadata (date, read time, author)
  Layout: article body + sticky sidebar TOC
  Footer: All Posts link only
```

---

## Step 9 — Two-Site Deployment

### File mapping

| Domain                 | File                              | Repo               |
| ---------------------- | --------------------------------- | ------------------ |
| `padmashri.org`        | `blog-only.html` → `index.html`   | `padmashri-blog`   |
| `resume.padmashri.org` | `resume-only.html` → `index.html` | `padmashri-resume` |

### DNS (Squarespace)

Already configured A records for `padmashri.org`. Only add:

| Type  | Host     | Data                |
| ----- | -------- | ------------------- |
| CNAME | `resume` | `advirao.github.io` |

### GitHub Pages

Each repo → Settings → Pages → Source: `main` → Set Custom domain

### CNAME files

- `padmashri-blog/CNAME` → `padmashri.org`
- `padmashri-resume/CNAME` → `resume.padmashri.org`

---

## Step 10 — Git Setup

```bash
git init
# .gitignore excludes *.pdf, *.py scripts but whitelists resume PDF:
# Add: !padmashri_resume.pdf

git add index.html style.css main.js .gitignore .agents/ CNAME
git add -f padmashri_resume.pdf   # force-add whitelisted PDF
git commit -m "feat: initial resume website"
```

---

## Pre-Launch Checklist

- [ ] All section `id` attributes match nav `href` anchors
- [ ] Fonts load from Google Fonts
- [ ] All job toggles open/close correctly
- [ ] Hamburger closes when nav link is clicked
- [ ] `padmashri_resume.pdf` committed (`git ls-files padmashri_resume.pdf`)
- [ ] CNAME file present in each deployment repo
- [ ] Blog post "Read Story" links work from blog-only.html
- [ ] Blog post "← Back to Blog" links back to blog-only.html
- [ ] TOC links scroll to correct sections in blog post
- [ ] `publish_blog.py` tested with a new PDF
