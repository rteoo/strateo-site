# Strateo SEO and GEO audit

Review date: 2026-07-12

Production URL reviewed: `https://www.strateo.com.br/`

## Executive verdict

The production site is publicly reachable, uses HTTPS, redirects the apex domain to `www`, returns `200` to both Googlebot and OAI-SearchBot, and exposes its important content as semantic HTML. Those are good foundations.

Discoverability is nevertheless weak because the site provides almost none of the signals that help search engines and answer engines establish a canonical URL, identify the real-world organization, discover content systematically, or cite specific expertise. The public domain did not appear as a first-party result in the reviewed brand and `site:` searches; this is an external-search observation, not a substitute for Google Search Console's URL Inspection report.

## Current-state scorecard

| Area | Status | Evidence |
| --- | --- | --- |
| Basic crawlability | Good | Homepage returns `200` to Googlebot and OAI-SearchBot; no `noindex` or blocking header was found. |
| Canonicalization | Partial | `https://strateo.com.br/` redirects to `https://www.strateo.com.br/`, but the page has no HTML canonical link. |
| Crawl discovery | Weak | Both `/robots.txt` and `/sitemap.xml` return `404`. A missing robots file does not block crawling, but there is no sitemap declaration or explicit crawler policy. |
| Search snippet | Partial | Title and meta description exist, but they are abstract and do not clearly state “consultoria”, the service categories, audiences, or geographic entity. |
| Structured data | Missing | No JSON-LD or other structured data is present. |
| Entity authority | Weak | Legal name and address appear in visible text, but there is no organization schema, CNPJ, phone, leadership/about information, or verified `sameAs` profile links. |
| Topical authority | Weak | One URL covers all topics; there are no focused service pages, audience pages, case studies, articles, or FAQs. |
| Citation readiness | Weak | Most claims are principles or promises without named expertise, methodology detail, examples, data, dates, or measurable outcomes. |
| Social/share presentation | Missing | No Open Graph, X card, or social-preview image metadata is present. |
| Mobile and semantic HTML | Good | Important content is present in the initial HTML, headings are orderly, and responsive layouts avoid horizontal overflow. |

## High-priority actions

### 1. Add crawl and canonical files

Add an HTML canonical link using the final production hostname:

```html
<link rel="canonical" href="https://www.strateo.com.br/">
```

Add `/robots.txt`:

```text
User-agent: *
Allow: /

User-agent: OAI-SearchBot
Allow: /

Sitemap: https://www.strateo.com.br/sitemap.xml
```

`OAI-SearchBot` controls eligibility for ChatGPT Search discovery. `GPTBot` is a separate training-control decision and is not required for appearing in ChatGPT Search.

Add `/sitemap.xml`, initially containing the canonical homepage and later every durable public page. Submit it in Google Search Console and Bing Webmaster Tools.

### 2. Make the homepage describe the business in search language

The current headline is memorable, but the title, description, and opening copy do not directly answer what Strateo is. Add a plain-language sentence near the top such as:

> A Strateo é uma consultoria de estratégia, processos, indicadores e automação com IA para empresas do mercado financeiro, indústria, agro, construção e negócios familiares.

Suggested metadata direction:

```html
<title>Strateo | Estratégia, processos e automação com IA</title>
<meta name="description" content="Consultoria para transformar estratégia em rotinas, indicadores, controles e automações com IA para mercado financeiro, indústria, agro e negócios familiares.">
```

The exact wording should reflect the services Strateo is prepared to sell and substantiate; avoid adding keywords for services that are not genuinely offered.

### 3. Establish the Strateo entity

Add JSON-LD on the homepage using `Organization` or the most accurate `LocalBusiness` subtype. Include only verified facts that are also visible or supported elsewhere:

- `name` and `legalName`
- canonical `url`
- crawlable logo URL
- business description
- primary email
- full postal address with `BR` country code
- phone, founding date, CNPJ/tax identifier, and leadership only if approved for publication
- official LinkedIn and other verified profiles through `sameAs`

Create a substantive “Sobre a Strateo” page that identifies the company, leadership, relevant experience, operating location, who it serves, and how engagements work. Keep the Google Business Profile consistent with the site name, address, phone, service categories, and canonical URL.

### 4. Create focused, original pages

A single one-page site gives Google and answer engines only one URL to retrieve for every question. Create a small set of deep, useful pages rather than many thin pages:

- `/consultoria-de-processos-e-gestao/`
- `/automacao-com-ia/`
- `/escritorios-de-investimento/`
- `/mercado-financeiro-e-capitais/`
- `/industria-agro-construcao/`
- `/negocios-familiares/`
- `/casos/`
- `/sobre/`
- `/contato/`

