# Strateo Audit Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the UX/accessibility and SEO/GEO recommendations in `audit/REVIEW.md` and `audit/SEO-GEO-REVIEW.md` across the production static site.

**Architecture:** Preserve the dependency-free static site and its existing visual language. Expand it into a small multi-page site built from plain HTML with shared `styles.css`, `script.js`, and assets; add crawler files and JSON-LD; use a Python standard-library acceptance suite to prevent metadata, content, accessibility, and linking regressions.

**Tech Stack:** HTML5, CSS, browser JavaScript, Python 3 `unittest`, Vercel static hosting.

## Global Constraints

- Keep the canonical production origin exactly `https://www.strateo.com.br`.
- Do not invent client names, case-study outcomes, leadership facts, telephone numbers, CNPJ details, certifications, ratings, regulatory relationships, or social-profile URLs.
- Preserve the existing Strateo petroleum/cream visual system, wordmark, typographic hierarchy, and responsive behavior.
- Use `OAI-SearchBot` for ChatGPT Search crawl intent; do not make a `GPTBot` training-policy decision.
- Keep every public claim visible in page content consistent with structured data.
- Do not add a framework, package manager, build system, analytics identifier, or third-party form service.
- Never add Codex attribution to commits.

---

### Task 1: Acceptance test harness

**Files:**
- Create: `tests/test_site.py`
- Test: `tests/test_site.py`

**Interfaces:**
- Consumes: public HTML files, `robots.txt`, `sitemap.xml`, and shared assets.
- Produces: `python3 -m unittest discover -s tests -v` as the repository-wide acceptance command.

- [ ] **Step 1: Write failing metadata and crawler tests**

Create a standard-library test module that parses every expected page and asserts: `pt-BR`, one H1, unique title/description, absolute self-canonical, Open Graph/X metadata, JSON-LD on the homepage, `robots.txt` OAI access, and a sitemap URL for every public page.

```python
PUBLIC_PATHS = {
    "": "index.html",
    "consultoria-de-processos-e-gestao": "consultoria-de-processos-e-gestao/index.html",
    "automacao-com-ia": "automacao-com-ia/index.html",
    "escritorios-de-investimento": "escritorios-de-investimento/index.html",
    "mercado-financeiro-e-capitais": "mercado-financeiro-e-capitais/index.html",
    "industria-agro-construcao": "industria-agro-construcao/index.html",
    "negocios-familiares": "negocios-familiares/index.html",
    "sobre": "sobre/index.html",
    "contato": "contato/index.html",
}
```

- [ ] **Step 2: Write failing UX/accessibility/content tests**

Assert the homepage has a skip link, mobile-menu button with `aria-expanded` and `aria-controls`, navigation links to the focused pages, no known typo, no misleading “Resultados” navigation, a visible email address, a prefilled email CTA labelled as email, answer-first FAQ content, and no unsupported case/client claims.

- [ ] **Step 3: Run tests to verify RED**

Run: `python3 -m unittest discover -s tests -v`

Expected: failures for missing pages, crawler files, metadata, structured data, mobile navigation, and revised content.

- [ ] **Step 4: Commit tests**

```bash
git add tests/test_site.py docs/superpowers/plans/2026-07-12-strateo-audit-implementation.md
git commit -m "test: define site audit acceptance criteria"
```

### Task 2: Technical SEO and entity foundation

**Files:**
- Modify: `index.html`
- Create: `robots.txt`
- Create: `sitemap.xml`
- Create: `assets/strateo-social-card.png`
- Test: `tests/test_site.py`

**Interfaces:**
- Consumes: canonical origin and current public company name, email, address, logo, and service description.
- Produces: crawlable homepage metadata, `Organization` JSON-LD, explicit crawler policy, sitemap, and social-preview asset.

- [ ] **Step 1: Add homepage metadata and JSON-LD**

Use the title `Strateo | Estratégia, processos e automação com IA`, a concrete consulting description, canonical URL, `robots=index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1`, Open Graph tags, X summary-large-image tags, and one `Organization` JSON-LD object containing only the visible legal name, email, canonical URL, logo, description, and Goiânia postal address.

- [ ] **Step 2: Add crawler files**

Create `robots.txt` with these exact controls:

```text
User-agent: *
Allow: /

User-agent: OAI-SearchBot
Allow: /

Sitemap: https://www.strateo.com.br/sitemap.xml
```

Create a valid XML sitemap using only canonical URLs defined in `PUBLIC_PATHS` and one `<lastmod>2026-07-12</lastmod>` per URL.

- [ ] **Step 3: Add the social card**

Create a 1200×630 brand-consistent image named `assets/strateo-social-card.png` and wire its absolute production URL into Open Graph and X metadata.

- [ ] **Step 4: Run targeted tests**

Run: `python3 -m unittest tests.test_site.MetadataTests tests.test_site.CrawlerTests -v`

Expected: metadata and crawler tests pass; page-set tests still fail until Task 4.

- [ ] **Step 5: Commit the technical foundation**

```bash
git add index.html robots.txt sitemap.xml assets/strateo-social-card.png
git commit -m "feat: add search discovery foundation"
```

### Task 3: Homepage UX, accessibility, and GEO content

**Files:**
- Modify: `index.html`
- Modify: `styles.css`
- Modify: `script.js`
- Test: `tests/test_site.py`

**Interfaces:**
- Consumes: existing design tokens and the page URLs in `PUBLIC_PATHS`.
- Produces: accessible responsive navigation, accurate contact actions, principles naming, focused internal links, and visible answer-first content.

- [ ] **Step 1: Implement accessible navigation**

