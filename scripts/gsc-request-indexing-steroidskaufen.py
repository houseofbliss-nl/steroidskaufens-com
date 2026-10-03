# Demande d'indexation URL par URL (équivalent "Demander l'indexation" de l'inspecteur GSC).
# Chaque appel inspect() = une demande d'indexation pour cette URL.
# Quota API : ~2000 appels/jour. Ne soumettre que des URLs MODIFIÉES / stratégiques.
import json, os, sys, time, glob
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

# URLs à soumettre : articles blog réécrits (sans extension, canonical).
# On génère automatiquement depuis les slugs des lots 1-3.
BLOG_DIR = os.path.join(HERE, "..", "de", "blog", "post")
slugs = [
    # lot 1
    "wirkungen-von-rad-140-wirkung-meinungen-und-dosierung",
    "wirkungen-von-ligandrol-lgd-4033-wirkung-meinungen-und-dosierung",
    "semaglutid-erfahrungen-2026-wirkung-dosierung-und-kosten-",
    "die-besten-medikamente-zur-gewichtsreduktion-liste",
    "welche-peptide-fuer-bodybuilding-waehlen",
    "ozempic-als-wirksames-schlankheitsmittel",
    "beste-steroide-fuer-muskelaufbau",
    # lot 2
    "dianabol-vs-testosteron-was-ist-besser-fuer-deinen-ersten-cycle",
    "steroide-und-blutbild-welche-werte-wir-kontrollieren-muessen-und-wie-oft",
    "mk-677-kombinieren",
    "prophylaxe-waehrend-eines-steroidzyklus",
    "semaglutid-nebenwirkungen-vermeiden-dosierung-tipps-und-magenprobleme-gezielt-reduzieren",
    "beste-hgh-peptide",
    "cardarine-in-kombination-mit-steroiden",
    "vergleich-von-testosteron-cypionat-und-testosteron-enanthate",
    # lot 3
    "wie-behandelt-man-sexuelle-funktionsstoerungen",
    "retatrutid-2026-vom-labor-zum-staerksten-adipositas-medikament-der-klinischen-forschung",
    "kagrilintid-beim-abnehmen",
    "winstrol-zyklus-wirkung-und-nutzen",
    "diaet-fuer-masse-grundregeln",
    "vergleich-von-trenbolone-acetate-und-enanthate-wirkung-dosierung",
    "mk-677-erfahrungen-test-bewertung-und-wirkung",
    "ostarine-mk-2866-wirkungen-meinungen-dosierung",
    "ratatrutid-vs-tirzepatid",
    "was-sind-die-sichersten-sarms",
    "wie-loest-man-peptide-auf-und-wie-berechnet-man-die-dosis",
    "essenzielle-supplemente-auf-dem-steroidzyklus",
]

URLS = [SITE + "de/blog/post/" + s for s in slugs]

print(f"{len(URLS)} URLs à soumettre pour indexation...")
ok = 0
for u in URLS:
    try:
        resp = svc.urlInspection().index().inspect(body={"inspectionUrl": u, "siteUrl": SITE}).execute()
        ide = resp.get("inspectionResult", {}).get("indexStatusResult", {})
        verdict = ide.get("verdict", "?")
        cov = ide.get("coverageState", "?")
        print(f"  [{verdict:7s} | {cov[:38]:38s}] {u.replace(SITE,'/')}")
        ok += 1
    except Exception as e:
        print(f"  [ERREUR] {u}: {e}")
    time.sleep(1.1)

print(f"\nSoumis avec succès : {ok}/{len(URLS)}")
print("Terminé.")