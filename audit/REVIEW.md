# Strateo website review

Review date: 2026-07-12

## Scope

Combined UX, responsive-design, accessibility, and basic implementation review of the static Strateo institutional website. The main journey reviewed was: understand the offer, inspect the method and target audiences, assess the stated outcomes, and reach the contact action.

## Verdict

The site is visually strong, cohesive, and technically clean for a compact institutional page. The biggest gaps are not visual polish: the mobile header removes primary navigation, the “Resultados” destination contains principles rather than evidence of results, and the primary scheduling action is only a bare email link. These weaken discoverability, trust, and conversion.

## Flow review

1. **Hero and offer — healthy with one conversion caveat.** The hierarchy is immediate, the visual motif supports the systems theme, and both desktop and mobile reflow cleanly. The CTA label promises scheduling but opens a generic email draft with no subject or context.
2. **Method — healthy.** The four-step structure scans quickly, the visual system is consistent, and the anchor lands below the sticky desktop header. The 11 px card numbers use a low-contrast gray (3.06:1 on white), below the 4.5:1 target for small text.
3. **Audience — needs copy cleanup.** The four segments are easy to compare. The first card contains the typo “com, processo”; “AI · MFO” is ambiguous alongside the site's use of “IA”; and mixed-language terms such as “asset”, “wealth”, and “Founder-led” make the Portuguese voice less consistent.
4. **Results/principles — structurally healthy, semantically mismatched.** The section is visually compelling, but the navigation label “Resultados” creates an expectation of cases, figures, or proof. The content is instead a set of operating principles.
5. **Contact — functional but high-friction.** The section is prominent and the address is clear. The only action is `mailto:`, so users without a configured mail client or those expecting a scheduling flow receive no guided next step.
6. **Mobile — visually healthy, navigation needs work.** The page fits at 390 px and 320 px without horizontal overflow; CTAs become full-width and remain easy to tap. Below 760 px the primary section navigation disappears entirely, leaving only the contact CTA in the header and the footer links after the whole page.

## Prioritized findings

### High impact

- Preserve primary navigation on mobile with a compact menu or a simple horizontally scrollable section-nav pattern.
- Make the scheduling CTA match its promise: use a real booking destination, a lightweight contact form, or at minimum a prefilled email subject/body and label the action as email.
- Replace or rename “Resultados”: add credible proof (specific outcomes, anonymized case snapshots, client types, or measurable improvements), or rename the navigation and section to “Princípios”.

### Medium impact

- Correct “cadência comercial com, processo” and normalize language/acronyms across the audience cards.
- Add a skip link targeting `#topo`/`main` for keyboard and assistive-technology users.
- Increase the method-card number contrast from `--text-subtle` to a color that reaches at least 4.5:1 on white, or treat the numbers as decorative and hide them from assistive technology if they carry no meaning.

### Lower impact

- Add canonical and social-preview metadata (`og:title`, `og:description`, `og:image`, and X card metadata) so shared links look intentional.
- Consider adding a visible email address or alternative contact method so the CTA is not the only way to discover the destination.

## Confirmed strengths

- Clear heading hierarchy, `pt-BR` language declaration, landmarks, labeled navigation, image alt text, and decorative SVGs hidden from assistive technology.
- Strong color and type system with readable body-copy contrast.
- Responsive reflow works at 1280 px, 390 px, and 320 px with no horizontal overflow.
- Primary buttons meet a 44 px minimum height; focus-visible styles and reduced-motion handling are present in the CSS.
- No browser console warnings or errors were observed during the reviewed flow.

## Evidence limits

- This was a local static-site review, not a production performance, analytics, SEO-indexing, or end-to-end email-delivery test.
- Keyboard focus movement could not be exercised reliably through the browser-control surface; focus styles were confirmed in source, but a manual keyboard pass is still recommended.
- Screenshot evidence cannot establish full WCAG conformance or screen-reader behavior.

## Accepted screenshots

- `01-desktop-hero.png`
- `02-desktop-method.png`
- `03-desktop-audience.png`
- `04-desktop-results.png`
- `05-desktop-contact.png`
- `06-mobile-hero.png`
- `08-mobile-contact.png`
