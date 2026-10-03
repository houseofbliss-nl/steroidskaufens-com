# Réécriture ciblée lot 1 — articles blog déjà indexés (07 fichiers).
# Même URL + même canonical. Aligne title/&amp; H1 / lead / FAQ sur les requêtes
# exactes collectées (autocomplete DE + requêtes à clic GSC).
import sys, re, os
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "..", "de", "blog", "post")

# (fichier, title, meta, H1, phrase d'accroche lead, question FAQ, réponse FAQ)
EDITS = [
 ("wirkungen-von-rad-140-wirkung-meinungen-und-dosierung.html",
  "RAD 140 kaufen: Wirkung, Dosierung &amp; Erfahrungen",
  "RAD 140 kaufen: Wirkung, Dosierung, Erfahrungen und Vorher-Nachher-Bilder. Alles zum SARM Rad140 auf einen Blick – diskreter Versand in ganz Deutschland.",
  "RAD 140 kaufen: Wirkung, Dosierung &amp; Erfahrungen",
  "RAD 140 kaufen und richtig dosieren: Testolone ist der stärkste etablierte SARM auf dem Markt. Wer Rad140 bestellen möchte, findet in diesem Ratgeber Wirkung, Dosierung, Nebenwirkungen und echte Erfahrungen.",
  "Kann ich RAD-140 in Deutschland kaufen?",
  "Ja, RAD-140 ist in unserem Shop erhältlich und wird diskret nach ganz Deutschland versendet. Als Research-Chemical ist Testolone nicht als Arzneimittel zugelassen — informieren Sie sich vor der Bestellung über die rechtliche Lage in Ihrer Region."),

 ("wirkungen-von-ligandrol-lgd-4033-wirkung-meinungen-und-dosierung.html",
  "Ligandrol LGD-4033 kaufen: Wirkung, Dosierung &amp; Erfahrungen",
  "Ligandrol LGD-4033 kaufen: Wirkung, Dosierung und echte Erfahrungen. Alles zum SARM Ligandrol – diskreter Versand in ganz Deutschland.",
  "Ligandrol LGD-4033 kaufen: Wirkung, Dosierung &amp; Erfahrungen",
  "Ligandrol kaufen und LGD-4033 richtig dosieren: Der als Anabolicum bekannte SARM gehört zu den stärksten auf dem Markt. Hier finden Sie Wirkung, Erfahrungen und alle kaufrelevanten Infos auf einen Blick.",
  "Wo kann ich Ligandrol LGD-4033 kaufen?",
  "Ligandrol ist in unserem Shop erhältlich und wird diskret in ganz Deutschland versendet. Achten Sie beim Kauf auf geprüfte Qualität und ein seriöses Analysezertifikat des Herstellers."),

 ("semaglutid-erfahrungen-2026-wirkung-dosierung-und-kosten-.html",
  "Semaglutid kaufen: Erfahrungen 2026, Wirkung, Dosierung &amp; Kosten",
  "Semaglutid kaufen: Erfahrungen 2026, Wirkung, Dosierung und Kosten im Überblick. Abnehmen mit Semaglutid im Selbstversuch erklärt.",
  "Semaglutid kaufen: Erfahrungen 2026, Wirkung, Dosierung &amp; Kosten",
  "Semaglutid kaufen und damit abnehmen: Der GLP-1-Rezeptoragonist hat in den letzten zwei Jahren einen regelrechten Boom in Deutschland ausgelöst — Millionen Menschen weltweit spritzen ihn wöchentlich, um Körpergewicht zu reduzieren.",
  "Kann ich Semaglutid ohne Rezept kaufen?",
  "Semaglutid ist in Deutschland verschreibungspflichtig. Zahlreiche Online-Shops bieten den Wirkstoff dennoch als Research-Chemical an — prüfen Sie vor dem Kauf die rechtliche Lage. In unserem Sortiment finden Sie Alternativen zur Gewichtsreduktion mit diskretem Versand in ganz Deutschland."),

 ("die-besten-medikamente-zur-gewichtsreduktion-liste.html",
  "Die besten Medikamente zur Gewichtsreduktion 2026: Liste &amp; Vergleich",
  "Die besten Medikamente zum Abnehmen 2026 im Vergleich: Ozempic, Semaglutid, Tirzepatid, Retatrutid, Orforglipron – Liste mit Wirkung, Preis &amp; Dosierung.",
  "Die besten Medikamente zur Gewichtsreduktion 2026: Liste &amp; Vergleich",
  "Die besten Medikamente zur Gewichtsreduktion 2026 im Vergleich: Diese Liste zeigt, welche Wirkstoffe wirklich helfen. Ozempic, Semaglutid, Tirzepatid, Retatrutid und weitere Abnehm-Mittel mit Wirkung, Preis und Dosierung.",
  "Wo kann ich Medikamente zur Gewichtsreduktion kaufen?",
  "Viele der hier vorgestellten Wirkstoffe sind in Deutschland verschreibungspflichtig. In unserem Shop finden Sie eine Auswahl an Produkten zur Unterstützung der Gewichtsreduktion mit diskretem Versand in ganz Deutschland."),

 ("welche-peptide-fuer-bodybuilding-waehlen.html",
  "Peptide für Bodybuilding kaufen: BPC-157, TB-500, CJC-1295",
  "Peptide für Bodybuilding kaufen: BPC-157, TB-500, CJC-1295 und mehr im Vergleich. Welches Peptid für Muskelaufbau, Fettverbrennung &amp; Regeneration?",
  "Peptide für Bodybuilding kaufen: BPC-157, TB-500, CJC-1295",
  "Peptide für Bodybuilding kaufen und richtig wählen: BPC-157, TB-500, CJC-1295 und weitere sind längst aus der Nische der „Profi-Anwender\" in den Mainstream der Trainingsplanung eingewandert.",
  "Wo kann ich Peptide für Bodybuilding kaufen?",
  "Geeignete Peptide für Muskelaufbau, Fettverbrennung und Regeneration finden Sie in unserem Shop mit diskretem Versand in ganz Deutschland. Achten Sie auf lyophilisiert gelieferte Ware und prüfen Sie die empfohlene Lagerung im Kühlschrank."),

 ("ozempic-als-wirksames-schlankheitsmittel.html",
  "Ozempic zum Abnehmen: Erfahrungen, Dosierung &amp; Alternativen",
  "Ozempic zum Abnehmen: Erfahrungen, Wirkstoff Semaglutid, Dosierung und Alternativen wie Mounjaro, Retatrutid und Wegovy im Vergleich.",
  "Ozempic zum Abnehmen: Erfahrungen, Dosierung &amp; Alternativen",
  "Ozempic zum Abnehmen: Der Markenname für den Wirkstoff Semaglutid wurde ursprünglich als Therapie für Patienten mit Typ-2-Diabetes auf den Markt gebracht — heute ist er das meistdiskutierte Schlankheitsmittel der Welt.",
  "Kann ich Ozempic in Deutschland kaufen?",
  "Ozempic ist in Deutschland verschreibungspflichtig und offiziell nur für Typ-2-Diabetes zugelassen. Viele Anwender nutzen es trotzdem zum Abnehmen. Zur Gewichtsreduktion stehen Alternativen wie Wegovy, Mounjaro oder Retatrutid im Fokus — unser Shop liefert diskret in ganz Deutschland."),

 ("beste-steroide-fuer-muskelaufbau.html",
  "Beste Steroide für Muskelaufbau 2026: Liste &amp; Vergleich",
  "Beste Steroide für Muskelaufbau und Masse im Vergleich: Testosteron, Dianabol, Deca, Winstrol – Liste mit Dosierung und Nebenwirkungen.",
  "Beste Steroide für Muskelaufbau 2026: Liste &amp; Vergleich",
  "Beste Steroide für Muskelaufbau 2026 im Vergleich: Testosteron, Dianabol und Anapolon gehören zu den wirksamsten anabolen Steroiden für die Massephase — doch welches ist für welchen Anwender wirklich das Beste?",
  "Wo kann ich Steroide für Muskelaufbau kaufen?",
  "Steroide für die Massephase sind in Deutschland nicht legal erhältlich. Unser Shop führt dennoch ein breites Sortiment für den Muskelaufbau mit diskretem Versand in ganz Deutschland — informieren Sie sich vor dem Kauf über die rechtliche Lage in Ihrer Region."),
]

