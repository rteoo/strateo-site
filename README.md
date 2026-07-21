# Strateo Site

Static institutional website for **Strateo** (Strateo Serviços Empresariais Ltda.), a Brazilian business-consulting brand. Hand-authored HTML/CSS/JS — no framework, no build step.

## Run locally

Any static file server works:

```sh
python3 -m http.server 4174
```

Then open http://localhost:4174.

## Structure

- `index.html` — homepage (services, method, audiences, principles, FAQ and contact)
- `<slug>/index.html` — focused service, audience, about and contact pages
- `styles.css` — all styling; design tokens (color/space/type scales) as CSS custom properties at the top
- `script.js` — scroll header state + reveal-on-scroll animation
- `assets/` — canonical wordmarks, favicon, social profile and social card

## Notes

- All copy is Brazilian Portuguese (`lang="pt-BR"`); keep tone and accents precise.
- Reuse the CSS custom properties in `styles.css` instead of hardcoding colors/sizes.
- When replacing an asset, bump the `?v=N` query string on its references in `index.html` to bust caches.
- Fonts load from Google Fonts via `@import` in `styles.css` (not bundled).
- Agent/contributor guidance: see [`AGENTS.md`](AGENTS.md).
- Brand identity and site/design plans live in the external workspace (Teô's brain vault), not in this repo.
