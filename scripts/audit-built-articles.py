#!/usr/bin/env python3
"""Audit every published article in the built sitemap; report legacy issues without deleting content."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import xml.etree.ElementTree as ET

ROOT = Path("_site")
BASE = "/s-comodo"
NS = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.ids, self.h1, self.canonical, self.og, self.local_images, self.categories = [], 0, [], [], [], []
        self.lang = ""
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"): self.ids.append(a["id"])
        if tag == "html": self.lang = a.get("lang", "")
        if tag == "h1": self.h1 += 1
        if tag == "link" and a.get("rel") == "canonical": self.canonical.append(a.get("href", ""))
        if tag == "meta" and a.get("property") == "og:image": self.og.append(a.get("content", ""))
        if tag == "img": self.local_images.append((a.get("src", ""), a.get("alt")))
        if tag == "a" and "category-link" in a.get("class", "").split(): self.categories.append(a.get("href", ""))

def resolve(url):
    path = unquote(urlsplit(url).path)
    if not path.startswith(BASE + "/"): return None
    path = ROOT / path[len(BASE)+1:]
    return path / "index.html" if path.is_dir() else path

rows = []
for entry in ET.parse(ROOT / "sitemap.xml").findall("s:url", NS):
    if entry.find("s:lastmod", NS) is None: continue
    url = entry.findtext("s:loc", namespaces=NS)
    path = resolve(url)
    flags = []
    if not path or not path.is_file():
        rows.append({"url": url, "issues": ["missing_page"]})
        continue
    page = Page()
    page.feed(path.read_text(encoding="utf-8"))
    if page.h1 != 1: flags.append("h1_count:" + str(page.h1))
    if page.canonical != [url]: flags.append("canonical")
    if len(page.og) != 1: flags.append("social_cover_count:" + str(len(page.og)))
    for image in page.og:
        target = resolve(image)
        if target is not None and not target.is_file(): flags.append("missing_social_cover:" + image)
    for image, alt in page.local_images:
        if alt is None: flags.append("missing_alt:" + image)
        target = resolve(image)
        if target is not None and not target.is_file(): flags.append("missing_image:" + image)
    for link in page.categories:
        target = resolve(link)
        anchor = urlsplit(link).fragment
        if target and target.is_file() and anchor:
            topic = Page(); topic.feed(target.read_text(encoding="utf-8"))
            if anchor not in topic.ids: flags.append("missing_topic:" + anchor)
    duplicates = [i for i,n in Counter(page.ids).items() if n > 1]
    flags.extend("duplicate_id:" + i for i in duplicates)
    rows.append({"url": url, "lang": page.lang, "issues": sorted(set(flags))})
print(json.dumps({"articles": len(rows), "languages": dict(Counter(r.get("lang", "?") for r in rows)),
                  "clean": sum(not r["issues"] for r in rows),
                  "results": rows}, ensure_ascii=False, indent=2))
