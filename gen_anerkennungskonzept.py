# -*- coding: utf-8 -*-
"""Generate the clean, consolidated Anerkennungskonzept / Betriebskonzept PDF for Stern Entlastungsdienst."""
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

OUT = "/home/boss/.openclaw/workspace/projects/stern-entlastungsdienst/Stern-Entlastungsdienst-Anerkennungskonzept.pdf"

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
S["field"] = ParagraphStyle("field", fontName=FONT, fontSize=10, leading=16, spaceAfter=3)
S["checkbox"] = ParagraphStyle("checkbox", fontName=FONT, fontSize=10, leading=15, leftIndent=6, spaceAfter=1)

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

def FIELD(label):
    return Paragraph("<b>%s</b> ______________________________________________" % label, S["field"])

def CB(label):
    return Paragraph("☐  %s" % label, S["checkbox"])

def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(GREY)
    canvas.drawString(2*cm, 1.1*cm, "Stern Entlastungsdienst - Betriebskonzept / Anerkennung nach AnFöVO NRW")
    canvas.drawRightString(A4[0]-2*cm, 1.1*cm, "Seite %d" % doc.page)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.2)
    canvas.line(2*cm, 1.35*cm, A4[0]-2*cm, 1.35*cm)
    canvas.restoreState()

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm,
                      topMargin=1.8*cm, bottomMargin=1.8*cm, title="Betriebskonzept Stern Entlastungsdienst")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=footer)])

E = []

# COVER
E.append(Spacer(1, 3.0*cm))
E.append(HRFlowable(width="60%", thickness=2, color=GOLD, hAlign="CENTER", spaceAfter=18))
E.append(P("Stern Entlastungsdienst", "title"))
E.append(P("Persönlich helfen. Digital organisieren.", "subtitle"))
E.append(Spacer(1, 0.6*cm))
E.append(P("Betriebskonzept", "bpt"))
E.append(P("Antrag auf Anerkennung als Angebot zur Unterstützung im Alltag", "subtitle"))
E.append(P("nach der Anerkennungs- und Förderungsverordnung NRW (AnFöVO NRW)", "subtitle"))
E.append(Spacer(1, 1.4*cm))
E.append(P("Standort: Duisburg, Nordrhein-Westfalen", "subtitle"))
E.append(P("Stand: August 2026", "subtitle"))
E.append(PageBreak())

# TOC
E.append(H("Inhaltsverzeichnis"))
toc = [
    "1. Unternehmensvorstellung",
    "2. Betriebskonzept",
    "3. Leistungsangebot und Tätigkeitsliste",
    "4. Einsatzorganisation und Qualitätsmanagement",
    "5. Datenschutzkonzept (DSGVO)",
    "6. Beschwerdemanagement",
    "7. Qualifikation und Fortbildung",
    "8. Anlagen",
    "Anlage 1: Einsatzdokumentation / Leistungsnachweis",
    "Anlage 2: Erstaufnahmebogen",
    "Anlage 3: Beschwerdeformular",
    "Anlage 4: Datenschutz- und Verschwiegenheitserklärung",
    "Anlage 5: Einwilligung zur Datenverarbeitung",
]
for t in toc:
    E.append(Paragraph(t, S["body"]))
E.append(PageBreak())

# 1 UNTERNEHMENSVORSTELLUNG
E.append(H("1. Unternehmensvorstellung"))
E.append(P("<b>Stern Entlastungsdienst</b><br/>Persönlich helfen. Digital organisieren."))
E.append(P("Der Stern Entlastungsdienst bietet Unterstützungsleistungen im Alltag für Menschen an, die aufgrund "
           "von Alter, Einschränkungen oder Unterstützungsbedarf Hilfe bei alltäglichen Aufgaben benötigen. Ziel ist "
           "es, Menschen dabei zu unterstützen, möglichst lange selbstständig in ihrem vertrauten Umfeld leben zu "
           "können und gleichzeitig Angehörige zu entlasten."))
E.append(P("Die Leistungen sind bewusst nicht-medizinisch und werden wohnortnah, zuverlässig und qualitätsorientiert "
           "erbracht. Die Organisation erfolgt digital unterstützt – das Leitbild lautet: "
           "<b>„Persönlich helfen. Digital organisieren.“</b>"))
E.append(PageBreak())

