# Resoumission sitemap steroidskaufen via l'API Search Console (webmasters v3).
# L'API permet submit/delete pour les sitemaps (seul le Search Analytics est read-only).
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
FEED = "https://steroidskaufen.dealsnows.com/sitemap.xml"

# 1) état actuel avant resoumission
try:
    lst = svc.sitemaps().list(siteUrl=SITE).execute()
    print("== Sitemaps soumis avant ==")
    for s in lst.get("sitemap", []):
        print(f"- {s.get('path')}  lastSubmitted={s.get('lastSubmitted','?')}  pending={s.get('isPending')}")
except Exception as e:
    print("Liste sitemaps impossible:", e)

# 2) resoumission (PUT)
print("\n== Resoumission ==")
try:
    svc.sitemaps().submit(siteUrl=SITE, feedpath=FEED).execute()
    print(f"OK: {FEED} resoumis avec succès.")
except Exception as e:
    print(f"ERREUR submit: {e}")

# 3) vérification immédiate
time.sleep(2)
try:
    lst = svc.sitemaps().list(siteUrl=SITE).execute()
    print("\n== Sitemaps après ==")
    for s in lst.get("sitemap", []):
        print(f"- {s.get('path')}  lastSubmitted={s.get('lastSubmitted','?')}  pending={s.get('isPending')}  errors={s.get('errors')} warnings={s.get('warnings')} contents={s.get('contents',[])}")
except Exception as e:
    print("Vérification après impossible:", e)
print("\nTerminé.")