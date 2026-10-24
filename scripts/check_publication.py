#!/usr/bin/env python3
from pathlib import Path
import subprocess,sys,re
tracked=subprocess.run(["git","ls-files"],capture_output=True,text=True,check=True).stdout.splitlines()
blocked=[p for p in tracked if p.startswith("_drafts/") or p.startswith("docs/SC0")]
for p in Path("_posts").rglob("*.md") if Path("_posts").exists() else []:
 t=p.read_text(encoding="utf-8")
 if not re.search(r"(?m)^reviewed:\s*true\s*$",t) or not re.search(r"(?m)^editorial_status:\s*(pubblicato|published)\s*$",t):
  blocked.append(str(p)+" (no approval)")
if blocked:sys.exit("PUBLICATION BLOCKED:\n"+"\n".join(blocked))
print("Public release safety check OK")
