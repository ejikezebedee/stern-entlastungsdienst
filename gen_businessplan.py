# -*- coding: utf-8 -*-
"""Generate the Stern Entlastungsdienst business plan PDF (German)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, HRFlowable,
                                ListFlowable, ListItem, KeepTogether)

FONT = "DejaVuSans"
FONT_B = "DejaVuSans-Bold"
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans-Oblique", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"))

OUT = "/home/boss/.openclaw/workspace/projects/stern-entlastungsdienst/Stern-Entlastungsdienst-Businessplan.pdf"

NAVY = colors.HexColor("#1f3a5f")
GOLD = colors.HexColor("#c9a227")
LIGHT = colors.HexColor("#eef2f7")
GREY = colors.HexColor("#5a5a5a")

styles = getSampleStyleSheet()

S = {}
S["title"] = ParagraphStyle("title", fontName=FONT_B, fontSize=26, leading=32,
                            textColor=NAVY, alignment=TA_CENTER, spaceAfter=6)
S["subtitle"] = ParagraphStyle("subtitle", fontName=FONT, fontSize=14, leading=20,
                               textColor=GREY, alignment=TA_CENTER, spaceAfter=4)
S["h1"] = ParagraphStyle("h1", fontName=FONT_B, fontSize=15, leading=20,
                         textColor=NAVY, spaceBefore=14, spaceAfter=6)
S["h2"] = ParagraphStyle("h2", fontName=FONT_B, fontSize=12, leading=16,
                         textColor=colors.HexColor("#2c4a6e"), spaceBefore=10, spaceAfter=4)
S["body"] = ParagraphStyle("body", fontName=FONT, fontSize=10, leading=14.5,
                           alignment=TA_JUSTIFY, spaceAfter=6)
S["bullet"] = ParagraphStyle("bullet", fontName=FONT, fontSize=10, leading=14,
                             alignment=TA_LEFT, leftIndent=14, spaceAfter=2)
S["tbl"] = ParagraphStyle("tbl", fontName=FONT, fontSize=9, leading=12)
S["tblb"] = ParagraphStyle("tblb", fontName=FONT_B, fontSize=9, leading=12)
S["small"] = ParagraphStyle("small", fontName=FONT, fontSize=8.5, leading=12,
                            textColor=GREY, alignment=TA_CENTER)
S["h2c"] = ParagraphStyle("h2c", parent=S["h2"], alignment=TA_CENTER)

def P(text, style="body"):
    return Paragraph(text, S[style])

def B(text):
    return ListFlowable([ListItem(Paragraph(t, S["bullet"]), leftIndent=14)
                         for t in text], bulletType="bullet", bulletFontName=FONT,
                        bulletFontSize=10, leftIndent=18)

def H(text):
    return Paragraph(text, S["h1"])

def H2(text):
    return Paragraph(text, S["h2"])

def TBL(header, rows, widths, align_right_cols=()):
    data = [[Paragraph(c, S["tblb"]) for c in header]]
    for r in rows:
        data.append([Paragraph(c, S["tbl"]) for c in r])
    t = Table(data, colWidths=widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#c8cfd8")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    for c in align_right_cols:
        style.append(("ALIGN", (c, 0), (c, -1), "RIGHT"))
    t.setStyle(TableStyle(style))
    return t

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(GREY)
    canvas.drawString(2*cm, 1.1*cm, "Stern Entlastungsdienst - Persönlich helfen. Digital organisieren.")
    canvas.drawRightString(A4[0]-2*cm, 1.1*cm, "Seite %d" % doc.page)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.2)
    canvas.line(2*cm, 1.35*cm, A4[0]-2*cm, 1.35*cm)
    canvas.restoreState()

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm,
                      topMargin=1.8*cm, bottomMargin=1.8*cm, title="Businessplan Stern Entlastungsdienst")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=footer)])

E = []
story = E

# ---------------- COVER ----------------
E.append(Spacer(1, 3.2*cm))
E.append(HRFlowable(width="60%", thickness=2, color=GOLD, hAlign="CENTER", spaceAfter=18))
E.append(P("Stern Entlastungsdienst", "title"))
E.append(P("Persönlich helfen. Digital organisieren.", "subtitle"))
E.append(Spacer(1, 0.6*cm))
S["bpt"] = ParagraphStyle("bpt", fontName=FONT_B, fontSize=18, leading=22, textColor=GOLD, alignment=TA_CENTER, spaceAfter=4)
E.append(P("Businessplan", "bpt"))
E.append(P("Ein innovatives Entlastungskonzept für pflegebedürftige Menschen und ihre Angehörigen", "subtitle"))
E.append(Spacer(1, 1.6*cm))
E.append(P("Standort: Duisburg, Nordrhein-Westfalen", "subtitle"))
E.append(P("Angebot zur Unterstützung im Alltag nach § 45a SGB XI", "subtitle"))
E.append(P("Stand: August 2026", "subtitle"))
E.append(PageBreak())

# ---------------- INHALTSVERZEICHNIS ----------------
E.append(H("Inhaltsverzeichnis"))
toc = [
    "1. Executive Summary",
    "2. Unternehmensvorstellung",
    "3. Geschäftsidee und Leistungsangebot",
    "4. Marktanalyse und Zielgruppe",
    "5. Marketing und Vertrieb",
    "6. Organisation und Personalstruktur",
    "7. Digitalisierung und App-Konzept",
    "8. Finanzplanung und Wirtschaftlichkeit",
    "9. Chancen- und Risikoanalyse",
    "10. Zukunftsvision und Wachstumsstrategie",
    "11. Fazit",
    "Anhang A: Anerkennungs- und Qualitätskonzept",
    "Anhang B: Datenschutzkonzept",
    "Anhang C: Regionalbüro Duisburg",
    "Anhang D: KI-Weiterbildungskonzept",
]
for t in toc:
    E.append(Paragraph(t, S["body"]))
E.append(PageBreak())

# ---------------- 1 EXECUTIVE SUMMARY ----------------
E.append(H("1. Executive Summary"))
E.append(P("Der Stern Entlastungsdienst ist ein Angebot zur Unterstützung im Alltag (sog. Alltagsbegleitung) "
           "für pflegebedürftige Menschen, Menschen mit Pflegegrad (1–5) und ihre pflegenden Angehörigen in Duisburg "
           "und im regionalen Umfeld (NRW). Wir verbinden persönliche, menschliche Betreuung mit einer modernen, "
           "digitalen Organisation – unser Leitbild lautet: <b>„Persönlich helfen. Digital organisieren.“</b>"))
E.append(P("Unsere Leistungen sind bewusst nicht-medizinisch: Haushaltshilfe, Einkäufe, Begleitung zu Arzt-, "
           "Behörden- und Freizeitterminen, gesellschaftliche Betreuung, Erledigungen sowie digitale Alltagshilfe. "
           "Dadurch entlasten wir pflegende Angehörige und ermöglichen es Menschen, möglichst lange selbstbestimmt "
           "in ihrem vertrauten Zuhause zu leben."))
E.append(P("<b>Finanzierung:</b> Unsere Leistungen werden über den monatlichen Entlastungsbetrag nach § 45b SGB XI "
           "(131 € pro Monat, erhöht zum 1. Januar 2025) abgerechnet – sowie perspektivisch über den Umwandlungsanspruch "
           "aus nicht ausgeschöpften Pflegesachleistungen. Dadurch entsteht für den Kunden ein staatlich finanzierter, "
           "wiederkehrender Leistungsanspruch, der häufig ungenutzt bleibt."))
E.append(P("<b>Wirtschaftlichkeit:</b> Wir kalkulieren mit einem Stundensatz von 28,50 €, einem Mindesteinsatz von "
           "120 Minuten und einer Abrechnung in 30-Minuten-Schritten. Der Break-even wird voraussichtlich bei rund "
           "25–30 Kunden erreicht. Die 3-Jahres-Planung zeigt einen kontrollierten Aufbau von ca. 44.400 € Umsatz im "
           "Jahr 1 auf ca. 148.100 € im Jahr 3."))
E.append(P("<b>Alleinstellungsmerkmal:</b> Während viele Anbieter noch mit Papier und Telefon arbeiten, setzen wir "
           "auf eine eigene digitale Einsatzplattform (Buchung, Einsatzplanung, Dokumentation, Abrechnung) mit "
           "perspektivisch KI-gestützter Organisation. Dies ist der Kern unserer Skalierbarkeit."))
E.append(PageBreak())

# ---------------- 2 UNTERNEHMENSVORSTELLUNG ----------------
E.append(H("2. Unternehmensvorstellung"))
E.append(H2("2.1 Unternehmensprofil"))
E.append(P("<b>Name:</b> Stern Entlastungsdienst<br/>"
           "<b>Slogan:</b> „Persönlich helfen. Digital organisieren.“<br/>"
           "<b>Standort:</b> Duisburg, Nordrhein-Westfalen (mobiler Dienst)<br/>"
           "<b>Rechtsform:</b> Einzelunternehmen / Kleinunternehmen<br/>"
           "<b>Status:</b> Gewerbe angemeldet, erste Bestandskunden vorhanden"))
E.append(H2("2.2 Gründerprofil und Motivation"))
E.append(P("Der Gründer bringt praktische Erfahrung aus der Betreuung von ca. 5–6 Bestandskunden mit und hat einen "
           "IHK-Gründungskurs absolviert; Kontakt zu Pflegekassen besteht bereits. Die Motivation ist die Verbindung "
           "von praktischer, persönlicher Hilfe mit modernen digitalen Arbeitsweisen, um die Alltagsorganisation für "
           "Kunden und Angehörige spürbar zu verbessern."))
E.append(H2("2.3 Leitbild"))
E.append(P("<b>Persönlich helfen:</b> Individuelle, zuverlässige und respektvolle Unterstützung für Pflegebedürftige "
           "und Angehörige – mit menschlicher Nähe als Kern."))
E.append(P("<b>Digital organisieren:</b> Einsatz moderner Technologien für intelligente Koordination, Vernetzung der "
           "Mitarbeitenden und optimale Kapazitätsnutzung."))
E.append(P("Drei Kernwerte prägen unsere Marke: <b>flexibel</b> (Organisation/Personal), <b>effizient</b> "
           "(App/Technik) und <b>menschlich</b> (Kundenkontakt)."))
E.append(PageBreak())

# ---------------- 3 GESCHAEFTSIDEE ----------------
E.append(H("3. Geschäftsidee und Leistungsangebot"))
E.append(H2("3.1 Geschäftsidee"))
E.append(P("Persönliche Unterstützung im Alltag für Menschen mit Pflegebedarf und ihre Angehörigen. Der Schwerpunkt "
           "liegt auf alltagsnahen Hilfen (Begleitung, Erledigungen, hauswirtschaftliche Unterstützung). Die "
           "Innovation ist die Kombination aus menschlicher Nähe und digitaler Einsatzplanung."))
E.append(H2("3.2 Leistungsangebot"))
E.append(H2("Alltagshilfe"))
E.append(B([
    "Unterstützung im Haushalt",
    "Ordnung und Struktur im Alltag",
    "Wäscheversorgung",
    "Leichte hauswirtschaftliche Tätigkeiten",
]))
E.append(H2("Begleitung und Unterstützung"))
E.append(B([
    "Begleitung zu Arztterminen",
    "Begleitung zu Behörden und wichtigen Terminen",
    "Unterstützung bei Besorgungen",
    "Spaziergänge und gesellschaftliche Betreuung",
]))
E.append(H2("Erledigungen"))
E.append(B([
    "Einkäufe",
    "Apothekengänge und Rezeptbesorgungen",
    "Post- und Botengänge",
    "Schriftverkehr",
]))
E.append(H2("Digitale Alltagshilfe"))
E.append(B([
    "Unterstützung bei Smartphone, Tablet und Computer",
    "Hilfe bei digitalen Anwendungen",
    "Unterstützung bei Online-Terminen",
]))
E.append(H2("3.3 Abrechnungsmodell"))
E.append(B([
    "<b>Stundensatz:</b> 28,50 €",
    "<b>Mindestdauer je Einsatz:</b> 120 Minuten (berücksichtigt Anfahrt, Vorbereitung, Durchführung, Dokumentation)",
    "<b>Abrechnungstakt:</b> 30-Minuten-Schritte",
    "<b>Finanzierung über Pflegekasse:</b> monatlicher Entlastungsbetrag nach § 45b SGB XI (131 €)",
    "<b>Perspektivisch:</b> Umwandlungsanspruch aus nicht ausgeschöpften Pflegesachleistungen",
]))
E.append(H2("3.4 Ablauf eines Einsatzes"))
E.append(B([
    "1. Anfrage durch Kunde oder Angehörige",
    "2. Bedarfsermittlung und Erstgespräch",
    "3. Planung des passenden Unterstützungsumfangs",
    "4. Terminvereinbarung",
    "5. Durchführung der Leistung",
    "6. Dokumentation des Einsatzes",
    "7. Rückmeldung und Qualitätssicherung",
]))
E.append(PageBreak())

# ---------------- 4 MARKTANALYSE ----------------
E.append(H("4. Marktanalyse und Zielgruppe"))
E.append(H2("4.1 Zielgruppen"))
E.append(B([
    "Pflegebedürftige Menschen mit anerkanntem Pflegegrad (1–5)",
    "Ältere Menschen mit Unterstützungsbedarf ohne Pflegegrad",
    "Menschen mit Einschränkungen im Alltag",
    "Pflegende Angehörige, die Entlastung benötigen",
]))
E.append(H2("4.2 Marktsituation"))
E.append(P("Deutschland altert; die Nachfrage nach alltagsunterstützenden Leistungen wächst kontinuierlich. "
           "Jeder Mensch mit Pflegegrad, der zuhause versorgt wird, erhält den Entlastungsbetrag von 131 € monatlich. "
           "Dieser Betrag verfällt häufig ungenutzt, weil Angehörige die Möglichkeiten nicht kennen oder die "
           "Antragswege als Hürde empfinden. Hier liegt unsere Chance: ein niedrigschwelliges, verständliches und "
           "digital organisiertes Angebot."))
E.append(P("Duisburg weist aufgrund der demografischen Entwicklung einen steigenden Bedarf an Unterstützung im "
           "Alltag, haushaltsnahen Dienstleistungen, Begleitung zu Terminen sowie Einkaufs- und Besorgungsdiensten auf."))
E.append(H2("4.3 Wettbewerbsvorteil"))
E.append(P("Die meisten kleinen Anbieter arbeiten noch papierbasiert und telefonisch. Unsere digitale Organisation "
           "(Einsatzplanung, Dokumentation, Abrechnung, Kundenportal) ist ein echtes Alleinstellungsmerkmal und "
           "ermöglicht Skalierung ohne überproportionalen Verwaltungsaufwand."))
E.append(PageBreak())

# ---------------- 5 MARKETING ----------------
E.append(H("5. Marketing und Vertrieb"))
E.append(H2("5.1 Online"))
E.append(B([
    "Eigene Website",
    "Google-Unternehmensprofil",
    "Facebook",
    "Instagram",
    "Perspektivisch eigene digitale Plattform/App",
]))
E.append(H2("5.2 Offline"))
E.append(B([
    "Flyer",
    "Ärzte und Fachärzte",
    "Pflegedienste",
    "Apotheken",
    "Seniorenbüros und Pflegestützpunkte",
    "Kirchengemeinden",
    "Krankenhäuser / Entlassmanagement & Sozialdienste (B2B)",
    "Empfehlungen zufriedener Kunden",
]))
E.append(H2("5.3 Vertriebsstrategie"))
E.append(P("Der Vertrieb setzt auf persönliche Beratung sowie Kooperationen mit Ärzten, Pflegekassen, "
           "Pflegestützpunkten, Tagespflegeeinrichtungen und dem Regionalbüro Alter, Pflege und Demenz NRW. "
           "Zusätzlich werden lokale Netzwerke mit Physiotherapeuten, Pflegediensten, Seniorenheimen und Hochschulen "
           "aufgebaut."))
E.append(PageBreak())

# ---------------- 6 ORGANISATION ----------------
E.append(H("6. Organisation und Personalstruktur"))
E.append(H2("6.1 Organisationsmodell"))
E.append(P("Im Mittelpunkt steht eine intelligente Einsatzplattform, die Kunden, Mitarbeitende und die Zentrale "
           "verbindet. Einsätze werden in klar definierten Einsatzpaketen organisiert, die über die mobile App flexibel "
           "angenommen werden können. Eine smarte regionale Einsatzplanung schlägt passende Einsätze in der Nähe vor, "
           "um Wege zu sparen und Ressourcen effizient zu nutzen."))
E.append(P("Das Modell ist besonders geeignet für flexible Beschäftigungsmodelle (Studierende, Teilzeitkräfte, "
           "geringfügig Beschäftigte) mit wechselnden Zeitfenstern. Die Vergütung erfolgt transparent und "
           "gesetzeskonform."))
E.append(H2("6.2 Personalaufbau"))
E.append(B([
    "<b>Jahr 1:</b> Inhaber, später erste studentische Unterstützung",
    "<b>Jahr 2:</b> 2–4 studentische Mitarbeitende, flexible Einsatzplanung",
    "<b>Jahr 3:</b> 5–8 studentische oder geringfügig Beschäftigte, Einsatzkoordination über digitale Prozesse",
]))
E.append(P("Grundsatz: Wohnortnahe Teilzeit- und Minijobkräfte verkürzen Wege und erhöhen die Reaktionsfähigkeit. "
           "Vollzeitstellen entstehen erst, wenn die Nachfrage dauerhaft ausreicht. Wo möglich werden feste "
           "Bezugspersonen eingesetzt; die digitale Organisation sichert eine nahtlose Vertretung bei Ausfällen."))
E.append(H2("6.3 Struktur Regionalbüro (perspektivisch)"))
E.append(B([
    "<b>Regionalleitung:</b> Gesamtkoordination, Qualitätskontrolle, Ansprechpartner für Behörden",
    "<b>Verwaltungskraft:</b> Kundendatenverwaltung, Terminorganisation, Dokumentation",
    "<b>Einsatzkoordination:</b> Dienstplanung, Koordination der Betreuungskräfte, Ausfallmanagement",
    "<b>Betreuungskräfte:</b> Durchführung der Entlastungsleistungen beim Kunden",
]))
E.append(PageBreak())

# ---------------- 7 DIGITALISIERUNG ----------------
E.append(H("7. Digitalisierung und App-Konzept"))
E.append(H2("7.1 Digitalisierungskonzept"))
E.append(P("Geplant ist der schrittweise Aufbau einer digitalen Unternehmensstruktur:"))
E.append(B([
    "Digitale Terminplanung und Einsatzverwaltung",
    "Automatische Dokumentation",
    "Digitale Formulare",
    "Kunden- und Mitarbeitendenverwaltung",
    "Automatisierte Rechnungsstellung",
    "Digitale Kommunikation",
    "KI-Unterstützung für Verwaltungsaufgaben",
    "Langfristig eine eigene App",
]))
E.append(H2("7.2 Software-Strategie (SaaS-first, insolvenzsicher)"))
E.append(P("Um das IT-Budget realistisch zu halten, erfolgt der Aufbau in Stufen: In den Jahren 1–2 wird etablierte, "
           "DSGVO-konforme White-Label-Pflegesoftware (z. B. TourCare, Mobile SystemCare) genutzt. Dies sichert sofortige "
           "Konformität, Schnittstellen zu Pflegekassen und ein angemessenes IT-Budget von 1.200–2.400 € p. a. Ab Jahr 3 "
           "erfolgt die schrittweise Eigenentwicklung einer App bzw. API-Anbindung, sobald das Kundenvolumen die "
           "Investition trägt."))
E.append(H2("7.3 App-Konzept (Zielbild)"))
E.append(P("Die App bildet die drei Nutzergruppen ab:"))
E.append(B([
    "<b>Familien/Kunden:</b> Buchung, Preisansicht (131-€-Budget vs. Privatleistung), Einsatzverfolgung, Rechnungen, Chat",
    "<b>Helfer/Personal:</b> Tagesplan, Navigation, Check-in/Check-out, Aufgabenliste, Einsatzbericht",
    "<b>Verwaltung:</b> Dashboard, Kunden-/Personalverwaltung, Einsatzplanung, Abrechnung, Berichte, Compliance",
]))
E.append(P("Die Abrechnung unterstützt zwei Modelle: Erstattung an die Familie sowie die Direktabrechnung mit der "
           "Pflegekasse (Entlastungsbetrag). Damit fließt die Abrechnung – wie gewünscht – direkt an die "
           "Versicherung/Pflegekasse."))
E.append(H2("7.4 KI-Konzept und DSGVO"))
E.append(P("KI wird eingesetzt, um Verwaltungsaufgaben zu automatisieren, Einsatzpläne intelligent zu erstellen, "
           "Dokumente zu verarbeiten und Arbeitsabläufe zu optimieren. Langfristig werden eigene KI-Agenten für "
           "organisatorische Prozesse entwickelt. Dadurch bleibt mehr Zeit für die eigentliche Betreuung."))
E.append(P("<b>DSGVO-Konformität (Art. 9 DSGVO):</b> KI- und Cloud-Systeme werden ausschließlich DSGVO-konform "
           "(EU-Hosting) betrieben. Sensible Gesundheitsdaten werden vor einer KI-gestützten Verarbeitung strikt "
           "pseudonymisiert bzw. anonymisiert; es erfolgt keine Übermittlung an US-Server."))
E.append(PageBreak())

# ---------------- 8 FINANZPLANUNG ----------------
E.append(H("8. Finanzplanung und Wirtschaftlichkeit"))
E.append(H2("8.1 Kalkulationsgrundlagen"))
E.append(B([
    "<b>Stundensatz:</b> 28,50 €",
    "<b>Mindesteinsatz:</b> 120 Minuten",
    "<b>Abrechnungstakt:</b> 30 Minuten",
    "<b>Wochen pro Monat:</b> 4,33",
    "<b>Entlastungsbetrag pro Kunde:</b> 131 € / Monat (ca. 4,6 Stunden Leistung)",
]))
E.append(H2("8.2 3-Jahres-Finanzplanung (Stundenmodell)"))
E.append(TBL(
    ["Jahr", "Stunden/Woche", "Monatsumsatz", "Jahresumsatz", "Kosten/Jahr", "Ergebnis vor Steuern"],
    [
        ["Jahr 1 – Aufbau", "30 h", "ca. 3.700 €", "ca. 44.400 €", "ca. 8.880 €", "ca. 35.520 €"],
        ["Jahr 2 – Wachstum", "60 h", "ca. 7.400 €", "ca. 88.800 €", "ca. 45.000 €", "ca. 43.800 €"],
        ["Jahr 3 – Ausbau", "100 h", "ca. 12.340 €", "ca. 148.100 €", "ca. 90.000 €", "ca. 58.100 €"],
    ],
    widths=[3.4*cm, 2.2*cm, 2.6*cm, 2.6*cm, 2.4*cm, 2.8*cm],
    align_right_cols=(2, 3, 4, 5),
))
E.append(Spacer(1, 0.3*cm))
E.append(H2("8.3 Kostenstruktur (jährlich)"))
E.append(TBL(
    ["Kostenart", "Jahr 1", "Jahr 2", "Jahr 3"],
    [
        ["Versicherung", "960 €", "1.200 €", "1.500 €"],
        ["Telefon/Internet", "720 €", "900 €", "1.200 €"],
        ["Software/Digitalisierung", "1.200 €", "2.400 €", "4.000 €"],
        ["Marketing", "1.800 €", "3.000 €", "5.000 €"],
        ["Fahrtkosten", "3.000 €", "6.000 €", "10.000 €"],
        ["Personal", "0 €", "31.500 €", "60.000 €"],
        ["Sonstige Kosten", "1.200 €", "2.000 €", "3.000 €"],
    ],
    widths=[7.0*cm, 3.0*cm, 3.0*cm, 3.0*cm],
    align_right_cols=(1, 2, 3),
))
E.append(Spacer(1, 0.3*cm))
E.append(H2("8.4 Monatliche Fixkosten zum Start (ca. 1.600 €)"))
E.append(TBL(
    ["Position", "Monatlich"],
    [
        ["Büromiete", "300 €"],
        ["Telefon/Internet", "50 €"],
        ["Software/Lizenzen", "80 €"],
        ["Betriebshaftpflicht/Versicherungen", "120 €"],
        ["Steuerberater/Buchhaltung", "150 €"],
        ["Werbung/Marketing", "250 €"],
        ["Fahrtkosten", "300 €"],
        ["Büromaterial/Druck", "100 €"],
        ["Sonstiges inkl. Bankgebühren", "250 €"],
        ["<b>Gesamt</b>", "<b>ca. 1.600 €</b>"],
    ],
    widths=[9.0*cm, 4.0*cm],
    align_right_cols=(1,),
))
E.append(Spacer(1, 0.3*cm))
E.append(H2("8.5 Break-even und Skalierung (Kundenmodell)"))
E.append(P("Alternative Betrachtung über den Entlastungsbetrag: Bei durchschnittlich 131 € Umsatz und ca. 70 € "
           "Personalkosten pro Kunde wird die Gewinnschwelle bei ca. 30 Kunden erreicht. Die Fixkosten steigen "
           "moderat mit jeder Wachstumsstufe (ca. 1.600 € zu Beginn bis ca. 2.500 € bei 500 Kunden)."))
E.append(H2("8.6 Wachstumsstufen (kapazitätskonsistent)"))
E.append(P("Die Kundenentwicklung ist bewusst mit der Stundenkapazität abgeglichen, um Engpässe zu vermeiden. "
           "Ein einzelner Gründer kann bei ca. 30–35 Direktstunden pro Woche realistisch 15–25 Kunden betreuen; "
           "weiteres Wachstum setzt zusätzliche Kräfte voraus."))
E.append(TBL(
    ["Zeitraum", "Phasen", "Kundenzahl"],
    [
        ["Jahr 1", "Phase 1–2", "5–15 Kunden (Aufbau)"],
        ["Jahr 1", "Phase 3–4", "15–25 Kunden (Kapazitätsgrenze 1 Gründer)"],
        ["Jahr 2", "Phase 5–6", "25–60 Kunden (erste Minijobber/Studierende)"],
        ["Jahr 3", "Phase 7–8", "60–120 Kunden (festes Team, digitale Skalierung)"],
    ],
    widths=[3.2*cm, 3.6*cm, 9.2*cm],
))
E.append(PageBreak())

# ---------------- 9 CHANCEN & RISIKEN ----------------
E.append(H("9. Chancen- und Risikoanalyse"))
E.append(H2("9.1 Chancen"))
E.append(B([
    "Hohe und demografisch wachsende Nachfrage",
    "Staatlich finanzierter, wiederkehrender Entlastungsbetrag (131 € / Monat)",
    "Effizienz- und Skalierungsvorteil durch digitale Tools",
    "Geringe Einstiegshürde (keine medizinische Qualifikation erforderlich)",
    "Differenzierung gegenüber papierbasierten Wettbewerbern",
]))
E.append(H2("9.2 Risiken und Gegenmaßnahmen"))
E.append(TBL(
    ["Risiko", "Gegenmaßnahme"],
    [
        ["Verzögerung der Anerkennung als Entlastungsdienst", "Frühzeitige Abstimmung mit Kommune und Pflegekasse; vollständige Unterlagen"],
        ["Verzögerungen bei App-Umsetzung", "Schrittweiser Aufbau; Start mit schlanker Lösung (Buchung/Planung)"],
        ["Begrenzte Startressourcen", "Nutzung von Förderungen (Bildungsgutschein, Gründungszuschuss)"],
        ["Personalfluktuation", "Attraktive, flexible Arbeitsmodelle; faire Vergütung; feste Bezugspersonen"],
        ["Regulatorische Änderungen (Landesrecht NRW)", "Kontinuierliche Beobachtung; Beratung durch Steuerberater und Verbände"],
        ["Zahlungs-/Abrechnungsrisiken", "Transparente Leistungsnachweise; Direktabrechnung mit Pflegekasse"],
    ],
    widths=[6.5*cm, 9.5*cm],
))
E.append(PageBreak())

# ---------------- 10 ZUKUNFTSVISION ----------------
E.append(H("10. Zukunftsvision und Wachstumsstrategie"))
E.append(P("Der Stern Entlastungsdienst soll sich von einem regionalen Anbieter zu einem modernen, digital "
           "unterstützten Dienstleistungsunternehmen entwickeln."))
E.append(H2("10.1 Langfristige Ziele"))
E.append(B([
    "Wirtschaftlich stabiles Unternehmen",
    "Moderne KI-gestützte Organisation",
    "Eigene digitale Plattform/App",
    "Hohe Servicequalität",
    "Attraktive Arbeitsplätze für Studierende und Teilzeitkräfte",
    "Nachhaltiges Wachstum",
]))
E.append(H2("10.2 Umsetzungsplan in 3 Phasen"))
E.append(TBL(
    ["Phase", "Schwerpunkt"],
    [
        ["Phase 1", "Gründung, erste Kunden, Anerkennungsverfahren"],
        ["Phase 2", "Digitalisierung (Einführung App zur Einsatzplanung), Weiterbildung der Gründerperson"],
        ["Phase 3", "Skalierung durch Aufbau eines Studierenden-Netzwerks mit KI-gestützter Organisation"],
    ],
    widths=[3.0*cm, 13.0*cm],
))
E.append(H2("10.3 Regionale Expansion"))
E.append(P("Nach der Stabilisierung in Duisburg erfolgt die schrittweise Expansion in die Nachbarstädte "
           "<b>Mülheim an der Ruhr</b>, <b>Oberhausen</b> und <b>Essen</b>. Die digitale Plattform macht diese "
           "Ausweitung ohne proportional steigenden Verwaltungsaufwand möglich."))
E.append(PageBreak())

# ---------------- 11 FAZIT ----------------
E.append(H("11. Fazit"))
E.append(P("Der Stern Entlastungsdienst verbindet ein bewährtes, staatlich finanziertes Geschäftsmodell "
           "(Entlastungsbetrag nach § 45b SGB XI) mit einer modernen, digitalen Organisation. Die Nachfrage ist "
           "demografisch gesichert, die Einstiegshürden sind niedrig und das digitale Alleinstellungsmerkmal "
           "ermöglicht nachhaltiges, kontrolliertes Wachstum. Mit der Anerkennung als Angebot zur Unterstützung im "
           "Alltag in NRW, einer soliden Finanzplanung und dem schrittweisen Aufbau der digitalen Plattform ist das "
           "Unternehmen gut positioniert, um Pflegebedürftige zu unterstützen und Angehörige nachhaltig zu entlasten."))
E.append(PageBreak())

# ---------------- ANHANG A ----------------
E.append(H("Anhang A: Anerkennungs- und Qualitätskonzept"))
E.append(P("<b>Ziel:</b> Anerkennung als Anbieter von Unterstützungsleistungen im Alltag nach den landesrechtlichen "
           "Vorgaben NRW (Anerkennungs- und Förderungsverordnung NRW)."))
E.append(H2("A.1 Rechtliche Grundlagen"))
E.append(B([
    "Abrechnung nach SGB XI und ergänzenden Regelungen des Landes NRW",
    "Entlastungsbetrag nach § 45b SGB XI",
    "Umwandlungsanspruch aus Pflegesachleistungen",
    "Zusammenarbeit mit Pflegekassen, Kommune und Behörden",
]))
E.append(H2("A.2 Qualifikation und Zuverlässigkeit"))
E.append(B([
    "Qualifikations- bzw. Schulungsnachweise",
    "Erweitertes Führungszeugnis (soweit erforderlich)",
    "Belehrung nach Infektionsschutzgesetz (falls erforderlich)",
    "Nachweis Erste-Hilfe-Schulung (falls vorhanden)",
    "Verpflichtung zur Verschwiegenheit und zum Datenschutz",
]))
E.append(P("<b>Fachleitung (AnFöVO NRW):</b> Um den Vorgaben der Anerkennungs- und Förderungsverordnung NRW "
           "vollumfänglich zu entsprechen, wird bei Bedarf eine examinierte Pflegefachkraft (z. B. auf Minijob-Basis "
           "oder als freie Mitarbeiterin) für Qualitätskontrolle und Fachleitung vertraglich gebunden."))
E.append(H2("A.3 Qualitätsmanagement"))
E.append(B([
    "Auswahl und strukturierte Einarbeitung der Mitarbeitenden",
    "Fachgerechte Dokumentation jedes Einsatzes",
    "Datenschutz und Schweigepflicht",
    "Transparentes Beschwerdemanagement",
    "Regelmäßige Fortbildungen",
]))
E.append(H2("A.4 Fortbildungsthemen"))
E.append(B([
    "Kommunikation und Gesprächsführung",
    "Umgang mit Menschen mit Demenz",
    "Erste Hilfe",
    "Datenschutz (DSGVO)",
    "Hygiene und Infektionsschutz",
    "Arbeitssicherheit",
    "Umgang mit Notfallsituationen",
]))
E.append(H2("A.5 Benötigte Unterlagen (Anlagen)"))
E.append(B([
    "Anlage 1: Einsatzdokumentation / Leistungsnachweis",
    "Anlage 2: Erstaufnahmebogen",
    "Anlage 3: Beschwerdeformular",
    "Anlage 4: Datenschutz- und Verschwiegenheitserklärung",
    "Anlage 5: Einwilligung zur Datenverarbeitung",
    "Anlage 6: Qualifikationsnachweise",
    "Anlage 7: Erweitertes Führungszeugnis (falls erforderlich)",
    "Anlage 8: Weitere Nachweise (Erste Hilfe, Fortbildungen)",
]))
E.append(PageBreak())

# ---------------- ANHANG B ----------------
E.append(H("Anhang B: Datenschutzkonzept"))
E.append(P("Grundlage: Datenschutz-Grundverordnung (DSGVO), Bundesdatenschutzgesetz (BDSG) und geltende "
           "landesrechtliche Vorgaben."))
E.append(H2("B.1 Verarbeitete Daten"))
E.append(B([
    "Kundendaten (Name, Anschrift, Kontakt, ggf. Geburtsdaten, Einsatzdaten)",
    "Angehörigendaten (Name, Telefon, Kontakt für Abstimmungen)",
    "Mitarbeitendendaten (persönliche Daten, Qualifikation, Einsatzplanung)",
]))
E.append(H2("B.2 Grundsätze"))
E.append(B([
    "Zweckbindung – Daten nur für notwendige Zwecke",
    "Datensparsamkeit – nur erforderliche Informationen",
    "Vertraulichkeit – keine unbefugte Weitergabe",
    "Sicherheit – geschützte Speicherung und Verarbeitung",
]))
E.append(H2("B.3 Technische und organisatorische Maßnahmen (TOM)"))
E.append(B([
    "Passwortgeschützte Systeme",
    "Regelmäßige Software-Updates",
    "Zugriff nur für berechtigte Personen",
    "Verschlossene Aufbewahrung von Papierunterlagen",
    "Regelmäßige Datensicherung",
]))
E.append(H2("B.4 Aufbewahrung und Löschung"))
E.append(P("Daten werden nur so lange gespeichert, wie gesetzliche oder organisatorische Zwecke es erfordern. "
           "Danach erfolgt die sichere Löschung digitaler Daten bzw. datenschutzgerechte Vernichtung von "
           "Papierunterlagen."))
E.append(PageBreak())

# ---------------- ANHANG C ----------------
E.append(H("Anhang C: Regionalbüro Duisburg"))
E.append(H2("C.1 Standort und Aufgaben"))
E.append(P("Das Regionalbüro Duisburg dient als zentrale Anlaufstelle für Kunden, Mitarbeitende, "
           "Kooperationspartner und Behörden."))
E.append(B([
    "Beratung von Pflegebedürftigen und Angehörigen",
    "Aufnahme und Verwaltung neuer Kundenanfragen",
    "Bedarfsanalyse und individuelle Hilfeplanung",
    "Einsatzplanung und Koordination der Betreuungskräfte",
    "Mitarbeiterverwaltung und Begleitung",
    "Qualitätssicherung, Dokumentation und Datenschutz",
    "Zusammenarbeit mit Pflegekassen und Netzwerkpartnern",
]))
E.append(H2("C.2 Räumliche Ausstattung"))
E.append(B([
    "Beratungsbereich für Kundengespräche",
    "Arbeitsplatz für Verwaltung und Organisation",
    "Datenschutzgerechte Ablagemöglichkeiten",
    "Telefon- und digitale Kommunikationsmöglichkeiten",
    "Besprechungsmöglichkeit und Schulungsmaterialien",
]))
E.append(H2("C.3 Öffnungszeiten"))
E.append(P("<b>Bürozeiten:</b> Montag–Freitag 08:00–16:00 Uhr<br/>"
           "<b>Telefonische Erreichbarkeit:</b> Montag–Freitag 08:00–18:00 Uhr<br/>"
           "<b>Nach Vereinbarung:</b> Beratungstermine außerhalb der Öffnungszeiten möglich"))
E.append(H2("C.4 Entwicklungsperspektive"))
E.append(B([
    "Aufbau eines festen Mitarbeiterteams",
    "Ausbau des Kundenstamms",
    "Erweiterung des Unterstützungsangebots",
    "Zusammenarbeit mit weiteren regionalen Partnern",
    "Nachhaltige Versorgung als regionaler Mittelpunkt",
]))
E.append(PageBreak())

# ---------------- ANHANG D ----------------
E.append(H("Anhang D: KI-Weiterbildungskonzept"))
E.append(P("Zur digitalen Weiterentwicklung des Unternehmens wird eine strukturierte KI-Weiterbildung angestrebt "
           "(Förderung über Bildungsgutschein)."))
E.append(H2("D.1 Lernpfad (6–9 Monate, 3 Stufen)"))
E.append(TBL(
    ["Stufe", "Dauer", "Inhalte"],
    [
        ["Stufe 1 – KI-Grundlagen", "ca. 2 Monate", "KI-Grundlagen, ChatGPT, Prompt Engineering, Datenschutz"],
        ["Stufe 2 – KI im Unternehmen", "2–3 Monate", "Prozessanalyse, KI-Einführung, Projektmanagement"],
        ["Stufe 3 – Spezialisierung", "2–4 Monate", "Python, APIs, KI-Agenten, Cloud, eigenes Praxisprojekt"],
    ],
    widths=[5.5*cm, 2.5*cm, 8.0*cm],
))
E.append(H2("D.2 Mögliche Anbieter in Duisburg"))
E.append(B([
    "COMCAVE Duisburg (KI, Prompt Engineering, Python, Datenanalyse)",
    "DAA – Deutsche Angestellten-Akademie (IT, Digitalisierung)",
    "Niederrheinische IHK Duisburg-Wesel-Kleve (KI-Zertifikatslehrgänge)",
]))
E.append(H2("D.3 Qualifikationskette"))
E.append(P("KI-Grundlagen → Prompt Engineer → <b>KI-Manager (IHK)</b> → KI-Governance/EU AI Act → "
           "KI-Multiplikator oder KI-Beauftragter"))
E.append(Spacer(1, 1.0*cm))
E.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=8))
E.append(P("Dieser Businessplan dient der Unternehmensplanung sowie als Grundlage für Gespräche mit Jobcenter, "
           "Regionalbüro und Banken. Er stellt keine Rechts- oder Steuerberatung dar. Die Anerkennungsregeln NRW sind "
           "mit der Kommune Duisburg und der zuständigen Pflegekasse, die steuerliche Behandlung mit einem "
           "Steuerberater abzustimmen.", "small"))

doc.build(story)
print("PDF written:", OUT)
