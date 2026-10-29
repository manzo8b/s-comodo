#!/usr/bin/env python3
"""S-COMODO chromatic UI regression smoke on Jekyll static preview."""
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8765/s-comodo"
PAGES = ["/", "/es/", "/en/", "/archivio/", "/temi/", "/es/archivo/", "/en/archive/"]
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
    try:
        page = browser.new_page(viewport={"width": 1365, "height": 900})
        errors = []
        page.on("pageerror", lambda e: errors.append(str(e)))
        for route in PAGES:
            resp = page.goto(BASE + route, wait_until="domcontentloaded")
            assert resp and resp.status == 200, (route, resp.status if resp else None)
            assert page.locator(".site-masthead").count() == 1, route
            assert page.locator("main").count() == 1, route
            assert page.locator('a[href="mailto:marcelo2020.it@gmail.com"]').count() >= 1, route
            assert page.locator("a.manzo-footer-credit").count() == 0, "footer structure changed?"
            color = page.locator(".site-masthead").evaluate("(e)=>getComputedStyle(e).borderBottomColor")
            assert color == "rgb(12, 97, 93)", (route, color)
        page.goto(BASE + "/", wait_until="domcontentloaded")
        cards = page.locator(".home-editorial-card")
        assert cards.count() >= 3, "Homepage editorial covers missing"
        borders = cards.evaluate_all("(es)=>es.slice(0,4).map(e=>getComputedStyle(e).borderTopColor)")
        assert len(set(borders)) >= 3, borders
        link = page.locator(".site-navigation .site-links a").first
        assert link.is_visible()
        page.locator("link[href*='editorial-colors.css']").count() == 1
        assert not errors, errors

        mobile = browser.new_page(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
        mobile_errors = []
        mobile.on("pageerror", lambda e: mobile_errors.append(str(e)))
        for route in ["/", "/es/", "/en/", "/archivio/", "/temi/"]:
            resp = mobile.goto(BASE + route, wait_until="domcontentloaded")
            assert resp and resp.status == 200, route
            assert mobile.locator(".site-logo").is_visible(), route
            overflow = mobile.evaluate("document.documentElement.scrollWidth>window.innerWidth+2")
            assert not overflow, "Horizontal overflow " + route
        assert not mobile_errors, mobile_errors
        print("S-COMODO editorial colors: desktop, IT/ES/EN, cards, nav, mobile PASS")
    finally:
        browser.close()
