# -*- coding: utf-8 -*-
"""Generate the English business plan PDF for Stern Entlastungsdienst."""
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

OUT = "/home/boss/.openclaw/workspace/projects/stern-entlastungsdienst/Stern-Entlastungsdienst-Businessplan-EN.pdf"

NAVY = colors.HexColor("#1f3a5f")
GOLD = colors.HexColor("#c9a227")
LIGHT = colors.HexColor("#eef2f7")
GREY = colors.HexColor("#5a5a5a")

S = {}
S["title"] = ParagraphStyle("title", fontName=FONT_B, fontSize=26, leading=32, textColor=NAVY, alignment=TA_CENTER, spaceAfter=6)
S["subtitle"] = ParagraphStyle("subtitle", fontName=FONT, fontSize=14, leading=20, textColor=GREY, alignment=TA_CENTER, spaceAfter=4)
S["h1"] = ParagraphStyle("h1", fontName=FONT_B, fontSize=15, leading=20, textColor=NAVY, spaceBefore=14, spaceAfter=6)
S["h2"] = ParagraphStyle("h2", fontName=FONT_B, fontSize=12, leading=16, textColor=colors.HexColor("#2c4a6e"), spaceBefore=10, spaceAfter=4)
S["body"] = ParagraphStyle("body", fontName=FONT, fontSize=10, leading=14.5, alignment=TA_JUSTIFY, spaceAfter=6)
S["bullet"] = ParagraphStyle("bullet", fontName=FONT, fontSize=10, leading=14, alignment=TA_LEFT, leftIndent=14, spaceAfter=2)
S["tbl"] = ParagraphStyle("tbl", fontName=FONT, fontSize=9, leading=12)
S["tblb"] = ParagraphStyle("tblb", fontName=FONT_B, fontSize=9, leading=12)
S["small"] = ParagraphStyle("small", fontName=FONT, fontSize=8.5, leading=12, textColor=GREY, alignment=TA_CENTER)
S["bpt"] = ParagraphStyle("bpt", fontName=FONT_B, fontSize=18, leading=22, textColor=GOLD, alignment=TA_CENTER, spaceAfter=4)

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
    canvas.drawString(2*cm, 1.1*cm, "Stern Entlastungsdienst - Personal help. Digital organization.")
    canvas.drawRightString(A4[0]-2*cm, 1.1*cm, "Page %d" % doc.page)
    canvas.setStrokeColor(GOLD)
    canvas.setLineWidth(1.2)
    canvas.line(2*cm, 1.35*cm, A4[0]-2*cm, 1.35*cm)
    canvas.restoreState()

doc = BaseDocTemplate(OUT, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm,
                      topMargin=1.8*cm, bottomMargin=1.8*cm, title="Business Plan Stern Entlastungsdienst")
frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=footer)])

E = []

# COVER
E.append(Spacer(1, 3.2*cm))
E.append(HRFlowable(width="60%", thickness=2, color=GOLD, hAlign="CENTER", spaceAfter=18))
E.append(P("Stern Entlastungsdienst", "title"))
E.append(P("Personal help. Digital organization.", "subtitle"))
E.append(Spacer(1, 0.6*cm))
E.append(P("Business Plan", "bpt"))
E.append(P("An innovative relief concept for people in need of care and their relatives", "subtitle"))
E.append(Spacer(1, 1.6*cm))
E.append(P("Location: Duisburg, North Rhine-Westphalia", "subtitle"))
E.append(P("Everyday support service under § 45a SGB XI", "subtitle"))
E.append(P("Status: August 2026", "subtitle"))
E.append(PageBreak())

# TOC
E.append(H("Table of Contents"))
toc = [
    "1. Executive Summary",
    "2. Company Profile",
    "3. Business Idea and Service Offering",
    "4. Market Analysis and Target Group",
    "5. Marketing and Sales",
    "6. Organisation and Staffing Structure",
    "7. Digitalisation and App Concept",
    "8. Financial Planning and Profitability",
    "9. Opportunities and Risk Analysis",
    "10. Vision and Growth Strategy",
    "11. Conclusion",
    "Annex A: Recognition and Quality Concept",
    "Annex B: Data Protection Concept",
    "Annex C: Duisburg Regional Office",
    "Annex D: AI Training Concept",
]
for t in toc:
    E.append(Paragraph(t, S["body"]))
