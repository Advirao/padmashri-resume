#!/usr/bin/env python3
"""
publish_blog.py — Drop a PDF or Word doc, publish a blog post automatically.

Usage:
    python publish_blog.py "My Journal.pdf"
    python publish_blog.py "Travel Notes.docx"

What it does:
    1. Extracts text from the file
    2. Generates a styled blog post in blogs/<slug>.html
    3. Adds a new card to blog-only.html
    4. Opens both in Chrome for review
"""

import sys
import os
import re
import json
import subprocess
from datetime import datetime
from pathlib import Path

# ── Helpers ────────────────────────────────────────────────────────────────────

def slugify(text):
    """Convert title to a URL-safe filename slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')

def extract_pdf(path):
    """Extract text from PDF using PyMuPDF."""
    try:
        import fitz
    except ImportError:
        print("Installing pymupdf...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pymupdf", "-q"])
        import fitz

    doc = fitz.open(path)
    pages = []
    for page in doc:
        pages.append(page.get_text())
    return '\n'.join(pages)

def extract_docx(path):
    """Extract text from Word .docx file."""
    try:
        from docx import Document
    except ImportError:
        print("Installing python-docx...")
        subprocess.run([sys.executable, "-m", "pip", "install", "python-docx", "-q"])
        from docx import Document

    doc = Document(path)
    return '\n'.join(p.text for p in doc.paragraphs if p.text.strip())

def extract_text(path):
    ext = Path(path).suffix.lower()
    if ext == '.pdf':
        return extract_pdf(path)
    elif ext in ('.docx', '.doc'):
        return extract_docx(path)
    else:
        print(f"ERROR: Unsupported file type '{ext}'. Use .pdf or .docx")
        sys.exit(1)

def parse_sections(raw_text):
    """
    Split raw text into a title + list of (heading, paragraphs) sections.
    Heuristic: short lines (< 60 chars) that look like headings become section dividers.
    """
    lines = [l.strip() for l in raw_text.splitlines()]
    lines = [l for l in lines if l]  # remove blanks

    # Grab the first non-empty line as title candidate
    title = lines[0] if lines else "New Blog Post"

    # Combine remaining lines into paragraphs
    body_lines = lines[1:]

    sections = []
    current_heading = None
    current_paras = []
    buffer = []

    def flush_buffer():
        if buffer:
            text = ' '.join(buffer).strip()
            if text:
                current_paras.append(text)
            buffer.clear()

    heading_pattern = re.compile(
        r'^(Day\s+\d+|Chapter\s+\d+|Part\s+\d+|Section\s+\d+|[A-Z][^a-z]{4,})',
        re.IGNORECASE
    )

    for line in body_lines:
        # Treat short lines (< 65 chars) ending without period as potential headings
        is_heading = (
            len(line) < 65
            and not line.endswith('.')
            and not line.endswith(',')
            and (heading_pattern.match(line) or line.isupper() or line.istitle())
        )

        if is_heading and len(line) > 3:
            flush_buffer()
            if current_paras or current_heading:
                sections.append((current_heading, current_paras))
            current_heading = line
            current_paras = []
        else:
            buffer.append(line)

    flush_buffer()
    if current_paras or current_heading:
        sections.append((current_heading, current_paras))

    # If no sections were detected, treat entire body as one section
    if not sections:
        all_text = ' '.join(body_lines)
        # Split into ~300 word chunks as paragraphs
        words = all_text.split()
        paras = []
        for i in range(0, len(words), 80):
            paras.append(' '.join(words[i:i+80]))
        sections = [(None, paras)]

    return title, sections

def word_count(sections):
    total = sum(len(p.split()) for _, paras in sections for p in paras)
    minutes = max(1, round(total / 200))
    return f"{minutes} min read"

def make_excerpt(sections, max_words=35):
    for _, paras in sections:
        for p in paras:
            words = p.split()
            if len(words) > 10:
                excerpt = ' '.join(words[:max_words])
                return excerpt + '…'
    return "Read the full story."

def html_escape(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

# ── HTML Generation ─────────────────────────────────────────────────────────────

def generate_post_html(title, sections, slug, date_str, read_time):
    """Generate a complete blog post HTML file."""

    def render_section(heading, paras):
        html = ""
        if heading:
            hid = slugify(heading)
            safe_heading = html_escape(heading)
            html += f'        <h2 class="blog-section-heading" id="{hid}">{safe_heading}</h2>\n\n'
        for p in paras:
            safe_p = html_escape(p)
            html += f'        <p>{safe_p}</p>\n\n'
        return html

    body_html = ""
    for heading, paras in sections:
        body_html += render_section(heading, paras)

    # Build TOC
    toc_items = ""
    for heading, _ in sections:
        if heading:
            hid = slugify(heading)
            safe_h = html_escape(heading)
            toc_items += f'          <li><a href="#{hid}" class="toc-link">{safe_h}</a></li>\n'
    if not toc_items:
        toc_items = f'          <li><a href="#content" class="toc-link">Story</a></li>\n'

    safe_title = html_escape(title)

    return f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{safe_title} — Padmashri R</title>
    <meta name="description" content="{safe_title} — a personal journal by Padmashri R." />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet" />
    <link rel="stylesheet" href="../style.css" />
    <style>
      .blog-post-hero {{
        background: var(--ivory-light);
        padding: 140px 0 60px;
        border-bottom: 1px solid var(--border);
      }}
      .blog-post-hero .container {{ max-width: 760px; }}
      .blog-back-link {{
        display: inline-flex; align-items: center; gap: 0.4rem;
        font-size: 0.8rem; font-family: var(--font-sans); font-weight: 500;
        color: var(--slate-light); text-decoration: none;
        letter-spacing: 0.05em; text-transform: uppercase; margin-bottom: 2rem;
        transition: color var(--transition);
      }}
      .blog-back-link:hover {{ color: var(--clay); }}
      .blog-back-link:hover svg {{ transform: translateX(-3px); }}
      .blog-back-link svg {{ transition: transform var(--transition); }}
      .blog-post-category {{
        display: inline-block; font-size: 0.7rem; font-family: var(--font-sans);
        font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase;
        color: var(--clay); background: rgba(217,119,87,0.1);
        padding: 0.3rem 0.75rem; border-radius: 50px; margin-bottom: 1.25rem;
      }}
      .blog-post-title {{
        font-family: var(--font-serif); font-size: clamp(2.2rem, 5vw, 3.6rem);
        font-weight: 600; color: var(--slate-dark); line-height: 1.15; margin: 0 0 1.25rem;
      }}
      .blog-post-meta {{
        display: flex; align-items: center; gap: 1.5rem; flex-wrap: wrap;
        font-family: var(--font-sans); font-size: 0.85rem; color: var(--slate-light);
        border-top: 1px solid var(--border); padding-top: 1.25rem; margin-top: 1.25rem;
      }}
      .blog-meta-item {{ display: flex; align-items: center; gap: 0.4rem; }}
      .blog-meta-item svg {{ opacity: 0.6; }}
      .blog-post-layout {{
        display: grid; grid-template-columns: 1fr 240px; gap: 4rem;
        max-width: 1040px; margin: 0 auto; padding: 4rem 2rem 6rem;
      }}
      .blog-post-body {{ min-width: 0; }}
      .blog-section-heading {{
        font-family: var(--font-serif); font-size: 1.6rem; font-weight: 600;
        color: var(--slate-dark); margin: 3rem 0 1rem; padding-top: 2rem;
        border-top: 2px solid var(--border); position: relative;
      }}
      .blog-section-heading::before {{
        content: ''; position: absolute; top: -2px; left: 0;
        width: 48px; height: 2px; background: var(--clay);
      }}
      .blog-post-body p {{
        font-family: var(--font-sans); font-size: 1.05rem; line-height: 1.85;
        color: var(--slate-medium); margin: 0 0 1.4rem;
      }}
      .blog-post-body p:first-of-type {{ font-size: 1.15rem; color: var(--slate-dark); }}
      .blog-post-sidebar {{
        position: sticky; top: 100px; align-self: start;
        padding: 1.5rem; background: var(--ivory-medium);
        border-radius: 12px; border: 1px solid var(--border);
      }}
      .toc-label {{
        font-family: var(--font-sans); font-size: 0.7rem; font-weight: 600;
        letter-spacing: 0.12em; text-transform: uppercase;
        color: var(--slate-light); margin: 0 0 1rem;
      }}
      .toc-list {{ list-style: none; padding: 0; margin: 0; }}
      .toc-list li + li {{ margin-top: 0.4rem; }}
      .toc-list a {{
        font-family: var(--font-sans); font-size: 0.85rem; color: var(--slate-light);
        text-decoration: none; display: block; padding: 0.35rem 0.75rem;
        border-radius: 6px; border-left: 2px solid transparent; transition: all var(--transition);
      }}
      .toc-list a:hover, .toc-list a.active {{
        color: var(--clay); border-left-color: var(--clay); background: rgba(217,119,87,0.06);
      }}
      .back-to-top {{
        position: fixed; bottom: 2rem; right: 2rem; width: 46px; height: 46px;
        background: var(--slate-dark); color: white; border: none; border-radius: 50%;
        cursor: pointer; display: flex; align-items: center; justify-content: center;
        opacity: 0; transform: translateY(10px); transition: all 0.3s;
        pointer-events: none; z-index: 100;
      }}
      .back-to-top.visible {{ opacity: 1; transform: translateY(0); pointer-events: all; }}
      .back-to-top:hover {{ background: var(--clay); }}
      @media (max-width: 900px) {{
        .blog-post-layout {{ grid-template-columns: 1fr; gap: 2rem; padding: 3rem 1.5rem 5rem; }}
        .blog-post-sidebar {{ position: static; order: -1; }}
      }}
      @media (max-width: 600px) {{
        .blog-post-hero {{ padding: 120px 0 40px; }}
        .blog-post-title {{ font-size: 2rem; }}
        .blog-post-layout {{ padding: 2rem 1rem 4rem; }}
      }}
    </style>
  </head>
  <body>
    <nav class="nav" id="main-nav">
      <div class="nav-inner">
        <div class="nav-logo">PR</div>
        <ul class="nav-links" id="nav-links">
          <li><a href="../blog-only.html#posts" class="nav-link">All Posts</a></li>
        </ul>
        <button class="hamburger" id="hamburger" aria-label="Toggle menu">
          <span></span><span></span><span></span>
        </button>
      </div>
    </nav>

    <header class="blog-post-hero">
      <div class="container">
        <a href="../blog-only.html" class="blog-back-link">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M19 12H5M12 5l-7 7 7 7"/>
          </svg>
          Back to Blog
        </a>
        <div class="blog-post-category">Journal</div>
        <h1 class="blog-post-title">{safe_title}</h1>
        <div class="blog-post-meta">
          <div class="blog-meta-item">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>
            </svg>
            {date_str}
          </div>
          <div class="blog-meta-item">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>
            </svg>
            {read_time}
          </div>
          <div class="blog-meta-item">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>
            </svg>
            Padmashri R
          </div>
        </div>
      </div>
    </header>

    <div class="blog-post-layout">
      <article class="blog-post-body" id="content">
{body_html}
      </article>
      <aside class="blog-post-sidebar">
        <p class="toc-label">Table of Contents</p>
        <ul class="toc-list">
{toc_items}
        </ul>
      </aside>
    </div>

    <footer class="footer">
      <div class="container">
        <div class="footer-inner">
          <div class="footer-logo">PR</div>
          <p class="footer-copy">© {datetime.now().year} Padmashri R. All rights reserved.</p>
          <nav class="footer-nav">
            <a href="../blog-only.html#posts">All Posts</a>
          </nav>
        </div>
      </div>
    </footer>

    <button class="back-to-top" id="back-to-top" aria-label="Back to top">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 19V5M5 12l7-7 7 7"/>
      </svg>
    </button>

    <script>
      const nav = document.getElementById('main-nav');
      window.addEventListener('scroll', () => {{
        nav.classList.toggle('scrolled', window.scrollY > 40);
        document.getElementById('back-to-top').classList.toggle('visible', window.scrollY > 400);
      }});
      const hamburger = document.getElementById('hamburger');
      const navLinks = document.getElementById('nav-links');
      hamburger.addEventListener('click', () => {{
        hamburger.classList.toggle('open');
        navLinks.classList.toggle('open');
      }});
      navLinks.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {{
        hamburger.classList.remove('open');
        navLinks.classList.remove('open');
      }}));
      document.getElementById('back-to-top').addEventListener('click', () => window.scrollTo({{top:0,behavior:'smooth'}}));
      const headings = document.querySelectorAll('.blog-section-heading');
      const tocLinks = document.querySelectorAll('.toc-link');
      const observer = new IntersectionObserver(entries => {{
        entries.forEach(e => {{
          if (e.isIntersecting) {{
            tocLinks.forEach(l => l.classList.remove('active'));
            const a = document.querySelector(`.toc-link[href="#${{e.target.id}}"]`);
            if (a) a.classList.add('active');
          }}
        }});
      }}, {{rootMargin: '-20% 0px -60% 0px'}});
      headings.forEach(h => observer.observe(h));
    </script>
  </body>
</html>
'''

# ── Update blog-only.html ───────────────────────────────────────────────────────

def add_card_to_blog(title, slug, excerpt, date_str, blog_html_path="blog-only.html"):
    """Insert a new blog card into blog-only.html before the placeholder card."""
    safe_title = html_escape(title)
    safe_excerpt = html_escape(excerpt)
    month_year = datetime.now().strftime("%B %Y")

    new_card = f'''
          <!-- Auto-generated: {safe_title} -->
          <article class="blog-card reveal">
            <div class="blog-card-inner">
              <div class="blog-card-top">
                <span class="blog-card-tag">Journal</span>
                <span class="blog-card-date">{month_year}</span>
              </div>
              <h3 class="blog-card-title">{safe_title}</h3>
              <p class="blog-card-excerpt">{safe_excerpt}</p>
              <div class="blog-card-footer">
                <a href="blogs/{slug}.html" class="blog-card-link">
                  Read Story
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M5 12h14M12 5l7 7-7 7"/>
                  </svg>
                </a>
              </div>
            </div>
          </article>
'''

    content = open(blog_html_path, 'r', encoding='utf-8').read()

    # Insert before the placeholder "Coming Soon" card
    placeholder_marker = '<!-- Placeholder: Future Post -->'
    if placeholder_marker in content:
        content = content.replace(placeholder_marker, new_card + '\n          ' + placeholder_marker)
    else:
        # Fallback: insert before closing </div> of blog-posts-grid
        content = content.replace('        </div>\n      </div>\n    </section>', 
                                   new_card + '        </div>\n      </div>\n    </section>', 1)

    open(blog_html_path, 'w', encoding='utf-8').write(content)

# ── Main ────────────────────────────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nERROR: Please provide a file path.")
        print("Example: python publish_blog.py \"My Journal.pdf\"")
        sys.exit(1)

    filepath = sys.argv[1]
    if not os.path.exists(filepath):
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)

    filename = Path(filepath).stem
    print(f"\n📄 Reading: {filepath}")

    # 1. Extract text
    raw_text = extract_text(filepath)
    print(f"   Extracted {len(raw_text)} characters of text")

    # 2. Parse into sections
    title, sections = parse_sections(raw_text)
    print(f"   Title detected: '{title}'")
    print(f"   Sections found: {len(sections)}")

    # 3. Generate metadata
    slug = slugify(title)
    date_str = datetime.now().strftime("%B %d, %Y")
    read_time = word_count(sections)
    excerpt = make_excerpt(sections)

    print(f"   Slug: {slug}")
    print(f"   Read time: {read_time}")

    # 4. Generate blog post HTML
    os.makedirs("blogs", exist_ok=True)
    post_path = f"blogs/{slug}.html"
    html = generate_post_html(title, sections, slug, date_str, read_time)
    open(post_path, 'w', encoding='utf-8').write(html)
    print(f"\n✅ Blog post created: {post_path}")

    # 5. Update blog-only.html
    add_card_to_blog(title, slug, excerpt, date_str)
    print(f"✅ Card added to blog-only.html")

    # 6. Open in Chrome
    abs_path = os.path.abspath(post_path)
    blog_abs = os.path.abspath("blog-only.html")
    url_post = f"file:///{abs_path.replace(os.sep, '/')}"
    url_blog = f"file:///{blog_abs.replace(os.sep, '/')}"

    print(f"\n🌐 Opening in Chrome...")
    try:
        # Windows: use Start-Process
        subprocess.Popen(
            ['powershell', '-Command',
             f'Start-Process chrome --ArgumentList "--new-window","{url_blog}","{url_post}"'],
            shell=True
        )
    except Exception:
        print(f"  (Open manually: {url_blog})")

    print("\n🎉 Done!")
    print(f"   Post page : {post_path}")
    print(f"   Blog index: blog-only.html")
    print(f"\n⚠️  Quick review tips:")
    print(f"   - Check section headings look right in the post")
    print(f"   - Adjust the card excerpt in blog-only.html if needed")
    print(f"   - The TOC auto-generates from detected headings")

if __name__ == "__main__":
    main()
