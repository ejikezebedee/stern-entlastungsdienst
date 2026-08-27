# -*- coding: utf-8 -*-
"""Generate the Stern Entlastungsdienst Begleitdokumente (supporting documents) PDF for Jobcenter."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, HRFlowable,
                                ListFlowable, ListItem)

FONT = "DejaVuSans"
FONT_B = "DejaVuSans-Bold"
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont("DejaVuSans", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("DejaVuSans-Bold", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))

OUT = "/home/boss/.openclaw/workspace/projects/stern-entlastungsdienst/Stern-Entlastungsdienst-Begleitdokumente.pdf"

NAVY = colors.HexColor("#1f3a5f")
GOLD = colors.HexColor("#c9a227")
LIGHT = colors.HexColor("#eef2f7")
GREY = colors.HexColor("#5a5a5a")

S = {}
S["title"] = ParagraphStyle("title", fontName=FONT_B, fontSize=24, leading=30, textColor=NAVY, alignment=TA_CENTER, spaceAfter=6)
S["subtitle"] = ParagraphStyle("subtitle", fontName=FONT, fontSize=13, leading=19, textColor=GREY, alignment=TA_CENTER, spaceAfter=4)
S["h1"] = ParagraphStyle("h1", fontName=FONT_B, fontSize=15, leading=20, textColor=NAVY, spaceBefore=14, spaceAfter=6)
S["h2"] = ParagraphStyle("h2", fontName=FONT_B, fontSize=12, leading=16, textColor=colors.HexColor("#2c4a6e"), spaceBefore=10, spaceAfter=4)
S["body"] = ParagraphStyle("body", fontName=FONT, fontSize=10, leading=14.5, alignment=TA_JUSTIFY, spaceAfter=6)
S["bullet"] = ParagraphStyle("bullet", fontName=FONT, fontSize=10, leading=14, alignment=TA_LEFT, leftIndent=14, spaceAfter=2)
S["tbl"] = ParagraphStyle("tbl", fontName=FONT, fontSize=9, leading=12)
S["tblb"] = ParagraphStyle("tblb", fontName=FONT_B, fontSize=9, leading=12)
S["small"] = ParagraphStyle("small", fontName=FONT, fontSize=8.5, leading=12, textColor=GREY, alignment=TA_CENTER)
S["bpt"] = ParagraphStyle("bpt", fontName=FONT_B, fontSize=17, leading=22, textColor=GOLD, alignment=TA_CENTER, spaceAfter=4)

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
    canvas.drawString(2*cm, 1.1*cm, "Stern Entlastungsdienst - Begleitdokumente zum Businessplan")
    canvas.drawRightString(A4[0]-2*cm, 1.1*cm, "Seite %d" % doc.page)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.2)
    canvas.line(2*cm, 1.35*cm, A4[0]-2*cm, 1.35*cm)
    canvas.restoreState()

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm,
                      topMargin=1.8*cm, bottomMargin=1.8*cm, title="Begleitdokumente Stern Entlastungsdienst")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=footer)])

E = []

# COVER
E.append(Spacer(1, 3.0*cm))
E.append(HRFlowable(width="60%", thickness=2, color=GOLD, hAlign="CENTER", spaceAfter=18))
E.append(P("Stern Entlastungsdienst", "title"))
E.append(P("Persönlich helfen. Digital organisieren.", "subtitle"))
E.append(Spacer(1, 0.6*cm))
E.append(P("Begleitdokumente zum Businessplan", "bpt"))
E.append(P("Kapitalbedarf · Finanzierung · Lebenslauf · Zeitplan · Checkliste", "subtitle"))
E.append(Spacer(1, 1.4*cm))
E.append(P("Standort: Duisburg, Nordrhein-Westfalen", "subtitle"))
E.append(P("Stand: August 2026", "subtitle"))
E.append(PageBreak())

# 1 KAPITALBEDARF
E.append(H("1. Kapitalbedarfs- und Finanzierungsplan"))
E.append(P("Dieser Plan ergänzt Kapitel 8 des Businessplans. Er zeigt, welches Startkapital benötigt wird, "
           "womit es gedeckt wird und wie die Liquidität in der Anlaufphase gesichert ist. Alle Beträge sind "
           "Schätzwerte und vor Einreichung zu verifizieren."))

E.append(H2("1.1 Einmalige Gründungs- und Anlaufkosten"))
E.append(TBL(
    ["Position", "Betrag"],
    [
        ["Gewerbeanmeldung (Stadt Duisburg)", "ca. 40 €"],
        ["IHK-Grundbeitrag (Einzelunternehmen, oft befreit)", "0–100 €"],
        ["Erstausstattung Büro / IT (Notebook, Telefon, Möbel)", "ca. 500 €"],
        ["Marketing-Start (Website, Flyer, Google-Profil)", "ca. 500 €"],
        ["Kautions-/Nebenkosten Büro (falls Büro angemietet)", "ca. 300 €"],
        ["<b>Summe einmalige Kosten</b>", "<b>ca. 1.400–1.500 €</b>"],
    ],
    widths=[11.0*cm, 5.0*cm],
    align_right_cols=(1,),
))
E.append(Spacer(1, 0.3*cm))

E.append(H2("1.2 Laufende Fixkosten (monatlich, aus Businessplan Kap. 8.4)"))
E.append(P("Monatliche Fixkosten zum Start: <b>ca. 1.600 €</b> (Büromiete 300 €, Telefon/Internet 50 €, "
           "Software 80 €, Versicherung 120 €, Steuerberater 150 €, Werbung 250 €, Fahrtkosten 300 €, "
           "Büromaterial 100 €, Sonstiges 250 €)."))

E.append(H2("1.3 Kapitalbedarf für die Anlaufphase"))
E.append(P("Bis zum Erreichen der Gewinnschwelle (ca. 25–30 Kunden) wird eine Anlaufphase von 6 Monaten "
           "angesetzt. Der Gründer startet bereits mit ca. 5–6 Bestandskunden, sodass ein Teil der Fixkosten "
           "früh durch Umsatz gedeckt wird."))
E.append(TBL(
    ["Position", "Berechnung", "Betrag"],
    [
        ["Einmalige Kosten", "siehe 1.1", "ca. 1.500 €"],
        ["6 Monate Fixkosten", "6 × 1.600 €", "ca. 9.600 €"],
        ["Liquiditätsreserve / Unvorhergesehenes", "ca. 1 Monat Fixkosten", "ca. 1.600 €"],
        ["<b>Gesamter Kapitalbedarf (Anlauf)</b>", "", "<b>ca. 12.700 €</b>"],
    ],
    widths=[7.0*cm, 5.0*cm, 4.0*cm],
    align_right_cols=(2,),
))
E.append(P("<b>Hinweis:</b> Da bereits Bestandskunden vorhanden sind, reduziert sich der tatsächliche "
           "Finanzierungsbedarf durch laufende Einnahmen. Der ausgewiesene Betrag ist die konservative "
           "Obergrenze."))

E.append(H2("1.4 Finanzierung"))
E.append(TBL(
    ["Finanzierungsquelle", "Betrag"],
    [
        ["Eigenmittel des Gründers", "ca. 2.000–3.000 €"],
        ["Gründungszuschuss (Jobcenter, § 16b SGB II / § 93 SGB III)", "beantragt – Höhe offen"],
        ["Bildungsgutschein (KI-Weiterbildung)", "separat beantragt"],
        ["<b>Gesamt</b>", "<b>offen</b>"],
    ],
    widths=[11.0*cm, 5.0*cm],
    align_right_cols=(1,),
))
E.append(PageBreak())

# 2 LIQUIDITAET
E.append(H("2. Liquiditätsplanung (Anlaufphase, vereinfacht)"))
E.append(P("Schematische Monatsübersicht der ersten 6 Monate. Die Umsätze wachsen mit dem Kundenaufbau "
           "(vgl. Wachstumsstufen im Businessplan)."))
E.append(TBL(
    ["Monat", "Kunden", "Umsatz (131 €/Kunde)", "Fixkosten", "Saldo kumuliert"],
    [
        ["Monat 1", "6", "786 €", "1.600 €", "− 814 €"],
        ["Monat 2", "9", "1.179 €", "1.600 €", "− 1.235 €"],
        ["Monat 3", "13", "1.703 €", "1.600 €", "− 1.132 €"],
        ["Monat 4", "18", "2.358 €", "1.600 €", "− 374 €"],
        ["Monat 5", "23", "3.013 €", "1.600 €", "+ 1.039 €"],
        ["Monat 6", "28", "3.668 €", "1.600 €", "+ 3.107 €"],
    ],
    widths=[2.6*cm, 2.4*cm, 4.0*cm, 3.0*cm, 4.0*cm],
    align_right_cols=(2, 3, 4),
))
E.append(P("<b>Erläuterung:</b> Ab ca. 25–30 Kunden (Monat 5–6) ist die Gewinnschwelle erreicht und der "
           "laufende Betrieb trägt sich selbst. Die kumulierte Unterdeckung der ersten Monate wird durch "
           "Eigenmittel bzw. den Gründungszuschuss überbrückt."))
E.append(PageBreak())

# 3 LEBENSLAUF
E.append(H("3. Lebenslauf-Vorlage (Gründer)"))
E.append(P("Bitte ausfüllen und unterschrieben beifügen. Der Lebenslauf ist eine Standardanlage zum "
           "Gründungszuschuss-Antrag."))
E.append(H2("Persönliche Daten"))
E.append(P("Name: ____________________________________________<br/>"
           "Anschrift: ____________________________________________<br/>"
           "Telefon / E-Mail: ____________________________________________<br/>"
           "Geburtsdatum / -ort: ____________________________________________"))
E.append(H2("Beruflicher Werdegang"))
E.append(P("(Zeitraum – Tätigkeit / Arbeitgeber – in Stichpunkten)")
        )
E.append(Spacer(1, 1.2*cm))
E.append(HRFlowable(width="100%", thickness=0.5, color=GREY, spaceAfter=10))
E.append(Spacer(1, 1.2*cm))
E.append(HRFlowable(width="100%", thickness=0.5, color=GREY, spaceAfter=10))
E.append(Spacer(1, 1.2*cm))
E.append(H2("Qualifikationen & Schulungen"))
E.append(P("• IHK-Gründungskurs (absolviert)<br/>"
           "• Geplant: KI-Weiterbildung (Bildungsgutschein)<br/>"
           "• Erste-Hilfe-Schulung (falls vorhanden)<br/>"
           "• Weitere: ____________________________________________"))
E.append(H2("Erfahrung in der Betreuung"))
E.append(P("Betreuung von ca. 5–6 Bestandskunden im Bereich Alltagsbegleitung / Unterstützung im Alltag. "
           "Kontakt zu Pflegekassen besteht bereits."))
E.append(Spacer(1, 0.5*cm))
E.append(P("Datum: __________________ &nbsp;&nbsp;&nbsp; Unterschrift: __________________"))
E.append(PageBreak())

# 4 ZEITPLAN
E.append(H("4. Umsetzungs- und Zeitplan"))
E.append(TBL(
    ["Zeitraum", "Meilenstein"],
    [
        ["Woche 1–2", "Rechtsform klären, Gründungsberatung (IHK/Startercenter), Förderanträge"],
        ["Woche 2–3", "Gewerbeanmeldung, Finanzamt (steuerliche Erfassung), Geschäftskonto"],
        ["Woche 3–8", "Anerkennung als Entlastungsdienst (AnFöVO NRW), Pflegekassen-Verträge"],
        ["Woche 4–8", "Versicherungen (Betriebshaftpflicht, BG), Personal & Schulung"],
        ["Woche 6–12", "Website, Marketing, erste Kunden gewinnen (Ziel Phase 1: 5–15 Kunden)"],
        ["Monat 3–12", "KI-Weiterbildung, SaaS-Pflegesoftware einführen, Prozesse digitalisieren"],
        ["Jahr 1–2", "Break-even (25–30 Kunden), Regionalbüro Duisburg, Personalaufbau"],
        ["Jahr 2–3", "Skalierung (25–60 → 60–120 Kunden), Expansion Mülheim → Oberhausen → Essen"],
    ],
    widths=[3.6*cm, 12.4*cm],
))
E.append(PageBreak())

# 5 CHECKLISTE
E.append(H("5. Checkliste: Unterlagen für den Jobcenter-Termin"))
E.append(P("Termin: <b>Freitag, 21.08.2026, 11:15 Uhr, Herr Aholt, Jobcenter Duisburg, "
           "Wintgensstr. 29-33, 47058 Duisburg, Raum 218</b>"))
E.append(B([
    "Businessplan (ausgedruckt, mit Deckblatt)",
    "Dieses Begleitdokument (Kapitalbedarf, Finanzierung, Zeitplan)",
    "Lebenslauf (unterschrieben)",
    "Qualifikations- und Schulungsnachweise (IHK-Kurs etc.)",
    "Gewerbeanmeldung (Kopie)",
    "Steuernummer / Fragebogen zur steuerlichen Erfassung (falls vorhanden)",
    "Erweitertes Führungszeugnis (falls angefordert)",
    "Ausgefüllter Antrag auf Gründungszuschuss (Jobcenter-Formular)",
    "Stellungnahme einer fachkundigen Stelle (IHK) – falls bereits eingeholt",
    "Eigener Personalausweis",
]))
E.append(PageBreak())

# 6 IHK ANFRAGE
E.append(H("6. Entwurf: Anfrage an die IHK (fachkundige Stellungnahme)"))
E.append(P("Für den Gründungszuschuss verlangt das Jobcenter in der Regel eine Stellungnahme einer "
           "fachkundigen Stelle (Tragfähigkeitsbescheinigung). Diese stellt in Duisburg die Niederrheinische "
           "IHK Duisburg-Wesel-Kleve aus. Folgender Entwurf kann als Anfrage verwendet werden:"))
E.append(Spacer(1, 0.3*cm))
E.append(P("<b>Betreff: Bitte um Stellungnahme zur Tragfähigkeit meiner Existenzgründung</b>", "body"))
E.append(P("Sehr geehrte Damen und Herren,<br/><br/>"
           "ich plane die Gründung des „Stern Entlastungsdienst“, eines Angebots zur Unterstützung im Alltag "
           "(§ 45a SGB XI) für pflegebedürftige Menschen und ihre Angehörigen in Duisburg. Zur Beantragung des "
           "Gründungszuschusses beim Jobcenter benötige ich eine fachkundige Stellungnahme zur Tragfähigkeit "
           "meines Vorhabens.<br/><br/>"
           "Anbei übersende ich meinen Businessplan, die Kapitalbedarfs- und Finanzplanung sowie meinen "
           "Lebenslauf. Gerne komme ich zu einem Beratungsgespräch vorbei.<br/><br/>"
           "Mit freundlichen Grüßen<br/>"
           "____________________________________________"))
E.append(Spacer(1, 0.5*cm))
E.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=8))
E.append(P("Diese Dokumente ergänzen den Businessplan. Sie stellen keine Rechts-, Steuer- oder "
           "Förderberatung dar. Verbindliche Auskünfte erteilen das Jobcenter, die IHK sowie die zuständige "
           "Pflegekasse.", "small"))

doc.build(E)
print("PDF written:", OUT)
