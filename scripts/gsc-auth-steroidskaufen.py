# Autorisation Google Search Console pour steroidskaufen (28/09/2026).
# App desktop "steroidskaufen-api" (client_id 553347412423-...). Flux OAuth local :
# n'ouvre PAS le navigateur → affiche l'URL, on l'ouvre dans Chrome existant.
# Crée gsc-token-steroidskaufen.json (à côté du client_secret).
#
# Usage :  python gsc-auth-steroidskaufen.py
import json, os, sys, glob, time

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
SCOPES = ["https://www.googleapis.com/auth/webmasters"]  # complet : permet soumettre sitemaps
TOKEN_FILE = os.path.join(HERE, "gsc-token-steroidskaufen.json")

cands = sorted(glob.glob(os.path.join(HERE, "client_secret_*.json")), key=os.path.getmtime)
if not cands:
    print("ERREUR : aucun client_secret_*.json dans " + HERE)
    sys.exit(1)
CLIENT_FILE = cands[-1]
print("client_secret utilisé :", os.path.basename(CLIENT_FILE))

if os.path.exists(TOKEN_FILE):
    try:
        with open(TOKEN_FILE, "r", encoding="utf-8") as f:
            cred_data = json.load(f)
        if cred_data.get("refresh_token"):
            print("Token déjà présent (" + os.path.basename(TOKEN_FILE) + ") — rien à faire.")
            sys.exit(0)
    except Exception:
        pass

from google_auth_oauthlib.flow import InstalledAppFlow

flow = InstalledAppFlow.from_client_secrets_file(CLIENT_FILE, SCOPES)

# Laisser l'URL s'afficher puis on l'ouvre dans Chrome déjà ouvert.
# Pour que Claude puisse relire l'URL : on l'écrit aussi dans un fichier.
import urllib.request, urllib.parse
from google_auth_oauthlib.flow import InstalledAppFlow as _I

# On récupère l'URL d'autorisation manuellement via le flow (code <= run_local_server).
# astuce : on force open_browser=False, run_local_server print l'URL.
print("FLOW_START")
flow.run_local_server(port=0, prompt="consent", open_browser=False,
                      authorization_prompt_message="AUTHORIZE_URL:{url}")

with open(CLIENT_FILE, "r", encoding="utf-8") as f:
    ccfg = json.load(f)
cinfo = ccfg.get("installed") or ccfg.get("web") or ccfg
with open(TOKEN_FILE, "w", encoding="utf-8") as f:
    json.dump(
        {
            "client_id": cinfo["client_id"],
            "client_secret": cinfo["client_secret"],
            "refresh_token": flow.credentials.refresh_token,
            "token_uri": cinfo["token_uri"],
            "scopes": list(flow.credentials.scopes),
        },
        f,
        indent=2,
    )
print("OK — Autorisation réussie. Token enregistré : " + TOKEN_FILE)