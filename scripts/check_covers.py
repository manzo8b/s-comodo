#!/usr/bin/env python3
"""S-COMODO editorial cover audit. Uses only the Python standard library.
Run from the repo root: python3 scripts/check_covers.py
Optional: --json emits machine-readable results. Existing legacy covers are
reported, never automatically replaced or treated as documented photographs.
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
POSTS = ROOT / "_posts"
RISK_WORDS = ("tipografic", "con titolo", "titolo leggibile", "testo incorporato",
              "copertina grafica", "cover grafica")


def front_matter(path: Path) -> dict[str, str]:
    raw = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*(?:\n|\Z)", raw, flags=re.S)
    if not match:
        return {}
    data = {}
    for line in match.group(1).splitlines():
        if line.startswith((" ", "\t", "#", "-")):
            continue
        item = re.match(r"([a-zA-Z_][\w-]*):\s*(.*)", line)
        if item:
            data[item.group(1)] = item.group(2).strip().strip("'\"")
    return data


def check(path: Path) -> dict:
    fm = front_matter(path)
    lang = fm.get("lang", "it")
    image = fm.get("image", "")
    name = path.name
    problems: list[str] = []
    if not fm.get("editorial_status"):
        problems.append("no_editorial_status")
    if fm.get("editorial_status") != "pubblicato":
        return {"file": name, "lang": lang, "published": False, "issues": problems}
    if not image:
        problems.append("missing_cover")
    elif image.startswith("/"):
        target = ROOT / image.lstrip("/")
        if not target.is_file():
            problems.append("missing_local_asset")
    else:
        problems.append("external_or_relative_cover_review")
    if not fm.get("image_alt"):
        problems.append("missing_alt")
    if not fm.get("image_caption"):
        problems.append("missing_caption")
    alt = fm.get("image_alt", "").lower()
    if any(token in alt for token in RISK_WORDS):
        problems.append("possible_title_inside_image_review")
    if image.lower().endswith(".svg"):
        problems.append("vector_cover_requires_photo_review")
    if image and not image.lower().endswith((".webp", ".jpg", ".jpeg", ".png", ".avif", ".svg")):
        problems.append("unknown_image_format")
    return {"file": name, "lang": lang, "article_id": fm.get("article_id", ""),
            "title": fm.get("title", ""), "image": image,
            "published": True, "issues": problems}


def main() -> int:
    if not POSTS.is_dir():
        print("_posts directory not found; run from the repository checkout.", file=sys.stderr)
        return 2
    rows = [check(path) for path in sorted(POSTS.iterdir()) if path.suffix.lower() in (".html", ".md", ".markdown")]
    published = [r for r in rows if r["published"]]
    counts = Counter(issue for r in published for issue in r["issues"])
    families: dict[str, list[str]] = defaultdict(list)
    for r in published:
        if r["article_id"]:
            families[r["article_id"]].append(r["lang"])
    report = {"published_pages": len(published), "unique_story_ids": len(families),
              "issue_counts": dict(counts), "results": published}
    if "--json" in sys.argv:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("S-COMODO · Editorial cover audit")
        print(f"Published pages: {len(published)}, unique story ids: {len(families)}")
        for k, v in counts.most_common():
            print(f"  {k}: {v}")
        for row in published:
            if row["issues"]:
                print(f"  {row['file']}: {', '.join(row['issues'])}")
        print("Review flags are not automatic publication blockers: inspect cover pixels.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
