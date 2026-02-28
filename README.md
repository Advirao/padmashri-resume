# Personal Resume Website

A modern, scrollable single-page resume website for Padmashri R, built with vanilla HTML, CSS, and JavaScript using an Anthropic-inspired design system.

## Tech Stack

- **HTML5** — Semantic, accessible markup
- **Vanilla CSS** — Custom properties design system, no frameworks
- **Vanilla JS** — IntersectionObserver animations, accordion, mobile nav
- **Google Fonts** — Playfair Display + Inter

## Design

Inspired by [Anthropic's website](https://anthropic.com) — warm ivory/cream palette, dark slate typography, editorial serif headings, generous whitespace.

See `.agents/design.md` for full design documentation.

## Project Structure

```
├── index.html               # Main page
├── style.css                # Design system + styles
├── main.js                  # Interactivity
├── padmashri_resume.pdf     # Resume PDF (committed for GitHub Pages download)
├── .gitignore
└── .agents/
    ├── design.md            # Design decisions & tokens
    ├── rules.md             # Coding rules & conventions
    └── workflows/
        └── build-resume-website.md   # Step-by-step workflow
```

## Features

- Smooth scroll navigation with active link tracking
- Animated hero entrance with staggered elements
- Hero CTA icon buttons: **Exp** · **Email** · **LinkedIn** · **Resume (download)**
- Expandable/collapsible job accordion
- IntersectionObserver scroll reveal for all cards
- Frosted glass fixed navbar
- Fully responsive (mobile hamburger menu)
- Resume PDF download (serves `padmashri_resume.pdf`)

## Usage

Open `index.html` in any browser — no build step required.

## GitHub Pages Deployment

`padmashri_resume.pdf` is committed to the repo (whitelisted via `!padmashri_resume.pdf` in `.gitignore`) so the download button works correctly when hosted on GitHub Pages.
