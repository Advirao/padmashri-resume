# padmashri.org — Personal Website

A personal website with two distinct sections, both hosted on GitHub Pages for free.

| URL                                                  | Purpose                         | Audience                        |
| ---------------------------------------------------- | ------------------------------- | ------------------------------- |
| [padmashri.org](https://padmashri.org)               | Blog — "Padmashri Writes."      | Friends, family, general public |
| [resume.padmashri.org](https://resume.padmashri.org) | Resume — Data & BI Professional | Recruiters, employers           |

---

## Tech Stack

- **HTML5** + **Vanilla CSS** + **Vanilla JS** — no frameworks, no build step
- **Fonts:** Playfair Display (serif) + Inter (sans) via Google Fonts
- **Hosting:** GitHub Pages (free)
- **Domain:** padmashri.org via Squarespace DNS

## Design

Anthropic-inspired design system — warm ivory palette (`#faf9f5`), editorial serif headings (Playfair Display), clay accent (`#d97757`). See `.agents/design.md` for the full design system.

---

## Project Structure

```
resume/
├── index.html              # Full combined site (local dev reference)
├── resume-only.html        # → resume.padmashri.org
├── blog-only.html          # → padmashri.org
├── style.css               # Shared design system
├── main.js                 # Resume interactivity
├── publish_blog.py         # Blog publishing automation
├── padmashri_resume.pdf    # Resume PDF (committed for download)
├── Journal.pdf             # Arizona trip source PDF
├── CNAME                   # resume.padmashri.org
├── blogs/
│   └── arizona-trip.html   # Arizona Adventure (June 2025)
└── .agents/
    ├── design.md           # Full design system reference
    ├── rules.md            # Coding conventions & architecture
    └── workflows/
        └── build-resume-website.md
```

---

## Publishing a New Blog Post

Drop a PDF or Word doc and run one command:

```bash
python publish_blog.py "My New Journal.pdf"
```

This automatically extracts content, generates a styled HTML post, adds a card to the blog index, and opens Chrome for review.

---

## Deployment

Two separate GitHub repos, each with a `CNAME` file and GitHub Pages enabled:

**Blog** (`padmashri-blog` repo):

```bash
git init && git add . && git commit -m "feat: blog"
git remote add origin https://github.com/Advirao/padmashri-blog.git
git push -u origin main
# → Settings > Pages > Custom domain: padmashri.org
```

**Resume** (`padmashri-resume` repo — this repo):

```bash
# Already set up. Just ensure:
# → Settings > Pages > Custom domain: resume.padmashri.org
```

**DNS** (Squarespace — only one record to add):

| Type  | Host     | Data                |
| ----- | -------- | ------------------- |
| CNAME | `resume` | `advirao.github.io` |

The 4 A records for `padmashri.org` are already configured.
