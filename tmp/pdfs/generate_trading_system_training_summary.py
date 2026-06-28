from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak


OUT = "output/pdf/交易体系构建与心态管理培训总结.pdf"
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"


def reg_font():
    pdfmetrics.registerFont(TTFont("STHeiti", FONT))


def styles():
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
    canvas.drawString(18 * mm, 12 * mm, "交易体系构建与心态管理培训总结 | 发言人：Key")
    canvas.drawRightString(192 * mm, 12 * mm, str(doc.page))
    canvas.restoreState()


def build():
    reg_font()
    st = styles()
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
    story.append(p("交易体系构建与心态管理培训总结", st["title"]))
    story.append(p("会议主题：交易体系构建与心态管理培训<br/>发言人：Key<br/>整理日期：2026-06-28", st["subtitle"]))
    story.append(Spacer(1, 7 * mm))
    story.append(p("核心摘要", st["h1"]))
    story.append(
        p(
            "本次培训围绕止损、选股、仓位和心态四个核心问题展开。Key 的核心框架是：先判断市场所处周期和资金偏好的图形，"
            "再用 5 日线/10 日线建立技术止损标准，用分仓试错解决二选一和恐高问题，最后通过降低预期、屏蔽噪音和稳定复利来克服踏空心理。"
            "整套方法不是追求每一笔完美，而是让账户进入可复制、可纠错、可长期执行的正循环。",
            st["verdict"],
        )
    )
    story.append(
        table(
            [
                ["模块", "核心观点", "落地动作"],
                ["市场阶段", "当前偏第四阶段加速，AI 概念向传统化工、金属、材料等补涨扩散", "优先看强势图形和二波突破"],
                ["图形偏好", "资金偏好新高突破回踩、连阳；箱体震荡相对弱", "用图形强弱筛票"],
                ["止损纪律", "买入标准被破坏就离场，强势股看 5 日线，趋势股看 10 日线", "提前写止损条件"],
                ["选股仓位", "承认概率，无法二选一时分仓试错", "A/B 各半仓，后续总结强弱共性"],
                ["心态管理", "降低预期，接受卖飞，屏蔽群内噪音", "追求月度稳定盈利"],
            ],
            [27 * mm, 82 * mm, 55 * mm],
        )
    )
    story.append(PageBreak())

    story.append(p("一、市场周期与图形偏好", st["h1"]))
    story.append(p("1. 市场周期阶段", st["h2"]))
    story.extend(
        bullets(
            [
                "Key 将当前行情定位为第四阶段的偏加速期。此前经历第一阶段 2024 年 9 月、第二阶段中继续创、第三阶段主升浪，第三阶段主线包括机器人、商业航天等新质生产力。",
                "当前第四阶段表现为传统行业蹭上 AI 逻辑后的补涨，例如 AI 金属、AI 材料、传统化工股等。",
                "未来展望是：本轮调整结束后，市场可能进入第五阶段加速期，因此当下的重点不是盲目悲观，而是识别下一轮资金会选择什么强势结构。",
            ],
            st["base"],
        )
    )
    story.append(p("2. 资金图形偏好", st["h2"]))
    story.extend(
        bullets(
            [
                "当前市场资金偏好“新高突破回踩”和“连阳”形态，这类股票通常代表资金态度更强。",
                "强弱对比标准：连阳、新高、二波突破偏强；箱体震荡、反复横盘偏弱。",
                "近期较好的个股，多是前一波强势股调整后的二波突破，而不是低位长期横盘股突然启动。",
            ],
            st["base"],
        )
    )
    story.append(
        p(
            "复盘使用方式：每天把候选股先按图形分层。第一层是新高突破回踩和连阳，第二层是二波突破，第三层才是箱体震荡。"
            "如果市场处于加速阶段，弱图形即使逻辑不错，也要降低预期。",
            st["box"],
        )
    )

    story.append(p("二、止损策略与交易纪律", st["h1"]))
    story.append(p("1. 止损的底层逻辑", st["h2"]))
    story.extend(
        bullets(
            [
                "买入股票要基于标准，例如逻辑、事件预期、图形、资金强度。只要买入标准被破坏，就应当执行离场。",
                "Key 用情感关系作类比：买入如同开始一段关系，关系能持续的前提是原先看中的标准仍然存在；标准消失，就不要靠幻想续命。",
                "如果基于事件节点买入，例如 SpaceX 上市等预期，节点临近前要观察板块强度。若节点前板块弱，说明逻辑没有被市场认可，应提前处理。",
            ],
            st["base"],
        )
    )
    story.append(p("2. 技术止损标准", st["h2"]))
    story.append(
        table(
            [
                ["类型", "生命线", "处理方式"],
                ["强势股", "5 日线", "盘中有效跌破且无反包迹象，考虑减仓或离场"],
                ["趋势股", "10 日线", "跌破 10 日线说明调整周期可能延长，需要警惕"],
                ["事件驱动股", "事件前板块强度", "节点前不强，说明市场不认可，应提前降低仓位"],
                ["逻辑股", "逻辑是否证伪", "逻辑破坏比技术破位更优先，应快速修正"],
            ],
            [30 * mm, 45 * mm, 89 * mm],
        )
    )
    story.append(
        p(
            "交易纪律模板：买入前写清楚“我为什么买、什么情况说明我错了、错了以后减多少”。"
            "止损不是亏钱后的临时反应，而是买入计划的一部分。",
            st["box"],
        )
    )

    story.append(PageBreak())
    story.append(p("三、选股策略与仓位管理", st["h1"]))
    story.append(p("1. 解决二选一总选错", st["h2"]))
    story.extend(
        bullets(
            [
                "当无法判断 A 与 B 谁更强时，不要强行 All in 单选，可以用分仓试错法：两只各买一半。",
                "通过后续走势观察强弱差异，逐步总结强势股共性，再在下一次交易中提高强势图形的仓位比例。",
                "交易要有概率思维。单次选错不是能力全盘失败，关键是降低单次错误对账户和心态的冲击。",
            ],
            st["base"],
        )
    )
    story.append(p("2. 克服恐高心理", st["h2"]))
    story.extend(
        bullets(
            [
                "高位股不敢买，核心不是不知道逻辑，而是身体没有适应波动。可以从极小仓位开始试错。",
                "渐进式加仓路径：2000 元试错，能稳定赚钱后提高到 5000、1 万、5 万，逐步训练对强势股波动的承受力。",
                "恐高不靠喊口号解决，而靠低成本实践，让自己真实经历“高位强者还能继续强”的过程。",
            ],
            st["base"],
        )
    )
    story.append(
        table(
            [
                ["问题", "错误反应", "正确机制"],
                ["二选一选错", "重仓单押，错了自责", "A/B 分仓试错，复盘强弱共性"],
                ["恐高", "只敢买低位弱股", "小仓买强势高位股训练波动承受"],
                ["亏损扩大", "临盘犹豫不止损", "买入前写好 5 日线/10 日线或逻辑止损"],
                ["心态崩溃", "仓位超过承受力", "降低仓位直到能正常执行"],
            ],
            [30 * mm, 58 * mm, 76 * mm],
        )
    )

    story.append(p("四、心态管理与交易误区", st["h1"]))
    story.append(p("1. 降低预期，接受卖飞", st["h2"]))
    story.extend(
        bullets(
            [
                "多数交易者属于 75 分选手，目标可以是年化 50%，不要强求自己做到 90 分甚至翻倍选手的极致卖点。",
                "能红盘卖出已经超过多数投资者，卖飞不是失败，很多时候是能保住利润的福报。",
                "不要为了追求最高点卖出，把原本赚钱的交易变成亏损离场。",
            ],
            st["base"],
        )
    )
    story.append(p("2. 仓位必须匹配心理承受力", st["h2"]))
    story.extend(
        bullets(
            [
                "因恐慌在开盘 -2% 割肉，往往不是股票问题，而是心理承受力和仓位不匹配。",
                "如果一只票的正常波动会让自己无法睡觉、无法执行计划，说明仓位过大。",
                "心态问题不能只靠“想通”，更有效的是通过降低仓位，让自己恢复执行力。",
            ],
            st["base"],
        )
    )
    story.append(p("3. 处理踏空心理", st["h2"]))
    story.extend(
        bullets(
            [
                "踏空感来自幸存者偏差。群里展示的往往是赚钱案例，而不是所有人的真实收益分布。",
                "减少关注群内炫耀信息，避免因为别人赚钱而打乱自己的交易节奏。",
                "应对踏空的最好方法，是保证每月持续盈利，而不是追逐单日暴利。",
            ],
            st["base"],
        )
    )

    story.append(PageBreak())
    story.append(p("五、盘中题材挖掘与量化应对", st["h1"]))
    story.append(p("1. 突发题材强度判断", st["h2"]))
    story.extend(
        bullets(
            [
                "量化时代，封单量容易失真。单纯看 9:15 的封单意义不大，因为很多是虚假挂单。",
                "真正强度要看 9:20 和 9:24:50 附近的封单变化，尤其是撤单后的真实承接。",
                "突发题材如果出现三个以上一字板，并且包含 20cm 一字板，通常说明题材强度较高，次日可能有高溢价。",
            ],
            st["base"],
        )
    )
    story.append(p("2. 盘中挖掘工具与流程", st["h2"]))
    story.extend(
        bullets(
            [
                "可以使用 AI 工具，例如 DeepSeek，快速梳理产业链和关联标的，提高题材挖掘效率。",
                "对午间或盘中突发题材，例如电感等，要结合市场情绪、板块轮动、涨停结构和核心标的强度即时判断。",
                "盘中题材没有固定模式，重点是建立观察顺序：消息强度、涨停数量、20cm 表现、核心股封单、板块扩散、次日溢价。",
            ],
            st["base"],
        )
    )
    story.append(
        table(
            [
                ["时间点/信号", "观察重点", "意义"],
                ["9:15", "初始封单", "参考价值低，量化虚假挂单较多"],
                ["9:20", "撤单后封单", "初步判断真实强度"],
                ["9:24:50", "临近开盘封单", "更接近真实资金态度"],
                ["三个以上一字板", "是否形成板块强度", "题材可能具备延续性"],
                ["20cm 一字板", "是否有创业板/科创板核心强度", "通常代表更高溢价预期"],
            ],
            [32 * mm, 66 * mm, 66 * mm],
        )
    )

    story.append(p("六、可执行交易清单", st["h1"]))
    story.append(
        table(
            [
                ["环节", "检查问题", "执行标准"],
                ["买入前", "我买的是逻辑、图形、节点，还是情绪？", "写出买入理由和证伪条件"],
                ["持仓中", "是否跌破对应生命线？", "强势股看 5 日线，趋势股看 10 日线"],
                ["选股时", "A/B 无法判断谁强怎么办？", "分仓试错，不单押"],
                ["恐高时", "是否因为高位而错过强者？", "用小仓位训练高位强股波动"],
                ["卖出时", "是否为了极致卖点把利润拖没？", "红盘卖出可以接受，卖飞不等于失败"],
                ["踏空时", "是否被别人赚钱影响节奏？", "屏蔽噪音，回到月度稳定盈利目标"],
                ["复盘时", "今天亏损来自模式问题还是执行问题？", "分开记录，不混在一起自责"],
            ],
            [28 * mm, 70 * mm, 66 * mm],
            font_size=7.5,
            leading=10.5,
        )
    )
    story.append(Spacer(1, 8 * mm))
    story.append(
        p(
            "最终落点：交易体系不是寻找一个永远正确的答案，而是形成一套能让自己在不确定市场中反复试错、及时纠错、稳定执行的机制。"
            "少一点完美主义，多一点标准化；少一点群体比较，多一点账户复利。",
            st["verdict"],
        )
    )
    story.append(p("资料来源：用户提供的腾讯会议纪要文本。", st["note"]))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