Each page should have a unique title, description, canonical URL, clear H1, internal links, concrete deliverables, engagement process, suitability criteria, and original evidence. Do not publish templated keyword variants with little added value.

### 5. Publish proof that can be cited

The section labelled “Resultados” currently contains principles. Either rename it “Princípios” or replace it with evidence such as:

- anonymized case summaries with starting condition, intervention, timeframe, and outcome
- quantified improvements where disclosure is permitted
- methodology details and decision criteria
- founder/consultant credentials and first-hand experience
- dated articles that answer real client questions using original frameworks or data

Generative search systems are more likely to retrieve and cite a passage that makes a precise, self-contained claim and supports it than a generic marketing statement.

### 6. Add answer-first content for GEO

Add concise, visible answers to the questions prospects actually ask. Good starting topics include:

- O que faz a Strateo?
- Para quais empresas a Strateo trabalha?
- Como funciona o diagnóstico de campo?
- Quando uma empresa deve automatizar um processo com IA?
- Como estruturar indicadores e cadência comercial em um escritório de investimentos?
- Como melhorar controles sem aumentar a burocracia?
- Qual é a diferença entre processo, rotina, indicador e automação?

Each answer should state the answer first, then provide context, examples, limitations, and a link to a deeper service or case page. FAQ content may help retrieval and comprehension, but FAQ schema should not be treated as a guaranteed rich-result tactic.

## Medium-priority actions

- Add `og:title`, `og:description`, `og:url`, `og:type`, a purpose-built 1200×630 image, and equivalent X card metadata.
- Make the email address visible as text and add a stable phone or booking destination if available.
- Add descriptive image filenames and useful alt text to future non-decorative images; avoid publishing important evidence only inside images.
- Reduce the render-blocking Google Fonts request to the families and weights actually used, or self-host optimized subsets if operationally worthwhile.
- Track `utm_source=chatgpt.com` referrals and organic landing-page conversions in analytics.
- Verify both Google Search Console and Bing Webmaster Tools, submit the sitemap, request homepage indexing, and monitor branded/non-branded queries separately.

## What not to prioritize

- Do not expect an `llms.txt` file, “AI schema”, or keyword-heavy hidden text to create inclusion. Google explicitly says no new AI text files or special schema are required for its AI features; OpenAI's published requirement is crawler access through OAI-SearchBot.
- Do not generate large numbers of near-duplicate location or service pages. Originality, usefulness, and verifiable first-hand evidence matter more than page count.
- Do not add ratings, clients, certifications, regulatory relationships, outcomes, or `sameAs` links that cannot be substantiated.

## Recommended implementation order

1. Canonical tag, `robots.txt`, `sitemap.xml`, and crawler verification.
2. Better title, meta description, and a direct “what Strateo is” sentence.
3. Organization/LocalBusiness JSON-LD and a complete About page.
4. Search Console, Bing Webmaster Tools, Google Business Profile, and analytics setup.
5. Two priority service pages and one strong case study.
6. Remaining audience pages and answer-first knowledge content.
7. Social-preview metadata and performance cleanup.

## Verification after publication

- Confirm `200` responses for Googlebot and OAI-SearchBot.
- Confirm `/robots.txt` and `/sitemap.xml` return valid content.
- Validate canonical URLs and structured data.
- Use Google Search Console URL Inspection and request indexing.
- Submit and inspect the sitemap in Google Search Console and Bing Webmaster Tools.
- Search for the brand and canonical domain after recrawling; indexing may take time and is not guaranteed.
- Monitor organic impressions, indexed pages, branded queries, non-branded service queries, and referrals containing `utm_source=chatgpt.com`.

## Authoritative references

- Google, AI features and websites: https://developers.google.com/search/docs/appearance/ai-features
- Google, generative AI optimization guide: https://developers.google.com/search/docs/fundamentals/ai-optimization-guide
- Google, developer SEO guide: https://developers.google.com/search/docs/fundamentals/get-started-developers
- Google, Organization structured data: https://developers.google.com/search/docs/appearance/structured-data/organization
- Google, LocalBusiness structured data: https://developers.google.com/search/docs/appearance/structured-data/local-business
- OpenAI, Publishers and Developers FAQ: https://help.openai.com/en/articles/12627856-publishers-and-developers-faq
- OpenAI, ChatGPT Search: https://help.openai.com/en/articles/9237897-chatgpt-search
