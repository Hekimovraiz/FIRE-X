#!/usr/bin/env python3
"""
FIRE-X Master Dossier & Jury Defense Generator (PDF)
====================================================
NASA Space Apps Challenge 2026 — Flame in Freefall
Team: SpaceAz (Murad Fatullazada, Sabir Məmmədzadə, Raiz Həkimov, Şahvələd Vəlizadə, Hüseyn Alırzayev)

Generates a comprehensive, publication-grade PDF containing:
1. Challenge Mission & Science Breakdown
2. Complete FIRE-X System Architecture & Hardware Bridge
3. NASA PSI Data Provenance & 892 Experiment Catalog
4. Complete Answers to 31 Crucial Jury Questions
"""

import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, Image, HRFlowable
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Register Unicode Noto Sans fonts
FONT_REGULAR = "/usr/share/fonts/noto/NotoSans-Regular.ttf"
FONT_BOLD = "/usr/share/fonts/noto/NotoSans-Bold.ttf"
FONT_ITALIC = "/usr/share/fonts/noto/NotoSans-Italic.ttf"
FONT_BOLD_ITALIC = "/usr/share/fonts/noto/NotoSans-BoldItalic.ttf"

pdfmetrics.registerFont(TTFont("NotoSans", FONT_REGULAR))
pdfmetrics.registerFont(TTFont("NotoSans-Bold", FONT_BOLD))
pdfmetrics.registerFont(TTFont("NotoSans-Italic", FONT_ITALIC))
pdfmetrics.registerFont(TTFont("NotoSans-BoldItalic", FONT_BOLD_ITALIC))

# Colors
C_PRIMARY = colors.HexColor("#070D1A")
C_NAVY = colors.HexColor("#0F172A")
C_CYAN = colors.HexColor("#00838F")
C_CYAN_LIGHT = colors.HexColor("#E0F7FA")
C_ORANGE = colors.HexColor("#D84315")
C_ORANGE_LIGHT = colors.HexColor("#FBE9E7")
C_TEXT = colors.HexColor("#1E293B")
C_MUTED = colors.HexColor("#64748B")
C_BG_CARD = colors.HexColor("#F8FAFC")
C_BORDER = colors.HexColor("#CBD5E1")
C_GREEN = colors.HexColor("#2E7D32")
C_GREEN_LIGHT = colors.HexColor("#E8F5E9")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        if self._pageNumber == 1:
            return  # Skip cover page
        self.saveState()
        self.setFont("NotoSans", 8)
        self.setFillColor(C_MUTED)
        
        # Header
        self.drawString(54, 802, "NASA SPACE APPS 2026 // FIRE-X MASTER DOSSIER — TEAM SPACEAZ")
        self.drawRightString(541, 802, "FLAME IN FREEFALL")
        self.setStrokeColor(C_BORDER)
        self.setLineWidth(0.6)
        self.line(54, 795, 541, 795)
        
        # Footer
        self.line(54, 48, 541, 48)
        self.drawString(54, 34, "KONFİDENSİAL // MÜNSİF VƏ MÜDAFİƏ ÜÇÜN RƏSMİ SƏNƏD")
        self.drawRightString(541, 34, f"Səhifə {self._pageNumber} / {page_count}")
        self.restoreState()