Add a visible-on-focus skip link to `#conteudo`, give `<main>` that ID, add a mobile menu button with `aria-expanded="false"` and `aria-controls="navegacao-principal"`, keep the navigation available at every viewport, and link it to `/#metodo`, `/#para-quem`, `/#principios`, `/sobre/`, and `/contato/`.

- [ ] **Step 2: Implement menu behavior**

In `script.js`, toggle the header's `data-menu-open` attribute and button `aria-expanded`; close on navigation click, `Escape`, and resize above 760 px; return focus to the button after Escape.

- [ ] **Step 3: Correct conversion and content mismatches**

Rename “Resultados” to “Princípios”, fix `com, processo`, replace ambiguous/mixed badges and wording with consistent Portuguese, label mail CTAs “Enviar e-mail”, use a prefilled `mailto:` subject/body, show `contato@strateo.com.br` as visible linked text, and change header/hero conversion copy to “Falar com a Strateo”.

- [ ] **Step 4: Add answer-first and internal-link content**

Add a concise “O que a Strateo faz” introduction, a linked services section, and a visible questions section answering what the company does, who it serves, how diagnosis works, when to automate with AI, and how to improve controls without unnecessary bureaucracy.

- [ ] **Step 5: Fix visual accessibility and performance**

Use a 4.5:1-or-better text color for 11 px method indices, preserve a contrasting inverse-section index color, keep 44 px interactive targets, style the mobile menu and subpage components, and reduce the Google Fonts request to used families/weights.

- [ ] **Step 6: Run UX/content tests**

Run: `python3 -m unittest tests.test_site.HomepageExperienceTests -v`

Expected: all homepage experience tests pass.

- [ ] **Step 7: Commit the homepage upgrade**

```bash
git add index.html styles.css script.js
git commit -m "feat: improve homepage clarity and accessibility"
```

### Task 4: Focused service, audience, About, and Contact pages

**Files:**
- Create: `consultoria-de-processos-e-gestao/index.html`
- Create: `automacao-com-ia/index.html`
- Create: `escritorios-de-investimento/index.html`
- Create: `mercado-financeiro-e-capitais/index.html`
- Create: `industria-agro-construcao/index.html`
- Create: `negocios-familiares/index.html`
- Create: `sobre/index.html`
- Create: `contato/index.html`
- Modify: `styles.css`
- Test: `tests/test_site.py`

**Interfaces:**
- Consumes: shared header/footer structure, canonical origin, public company facts, and homepage claims.
- Produces: nine total focused, internally linked, canonical public URLs without unsupported evidence.

- [ ] **Step 1: Create the process-consulting and AI-automation pages**

Each page must include a unique title/description/H1, direct definition, intended audience, concrete deliverables, four-step engagement flow, limitations/suitability language, contextual links, and the same visible email/contact action.

- [ ] **Step 2: Create four audience pages**

Expand only the claims already present on the homepage. Use precise Portuguese headings and paragraphs for investment offices, financial/capital markets, industry/agro/construction, and family businesses. Do not claim clients, results, certifications, or regulatory endorsements.

- [ ] **Step 3: Create About and Contact pages**

The About page must identify Strateo Serviços Empresariais Ltda., the public service model, Goiânia address, audiences, and operating principles without naming unverified people. The Contact page must display the email and address, explain what information to include, and use the same prefilled email CTA.

- [ ] **Step 4: Add shared subpage styling**

Add reusable classes for compact hero, breadcrumbs, prose sections, definition callouts, deliverable grids, question blocks, related links, and final CTA while preserving the current tokens and responsive breakpoints.

- [ ] **Step 5: Run full acceptance suite**

Run: `python3 -m unittest discover -s tests -v`

Expected: all tests pass.

- [ ] **Step 6: Commit focused pages**

```bash
git add consultoria-de-processos-e-gestao automacao-com-ia escritorios-de-investimento mercado-financeiro-e-capitais industria-agro-construcao negocios-familiares sobre contato styles.css sitemap.xml
git commit -m "feat: add focused service and audience pages"
```

### Task 5: Automated and rendered verification

**Files:**
- Modify if needed: any file above
- Create: `audit/IMPLEMENTATION-VERIFICATION.md`

**Interfaces:**
- Consumes: completed public site and acceptance suite.
- Produces: requirement-by-requirement proof, accepted desktop/mobile screenshots, and production-readiness handoff.

- [ ] **Step 1: Run automated verification**

Run:

```bash
python3 -m unittest discover -s tests -v
python3 -m http.server 4174
```

Confirm HTML pages, CSS, JavaScript, crawler files, sitemap XML, JSON-LD JSON, public internal links, and image assets all load without errors.

- [ ] **Step 2: Perform browser QA**

At desktop, 390×844, and 320×720, verify the homepage, mobile menu open/close/Escape behavior, every navigation target, homepage sections, one service page, About, and Contact. Confirm no horizontal overflow, no clipped headings, and visible focus treatment.

- [ ] **Step 3: Recheck external crawler behavior if deployed**

After deployment, verify `200` responses for the homepage as Googlebot and OAI-SearchBot, plus valid `robots.txt` and `sitemap.xml`. If deployment is outside the current task's available credentials, document the exact remaining production checks without claiming them complete.

- [ ] **Step 4: Record completion evidence**

Create `audit/IMPLEMENTATION-VERIFICATION.md` mapping every finding in both audit files to `implemented`, `safely substituted`, `external follow-up`, or `not applicable`, with file/test/browser evidence.

- [ ] **Step 5: Run final hygiene checks**

Run:

```bash
git diff --check
git status --short
```

Expected: no whitespace errors; only intentional files are changed or untracked.

- [ ] **Step 6: Commit verification artifacts**

```bash
git add audit/REVIEW.md audit/SEO-GEO-REVIEW.md audit/IMPLEMENTATION-VERIFICATION.md tests
git commit -m "docs: record site audit verification"
```
