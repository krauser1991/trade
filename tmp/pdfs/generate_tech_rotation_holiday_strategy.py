from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak


OUT = "output/pdf/科技板块轮动与节前策略研讨会总结.pdf"
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"


def reg_font():
    pdfmetrics.registerFont(TTFont("STHeiti", FONT))


def make_styles():
    sample = getSampleStyleSheet()
    base = ParagraphStyle(
        "BaseCN",
        parent=sample["Normal"],
        fontName="STHeiti",
        fontSize=9.2,
        leading=14,
        textColor=colors.HexColor("#202124"),
        alignment=TA_LEFT,
        spaceAfter=5,
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
            spaceAfter=9,
        ),
        "subtitle": ParagraphStyle(
            "SubtitleCN",
            parent=base,
            fontSize=10.5,
            leading=16,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4b5563"),
            spaceAfter=13,
        ),
        "h1": ParagraphStyle(
            "H1CN",
            parent=base,
            fontSize=14.5,
            leading=20,
            textColor=colors.HexColor("#0f172a"),
            spaceBefore=8,
            spaceAfter=7,
        ),
        "h2": ParagraphStyle(
            "H2CN",
            parent=base,
            fontSize=11.2,
            leading=16,
            textColor=colors.HexColor("#1f2937"),
            spaceBefore=4,
            spaceAfter=5,
        ),
        "note": ParagraphStyle(
            "NoteCN",
            parent=base,
            fontSize=8,
            leading=12,
            textColor=colors.HexColor("#6b7280"),
        ),
        "verdict": ParagraphStyle(
            "VerdictCN",
            parent=base,
            fontSize=10.2,
            leading=16,
            textColor=colors.HexColor("#7f1d1d"),
            backColor=colors.HexColor("#fff1f2"),
            borderColor=colors.HexColor("#fecdd3"),
            borderWidth=0.5,
            borderPadding=8,
            spaceAfter=8,
        ),
        "box": ParagraphStyle(
            "BoxCN",
            parent=base,
            fontSize=9.2,
            leading=14,
            textColor=colors.HexColor("#0f172a"),
            backColor=colors.HexColor("#f8fafc"),
            borderColor=colors.HexColor("#cbd5e1"),
            borderWidth=0.4,
            borderPadding=7,
            spaceAfter=7,
        ),
    }


def p(text, style):
    return Paragraph(text, style)


def bullets(items, style):
    return [p("• " + item, style) for item in items]


