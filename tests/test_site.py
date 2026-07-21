"""Acceptance tests for the Strateo static site.

Run from the repository root:

    python3 -m unittest discover -s tests -v

Standard library only — no package manager exists in this repository.
"""

import json
import re
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORIGIN = "https://www.strateo.com.br"

# URL path -> file relative to repo root. "" is the homepage.
PUBLIC_PATHS = {
    "": "index.html",
    "consultoria-de-processos-e-gestao": "consultoria-de-processos-e-gestao/index.html",
    "automacao-com-ia": "automacao-com-ia/index.html",
    "consultoria-regulatoria-mercado-financeiro": "consultoria-regulatoria-mercado-financeiro/index.html",
    "escritorios-de-investimento": "escritorios-de-investimento/index.html",
    "mercado-financeiro-e-capitais": "mercado-financeiro-e-capitais/index.html",
    "industria-agro-construcao": "industria-agro-construcao/index.html",
    "negocios-familiares": "negocios-familiares/index.html",
    "sobre": "sobre/index.html",
    "contato": "contato/index.html",
}


def canonical_url(path):
    return f"{ORIGIN}/" if path == "" else f"{ORIGIN}/{path}/"


def read_page(path):
    return (ROOT / PUBLIC_PATHS[path]).read_text(encoding="utf-8")


def existing_pages():
    return {p: read_page(p) for p in PUBLIC_PATHS if (ROOT / PUBLIC_PATHS[p]).exists()}


