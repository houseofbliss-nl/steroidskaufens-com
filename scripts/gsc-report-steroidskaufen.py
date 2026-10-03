# Rapport GSC steroidskaufen : sitemaps + requêtes + pages + agrégats.
import json, os, sys, time
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
        creds.refresh(google.auth.transport.requests.Request())
        break
    except Exception as e:
        print(f"(token refresh retry: {type(e).__name__})")
        time.sleep(6)

svc = build("webmasters", "v3", credentials=creds)
SITE = "https://steroidskaufen.dealsnows.com/"
START, END = "2026-07-01", "2026-09-28"

def q(body):
    return svc.searchanalytics().query(siteUrl=SITE, body=body).execute()

print("== 1) AGRÉGAT GLOBAL (90 j) ==")
try:
    r = q({"startDate": START, "endDate": END})["rows"][0]
    print(f"clics={r['clicks']} impressions={r['impressions']} ctr={r['ctr']:.3f} position={r['position']:.1f}")
except Exception as e:
    print("Erreur:", e)

print()
print("== 2) TOP 30 REQUÊTES ==")
try:
    rows = q({"startDate": START, "endDate": END, "dimensions": ["query"], "rowLimit": 30}).get("rows", [])
    for r in rows:
        k = r["keys"][0]
        print(f"- {k[:55]:<55} | clics={r['clicks']:>3} imp={r['impressions']:>5} pos={r['position']:>5.1f}")
except Exception as e:
    print("Erreur:", e)

print()
print("== 3) TOP 20 PAGES ==")
try:
    rows = q({"startDate": START, "endDate": END, "dimensions": ["page"], "rowLimit": 20}).get("rows", [])
    for r in rows:
        k = r["keys"][0].replace(SITE, "/")
        print(f"- {k[:80]:<80} | clics={r['clicks']:>3} imp={r['impressions']:>4}")
except Exception as e:
    print("Erreur:", e)

print()
print("== 4) SITEMAPS SOUMIS ==")
try:
    sm = svc.sitemaps().list(siteUrl=SITE).execute()
    for s in sm.get("sitemap", []):
        print("-", s.get("path"),
              "| lastSubmitted:", s.get("lastSubmitted"),
              "| lastDownloaded:", s.get("lastDownloaded"),
              "| isPending:", s.get("isPending"),
              "| errors:", s.get("errors"),
              "| warnings:", s.get("warnings"))
except Exception as e:
    print("Erreur:", e)