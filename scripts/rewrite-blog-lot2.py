# Réécriture ciblée lot 2 — les articles du blog déjà indexés en position de
# première page (0 clic) + requêtes exactes à volume. Même URL, même canonical.
import sys, re, os
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "..", "de", "blog", "post")

EDITS = [
 ("dianabol-vs-testosteron-was-ist-besser-fuer-deinen-ersten-cycle.html",
  "Dianabol vs Testosteron: Was ist besser für den ersten Cycle?",
  "Dianabol vs Testosteron: Welche Kur eignet sich für den ersten Cycle? Wirkung, Nebenwirkungen und Dosierung im direkten Vergleich – mit Kaufempfehlung.",
  "Dianabol vs Testosteron: Was ist besser für den ersten Cycle?",
  "Dianabol oder Testosteron für den ersten Zyklus? Vor der ersten Kur stehen die meisten Anwender vor genau dieser Frage: Dianabol oral oder Testosteron Enantat injizierbar — wir zeigen die Unterschiede, mit Kaufhinweisen für Deutschland.",
  "Kann ich Dianabol Tabletten kaufen?",
  "Dianabol Tabletten (Methandienon) sind in Deutschland nicht legal erhältlich — anders als unser Sortiment an Testosteron-Kuren und PCT-Produkten, die wir diskret in ganz Deutschland versenden. Informieren Sie sich vor dem Kauf über die rechtliche Lage."),

 ("steroide-und-blutbild-welche-werte-wir-kontrollieren-muessen-und-wie-oft.html",
  "Steroide und Blutbild: Welche Werte man vor und nach der Kur kontrollieren muss",
  "Steroide und Blutbild: Welche Werte sind vor, während und nach der Kur entscheidend? Leber, Cholesterin, Testosteron, LH/FSH – mit Ablauf und Häufigkeit.",
  "Steroide und Blutbild: Welche Werte man vor und nach der Kur kontrollieren muss",
  "Steroide und Blutbild gehören untrennbar zusammen: Anabole Steroide verändern unseren Körper nicht nur äußerlich, sondern auch Leberwerte, Cholesterin und Hormone. Dieser Ratgeber zeigt, welche Werte Sie wie oft kontrollieren sollten — für einen sicheren Zyklus.",
  "Welche Blutwerte sind nach einem Steroidzyklus am wichtigsten?",
  "Nach der Kur zählen vor allem Testosteron, LH, FSH, Leberwerte (ALT/AST, GGT) und das Lipidprofil (HDL/LDL). Ein vollständiges Blutbild 6 Wochen nach PCT-Ende gibt Sicherheit, dass sich der Hormonhaushalt erholt hat."),

 ("mk-677-kombinieren.html",
  "MK-677 kombinieren: Die besten Stack-Partner für Muskelaufbau",
  "MK-677 kombinieren: Mit welchen Substanzen erzielt man die besten Ergebnisse? Die besten Stack-Partner, Dosierung und wovon man die Finger lassen sollte.",
  "MK-677 kombinieren: Die besten Stack-Partner für Muskelaufbau",
  "MK-677 kombinieren heißt, das volle Potenzial des Wachstumshormon-Sekretagogums zu nutzen: Wir zeigen die besten Stack-Partner, die kombinierte Dosierung und worauf Sie verzichten sollten — damit der Stack effektiv und sicher bleibt.",
  "Kann man MK-677 überhaupt kaufen?",
  "MK-677 (Ibutamoren) wird als Research-Chemical gehandelt und ist in Deutschland nicht als Arzneimittel zugelassen. In unserem Shop finden Sie eine Auswahl an Wachstumshormon-Sekretagogen — diskreter Versand in ganz Deutschland."),

 ("prophylaxe-waehrend-eines-steroidzyklus.html",
  "Prophylaxe während des Steroidzyklus: Schutz von Leber, Herz & Nebenwirkungen",
  "Prophylaxe während des Steroidzyklus: Welche Medikamente schützen Leber, Blutdruck und Östrogenwerte wirklich? Der komplette Präventions-Guide für die Kur.",
  "Prophylaxe während des Steroidzyklus: Schutz von Leber, Herz & Nebenwirkungen",
  "Die Prophylaxe während des Steroidzyklus ist nicht optional — sie entscheidet darüber, ob ein Zyklus langfristig Fortschritt bringt oder Schäden hinterlässt. Welche Substanzen Leberschutz, Blutdruck und Östrogenkontrolle wirklich leisten, lesen Sie hier.",
  "Welche Prophylaxe-Medikamente brauche ich wirklich?",
  "Im Kern: einen Leberschutz (z. B. UDCA/TUDCA) bei oralen Steroiden, einen Aromatasehemmer bei hohen Testosterondosen, ein Blutdruck-Monitoring und ggf. Unterstützung des Lipidprofils. Die genaue Auswahl hängt vom Zyklus ab."),

 ("semaglutid-nebenwirkungen-vermeiden-dosierung-tipps-und-magenprobleme-gezielt-reduzieren.html",
  "Semaglutid Nebenwirkungen vermeiden: Dosierung, Tipps gegen Magenprobleme",
  "Semaglutid Nebenwirkungen vermeiden: Übelkeit, Durchfall und Magenprobleme gezielt reduzieren – mit der richtigen Dosierung und konkreten Alltagstipps.",
  "Semaglutid Nebenwirkungen vermeiden: Dosierung, Tipps gegen Magenprobleme",
  "Semaglutid Nebenwirkungen vermeiden, statt sie auszuhalten: Übelkeit, Durchfall und Verstopfung sind die häufigsten Begleiter — mit der richtigen Dosierung, Injektionsstelle und Ernährung lassen sie sich gezielt minimieren.",
  "Ist Semaglutid rezeptfrei in der Apotheke erhältlich?",
  "Nein — Semaglutid ist in Deutschland verschreibungspflichtig. Wer den Wirkstoff dennoch als Research-Chemical bestellen möchte, sollte die rechtliche Lage prüfen. Unser Shop versendet zugelassene Alternativen diskret in ganz Deutschland."),

 ("beste-hgh-peptide.html",
  "Beste HGH-Peptide 2026: Wirkung, Dosierung & Vergleich",
  "Beste HGH-Peptide: GHRP-6, Ipamorelin, CJC-1295 im Vergleich – Wirkung, Dosierung und welche Sekretagoge sich für Muskelaufbau und Fettabbau lohnen.",
  "Beste HGH-Peptide 2026: Wirkung, Dosierung & Vergleich",
  "Beste HGH-Peptide und ihre Wirkung im direkten Vergleich: GHRP-6, Ipamorelin, CJC-1295 stimulieren die körpereigene Wachstumshormon-Ausschüttung auf unterschiedliche Weise — wir zeigen, welches Peptid sich für welches Ziel lohnt.",
  "Welches HGH-Peptid ist am besten für Anfänger?",
  "Für Einsteiger empfehlen wir GHRP-6 oder Ipamorelin in moderater Dosierung — sie sind gut verträglich und machen das Prinzip der Sekretagoge verständlich. Beide finden Sie in unserem Sortiment mit diskretem Versand nach ganz Deutschland."),

 ("cardarine-in-kombination-mit-steroiden.html",
  "Cardarine in Kombination mit Steroiden: Wirkung & Dosierung (GW-501516)",
  "Cardarine (GW-501516) in Kombination mit Steroiden: Die ideale Ergänzung für Fettverbrennung und Ausdauer – Wirkung, Dosierung und Erfahrungen.",
  "Cardarine in Kombination mit Steroiden: Wirkung & Dosierung (GW-501516)",
  "Cardarine in Kombination mit Steroiden ist ein etablierter Klassiker: Der PPAR-δ-Agonist GW-501516 verbrennt Fett und steigert die Ausdauer, während die Anabolika den Muskelaufbau übernehmen. Wirkung, Dosierung und Risiken im Überblick — inklusive Kaufhinweis.",
  "Kann ich Cardarine ohne Probleme kombinieren?",
  "Cardarine wird häufig mit Testosteron oder SARMs kombiniert, da keine östrogenen Effekte auftreten. Wichtig ist eine moderate Dosierung (10–20 mg/Tag) und eine Zykluslänge von maximal 8 Wochen — unser Shop liefert GW-501516 diskret in ganz Deutschland."),

 ("vergleich-von-testosteron-cypionat-und-testosteron-enanthate.html",
  "Testosteron Cypionat vs Enanthate: Wirkung, Unterschied & Dosierung",
  "Testosteron Cypionat vs Enanthate: Wirkung, Halbwertszeit und welcher Ester sich für Einsteiger und Profis besser eignet – Vergleich mit Dosierung.",
  "Testosteron Cypionat vs Enanthate: Wirkung, Unterschied & Dosierung",
  "Testosteron Cypionat und Testosteron Enanthate sind die zwei meistgenutzten injizierbaren Testosteron-Ester weltweit — der Unterschied liegt in der Halbwertszeit und der Dosierungsfrequenz. Wir vergleichen beide Varianten für Einsteiger und Fortgeschrittene.",
  "Wie oft muss ich Cypionat bzw. Enanthate spritzen?",
  "Enanthate wird typischerweise alle 3,5–7 Tage injiziert, Cypionat alle 5–7 Tage — beide mit ähnlicher Wirkdauer. Die Wahl hängt v. a. von der Injektionsfrequenz ab, die Sie bevorzugen. Beide Testosteron-Ester finden Sie in unserem Shop."),
]

def sec_faq(q, a):
    return ('<div class="sk-faq__item">\n    <p class="sk-faq__q">' + q + '</p>\n    <p class="sk-faq__a">' + a + '</p>\n  </div>')

for fn, title, meta, h1, lead, q, a in EDITS:
    path = os.path.join(DIR, fn)
    if not os.path.exists(path):
        print("ABSENT:", fn); continue
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
        ai = src.find('<div class="sk-cta-support">')
        assert ai != -1, fn + " cta"
        block = ('<div class="sk-faq">\n  <h2 class="sk-faq__title">Häufig gestellte Fragen</h2>\n  ' + sec_faq(q, a) + '\n</div>\n\n\n')
        src = src[:ai] + block + src[ai:]
    else:
        end_item = src.find("\n  </div>", idx); assert end_item != -1, fn + " fin"
        item = "\n  " + sec_faq(q, a)
        src = src[:end_item + len("\n  </div>")] + item + src[end_item + len("\n  </div>"):]

    open(path, "w", encoding="utf-8").write(src)
    print("OK", fn[:60])
print("\nTerminé.")