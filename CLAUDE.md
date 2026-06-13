# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

MkDocs Material documentation site for a mathematical textbook. Content uses LaTeX (MathJax)
and includes Python example scripts. Three specialized review/write agents live in `agents/`;
their full instructions are in `agents/SKILL.md`.

## Build Commands

```bash
mkdocs serve          # local dev with live reload
mkdocs build          # build static site
mkdocs build --strict # used in CI — all warnings are errors
pip install -r requirements.txt
```

## Deployment

GitHub Actions (`.github/workflows/deploy-mkdocs.yml`) auto-deploys to GitHub Pages on push
to `main`. Build uses `--strict` mode.

## Repository Structure

```
book_name/
├── CLAUDE.md
├── README.md
├── mkdocs.yml
├── requirements.txt
├── agents/
│   ├── SKILL.md            ← agent orchestration hub (read this first)
│   ├── MATH_REVIEWER.md
│   ├── WRITING_REVIEWER.md
│   └── WRITER.md
├── .github/workflows/deploy-mkdocs.yml
└── docs/
    ├── index.md
    ├── assets/favicon.ico
    ├── stylesheets/extra.css
    ├── javascripts/mathjax.js
    └── chapter_name/
        ├── index.md
        └── section_name/
            ├── topic.md
            ├── topic.py
            ├── module/__init__.py
            └── figures/
```

## Agent Commands (Quick Reference)

> Full command semantics, file conventions, and agent prompts: **read `agents/SKILL.md` first**.

| Command | What it does |
|---|---|
| `review <file\|folder\|all>` | Freeze vN snapshot, run both reviewers, print to stdout. No writes. |
| `write <file\|folder\|all> [if score < N]` | Requires prior `review`. Runs reviewers in-memory, writes improved file, updates score. |
| `update <file\|folder\|all> [if score < N]` | `review` + `write` in one step. |
| `fetch-pdf <pdf-path> [<target>]` | Extract math problems from a Korean PDF and produce (or extend) MkDocs section files in the benchmark style, with auto-generated figures. |

**Path convention**: paths are relative to `docs/` — omit the `docs/` prefix.

**Execution rules**: sequential only · batch size = 1 · commit after each file.

## File Management

| File | Git | GitHub Pages |
|---|---|---|
| `<name>.md` | ✅ committed | ✅ published |
| `<name>_score.md` | ✅ committed | ❌ excluded via `mkdocs.yml` |
| `<name>_v[0-9]*.md` | ❌ gitignored | ❌ never built |

`.gitignore` entry: `docs/**/*_v[0-9]*.md`

`mkdocs.yml` exclusion:
```yaml
exclude_docs: |
  *_score.md
  *_v[0-9]*.md
```

Commit after `update` — stage only `<name>.md` and `<name>_score.md`:
```bash
git add docs/path/to/<name>.md docs/path/to/<name>_score.md
git commit -m "update: <name>"
```

## Navigation Structure

Nav hierarchy: **Parts → Chapters → Sections → Pages**. Nav entries point to `.md` and `.py`
files only.

```yaml
nav:
  - I Part Title:
    - 1 Chapter Title:
      - Chapter Overview: ch01/index.md
      - 1.1 Section Title:
        - Topic Title: ch01/section_title/topic_title.md
```

YAML quoting: quote any title containing `:`, `#`, `*`, `&`.

## Content Conventions (Summary)

Full MathJax/admonition rules are in `agents/SKILL.md`. Key points:

- `$...$` inline math, `$$...$$` display — always blank lines above and below display math
- No blank lines *inside* `$$...$$` blocks
- No LaTeX in `#` headings (breaks TOC)
- `\$` for currency, never bare `$`
- QED: `$\square$`
- **Korean text after inline math**: insert one space between the closing `$` and the following Hangul character. Example: `$ab = 1$ 일 때` (not `$ab = 1$일 때`), `$v = x$ 이므로` (not `$v = x$이므로`). Does not apply when the next character is punctuation, whitespace, English, or another math expression.
- Every content page ends with `## Exercises` (interleaved solutions, collapsible)
- Python: module docstring · `# ===` dividers · `if __name__ == "__main__":` guard

## Common Tasks

### Add a new section
1. Create `docs/chapter_name/section_name/` with `.md`/`.py` files
2. Add nav entries to `mkdocs.yml` (`.md` and `.py` only)

### Add a new chapter
1. Create `docs/chapter_name/` with `index.md` and section subdirectories
2. Add chapter block to `mkdocs.yml` under the correct Part

### Add a Python example
1. Create `.py` in the relevant section directory
2. Educational style: module docstring, `# ===` dividers, `if __name__ == "__main__":` guard

### Ingest a PDF (`fetch-pdf`)

Convert a Korean math PDF (exam booklet, textbook, etc.) into new MkDocs
section files in the benchmark style. **Full workflow and style requirements:
see `agents/WRITER.md` § "PDF Ingestion Mode".**

Benchmark file used as the style template:
`docs/ch01/integration_by_parts/integration_by_parts.md` (intro → 보기 →
연습문제 with collapsible 풀이, 6–8 figures per topic).

Quick form:

```
fetch-pdf <pdf-path> <target.md>          # create or extend a single section
fetch-pdf <pdf-path>                       # read PDF, propose layout, confirm first
```

Each fetched section produces:

- `docs/<ch>/<section>/<section>.md` (Korean body, ~250–320 lines)
- `docs/<ch>/<section>/figures/<section>_figures.py`
- `docs/<ch>/<section>/figures/*.png` (6–8 PNGs)
- `mkdocs.yml` nav entry added
- Build verified with `mkdocs build --strict`
