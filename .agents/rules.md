---
description: Core rules, conventions, and constraints for this personal website (resume + blog)
---

# Rules — padmashri.org & resume.padmashri.org

## Technology Stack

- **HTML** — Semantic HTML5 (no frameworks)
- **CSS** — Vanilla CSS with custom properties (no Tailwind, no preprocessors)
- **JavaScript** — Vanilla ES2020+ (no libraries, no bundlers)
- **Fonts** — Google Fonts only (`Playfair Display` + `Inter`)
- **No build step** — files must work by opening any `.html` file directly in a browser
- **PDF** — `padmashri_resume.pdf` committed to git (exception in `.gitignore`) so the download button works on GitHub Pages

---

## Project Structure

```
resume/                         ← main working project
├── index.html                  # Combined site (resume + blog preview) — local reference only
├── resume-only.html            # Resume-only version → deploys to resume.padmashri.org
├── blog-only.html              # Blog landing page → deploys to padmashri.org
├── style.css                   # Shared design system (used by all pages)
├── main.js                     # Interactivity for resume (accordion, scroll reveal, etc.)
├── publish_blog.py             # 🛠 One-command blog publisher: python publish_blog.py file.pdf
├── CNAME                       # Contains: resume.padmashri.org (for GitHub Pages)
├── padmashri_resume.pdf        # Resume PDF — committed intentionally for download
├── Journal.pdf                 # Source PDF for Arizona trip blog post
├── refernce style.png          # Design reference screenshot (Anthropic)
├── .gitignore
├── README.md
├── blogs/
│   └── arizona-trip.html       # Blog post: Arizona Adventure (June 2025)
└── .agents/
    ├── design.md
    ├── rules.md
    └── workflows/
        └── build-resume-website.md

```

### Deployment folders (ready to push to GitHub)

```
MyProject/
├── padmashri-blog/             ← Push to GitHub repo "padmashri-blog" → padmashri.org
│   ├── index.html              (copy of blog-only.html)
│   ├── style.css
│   ├── CNAME                   (contains: padmashri.org)
│   └── blogs/
│       └── arizona-trip.html
│
└── padmashri-resume-deploy/    ← Push to GitHub repo "padmashri-resume" → resume.padmashri.org
    ├── index.html              (copy of resume-only.html)
    ├── style.css
    ├── main.js
    ├── padmashri_resume.pdf
    └── CNAME                   (contains: resume.padmashri.org)
```

---

## Two-Site Architecture

| URL                    | Source file        | GitHub repo        | Audience                 |
| ---------------------- | ------------------ | ------------------ | ------------------------ |
| `padmashri.org`        | `blog-only.html`   | `padmashri-blog`   | Friends, family, general |
| `resume.padmashri.org` | `resume-only.html` | `padmashri-resume` | Recruiters, employers    |

---

## Adding a New Blog Post

```bash
python publish_blog.py "My New Journal.pdf"
# or
python publish_blog.py "Travel Notes.docx"
```

This script automatically:

1. Extracts text from PDF or Word doc
2. Detects title and section headings
3. Generates `blogs/<slug>.html` with full styling
4. Adds a card to `blog-only.html`
5. Opens Chrome to review

After reviewing, copy updated files to `padmashri-blog/` folder and push to GitHub.

---

## CSS Rules

1. **Always use CSS custom properties** for every color, spacing, and type value
2. **Desktop-first** with `max-width` breakpoints at `900px` and `600px`
3. **Spacing scale** — use `--sp-1` through `--sp-12` (0.25rem steps), never hardcode pixel values
4. **Transitions** — always use `var(--transition)` (`0.3s cubic-bezier(0.4, 0, 0.2, 1)`)
5. **Never use `!important`**
6. **Color names** must match the design palette exactly (e.g. `--ivory-light`, `--slate-dark`, `--clay`)

## HTML Rules

1. Use semantic elements: `<header>`, `<nav>`, `<section>`, `<article>`, `<footer>`
2. Every `<section>` must have a unique `id` for anchor navigation
3. All interactive elements need `aria-*` attributes
4. `<meta name="description">` must be filled in

## JavaScript Rules

1. No `document.write()`, no `eval()`
2. Use `IntersectionObserver` for scroll effects — never scroll events for reveal animations
3. Use `{ passive: true }` on all scroll/touch listeners
4. Accordion: toggle `collapsed` class + `aria-expanded` simultaneously
5. Hero entrance animation uses `requestAnimationFrame` double-call pattern

## Git Rules

- Commit message format: `type: short description` (e.g. `feat: add blog post`)
- `padmashri_resume.pdf` IS committed intentionally — `git add -f` + `!padmashri_resume.pdf` in `.gitignore`
- Never commit: `Journal.pdf`, `*.py` scripts, `refernce style.png`, `resume-only.html`, `blog-only.html` to the deployment repos
- Never commit OS files (`.DS_Store`, `Thumbs.db`) or editor folders