class PageIndex(HTMLParser):
    """Collects the tag facts the tests assert on."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1_count = 0
        self.metas = []          # list of attr dicts
        self.links = []          # <link> attr dicts
        self.anchors = []        # <a> attr dicts
        self.buttons = []        # <button> attr dicts
        self.ids = set()
        self.title = None
        self.lang = None
        self.ld_json = []
        self._in_title = False
        self._in_ld = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        if tag == "html":
            self.lang = attrs.get("lang")
        elif tag == "h1":
            self.h1_count += 1
        elif tag == "meta":
            self.metas.append(attrs)
        elif tag == "link":
            self.links.append(attrs)
        elif tag == "a":
            self.anchors.append(attrs)
        elif tag == "button":
            self.buttons.append(attrs)
        elif tag == "title":
            self._in_title = True
        elif tag == "script" and attrs.get("type") == "application/ld+json":
            self._in_ld = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "script":
            self._in_ld = False

    def handle_data(self, data):
        if self._in_title:
            self.title = (self.title or "") + data.strip()
        elif self._in_ld:
            self.ld_json.append(data)

    def meta(self, **want):
        for attrs in self.metas:
            if all(attrs.get(k) == v for k, v in want.items()):
                return attrs
        return None


def index_page(html):
    parser = PageIndex()
    parser.feed(html)
    return parser


class MetadataTests(unittest.TestCase):
    def test_all_public_pages_exist(self):
        missing = [p for p in PUBLIC_PATHS if not (ROOT / PUBLIC_PATHS[p]).exists()]
        self.assertEqual(missing, [], f"missing public pages: {missing}")

    def test_language_and_single_h1(self):
        for path, html in existing_pages().items():
            page = index_page(html)
            with self.subTest(page=path or "home"):
                self.assertEqual(page.lang, "pt-BR")
                self.assertEqual(page.h1_count, 1, "each page needs exactly one h1")

    def test_titles_and_descriptions_unique(self):
        titles, descriptions = {}, {}
        for path, html in existing_pages().items():
            page = index_page(html)
            with self.subTest(page=path or "home"):
                self.assertTrue(page.title, "missing <title>")
                desc = page.meta(name="description")
                self.assertIsNotNone(desc, "missing meta description")
                self.assertNotIn(page.title, titles, f"title duplicated with {titles.get(page.title)}")
                self.assertNotIn(desc["content"], descriptions,
                                 f"description duplicated with {descriptions.get(desc['content'])}")
                titles[page.title] = path
                descriptions[desc["content"]] = path

    def test_canonical_and_robots_meta(self):
        for path, html in existing_pages().items():
            page = index_page(html)
            with self.subTest(page=path or "home"):
                canonicals = [l for l in page.links if l.get("rel") == "canonical"]
                self.assertEqual(len(canonicals), 1, "exactly one canonical link required")
                self.assertEqual(canonicals[0].get("href"), canonical_url(path))
                robots = page.meta(name="robots")
                self.assertIsNotNone(robots, "missing robots meta")
                self.assertIn("index,follow", robots["content"].replace(" ", ""))

    def test_social_metadata(self):
        for path, html in existing_pages().items():
            page = index_page(html)
            with self.subTest(page=path or "home"):
                for prop in ("og:title", "og:description", "og:url", "og:type", "og:image"):
                    self.assertIsNotNone(page.meta(property=prop), f"missing {prop}")
                self.assertEqual(page.meta(property="og:url")["content"], canonical_url(path))
                og_image = page.meta(property="og:image")["content"]
                self.assertTrue(og_image.startswith(f"{ORIGIN}/assets/"),
                                "og:image must be an absolute production URL")
                card = page.meta(name="twitter:card")
                self.assertIsNotNone(card, "missing twitter:card")
                self.assertEqual(card["content"], "summary_large_image")
                self.assertIsNotNone(page.meta(name="twitter:image"), "missing twitter:image")

    def test_homepage_organization_jsonld(self):
        page = index_page(read_page(""))
        self.assertEqual(len(page.ld_json), 1, "homepage needs exactly one JSON-LD block")
        data = json.loads(page.ld_json[0])
        graph = data["@graph"]
        organization = next(item for item in graph if item["@type"] == "Organization")
        website = next(item for item in graph if item["@type"] == "WebSite")
        self.assertEqual(organization["name"], "Strateo")
        self.assertEqual(organization["legalName"], "Strateo Serviços Empresariais Ltda.")
        self.assertEqual(organization["url"], f"{ORIGIN}/")
        self.assertEqual(organization["email"], "contato@strateo.com.br")
        self.assertTrue(organization["logo"]["url"].startswith(f"{ORIGIN}/assets/"))
        self.assertEqual(website["publisher"]["@id"], organization["@id"])
        address = organization["address"]
        self.assertEqual(address["@type"], "PostalAddress")
        self.assertEqual(address["addressLocality"], "Goiânia")
        self.assertEqual(address["addressRegion"], "GO")
        self.assertEqual(address["addressCountry"], "BR")
        self.assertIn("postalCode", address)
        # No unverified entity facts.
        for banned in ("telephone", "sameAs", "founder", "taxID", "vatID", "foundingDate"):
            self.assertNotIn(banned, organization,
                             f"JSON-LD must not publish unverified field {banned}")

    def test_social_card_asset_exists(self):
        self.assertTrue((ROOT / "assets" / "strateo-social-card.png").exists())

    def test_current_brand_assets_exist(self):
        for name in (
            "strateo-wordmark-v2-petroleum.png",
            "strateo-favicon-v3.png",
            "strateo-favicon-v3.ico",
            "strateo-social-profile-v3.png",
        ):
            self.assertTrue((ROOT / "assets" / name).exists(), f"missing brand asset {name}")

    def test_all_pages_use_current_brand_assets(self):
        for path, html in existing_pages().items():
            with self.subTest(page=path or "home"):
                self.assertIn("strateo-favicon-v3.png?v=1", html)
                self.assertIn("strateo-wordmark-v2-petroleum.png?v=1", html)

    def test_regulatory_service_jsonld(self):
        html = read_page("consultoria-regulatoria-mercado-financeiro")
        page = index_page(html)
        self.assertEqual(len(page.ld_json), 1)
        graph = json.loads(page.ld_json[0])["@graph"]
        service = next(item for item in graph if item["@type"] == "Service")
        breadcrumb = next(item for item in graph if item["@type"] == "BreadcrumbList")
        self.assertIn("Consultoria regulatória", service["name"])
        self.assertEqual(service["provider"]["@id"], f"{ORIGIN}/#organization")
        self.assertEqual(len(breadcrumb["itemListElement"]), 2)
        self.assertIn("não substitui parecer jurídico", html)


class CrawlerTests(unittest.TestCase):
    def test_robots_txt(self):
        robots = ROOT / "robots.txt"
        self.assertTrue(robots.exists(), "robots.txt missing")
        text = robots.read_text(encoding="utf-8")
        self.assertIn("User-agent: *\nAllow: /", text)
        self.assertIn("User-agent: OAI-SearchBot\nAllow: /", text)
        self.assertIn(f"Sitemap: {ORIGIN}/sitemap.xml", text)
        self.assertNotIn("GPTBot", text, "GPTBot policy is a separate decision; keep it out")

    def test_sitemap_covers_every_public_page(self):
        sitemap = ROOT / "sitemap.xml"
        self.assertTrue(sitemap.exists(), "sitemap.xml missing")
        tree = ET.parse(sitemap)
        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = {}
        for node in tree.getroot().findall("sm:url", ns):
            loc = node.findtext("sm:loc", namespaces=ns)
            urls[loc] = node.findtext("sm:lastmod", namespaces=ns)
        expected = {canonical_url(p) for p in PUBLIC_PATHS}
        self.assertEqual(set(urls), expected)
        for loc, lastmod in urls.items():
            self.assertRegex(lastmod or "", r"^\d{4}-\d{2}-\d{2}$", f"{loc} needs a lastmod date")


class HomepageExperienceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = read_page("")
        cls.page = index_page(cls.html)

    def test_skip_link_and_main_target(self):
        self.assertIn("conteudo", self.page.ids, "main content target #conteudo missing")
        hrefs = [a.get("href") for a in self.page.anchors]
        self.assertIn("#conteudo", hrefs, "skip link to #conteudo missing")

    def test_mobile_menu_button_is_accessible(self):
        button = next((b for b in self.page.buttons if "aria-controls" in b), None)
        self.assertIsNotNone(button, "menu button with aria-controls missing")
        self.assertEqual(button["aria-controls"], "navegacao-principal")
        self.assertEqual(button.get("aria-expanded"), "false")
        self.assertIn("navegacao-principal", self.page.ids)

    def test_navigation_targets(self):
        hrefs = {a.get("href") for a in self.page.anchors}
        for target in ("/#metodo", "/#para-quem", "/#principios", "/sobre/", "/contato/"):
            self.assertIn(target, hrefs, f"navigation must link {target}")

    def test_principles_replace_results(self):
        self.assertIn("principios", self.page.ids, "section id principios missing")
        self.assertNotIn("resultados", self.page.ids, "misleading resultados anchor must go")
        self.assertNotRegex(self.html, r">\s*Resultados\s*<", "nav label Resultados is misleading")

    def test_no_known_typo(self):
        self.assertNotIn("com, processo", self.html)

    def test_email_cta_is_prefilled_without_plain_address(self):
        self.assertNotRegex(self.html, r">\s*contato@strateo\.com\.br\s*<",
                            "homepage must not repeat the email address as plain linked text")
        self.assertIn("mailto:contato@strateo.com.br?subject=", self.html,
                      "mail CTA must be prefilled")
        self.assertIn("Enviar e-mail", self.html, "mail CTA must be labelled as email")
        self.assertIn("Falar com a Strateo", self.html)
        self.assertNotIn("Agendar conversa", self.html,
                         "CTA must not promise scheduling it cannot deliver")

    def test_browser_feedback_content_and_service_order(self):
        services = self.html.split('<div class="services-grid">', 1)[1].split('</div>', 1)[0]
        self.assertLess(services.index("Consultoria de processos e gestão"),
                        services.index("Consultoria regulatória"))
        self.assertLess(services.index("Consultoria regulatória"),
                        services.index("Automação com IA"))
        self.assertNotIn("CVM", services)
        self.assertIn("Legado · continuidade", self.html)
        self.assertNotIn("Gestão do fundador", self.html)
        self.assertIn("M6.5 3.5h7l4 4v13h-11z", self.html)

    def test_answer_first_content(self):
        self.assertIn("O que a Strateo faz", self.html)
        self.assertIn("consultoria", self.html.lower(),
                      "homepage must say plainly that Strateo is a consultancy")
        for question in (
            "O que a Strateo faz",
            "Para quais empresas",
            "diagnóstico de campo",
            "automatizar um processo com IA",
            "burocracia",
        ):
            self.assertIn(question, self.html, f"answer-first content missing: {question}")

    def test_services_are_linked(self):
        hrefs = {a.get("href") for a in self.page.anchors}
        self.assertIn("/consultoria-de-processos-e-gestao/", hrefs)
        self.assertIn("/automacao-com-ia/", hrefs)
        self.assertIn("/consultoria-regulatoria-mercado-financeiro/", hrefs)

    def test_updated_audience_language(self):
        self.assertIn("Serviços e Agro", self.html)
        self.assertIn("empresas do mercado financeiro, de serviços, agro e negócios familiares", self.html)
        self.assertNotIn("Indústria, agro e construção", self.html)

    def test_formulaic_titles_are_removed(self):
        for phrase in (
            "Planejamento que não vira rotina é só intenção bem diagramada",
            "Consultoria que vira operação, não relatório",
            "Estratégia que vira sistema, em quatro movimentos",
        ):
            self.assertNotIn(phrase, self.html)

    def test_no_unsupported_claims(self):
        for phrase in ("nossos clientes", "clientes como", "casos de sucesso"):
            self.assertNotIn(phrase, self.html.lower(),
                             f"unsupported claim phrasing: {phrase}")

    def test_language_is_consistent_portuguese(self):
        self.assertNotIn("AI · MFO", self.html, "ambiguous badge must be replaced")
        self.assertNotIn("Founder-led", self.html, "badge must be Portuguese")


class SubpageTests(unittest.TestCase):
    def test_subpages_share_chrome_and_link_internally(self):
        pages = existing_pages()
        for path, html in pages.items():
            if path == "":
                continue
            page = index_page(html)
            hrefs = {a.get("href") for a in page.anchors}
            with self.subTest(page=path):
                self.assertIn("/styles.css", html, "subpage must use the shared stylesheet")
                self.assertIn("/script.js", html, "subpage must use the shared script")
                self.assertIn("/", hrefs, "subpage must link back to the homepage")
                internal = {h for h in hrefs
                            if h and h.startswith("/") and h.strip("/") in PUBLIC_PATHS and h != "/"}
                self.assertGreaterEqual(len(internal), 2,
                                        f"subpage should cross-link at least 2 pages, got {internal}")
                self.assertIn("mailto:contato@strateo.com.br?subject=", html,
                              "subpage must carry the prefilled email CTA")


if __name__ == "__main__":
    unittest.main()