# 2 BETRIEBSKONZEPT
E.append(H("2. Betriebskonzept"))
E.append(H2("2.1 Ziel"))
E.append(P("Der Stern Entlastungsdienst unterstützt pflegebedürftige Menschen und ihre Angehörigen mit "
           "verlässlichen Angeboten zur Unterstützung im Alltag. Ziel ist es, die Selbstständigkeit der betreuten "
           "Menschen zu erhalten, ihre Teilhabe am gesellschaftlichen Leben zu fördern und pflegende Angehörige "
           "spürbar zu entlasten."))
E.append(H2("2.2 Zielgruppe"))
E.append(B([
    "Pflegebedürftige Menschen mit anerkanntem Pflegegrad",
    "Ältere Menschen mit Unterstützungsbedarf",
    "Menschen mit körperlichen oder gesundheitlichen Einschränkungen",
    "Pflegende Angehörige, die Entlastung benötigen",
]))
E.append(H2("2.3 Grundsätze"))
E.append(B([
    "Respektvoller Umgang",
    "Zuverlässigkeit und Pünktlichkeit",
    "Individuelle Unterstützung nach Bedarf",
    "Vertraulicher Umgang mit Informationen",
    "Einhaltung aller gesetzlichen Vorgaben",
]))
E.append(H2("2.4 Organisation der Betreuung"))
E.append(B([
    "Erstgespräch und Bedarfsermittlung",
    "Abstimmung des Leistungsumfangs",
    "Planung und Dokumentation der Einsätze",
    "Zeitnahe Berücksichtigung von Änderungen",
]))
E.append(H2("2.5 Umfang der Leistungen"))
E.append(B([
    "Unterstützung im Haushalt",
    "Einkaufshilfe",
    "Begleitung zu Arzt-, Therapie- und Behördenterminen",
    "Alltags- und Freizeitbegleitung",
    "Unterstützung bei der Alltagsorganisation",
    "Entlastung pflegender Angehöriger",
]))
E.append(H2("2.6 Vergütung und Einsatzbedingungen"))
E.append(B([
    "<b>Stundensatz:</b> 28,50 €",
    "<b>Mindestdauer je Einsatz:</b> 120 Minuten",
    "<b>Abrechnungstakt:</b> 30-Minuten-Schritte",
    "Einsätze nur nach Terminvereinbarung",
    "Dokumentation nach jedem Einsatz",
]))
E.append(PageBreak())

# 3 LEISTUNGSANGEBOT
E.append(H("3. Leistungsangebot und Tätigkeitsliste"))
E.append(P("Der Stern Entlastungsdienst unterstützt pflegebedürftige Menschen und ihre Angehörigen im Alltag und "
           "fördert die Selbstständigkeit der betreuten Personen. Die Leistungen umfassen:"))
E.append(B([
    "Unterstützung im Haushalt (leichte hauswirtschaftliche Tätigkeiten)",
    "Reinigung und Wäscheversorgung",
    "Einkaufshilfe",
    "Begleitung zu Arztterminen, Therapien oder Behörden",
    "Spaziergänge und Freizeitbegleitung",
    "Alltags- und gesellschaftliche Begleitung",
    "Hilfe beim Schriftverkehr und leichte Verwaltungsangelegenheiten",
    "Apotheken- und Rezeptbesorgungen",
    "Stundenweise Entlastung für pflegende Angehörige",
]))
E.append(P("Die Einsätze werden individuell geplant, nach den vereinbarten Vorgaben durchgeführt und nach jedem "
           "Einsatz dokumentiert."))
E.append(P("<b>Einsatzbedingungen:</b> Stundensatz 28,50 €, Mindestdauer 120 Minuten pro Einsatz, Abrechnung in "
           "30-Minuten-Schritten."))
E.append(PageBreak())

# 4 EINSATZORGANISATION
E.append(H("4. Einsatzorganisation und Qualitätsmanagement"))
E.append(H2("4.1 Einsatzorganisation"))
E.append(P("Einsätze des Stern Entlastungsdienstes werden gemeinsam mit den Kundinnen und Kunden sowie ihren "
           "Angehörigen geplant; Änderungen sind jederzeit abstimmbar. Zu Beginn der Betreuung wird der "
           "Unterstützungsbedarf besprochen, dokumentiert und ein passender Einsatzplan erstellt. Jeder Einsatz "
           "wird zuverlässig, pünktlich und respektvoll unter Achtung der Privatsphäre und der persönlichen Wünsche "
           "durchgeführt."))
