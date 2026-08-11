# Daily Review Image System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the first usable version of the daily review HTML/PNG generation pipeline.

**Architecture:** Keep the pipeline file-based and reproducible: a daily JSON file is validated and rendered into a standalone dark-theme HTML page, then Playwright captures the full page as a vertical PNG. Markdown remains the long-form source of truth for Obsidian, while JSON powers the visual components.

**Tech Stack:** Python 3 standard library for validation/rendering, standalone HTML/CSS template, Node.js Playwright for full-page screenshots.

## Global Constraints

- Daily review reports default to HTML and PNG, not PDF.
- HTML output path: `output/html/`.
- PNG output path: `output/images/`.
- Daily structured data path: `data/daily/YYYY-MM-DD-market.json`.
- Template path: `templates/daily-review-dark.html`.
- Generated output must include: title, date, key metric cards, market review, theme review, holding/trade review, next-day plan, risk notice.
- A 股 colors: red means up/positive, green means down/risk.
- Missing account or trade data must be marked as `未提供`, never guessed.
- Bottom risk notice must include: `仅作个人复盘与交易计划，不构成投资建议。`
- Do not edit historical PDFs or temporary PDF scripts.

---

## File Structure

- Create `data/daily/README.md`: explains how to fill daily JSON files.
- Create `data/daily/sample-market.json`: sample input used by tests and local validation.
- Create `templates/daily-review-dark.html`: standalone HTML template with placeholders.
- Create `scripts/render_daily_review.py`: validates JSON, renders HTML, prints output path.
- Create `scripts/screenshot_daily_review.js`: captures a full-page PNG from rendered HTML.
- Create `scripts/verify_daily_review_html.js`: checks required DOM elements and overflow basics.
- Create `output/images/.gitkeep`: keeps the image output directory in git.
- Modify `docs/daily-review-image-system.md`: add implementation command references.

## Task 1: Daily JSON Contract

**Files:**
- Create: `data/daily/README.md`
- Create: `data/daily/sample-market.json`

**Interfaces:**
- Produces: JSON fields consumed by `scripts/render_daily_review.py`: `date`, `title`, `tags`, `summary`, `metrics`, `market_review`, `themes`, `stocks`, `account`, `trades`, `holdings`, `next_day_plan`, `discipline`, `risk_notice`.

- [ ] **Step 1: Create sample JSON**

Create `data/daily/sample-market.json` with realistic sample data and explicit `未提供` fields for optional account/trade data.

- [ ] **Step 2: Document data entry rules**

Create `data/daily/README.md` explaining required fields, optional fields, and where each data type should come from.

- [ ] **Step 3: Verify JSON parses**

Run: `python3 -m json.tool data/daily/sample-market.json`
Expected: exit code 0 and formatted JSON output.

## Task 2: HTML Template

**Files:**
- Create: `templates/daily-review-dark.html`

**Interfaces:**
- Consumes: placeholder tokens rendered by Python: `{{title}}`, `{{date}}`, `{{tags}}`, `{{summary}}`, `{{metric_cards}}`, `{{market_sections}}`, `{{theme_rows}}`, `{{stock_rows}}`, `{{account_panel}}`, `{{trade_rows}}`, `{{holding_rows}}`, `{{next_day_plan}}`, `{{discipline_items}}`, `{{risk_notice}}`.
- Produces: standalone HTML that can be opened directly from disk.

- [ ] **Step 1: Create dark HTML skeleton**

Build a single-file HTML template with CSS variables, responsive wrapper, metric cards, tables, panels, and footer risk notice.

- [ ] **Step 2: Add responsive table handling**

Tables must use fixed layout, word wrapping, and mobile-friendly font sizes. The body must prevent horizontal overflow.

- [ ] **Step 3: Add required element markers**

Include stable markers for verification: `[data-review-root]`, `[data-required="risk-notice"]`, `[data-required="metrics"]`, `[data-required="next-day-plan"]`.

## Task 3: Python Renderer

**Files:**
- Create: `scripts/render_daily_review.py`

**Interfaces:**
- Consumes: `python3 scripts/render_daily_review.py data/daily/sample-market.json`
- Produces: `output/html/<date>-<safe-title>.html`
- Functions:
  - `load_review(path: Path) -> dict`
  - `validate_review(data: dict) -> list[str]`
  - `render_review(data: dict, template: str) -> str`
  - `write_html(data: dict, html: str) -> Path`

- [ ] **Step 1: Implement validation**

Validate required fields and require risk notice to contain the standard investment disclaimer.

- [ ] **Step 2: Implement escaping and render helpers**

Escape HTML with `html.escape`. Render tags, cards, lists, tables, and missing values consistently.

- [ ] **Step 3: Implement CLI**

The command prints the generated HTML path. If validation fails, print each error and exit with code 1.

- [ ] **Step 4: Render sample**

Run: `python3 scripts/render_daily_review.py data/daily/sample-market.json`
Expected: exit code 0 and one HTML file in `output/html/`.

## Task 4: Screenshot and HTML Verification

**Files:**
- Create: `scripts/screenshot_daily_review.js`
- Create: `scripts/verify_daily_review_html.js`
- Create: `output/images/.gitkeep`

**Interfaces:**
- Screenshot command: `node scripts/screenshot_daily_review.js output/html/<file>.html`
- Verify command: `node scripts/verify_daily_review_html.js output/html/<file>.html`
- Produces: `output/images/<same-name>.png`

- [ ] **Step 1: Implement screenshot script**

Use Playwright Chromium, load a local file URL, wait for network idle, compute full document height, and capture `fullPage: true`.

- [ ] **Step 2: Implement verification script**

Check required markers exist, body scroll width does not exceed viewport width by more than 2px at 430px and 1180px, and risk notice text exists.

- [ ] **Step 3: Verify rendered HTML**

Run: `node scripts/verify_daily_review_html.js output/html/<file>.html`
Expected: exit code 0.

- [ ] **Step 4: Capture PNG**

Run: `node scripts/screenshot_daily_review.js output/html/<file>.html`
Expected: exit code 0 and PNG path printed.

## Task 5: Documentation Wiring

**Files:**
- Modify: `docs/daily-review-image-system.md`

**Interfaces:**
- Consumes: commands created in Tasks 3 and 4.
- Produces: documented daily execution sequence.

- [ ] **Step 1: Add command examples**

Document how to render HTML, verify HTML, and capture PNG.

- [ ] **Step 2: Add first-stage limitation**

State that account/trade data remain manually confirmed, and automated market data ingestion is a later phase.

- [ ] **Step 3: Self-review**

Run a placeholder scan over the plan, documentation, template, and scripts.
Expected: no output.

## Task 6: Final Verification and Commit

**Files:**
- All created and modified files from Tasks 1-5.

**Interfaces:**
- Verification commands:
  - `python3 -m json.tool data/daily/sample-market.json`
  - `python3 scripts/render_daily_review.py data/daily/sample-market.json`
  - `node scripts/verify_daily_review_html.js output/html/<file>.html`
  - `node scripts/screenshot_daily_review.js output/html/<file>.html`
  - `git status --short`

- [ ] **Step 1: Run full verification**

Run all commands above using the actual generated HTML file path.

- [ ] **Step 2: Inspect changed files**

Run `git status --short` and confirm only this task's files are staged.

- [ ] **Step 3: Commit**

Commit message: `实现每日复盘HTML长图生成基础链路`

- [ ] **Step 4: Push**

Run `git push`.
