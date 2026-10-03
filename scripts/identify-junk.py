# Identifie les fichiers poubelles à supprimer :
#  1) modules soft-404 (auth/mon_rec/ver_rev/tops/tops_trend) avec contenu 404 vérifié
#  2) doublons à suffixe hex (base sans suffixe existe)
import os, re, glob, json

files = glob.glob('de/*.html') + [f for f in glob.glob('de/**/*.html', recursive=True)]
files = list(dict.fromkeys(files))  # dédoublonner tout en gardant l'ordre

sep = os.sep  # Windows: '\'  Unix: '/'

segments = {'auth', 'mon_rec', 'ver_rev', 'tops', 'tops_trend'}
mods = []
for f in files:
    parts = f.replace(os.sep, '/').split('/')
    if any(p in segments for p in parts[:-1]):
        src = open(f, encoding='utf-8', errors='replace').read()
        is404 = ('existiert nicht' in src) or ('Fehler 404' in src) or ('seite nicht' in src.lower())
        mods.append({'file': f, 'is404': is404})

hexd = []
for f in files:
    name = f.rsplit(sep, 1)[-1]
    m = re.search(r'([0-9a-fA-F]{4})\.html$', name)
    if not m:
        continue
    base = name[:m.start(1)] + '.html'
    basepath = os.path.join(f.rsplit(sep, 1)[0], base)
    if os.path.exists(basepath):
        hexd.append({'file': f, 'base': basepath})

print('=== MODULES soft-404 ===')
print('total fichiers sous auth/mon_rec/ver_rev/tops/tops_trend :', len(mods))
nb404 = sum(1 for x in mods if x['is404'])
print('   dont contenu vérifié 404 :', nb404)
print('   NON-404 (à conserver / inspecter) :', [x['file'] for x in mods if not x['is404']])
print()
print('=== DOUBLONS HEX avec base existante ===')
print('n :', len(hexd))
for x in hexd[:12]:
    print('  ', x['file'], '  <- base:', x['base'])

json.dump({'mods_to_delete': [x['file'] for x in mods if x['is404']],
           'hex_to_delete': [x['file'] for x in hexd]},
          open('_delete_list.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print()
print('Liste écrite dans _delete_list.json')