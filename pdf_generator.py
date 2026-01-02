"""
pdf_generator.py

Formatted, institution-grade PDF generation.
Text wrapping, spacing, and visual hierarchy handled explicitly.
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from textwrap import wrap


def draw_paragraph(c, text, x, y, max_width_chars=90, line_height=14):
    """
    Draw a wrapped paragraph and return the updated y-position.
    """
    wrapped_lines = wrap(text, max_width_chars)
    for line in wrapped_lines:
        c.drawString(x, y, line)
        y -= line_height
    return y


def generate_planning_pdf(
    file_path: str,
    location: str,
    date: str,
    summary_facts: dict,
    decision: dict,
    explanation: str,
    intent: str
):
    # ---- Context-aware title ----
    if intent == "school":
        title = "School Outdoor Heat Risk Planning Summary"
    elif intent == "construction":
        title = "Construction Heat Exposure Planning Summary"
    else:
        title = "Outdoor Heat Risk Planning Summary"

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    x_margin = 2 * cm
    y = height - 2 * cm

    # ---- Title ----
    c.setFont("Helvetica-Bold", 16)
    c.drawString(x_margin, y, title)
    y -= 24

    # ---- Metadata ----
    c.setFont("Helvetica", 10)
    c.drawString(x_margin, y, f"Location: {location}")
    y -= 14
    c.drawString(x_margin, y, f"Date: {date}")
    y -= 24

    # ---- PLANNING DECISION (MOST IMPORTANT SECTION) ----
    c.setFont("Helvetica-Bold", 13)
    c.drawString(x_margin, y, "Planning Decision")
    y -= 18

    verdict = decision.get("verdict", "UNAVAILABLE")
    reason = decision.get("reason", "")

    # Visual emphasis for verdict
    c.setFont("Helvetica-Bold", 11)
    c.drawString(x_margin, y, f"Recommended Action: {verdict}")
    y -= 16

    c.setFont("Helvetica", 10)
    y = draw_paragraph(
        c,
        f"Rationale: {reason}",
        x_margin,
        y,
        max_width_chars=95
    )

    y -= 24

    # ---- Planning Overview ----
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x_margin, y, "Planning Overview")
    y -= 16

    c.setFont("Helvetica", 10)
    y = draw_paragraph(c, explanation, x_margin, y)
    y -= 20

    # ---- Forecast Highlights ----
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x_margin, y, "Key Forecast Highlights")
    y -= 16

    c.setFont("Helvetica", 10)

    max_temp = summary_facts.get("max_temperature")
    peak_humidity = summary_facts.get("peak_humidity")
    high_risk_hours = summary_facts.get("high_risk_hours", [])

    if max_temp is not None:
        c.drawString(x_margin, y, f"• Maximum temperature: {max_temp}°C")
        y -= 14

    if peak_humidity is not None:
        c.drawString(x_margin, y, f"• Peak humidity: {peak_humidity}%")
        y -= 14

    if high_risk_hours:
        c.drawString(
            x_margin,
            y,
            f"• Elevated heat risk periods: {', '.join(high_risk_hours)}"
        )
        y -= 14

    y -= 30

    # ---- Disclaimer ----
    c.setFont("Helvetica-Oblique", 9)
    disclaimer = (
        "This document is intended to support planning decisions and does not "
        "replace official weather advisories or institutional safety protocols."
    )
    draw_paragraph(c, disclaimer, x_margin, y, max_width_chars=100, line_height=12)

    c.save()
