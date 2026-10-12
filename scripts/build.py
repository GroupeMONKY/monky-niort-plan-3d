#!/usr/bin/env python3
"""Réinjecte tarifs.json dans index.html (bloc <script id="tarifs-data">)."""
import json, re, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
data = json.loads((root / "tarifs.json").read_text(encoding="utf-8"))
html = (root / "index.html").read_text(encoding="utf-8")
blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
new, n = re.subn(r'(<script id="tarifs-data" type="application/json">).*?(</script>)',
                 lambda m: m.group(1) + blob + m.group(2), html, count=1, flags=re.S)
if n != 1:
    sys.exit("Bloc tarifs-data introuvable dans index.html")
(root / "index.html").write_text(new, encoding="utf-8")
print("index.html mis à jour depuis tarifs.json")
