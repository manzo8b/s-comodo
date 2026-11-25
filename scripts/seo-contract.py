#!/usr/bin/env python3
"""Validate the published sitemap, metadata, article schema and reciprocal language links."""
import json
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter
import xml.etree.ElementTree as ET

ROOT=Path("_site")
ORIGIN="https://manzo8b.github.io/s-comodo/"
NS={"s":"http://www.sitemaps.org/schemas/sitemap/0.9"}
class Document(HTMLParser):
    def __init__(self):
        super().__init__(); self.canonical=[]; self.lang=""; self.alternates={}; self.meta={}; self.schemas=[]; self.current=None; self.errors=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=="html": self.lang=a.get("lang","")
        if tag=="link" and a.get("rel")=="canonical": self.canonical.append(a.get("href"))
        if tag=="link" and a.get("rel")=="alternate" and a.get("hreflang"):
            k=a["hreflang"]
            if k in self.alternates: self.errors.append("duplicate hreflang "+k)
            self.alternates[k]=a.get("href")
        if tag=="meta":
            k=a.get("name") or a.get("property")
            if k: self.meta.setdefault(k,[]).append(a.get("content",""))
        if tag=="script" and a.get("type")=="application/ld+json": self.current=""
    def handle_data(self,data):
        if self.current is not None: self.current+=data
    def handle_endtag(self,tag):
        if tag=="script" and self.current is not None:
            try:self.schemas.append(json.loads(self.current))
            except ValueError as e:self.errors.append("invalid JSON-LD: "+str(e))
            self.current=None

entries=ET.parse(ROOT/"sitemap.xml").findall("s:url",NS)
urls=[e.findtext("s:loc",namespaces=NS) for e in entries]
errors=[]; docs={}; articles=set()
if len(set(urls))!=len(urls): errors.append("duplicate sitemap URLs")
for e,url in zip(entries,urls):
    if not url or not url.startswith(ORIGIN):
        errors.append("unexpected URL "+str(url)); continue
    path=ROOT/unquote(url[len(ORIGIN):])
    if path.is_dir():path=path/"index.html"
    if not path.is_file():errors.append("missing "+url);continue
    d=Document();d.feed(path.read_text(encoding="utf-8"));docs[url]=d
    def check(ok,message):
        if not ok:errors.append(url+": "+message)
    check(d.canonical==[url],"canonical mismatch")
    check(d.lang in {"it","es","en"},"invalid document language")
    check(not any("noindex" in x.lower() for x in d.meta.get("robots",[])),"noindex in sitemap")
    check(len(d.meta.get("description",[]))==1 and bool(d.meta["description"][0].strip()),"missing or duplicate description")
    for err in d.errors:errors.append(url+": "+err)
    if e.find("s:lastmod",NS) is not None:
        articles.add(url)
        s=[x for x in d.schemas if x.get("@type")=="Article"]
        check(len(s)==1,"expected one Article JSON-LD")
        if len(s)==1:
            a=s[0];check(a.get("url")==url and a.get("inLanguage")==d.lang,"schema URL/language mismatch")
            check(all(a.get(k) for k in ("headline","description","datePublished","author","publisher","image")),"incomplete Article")
        check(len(d.meta.get("og:image",[]))==1,"missing/duplicate social image")
        check(len(d.meta.get("article:published_time",[]))==1,"missing published date")
for url,d in docs.items():
    for lang,target in d.alternates.items():
        if lang=="x-default":continue
        other=docs.get(target)
        if not other or other.lang!=lang or other.alternates.get(d.lang)!=url:
            errors.append(url+": non-reciprocal hreflang "+lang)
    if d.alternates and d.alternates.get(d.lang)!=url:
        errors.append(url+": missing self hreflang")
print(json.dumps({"urls":len(urls),"articles":len(articles),"errors":errors},ensure_ascii=False,indent=2))
raise SystemExit(bool(errors))
