import re
from datetime import datetime
from io import BytesIO
from typing import Optional
from xml.sax.saxutils import escape

from flask import Flask, render_template, request, send_file
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer

app = Flask(__name__, static_folder="public", static_url_path="")


@app.get("/")
def landing():
    return render_template("index.html", title="GeneratorCV")


@app.get("/form")
def form_page():
    return render_template("form.html", title="Gerar curriculo | GeneratorCV")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "curriculo"


def _clean_text(value: Optional[str]) -> str:
    return (value or "").strip()


def _paragraph(text: Optional[str], fallback: str) -> str:
    cleaned = _clean_text(text)
    if not cleaned:
        return fallback
    safe = escape(cleaned)
    return safe.replace("\n", "<br/>")


def _format_skills(text: Optional[str]) -> str:
    cleaned = _clean_text(text)
    if not cleaned:
        return ""
    parts = [item.strip() for item in re.split(r"[,\n]", cleaned) if item.strip()]
    return " | ".join(parts) if parts else cleaned


def build_pdf(data: dict[str, str]) -> BytesIO:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=48,
        rightMargin=48,
        topMargin=48,
        bottomMargin=48,
        title="GeneratorCV",
        author=data.get("full_name", "") or "GeneratorCV",
    )

    styles = getSampleStyleSheet()
    name_style = ParagraphStyle(
        "Name",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=24,
        textColor=HexColor("#0f172a"),
        spaceAfter=6,
    )
    title_style = ParagraphStyle(
        "Title",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=12,
        textColor=HexColor("#475569"),
        spaceAfter=6,
    )
    contact_style = ParagraphStyle(
        "Contact",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        textColor=HexColor("#475569"),
        spaceAfter=16,
    )
    section_style = ParagraphStyle(
        "Section",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12,
        textColor=HexColor("#f59e0b"),
        spaceBefore=10,
        spaceAfter=6,
    )
    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        textColor=HexColor("#1f2937"),
    )

    full_name = _clean_text(data.get("full_name")) or "Seu nome"
    title = _clean_text(data.get("title"))
    contact_parts = [
        _clean_text(data.get("email")),
        _clean_text(data.get("phone")),
        _clean_text(data.get("location")),
    ]
    contact_line = " | ".join([part for part in contact_parts if part])

    story = [Paragraph(full_name, name_style)]
    if title:
        story.append(Paragraph(title, title_style))
    if contact_line:
        story.append(Paragraph(contact_line, contact_style))
    else:
        story.append(Spacer(1, 12))

    story.append(Paragraph("Resumo", section_style))
    story.append(
        Paragraph(
            _paragraph(data.get("summary"), "Sem resumo informado."),
            body_style,
        )
    )

    story.append(Paragraph("Experiencia", section_style))
    story.append(
        Paragraph(
            _paragraph(data.get("experience"), "Sem experiencia informada."),
            body_style,
        )
    )

    story.append(Paragraph("Educacao", section_style))
    story.append(
        Paragraph(
            _paragraph(data.get("education"), "Sem educacao informada."),
            body_style,
        )
    )

    story.append(Paragraph("Habilidades", section_style))
    skills = _format_skills(data.get("skills"))
    story.append(Paragraph(_paragraph(skills, "Sem habilidades informadas."), body_style))

    doc.build(story)
    buffer.seek(0)
    return buffer


@app.post("/generate")
def generate_pdf():
    data = {
        "full_name": request.form.get("full_name", ""),
        "title": request.form.get("title", ""),
        "email": request.form.get("email", ""),
        "phone": request.form.get("phone", ""),
        "location": request.form.get("location", ""),
        "summary": request.form.get("summary", ""),
        "experience": request.form.get("experience", ""),
        "education": request.form.get("education", ""),
        "skills": request.form.get("skills", ""),
    }
    pdf_buffer = build_pdf(data)
    timestamp = datetime.utcnow().strftime("%Y%m%d")
    filename = f"{slugify(data.get('full_name', '') or 'curriculo')}-{timestamp}.pdf"
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=filename,
        mimetype="application/pdf",
    )
