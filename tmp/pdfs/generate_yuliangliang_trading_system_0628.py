from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Preformatted,
)


SRC = Path("俞亮亮交易体系0628版.md")
OUT = "output/pdf/俞亮亮的交易体系0628版.pdf"
FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"


def reg_font():
    pdfmetrics.registerFont(TTFont("STHeiti", FONT))


def make_styles():
    sample = getSampleStyleSheet()
    base = ParagraphStyle(
        "BaseCN",
        parent=sample["Normal"],
        fontName="STHeiti",
        fontSize=8.8,
        leading=13.2,
        textColor=colors.HexColor("#202124"),
        alignment=TA_LEFT,
        spaceAfter=4,
    )
    return {
        "base": base,
        "title": ParagraphStyle(
            "TitleCN",
            parent=base,
            fontSize=22,
            leading=29,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111827"),
            spaceAfter=12,
        ),
        "subtitle": ParagraphStyle(
            "SubtitleCN",
            parent=base,
            fontSize=9.5,
            leading=15,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4b5563"),
            spaceAfter=10,
        ),
        "h1": ParagraphStyle(
            "H1CN",
            parent=base,
            fontSize=14.2,
            leading=19,
            textColor=colors.HexColor("#0f172a"),
            spaceBefore=8,
            spaceAfter=6,
        ),
        "h2": ParagraphStyle(
            "H2CN",
            parent=base,
            fontSize=11.2,
            leading=16,
            textColor=colors.HexColor("#1f2937"),
            spaceBefore=5,
            spaceAfter=4,
        ),
        "quote": ParagraphStyle(
            "QuoteCN",
            parent=base,
            fontSize=9.2,
            leading=14,
            textColor=colors.HexColor("#7f1d1d"),
            backColor=colors.HexColor("#fff1f2"),
            borderColor=colors.HexColor("#fecdd3"),
            borderWidth=0.4,
            borderPadding=7,
            leftIndent=0,
            spaceAfter=6,
        ),
        "code": ParagraphStyle(
            "CodeCN",
            fontName="STHeiti",
            fontSize=8.2,
            leading=11.5,
            textColor=colors.HexColor("#111827"),
            backColor=colors.HexColor("#f8fafc"),
            borderColor=colors.HexColor("#cbd5e1"),
            borderWidth=0.35,
            borderPadding=6,
            spaceAfter=6,
        ),
        "note": ParagraphStyle(
            "NoteCN",
            parent=base,
            fontSize=7.6,
            leading=11.5,
            textColor=colors.HexColor("#6b7280"),
        ),
    }


def escape(text):
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def inline(text):
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = escape(text)
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`([^`]+)`", r"<font color='#334155'>\1</font>", text)
    return text


def is_table_block(lines, i):
    return (
        i + 1 < len(lines)
        and lines[i].lstrip().startswith("|")
        and lines[i + 1].lstrip().startswith("|")
        and re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", lines[i + 1])
    )


def parse_table(lines, i):
    block = []
    while i < len(lines) and lines[i].lstrip().startswith("|"):
        block.append(lines[i])
        i += 1
    rows = []
    for idx, line in enumerate(block):
        if idx == 1:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    return rows, i


def make_table(rows):
    if not rows:
        return Spacer(1, 0)
    cols = max(len(r) for r in rows)
    normalized = [r + [""] * (cols - len(r)) for r in rows]
    available = 164 * mm
    if cols == 2:
        widths = [45 * mm, available - 45 * mm]
    elif cols == 3:
        widths = [36 * mm, 67 * mm, available - 103 * mm]
    elif cols == 4:
        widths = [28 * mm, 42 * mm, 53 * mm, available - 123 * mm]
    else:
        widths = [available / cols] * cols

    cell_style = ParagraphStyle(
        "CellCN",
        fontName="STHeiti",
        fontSize=7.2,
        leading=9.8,
        textColor=colors.HexColor("#111827"),
    )
    tdata = [[Paragraph(inline(c), cell_style) for c in row] for row in normalized]
    tbl = Table(tdata, colWidths=widths, hAlign="LEFT", repeatRows=1)
    style = [
        ("FONTNAME", (0, 0), (-1, -1), "STHeiti"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d1d5db")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111827")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
    ]
    for r in range(1, len(normalized)):
        if r % 2 == 0:
            style.append(("BACKGROUND", (0, r), (-1, r), colors.HexColor("#f9fafb")))
    tbl.setStyle(TableStyle(style))
    return tbl


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("STHeiti", 8)
    canvas.setFillColor(colors.HexColor("#6b7280"))
    canvas.drawString(18 * mm, 12 * mm, "俞亮亮的交易体系0628版 | 项目总结合并版")
    canvas.drawRightString(192 * mm, 12 * mm, str(doc.page))
    canvas.restoreState()


def build():
    reg_font()
    st = make_styles()
    doc = SimpleDocTemplate(
        OUT,
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=15 * mm,
        bottomMargin=18 * mm,
    )

    lines = SRC.read_text(encoding="utf-8").splitlines()
    story = []
    in_code = False
    code_lines = []
    first_title = True
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()

        if line.startswith("```"):
            if not in_code:
                in_code = True
                code_lines = []
            else:
                in_code = False
                story.append(Preformatted("\n".join(code_lines), st["code"]))
            i += 1
            continue

        if in_code:
            code_lines.append(line)
            i += 1
            continue

        if not line.strip():
            i += 1
            continue

        if is_table_block(lines, i):
            rows, i = parse_table(lines, i)
            story.append(make_table(rows))
            story.append(Spacer(1, 4))
            continue

        if line.startswith("# "):
            if first_title:
                story.append(Spacer(1, 12 * mm))
                story.append(Paragraph(inline(line[2:]), st["title"]))
                first_title = False
            else:
                story.append(PageBreak())
                story.append(Paragraph(inline(line[2:]), st["title"]))
            i += 1
            continue

        if line.startswith("## "):
            story.append(Paragraph(inline(line[3:]), st["h1"]))
            i += 1
            continue

        if line.startswith("### "):
            story.append(Paragraph(inline(line[4:]), st["h2"]))
            i += 1
            continue

        if line.startswith("> "):
            story.append(Paragraph(inline(line[2:]), st["quote"]))
            i += 1
            continue

        if line.startswith("- "):
            story.append(Paragraph("• " + inline(line[2:]), st["base"]))
            i += 1
            continue

        if re.match(r"^\d+\. ", line):
            story.append(Paragraph(inline(line), st["base"]))
            i += 1
            continue

        if line.startswith("**") and line.endswith("**"):
            story.append(Paragraph(inline(line), st["quote"]))
            i += 1
            continue

        if first_title:
            story.append(Paragraph(inline(line), st["subtitle"]))
        else:
            story.append(Paragraph(inline(line), st["base"]))
        i += 1

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
