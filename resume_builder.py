from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, HRFlowable,
    Table, TableStyle, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

# ─── SAMPLE DATA ────────────────────────────────────────────────────────────
data = {
    "name": "John Doe",
    "profession": "Software Engineer",
    "email": "john.doe@example.com",
    "phone": "(123) 456-7890",
    "linkedin": "linkedin.com/in/johndoe",
    "github": "github.com/johndoe",
    "summary": (
        "Experienced software engineer with 5+ years building scalable web "
        "applications. Proficient in Python, JavaScript, and cloud infrastructure. "
        "Passionate about clean code, performance optimization, and mentoring junior "
        "developers. Proven track record of delivering complex projects on time."
    ),
    "skills": ["Python", "JavaScript", "React", "Node.js", "SQL", "AWS", "Docker", "Git"],
    "soft_skills": ["Leadership", "Communication", "Problem Solving", "Teamwork"],
    "experience": [
        {
            "title": "Software Engineer at ABC Corp",
            "date": "2020 – Present",
            "description": (
                "Developed and maintained high-traffic web applications using React "
                "and Node.js. Reduced page load times by 40% through code splitting "
                "and caching strategies. Led a team of 4 engineers on a microservices migration."
            ),
        },
        {
            "title": "Junior Developer at XYZ Tech",
            "date": "2018 – 2020",
            "description": (
                "Assisted with full-stack feature development, testing, and documentation. "
                "Built internal tooling that saved the QA team 10 hours per week."
            ),
        },
    ],
    "degree": "Bachelor of Science in Computer Science",
    "university": "University of Technology",
    "graduation_date": "2018",
    "gpa": "3.8 / 4.0",
    "certifications": [
        "AWS Certified Developer – Associate",
        "Google Analytics Certification",
    ],
    "projects": [
        {
            "title": "E-Commerce Platform",
            "description": "Full-stack store built with React, Node.js, and PostgreSQL. Supports 10k+ monthly active users.",
        },
        {
            "title": "ML Predictive Analytics Tool",
            "description": "Developed a demand-forecasting model using scikit-learn that improved inventory accuracy by 25%.",
        },
    ],
    "languages": ["English (Fluent)", "Spanish (Intermediate)"],
}

# ─── COLOURS ────────────────────────────────────────────────────────────────
PURPLE       = colors.HexColor("#667eea")
DARK         = colors.HexColor("#333333")
MEDIUM       = colors.HexColor("#555555")
LIGHT        = colors.HexColor("#777777")
SKILL_BG     = colors.HexColor("#f0f4ff")
WHITE        = colors.white

# ─── STYLES ─────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

s_name = ParagraphStyle("name",
    fontSize=24, fontName="Helvetica-Bold",
    textColor=DARK, alignment=TA_CENTER, spaceAfter=4)

s_profession = ParagraphStyle("profession",
    fontSize=14, fontName="Helvetica",
    textColor=PURPLE, alignment=TA_CENTER, spaceAfter=6)

s_contact = ParagraphStyle("contact",
    fontSize=9, fontName="Helvetica",
    textColor=MEDIUM, alignment=TA_CENTER, spaceAfter=2)

s_section = ParagraphStyle("section",
    fontSize=11, fontName="Helvetica-Bold",
    textColor=DARK, spaceBefore=10, spaceAfter=4)

s_body = ParagraphStyle("body",
    fontSize=9.5, fontName="Helvetica",
    textColor=colors.HexColor("#444444"), leading=14, spaceAfter=4)

s_item_title = ParagraphStyle("item_title",
    fontSize=10, fontName="Helvetica-Bold",
    textColor=DARK, spaceAfter=1)

s_item_sub = ParagraphStyle("item_sub",
    fontSize=9.5, fontName="Helvetica-Oblique",
    textColor=MEDIUM, spaceAfter=2)

s_date = ParagraphStyle("date",
    fontSize=9, fontName="Helvetica",
    textColor=LIGHT, alignment=TA_LEFT)

