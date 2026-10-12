#!/usr/bin/env python3
"""Compare les prix de tarifs.json avec ceux affichés sur monky.fr.
Écrit un rapport Markdown dans rapport.md et sort avec le code 1 s'il y a des écarts."""
import json, re, sys, pathlib, urllib.request, html as H
root = pathlib.Path(__file__).resolve().parent.parent
data = json.loads((root / "tarifs.json").read_text(encoding="utf-8"))
UA = {"User-Agent": "Mozilla/5.0 (verif-tarifs Monky Niort)"}
PRICE = re.compile(r"(\d{1,3}(?:[.,]\d{1,2})?)\s*(?:€|&euro;|EUR)", re.I)

def fetch(url):
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, r.read().decode("utf-8", "ignore")
    except Exception as e:
        return getattr(e, "code", 0) or 0, str(e)

def prices(page):
    t = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", page, flags=re.S | re.I)
    t = H.unescape(re.sub(r"<[^>]+>", " ", t))
    return sorted({round(float(p.replace(",", ".")), 2) for p in PRICE.findall(t)})

cache, lines, gaps = {}, [], 0
def site(url):
    if url not in cache:
        cache[url] = fetch(url)
    return cache[url]

checks = [("Pass journée", data.get("pass_source"), data.get("pass", []))]
checks += [(v["nom"], v.get("source"), v.get("lignes", [])) for v in data["activites"].values()]
for nom, url, lignes in checks:
    ours = sorted({round(float(l["p"]), 2) for l in lignes if isinstance(l.get("p"), (int, float))})
    if not url or not ours:
        continue
    code, page = site(url)
    if code != 200:
        lines.append(f"| {nom} | ⚠️ page inaccessible ({code}) | {url} |")
        continue
    found = prices(page)
    missing = [p for p in ours if p not in found]
    if missing:
        gaps += 1
        lines.append(f"| {nom} | absents du site : {', '.join(f'{p:.2f} €' for p in missing)} — prix vus : {', '.join(f'{p:.2f}' for p in found) or 'aucun'} | {url} |")

report = "# Vérification des tarifs Monky Niort\n\n"
if lines:
    report += f"{gaps} activité(s) avec écart.\n\n| Activité | Constat | Page |\n|---|---|---|\n" + "\n".join(lines) + "\n"
else:
    report += "Aucun écart : tous les prix de tarifs.json sont présents sur le site.\n"
(root / "rapport.md").write_text(report, encoding="utf-8")
print(report)
sys.exit(1 if lines else 0)
