#!/usr/bin/env python3
"""Automated accessibility audit. Not a WCAG conformity certificate."""
import json, os
from pathlib import Path
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
from playwright.sync_api import sync_playwright
BASE=os.environ.get("SCOMODO_BASE","http://127.0.0.1:8765/s-comodo").rstrip("/")
NS={"s":"http://www.sitemaps.org/schemas/sitemap/0.9"}
urls=[e.findtext("s:loc",namespaces=NS) for e in ET.parse("_site/sitemap.xml").findall("s:url",NS)]
rows=[]
with sync_playwright() as p:
    browser=p.chromium.launch()
    ctx=browser.new_context(viewport={"width":390,"height":900},reduced_motion="reduce")
    ctx.route("**/*",lambda route:route.continue_() if route.request.url.startswith(BASE+"/") else route.abort())
    for url in urls:
        path=urlsplit(url).path.removeprefix("/s-comodo") or "/"
        page=ctx.new_page()
        response=page.goto(BASE+path,wait_until="load",timeout=30000)
        if not response or not response.ok: raise RuntimeError("HTTP "+path)
        page.add_script_tag(path=os.environ["AXE_PATH"])
        result=page.evaluate("""async () => await axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa','wcag22aa']}})""")
        rows.append({"route":path,"violations":[{"id":v["id"],"impact":v["impact"],"help":v["help"],"nodes":[{"target":n["target"],"summary":n.get("failureSummary")} for n in v["nodes"]]} for v in result["violations"]],"incomplete":[{"id":v["id"],"nodes":len(v["nodes"])} for v in result["incomplete"]]})
        page.close()
    browser.close()
report={"pages":len(rows),"pagesWithoutDetectedViolations":sum(not r["violations"] for r in rows),"results":rows}
Path("quality-reports").mkdir(exist_ok=True)
Path("quality-reports/axe.json").write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!="results"}))
for r in rows:
    if r["violations"]: print(r["route"],[(v["id"],v["impact"],len(v["nodes"])) for v in r["violations"]])
