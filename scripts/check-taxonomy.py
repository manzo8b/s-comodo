#!/usr/bin/env python3
"""Verify every published article is listed once under a valid localized topic."""
from pathlib import Path
from urllib.parse import urlsplit
from collections import Counter
from html.parser import HTMLParser
import xml.etree.ElementTree as ET
ROOT=Path("_site")
BASE="/s-comodo"
TOPICS={"democrazia-diritti","economia-istituzioni","societa-comunita","storia-identita","scienza-salute","tecnologia-risorse","media-informazione"}
NS={"s":"http://www.sitemaps.org/schemas/sitemap/0.9"}
def path(url):
    return urlsplit(url).path.removeprefix(BASE)
def edition(p):
    return "es" if p.startswith("/es/") else "en" if p.startswith("/en/") else "it"
def file(p):
    return ROOT / p.lstrip("/") / "index.html"
class Parser(HTMLParser):
    def __init__(self):
        super().__init__();self.groups={};self.current=None;self.category=[];self.formats=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs);classes=a.get("class","").split()
        if tag=="section" and "topic-section" in classes:
            self.current=a.get("id");self.groups.setdefault(self.current,[])
        if tag=="a" and self.current and a.get("href"):
            self.groups[self.current].append(path(a["href"]))
        if tag=="a" and "category-link" in classes:self.category.append(a.get("href",""))
        if "article-format" in classes:self.formats.append(a.get("data-format"))
    def handle_endtag(self,tag):
        if tag=="section":self.current=None
def parse(p):
    d=Parser();d.feed(file(p).read_text(encoding="utf-8"));return d
articles=[path(e.findtext("s:loc",namespaces=NS)) for e in ET.parse(ROOT/"sitemap.xml").findall("s:url",NS) if e.find("s:lastmod",NS) is not None]
counts=Counter();errors=[]
for lang,route in (("it","/temi/"),("es","/es/temas/"),("en","/en/topics/")):
    d=parse(route)
    if set(d.groups)!=TOPICS:errors.append(f"{lang}: topic IDs mismatch")
    actual=Counter(p for group in d.groups.values() for p in group)
    expected=Counter(p for p in articles if edition(p)==lang)
    if actual!=expected:errors.append(f"{lang}: missing/duplicate articles {actual-expected} {expected-actual}")
    for topic,group in d.groups.items():
        counts[topic]+=len(group)
        for p in group:
            if p not in expected:continue
            a=parse(p)
            if not any(urlsplit(link).fragment==topic and path(link)==route for link in a.category):errors.append(p+": category link mismatch")
            if not any(f in {"dossier","saggio","contesto"} for f in a.formats):errors.append(p+": missing editorial format")
print("Taxonomy:",len(articles),"articles;",dict(counts))
if errors:raise SystemExit("\n".join(errors))
print("Taxonomy PASS")
