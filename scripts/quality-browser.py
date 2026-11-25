#!/usr/bin/env python3
"""Local browser QA: all articles and three homepages; no field CWV claims."""
import json, os
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright

BASE=os.environ.get("SCOMODO_BASE","http://127.0.0.1:8765/s-comodo").rstrip("/")
NS={"s":"http://www.sitemaps.org/schemas/sitemap/0.9"}
routes=["/","/es/","/en/"]
for item in ET.parse("_site/sitemap.xml").findall("s:url",NS):
    if item.find("s:lastmod",NS) is not None:
        routes.append(urlsplit(item.findtext("s:loc",namespaces=NS)).path.removeprefix("/s-comodo"))
rows=[]
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True)
    for width in (390,1440):
        ctx=browser.new_context(viewport={"width":width,"height":900}, reduced_motion="reduce")
        ctx.route("**/*",lambda route: route.continue_() if route.request.url.startswith(BASE+"/") else route.abort())
        for route in routes:
            page=ctx.new_page(); errors=[]
            response=page.goto(BASE+route,wait_until="load",timeout=30000)
            if not response or not response.ok:errors.append("HTTP")
            if page.locator("h1").count()!=1:errors.append("h1")
            if page.locator("main").count()!=1:errors.append("main landmark")
            page.keyboard.press("Tab")
            if not page.locator(".skip-link:focus").count():errors.append("skip link not first focus")
            else:
                page.keyboard.press("Enter")
                if not page.locator("#contenuto:focus").count():errors.append("skip target not focused")
            if route in ("/","/es/","/en/"):
                def edition(r):
                    return "/es/" if r.startswith("/es/") else "/en/" if r.startswith("/en/") else "/"
                expected=[r for r in routes[3:] if edition(r)==route][:7]
                actual=page.locator(".nsp-hero h1 a, .nsp-triple .nsp-card h3 a").evaluate_all("(els) => els.map(e => new URL(e.href).pathname.replace(/^\\/s-comodo/, ''))")
                if actual!=expected:errors.append("homepage chronology or story count: "+str(actual))
                more=page.locator(".nsp-latest h3 a").evaluate_all("(els) => els.map(e => e.href)")
                if any(urlsplit(u).path.removeprefix("/s-comodo") in actual for u in more):errors.append("duplicate home story")
                if width==1440 and len(expected)>4:
                    tops=page.locator(".nsp-triple .nsp-card").evaluate_all("(els) => els.map(e => Math.round(e.getBoundingClientRect().top))")
                    if len(set(tops[:3]))!=1 or tops[3]<=tops[0]:errors.append("desktop story row layout")
            data=page.evaluate("""() => {
              const resources=performance.getEntriesByType('resource');
              const nav=performance.getEntriesByType('navigation')[0];
              const cover=document.querySelector('.article-image img,.nsp-hero__photo img');
              return {overflow:document.documentElement.scrollWidth>innerWidth+2,
                coverLoaded:!cover||(cover.complete&&cover.naturalWidth>0),
                missingAlt:[...document.images].filter(i=>!i.hasAttribute('alt')).length,
                resourceCount:resources.length,transferBytes:resources.reduce((s,r)=>s+r.transferSize,nav?.transferSize||0),
                domContentLoadedMs:Math.round(nav?.domContentLoadedEventEnd||0),
                loadMs:Math.round(nav?.loadEventEnd||0)};
            }""")
            for key in ("overflow","missingAlt"):
                if data[key]:errors.append(key)
            if not data["coverLoaded"]:errors.append("cover failed to load")
            rows.append({"route":route,"width":width,"metrics":data,"issues":errors})
            page.close()
        ctx.close()
    browser.close()
report={"scope":"Local Chromium smoke tests, not Lighthouse or WCAG certification","pages":len(routes),"checks":len(rows),"clean":sum(not row["issues"] for row in rows),"results":rows}
Path("quality-browser-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!="results"},indent=2))
for row in rows:
    if row["issues"]:print(row["route"],row["width"],row["issues"])
# Baseline 25 November 2026: all 70 checks passed. Fail on any regression.
raise SystemExit(any(row['issues'] for row in rows))
