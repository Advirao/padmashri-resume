---
description: How to build a modern resume website from a PDF using Anthropic-inspired styling
---

# Workflow: Build Resume Website from PDF

## Overview

This workflow converts a PDF resume into a beautiful, scrollable single-page website using vanilla HTML/CSS/JS with an Anthropic-inspired design system.

---

## Step 1 — Read Reference Files

Read all reference inputs before touching any code:

```
1a. View the reference image (style.png / screenshot) — note: colors, fonts, spacing rhythm, section layout
1b. Read style.txt — extract CSS custom property names for colors, type scale, spacing tokens
1c. Note the primary background color, text color, accent color, and font family pairs
```

**Key things to capture from the Anthropic style:**

- Background: `#faf9f5` (ivory-light), `#f0eee6` (ivory-medium)
- Text: `#141413` (slate-dark), `#5e5d59` (slate-light)
- Accent: `#d97757` (clay)
- Fonts: Serif (Georgia fallback) + Sans (Arial fallback) → map to Google Fonts equivalents

---

## Step 2 — Extract PDF Content

PDFs with multi-column layouts require a structured extraction approach.

```bash
pip install pymupdf
```

Write an extraction script:

```python
import fitz

doc = fitz.open('resume.pdf')
with open('resume_content.txt', 'w', encoding='utf-8') as out:
    for page_num, page in enumerate(doc):
        out.write(f'=== PAGE {page_num+1} ===\n')
        d = page.get_text('dict')
        blocks = d['blocks']
        # Sort by row (y) then column (x) for multi-column PDFs
        for b in sorted(blocks, key=lambda x: (round(x['bbox'][1]/10), x['bbox'][0])):
            if b['type'] == 0:
                for line in b['lines']:
                    line_text = ''.join(span['text'] for span in line['spans'])
                    if line_text.strip():
                        y = line['bbox'][1]
                        x0 = line['bbox'][0]
                        out.write(f'x={x0:.0f} y={y:.0f} | {line_text.strip()}\n')
```

> **Note:** Always write to a file, not stdout — terminal output gets truncated.
> Use `page.get_text('dict')` (not `rawdict`) — rawdict uses `chars` not `text`.

**Organize extracted content into sections:**

- Name + Contact
- Professional Summary
- Work Experience (company, role, dates, bullets)
- Education
- Certifications / Skills

---

## Step 3 — Create Design Tokens in CSS

Start with `:root` custom properties. Map the reference palette directly:

```css
:root {
  /* Colors from reference */
  --ivory-light: #faf9f5;
  --ivory-medium: #f0eee6;
  --slate-dark: #141413;
  --slate-medium: #3d3d3a;
  --slate-light: #5e5d59;
  --clay: #d97757;
  --border: rgba(20, 20, 19, 0.1);

  /* Map Google Fonts to reference font roles */
  --font-serif: "Playfair Display", Georgia, serif; /* → Anthropic Serif */
  --font-sans: "Inter", Arial, sans-serif; /* → Anthropic Sans */

  /* Spacing scale */
  --sp-4: 1rem;
  --sp-5: 1.5rem;
  --sp-6: 2rem;
  /* ... etc */

  --transition: 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

---

## Step 4 — Build HTML Structure

Use semantic HTML. The page structure must be:

```
<nav>              — Fixed, frosted glass, scroll-aware
<header#hero>      — Full-viewport hero with name, subtitle, stats
<section#about>    — Summary paragraph + skill chips
<section#experience> — Job accordion cards
<section#education>  — 3-column card grid
<section#certifications> — Dark-background cert list
<section#contact>  — Contact details + CTA button
<footer>           — Logo + copyright + quick nav
```

**Every `<section>` must have a matching `id` for anchor navigation.**

---

## Step 5 — Implement Hero Section

The hero is the most important section. Must include:

1. **Eyebrow label** — small uppercase + wide letter-spacing
2. **Large serif name** — `clamp(4rem, 10vw, 9rem)` with tight tracking
3. **Subtitle** — sans-serif, muted color, max 60ch
4. **CTA icon buttons** — circle buttons with SVG icons + small label below each
   - Pattern: `.btn-icon-wrap > a.btn-icon + span.btn-icon-label`
   - First icon: dark filled (`btn-icon--dark`); rest: outlined (`btn-icon--outline`)
   - Icons: Exp (briefcase) · Email (envelope) · LinkedIn · Resume (download arrow)
   - Resume icon uses `href="padmashri_resume.pdf" download="Padmashri_R_Resume.pdf"`
5. **Stats row** — 3 metrics with vertical dividers, separated by `border-top`
6. **Scroll indicator** — animated arrow/line at bottom

---

## Step 6 — Build Experience Accordion

Each job requires:

- Number badge (01, 02...) in muted serif
- Company name (H3, serif)
- Role (colored with `--clay`)
- Date range (small, muted)
- Toggle button (`+` / `−`) with `aria-expanded`
- Collapsible panel: tech tags + bullet list

**Accordion animation uses `max-height` transition:**

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

---

## Step 7 — Add JavaScript Interactivity

Three core features:

```
a) Nav scroll effect     → toggle 'scrolled' class on window scroll
b) Hamburger menu        → toggle 'open' class on nav links list
c) Scroll reveal         → IntersectionObserver on .reveal elements
d) Accordion toggle      → toggle 'collapsed' class + aria-expanded
e) Active nav tracking   → IntersectionObserver on sections
f) Hero entrance anim    → requestAnimationFrame double-call for staggered entrance
g) Parallax (optional)   → translate hero bg text on scroll
```

---

## Step 8 — Responsive Breakpoints

Apply two breakpoints after desktop styles are complete:

```css
@media (max-width: 900px) {
  /* Tablet */
}
@media (max-width: 600px) {
  /* Mobile */
}
```

At 900px: hide nav links, show hamburger, stack About grid to 1 column.
At 600px: stack all grids to 1 column, center footer.

---

## Step 9 — Git Setup

```bash
# Initialize
git init

# Create .gitignore (must run before git add)
# .gitignore should exclude: *.pdf, .DS_Store, Thumbs.db, *.py scripts, /tmp/
# BUT whitelist the resume PDF so it deploys to GitHub Pages:
# Add this line to .gitignore: !padmashri_resume.pdf

git add index.html style.css main.js .gitignore .agents/
git add -f padmashri_resume.pdf   # force-add whitelisted PDF
git commit -m "feat: initial resume website with Anthropic-inspired design"
```

---

## Checklist Before Launch

- [ ] All section `id` attributes match nav `href` anchors
- [ ] Fonts load from Google Fonts (check for CORS / offline fallback)
- [ ] All job toggles open/close correctly
- [ ] Hamburger closes when a nav link is clicked
- [ ] Page works with JavaScript disabled (content still readable)
- [ ] `padmashri_resume.pdf` committed to git (`git ls-files padmashri_resume.pdf` returns the file)
- [ ] `.gitignore` has `!padmashri_resume.pdf` exception so PDF is not blocked
- [ ] Download button `href` filename matches exact PDF filename on disk
- [ ] Hero CTA icons: Exp, Email, LinkedIn, Resume all work correctly