E.append(PageBreak())

# 1 EXEC SUMMARY
E.append(H("1. Executive Summary"))
E.append(P("Stern Entlastungsdienst is an everyday support service (Alltagsbegleitung) for people in need of care "
           "(care levels 1–5) and their caring relatives in Duisburg and the surrounding region (NRW). We combine "
           "personal, human care with modern digital organisation – our guiding principle is: "
           "<b>“Personal help. Digital organization.”</b>"))
E.append(P("Our services are deliberately non-medical: household assistance, shopping, accompaniment to medical, "
           "authority and leisure appointments, social care, errands, and digital everyday assistance. In this way "
           "we relieve caring relatives and enable people to live independently in their familiar home for as long "
           "as possible."))
E.append(P("<b>Funding:</b> Our services are billed via the monthly relief amount (Entlastungsbetrag) under "
           "§ 45b SGB XI (€131 per month, increased on 1 January 2025) – and, prospectively, via the conversion "
           "entitlement from unused care benefits in kind. This gives the client a state-funded, recurring "
           "entitlement that often remains unused."))
E.append(P("<b>Profitability:</b> We calculate with an hourly rate of €28.50, a minimum assignment of 120 minutes "
           "and billing in 30-minute increments. Break-even is expected at around 25–30 clients. The 3-year plan "
           "shows a controlled build-up from approx. €44,400 revenue in year 1 to approx. €148,100 in year 3."))
E.append(P("<b>Unique selling point:</b> While many providers still work with paper and telephone, we rely on a "
           "digital operations platform (booking, scheduling, documentation, billing) with AI-supported organisation "
           "in the long term. This is the core of our scalability."))
E.append(PageBreak())

# 2 COMPANY
E.append(H("2. Company Profile"))
E.append(H2("2.1 Company data"))
E.append(P("<b>Name:</b> Stern Entlastungsdienst<br/>"
           "<b>Slogan:</b> “Personal help. Digital organization.”<br/>"
           "<b>Location:</b> Duisburg, North Rhine-Westphalia (mobile service)<br/>"
           "<b>Legal form:</b> Sole proprietorship / small business<br/>"
           "<b>Status:</b> Business registered, first existing clients on board"))
E.append(H2("2.2 Founder profile and motivation"))
E.append(P("The founder brings practical experience from looking after approx. 5–6 existing clients and has "
           "completed an IHK start-up course; contact with care insurance funds (Pflegekassen) already exists. The "
           "motivation is to combine practical, personal help with modern digital working methods in order to "
           "noticeably improve day-to-day organisation for clients and relatives."))
E.append(H2("2.3 Guiding principle"))
E.append(P("<b>Personal help:</b> Individual, reliable and respectful support for people in need of care and their "
           "relatives – with human closeness at its core."))
E.append(P("<b>Digital organization:</b> Use of modern technology for intelligent coordination, networking of staff "
           "and optimal capacity utilisation."))
E.append(P("Three core values shape our brand: <b>flexible</b> (organisation/staff), <b>efficient</b> "
           "(app/technology) and <b>human</b> (client contact)."))
E.append(PageBreak())

# 3 IDEA
E.append(H("3. Business Idea and Service Offering"))
E.append(H2("3.1 Business idea"))
E.append(P("Personal everyday support for people with care needs and their relatives. The focus is on practical "
           "everyday assistance (accompaniment, errands, household support). The innovation is the combination of "
           "human closeness and digital scheduling."))
