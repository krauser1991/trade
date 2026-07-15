from pathlib import Path
import re

import pdfplumber

ROOT = Path("/Users/krauser/Documents/Obsidian Vault/trade")
READER = ROOT / "reader"
OUT = ROOT / "tmp/pdfs/robot_reader_digest.txt"

keywords = [
    "机器人", "人形", "具身智能", "执行器", "电机", "减速器", "丝杠",
    "灵巧手", "传感器", "激光雷达", "量产", "商业化", "特斯拉",
    "Optimus", "供应链", "工艺", "冷锻", "散热", "财报",
]

files = [
    p for p in sorted(READER.glob("*.pdf"))
    if any(k in p.name for k in ["机器人", "人形", "具身智能", "冷锻", "激光雷达"])
]

def compact(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "")
    return text.strip()

with OUT.open("w", encoding="utf-8") as out:
    for path in files:
        out.write("=" * 100 + "\n")
        out.write(f"FILE: {path.name}\n")
        try:
            with pdfplumber.open(str(path)) as pdf:
                out.write(f"PAGES: {len(pdf.pages)}\n")
                full = []
                for i, page in enumerate(pdf.pages, start=1):
                    text = compact(page.extract_text() or "")
                    if text:
                        full.append((i, text))
                head = " ".join(t for _, t in full[:3])[:4500]
                out.write("\n[HEAD]\n")
                out.write(head + "\n")
                out.write("\n[KEYWORD SNIPPETS]\n")
                seen = 0
                for page_no, text in full:
                    for kw in keywords:
                        idx = text.find(kw)
                        if idx >= 0:
                            start = max(0, idx - 180)
                            end = min(len(text), idx + 380)
                            out.write(f"- p{page_no} kw={kw}: {text[start:end]}\n")
                            seen += 1
                            break
                    if seen >= 18:
                        break
                out.write("\n")
        except Exception as exc:
            out.write(f"ERROR: {exc}\n\n")

print(OUT)
