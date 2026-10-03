# Inspection URL Search Console via API (webmasters v3, urlInspection.index).
# Donne l'état d'indexation exact + la cause si non indexé.
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

SITE = "https://steroidskaufen.dealsnows.com/"
svc = build("searchconsole", "v1", credentials=creds)

URLS = [
    # pages produits à fort trafic qui avaient été déindexées
    "https://steroidskaufen.dealsnows.com/de/bromantan/256-bromantan-endogenic-60-kapseln",
    "https://steroidskaufen.dealsnows.com/de/testosteron-enantat/303-anubis-testosteron-enanthat-250-mg-10-ml",
    "https://steroidskaufen.dealsnows.com/de/testosterone-cypionate/302-anubis-testosteron-cypionat-250-mg-10-ml",
    "https://steroidskaufen.dealsnows.com/de/96-anubis",
    # articles blog réécrits (échantillon)
    "https://steroidskaufen.dealsnows.com/de/blog/post/wirkungen-von-rad-140-wirkung-meinungen-und-dosierung",
    "https://steroidskaufen.dealsnows.com/de/blog/post/mk-677-erfahrungen-test-bewertung-und-wirkung",
]

def status_label(resp):
    ide = resp.get("inspectionResult", {}).get("indexStatusResult", {})
    v = ide.get("verdict", "?")
    cov = ide.get("coverageState", "?")
    cxt = ide.get("indexingState", "?")
    rob = ide.get("robotsTxtState", "?")
    crawl = ide.get("lastCrawlTime", "?")
    can = ide.get("googleCanonical", "?")
    return f"verdict={v} | coverage={cov} | indexing={cxt} | robots={rob} | crawl={crawl} | canonical={can}"

for u in URLS:
    try:
        resp = svc.urlInspection().index().inspect(body={"inspectionUrl": u, "siteUrl": SITE}).execute()
        print(u.replace(SITE, "/"))
        print("   ", status_label(resp))
        refs = resp.get("inspectionResult", {}).get("indexStatusResult", {}).get("referringUrls", [])
        if refs:
            print("    refs:", refs)
        msg = resp.get("inspectionResult", {}).get("indexStatusResult", {}).get("message") or resp.get("inspectionResult", {}).get("indexStatusResult", {}).get("lastCrawlError")
        if msg:
            print("    message:", msg)
    except Exception as e:
        print(f"ERREUR {u}: {e}")
    time.sleep(1)
print("\nTerminé.")