# AGENTS.md

Canonical agent contract for this repository — it guides Claude Code, Codex, and any other coding agent. `CLAUDE.md` is a single `@AGENTS.md` import so Claude Code auto-loads these rules; make all edits here, never fork guidance into `CLAUDE.md`.

## Project

Static institutional/marketing website for **Strateo** (Strateo Serviços Empresariais Ltda.), a Brazilian business-consulting brand: a homepage plus eight focused subpages (services, audiences, about, contact). All copy is in Brazilian Portuguese (`<html lang="pt-BR">`). Hand-authored HTML/CSS/JS — **no framework, no build step, no package manager.**

## Stack & Structure

- Plain HTML5 (homepage `index.html` + `<slug>/index.html` subpages sharing header/footer chrome), CSS3 (`styles.css`, design-token system via CSS custom properties), vanilla ES6+ JS (`script.js`: scroll header state, accessible mobile menu, `IntersectionObserver` reveal-on-scroll).
- Fonts load from Google Fonts CDN via `@import` in `styles.css` (Schibsted Grotesk, Hanken Grotesk, Spline Sans Mono) — the site is **not** fully offline; native OS fallback fonts are specified after the web fonts.
- `assets/` holds the v2 brand assets (all PNG): `strateo-wordmark-v2.png` (light surfaces), `strateo-wordmark-v2-reverse.png` (dark surfaces), `strateo-favicon-v2.png`. Canonical sources live in the brand design system (`.../strateo/business/brand/design-system/assets/`) — recapture there, never redraw. Everything is flat at the repo root.

```
index.html                        # homepage
<slug>/index.html                 # 8 subpages: consultoria-de-processos-e-gestao,
                                  # automacao-com-ia, escritorios-de-investimento,
                                  # mercado-financeiro-e-capitais, industria-agro-construcao,
                                  # negocios-familiares, sobre, contato
styles.css                        # all styling + design tokens (shared by every page)
script.js                         # header scroll state + mobile menu + reveal animation
assets/                           # logos, favicon, social card
robots.txt / sitemap.xml          # crawler files (canonical origin https://www.strateo.com.br)
tests/test_site.py                # stdlib acceptance suite (metadata, crawler files, UX)
README.md
```

Homepage section IDs (for nav links/anchors): `#conteudo` (main/skip-link target), `#servicos`, `#metodo`, `#para-quem`, `#principios`, `#perguntas`, `#contato`. Subpages use root-absolute paths (`/styles.css`, `/assets/...`).

## Commands

No package manager, build, lint or format tooling. Preview with any static file server, and run the stdlib acceptance suite before claiming completion:

```bash
python3 -m http.server 4174                # then open http://localhost:4174
python3 -m unittest discover -s tests -v   # acceptance suite — must stay green
```

Edits to HTML/CSS/JS take effect on refresh — no compile or bundle step. When adding or removing a public page, update `tests/test_site.py` (`PUBLIC_PATHS`) and `sitemap.xml` together.

## Conventions & Rules

- **All user-facing copy stays in Brazilian Portuguese** (pt-BR), matching the existing direct business-consulting register. Preserve `lang="pt-BR"`. Copy precision matters (accents, grammar, agreement) — this is public marketing material.
- **Reuse the existing design tokens** defined at the top of `styles.css` rather than hardcoding values: color scales `--petroleum-*`, `--cream-*`, `--graphite-*`, `--sage-*`; spacing `--space-*`; type scale `--text-*`; fonts `--font-display` / `--font-sans` / `--font-mono`.
- **Asset cache-busting:** asset references use `?v=N` query strings (e.g. `assets/strateo-favicon-v2.png?v=1`). When you replace a file in `assets/`, bump the `?v=N` on every `<img>`/`<link>` pointing at it to bust browser/CDN caches.
- **Verification:** run the acceptance suite (`python3 -m unittest discover -s tests -v`), then check in a browser that the `data-scrolled` header state, the mobile menu (`data-menu-open`, Escape closes) and the `.reveal` / `IntersectionObserver` animation still work after CSS/JS edits. There is no CI — the suite runs locally.
- **No invented claims:** never add clients, case results, certifications, phone numbers, CNPJ, `sameAs` profiles or regulatory endorsements to copy or JSON-LD. The test suite asserts some of these stay absent.
- **Commit style:** small, single-purpose commits describing the specific content/copy change (matching history, e.g. "Update family business audience copy"). No AI attribution in commit messages.

## Note

The README references brand/planning docs at absolute macOS paths (`/Users/teodoro/.openclaw/...`) that are not part of this repo and may be inaccessible — treat them as optional background context, not something to fetch or assume exists.
