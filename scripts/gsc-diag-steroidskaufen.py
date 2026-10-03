# Diagnostic approfondi 02/10 — pourquoi trafic plafonné à ~86 clics.
import json, os, sys, time
from collections import defaultdict
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))

import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import requests

tok = json.load(open(os.path.join(HERE, "gsc-token-steroidskaufen.json"), encoding="utf-8"))
creds = Credentials(None, refresh_token=tok["refresh_token"], token_uri=tok["token_uri"],
                    client_id=tok["client_id"], client_secret=tok["client_secret"], scopes=tok["scopes"])
for _ in range(4):
    try:
        creds.refresh(google.auth.transport.requests.Request())
        break
    except Exception as e:
        print(f"(refresh retry {type(e).__name__})")
        time.sleep(6)

svc = build("webmasters", "v3", credentials=creds)
SITE = "https://steroidskaufen.dealsnows.com/"

def q(body):
    return svc.searchanalytics().query(siteUrl=SITE, body=body).execute()

print("=" * 76)
print("  steroidskaufen.dealsnows.com — diagnostic 02/10")
print("=" * 76)

print("\n== 1) AGRÉGATS PAR PÉRIODE (le « plateau ») ==")
for label, (s, e) in {
    "90 jours    (04/07 → 30/09)": ("2026-07-04", "2026-09-30"),
    "30 derniers (01/09 → 30/09)": ("2026-09-01", "2026-09-30"),
    "30 préc.    (02/08 → 31/08)": ("2026-08-02", "2026-08-31"),
    "30 avant    (04/07 → 02/08)": ("2026-07-04", "2026-08-02"),
}.items():
    try:
        r = q({"startDate": s, "endDate": e})["rows"][0]
        print(f"  {label} : clics={r['clicks']:>3} impressions={r['impressions']:>4} ctr={r['ctr']*100:.1f}% pos moy={r['position']:.1f}")
    except Exception as ex:
        print(f"  {label} : {ex}")

print("\n== 2) TENDANCE HEBDOMADAIRE (90 jours, par semaine) ==")
try:
    rows = q({"startDate": "2026-07-04", "endDate": "2026-09-30", "dimensions": ["date"],
              "rowLimit": 120}).get("rows", [])
    w = defaultdict(lambda: [0, 0])
    for r in rows:
        d = r["keys"][0]  # YYYY-MM-DD
        wk = f"{d[:4]}-S{(int(d[8:10]) - 1) // 7 + 1}"  # approximation
        # regroupement calendaire propre :
        from datetime import date as _d
        dt = _d.fromisoformat(d)
        iso = dt.isocalendar()
        wk = f"{iso[0]}-W{iso[1]:02d}"
        w[wk][0] += r["clicks"]; w[wk][1] += r["impressions"]
    for wk in sorted(w):
        c, i = w[wk]
        print(f"  {wk} : clics={c:>3} impressions={i:>4}")
except Exception as ex:
    print("  erreur:", ex)

print("\n== 3) TOP 25 REQUÊTES (90 j) ==")
try:
    for r in q({"startDate": "2026-07-04", "endDate": "2026-09-30",
                "dimensions": ["query"], "rowLimit": 25}).get("rows", []):
        k = r["keys"][0]
        print(f"  - {k[:52]:<52} | clics={r['clicks']:>3} imp={r['impressions']:>5} pos={r['position']:>5.1f}")
except Exception as ex:
    print("  erreur:", ex)

print("\n== 4) OPPORTUNITÉS : impressions fortes, 0 clic (CTR nul) ==")
try:
    rows = q({"startDate": "2026-07-04", "endDate": "2026-09-30",
              "dimensions": ["query"], "rowLimit": 250}).get("rows", [])
    seen = 0
    for r in sorted(rows, key=lambda x: -x["impressions"]):
        if r["clicks"] == 0 and r["impressions"] >= 15:
            k = r["keys"][0]
            print(f"  - {k[:52]:<52} | imp={r['impressions']:>4} pos={r['position']:>5.1f}")
            seen += 1
        if seen >= 15:
            break
    if seen == 0:
        print("  (aucune)")
except Exception as ex:
    print("  erreur:", ex)

print("\n== 5) TOP 20 PAGES (90 j) ==")
try:
    for r in q({"startDate": "2026-07-04", "endDate": "2026-09-30",
                "dimensions": ["page"], "rowLimit": 20}).get("rows", []):
        k = r["keys"][0].replace(SITE, "/")
        print(f"  - {k[:85]:<85} | clics={r['clicks']:>3} imp={r['impressions']:>4}")
except Exception as ex:
    print("  erreur:", ex)

print("\n== 6) SITEMAPS DANS GSC ==")
try:
    sm = svc.sitemaps().list(siteUrl=SITE).execute()
    for s in sm.get("sitemap", []):
        print(f"  - {s.get('path')}")
        print(f"      submitted={s.get('lastSubmitted')} downloaded={s.get('lastDownloaded')} pending={s.get('isPending')} errors={s.get('errors')} warnings={s.get('warnings')}")
except Exception as ex:
    print("  erreur:", ex)

print("\n== 7) INSPECTION URL (état réel des pages qui cliquent) ==")
URLS = [
    SITE + "de/",
    SITE + "de/96-anubis",
    SITE + "de/bromantan/256-bromantan-endogenic-60-kapseln",
    SITE + "de/blog/post/vergleich-von-testosteron-cypionat-und-testosteron-enanthate",
    SITE + "de/10-orale-steroide",
]
def inspect(url):
    for i in range(4):
        try:
            r = requests.post(
                "https://searchconsole.googleapis.com/v1/urlInspection/index:inspect",
                headers={"Authorization": "Bearer " + creds.token, "Content-Type": "application/json"},
                json={"inspectionUrl": url, "siteUrl": SITE}, timeout=60)
            if r.status_code == 200:
                return r.json()
            return {"x": f"HTTP {r.status_code}"}
        except Exception as e:
            time.sleep(5)
    return {"x": "timeout"}
for u in URLS:
    res = inspect(u).get("inspectionResult", {})
    isr = res.get("indexStatusResult", {})
    cov = isr.get("coverageState")
    flag = "✅" if cov in ("Indexed", "Submitted and indexed") else "⚠️"
    print(f"  {flag} {u.replace(SITE, '/')}")
    print(f"      coverage={cov} indexing={isr.get('indexingState')} fetch={isr.get('pageFetchState')} crawl={isr.get('lastCrawlTime')}")
    if cov not in ("Indexed", "Submitted and indexed"):
        print(f"      usrCanonical={isr.get('userCanonical')} gCanonical={isr.get('googleCanonical')} title={res.get('indexStatusResult', {}).get('title', '')[:60]}")
    time.sleep(2)

print("\n(termine)")