def build_pdf(filename: str):
    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom Typography Styles
    body = ParagraphStyle('DocBody', fontName='NotoSans', fontSize=9.5, leading=14.5, textColor=C_TEXT)
    body_bold = ParagraphStyle('DocBodyBold', fontName='NotoSans-Bold', fontSize=9.5, leading=14.5, textColor=C_TEXT)
    h1 = ParagraphStyle('DocH1', fontName='NotoSans-Bold', fontSize=18, leading=23, textColor=C_PRIMARY, spaceAfter=8, spaceBefore=14)
    h2 = ParagraphStyle('DocH2', fontName='NotoSans-Bold', fontSize=13, leading=18, textColor=C_CYAN, spaceAfter=6, spaceBefore=12)
    h3 = ParagraphStyle('DocH3', fontName='NotoSans-Bold', fontSize=10.5, leading=15, textColor=C_NAVY, spaceAfter=4, spaceBefore=8)
    
    q_title = ParagraphStyle('DocQTitle', fontName='NotoSans-Bold', fontSize=10.5, leading=15, textColor=C_ORANGE, spaceAfter=4, spaceBefore=8)
    q_ans = ParagraphStyle('DocQAns', fontName='NotoSans', fontSize=9, leading=13.5, textColor=C_TEXT)
    
    callout_txt = ParagraphStyle('CalloutTxt', fontName='NotoSans', fontSize=8.5, leading=13, textColor=C_NAVY)
    badge_txt = ParagraphStyle('BadgeTxt', fontName='NotoSans-Bold', fontSize=8, leading=10, textColor=colors.white)
    table_cell = ParagraphStyle('TableCell', fontName='NotoSans', fontSize=8, leading=11, textColor=C_TEXT)
    table_hdr = ParagraphStyle('TableHdr', fontName='NotoSans-Bold', fontSize=8.5, leading=11.5, textColor=colors.white)

    story = []

    # =========================================================================
    # COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 20))
    logo_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "images", "Fire-X.jpeg")
    if os.path.exists(logo_path):
        img = Image(logo_path, width=90, height=90)
        story.append(img)
    
    story.append(Spacer(1, 15))
    cover_tag = ParagraphStyle('CoverTag', fontName='NotoSans-Bold', fontSize=9, leading=12, textColor=C_CYAN)
    story.append(Paragraph("NASA INTERNATIONAL SPACE APPS CHALLENGE 2026 // FLAME IN FREEFALL", cover_tag))
    story.append(Spacer(1, 8))
    
    cover_title = ParagraphStyle('CoverTitle', fontName='NotoSans-Bold', fontSize=26, leading=32, textColor=C_PRIMARY)
    story.append(Paragraph("FIRE-X MASTER DOSSIER", cover_title))
    
    cover_sub = ParagraphStyle('CoverSub', fontName='NotoSans-Bold', fontSize=14, leading=19, textColor=C_ORANGE)
    story.append(Paragraph("Mikroyerçəkim Yanma Elmi, Fiziki Testbed Telemetriya Körpüsü və Münsiflərin 31 Sualına Dəqiq Cavablar", cover_sub))
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=2, color=C_CYAN, spaceAfter=15, spaceBefore=0))

    # Meta box
    meta_html = (
        "<b>Komanda:</b> SpaceAz &nbsp;|&nbsp; <b>Məkan:</b> Gəncə, Azərbaycan &nbsp;|&nbsp; <b>Versiya:</b> v2.3 Enterprise Defense Edition<br/>"
        "<b>Komanda Tərkibi:</b> Murad Fatullazada (Hardware), Sabir Məmmədzadə (Backend), Raiz Həkimov (Frontend), Şahvələd Vəlizadə (Kibertəhlükəsizlik), Hüseyn Alırzayev (Data Science)<br/>"
        "<b>Məlumat Bazasının Həcmi:</b> 892 Kanonik Uçuş və Sınaq Rekordu (29 NASA Tədqiqat Ailəsi) &nbsp;|&nbsp; <b>Sitat Rejimi:</b> 100% NASA-STD-3001 Citation-Locked RAG"
    )
    meta_table = Table([[Paragraph(meta_html, callout_txt)]], colWidths=[487])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_BG_CARD),
        ('BOX', (0,0), (-1,-1), 1, C_BORDER),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 15))

    # Executive Overview
    story.append(Paragraph("İCRAÇI XÜLASƏ (EXECUTIVE SUMMARY)", h3))
    exec_text = (
        "Bu sənəd NASA Space Apps Challenge 2026 'Flame in Freefall' (Sərbəst Düşmədə Alov) mövzusunda "
        "mübarizə aparan <b>'SpaceAz'</b> komandasının <b>FIRE-X</b> layihəsi üçün hazırlanmış tam müdafiə sənədidir. "
        "Sənəd dörd əsas bloku birləşdirir: <b>1)</b> NASA çağırışının mikroyerçəkim fizikası və tələbləri, "
        "<b>2)</b> FIRE-X-in fiziki sensor testbedi, riyazi yanma mühərriki və sitat-təsdiqli arxitekturası, "
        "<b>3)</b> NASA PSI rəqəmsal uçuş arxivlərinin dəqiq mənşəyi və <b>4)</b> Münsiflərin (Judges) verə biləcəyi "
        "<b>31 ən çətin, tənqidi və elmi sualın dərhal veriləcək ən mükəmməl cavabları</b>."
    )
    story.append(Paragraph(exec_text, body))
    story.append(Spacer(1, 15))

    # Warning directive box
    dir_html = (
        "<b>⚠️ RƏSMİ UÇUŞ TƏHLÜKƏSİZLİK DİREKTİVİ (NASA-STD-3001):</b><br/>"
        "FIRE-X platforması Qərar Dəstək Sistemidir (Decision Support System — Non-Autonomic). Sistem süni intellektin "
        "uydurma məsləhət verməsinin (hallüsinasiya) qarşısını almaq üçün <b>100% NASA PSI uçuş sınaq nömrələri ilə sitat-təsdiqli (citation-locked)</b> "
        "qurulmuşdur. Əgər sorğu üzrə bazada empirik uçuş datası yoxdursa, avtonom ekstrapolyasiya bloklanır."
    )
    dir_table = Table([[Paragraph(dir_html, callout_txt)]], colWidths=[487])
    dir_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_ORANGE_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_ORANGE),
        ('PADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(dir_table)
    
    story.append(PageBreak())

    # =========================================================================
    # BÖLMƏ 1: NASA SPACE APPS CHALLENGE VƏ "FLAME IN FREEFALL" NƏDİR?
    # =========================================================================
    story.append(Paragraph("BÖLMƏ 1: NASA SPACE APPS 'FLAME IN FREEFALL' ÇAĞIRIŞININ MAHİYYƏTİ", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=C_CYAN, spaceAfter=12, spaceBefore=0))

    story.append(Paragraph("1.1. Çağırışın Rəsmi Missiyası", h2))
    p1 = (
        "NASA Space Apps 2026-nın <b>'Flame in Freefall' (Sərbəst Düşmədə Alov)</b> çağırışı iştirakçılardan "
        "Beynəlxalq Kosmik Stansiyada (BKS), düşmə qüllələrində (Drop Towers) və avtonom kosmik gəmilərdə (Cygnus) "
        "keçirilmiş mikroyerçəkim yanma tədqiqatlarının məlumatlarını analiz edərək kosmik gəmilərin, Ay və Mars "
        "yaşayış modullarının yanğın təhlükəsizliyini təmin edən qabaqcıl süni intellekt və analitika platforması qurmağı tələb edir."
    )
    story.append(Paragraph(p1, body))
    story.append(Spacer(1, 8))

    story.append(Paragraph("1.2. Mikroyerçəkimdə Yanma Niyə Yerdəkindən Tam Fərqlidir?", h2))
    p2 = (
        "Yerdə qravitasiya (1.0g) təbii <b>arximed / istilik konveksiyasını (buoyancy)</b> yaradır: isti, az sıx qazlar "
        "yuxarı qalxır, alova aşağıdan təzə oksigen sorur və tüstü yuxarı yönəlir (alov damcı və şam formalı olur). "
        "Lakin mikroyerçəkimdə (10⁻⁴ – 10⁻⁶ g) təbii konveksiya sıfıra enir. Nəticədə fizika kökündən dəyişir:"
    )
    story.append(Paragraph(p2, body))
    story.append(Spacer(1, 6))

    points = [
        "<b>1. Kürəvi Simmetriya (Spherical Flames):</b> Alov yuxarı dartılmır, yanacaq damcısının və ya brülörün ətrafında mükəmməl kürə forması alır. Yanma yalnız molekulyar diffuziya ilə idarə olunur (Stefan axını).",
        "<b>2. Radiativ Sönmə (Radiative Extinction):</b> Yanma məhsulları (CO₂, H₂O) alovun ətrafında qalaraq onu boğur və his hissəciklərinin güclü istilik şüalanması alovu soyudaraq vaxtından əvvəl qəfil söndürür (Extinction Diameter d<sub>e</sub>).",
        "<b>3. Görünməz Soyuq Alovlar (Cool Flames, 600–800 K):</b> FLEX-2 təcrübələrində sübut olundu ki, görünən isti alov söndükdən sonra belə, alov görünməz şəkildə peroksi-radikal zəncirvari reaksiya ilə aşağı temperaturda yanmağa davam edir və yenidən qəfil alovlanma təhlükəsi yaradır.",
        "<b>4. Aşağı Axın Yanarlıq Piki (Low-Flow Flammability Peak):</b> Durğun 0g havasında materiallar öz tüstüsündə boğulub sönsə də, zəif hava axını (2 – 12 sm/s) verildikdə təzə oksigen çatır, lakin soyuducu güclü külək olmur. Nəticədə alov Yerdəkindən daha sürətlə yayılır!",
        "<b>5. Tüstü Aqreqasiyası:</b> Mikroyerçəkimdə yanma zonası uzun qaldığı üçün tüstü hissəcikləri Yerdəki kimi kiçik qalmır, uzun zəncirvari fraktal aqreqatlara çevrilir."
    ]
    for pt in points:
        story.append(Paragraph(f"• {pt}", body))
        story.append(Spacer(1, 4))

    story.append(Spacer(1, 6))
    story.append(Paragraph("1.3. Nə üçün Yerdəki Standartlar və Sensorlar Kosmosda İflas Edir?", h2))
    p3 = (
        "Yerdə istifadə olunan optik və ionlaşma tüstü detektorları isti havanın tavana qalxmasına arxalanır. "
        "Kosmosda isə konveksiya olmadığı üçün tüstü tavana qalxmır, kabinədə sərbəst üzür. Bundan əlavə, Ay və Marsda "
        "kosmonavtların gətirdiyi incə <b>reqolit tozu (regolith dust)</b> Yerdəki sensorları aldadaraq daimi yalançı həyəcan (false alarm) yaradır. "
        "Məhz buna görə NASA-ya yeni nəsil fiziki telemetriya və riyazi yanma intellekti tələb olunur."
    )
    story.append(Paragraph(p3, body))
    story.append(Spacer(1, 14))

    # =========================================================================
    # BÖLMƏ 2: FIRE-X LAYİHƏSİNİN TAM MİMARİSİ
    # =========================================================================
    story.append(Paragraph("BÖLMƏ 2: FIRE-X PLATFORMASININ TAM MÜHƏNDİSLİK MİMARİSİ", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=C_CYAN, spaceAfter=12, spaceBefore=0))

    story.append(Paragraph("2.1. Layihənin Konseptual Ekosistemi", h2))
    arch_desc = (
        "FIRE-X dörd qarşılıqlı inteqrasiya olunmuş səviyyədən ibarətdir: "
        "<b>1) Fiziki Testbed Edge Node</b> (ESP-32 + SnO₂ elektrokimyəvi və optik sensor), "
        "<b>2) Riyazi Mikroyerçəkim Yanma Mühərriki</b> (`nasa_combustion_engine.py`), "
        "<b>3) İnteraktiv Analitika və 3D Veb İnterfeysləri</b> (FastAPI + Streamlit v2 + Three.js), "
        "və <b>4) Sitat-Təsdiqli Təhlükəsizlik RAG Mühərriki</b> (`citation_rag_engine.py`)."
    )
    story.append(Paragraph(arch_desc, body))
    story.append(Spacer(1, 10))

    # Architecture Table
    arch_table_data = [
        [Paragraph("Səviyyə (Layer)", table_hdr), Paragraph("Texnologiya & Fayl", table_hdr), Paragraph("Funksional Təyinatı & Missiya Əhəmiyyəti", table_hdr)],
        [
            Paragraph("<b>1. Fiziki Testbed Node</b>", table_cell),
            Paragraph("ESP-32 NodeMCU, SnO₂ Sensor, Parametrik 3D Korpus", table_cell),
            Paragraph("Məişət qaz detektoru DEYİL! Kabin daxilində lokal uçucu piroliz qazlarını və optik tüstü sıxlığını real vaxtda ölçərək yanma mühərrikinə sərhəd şərtlərini ötürən fiziki körpüdür.", table_cell)
        ],
        [
            Paragraph("<b>2. Yanma Fizikası Mühərriki</b>", table_cell),
            Paragraph("`backend/nasa_combustion_engine.py` (Python, NumPy, Pandas)", table_cell),
            Paragraph("FLEX d²-qanunu, radiativ sönmə diametri (d<sub>e</sub>), BASS-II məcburi axın alov yayılma sürəti (S<sub>f</sub>), və MOC yanarlıq sərhədlərini hesablayan analitik riyazi mühərrik.", table_cell)
        ],
        [
            Paragraph("<b>3. İnteraktiv Analitika Paneli</b>", table_cell),
            Paragraph("`analytics_dashboard_v2.py` (Streamlit, Plotly)", table_cell),
            Paragraph("NASA PSI uçuş sınaqlarının parametr dəyişməsi ilə alov davranışını proqnozlaşdıran qrafik həllər, d²(t) traektoriyaları və xam CSV arxivlərinin təhlili.", table_cell)
        ],
        [
            Paragraph("<b>4. Sitat-Təsdiqli RAG</b>", table_cell),
            Paragraph("`backend/citation_rag_engine.py` (FastAPI, SQLite)", table_cell),
            Paragraph("Hər bir cavaba rəsmi NASA PSI uçuş sınaq nömrəsini zəncirləyən, qeyri-elmi suallarda hallüsinasiyanı bloklayan NASA-STD-3001 uyğun təhlükəsizlik qoruyucusu.", table_cell)
        ]
    ]
    t_arch = Table(arch_table_data, colWidths=[100, 140, 247])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_BG_CARD]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 12))

    story.append(Paragraph("2.2. Riyazi Yanma Modelləri və Tənliklər", h2))
    p_eq = (
        "Mühərrikimiz iki təməl aerokosmik yanma modelini proqramlaşdırır:<br/><br/>"
        "<b>A) Damcı Yanmasının d²-Qanunu və Radiativ Sönmə (NASA PSI-69 FLEX):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b><font color=\"#00838F\">d²(t) = d₀² − K · t</font></b>,&nbsp;&nbsp;&nbsp;&nbsp;burada&nbsp;&nbsp;<b>K = [ 8 · k<sub>g</sub> / (ρ<sub>l</sub> · c<sub>p,g</sub>) ] · ln(1 + B<sub>q</sub>)</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b><font color=\"#00838F\">d<sub>e</sub> = d₀ · [ 0.32 · (21.0 / X<sub>O₂</sub>)<sup>0.45</sup> · (1 + 0.52 · (X<sub>CO₂</sub> / 50)) · (1 + 0.40 · (X<sub>He</sub> / 40)) ]</font></b><br/>"
        "Burada d<sub>e</sub> radiativ sönmə diametridir. CO₂ istilik şüalanmasını artıraraq sönmə diametrini böyüdür, Helium (He) isə yüksək istilikkeçirmə ilə alov nüvəsini soyudur.<br/><br/>"
        "<b>B) Mikroyerçəkim Məcburi Axında Alov Yayılma Sürəti S<sub>f</sub> (NASA PSI-25 BASS-II & PSI-98 SAFFIRE):</b><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;<b><font color=\"#00838F\">S<sub>f</sub> = S<sub>base</sub> · ((X<sub>O₂</sub> − MOC) / 10) · (P / 101.3)<sup>0.55</sup> · [ (U<sub>inf</sub> / U<sub>peak</sub>) · exp(1 − U<sub>inf</sub> / U<sub>peak</sub>) ]</font></b><br/>"
        "Bu tənlik ventilyator sürəti U<sub>inf</sub> ~ 5 – 12 sm/s olduqda alov yayılma sürətinin pik həddə çatmasını (U<sub>peak</sub>) və Yerdəki normal qravitasiya sürətini aşmasını riyazi sübut edir."
    )
    story.append(Paragraph(p_eq, body))
    story.append(Spacer(1, 14))

    # =========================================================================
    # BÖLMƏ 3: NASA DATALARI HARADAN GƏLİR?
    # =========================================================================
    story.append(Paragraph("BÖLMƏ 3: NASA PSI MƏLUMAT BAZASININ MƏNŞƏYİ VƏ KATALOQU", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=C_CYAN, spaceAfter=12, spaceBefore=0))

    story.append(Paragraph("3.1. Rəsmi Mənbə: NASA Physical Sciences Informatics (PSI)", h2))
    p_psi = (
        "FIRE-X platformasının istifadə etdiyi bütün uçuş telemetriyası NASA-nın <b>Physical Sciences Informatics (PSI)</b> "
        "açıq dövlət elmi arxivindən (https://psi.nasa.gov/) götürülmüşdür. Baza ümumilikdə <b>892 kanonik eksperiment qeydini</b> "
        "(29 unikal araşdırma ailəsi, 45 müxtəlif yanacaq növü, Oksigen faizi 12%-dən 85%-dək, təzyiq 40 kPa-dan 300 kPa-dək, "
        "Sönmə Diametri, Axın Sürəti, CO₂ / He seyreltmə konsentrasiyaları, material növü və avadanlıq tipi) əhatə edir."
    )
    story.append(Paragraph(p_psi, body))
    story.append(Spacer(1, 10))

    # Data Catalog Table
    data_cat = [
        [Paragraph("Tədqiqat (Suite)", table_hdr), Paragraph("Aparat / Qurğu", table_hdr), Paragraph("Sınaq Sayı", table_hdr), Paragraph("Tədqiq Olunan Fiziki Hadisə & Nəticə", table_hdr)],
        [
            Paragraph("<b>FLEX / FLEX-2</b><br/>(PSI-69 / PSI-70)", table_cell),
            Paragraph("ISS CIR<br/>(MDCA / MIST)", table_cell),
            Paragraph("<b>274 sınaq</b>", table_cell),
            Paragraph("Təcrid olunmuş damcıların kürəvi yanması, 70%-dək CO₂ və 45%-dək Helium seyreltmə qazları ilə sönmə hədləri, iki-mərhələli görünməz soyuq alovlar.", table_cell)
        ],
        [
            Paragraph("<b>BASS-I / BASS-II</b><br/>(PSI-25)", table_cell),
            Paragraph("ISS MSG<br/>(SPICE axın kanalı)", table_cell),
            Paragraph("<b>129 sınaq</b>", table_cell),
            Paragraph("Bərk polimer lövhələrin (PMMA) və Nomex parçaların məcburi hava axınında (0–55 sm/s) alovlanması və sönmə sərhədləri.", table_cell)
        ],
        [
            Paragraph("<b>SAFFIRE I–VI</b><br/>(PSI-98)", table_cell),
            Paragraph("Cygnus Gəmisi<br/>(Post-BKS)", table_cell),
            Paragraph("<b>72 sınaq</b>", table_cell),
            Paragraph("Kosmonavtlar ayrıldıqdan sonra Cygnus gəmisində aparılmış 1.0 m miqyaslı real yanğın yayılma sınaqları (21% vs 34% O₂ Artemis atmosferi).", table_cell)
        ],
        [
            Paragraph("<b>ACME Suite</b><br/>(CFI, CFI-G, BRE, E-FIELD, CLD)", table_cell),
            Paragraph("ISS CIR<br/>(Qaz brülörləri)", table_cell),
            Paragraph("<b>186 sınaq</b>", table_cell),
            Paragraph("85% O₂-yə qədər tərs (inside-out) qaz alovları, his konsentrasiyası və +5 kV elektrik sahəsi ilə qismən cazibə təqlidi.", table_cell)
        ],
        [
            Paragraph("<b>SAME & DAFT</b><br/>(SAME-R, DAFT-2)", table_cell),
            Paragraph("ISS MSG<br/>(Aerozol kamerası)", table_cell),
            Paragraph("<b>68 sınaq</b>", table_cell),
            Paragraph("Tüstü hissəciklərinin fraktal zəncirlənməsi və Ay/Mars reqolit tozunun (&gt; 1 μm) tüstüdən (&lt; 0.5 μm) lazerlə fərqləndirilməsi.", table_cell)
        ],
        [
            Paragraph("<b>NASA-STD-6001</b><br/>(Test 1 WSTF)", table_cell),
            Paragraph("WSTF Qravitasiya<br/>Yanma Kamerası", table_cell),
            Paragraph("<b>163 sınaq</b>", table_cell),
            Paragraph("Normal 1.0g yer qravitasiyasında materialların yuxarı alovlanma sınaqları — mikroyerçəkim modelləri üçün yuxarı sərhəd (upper bound).", table_cell)
        ]
    ]
    t_data = Table(data_cat, colWidths=[90, 95, 65, 237])
    t_data.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), C_PRIMARY),
        ('GRID', (0,0), (-1,-1), 0.5, C_BORDER),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, C_BG_CARD]),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(t_data)
    story.append(Spacer(1, 10))

    story.append(Paragraph("3.2. Nə üçün Raket Mühərriki Yanacaqları (Propellants) Xaric Edilib?", h2))
    p_prop = (
        "Bəzi həvəskar layihələr raket yanacaqlarını (LOX / RP-1, hidrogen) qarışdırırlar. NASA-nın 'Flame in Freefall' "
        "təlimatına əsasən, raket mühərrikləri yüksək təzyiqli (&gt; 50 bar) turbulent rejimdə işləyir və orada Froud ədədi Fr &gt;&gt; 1000 olduğu üçün "
        "qravitasiya yanmaya heç bir təsir göstərmir. Çağırışın əsas məğzi kosmik yaşayış modullarındakı <b>zəif laminar axın (0 – 30 sm/s) "
        "və aşağı qravitasiyada kabin yanğın təhlükəsizliyidir</b>. Buna görə raket yanacaqlarının xaric edilməsi elmi cəhətdən 100% doğrudur."
    )
    story.append(Paragraph(p_prop, body))
    story.append(Spacer(1, 14))

    story.append(PageBreak())

    # =========================================================================
    # BÖLMƏ 4: MÜNSİFLƏRİN (JUDGES) 31 KRİTİK SUALINA DƏQİQ CAVABLAR
    # =========================================================================
    story.append(Paragraph("BÖLMƏ 4: MÜNSİFLƏRİN 31 KRİTİK SUALINA RƏSMİ CAVABLAR (JURY DEFENSE)", h1))
    story.append(HRFlowable(width="100%", thickness=1, color=C_ORANGE, spaceAfter=12, spaceBefore=0))

    p_defense_intro = (
        "Bu bölmə münsiflərin təqdimat və ya stend nümayişi zamanı verə biləcəyi 31 ən kəskin, texniki və elmi suala "
        "SpaceAz komandasının hazır, səhvsiz və arqumentləşdirilmiş rəsmi cavablarını ehtiva edir. "
        "Cavablar 6 tematik blokda strukturlaşdırılmışdır:"
    )
    story.append(Paragraph(p_defense_intro, body))
    story.append(Spacer(1, 8))

    questions_data = [
        # BLOK 1: Çağırış Missiyası və Mikroyerçəkim Yanma Elmi
        (
            "Sual 1: NASA Space Apps 'Flame in Freefall' çağırışının əsas məqsədi nədir və FIRE-X bunu necə qarşılayır?",
            "Çağırışın əsas məqsədi mikroyerçəkim şəraitində yanğınların necə yayıldığını, boğulduğunu və söndüyünü öyrənərək gələcək Ay (Artemis) və Mars missiyalarında kosmonavtların təhlükəsizliyini təmin edən həllər yaratmaqdır. FIRE-X NASA-nın rəsmi PSI arxivindəki 892 sınağı birləşdirir, riyazi yanma qanunları ilə modelləşdirir və kosmik stansiyalar üçün sübutlu qərar dəstək sistemi təqdim edir."
        ),
        (
            "Sual 2: Mikroyerçəkimdə yanğın necə davranır və niyə Yerdəki qaydalar kosmosda işləmir?",
            "Yerdə qravitasiya təbii konveksiya yaradır: isti hava qalxır, alova oksigen çəkir və alov konusvari formalaşır. Mikroyerçəkimdə konveksiya sıfırdır. Alov kürəvi simmetriya alır, oksigen yalnız zəif molekulyar diffuziya ilə gəlir və alov öz tüstüsü (CO₂) ilə əhatələnərək tez sönür. Yerdəki yanğın qaydaları kosmosda ona görə işləmir ki, orada hava axını açıldıqda alov gözlənilmədən daha şiddətlə yayılır."
        ),
        (
            "Sual 3: 'Görünməz Soyuq Alov' (Cool Flame) nədir və kosmonavtlar üçün nə dərəcədə təhlükəlidir?",
            "NASA FLEX-2 eksperimentində kəşf edildi ki, alkan damcılarında görünən isti alov söndükdən sonra belə, yanma 600–800 K temperaturda gözəgörünməz şəkildə davam edir. İnsan gözü və standart yanğın detektorları onu görmür. Lakin kabinəyə təsadüfən təzə oksigen daxil olduqda bu soyuq alov dərhal partlayışla yenidən isti alova keçir (re-ignition). FIRE-X soyuq alov hədlərini əvvəlcədən proqnozlaşdırır."
        ),
        (
            "Sual 4: 'Aşağı Axın Yanarlıq Piki' (Low-Flow Flammability Peak) paradoksu nədir?",
            "BKS-də hava tam durğun olduqda alov boğulub sönür. Lakin ventilyasiya fanları işə düşüb zəif hava axını (5 – 12 sm/s) yaratdıqda, axın alova oksigen daşıyır, lakin sürət hələ çox kiçik olduğu üçün alovu soyudub söndürə bilmir. Nəticədə bərk materiallar (PMMA, pambıq) Yerdəki 1.0g çəkimindən daha sürətlə və daha təhlükəli alovlanır. Bu fenomen NASA PSI-25 BASS-II tədqiqatında sübut olunub və mühərrikimizdə modelləşdirilib."
        ),
        (
            "Sual 5: Niyə layihənizdən raket mühərriki yanacaqlarını çıxarmısınız? Bu çatışmazlıq deyilmi?",
            "Qətiyyən çatışmazlıq deyil, əksinə elmi dəqiqliyimizin sübutudur! Raket mühərriklərində yanacaq (LOX / RP-1) 50-100 bar təzyiq altında turbulent injektorlarla püskürdülür və Froud ədədi Fr &gt;&gt; 1000 olur — burada inersiya qravitasiyanı tam üstələyir. 'Flame in Freefall' çağırışının məğzi isə zəif sürətli (0 – 30 sm/s) kabin yanğınlarıdır. Raket yanacağını bura qatmaq fizikadan bixəbərlik olardı."
        ),

        # BLOK 2: Fiziki Donanım və Sensor Düyünü
        (
            "Sual 6: Masadakı cihazınız adi məişət metan qazı detektoruna bənzəyir. Bu kosmik yanma fizikası ilə necə əlaqəlidir?",
            "Bu adi qaz siqnalizasiyası deyil — bu, FIRE-X-in <b>Fiziki Mühit Testbed Node (Atmospheric Boundary Telemetry Node)</b> avadanlığıdır. Cihazımız kosmik modulun lokal bölməsindəki termal parçalanma, ilkin piroliz qazları və optik tüstü qatılığını ölçür. Bu məlumat birbaşa backend-ə ötürülür və `nasa_combustion_engine.py` mühərrikimiz həmin lokal qaz sıçrayışını mikroyerçəkim alov yayılma sürətinə və radiativ sönmə həddinə çevirir."
        ),
        (
            "Sual 7: ESP-32 mikrokontrolleri və sensor dövrəsi necə proqramlaşdırılıb?",
            "ESP-32 NodeMCU mikrokontrollerində SnO₂ elektrokimyəvi sensorun analoq çıxışı 12-bitlik daxili ADC (GPIO 34) vasitəsilə oxunur. GPIO 34 ADC1 blokuna aid olduğu üçün Wi-Fi ötürülməsi zamanı oxunuşlarda küy yaranmır. Cihaz FreeRTOS taymeri ilə hər 1.5 saniyədən bir JSON telemetriya paketini HTTP POST sorğusu ilə `/api/sensor-data` endpointinə göndərir."
        ),
        (
            "Sual 8: Cihazın 3D korpusunun dizaynında hansı mühəndislik həlləri tətbiq olunub?",
            "Korpus xüsusi olaraq mikroyerçəkim ventilyasiya standartlarına uyğun modelləşdirilib. Yan tərəflərdə hava dövranını təmin edən aerodinamik louver qəfəsləri, daxildə ESP32 və sensoru təcrid edən arakəsmə, Type-C enerji portu kəsiyi və səs xəbərdarlığı üçün akustik pəncərələr qoyulub. Model tamamilə sukeçirməz (watertable) manifold mesh olaraq 3D çap üçün hazırdır və platformamızda interaktiv 3D turntable ilə nümayiş etdirilir."
        ),
        (
            "Sual 9: Bu sensor qurğusu birbaşa kosmosa uçmağa hazırdırmı?",
            "Hazırkı qurğu Yerüstü Funksional Testbed Prototipidir (TRL-4 səviyyəsi). Kosmik uçuş (TRL-7/8) üçün mikrokontroller radiasiyaya davamlı (rad-hard, məsələn Vorago və ya BAE rad-tolerant çiplər) arxitekturaya keçirilməli, sensor isə hermetik teflon örtüklü NASA-STD-6001 B sinifli material korpusa yerləşdirilməlidir. Bizim arxitektura tam modulyardır və istənilən kosmik sensor şinasına (MIL-STD-1553 və ya SpaceWire) asanlıqla inteqrasiya oluna bilir."
        ),
        (
            "Sual 10: Əgər internet kəsilsə və ya cihaz sönərsə, sisteminiz dayanırmı?",
            "Xeyr, qətiyyən dayanmır. Backend-də quraşdırdığımız avtomatik `Watchdog & Testbed Simulator` rejimi var. Əgər fiziki cihazdan 10 saniyə ərzində paket gəlmirsə, sistem avtomatik olaraq 'STANDBY' rejiminə keçir və münsiflərə nümayiş üçün daxili riyazi test simulyatorunu aktivləşdirməyə imkan verir."
        ),

        # BLOK 3: NASA Məlumat Bazası (PSI) və Datanın Mənşəyi
        (
            "Sual 11: NASA-nın hansı rəsmi bazalarından istifadə etmisiniz və datanın mənbəyi haradır?",
            "Əsas mənbəyimiz NASA-nın rəsmi <b>Physical Sciences Informatics (PSI)</b> sistemidir. Buraya Glenn Tədqiqat Mərkəzi (GRC) və Marshall Kosmik Uçuş Mərkəzi (MSFC) tərəfindən idarə olunan BKS uçuş təcrübələrinin rəqəmsal telemetriya cədvəlləri daxildir. Həmçinin NASA NTRS (Technical Reports Server) və WSTF (White Sands Test Facility) sınaq protokollarından istifadə olunub."
        ),
        (
            "Sual 12: Baza daxilində neçə eksperiment var və onların tərkibi nədir?",
            "Verilənlər bazamızda (`fire_safety.db`) <b>892 kanonik uçuş və yerüstü sərhədləmə sınağı</b> var. Bu sınaqlar 29 fərqli araşdırma ailəsini, 12%-dən 85%-ə qədər oksigen konsentrasiyalarını, 40-dan 300 kPa-dək təzyiqləri, həmçinin CO₂ (70%-dək) və Helium (45%-dək) seyreltmə qazlarını əhatə edir."
        ),
        (
            "Sual 13: BKS-dəki CIR və MSG laboratoriyalarının fərqi nədir və siz hansı dataları götürmüsünüz?",
            "CIR (Combustion Integrated Rack) BKS-in ABŞ 'Destiny' laboratoriyasında yerləşən, optik diaqnostika kameraları və radiometrlərlə təchiz olunmuş hermetik yanma kamerasıdır (buradan FLEX damcı və ACME qaz alovları götürülüb). MSG (Microgravity Science Glovebox) isə əlcəkli izolyasiya edilmiş iş kamerasıdır — buradan isə SPICE axın kanalında bərk cisimlərin yanmasını öyrənən BASS-II və aerozol sınaqları olan SAME/DAFT dataları götürülüb."
        ),
        (
            "Sual 14: SAFFIRE eksperimenti nədir və niyə kosmonavtlar olmayan gəmidə aparılıb?",
            "BKS-də kosmonavtların həyatını riskə atmamaq üçün 10-15 sm-dən böyük yanğın sınaqları qadağandır. Buna görə NASA 'SAFFIRE' tədqiqatını BKS-i tərk edib Yer atmosferində yanmağa gedən pilotsuz 'Cygnus' yük gəmisinin daxilində apardı. Gəmidə 1.0 metr ölçülü böyük parçalar yandırıldı. Biz SAFFIRE I-dən VI-ya qədər olan 72 böyük miqyaslı yanğın sınağını bazamıza daxil etmişik."
        ),
        (
            "Sual 15: NASA-STD-6001 Test 1 nədir və bu yer sınağının kosmik layihədə nə işi var?",
            "NASA-STD-6001 Test 1 — NASA-nın White Sands bazasında (WSTF) tətbiq etdiyi rəsmi material alovlanma sınağıdır. Bu test 1.0g normal cazibədə materialın 15 sm-dən çox yanıb-yanmadığını yoxlayır. Biz bu 163 sınağı mikroyerçəkim üçün <b>yuxarı sərhəd (upper bound)</b> kimi istifadə edirik ki, 0g ilə 1g arasındakı fərqi riyazi olaraq dəqiq məhdudlaşdıraq."
        ),

        # BLOK 4: Riyazi Modellər və Yanma Fizikası Mühərriki
        (
            "Sual 16: Datalar üzərində real riyazi və prediktiv modellər necə qurulub?",
            "Biz sadəcə qrafik çəkməmişik; `backend/nasa_combustion_engine.py` modulunda fiziki qanunları kodlaşdırmışıq. Məsələn, istifadəçi oksigeni 21%-dən 34%-ə qaldırdıqda və ventilyator axınını 8 sm/s etdikdə, sistem Fernandez-Pello tənliyi ilə PMMA üçün alov yayılma sürətini dərhal S<sub>f</sub> = 0.404 mm/s olaraq dəqiq hesablayır və təhlükə səviyyəsini 'ELEVATED' olaraq çıxarır."
        ),
        (
            "Sual 17: Damcı yanmasında CO₂ və Helium qazlarının təsirini necə fərqləndirirsiniz?",
            "NASA PSI-69 FLEX məlumatları göstərir ki, CO₂ və Helium fərqli fiziki mexanizmlərlə alovu söndürür. CO₂ yüksək molyar kütləyə malikdir və radiativ şüalanmanı kəskin artıraraq alovu boğur (sönmə diametrini d<sub>e</sub> böyüdür). Helium isə azotdan 6 dəfə yüksək istilikkeçirmə qabiliyyətinə malikdir və istiliyi alovdan dərhal kənara sovuraraq keçiricilik yolu ilə soyudur. Modelimiz hər iki qazın faizini ayrı-ayrı tənliklə hesablayır."
        ),
        (
            "Sual 18: Bərk materialların yanma hədlərini (MOC) necə hesablayırsınız?",
            "MOC (Minimum Oxygen Concentration) materialın yanmanı davam etdirə biləcəyi ən aşağı oksigen faizidir. Durğun 0g havasında PMMA üçün MOC 21.0%-dir (yəni 21%-də belə sönür). Lakin zəif hava axını (8 sm/s) verildikdə MOC 14.5%-ə düşür! Yəni oksigen azalsa belə yanğın dayanmır. Mühərrikimiz havalandırma sürətindən asılı olaraq dinamik MOC həddini eksponensial tənliklə hesablayır."
        ),
        (
            "Sual 19: FHI (Fire Hazard Index) nədir və necə hesablanır?",
            "FHI (0.0 – 10.0) — yanğın riskini kompleks qiymətləndirən patentləşdirilə bilən indeksimizdir. O, baza oksigen qatılığı (O₂ / 21)<sup>1.5</sup>, təzyiq əmsalı (P / 101.3)<sup>0.4</sup>, fiziki testbeddən gələn piroliz uçucu maddələri (PPM) və optik tüstü sıxlığı (Smoke %) faktorlarının çəkili inteqrasiyası ilə hesablanır. 0–3.5 aşağı, 3.5–6.8 nominal, 6.8–8.5 yüksək, 8.5–10.0 kritik təhlükədir."
        ),
        (
            "Sual 20: Bazanızda Ay (0.16g) və Mars (0.38g) uçuş sınaqları varmı? Yoxdursa, bunu necə hesablayırsınız?",
            "Bu suala səmimi və ən elmi cavab: Hazırda bütün dünyada və NASA PSI-da heç kimdə birbaşa qismən cazibə uçuş sınağı YOXDUR! Çünki NASA-nın LUCI və FM2 qismən cazibə santrifuqa aparatları hələ kosmosa uçmayıb. FIRE-X burada dünya elmi üçün ən etibarlı metodu tətbiq edir: <b>0g–1g Bounding Modeli</b>. Biz Ayın 0.16g cazibəsini u<sub>b</sub> = sqrt(g · β · ΔT · L) ~ 12.2 sm/s ekvivalent konvektiv axın sürətinə çevirərək BASS-II və SAFFIRE məlumatları ilə dəqiq sərhədləyirik."
        ),

        # BLOK 5: Süni İntellekt (AI), RAG və Uçuş Təhlükəsizliyi
        (
            "Sual 21: Kosmosda həyati təhlükə anında süni intellektə güvənmək olarmı? Hallüsinasiya etsə nə olar?",
            "Məhz buna görə biz standart ChatGPT tipli sərbəst çatbot qurmadıq! Biz <b>Citation-Locked (Sitat-Təsdiqli) RAG</b> arxitekturası tətbiq etdik. Model hər bir tövsiyə üçün mütləq arxasında duran real NASA uçuş sınaq nömrəsini göstərməlidir. Əgər sual uydurmadırsa və bazada qarşılığı yoxdursa, modelin cavab uydurması proqram səviyyəsində qadağan edilib."
        ),
        (
            "Sual 22: Citation-Locked RAG kod səviyyəsində necə işləyir?",
            "`backend/citation_rag_engine.py` modulunda sorğu daxil olduqda əvvəlcə SQLite bazasındakı sınaqlar axtarılır. Tapılan rəsmi qeydlər prompt-a rəsmi sitat kodu kimi (`[Source: NASA BASS-II, PSI-ID: 25, Run: BASS-14]`) ötürülür. Çıxış mətni yoxlanılır; əgər sitat yoxdursa və ya empirik baza boşdursa, NASA-STD-3001 fallback mətni qaytarılır."
        ),
        (
            "Sual 23: Əgər istifadəçi bazada olmayan qeyri-elmi və ya zərərli sual versə, AI necə reaksiya verir?",
            "Sistem dərhal rəsmi təhlükəsizlik bildirişi qaytarır: '⚠️ Insufficient empirical data in NASA PSI records for this specific query. Per NASA-STD-3001 spaceflight safety directives, autonomous AI extrapolation is inhibited...' Yəni heç bir halda təsdiqlənməmiş fərziyyə irəli sürülmür."
        ),
        (
            "Sual 24: Bu sistem avtonom idarəedicidir (autopilot), yoxsa qərar dəstək sistemi?",
            "Bütün interfeyslərimizdə açıq xəbərdarlıq qoyulub: <b>'FIRE-X Decision Support System — Empirical Analytics & Reference Tool (Non-Autonomic)'</b>. Bu sistem qərar qəbul edən uçuş mühəndisinə və Hyuston Uçuş Nəzarət Mərkəzinə (MCC-H) saniyələr içində 892 sınağın elmi nəticəsini xatırladan analitik məsləhətçi alətdir."
        ),
        (
            "Sual 25: Platforma hansı dilləri dəstəkləyir və Azərbaycan dili necə təmin olunub?",
            "Platformamız 100% ikidillidir (İngilis və Azərbaycan). Bütün naviqasiya, 3D laboratoriya, simulyator və AI köməkçi Azərbaycan dilində xalis elmi terminologiya ilə cavab verir. İstifadəçi bir kliklə dillər arasında keçid edə bilir."
        ),

        # BLOK 6: Missiyalar, Yerə Transfer (Spin-Off) və Gələcək İnkişaf
        (
            "Sual 26: Artemis Ay Yaşayış Modulunun atmosferi (34% O₂, 56.5 kPa) BKS-dən niyə qat-qat təhlükəlidir?",
            "BKS atmosferi Yerdəki kimidir (21% O₂, 101.3 kPa). Lakin NASA Artemis missiyalarında skafandr çıxışlarını (EVA) asanlaşdırmaq üçün kabinəni 34% O₂ və aşağı təzyiqdə (56.5 kPa) saxlayacaq. Oksigen 34%-ə qalxdıqda materialların alovlanma müqaviməti çökür, yanma sürəti 2 dəfədən çox artır və Yerdə çətin yanan maddələr belə barıt kimi alışır. FIRE-X Artemis üçün FHI indeksini 8.3 (Kritik) olaraq hesablayır."
        ),
        (
            "Sual 27: Ay/Mars Roveri və EVA Skafandrı (85-100% O₂) üçün hansı nəticələr əldə etmisiniz?",
            "EVA skafandrları 100%-ə yaxın təmiz oksigendə işləyir. ACME CFI-G eksperimentindən götürdüyümüz 85% O₂ sınaqları göstərir ki, bu şəraitdə hər hansı mikroskopik qığılcım qarşısıalınmaz diffuziya partlayışına səbəb ola bilər. Buna görə skafandrlarda yalnız Teflon, Beta-parça və qızıl suyuna çəkilmiş polimerlər istifadə edilməlidir."
        ),
        (
            "Sual 28: SAME və DAFT eksperimentlərinin Ay tozu (regolith) ilə bağlı kəşfi nədir?",
            "Ay və Mars səthindəki reqolit tozu iti, elektrostatik yüklü hissəciklərdən ibarətdir (&gt; 1 μm). Kosmonavt kabinəyə qayıtdıqda bu toz havaya qalxır və tüstü detektorlarını aldadır. NASA DAFT sınaqları çox-bucaqlı optik səpilmə nisbəti ilə sub-mikron tüstü (&lt; 0.5 μm) ilə mineral reqolit tozunu bir-birindən ayıran dalğa uzunluqlarını müəyyən edib."
        ),
        (
            "Sual 29: Bu layihənin Yerdə (gündəlik həyatda) hansı spin-off tətbiqləri və faydası var?",
            "Mikroyerçəkim tədqiqatları Yerdə 3 böyük sənayeni dəyişdirir: 1) Məlumat mərkəzləri (Data Centers) və sualtı qayıqlar üçün su damcıları ilə söndürmə (Fine Water Mist) sistemləri, 2) Tozlu zavodlarda və mədənlərdə yalançı həyəcan verməyən fotoelektrik tüstü sensorları, 3) Yanğınsöndürənlər üçün yüksək temperatur və zəhərli qaz buraxmayan yeni nəsil kompozit geyimlər (PBI/Nomex)."
        ),
        (
            "Sual 30: Siz bu layihəni hackathon (14-15 Noyabr) müddətində hazırlamısınız, yoxsa köhnə layihədir?",
            "Layihənin bütün əsas elmi nüvəsi və analitik modulları məhz hackathon zamanı sıfırdan mühəndisliklə yazılıb! GitHub repozitoriyamızda və README sənədimizdəki şəffaf cədvəldə göstərildiyi kimi: `backend/nasa_combustion_engine.py` (riyazi yanma fizikası), `backend/citation_rag_engine.py` (sitat-təsdiqli RAG), `analytics_dashboard_v2.py` (Streamlit paneli) və fiziki cihazın telemetriya körpüsü məhz hackathon günlərində yazılaraq 1,020+ yeni sətirlə commit olunub."
        ),
        (
            "Sual 31: Komandanızın tərkibi və iş bölgüsü necə qurulub?",
            "SpaceAz komandası 5 nəfərdən ibarətdir və hər kəs konkret ixtisaslaşmış sahəyə cavabdehdir: Murad Fatullazada (Hardware, ESP32 və 3D CAD), Sabir Məmmədzadə (Backend arxitekturası və FastAPI), Raiz Həkimov (Frontend, Three.js 3D WebGL və UI/UX), Şahvələd Vəlizadə (Kibertəhlükəsizlik və sitat qoruyucusu), Hüseyn Alırzayev (Data Science və NASA PSI modelləşdirməsi). Biz fərqli şəhərlərdən (Bakı, Sumqayıt, Qusar, Şəmkir) gələrək vahid bir arxitektura qurduq."
        )
    ]

    for idx, (q, a) in enumerate(questions_data, start=1):
        q_box = [
            Paragraph(f"<b>{q}</b>", q_title),
            Spacer(1, 3),
            Paragraph(a, q_ans)
        ]
        q_table = Table([[q_box]], colWidths=[487])
        q_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), C_BG_CARD if idx % 2 == 1 else colors.HexColor("#FFFFFF")),
            ('BOX', (0,0), (-1,-1), 0.5, C_BORDER),
            ('LEFTPADDING', (0,0), (-1,-1), 10),
            ('RIGHTPADDING', (0,0), (-1,-1), 10),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ]))
        story.append(q_table)
        story.append(Spacer(1, 6))

    # Concluding stamp
    story.append(Spacer(1, 10))
    stamp_html = (
        "<b>RƏSMİ TƏSDİQ VƏ BƏYANAT:</b><br/>"
        "FIRE-X NASA Space Apps Challenge 2026 Flame in Freefall çağırışının bütün münsif meyarlarına (Impact, Creativity, "
        "Validity & Relevance, Technical Achievement, Presentation) tam cavab verir. Bu sənəddəki məlumatlar NASA PSI "
        "və rəsmi kosmik uçuş hesabatları ilə 100% təsdiqlənmişdir.<br/>"
        "<b>© 2026 SpaceAz Team // Bütün hüquqlar qorunur.</b>"
    )
    stamp_table = Table([[Paragraph(stamp_html, callout_txt)]], colWidths=[487])
    stamp_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), C_CYAN_LIGHT),
        ('BOX', (0,0), (-1,-1), 1, C_CYAN),
        ('PADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(stamp_table)

    # Build the document using NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Master Dossier successfully generated at: {filename}")


if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else "FIRE-X_NASA_SpaceApps_Master_Dossier_31_Questions.pdf"
    build_pdf(target)
