# AGENTS.md

Canonical agent contract for this repository — it guides Claude Code, Codex, and any other coding agent. `CLAUDE.md` is a single `@AGENTS.md` import so Claude Code auto-loads these rules; make all edits here, never fork guidance into `CLAUDE.md`.

## Project

Static, single-page institutional/marketing website for **Strateo** (Strateo Serviços Empresariais Ltda.), a Brazilian business-consulting brand. All copy is in Brazilian Portuguese (`<html lang="pt-BR">`). Hand-authored HTML/CSS/JS — **no framework, no build step, no package manager.**

## Stack & Structure

- Plain HTML5 (`index.html`), CSS3 (`styles.css`, ~888 lines, design-token system via CSS custom properties), vanilla ES6+ JS (`script.js`, ~33 lines: scroll header state + `IntersectionObserver` reveal-on-scroll).
- Fonts load from Google Fonts CDN via `@import` in `styles.css` (Schibsted Grotesk, Hanken Grotesk, Spline Sans Mono) — the site is **not** fully offline; native OS fallback fonts are specified after the web fonts.
- `assets/` holds the v2 brand assets (all PNG): `strateo-wordmark-v2.png` (light surfaces), `strateo-wordmark-v2-reverse.png` (dark surfaces), `strateo-favicon-v2.png`. Canonical sources live in the brand design system (`.../strateo/business/brand/design-system/assets/`) — recapture there, never redraw. Everything is flat at the repo root.

```
index.html      # entry point; loads styles.css in <head>, script.js before </body>
styles.css      # all styling + design tokens
script.js       # header scroll state + reveal animation
assets/         # favicon, logos
README.md
```

Single-page section IDs (for nav links/anchors): `#topo`, `#metodo`, `#para-quem`, `#resultados`, `#contato`.

## Commands

There is **no** install/build/test/lint/typecheck/format tooling. Preview locally with any static file server:

```bash
python3 -m http.server 4174   # then open http://localhost:4174
```

Edits to `index.html` / `styles.css` / `script.js` take effect on refresh — no compile or bundle step.

## Conventions & Rules

- **All user-facing copy stays in Brazilian Portuguese** (pt-BR), matching the existing direct business-consulting register. Preserve `lang="pt-BR"`. Copy precision matters (accents, grammar, agreement) — this is public marketing material.
- **Reuse the existing design tokens** defined at the top of `styles.css` rather than hardcoding values: color scales `--petroleum-*`, `--cream-*`, `--graphite-*`, `--sage-*`; spacing `--space-*`; type scale `--text-*`; fonts `--font-display` / `--font-sans` / `--font-mono`.
- **Asset cache-busting:** asset references use `?v=N` query strings (e.g. `assets/strateo-favicon-v2.png?v=1`). When you replace a file in `assets/`, bump the `?v=N` on every `<img>`/`<link>` pointing at it to bust browser/CDN caches.
- **Verification is manual:** open the page in a browser and confirm the `data-scrolled` header state and the `.reveal` / `IntersectionObserver` scroll animation still work after CSS/JS edits. There are no automated tests or CI.
- **Commit style:** small, single-purpose commits describing the specific content/copy change (matching history, e.g. "Update family business audience copy"). No AI attribution in commit messages.

## Note

The README references brand/planning docs at absolute macOS paths (`/Users/teodoro/.openclaw/...`) that are not part of this repo and may be inaccessible — treat them as optional background context, not something to fetch or assume exists.