E.append(H2("3.2 Service offering"))
E.append(H2("Everyday assistance"))
E.append(B([
    "Household support",
    "Order and structure in everyday life",
    "Laundry care",
    "Light housekeeping tasks",
]))
E.append(H2("Accompaniment and support"))
E.append(B([
    "Accompaniment to medical appointments",
    "Accompaniment to authorities and important appointments",
    "Support with errands",
    "Walks and social care",
]))
E.append(H2("Errands"))
E.append(B([
    "Shopping",
    "Pharmacy pick-ups and prescription collections",
    "Postal and courier errands",
    "Correspondence",
]))
E.append(H2("Digital everyday assistance"))
E.append(B([
    "Support with smartphone, tablet and computer",
    "Help with digital applications",
    "Support with online appointments",
]))
E.append(H2("3.3 Billing model"))
E.append(B([
    "<b>Hourly rate:</b> €28.50",
    "<b>Minimum assignment:</b> 120 minutes (covers travel, preparation, delivery, documentation)",
    "<b>Billing increment:</b> 30-minute steps",
    "<b>Funding via care insurance:</b> monthly relief amount under § 45b SGB XI (€131)",
    "<b>Prospectively:</b> conversion entitlement from unused care benefits in kind",
]))
E.append(H2("3.4 Flow of an assignment"))
E.append(B([
    "1. Enquiry by client or relatives",
    "2. Needs assessment and initial meeting",
    "3. Planning of the appropriate support scope",
    "4. Appointment scheduling",
    "5. Delivery of the service",
    "6. Documentation of the assignment",
    "7. Feedback and quality assurance",
]))
E.append(PageBreak())

# 4 MARKET
E.append(H("4. Market Analysis and Target Group"))
E.append(H2("4.1 Target groups"))
E.append(B([
    "People in need of care with a recognised care level (1–5)",
    "Older people with support needs but without a care level",
    "People with everyday limitations",
    "Caring relatives who need relief",
]))
E.append(H2("4.2 Market situation"))
E.append(P("Germany is ageing; demand for everyday support services is growing continuously. Every person with a "
           "care level who is cared for at home receives the relief amount of €131 per month. This amount frequently "
           "goes unused because relatives are unaware of the options or perceive the application process as a hurdle. "
           "This is our opportunity: a low-threshold, easy-to-understand and digitally organised offering."))
E.append(H2("4.3 Competitive advantage"))
E.append(P("Most small providers still work on paper and by telephone. Our digital organisation (scheduling, "
           "documentation, billing, client portal) is a genuine unique selling point and enables scaling without "
           "disproportionate administrative effort."))
E.append(PageBreak())

# 5 MARKETING
E.append(H("5. Marketing and Sales"))
E.append(H2("5.1 Online"))
E.append(B([
    "Own website",
    "Google Business Profile",
    "Facebook",
    "Instagram",
    "Prospectively an own digital platform/app",
]))
E.append(H2("5.2 Offline"))
E.append(B([
    "Flyers",
    "Doctors and specialists",
    "Care services",
    "Pharmacies",
    "Senior citizens' offices and care support points (Pflegestützpunkte)",
    "Church communities",
    "Hospitals / discharge management & social services (B2B)",
    "Recommendations from satisfied clients",
]))
E.append(H2("5.3 Sales strategy"))
E.append(P("Sales rely on personal advice as well as cooperation with doctors, care insurance funds, care support "
           "points, day-care facilities and the regional office Alter, Pflege und Demenz NRW. In addition, local "
           "networks are built with physiotherapists, care services, senior homes and universities."))
E.append(PageBreak())

# 6 ORGANISATION
E.append(H("6. Organisation and Staffing Structure"))
E.append(H2("6.1 Organisational model"))
E.append(P("At the centre is an intelligent operations platform that connects clients, staff and the central office. "
           "Assignments are organised in clearly defined packages that can be accepted flexibly via the mobile app. "
           "Smart regional scheduling suggests suitable nearby assignments to save travel and use resources efficiently."))
E.append(P("The model is particularly suited to flexible employment models (students, part-time workers, marginal "
           "employees) with changing time windows. Remuneration is transparent and legally compliant."))
E.append(H2("6.2 Staffing build-up"))
E.append(B([
    "<b>Year 1:</b> Owner, later first student support",
    "<b>Year 2:</b> 2–4 student employees, flexible scheduling",
    "<b>Year 3:</b> 5–8 student or marginal employees, coordination via digital processes",
]))
E.append(P("Principle: Local part-time and mini-job workers shorten travel and increase responsiveness. Full-time "
           "positions are only created once demand is sustainably sufficient. Where possible, fixed contact persons "
           "are used; digital organisation ensures seamless cover in case of absences."))
