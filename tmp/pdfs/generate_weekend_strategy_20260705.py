from pathlib import Path
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


ROOT = Path("/Users/krauser/Documents/Obsidian Vault/trade")
FONT_PATH = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

DOCS = [
    (
        ROOT / "interviews/2026-07-05-拆哥AI硬件业绩解读与市场博弈策略分享.md",
        ROOT / "output/pdf/2026-07-05-拆哥AI硬件业绩解读与市场博弈策略分享.pdf",
    ),
    (
        ROOT / "strategies/2026-07-05-周末消息面与2026-07-06周一交易策略.md",
        ROOT / "output/pdf/2026-07-05-周末消息面与2026-07-06周一交易策略.pdf",
    ),
]


def clean_inline(text: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    text = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"`([^`]+)`", r"<font name='CodeFont'>\1</font>", text)
    return text


def split_table_line(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_separator(line: str) -> bool:
    cells = split_table_line(line)
    return bool(cells) and all(re.match(r"^:?-{3,}:?$", c) for c in cells)


def add_page_number(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("CN", 8)
    canvas.setFillColor(colors.HexColor("#666666"))
    canvas.drawRightString(A4[0] - 16 * mm, 10 * mm, f"第 {doc.page} 页")
    canvas.restoreState()


def build_styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="TitleCN", fontName="CN", fontSize=20, leading=27,
        alignment=TA_CENTER, textColor=colors.HexColor("#172033"),
        spaceAfter=13,
    ))
    styles.add(ParagraphStyle(
        name="H2CN", fontName="CN", fontSize=14.2, leading=20,
        textColor=colors.HexColor("#0f3f6f"), spaceBefore=9, spaceAfter=6,
    ))
    styles.add(ParagraphStyle(
        name="H3CN", fontName="CN", fontSize=11.8, leading=16.5,
        textColor=colors.HexColor("#17324d"), spaceBefore=7, spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="BodyCN", fontName="CN", fontSize=9.0, leading=13.6,
        alignment=TA_LEFT, textColor=colors.HexColor("#222222"),
        spaceAfter=4.5,
    ))
    styles.add(ParagraphStyle(
        name="BulletCN", fontName="CN", fontSize=9.0, leading=13.6,
        leftIndent=12, firstLineIndent=-8, spaceAfter=3.8,
    ))
    styles.add(ParagraphStyle(
        name="CodeCN", fontName="CodeFont", fontSize=8.3, leading=11.8,
        leftIndent=8, rightIndent=8, textColor=colors.HexColor("#263238"),
        backColor=colors.HexColor("#f4f6f8"), borderPadding=6, spaceAfter=7,
    ))
    styles.add(ParagraphStyle(
        name="SmallCN", fontName="CN", fontSize=7.5, leading=10.1,
        textColor=colors.HexColor("#333333"),
    ))
    return styles


def build_pdf(md_path: Path, pdf_path: Path) -> None:
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(pdf_path),
        pagesize=A4,
        rightMargin=14 * mm,
        leftMargin=14 * mm,
        topMargin=15 * mm,
        bottomMargin=14 * mm,
    )
    styles = build_styles()
    story = []
    lines = md_path.read_text(encoding="utf-8").splitlines()
    in_code = False
    code_lines = []
    table_lines = []

    def flush_code() -> None:
        nonlocal code_lines
        if code_lines:
            story.append(Paragraph("<br/>".join(clean_inline(x) for x in code_lines), styles["CodeCN"]))
            code_lines = []

    def flush_table() -> None:
        nonlocal table_lines
        if not table_lines:
            return
        raw = [split_table_line(x) for x in table_lines if not is_separator(x)]
        table_lines = []
        if not raw:
            return
        col_count = max(len(r) for r in raw)
        normalized = [r + [""] * (col_count - len(r)) for r in raw]
        data = [[Paragraph(clean_inline(c), styles["SmallCN"]) for c in row] for row in normalized]
        width = doc.width
        if col_count == 4:
            col_widths = [width * 0.18, width * 0.29, width * 0.25, width * 0.28]
        elif col_count == 3:
            col_widths = [width * 0.22, width * 0.37, width * 0.41]
        elif col_count == 2:
            col_widths = [width * 0.31, width * 0.69]
        else:
            col_widths = [width / col_count] * col_count
        tbl = Table(data, colWidths=col_widths, repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eaf2fb")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#163a5f")),
            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#d6dee8")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 4),
            ("RIGHTPADDING", (0, 0), (-1, -1), 4),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))
        story.append(tbl)
        story.append(Spacer(1, 6))

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code:
                flush_code()
                in_code = False
            else:
                flush_table()
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if stripped.startswith("|") and stripped.endswith("|"):
            table_lines.append(line)
            continue
        flush_table()
        if not stripped:
            story.append(Spacer(1, 3))
        elif stripped.startswith("# "):
            story.append(Paragraph(clean_inline(stripped[2:]), styles["TitleCN"]))
        elif stripped.startswith("## "):
            story.append(Paragraph(clean_inline(stripped[3:]), styles["H2CN"]))
        elif stripped.startswith("### "):
            story.append(Paragraph(clean_inline(stripped[4:]), styles["H3CN"]))
        elif stripped.startswith("- "):
            story.append(Paragraph("• " + clean_inline(stripped[2:]), styles["BulletCN"]))
        elif re.match(r"^\d+\. ", stripped):
            story.append(Paragraph(clean_inline(stripped), styles["BulletCN"]))
        else:
            story.append(Paragraph(clean_inline(stripped), styles["BodyCN"]))

    flush_table()
    flush_code()
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)


if __name__ == "__main__":
    pdfmetrics.registerFont(TTFont("CN", FONT_PATH))
    pdfmetrics.registerFont(TTFont("CodeFont", FONT_PATH))
    for source_md, target_pdf in DOCS:
        build_pdf(source_md, target_pdf)
        print(target_pdf)
