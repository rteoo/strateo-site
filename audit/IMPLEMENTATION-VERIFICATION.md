# Audit implementation verification

Implementation date: 2026-07-18. Branch: `feat/seo-ux-audit`.

Maps every finding from `audit/REVIEW.md` and `audit/SEO-GEO-REVIEW.md` to one of:
**implemented** · **safely substituted** · **external follow-up** · **not applicable**.

Acceptance command (all 20 tests pass): `python3 -m unittest discover -s tests -v`

## UX / accessibility findings (REVIEW.md)

| Finding | Status | Evidence |
| --- | --- | --- |
| Mobile header removes primary navigation | implemented | Accessible menu button (`aria-expanded`, `aria-controls="navegacao-principal"`), sticky mobile header, dropdown panel. Browser-verified: open/close, close on nav click, close on `Escape` with focus returned to the button. `test_mobile_menu_button_is_accessible`. |
| Scheduling CTA promises what it can't deliver | implemented | Conversion copy is now "Falar com a Strateo" (anchors to contact); the mail action is labelled "Enviar e-mail" with a prefilled subject/body. `test_email_is_visible_and_prefilled`. |
| “Resultados” holds principles, not results | implemented | Renamed to “Princípios” in nav, footer and section id (`#principios`). `test_principles_replace_results`. |
| Typo “cadência comercial com, processo” | implemented | Corrected on the homepage and expanded pages. `test_no_known_typo`. |
| Ambiguous “AI · MFO” badge / mixed-language copy | implemented | Badges: “Assessoria · MFO”, “Gestão do fundador”; “asset e wealth” → “gestoras de recursos e de patrimônio”. `test_language_is_consistent_portuguese`. |
| Missing skip link | implemented | `.skip-link` → `#conteudo` (`<main id="conteudo">`), visible on focus. `test_skip_link_and_main_target`. |
| 11px method numbers at 3.06:1 contrast | implemented | Already fixed in PR #2 (rebrand): `--petroleum-500` at 13px on white. |
| No canonical / social-preview metadata | implemented | See SEO section below. |
| Email not visible as text | implemented | `contato@strateo.com.br` shown as linked text in the contact card and Contact page. |
| Manual keyboard pass / screen-reader conformance | external follow-up | Focus styles and menu focus return verified programmatically; a human keyboard + screen-reader pass is still recommended. |

## SEO / GEO findings (SEO-GEO-REVIEW.md)

| Finding | Status | Evidence |
| --- | --- | --- |
| No HTML canonical | implemented | Absolute self-canonical on all 9 pages. `test_canonical_and_robots_meta`. |
| `robots.txt` / `sitemap.xml` return 404 | implemented | Both created; robots allows `*` and `OAI-SearchBot`, declares the sitemap; sitemap lists all 9 canonical URLs with `lastmod`. `CrawlerTests`. |
| Abstract title/description | implemented | `Strateo | Estratégia, processos e automação com IA` + concrete consulting description; plain-language "what Strateo is" sentence in the new services section. |
| No structured data | implemented | One `Organization` JSON-LD block on the homepage limited to visible verified facts (name, legal name, URL, logo, description, email, Goiânia address). `test_homepage_organization_jsonld`. |
| Phone, CNPJ, leadership, `sameAs` in JSON-LD | safely substituted | Deliberately omitted — not approved/verified for publication. The test suite asserts these fields stay absent. |
| No About page / entity authority | implemented | `/sobre/` identifies the company, legal name, model, principles, address and founder (name only, no credential claims). |
| Single URL covers all topics | implemented | 8 focused pages: 2 services, 4 audiences, About, Contact — each with unique metadata, one H1, internal links and the email CTA. `SubpageTests`. |
| `/casos/` page | safely substituted | Not created: no disclosable case evidence exists yet; publishing thin or invented cases is worse than absence. Add when real, authorized cases exist. |
| Citable proof (cases, quantified outcomes) | external follow-up | Requires real client outcomes approved for disclosure. |
| Answer-first GEO content | implemented | Homepage “Perguntas diretas” section (6 answer-first Q&As with deep links); criteria/limitations sections on service pages. `test_answer_first_content`. |
| OG / X cards + 1200×630 image | implemented | Full OG/X metadata on all pages; purpose-built `assets/strateo-social-card.png` (1200×630, brand tokens). `test_social_metadata`. |
| Visible email / phone or booking destination | implemented (email) / external follow-up (phone·booking) | Email visible and linked; no verified phone or booking tool exists to publish. |
| Reduce Google Fonts payload | implemented | Import trimmed to the weights actually used (Schibsted 500–600, Hanken 400–600, Spline Mono 400–600). Self-hosting subsets remains optional follow-up. |
| Analytics, `utm_source=chatgpt.com` tracking | external follow-up | Plan constraint: no analytics identifiers added by this work. |
| Search Console / Bing / Google Business Profile | external follow-up | Requires account owner access: verify properties, submit `sitemap.xml`, request indexing, align GBP. |
| `llms.txt` / “AI schema” / keyword pages | not applicable | Explicitly de-prioritized by the audit itself. |

## Remaining production checks (after deploy)

Not claimable from this environment — run after the branch deploys to `https://www.strateo.com.br`:

1. `200` for `/` as Googlebot and as OAI-SearchBot (`curl -A`).
2. `robots.txt` and `sitemap.xml` return the committed content (no 404).
3. Validate JSON-LD in Google's Rich Results test; validate canonicals.
4. Search Console + Bing: verify, submit sitemap, request indexing of `/`.
5. Confirm the social card renders in a share preview (WhatsApp/LinkedIn/X).

## Verification evidence (local)

- `python3 -m unittest discover -s tests -v` → 20 tests, all pass.
- HTTP sweep via `python3 -m http.server 4174`: all 9 pages + robots, sitemap, CSS, JS and 4 image assets return `200`; sitemap parses as valid XML.
- Browser QA: desktop (1280), 400 and 320 widths — no horizontal overflow (`scrollWidth == innerWidth` on homepage, service page, About); menu behavior verified; header `data-scrolled` and reveal observer working; skip link appears on focus.
