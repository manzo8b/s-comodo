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
            assert page.locator(".manzo-footer-credit img").count() == 1, "Brand-footer image missing"
            color = page.locator(".site-masthead").evaluate("(e)=>getComputedStyle(e).borderBottomColor")
            assert color == "rgb(23, 28, 32)", (route, color)  # Reading Edition overrides older teal skin
        page.goto(BASE + "/", wait_until="domcontentloaded")
        assert page.locator(".front-lead").count() == 1, "Homepage lead story missing"
        cards = page.locator(".front-secondary")
        assert cards.count() >= 3, "Homepage secondary stories missing"
        assert page.locator(".front-lead h1 a").is_visible(), "Lead story link missing"
        assert page.locator(".front-secondary h2 a").count() >= 3, "Secondary links missing"
        link = page.locator(".site-navigation .site-links a").first
        assert link.is_visible()
        assert page.locator("link[href*='editorial-colors.css']").count() == 1
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
        # SC020 has an independent stylesheet, but must keep the host edition healthy.
        sc020_route = "/ozempic-scienza-fame-liberta-scelta/"
        resp = page.goto(BASE + sc020_route, wait_until="domcontentloaded")
        assert resp and resp.status == 200, ("SC020 article", resp.status if resp else None)
        assert page.locator("h1").first.inner_text().strip() == "Ozempic"
        assert page.locator(".sc020 .sc020-chapter").count() == 8
        assert page.locator(".sc020 .sc020-chart").count() == 1
        assert page.locator(".sc020 .sc020-risk").count() == 1
        assert page.locator(".sources ol li").count() == 9
        assert page.locator('link[href*="sc020-ozempic.css"]').count() == 1
        assert page.locator(".sc020 .sc020-chart").evaluate("(e)=>getComputedStyle(e).backgroundColor") == "rgb(255, 255, 255)"
        assert page.locator(".sc020 .sc020-risk").evaluate("(e)=>getComputedStyle(e).backgroundColor") == "rgb(255, 255, 255)"
        assert page.locator(".sc020 .sc020-delta").evaluate("(e)=>getComputedStyle(e).backgroundColor") == "rgb(255, 107, 0)"
        mobile_resp = mobile.goto(BASE + sc020_route, wait_until="domcontentloaded")
        assert mobile_resp and mobile_resp.status == 200
        assert mobile.locator("h1").first.is_visible()
        assert not mobile.evaluate("document.documentElement.scrollWidth>window.innerWidth+2"), "Horizontal overflow SC020"
        # SC020 readability and MANZO footer contrast, desktop and mobile.
        toc_link = page.locator(".sc020 .sc020-toc a").first
        assert toc_link.evaluate("(e)=>getComputedStyle(e).color") == "rgb(8, 8, 8)", "SC020 contents link not black"
        assert page.locator(".sc020 .sc020-toc").evaluate("(e)=>parseFloat(getComputedStyle(e).paddingLeft)") >= 22, "Contents padding too small"
        assert page.locator(".sc020 .sc020-flow > div").first.evaluate("(e)=>parseFloat(getComputedStyle(e).paddingLeft)") >= 18, "Mechanism card too tight"
        assert page.locator(".sc020 figure.sc020-figure").evaluate("(e)=>parseFloat(getComputedStyle(e).paddingLeft)") >= 22, "Illustration panel padding overridden"
        assert page.locator(".sc020 figure.sc020-chart").evaluate("(e)=>parseFloat(getComputedStyle(e).paddingLeft)") >= 22, "Chart panel padding overridden"
        index = page.locator(".reading-index")
        if index.locator("a").count():
            assert index.locator("a").first.evaluate("(e)=>getComputedStyle(e).color") == "rgb(8, 8, 8)", "Sidebar index is too faint"
        manzo = page.locator(".manzo-footer-credit")
        assert manzo.locator("span").evaluate("(e)=>getComputedStyle(e).color") == "rgb(16, 16, 16)", "MANZO footer text lacks contrast"
        assert manzo.locator("img").evaluate("(e)=>getComputedStyle(e).filter") == "none", "MANZO logo wrongly inverted"
        assert manzo.locator("a").evaluate("(e)=>getComputedStyle(e).backgroundColor") == "rgb(255, 255, 255)", "MANZO footer panel must be white"
        assert mobile.locator(".sc020 .sc020-flow > div").first.evaluate("(e)=>parseFloat(getComputedStyle(e).paddingLeft)") >= 14, "Mobile cards too tight"
        assert mobile.locator(".manzo-footer-credit img").evaluate("(e)=>getComputedStyle(e).filter") == "none", "Mobile logo wrongly inverted"
        assert not errors and not mobile_errors, (errors, mobile_errors)
        print("S-COMODO editorial colors: desktop, IT/ES/EN, cards, nav, mobile PASS")
    finally:
        browser.close()
