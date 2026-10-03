# Réécriture ciblée lot 3 — les articles restants classés en 1re page (pos 3-20)
# + mk-677 (1 clic). Même URL, même canonical.
import sys, re, os
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "..", "de", "blog", "post")

EDITS = [
 ("wie-behandelt-man-sexuelle-funktionsstoerungen.html",
  "Sexuelle Funktionsstörungen durch Steroide: Ursachen, Behandlung & Schutz",
  "Sexuelle Funktionsstörungen bei Steroiden: Ursachen (Östrogen, Prolaktin, Testosteron), Behandlungs-Optionen und wie Sie Libido & Erektionsfähigkeit schützen.",
  "Sexuelle Funktionsstörungen durch Steroide: Ursachen, Behandlung & Schutz",
  "Sexuelle Funktionsstörungen sind kein Randthema in der Steroid-Welt, sondern eines der häufigsten Begleitprobleme — wir zeigen Ursachen, wirksame Behandlungen und wie Sie Libido & Potenz während der Kur schützen."),
 ("retatrutid-2026-vom-labor-zum-staerksten-adipositas-medikament-der-klinischen-forschung.html",
  "Retatrutid kaufen: Das stärkste Abnehm-Medikament 2026 – Wirkung & Dosierung",
  "Retatrutid 2026: Das stärkste Adipositas-Medikament der klinischen Forschung – Wirkung, Dosierung, Erfahrungen und Kaufhinweise für Deutschland.",
  "Retatrutid kaufen: Das stärkste Abnehm-Medikament 2026 – Wirkung & Dosierung",
  "Retatrutid ist der neue Maßstab der Abnehm-Medikamente: Ein einzelnes Molekül stellt drei Stellschrauben des Stoffwechsels gleichzeitig um — wir erklären Wirkung, Dosierung und was Sie vor dem Kauf wissen müssen."),
 ("kagrilintid-beim-abnehmen.html",
  "Kagrilintid beim Abnehmen: Wirkung, Vorteile & Dosierung",
  "Kagrilintid beim Abnehmen: Wirkung, Vorteile und was wir wirklich wissen – das vielversprechende GLP-1-Analogon im direkten Vergleich mit Semaglutid & Retatrutid.",
  "Kagrilintid beim Abnehmen: Wirkung, Vorteile & Dosierung",
  "Kagrilintid beim Abnehmen: Während Semaglutid und Retatrutid die Schlagzeilen der GLP-1-Klasse beherrschen, ist Kagrilintid eine der spannendsten Alternativen — hier lesen Sie Wirkung, Vorteile und was wir wirklich wissen."),
 ("winstrol-zyklus-wirkung-und-nutzen.html",
  "Winstrol kaufen & Zyklus: Wirkung, Nutzen und Dosierung",
  "Winstrol (Stanozolol) kaufen und richtig dosieren: Wirkung, Nutzen im Cut und Zyklus-Planung – Tabletten vs. Injektionen plus Nebenwirkungen im Überblick.",
  "Winstrol kaufen & Zyklus: Wirkung, Nutzen und Dosierung",
  "Winstrol (Stanozolol) ist eines der bekanntesten Cutting-Steroide weltweit — für Härte und Definition in der Diät. Wir zeigen Wirkung, Nutzen, Dosierung und worauf beim Kauf zu achten ist."),
 ("diaet-fuer-masse-grundregeln.html",
  "Diät für Masseaufbau: Die wichtigsten Grundregeln zum Muskelaufbau",
  "Diät für Masseaufbau: Kalorien, Makros, Cheat Meals – die wichtigsten Grundregeln, um sauber und effektiv Muskelmasse aufzubauen, ohne unnötig Fett anzusetzen.",
  "Diät für Masseaufbau: Die wichtigsten Grundregeln zum Muskelaufbau",
  "Muskelaufbau funktioniert nicht ohne strukturierte Ernährung: Wer ektomorph veranlagt ist oder sauber aufbauen will, braucht die richtige Diät für Masse — Kalorienüberschuss, Makros und Timing im Überblick."),
 ("vergleich-von-trenbolone-acetate-und-enanthate-wirkung-dosierung.html",
  "Trenbolone Acetate vs Enanthate: Unterschied, Wirkung & Dosierung",
  "Trenbolone Acetate vs Enanthate: Wirkung, Dosierung und Unterschiede der zwei Ester – welche Variante für Cut und Masse, Nebenwirkungen und PCT.",
  "Trenbolone Acetate vs Enanthate: Unterschied, Wirkung & Dosierung",
  "Trenbolon Acetat und Trenbolon Enanthat sind zwei Ester desselben Wirkstoffs — der Unterschied steckt in der Halbwertszeit: Wir zeigen, welche Variante sich für welches Ziel eignet und wie sie dosiert wird."),
 ("mk-677-erfahrungen-test-bewertung-und-wirkung.html",
  "MK-677 Erfahrungen: Test, Bewertung, Wirkung & Ergebnis",
  "MK-677 Erfahrungen im Test: Wirkung, Bewertung und Ergebnisse von Ibutamoren – Schlaf, Appetit, Muskelaufbau und mögliche Nebenwirkungen im Ehrlichen Bericht.",
  "MK-677 Erfahrungen: Test, Bewertung, Wirkung & Ergebnis",
  "MK-677 (Ibutamoren) gehört zu den meistdiskutierten Wachstumshormon-Sekretagoga — echte Erfahrungen zeigen, was das Präparat für Schlaf, Appetit und Muskelaufbau wirklich leistet und welche Effekte ausbleiben."),
 ("ostarine-mk-2866-wirkungen-meinungen-dosierung.html",
  "Ostarine (MK-2866): Wirkungen, Meinungen & Dosierung erklärt",
  "Ostarine (MK-2866) kaufen und dosieren: Wirkungen auf Muskelaufbau und Joints, Meinungen aus der Praxis und die richtige Dosierung für Einsteiger.",
  "Ostarine (MK-2866): Wirkungen, Meinungen & Dosierung erklärt",
  "Ostarine (MK-2866) gehört zu den am besten erforschten SARMs: Wir zeigen alle Wirkungen, Erfahrungen aus der Praxis und die richtige Dosierung – auch für Einsteiger."),
 ("ratatrutid-vs-tirzepatid.html",
  "Retatrutid vs Tirzepatid: Welches Abnehm-Peptid gewinnt den Vergleich?",
  "Retatrutid vs Tirzepatid: Was ist besser zum Abnehmen? Wirkung, Gewichtsverlust-Daten, Dosierung und Nebenwirkungen im direkten Vergleich der GLP-1-Klasse.",
  "Retatrutid vs Tirzepatid: Welches Abnehm-Peptid gewinnt den Vergleich?",
  "Zwei der wirksamsten GLP-1-basierten Medikamente stehen in direktem Wettbewerb: Retatrutid und Tirzepatid — wir vergleichen Wirkungsweise, Klinik-Daten, Dosierung und Nebenwirkungen für die Entscheidung zum Abnehmen."),
 ("was-sind-die-sichersten-sarms.html",
  "Sicherste SARMs 2026: Liste, Erfahrungen & Risiken im Vergleich",
  "Sicherste SARMs im Vergleich: Ostarine, Ligandrol, RAD-140, MK-677 – wo liegen die tatsächlichen Risiken und welche SARM ist am besten für Einsteiger dokumentiert?",
  "Sicherste SARMs 2026: Liste, Erfahrungen & Risiken im Vergleich",
  "Nicht alle SARMs tragen das gleiche Risiko: Manche sind klinisch sehr gut dokumentiert, andere kaum erforscht — wir zeigen die sichersten SARMs mit Erfahrungen und Risikoprofil für Einsteiger und Fortgeschrittene."),
 ("wie-loest-man-peptide-auf-und-wie-berechnet-man-die-dosis.html",
  "Peptide auflösen & Dosierung berechnen: Die komplette Anleitung",
  "Peptide auflösen und die Dosis berechnen: Schritt-für-Schritt-Anleitung für BPC-157, TB-500 und Co – mit Rechenbeispielen und Fehler-Tipps.",
  "Peptide auflösen & Dosierung berechnen: Die komplette Anleitung",
  "Lyophilisierte Peptide wie BPC-157, TB-500 oder Melanotan-2 werden als Trockensubstanz geliefert und müssen erst aufgelöst und dosiert werden — diese Anleitung zeigt Schritt für Schritt, wie es sicher und exakt gelingt."),
 ("essenzielle-supplemente-auf-dem-steroidzyklus.html",
  "Supplemente im Steroidzyklus: Die essenziellen Unterstützer",
  "Essenzielle Supplemente auf dem Steroidzyklus: Leber, Herz, Gelenke & Testosteron schützen – Omega-3, TUDCA, Vitamin D und mehr im Überblick.",
  "Supplemente im Steroidzyklus: Die essenziellen Unterstützer",
  "Ein anaboler Zyklus verändert mehr als nur das Äußere: Leber, Herz, Gelenke und der eigene Hormonhaushalt arbeiten schwerer — die essenziellen Supplemente im Zyklus schützen genau diese Systeme."),
]

