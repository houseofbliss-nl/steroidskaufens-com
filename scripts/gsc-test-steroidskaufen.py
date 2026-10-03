# Test accès Search Console steroidskaufen : liste les propriétés accessibles avec le token.
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
print("== Propriétés accessibles ==")
try:
    sites = svc.sites().list().execute()
    for s in sites.get("siteEntry", []):
        print(f"- {s['siteUrl']}  | permission: {s.get('permissionLevel')}")
except Exception as e:
    print("Erreur:", e)