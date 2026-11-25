#!/usr/bin/env python3
"""Browser regression tests for the integrated newspaper dossier layout."""
import os
from playwright.sync_api import sync_playwright

BASE = os.environ.get("SCOMODO_BASE", "http://127.0.0.1:8765/s-comodo").rstrip("/")
ROUTES = {
    "/ueno-bank-anatomia-crisi/": (None, None),
    "/es/ueno-bank-anatomia-crisis/": (None, None),
    "/en/ueno-bank-anatomy-crisis/": (None, None),
    "/ueno-bank-audit-macro/": (None, None),
    "/es/ueno-bank-auditoria-macro/": (None, None),
    "/en/ueno-bank-macro-audit/": (None, None),
    "/la-democrazia-non-ha-padroni/": (".spain-dossier .sd-wide", ".spain-dossier .sd-chart"),
    "/malika-alzheimer-identita-transgender-privacy/": (".sc021 .wide", ".sc021 .s-privacy"),
    "/midterm-usa-2026-diversita-progressismo/": (None, ".sc019 .sc019-ending"),
    "/patrimoniale-ed-eredita-quanto-puo-tassare-lo-stato/": (None, None),
    "/es/patrimonial-herencias-capital-y-libertad/": (None, None),
}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for width in (320, 390, 768, 1100, 1280, 1440):
        page = browser.new_page(viewport={"width": width, "height": 900})
        for route, (wide, panel) in ROUTES.items():
            response = page.goto(BASE + route, wait_until="domcontentloaded")
            assert response and response.ok, (width, route, "HTTP")
            assert page.locator("h1").count() == 1, (width, route, "duplicate title")
            assert page.locator(".article-image img").count() == 1, (width, route, "cover")
            assert page.locator('meta[property="og:image"]').count() == 1, (width, route, "social cover")
            assert not page.evaluate("document.documentElement.scrollWidth > innerWidth + 2"), (width, route, "page overflow")
            if "anatom" in route:
                assert page.locator(".sc017 .sources li[id^=src]").count() == 27, (route, "sources")
                assert page.locator(".site-masthead").count() == 1, (route, "shared masthead")
                assert page.locator(".article-body .sc017 .legacy-copy").count() == 1
            if wide:
                blocks = page.locator(wide)
                assert blocks.count() > 0, (width, route, "missing blocks")
                for block in blocks.all():
                    assert block.evaluate("""e => {
                        const b=e.getBoundingClientRect(), c=e.closest('.article-body').getBoundingClientRect();
                        return b.left >= c.left-2 && b.right <= c.right+2;
                    }"""), (width, route, "block outside reading column")
            if panel:
                for block in page.locator(panel).all():
                    assert block.evaluate("(e) => getComputedStyle(e).backgroundColor === 'rgb(255, 255, 255)'"), (width, route, "panel background")
        page.close()
    browser.close()
print("Dossier layout regression PASS")