E.append(H2("6.3 Regional office structure (prospective)"))
E.append(B([
    "<b>Regional manager:</b> overall coordination, quality control, contact for authorities",
    "<b>Administrative clerk:</b> client data management, appointment organisation, documentation",
    "<b>Deployment coordinator:</b> duty rosters, coordination of care staff, absence management",
    "<b>Care staff:</b> delivery of relief services at the client's location",
]))
E.append(PageBreak())

# 7 DIGITALISATION
E.append(H("7. Digitalisation and App Concept"))
E.append(H2("7.1 Digitalisation concept"))
E.append(P("A step-by-step build-up of a digital corporate structure is planned:"))
E.append(B([
    "Digital appointment scheduling and deployment management",
    "Automatic documentation",
    "Digital forms",
    "Client and staff management",
    "Automated invoicing",
    "Digital communication",
    "AI support for administrative tasks",
    "In the long term an own app",
]))
E.append(H2("7.2 Software strategy (SaaS-first, insolvency-safe)"))
E.append(P("To keep the IT budget realistic, the build-up is staged: In years 1–2, established, GDPR-compliant "
           "white-label care software (e.g. TourCare, Mobile SystemCare) is used. This ensures immediate compliance, "
           "interfaces to care insurance funds and an appropriate IT budget of €1,200–2,400 p.a. From year 3, an own "
           "app or API connection is developed step by step once the client volume justifies the investment."))
E.append(H2("7.3 App concept (target vision)"))
E.append(P("The app maps the three user groups:"))
E.append(B([
    "<b>Families/clients:</b> booking, price view (€131 budget vs. private payment), assignment tracking, invoices, chat",
    "<b>Helpers/staff:</b> daily plan, navigation, check-in/check-out, task list, assignment report",
    "<b>Administration:</b> dashboard, client/staff management, scheduling, billing, reports, compliance",
]))
E.append(P("Billing supports two models: reimbursement to the family and direct billing with the care insurance fund "
           "(relief amount). This means billing flows – as requested – directly to the insurer/Pflegekasse."))
E.append(H2("7.4 AI concept and GDPR"))
E.append(P("AI is used to automate administrative tasks, create schedules intelligently, process documents and "
           "optimise workflows. In the long term, own AI agents for organisational processes will be developed. This "
           "leaves more time for the actual care work."))
E.append(P("<b>GDPR compliance (Art. 9 GDPR):</b> AI and cloud systems are operated exclusively GDPR-compliant "
           "(EU hosting). Sensitive health data is strictly pseudonymised or anonymised before AI-supported "
           "processing; there is no transfer to US servers."))
E.append(PageBreak())