def table(data, widths, header=True, font_size=7.6, leading=10.5):
    cell_style = ParagraphStyle(
        "Cell",
        fontName="STHeiti",
        fontSize=font_size,
        leading=leading,
        textColor=colors.HexColor("#111827"),
    )
    tdata = [[Paragraph(str(x), cell_style) for x in row] for row in data]
    tbl = Table(tdata, colWidths=widths, hAlign="LEFT", repeatRows=1 if header else 0)
    style = [
        ("FONTNAME", (0, 0), (-1, -1), "STHeiti"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#d1d5db")),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]
    if header:
        style += [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#111827")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ]
    for row in range(1 if header else 0, len(data)):
        if row % 2 == 0:
            style.append(("BACKGROUND", (0, row), (-1, row), colors.HexColor("#f9fafb")))
    tbl.setStyle(TableStyle(style))
    return tbl


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("STHeiti", 8)
    canvas.setFillColor(colors.HexColor("#6b7280"))
    canvas.drawString(18 * mm, 12 * mm, "科技板块轮动与节前策略研讨会总结 | 发言人：Key")
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
        topMargin=16 * mm,
        bottomMargin=18 * mm,
    )

    story = []
    story.append(Spacer(1, 16 * mm))
    story.append(p("科技板块轮动与节前策略研讨会总结", st["title"]))
    story.append(p("会议主题：科技板块轮动与节前策略研讨会<br/>发言人：Key<br/>整理日期：2026-06-28", st["subtitle"]))
    story.append(Spacer(1, 7 * mm))
    story.append(p("核心摘要", st["h1"]))
    story.append(
        p(
            "本次会议的核心判断是：当前科技行情不是单一 CPO 主线，而是算力、存储、半导体设备三大业绩要素轮流抬高水位。"
            "在美联储决议落地和节前效应共同影响下，交易重点不是满仓赌方向，而是用仓位控制降低卖飞和情绪化交易概率。"
            "策略上，保持对算力、存储、半导体设备的信念，优先选择新高附近或突破形态，节前仓位倾向控制在四成左右，并根据美股与次日 A 股承接动态调整。",
            st["verdict"],
        )
    )
    story.append(
        table(
            [
                ["模块", "核心观点", "操作抓手"],
                ["科技轮动", "算力、存储、半导体设备轮流抬高水位，不是 CPO 单线行情", "围绕三大方向做轮动观察"],
                ["资金承接", "午后承接好于去年 618，存储和半导体承接资金", "看核心板块是否持续接力"],
                ["外围变量", "美联储不加息预期已抢跑，落地后可能利好兑现", "看美股、日韩和 A 股高开承接"],
                ["仓位纪律", "七成以上仓位容易恐慌卖飞，五成以下更利于持股", "节前倾向四成左右"],
                ["选股偏好", "新高附近、突破形态更有确定性", "关注长电科技、富创精密等风向标"],
            ],
            [27 * mm, 83 * mm, 54 * mm],
        )
    )

    story.append(PageBreak())
    story.append(p("一、核心板块轮动与市场逻辑", st["h1"]))
    story.append(p("1. 科技轮动与资金流向", st["h2"]))
    story.extend(
        bullets(
            [
                "当前科技板块呈现轮动特征，并非仅靠光模块或 CPO 单独带动，而是由算力、存储、半导体设备三大核心要素轮流发力。",
                "存储板块表现强势，代表标的包括百维存储、香农芯创；PCB 板块虽有异动，但强度不足，需要观察核心标的带动效应。",
                "午后市场承接力度较强，不同于去年 618 的午后跳水，说明当前市场状态更健康，存储和半导体成为资金承接方向。",
            ],
            st["base"],
        )
    )
    story.append(p("2. 指数支撑与外围影响", st["h2"]))
    story.extend(
        bullets(
            [
                "科技板块，尤其是光模块方向的持续走强，仍然依赖指数环境支持。如果指数转弱，强势板块也容易出现波动。",
                "市场已提前抢跑美联储不加息预期，决议落地后存在利好兑现风险，需要观察美股、日韩市场以及 A 股高开后的承接。",
                "监管影响在强势市场中通常不会破坏逻辑票，但如果市场走弱或跌破均线，监管影响会被放大。",
            ],
            st["base"],
        )
    )
    story.append(
        p(
            "复盘重点：科技行情是否健康，不只看某一只光模块是否上涨，而要看存储、半导体设备、算力链能否轮流承接。"
            "如果只有单点强、板块不扩散，节前就要降低进攻仓位。",
            st["box"],
        )
    )

    story.append(p("二、交易策略与持仓管理", st["h1"]))
    story.append(p("1. 仓位控制与卖飞应对", st["h2"]))
    story.extend(
        bullets(
            [
                "账户整体仓位超过七成时，容易因为盘中波动而恐慌卖飞核心持仓，例如金志达这类趋势核心。",
                "建议将仓位控制在五成以下，以降低卖飞概率；节前更倾向控制在四成左右。",
                "必须建立对算力、存储、半导体设备三大方向的信念，否则容易在盘中震荡中卖掉底仓，随后两边踏空。",
                "趋势股常见节奏是强两天、弱两天，不需要每天大涨。关键是趋势没有破坏时，给它波动空间。",
            ],
            st["base"],
        )
    )
    story.append(
        table(
            [
                ["仓位状态", "典型心理", "建议动作"],
                ["七成以上", "容易恐慌，看到回撤就卖飞", "主动降仓，保留核心底仓"],
                ["五成左右", "攻守相对平衡", "适合趋势持有和小幅轮动"],
                ["四成左右", "节前更舒适，抗外围波动", "作为过节参考仓位"],
                ["两成以下", "容易踏空焦虑", "只适合市场风险显著放大时"],
            ],
            [31 * mm, 63 * mm, 70 * mm],
        )
    )
    story.append(p("2. 节前操作与选股思路", st["h2"]))
    story.extend(
        bullets(
            [
                "节前仓位规划以四成左右为基准，但要根据明日市场状态灵活调整。如果高开低走，应防利好兑现；如果承接后再次走强，可以保留核心仓位。",
                "选股优先选择新高附近或突破形态，这类图形在震荡市中更有确定性，例如长电科技、富创精密等。",
                "承认当前科技股有泡沫化炒作特征，但泡沫阶段并不等于马上结束。要做的是跟随趋势，同时提高利润垫，而不是盲目回避。",
            ],
            st["base"],
        )
    )

    story.append(PageBreak())
    story.append(p("三、重点个股与细分领域解析", st["h1"]))
    story.append(
        table(
            [
                ["方向", "核心标的/观察标的", "会议观点", "交易含义"],
                ["封测", "长电科技", "被视为本轮行情灵魂", "作为半导体强度风向标"],
                ["半导体设备", "富创精密、盛美上海、中微公司", "设备股表现强势", "观察突破和新高结构"],
                ["存储", "百维存储、香农芯创", "走势强劲，资金承接明显", "关注是否继续二次上攻"],
                ["算力/光模块", "中际旭创、新易盛", "CPO/NPO/LPO 轮动频繁", "核心票用于判断算力链水位"],
                ["硅光", "硅光方向弹性机会", "光模块细分弹性方向", "适合小仓跟踪弹性"],
                ["PCB", "盛宏股份等核心带动", "板块强度相对不足，更多偏情绪博弈", "需要核心票确认后再做扩散"],
                ["材料", "PCB 上游材料涨价逻辑", "涨价可形成补涨线索", "关注强度能否超过 PCB 主板块"],
                ["趋势股", "利通电子", "接受强两天弱两天节奏", "趋势未坏不因单日弱轻易卖"],
            ],
            [24 * mm, 38 * mm, 55 * mm, 47 * mm],
            font_size=7.1,
            leading=9.8,
        )
    )
    story.append(Spacer(1, 5 * mm))
    story.append(p("四、美联储决议后的节前策略", st["h1"]))
    story.append(
        table(
            [
                ["情景", "观察信号", "策略"],
                ["利好兑现", "美股冲高回落，日韩偏弱，A 股高开低走", "降低进攻仓位，保留核心底仓，减少追高"],
                ["二次走强", "美股科技强，日韩承接好，A 股高开后不回落", "维持四到五成，围绕核心方向轮动"],
                ["指数转弱", "指数跌破关键均线，监管影响被放大", "压缩仓位，优先处理弱图形和跟风票"],
                ["板块轮动健康", "存储、设备、算力交替走强", "持有核心，不因单日弱卖飞"],
                ["单点抱团", "只有少数龙头强，扩散不足", "提高谨慎度，避免后排补涨追高"],
            ],
            [27 * mm, 76 * mm, 61 * mm],
        )
    )
    story.append(Spacer(1, 8 * mm))
    story.append(
        p(
            "节前操作要点：不要把“看好科技”直接等同于高仓位。真正的策略是：看好方向，控制仓位，保留核心，避免后排追涨，"
            "用利润垫对抗波动，用美联储落地后的全球市场反馈修正次日计划。",
            st["box"],
        )
    )

    story.append(PageBreak())
    story.append(p("五、盘后复盘与次日交易清单", st["h1"]))
    story.append(
        table(
            [
                ["复盘项", "问题", "处理标准"],
                ["美联储", "决议落地后美股科技是冲高回落还是继续走强？", "决定次日科技仓位是否进攻"],
                ["日韩市场", "日韩是否承接美股方向？", "作为 A 股开盘情绪参考"],
                ["A 股指数", "高开后能否承接？是否跌破均线？", "决定监管和兑现风险是否放大"],
                ["三大方向", "算力、存储、半导体设备是否轮动？", "轮动健康则持核心，失衡则降后排"],
                ["核心标的", "长电科技、富创精密、百维存储等是否维持强势？", "作为板块风向标"],
                ["仓位", "当前是否超过五成？是否影响心态？", "节前倾向四成左右"],
                ["卖飞风险", "是否因为仓位过重导致拿不住？", "降低总仓，保留底仓"],
                ["后排风险", "是否追了弱图形或补涨后排？", "只做强图形，不做纯情绪追涨"],
            ],
            [27 * mm, 75 * mm, 62 * mm],
            font_size=7.4,
            leading=10.4,
        )
    )
    story.append(Spacer(1, 5 * mm))
    story.append(p("六、待办事项", st["h1"]))
    story.extend(
        bullets(
            [
                "晚上复盘美联储决议落地后的美股表现，重点看纳指、AI 算力链、半导体设备和存储相关标的。",
                "观察日韩股市次日开盘表现，判断外围情绪是否延续。",
                "明日盘中重点看 A 股是否高开低走，若高开后承接差，主动降低节前仓位。",
                "若科技主线二次走强，优先围绕算力、存储、半导体设备核心票做持有和轮动，不追弱后排。",
            ],
            st["base"],
        )
    )
    story.append(
        p(
            "最终落点：科技行情可以继续看多，但节前交易不能只靠信仰。正确做法是用四成左右仓位保留参与感，"
            "用核心标的判断板块强弱，用外围落地后的承接确认方向，用仓位控制解决卖飞和踏空两种心态问题。",
            st["verdict"],
        )
    )
    story.append(p("资料来源：用户提供的腾讯会议纪要文本。", st["note"]))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
