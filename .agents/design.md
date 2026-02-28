---
description: Design system and visual decisions for Padmashri R resume website
---

# Design System — Resume Website

## Design Inspiration

The visual identity is inspired by **Anthropic's website** (`anthropic.com`), specifically:

- The warm ivory/cream background palette
- Dark near-black slate for text (high contrast, editorial feel)
- Serif display headings mixed with clean sans-serif body text
- Minimal, generous whitespace with a newspaper/editorial quality
- Subtle borders instead of heavy shadows

---

## Color Palette

| Token            | Hex                  | Usage                                                       |
| ---------------- | -------------------- | ----------------------------------------------------------- |
| `--ivory-light`  | `#faf9f5`            | Page background, hero background                            |
| `--ivory-medium` | `#f0eee6`            | Section alternating backgrounds (About, Education, Contact) |
| `--ivory-dark`   | `#e8e6dc`            | Hover states on ivory surfaces                              |
| `--oat`          | `#e3dacc`            | Decorative accents                                          |
| `--slate-dark`   | `#141413`            | Primary text, buttons, nav logo, footer background          |
| `--slate-medium` | `#3d3d3a`            | Body text, job bullets                                      |
| `--slate-light`  | `#5e5d59`            | Subtext, secondary labels, nav links                        |
| `--cloud-medium` | `#b0aea5`            | Section labels, job numbers, date text                      |
| `--clay`         | `#d97757`            | Job role accent color, hover highlights                     |
| `--accent`       | `#c6613f`            | Darker clay variant, education grade badges                 |
| `--manilla`      | `#ebdbbc`            | Education grade badge background                            |
| `--kraft`        | `#d4a27f`            | Certification card icons                                    |
| `--border`       | `rgba(20,20,19,0.1)` | All dividers and card borders                               |

### Section Background Alternation

```
Hero         → --ivory-light   (warm white)
About        → --ivory-medium  (eggshell)
Experience   → --ivory-light   (warm white)
Education    → --ivory-medium  (eggshell)
Certifications → --slate-dark  (near-black, contrast section)
Contact      → --ivory-medium  (eggshell)
Footer       → --slate-dark    (near-black)
```

---

## Typography

### Font Families

| Role               | Font             | Fallback          |
| ------------------ | ---------------- | ----------------- |
| Display / Headings | Playfair Display | Georgia, serif    |
| Body / UI          | Inter            | Arial, sans-serif |

The `Playfair Display` matches Anthropic's `Anthropic Serif / Georgia` aesthetic. `Inter` is the clean sans counterpart to Anthropic's `Anthropic Sans / Arial`.

### Type Scale

| Token concept | CSS value                      | Used for                  |
| ------------- | ------------------------------ | ------------------------- |
| Hero title    | `clamp(4rem, 10vw, 9rem)`      | Page hero name            |
| Section title | `clamp(2.2rem, 4vw, 3.5rem)`   | H2 headings               |
| Job company   | `clamp(1.1rem, 1.8vw, 1.4rem)` | H3 in experience card     |
| Body          | `1rem`                         | Paragraphs, bullets       |
| Label / Tag   | `0.75–0.85rem`                 | Section labels, tech tags |

### Type Treatments

- **Italic + lighter weight** on hero subtitle word (e.g. `R.`) — editorial elegance
- **Section labels** are `uppercase + letter-spacing: 0.15em + cloud-medium color` — Anthropic-style eyebrow text
- **Headings** use `letter-spacing: -0.02em` (tight tracking) — premium, editorial look

---

## Layout & Spacing

### Container

- Max width: `89.5rem` (matching Anthropic's `--site--width`)
- Horizontal padding: `clamp(1.5rem, 4vw, 5rem)` — fluid gutters

### Spacing Scale

Uses `--sp-1` (0.25rem) through `--sp-12` (10rem), same rhythm as Anthropic's `--_spacing---space` tokens.

### Section Padding

All sections use `clamp(5rem, 10vh, 8rem)` vertical padding — generous breathing room.

---

## Components

### Navigation

- Fixed, `backdrop-filter: blur(12px)` frosted glass on ivory
- Border-bottom appears only after scroll (`scrolled` class via JS)
- Logo: 2-letter monogram in Playfair Display (serif)
- Links: thin underline animation on hover (`::after` scaleX trick)
- CTA button (pill shape, dark fill)

### Hero Section

- **Stats row**: 3 numbers separated by hairline dividers
- **Scroll indicator**: animated bouncing text + gradient line
- **Parallax**: background text drifts slightly upward on scroll (via JS)
- **Entrance animation**: each element staggers in with 100ms delay using `requestAnimationFrame`
- **CTA Icon Buttons**: four circle icon buttons in a row, each wrapped in `.btn-icon-wrap`
  - **Exp** (dark filled) — scrolls to `#experience`
  - **Email** (outline) — opens mailto link
  - **LinkedIn** (outline) — opens LinkedIn profile in new tab
  - **Resume** (outline) — triggers download of `padmashri_resume.pdf`
  - Each icon has a small label below it (`.btn-icon-label`, uppercase, 0.65rem)

> **Note:** The original large decorative `BI` background text (`hero-bg-text`) has been removed from the hero section.

### Job Experience Accordion

- Expanding/collapsing on `max-height` transition (not `height: auto`, which can't animate)
- `collapsed` class sets `max-height: 0; overflow: hidden`
- Clicking anywhere on the job header row (not just the `+` button) triggers toggle
- Tech tags displayed above bullet points inside the expanded section

### Cards (Education)

- White cards on ivory-medium background — subtle lift
- `transform: translateY(-4px)` + `box-shadow` on hover
- Grade displayed as a colored badge (`--manilla` bg + `--accent` text)

### Certifications

- Dark section (`--slate-dark` bg) for contrast — one dark band breaks the all-ivory monotony
- Cards use `rgba(255,255,255,0.05)` glass bg + `translateX(6px)` hover
- Icon squares with `rgba` white fill

### Scroll Reveal

- `IntersectionObserver` with `rootMargin: '0px 0px -60px 0px'` — elements animate when 60px above viewport bottom
- Sibling stagger: `transitionDelay = index * 80ms`
- Reset: `opacity: 0; transform: translateY(30px)` → `opacity: 1; transform: translateY(0)`

---

## Responsive Breakpoints

| Breakpoint | Changes                                                                                          |
| ---------- | ------------------------------------------------------------------------------------------------ |
| `≤ 900px`  | About grid → single column; Nav links hidden → hamburger menu shown; nav CTA hidden              |
| `≤ 600px`  | Edu grid → 1 column; cert cards → vertical stack; hero actions → column; footer → centered stack |

---

## PDF Content Extraction Strategy

The source `padmashri_resume.pdf` had a **multi-column layout** making standard `pdfminer` text extraction garbled. Solution:

1. Used `PyMuPDF (fitz)` with `page.get_text('dict')` to get structured block/line/span data
2. Sorted blocks by `(y-coordinate, x-coordinate)` to reconstruct reading order
3. Wrote output to a file (not stdout) to avoid terminal truncation
4. Manually organized content into website sections