# 8 FINANCE
E.append(H("8. Financial Planning and Profitability"))
E.append(H2("8.1 Calculation basis"))
E.append(B([
    "<b>Hourly rate:</b> €28.50",
    "<b>Minimum assignment:</b> 120 minutes",
    "<b>Billing increment:</b> 30 minutes",
    "<b>Weeks per month:</b> 4.33",
    "<b>Relief amount per client:</b> €131 / month (approx. 4.6 hours of service)",
]))
E.append(H2("8.2 3-year financial plan (hourly model)"))
E.append(TBL(
    ["Year", "Hours/week", "Monthly revenue", "Annual revenue", "Costs/year", "Result before tax"],
    [
        ["Year 1 – Build-up", "30 h", "≈ €3,700", "≈ €44,400", "≈ €8,880", "≈ €35,520"],
        ["Year 2 – Growth", "60 h", "≈ €7,400", "≈ €88,800", "≈ €45,000", "≈ €43,800"],
        ["Year 3 – Expansion", "100 h", "≈ €12,340", "≈ €148,100", "≈ €90,000", "≈ €58,100"],
    ],
    widths=[3.4*cm, 2.0*cm, 2.6*cm, 2.6*cm, 2.4*cm, 2.8*cm],
    align_right_cols=(2, 3, 4, 5),
))
E.append(Spacer(1, 0.3*cm))
E.append(H2("8.3 Cost structure (annual)"))
E.append(TBL(
    ["Cost item", "Year 1", "Year 2", "Year 3"],
    [
        ["Insurance", "€960", "€1,200", "€1,500"],
        ["Telephone/Internet", "€720", "€900", "€1,200"],
        ["Software/Digitalisation", "€1,200", "€2,400", "€4,000"],
        ["Marketing", "€1,800", "€3,000", "€5,000"],
        ["Travel costs", "€3,000", "€6,000", "€10,000"],
        ["Personnel", "€0", "€31,500", "€60,000"],
        ["Other costs", "€1,200", "€2,000", "€3,000"],
    ],
    widths=[7.0*cm, 3.0*cm, 3.0*cm, 3.0*cm],
    align_right_cols=(1, 2, 3),
))
E.append(Spacer(1, 0.3*cm))
E.append(H2("8.4 Monthly fixed costs at start (approx. €1,600)"))
E.append(TBL(
    ["Item", "Monthly"],
    [
        ["Office rent", "€300"],
        ["Telephone/Internet", "€50"],
        ["Software/Licences", "€80"],
        ["Business liability/insurance", "€120"],
        ["Tax advisor/accounting", "€150"],
        ["Advertising/Marketing", "€250"],
        ["Travel costs", "€300"],
        ["Office supplies/printing", "€100"],
        ["Other incl. bank charges", "€250"],
        ["<b>Total</b>", "<b>approx. €1,600</b>"],
    ],
    widths=[9.0*cm, 4.0*cm],
    align_right_cols=(1,),
))
E.append(Spacer(1, 0.3*cm))
E.append(H2("8.5 Break-even and scaling (client model)"))
E.append(P("Alternative view via the relief amount: With average revenue of €131 and approx. €70 personnel cost per "
           "client, the break-even point is reached at approx. 30 clients. Fixed costs rise moderately with each "
           "growth stage (approx. €1,600 at the start up to approx. €2,500 at 500 clients)."))
E.append(H2("8.6 Growth stages (capacity-consistent)"))
E.append(P("Client development is deliberately reconciled with hourly capacity to avoid bottlenecks. A single "
           "founder can realistically serve 15–25 clients at approx. 30–35 direct hours per week; further growth "
           "requires additional staff."))
E.append(TBL(
    ["Period", "Phases", "Number of clients"],
    [
        ["Year 1", "Phase 1–2", "5–15 clients (build-up)"],
        ["Year 1", "Phase 3–4", "15–25 clients (capacity limit of 1 founder)"],
        ["Year 2", "Phase 5–6", "25–60 clients (first mini-jobbers/students)"],
        ["Year 3", "Phase 7–8", "60–120 clients (fixed team, digital scaling)"],
    ],
    widths=[3.2*cm, 3.6*cm, 9.2*cm],
))
E.append(PageBreak())

# 9 RISKS
E.append(H("9. Opportunities and Risk Analysis"))
E.append(H2("9.1 Opportunities"))
E.append(B([
    "High and demographically growing demand",
    "State-funded, recurring relief amount (€131 / month)",
    "Efficiency and scaling advantage through digital tools",
    "Low entry barrier (no medical qualification required)",
    "Differentiation from paper-based competitors",
]))
E.append(H2("9.2 Risks and countermeasures"))
E.append(TBL(
    ["Risk", "Countermeasure"],
    [
        ["Delay in recognition as a relief service", "Early coordination with municipality and care fund; complete documentation"],
        ["Delays in app implementation", "Step-by-step build-up; start with a lean solution (booking/planning)"],
        ["Limited start-up resources", "Use of funding (education voucher, start-up grant)"],
        ["Staff turnover", "Attractive, flexible working models; fair pay; fixed contact persons"],
        ["Regulatory changes (NRW state law)", "Continuous monitoring; advice from tax advisor and associations"],
        ["Payment/billing risks", "Transparent service records; direct billing with care fund"],
    ],
    widths=[6.5*cm, 9.5*cm],
))
E.append(PageBreak())

# 10 VISION
E.append(H("10. Vision and Growth Strategy"))
E.append(P("Stern Entlastungsdienst is to develop from a regional provider into a modern, digitally supported "
           "service company."))
