# Audit SEO exhaustif de tous les fichiers HTML de steroidskaufen (clone travail).
# Détecte : title manquant/dupliqué/long, meta description manquante/dupliquée,
# H1 manquant/dupliqué, canonical absent/incohérent, noindex, contenu mince,
# images sans alt, modules sensibles (auth/mon_rec/ver_rev/tops), fichiers hors sitemap.
import sys, os, re, glob, collections
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(ROOT, "..")
HTML_FILES = [f for f in glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True) if ".git" not in f]

# charger le sitemap pour comparer
sitemap_urls = set()
sp = os.path.join(SITE, "sitemap.xml")
if os.path.exists(sp):
    s = open(sp, encoding="utf-8", errors="replace").read()
    sitemap_urls = set(re.findall(r"<loc>([^<]+)</loc>", s))
print(f"Fichiers HTML : {len(HTML_FILES)} | URLs sitemap : {len(sitemap_urls)}\n")

# construire les URLs canoniques propres (sans .html)
def clean_url(path):
    rel = os.path.relpath(path, SITE).replace("\\", "/")
    if rel.endswith(".html"):
        rel = rel[:-5]
    return "https://steroidskaufen.dealsnows.com/" + rel

problems = collections.defaultdict(list)
titles = collections.defaultdict(list)
metas = collections.defaultdict(list)
noindex_files = []
thin = []
without_alt = []

MODULES_SENSIBLES = ["auth", "mon_rec", "ver_rev", "tops_trend", "/tops/", "/tops", "order", "checkout", "cart", "login", "adresse", "mes_commandes", "historique"]

for f in HTML_FILES:
    rel = os.path.relpath(f, SITE).replace("\\", "/")
    src = open(f, encoding="utf-8", errors="replace").read()
    url = clean_url(f)

    # --- title ---
    m = re.search(r"<title>(.*?)</title>", src, re.S)
    if not m:
        problems["title manquant"].append(rel)
    else:
        t = " ".join(m.group(1).split())
        titles[t].append(rel)
        if len(t) > 62:
            problems["title > 62 chars (%d)" % len(t)].append(rel)
        elif len(t) < 20:
            problems["title < 20 chars"].append(rel)

    # --- meta description ---
    m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', src)
    if not m or not m.group(1).strip():
        problems["meta description manquante/vide"].append(rel)
    else:
        md = m.group(1)
        metas[md[:80]].append(rel)
        if len(md) > 160:
            problems["meta desc > 160 (%d)" % len(md)].append(rel)
        elif len(md) < 70:
            problems["meta desc < 70 (%d)" % len(md)].append(rel)

    # --- H1 ---
    h1s = re.findall(r"<h1[^>]*>(.*?)</h1>", src, re.S)
    if len(h1s) == 0:
        problems["H1 manquant"].append(rel)
    elif len(h1s) > 1:
        problems["H1 multiples (%d)" % len(h1s)].append(rel)

    # --- canonical ---
    cm = re.search(r'<link\s+rel="canonical"\s+href="([^"]*)"', src)
    if not cm:
        problems["canonical absent"].append(rel)
    else:
        can = cm.group(1)
        if can.rstrip("/") != url.rstrip("/") and can != url:
            problems["canonical != url (%s vs %s)" % (can, url)].append(rel)

    # --- noindex / robots meta ---
    if re.search(r'name="robots"\s+content="[^"]*noindex', src) or re.search(r'name="googlebot"[^"]*noindex', src) or re.search(r'class="[^"]*noindex', src) is not None and "robots" in src.lower():
        noindex_files.append(rel)

    # --- contenu mince (mots visibles, hors balises) ---
    text = re.sub(r"<[^>]+>", " ", src)
    text = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", src, flags=re.S)
    words = len(re.findall(r"\w+", text, re.U))
    if words < 150 and "/blog/post/" not in rel:
        problems["contenu mince (<150 mots) (%d)" % words].append(rel)

    # --- module sensible dans l'URL ---
    if any(mo in rel for mo in MODULES_SENSIBLES):
        # les fichiers de module ne doivent PAS être dans le sitemap/autorité
        problems["module sensible (?auth/mon_rec/etc.)"].append(rel)

    # --- images sans alt ---
    imgs = re.findall(r"<img[^>]*>", src)
    for im in imgs:
        if "alt=" not in im and "data-src" not in im:
            without_alt.append(rel)
            break

print("=" * 70)
print("A. PROBLÈMES DÉTECTÉS (fichiers concernés)")
print("=" * 70)
for k in sorted(problems.keys(), key=lambda x: -len(problems[x])):
    files = problems[k]
    print(f"\n### {k}  ({len(files)})")
    for r in files[:12]:
        print("   ", r)
    if len(files) > 12:
        print(f"    ... et {len(files)-12} autres")

print("\n" + "=" * 70)
print("B. TITLES DUPLIQUÉS")
print("=" * 70)
nb = 0
for t, files in sorted(titles.items(), key=lambda x: -len(x[1])):
    if len(files) > 1:
        nb += len(files)
        print(f"[{len(files)}x] {t[:75]}")
        for r in files[:6]:
            print("      ", r)
print(f"\nTOTAL pages en title dupliqué : {nb}")

print("\n" + "=" * 70)
print("C. META DESCRIPTIONS DUPLIQUÉES (prefix de 80 chars)")
print("=" * 70)
nb = 0
for md, files in sorted(metas.items(), key=lambda x: -len(x[1])):
    if len(files) > 1:
        nb += len(files)
        print(f"[{len(files)}x] {md}")
        for r in files[:5]:
            print("      ", r)
print(f"\nTOTAL pages en meta desc dupliquée : {nb}")

print("\n" + "=" * 70)
print("D. HORS SITEMAP")
print("=" * 70)
hors = []
for f in HTML_FILES:
    rel = os.path.relpath(f, SITE).replace("\\", "/")
    u = clean_url(f)
    if u not in sitemap_urls and "google25ebb8d7ce51a5bc" not in rel:
        hors.append(rel)
print(f"\nFichiers HTML pas dans le sitemap : {len(hors)}")
for r in sorted(hors)[:40]:
    print("   ", r)
if len(hors) > 40:
    print(f"    ... et {len(hors)-40} autres")

print("\n" + "=" * 70)
print("E. NOINDEX / ROBOTS META trouvés")
print("=" * 70)
for r in noindex_files[:20]:
    print("   ", r)
print(f"\nTOTAL fichiers avec meta robots contenant noindex : {len(noindex_files)}")

print("\n" + "=" * 70)
print("F. IMAGES SANS ALT -> premières")
print("=" * 70)
for r in without_alt[:20]:
    print("   ", r)
print(f"\nTOTAL fichiers avec au moins une img sans alt : {len(without_alt)}")

print("\nFin de l'audit.")