E.append(H2("4.2 Qualitätsstandards"))
E.append(B([
    "Freundlicher und respektvoller Umgang",
    "Pünktliche Einsätze",
    "Individuelle Betreuung",
    "Einhaltung des Datenschutzes",
    "Sorgfältige Dokumentation nach jedem Einsatz (Einsatzprotokoll)",
    "Regelmäßige Fortbildungen",
    "Kontinuierliche Verbesserung",
]))
E.append(H2("4.3 Qualitätssicherung"))
E.append(B([
    "Auswertung von Rückmeldungen der Kundinnen und Kunden",
    "Bearbeitung von Beschwerden",
    "Regelmäßige Überprüfung der Abläufe",
]))
E.append(PageBreak())

# 5 DATENSCHUTZ
E.append(H("5. Datenschutzkonzept (DSGVO)"))
E.append(P("Der Stern Entlastungsdienst verarbeitet personenbezogene Daten ausschließlich zur Durchführung der "
           "vereinbarten Betreuungs- und Entlastungsleistungen sowie zur Erfüllung gesetzlicher Verpflichtungen."))
E.append(H2("5.1 Grundsätze"))
E.append(B([
    "Personenbezogene Daten werden vertraulich behandelt.",
    "Es werden nur die Daten erhoben, die für die Betreuung erforderlich sind.",
    "Die Verarbeitung erfolgt nach DSGVO und Bundesdatenschutzgesetz (BDSG).",
]))
E.append(H2("5.2 Datenspeicherung"))
E.append(B([
    "Alle Unterlagen werden sicher aufbewahrt.",
    "Digitale Daten sind passwortgeschützt.",
    "Papierunterlagen werden in verschlossenen Schränken verwahrt.",
    "Zugriff erhalten ausschließlich berechtigte Personen.",
]))
E.append(H2("5.3 Weitergabe von Daten"))
E.append(P("Eine Weitergabe personenbezogener Daten erfolgt nur: mit Einwilligung der betreuten Person oder ihrer "
           "gesetzlichen Vertretung, aufgrund gesetzlicher Verpflichtungen oder wenn sie zur Durchführung der "
           "Betreuung erforderlich ist."))
E.append(H2("5.4 Rechte der betreuten Personen"))
E.append(B([
    "Auskunft über gespeicherte Daten",
    "Berichtigung unrichtiger Daten",
    "Löschung oder Einschränkung der Verarbeitung, soweit gesetzlich zulässig",
    "Widerruf einer erteilten Einwilligung für die Zukunft",
]))
E.append(H2("5.5 Verpflichtung zur Vertraulichkeit"))
E.append(P("Alle Mitarbeitenden verpflichten sich schriftlich zur Verschwiegenheit und zum vertraulichen Umgang "
           "mit personenbezogenen Daten."))
E.append(H2("5.6 Datenschutzbeauftragter"))
E.append(P("Soweit gesetzlich erforderlich, wird ein Datenschutzbeauftragter bestellt. Andernfalls ist die "
           "Unternehmensleitung für die Einhaltung der Datenschutzbestimmungen verantwortlich."))
E.append(PageBreak())

# 6 BESCHWERDEMANAGEMENT
E.append(H("6. Beschwerdemanagement"))
E.append(P("Ziel des Beschwerdemanagements ist es, Hinweise, Anregungen und Beschwerden ernst zu nehmen, zeitnah zu "
           "bearbeiten und die Qualität der Leistungen kontinuierlich zu verbessern."))
E.append(H2("6.1 Beschwerdeannahme"))
E.append(P("Beschwerden können mündlich, telefonisch, schriftlich oder per E-Mail eingereicht werden."))
E.append(H2("6.2 Bearbeitung"))
E.append(B([
    "Jede Beschwerde wird dokumentiert.",
    "Die Unternehmensleitung prüft den Sachverhalt.",
    "Gemeinsam mit der betroffenen Person wird nach einer angemessenen Lösung gesucht.",
    "Die Bearbeitung erfolgt zeitnah.",
]))
E.append(H2("6.3 Qualitätsverbesserung"))
E.append(P("Beschwerden und Anregungen werden ausgewertet und zur Verbesserung der Arbeitsabläufe genutzt. "
           "Wiederkehrende Probleme werden analysiert und durch geeignete Maßnahmen behoben."))