E.append(H2("10.1 Long-term goals"))
E.append(B([
    "Economically stable company",
    "Modern AI-supported organisation",
    "Own digital platform/app",
    "High service quality",
    "Attractive jobs for students and part-time workers",
    "Sustainable growth",
]))
E.append(H2("10.2 Implementation plan in 3 phases"))
E.append(TBL(
    ["Phase", "Focus"],
    [
        ["Phase 1", "Foundation, first clients, recognition procedure"],
        ["Phase 2", "Digitalisation (introduction of app for scheduling), further training of the founder"],
        ["Phase 3", "Scaling through build-up of a student network with AI-supported organisation"],
    ],
    widths=[3.0*cm, 13.0*cm],
))
E.append(H2("10.3 Regional expansion"))
E.append(P("After stabilisation in Duisburg, step-by-step expansion into the neighbouring cities of "
           "<b>Mülheim an der Ruhr</b>, <b>Oberhausen</b> and <b>Essen</b> follows. The digital platform makes this "
           "expansion possible without proportionally rising administrative effort."))
E.append(PageBreak())

# 11 CONCLUSION
E.append(H("11. Conclusion"))
E.append(P("Stern Entlastungsdienst combines a proven, state-funded business model (relief amount under § 45b "
           "SGB XI) with a modern, digital organisation. Demand is demographically secure, entry barriers are low and "
           "the digital unique selling point enables sustainable, controlled growth. With recognition as an everyday "
           "support service in NRW, a solid financial plan and the step-by-step build-up of the digital platform, the "
           "company is well positioned to support people in need of care and sustainably relieve their relatives."))
E.append(PageBreak())

# ANNEX A
E.append(H("Annex A: Recognition and Quality Concept"))
E.append(P("<b>Goal:</b> Recognition as a provider of everyday support services under the NRW state regulations "
           "(Anerkennungs- und Förderungsverordnung NRW)."))
E.append(H2("A.1 Legal basis"))
E.append(B([
    "Billing under SGB XI and supplementary regulations of the state of NRW",
    "Relief amount under § 45b SGB XI",
    "Conversion entitlement from care benefits in kind",
    "Cooperation with care funds, municipality and authorities",
]))
E.append(H2("A.2 Qualification and reliability"))
E.append(B([
    "Qualification and training certificates",
    "Extended certificate of good conduct (where required)",
    "Instruction under the Infection Protection Act (if required)",
    "Proof of first-aid training (if available)",
    "Commitment to confidentiality and data protection",
]))
E.append(P("<b>Professional leadership (AnFöVO NRW):</b> To fully comply with the requirements of the NRW "
           "Recognition and Funding Ordinance, a qualified nursing professional (e.g. on a mini-job basis or as a "
           "freelancer) is contracted where necessary for quality control and professional leadership."))
E.append(H2("A.3 Quality management"))
E.append(B([
    "Selection and structured induction of staff",
    "Proper documentation of every assignment",
    "Data protection and confidentiality",
    "Transparent complaint management",
    "Regular further training",
]))
E.append(H2("A.4 Training topics"))
E.append(B([
    "Communication and conversation skills",
    "Dealing with people with dementia",
    "First aid",
    "Data protection (GDPR)",
    "Hygiene and infection protection",
    "Occupational safety",
    "Dealing with emergency situations",
]))
E.append(H2("A.5 Required documents (annexes)"))
E.append(B([
    "Annex 1: Assignment documentation / service record",
    "Annex 2: Initial intake form",
    "Annex 3: Complaint form",
    "Annex 4: Data protection and confidentiality declaration",
    "Annex 5: Consent to data processing",
    "Annex 6: Qualification certificates",
    "Annex 7: Extended certificate of good conduct (if required)",
    "Annex 8: Further evidence (first aid, training)",
]))
E.append(PageBreak())

# ANNEX B
E.append(H("Annex B: Data Protection Concept"))
E.append(P("Basis: General Data Protection Regulation (GDPR), Federal Data Protection Act (BDSG) and applicable "
           "state regulations."))
