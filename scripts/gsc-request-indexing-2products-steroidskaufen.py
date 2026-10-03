# Demande d'indexation des 2 fiches produit enrichies (bromantan, anubis-enanthat).
# Chaque appel inspect() = une demande d'indexation (équivalent "Demander l'indexation").
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
    SITE + "de/bromantan/256-bromantan-endogenic-60-kapseln",
    SITE + "de/testosteron-enantat/303-anubis-testosteron-enanthat-250-mg-10-ml",
]

for u in URLS:
    body = {"inspectionUrl": u, "siteUrl": SITE}
    try:
        resp = svc.urlInspection().index().inspect(body=body).execute()
        r = resp.get("inspectionResult", {})
        isr = r.get("indexStatusResult", {}) or {}
        print(f"OK  {u}")
        print(f"    verdict={isr.get('verdict')}  coverage={isr.get('coverageState')}  indexing={isr.get('indexingState')}  robots={isr.get('robotsTxtState')}  refs={len(isr.get('referringUrls', []))}")
    except Exception as e:
        print(f"ERR {u} : {type(e).__name__}: {e}")

print("Terminé.")