E.append(H2("6.4 Dokumentation"))
E.append(P("Jede Beschwerde wird mit Datum, Inhalt, Bearbeitung und Ergebnis in einem Beschwerdeprotokoll "
           "festgehalten."))
E.append(PageBreak())

# 7 QUALIFIKATION
E.append(H("7. Qualifikation und Fortbildung"))
E.append(P("Der Stern Entlastungsdienst legt großen Wert auf eine fachlich qualifizierte, zuverlässige und "
           "kundenorientierte Betreuung. Alle Leistungen werden entsprechend den gesetzlichen Vorgaben und den "
           "Anforderungen der Anerkennungs- und Förderungsverordnung NRW erbracht."))
E.append(H2("7.1 Qualifikation"))
E.append(P("Die Betreuung erfolgt ausschließlich durch geeignete und zuverlässige Personen. Vor Aufnahme der "
           "Tätigkeit werden alle erforderlichen Nachweise geprüft und dokumentiert. Hierzu gehören insbesondere:"))
E.append(B([
    "Qualifikations- bzw. Schulungsnachweise",
    "Erweitertes Führungszeugnis (soweit erforderlich)",
    "Nachweis über die Belehrung nach dem Infektionsschutzgesetz (falls erforderlich)",
    "Verpflichtung zur Verschwiegenheit und zum Datenschutz",
]))
E.append(H2("7.2 Fortbildung"))
E.append(P("Alle Mitarbeitenden nehmen regelmäßig an Fort- und Weiterbildungen teil. Ziel ist die kontinuierliche "
           "Verbesserung der fachlichen, sozialen und organisatorischen Kompetenzen."))
E.append(P("<b>Mögliche Fortbildungsthemen:</b>"))
E.append(B([
    "Kommunikation und Gesprächsführung",
    "Umgang mit Menschen mit Demenz",
    "Erste Hilfe",
    "Datenschutz (DSGVO)",
    "Hygiene und Infektionsschutz",
    "Arbeitssicherheit",
    "Umgang mit Notfallsituationen",
]))
E.append(P("Durch regelmäßige Fortbildungen und den Austausch über praktische Erfahrungen wird die Qualität der "
           "Leistungen kontinuierlich gesichert und weiterentwickelt."))
E.append(PageBreak())

# 8 ANLAGEN
E.append(H("8. Anlagen"))
E.append(P("Dem Konzept sind folgende Unterlagen beigefügt:"))
E.append(B([
    "Anlage 1: Einsatzdokumentation (Einsatzprotokoll / Leistungsnachweis)",
    "Anlage 2: Erstaufnahmebogen",
    "Anlage 3: Beschwerdeformular",
    "Anlage 4: Datenschutz- und Verschwiegenheitserklärung",
    "Anlage 5: Einwilligung zur Datenverarbeitung",
    "Anlage 6: Qualifikations- und Schulungsnachweise (Kopien)",
    "Anlage 7: Erweitertes Führungszeugnis (Kopie, falls erforderlich)",
    "Anlage 8: Weitere Nachweise (z. B. Erste Hilfe, Fortbildungen)",
]))
E.append(PageBreak())

# ANLAGE 1
E.append(H("Anlage 1 – Einsatzdokumentation / Leistungsnachweis"))
E.append(Spacer(1, 0.3*cm))
E.append(FIELD("Kundin / Kunde:"))
E.append(FIELD("Pflegegrad:"))
E.append(FIELD("Datum:"))
E.append(P("<b>Einsatzzeit:</b> von ______________ Uhr bis ______________ Uhr", "field"))
E.append(FIELD("Mitarbeitende/r:"))
E.append(Spacer(1, 0.2*cm))
E.append(P("<b>Erbrachte Leistungen</b>", "body"))
for l in ["Haushaltshilfe", "Einkaufen", "Arztbegleitung", "Behördenbegleitung",
          "Spaziergang / Begleitung", "Alltagsbegleitung", "Entlastung pflegender Angehöriger"]:
    E.append(CB(l))