def sec_faq(q, a):
    return ('<div class="sk-faq__item">\n    <p class="sk-faq__q">' + q + '</p>\n    <p class="sk-faq__a">' + a + '</p>\n  </div>')

QUESTIONS = {
 "wie-behandelt-man-sexuelle-funktionsstoerungen.html": ("Kann ich sexuelle Funktionsstörungen während der Kur behandeln?",
   "Ja — die häufigsten Ursachen (zu hohes Östrogen, Prolaktin-Anstieg oder Testosteron-Mangel nach PCT) lassen sich gezielt angehen: Aromatasehemmer, Prolaktin-Kontrolle und ausreichend Testosteron-Basis. Unser Shop liefert passende Produkte diskret in ganz Deutschland."),
 "retatrutid-2026-vom-labor-zum-staerksten-adipositas-medikament-der-klinischen-forschung.html": ("Wo kann ich Retatrutid kaufen?",
   "Retatrutid ist in Deutschland nicht zugelassen und daher nicht regulär in der Apotheke erhältlich. Ähnliche GLP-1-Präparate und Alternativen zur Gewichtsreduktion finden Sie in unserem Shop — diskreter Versand in ganz Deutschland."),
 "kagrilintid-beim-abnehmen.html": ("Ist Kagrilintid in Deutschland verfügbar?",
   "Kagrilintid (Cagrilintide) befindet sich noch in klinischen Studien und ist nicht zugelassen. In unserem Shop finden Sie Alternativen zur Gewichtsreduktion aus derselben Wirkstoffklasse — diskreter Versand nach ganz Deutschland."),
 "winstrol-zyklus-wirkung-und-nutzen.html": ("Wo kann ich Winstrol kaufen?",
   "Winstrol (Stanozolol) ist in Deutschland nicht legal erhältlich. Unser Sortiment umfasst legale Alternativen und PCT-Produkte mit diskretem Versand in ganz Deutschland — informieren Sie sich vor dem Kauf über die rechtliche Lage."),
 "diaet-fuer-masse-grundregeln.html": ("Wie viele Kalorien brauche ich für die Massephase?",
   "Als Faustregel: +10–15 % über dem Erhaltungsumsatz, je nach Trainingsumfang. Rechnen Sie 2 g Eiweiß pro kg Körpergewicht, füllen Sie den Rest mit Kohlenhydraten und Fett. Ein Überschuss von 300–500 kcal bringt in 12 Wochen sichtbare Masse."),
 "vergleich-von-trenbolone-acetate-und-enanthate-wirkung-dosierung.html": ("Kann ich Trenbolone in diesem Shop kaufen?",
   "Trenbolone ist in Deutschland nicht legal erhältlich. Für cut- und massbezogene Alternativen sowie PCT-Unterstützung finden Sie in unserem Sortiment diskrete Lieferung in ganz Deutschland."),
 "mk-677-erfahrungen-test-bewertung-und-wirkung.html": ("Kann ich MK-677 legal in Deutschland kaufen?",
   "MK-677 (Ibutamoren) wird als Research-Chemical gehandelt und ist nicht als Medikament zugelassen. Wir versenden vergleichbare Sekretagoge und Regenerations-Produkte diskret in ganz Deutschland."),
 "ostarine-mk-2866-wirkungen-meinungen-dosierung.html": ("Wo kann ich Ostarine (MK-2866) kaufen?",
   "Ostarine wird als Research-Chemical gehandelt und ist in Deutschland nicht als Arzneimittel zugelassen. Unser Shop bietet Alternativen für Muskelaufbau und Regeneration — diskreter Versand in ganz Deutschland."),
 "ratatrutid-vs-tirzepatid.html": ("Sind Retatrutid und Tirzepatid rezeptfrei erhältlich?",
   "Nein — beide Wirkstoffe sind (noch) nicht frei verkäuflich: Tirzepatid (Mounjaro) ist verschreibungspflichtig, Retatrutid steckt in klinischen Studien. Ähnliche GLP-1-Analoga und Abnehm-Unterstützung finden Sie in unserem Shop."),
 "was-sind-die-sichersten-sarms.html": ("Kann ich die sichersten SARMs in diesem Shop kaufen?",
   "SARMs werden als Research-Chemicals gehandelt und sind in Deutschland nicht zugelassen. In unserem Sortiment finden Sie SARMs und Alternativen mit diskretem Versand in ganz Deutschland — prüfen Sie vorher die rechtliche Lage."),
 "wie-loest-man-peptide-auf-und-wie-berechnet-man-die-dosis.html": ("Wo kann ich qualitativ hochwertige Peptide kaufen?",
   "Hochwertige lyophilisierte Peptide (BPC-157, TB-500 u. a.) finden Sie in unserem Sortiment mit diskretem Versand in ganz Deutschland. Achten Sie auf den Preis pro mg und ein aktuelles Analysezertifikat."),
 "essenzielle-supplemente-auf-dem-steroidzyklus.html": ("Kann ich die essenziellen Supplemente hier kaufen?",
   "Viele der essenziellen Zyklus-Supplemente (TUDCA, Omega-3, Vitamin D, Zink u. a.) finden Sie in unserem Sortiment — ebenso wie Zyklus-Unterstützer und PCT-Produkte mit diskretem Versand in ganz Deutschland."),
}

