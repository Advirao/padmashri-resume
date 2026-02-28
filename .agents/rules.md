---
description: Core rules, conventions, and constraints for building resume/portfolio websites
---

# Rules — Resume Website

## Technology Stack

- **HTML** — Semantic HTML5 (no frameworks)
- **CSS** — Vanilla CSS with custom properties (no Tailwind, no preprocessors)
- **JavaScript** — Vanilla ES2020+ (no libraries, no bundlers)
- **Fonts** — Google Fonts only (`Playfair Display` + `Inter`)
- **No build step** — files must work by opening `index.html` directly in a browser

## File Structure

```
resume/
├── index.html        # Single-page app
├── style.css         # All styles
├── main.js           # All interactivity
├── .gitignore
└── .agents/
    ├── design.md
    ├── rules.md
    └── workflows/
        └── build-resume-website.md
```

## CSS Rules

1. **Always use CSS custom properties** for every color, spacing, and type value — define them all in `:root`
2. **Mobile-first is NOT required** here — desktop-first with `max-width` breakpoints at `900px` and `600px`
3. **Spacing scale** — use `--sp-1` through `--sp-12` (0.25rem steps), never hardcode pixel values
4. **Border radius** — use `--r-sm`, `--r-md`, `--r-lg`, `--r-full` tokens
5. **Transitions** — always use `var(--transition)` (`0.3s cubic-bezier(0.4, 0, 0.2, 1)`)
6. **Never use `!important`**
7. **Color names** must match the design palette exactly (e.g. `--ivory-light`, `--slate-dark`, `--clay`)

## HTML Rules

1. Use **semantic elements**: `<header>`, `<nav>`, `<section>`, `<article>`, `<footer>`
2. Every `<section>` must have a unique `id` for anchor navigation
3. All interactive elements need `aria-*` attributes
4. Images use absolute or relative paths — never base64 inline
5. `<meta name="description">` must be filled in

## JavaScript Rules

1. No `document.write()`, no `eval()`
2. Use `IntersectionObserver` for scroll effects — never `scroll` event for reveal animations
3. Use `{ passive: true }` on all scroll/touch listeners
4. Accordion pattern: toggle `collapsed` class + `aria-expanded` attribute simultaneously
5. Hero entrance animation uses `requestAnimationFrame` double-call pattern to ensure paint

## Accessibility

- All buttons have `aria-label` or visible text
- Toggle buttons update `aria-expanded` on state change
- Hamburger menu closes on nav link click
- `prefers-reduced-motion` respected for parallax

## Git Rules

- Commit message format: `type: short description` (e.g. `feat: add experience section`)
- Never commit `*.pdf` files (personal data)
- Never commit OS files (`.DS_Store`, `Thumbs.db`)
- Never commit editor folders (`.vscode/`, `.idea/`)