# ─── HELPERS ────────────────────────────────────────────────────────────────
def section_header(title):
    return [
        Spacer(1, 6),
        Paragraph(title, s_section),
        HRFlowable(width="100%", thickness=1.2, color=PURPLE, spaceAfter=5),
    ]

def skill_pill_table(skill_list, col_count=5):
    """Lay skills out as a wrapped pill-style table."""
    rows = []
    row = []
    for i, skill in enumerate(skill_list):
        cell = Paragraph(skill, ParagraphStyle("pill",
            fontSize=8.5, fontName="Helvetica",
            textColor=PURPLE, alignment=TA_CENTER))
        row.append(cell)
        if len(row) == col_count:
            rows.append(row)
            row = []
    if row:
        # Pad with empty cells
        while len(row) < col_count:
            row.append(Paragraph("", s_body))
        rows.append(row)

    col_w = (6.5 * inch) / col_count
    t = Table(rows, colWidths=[col_w] * col_count, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), SKILL_BG),
        ("ROUNDEDCORNERS", [6]),
        ("TOPPADDING",    (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [SKILL_BG]),
        ("GRID", (0, 0), (-1, -1), 0, WHITE),
        ("BOX",  (0, 0), (-1, -1), 0, WHITE),
    ]))
    return t

def exp_block(title, date, description):
    title_date = Table(
        [[Paragraph(title, s_item_title), Paragraph(date, s_date)]],
        colWidths=[4.5 * inch, 2 * inch]
    )
    title_date.setStyle(TableStyle([
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING",   (0, 0), (-1, -1), 0),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 0),
        ("TOPPADDING",    (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
        ("ALIGN",         (1, 0), (1, 0), "RIGHT"),
    ]))
    return KeepTogether([
        title_date,
        Paragraph(description, s_body),
        Spacer(1, 4),
    ])

# ─── BUILD ──────────────────────────────────────────────────────────────────
output_path = "/mnt/user-data/outputs/resume.pdf"

doc = SimpleDocTemplate(
    output_path,
    pagesize=letter,
    leftMargin=0.75 * inch,
    rightMargin=0.75 * inch,
    topMargin=0.6 * inch,
    bottomMargin=0.6 * inch,
)

story = []

# Header
story.append(Paragraph(data["name"], s_name))
story.append(Paragraph(data["profession"], s_profession))

contact_parts = [data["email"], data["phone"]]
if data.get("linkedin"):
    contact_parts.append(data["linkedin"])
if data.get("github"):
    contact_parts.append(data["github"])
story.append(Paragraph("  •  ".join(contact_parts), s_contact))
story.append(HRFlowable(width="100%", thickness=2, color=PURPLE, spaceAfter=6))

# Summary
story += section_header("PROFESSIONAL SUMMARY")
story.append(Paragraph(data["summary"], s_body))

# Technical Skills
story += section_header("TECHNICAL SKILLS")
story.append(skill_pill_table(data["skills"], col_count=5))

# Soft Skills
if data.get("soft_skills"):
    story += section_header("SOFT SKILLS")
    story.append(skill_pill_table(data["soft_skills"], col_count=4))

# Experience
story += section_header("PROFESSIONAL EXPERIENCE")
for exp in data["experience"]:
    story.append(exp_block(exp["title"], exp["date"], exp["description"]))

# Education
story += section_header("EDUCATION")
story.append(exp_block(
    data["degree"],
    data["graduation_date"],
    data["university"] + (f"  —  GPA: {data['gpa']}" if data.get("gpa") else "")
))

# Certifications
if data.get("certifications"):
    story += section_header("CERTIFICATIONS")
    for cert in data["certifications"]:
        story.append(Paragraph(f"• {cert}", s_body))

# Projects
if data.get("projects"):
    story += section_header("PROJECTS")
    for proj in data["projects"]:
        story.append(KeepTogether([
            Paragraph(proj["title"], s_item_title),
            Paragraph(proj["description"], s_body),
            Spacer(1, 3),
        ]))

# Languages
if data.get("languages"):
    story += section_header("LANGUAGES")
    story.append(skill_pill_table(data["languages"], col_count=4))

doc.build(story)
print(f"✅  Resume saved to: {output_path}")