for fn, title, meta, h1, lead in EDITS:
    path = os.path.join(DIR, fn)
    if not os.path.exists(path):
        print("ABSENT:", fn); continue
    q, a = QUESTIONS[fn]
    src = open(path, encoding="utf-8", errors="replace").read()

    m = re.search(r"<title>.*?</title>", src); assert m, fn+" title"
    src = src[:m.start()] + "<title>" + title + "</title>" + src[m.end():]

    m = re.search(r'(<meta\s+name="description"\s+content=")[^"]*"', src); assert m, fn+" meta"
    src = src[:m.start()] + m.group(1) + meta + '"' + src[m.end():]

    m = re.search(r"<h1[^>]*>.*?</h1>", src, re.S); assert m, fn+" h1"
    src = src[:m.start()] + "<h1>" + h1 + "</h1>" + src[m.end():]

    m = re.search(r'<p class="sk-lead"[^>]*>\s*', src); assert m, fn+" lead"
    src = src[:m.end()] + lead + " " + src[m.end():]

    idx = src.rfind("sk-faq__item")
    if idx == -1:
        # 2 cas : FAQ au format <details class="sk-faq"> OU pas de FAQ du tout.
        di = src.rfind('<details class="sk-faq">')
        if di != -1:
            # insérer un nouveau <details> juste après le dernier </details> du bloc
            end_det = src.find("</details>", di)
            while True:
                nxt = src.find("</details>", end_det + 1)
                if nxt == -1: break
                end_det = nxt
            item = '\n<details class="sk-faq"><summary>' + q + '</summary><p>' + a + '</p></details>'
            src = src[:end_det + len("</details>")] + item + src[end_det + len("</details>"):]
        else:
            ai = src.find('<div class="sk-cta-support">')
            assert ai != -1, fn + " cta"
            block = ('<div class="sk-faq">\n  <h2 class="sk-faq__title">Häufig gestellte Fragen</h2>\n  ' + sec_faq(q, a) + '\n</div>\n\n\n')
            src = src[:ai] + block + src[ai:]
    else:
        end_item = src.find("\n  </div>", idx); assert end_item != -1, fn + " fin"
        item = "\n  " + sec_faq(q, a)
        src = src[:end_item + len("\n  </div>")] + item + src[end_item + len("\n  </div>"):]

    open(path, "w", encoding="utf-8").write(src)
    print("OK", fn[:55])
print("\nTerminé.")