for fn, title, meta, h1, lead, q, a in EDITS:
    path = os.path.join(DIR, fn)
    src = open(path, encoding="utf-8", errors="replace").read()

    # --- title ---
    m = re.search(r"<title>.*?</title>", src)
    assert m, fn + " : title absent"
    src = src[:m.start()] + "<title>" + title + "</title>" + src[m.end():]

    # --- meta description ---
    m = re.search(r'(<meta\s+name="description"\s+content=")[^"]*"', src)
    assert m, fn + " : meta description absente"
    src = src[:m.start()] + m.group(1) + meta + '"' + src[m.end():]

    # --- H1 ---
    m = re.search(r"<h1[^>]*>.*?</h1>", src, re.S)
    assert m, fn + " : h1 absent"
    src = src[:m.start()] + "<h1>" + h1 + "</h1>" + src[m.end():]

    # --- lead : insérer la phrase d'accroche en tête du <p class="sk-lead"> ---
    m = re.search(r'<p class="sk-lead"[^>]*>\s*', src)
    assert m, fn + " : sk-lead absent"
    pos = m.end()
    src = src[:pos] + lead + " " + src[pos:]

    # --- FAQ : ajout d'un item (achat) en fin de section sk-faq ---
    idx = src.rfind("sk-faq__item")
    if idx == -1:
        # pas de sk-faq : créer la section juste avant CTA support
        print("   (pas de sk-faq, section creee)", fn)
        anchor = '<div class="sk-cta-support">'
        ai = src.find(anchor)
        assert ai != -1, fn + " : sk-cta-support introuvable"
        block = ('<div class="sk-faq">\n  <h2 class="sk-faq__title">Häufig gestellte Fragen</h2>\n'
                 '  <div class="sk-faq__item">\n    <p class="sk-faq__q">' + q + '</p>\n    <p class="sk-faq__a">' + a + '</p>\n  </div>\n</div>\n\n\n')
        src = src[:ai] + block + src[ai:]
    else:
        end_item = src.find("\n  </div>", idx)
        assert end_item != -1, fn + " : fin item FAQ introuvable"
        item = ('\n  <div class="sk-faq__item">\n    <p class="sk-faq__q">' + q + '</p>\n    <p class="sk-faq__a">' + a + '</p>\n  </div>')
        src = src[:end_item + len("\n  </div>")] + item + src[end_item + len("\n  </div>"):]

    open(path, "w", encoding="utf-8").write(src)
    print("OK", fn)

print("\nTerminé.")