E.append(CB("Sonstiges: ______________________________________"))
E.append(Spacer(1, 0.3*cm))
E.append(FIELD("Bemerkungen:"))
E.append(Spacer(1, 0.6*cm))
E.append(FIELD("Unterschrift Kundin / Kunde:"))
E.append(Spacer(1, 0.4*cm))
E.append(FIELD("Unterschrift Mitarbeitende/r:"))
E.append(PageBreak())

# ANLAGE 2
E.append(H("Anlage 2 – Erstaufnahmebogen"))
E.append(Spacer(1, 0.3*cm))
E.append(FIELD("Name:"))
E.append(FIELD("Geburtsdatum:"))
E.append(FIELD("Adresse:"))
E.append(FIELD("Telefon:"))
E.append(FIELD("Pflegegrad:"))
E.append(FIELD("Angehörige / Ansprechpartner:"))
E.append(Spacer(1, 0.2*cm))
E.append(P("<b>Gewünschte Leistungen</b>", "body"))
for l in ["Haushaltshilfe", "Einkaufshilfe", "Arztbegleitung", "Behördenbegleitung",
          "Alltagsbegleitung", "Entlastung Angehöriger"]:
    E.append(CB(l))
E.append(CB("Sonstiges: ______________________________________"))
E.append(Spacer(1, 0.3*cm))
E.append(FIELD("Besondere Hinweise:"))
E.append(Spacer(1, 0.6*cm))
E.append(FIELD("Datum:"))
E.append(Spacer(1, 0.4*cm))
E.append(FIELD("Unterschrift:"))
E.append(PageBreak())

# ANLAGE 3
E.append(H("Anlage 3 – Beschwerdeformular"))
E.append(Spacer(1, 0.3*cm))
E.append(FIELD("Datum:"))
E.append(FIELD("Name (freiwillig):"))
E.append(Spacer(1, 0.2*cm))
E.append(P("<b>Art der Rückmeldung</b>", "body"))
E.append(CB("Beschwerde"))
E.append(CB("Anregung"))
E.append(CB("Lob"))
E.append(Spacer(1, 0.3*cm))
E.append(FIELD("Beschreibung:"))
E.append(Spacer(1, 0.5*cm))
E.append(FIELD("Bearbeitung:"))
E.append(Spacer(1, 0.6*cm))
E.append(FIELD("Erledigt am:"))
E.append(Spacer(1, 0.4*cm))
E.append(FIELD("Bearbeitet durch:"))
E.append(PageBreak())

# ANLAGE 4
E.append(H("Anlage 4 – Datenschutz- und Verschwiegenheitserklärung"))
E.append(P("Ich verpflichte mich, alle personenbezogenen Daten der betreuten Personen vertraulich zu behandeln und "
           "ausschließlich im Rahmen meiner Tätigkeit zu verwenden. Die Datenschutzbestimmungen der DSGVO sowie die "
           "Verschwiegenheitspflicht werden eingehalten."))
E.append(Spacer(1, 0.6*cm))
E.append(FIELD("Name:"))
E.append(Spacer(1, 0.4*cm))
E.append(FIELD("Datum:"))
E.append(Spacer(1, 0.4*cm))
E.append(FIELD("Unterschrift:"))
E.append(PageBreak())

# ANLAGE 5
E.append(H("Anlage 5 – Einwilligung zur Datenverarbeitung"))
E.append(P("Ich willige ein, dass meine personenbezogenen Daten zum Zweck der Betreuung und Abrechnung verarbeitet "
           "werden. Die Datenschutzhinweise wurden mir erläutert."))
E.append(Spacer(1, 0.6*cm))
E.append(FIELD("Name:"))
E.append(Spacer(1, 0.4*cm))
E.append(FIELD("Datum:"))
E.append(Spacer(1, 0.4*cm))
E.append(FIELD("Unterschrift:"))
E.append(Spacer(1, 1.0*cm))
E.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=8))
E.append(P("Dieses Betriebskonzept dient als Antragsunterlage für die Anerkennung als Angebot zur Unterstützung im "
           "Alltag nach der Anerkennungs- und Förderungsverordnung NRW (AnFöVO NRW). Es stellt keine Rechtsberatung "
           "dar. Verbindliche Auskünfte erteilen die zuständige Kommune (Stadt Duisburg) und die Pflegekasse.",
           "small"))

doc.build(E)
print("PDF written:", OUT)
