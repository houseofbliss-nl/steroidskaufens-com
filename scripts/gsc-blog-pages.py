# Pages blog ayant des impressions/clics (90 j) — pour prioriser la réécriture.
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
        creds.refresh(google.auth.transport.requests.Request()); break
    except Exception as e:
        time.sleep(6)
svc = build("webmasters", "v3", credentials=creds)
SITE = "https://steroidskaufen.dealsnows.com/"

rows = svc.searchanalytics().query(siteUrl=SITE, body={
    "startDate": "2026-06-04", "endDate": "2026-09-30",
    "dimensions": ["page"], "rowLimit": 5000,
}).execute().get("rows", [])

# Filtrer les pages de blog uniquement + les pages éditoriales utiles
res = []
for r in rows:
    u = r["keys"][0]
    if "/blog/post/" in u and not u.endswith(("/auth/silver", "/mon_rec/gold", "/ver_rev/gold", "/tops_trend/5-percent", "/tops/10-percent")):
        res.append((u.replace(SITE, "/"), r["clicks"], r["impressions"], r["position"]))

res.sort(key=lambda x: (-x[2], -x[1]))
print(f"NB articles blog vus par Google (90 j): {len(res)}\n")
for u, c, i, pos in res:
    print(f"  imp={i:>4} clics={c:>3} pos={pos:>5.1f}  {u}")