E.append(H2("B.1 Processed data"))
E.append(B([
    "Client data (name, address, contact, if applicable date of birth, assignment data)",
    "Relative data (name, telephone, contact for coordination)",
    "Staff data (personal data, qualifications, scheduling)",
]))
E.append(H2("B.2 Principles"))
E.append(B([
    "Purpose limitation – data only for necessary purposes",
    "Data minimisation – only required information",
    "Confidentiality – no unauthorised disclosure",
    "Security – protected storage and processing",
]))
E.append(H2("B.3 Technical and organisational measures (TOM)"))
E.append(B([
    "Password-protected systems",
    "Regular software updates",
    "Access only for authorised persons",
    "Locked storage of paper documents",
    "Regular data backups",
]))
E.append(H2("B.4 Retention and deletion"))
E.append(P("Data is stored only for as long as legal or organisational purposes require. Thereafter, secure deletion "
           "of digital data and data-protection-compliant destruction of paper documents takes place."))
E.append(PageBreak())

# ANNEX C
E.append(H("Annex C: Duisburg Regional Office"))
E.append(H2("C.1 Location and tasks"))
E.append(P("The Duisburg regional office serves as the central point of contact for clients, staff, cooperation "
           "partners and authorities."))
E.append(B([
    "Advice for people in need of care and relatives",
    "Recording and managing new client enquiries",
    "Needs assessment and individual support planning",
    "Scheduling and coordination of care staff",
    "Staff management and support",
    "Quality assurance, documentation and data protection",
    "Cooperation with care funds and network partners",
]))
E.append(H2("C.2 Premises"))
E.append(B([
    "Advice area for client meetings",
    "Workplace for administration and organisation",
    "Data-protection-compliant filing",
    "Telephone and digital communication facilities",
    "Meeting room and training materials",
]))
E.append(H2("C.3 Opening hours"))
E.append(P("<b>Office hours:</b> Monday–Friday 08:00–16:00<br/>"
           "<b>Telephone availability:</b> Monday–Friday 08:00–18:00<br/>"
           "<b>By arrangement:</b> consultation appointments outside opening hours possible"))
E.append(H2("C.4 Development perspective"))
E.append(B([
    "Building a permanent staff team",
    "Expanding the client base",
    "Extending the service offering",
    "Cooperation with further regional partners",
    "Sustainable care as a regional hub",
]))
E.append(PageBreak())

# ANNEX D
E.append(H("Annex D: AI Training Concept"))
E.append(P("For the digital development of the company, a structured AI training programme is pursued (funded via "
           "education voucher / Bildungsgutschein)."))
E.append(H2("D.1 Learning path (6–9 months, 3 stages)"))
E.append(TBL(
    ["Stage", "Duration", "Content"],
    [
        ["Stage 1 – AI basics", "approx. 2 months", "AI basics, ChatGPT, prompt engineering, data protection"],
        ["Stage 2 – AI in business", "2–3 months", "Process analysis, AI introduction, project management"],
        ["Stage 3 – Specialisation", "2–4 months", "Python, APIs, AI agents, cloud, own practical project"],
    ],
    widths=[5.5*cm, 2.5*cm, 8.0*cm],
))
E.append(H2("D.2 Possible providers in Duisburg"))
E.append(B([
    "COMCAVE Duisburg (AI, prompt engineering, Python, data analysis)",
    "DAA – Deutsche Angestellten-Akademie (IT, digitalisation)",
    "Niederrheinische IHK Duisburg-Wesel-Kleve (AI certificate courses)",
]))
E.append(H2("D.3 Qualification chain"))
E.append(P("AI basics → Prompt Engineer → <b>AI Manager (IHK)</b> → AI Governance/EU AI Act → "
           "AI Multiplier or AI Officer"))
E.append(Spacer(1, 1.0*cm))
E.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=8))
E.append(P("This business plan serves corporate planning and as a basis for discussions with the Jobcenter, the "
           "regional office and banks. It does not constitute legal or tax advice. The NRW recognition rules must be "
           "clarified with the municipality of Duisburg and the responsible care insurance fund; tax treatment with a "
           "tax advisor.", "small"))

doc.build(E)
print("PDF written:", OUT)
