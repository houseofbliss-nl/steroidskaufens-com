# Rapport GSC : toutes les pages vues (90 j) + analyse des motifs
# (doublons .html, modules sensibles, fiches produits, catégories...)
import json, os, sys, time, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))

import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

tok = json.load(open(os.path.join(HERE, "gsc-token-steroidskaufen.json"), encoding="utf-8"))
creds = Credentials(None, refresh_token=tok["refresh_token"], token_uri=tok["token_uri"],
                    client_id=tok["client_id"], client_secret=tok["client_secret"], scopes=tok["scopes"])
for _ in range(4):
    try:
        creds.refresh(google.auth.transport.requests.Request()); break
    except Exception as e:
        time.sleep(6)
svc = build("webmasters", "v3", credentials=creds)
SITE = "https://steroidskaufen.dealsnows.com/"

rows = svc.searchanalytics().query(siteUrl=SITE, body={
    "startDate": "2026-07-05", "endDate": "2026-10-02",
    "dimensions": ["page"], "rowLimit": 25000,
}).execute().get("rows", [])

print(f"Pages avec impressions/clics (90 j) : {len(rows)}\n")

# analyser les motifs d'URL
pat = collections.Counter()
dup_entries = []
for r in rows:
    u = r["keys"][0].replace(SITE, "/")
    # catégoriser
    if "/auth/" in u or "/mon_rec/" in u or "/ver_rev/" in u or "/tops_trend/" in u or "/tops/" in u or "/zubehoer/" in u:
        pat["MODULES SENSIBLES (auth/mon_rec/tops/ver_rev)"] += 1
        dup_entries.append((r["clicks"], r["impressions"], u))
    elif u.endswith(".html") or u.endswith(".html/"):
        pat["URLs AVEC .html (doublon possible)"] += 1
    elif "/blog/post/" in u:
        pat["Articles blog"] += 1
    elif "/de/" == u:
        pat["Racine /de/"] += 1
    else:
        # produit ou catégorie
        segs = [s for s in u.split("/") if s]
        if len(segs) >= 2 and any(c.isdigit() for c in segs[-1]):
            pat["Fiches produit"] += 1
        else:
            pat["Autres (catégories/content/villes)"] += 1

for k, v in pat.most_common():
    print(f"  {v:>4}  {k}")

print("\n" + "=" * 70)
print("MODULES SENSIBLES vus par Google (impressions > 0) — DOUBLONS/CANONICAL ?")
print("=" * 70)
mods = [e for e in dup_entries if e[1] > 0]
for c, i, u in sorted(mods, key=lambda x: -x[1])[:15]:
    print(f"  clics={c} imp={i}  {u}")

print("\n" + "=" * 70)
print("TOP 25 PAGES toutes confondues")
print("=" * 70)
for r in sorted(rows, key=lambda x: -x["impressions"])[:25]:
    u = r["keys"][0].replace(SITE, "/")
    print(f"  imp={r['impressions']:>5} clics={r['clicks']:>3} pos={r['position']:>5.1f}  {u}")

# doublons .html vs sans
print("\n" + "=" * 70)
print("DOUBLONS .html / sans (même page)")
print("=" * 70)
print("  total URLs .html dans le rapport :", pat["URLs AVEC .html (doublon possible)"])
print("\nTerminé.")