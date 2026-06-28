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
    KeepTogether,
)


OUT = "output/pdf/华工科技价值投资报告.pdf"
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"


def reg_font():
    pdfmetrics.registerFont(TTFont("STHeiti", FONT))


def styles():
    s = getSampleStyleSheet()
    base = ParagraphStyle(
        "BaseCN",
        parent=s["Normal"],
        fontName="STHeiti",
        fontSize=9.2,
        leading=14,
        textColor=colors.HexColor("#202124"),
        spaceAfter=5,
        alignment=TA_LEFT,
    )
    title = ParagraphStyle(
        "TitleCN",
        parent=base,
        fontSize=23,
        leading=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#111827"),
        spaceAfter=10,
    )
    subtitle = ParagraphStyle(
        "SubTitleCN",
        parent=base,
        fontSize=11,
        leading=17,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#4b5563"),
        spaceAfter=16,
    )
    h1 = ParagraphStyle(
        "H1CN",
        parent=base,
        fontSize=15,
        leading=20,
        textColor=colors.HexColor("#0f172a"),
        spaceBefore=8,
        spaceAfter=8,
    )
    h2 = ParagraphStyle(
        "H2CN",
        parent=base,
        fontSize=11.5,
        leading=17,
        textColor=colors.HexColor("#1f2937"),
        spaceBefore=5,
        spaceAfter=5,
    )
    note = ParagraphStyle(
        "NoteCN",
        parent=base,
        fontSize=8,
        leading=12,
        textColor=colors.HexColor("#6b7280"),
    )
    verdict = ParagraphStyle(
        "VerdictCN",
        parent=base,
        fontSize=10.5,
        leading=16,
        textColor=colors.HexColor("#7f1d1d"),
        backColor=colors.HexColor("#fff1f2"),
        borderColor=colors.HexColor("#fecdd3"),
        borderWidth=0.5,
        borderPadding=8,
        spaceAfter=8,
    )
    return dict(base=base, title=title, subtitle=subtitle, h1=h1, h2=h2, note=note, verdict=verdict)


def p(txt, st):
    return Paragraph(txt, st)


def bullet(items, st):
    out = []
    for item in items:
        out.append(p("• " + item, st))
    return out


def table(data, widths=None, header=True, font_size=8.2, leading=11):
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
    for r in range(1 if header else 0, len(data)):
        if r % 2 == 0:
            style.append(("BACKGROUND", (0, r), (-1, r), colors.HexColor("#f9fafb")))
    tbl.setStyle(TableStyle(style))
    return tbl


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("STHeiti", 8)
    canvas.setFillColor(colors.HexColor("#6b7280"))
    canvas.drawString(18 * mm, 12 * mm, "华工科技价值投资报告 | 资料来源：公司公告、巨潮资讯、腾讯行情")
    canvas.drawRightString(192 * mm, 12 * mm, f"{doc.page}")
    canvas.restoreState()


def build():
    reg_font()
    st = styles()
    doc = SimpleDocTemplate(
        OUT,
        pagesize=A4,
        rightMargin=16 * mm,
        leftMargin=16 * mm,
        topMargin=16 * mm,
        bottomMargin=18 * mm,
    )

    story = []
    story.append(Spacer(1, 18 * mm))
    story.append(p("华工科技（000988）价值投资报告", st["title"]))
    story.append(p("从 AI 光联接、智能传感与激光智能制造三条曲线评估长期价值", st["subtitle"]))
    story.append(p("生成日期：2026-06-28<br/>报告性质：个人投研复盘与价值评估，不构成投资建议", st["subtitle"]))
    story.append(Spacer(1, 8 * mm))
    story.append(p("核心结论", st["h1"]))
    story.append(
        p(
            "华工科技是兼具 AI 光模块、传感器和激光智能制造的平台型科技制造公司。2025 年收入和利润保持较快增长，"
            "经营现金流改善，研发投入维持高位，基本面质量较好。但以 2026-06-26 收盘价 160.94 元、市值约 1617 亿元估算，"
            "公司静态 PE 约 110 倍、PB 约 14.6 倍、PS 约 11.3 倍，估值已经显著透支未来成长。价值投资角度更适合“跟踪等待”，"
            "而不是在高估值区间无安全边际追买。",
            st["verdict"],
        )
    )
    story.append(
        table(
            [
                ["投资维度", "评价", "结论"],
                ["公司质地", "三大业务联接、感知、智能制造均具产业地位，研发投入强", "优秀"],
                ["成长性", "2025 年收入 +22.59%，归母净利 +20.48%，光电器件系列产品 +53.39%", "较强"],
                ["现金流", "经营现金流 12.21 亿元，同比 +66.83%，但低于归母净利", "改善但需观察"],
                ["估值", "市值约 1617 亿元，对应 2025 归母净利 PE 约 110 倍", "偏贵"],
                ["安全边际", "需要未来多年高增长兑现，容错率低", "不足"],
                ["价值策略", "好公司不等于好价格，适合等估值消化或业绩上修确认", "跟踪等待"],
            ],
            [30 * mm, 88 * mm, 46 * mm],
        )
    )
    story.append(PageBreak())

    story.append(p("一、公司业务画像", st["h1"]))
    story.extend(
        bullet(
            [
                "联接业务：围绕 AI 智能互联、6G/F6G、车载高速光通信等场景，提供光模块、光器件、铜缆联接和光电集成相关解决方案。2025 年光电器件系列产品收入 60.97 亿元，同比增长 53.39%。",
                "感知业务：围绕新能源汽车热管理、温度、压力、湿度、光、空气质量、气体传感等多维感知场景。2025 年敏感元器件收入 40.27 亿元，同比增长 9.78%。",
                "智能制造业务：提供激光加工装备、智能制造产线和行业综合解决方案。2025 年激光加工装备及智能制造产线收入 36.36 亿元，同比增长 4.13%。",
                "公司并非单一光模块公司，而是“光联接 + 传感器 + 激光装备”的科技制造平台。估值时不能只按光模块高弹性定价，也不能忽略传统装备业务的周期属性。",
            ],
            st["base"],
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(
        table(
            [
                ["业务/产品", "2025 收入", "收入占比", "同比", "毛利率", "价值判断"],
                ["光电器件系列产品", "60.97 亿元", "42.48%", "+53.39%", "13.26%", "AI 算力与高速互联主驱动，但毛利率偏低，需看高端产品放量改善"],
                ["敏感元器件", "40.27 亿元", "28.05%", "+9.78%", "24.46%", "汽车与智能感知底盘业务，稳定性较好"],
                ["激光加工装备及智能制造", "36.36 亿元", "25.33%", "+4.13%", "29.40%", "装备属性强，盈利质量较好但成长弹性低于光联接"],
                ["激光全息膜", "4.64 亿元", "3.23%", "+8.61%", "31.08%", "小体量现金流业务，非估值主线"],
            ],
            [33 * mm, 25 * mm, 20 * mm, 18 * mm, 20 * mm, 50 * mm],
            font_size=7.4,
            leading=10,
        )
    )

    story.append(p("二、2025 年财务质量", st["h1"]))
    story.append(
        table(
            [
                ["指标", "2025", "2024", "同比/变化", "解读"],
                ["营业收入", "143.55 亿元", "117.09 亿元", "+22.59%", "收入增长较快，主要受光电器件高增长带动"],
                ["归母净利润", "14.71 亿元", "12.21 亿元", "+20.48%", "利润增长略低于收入增长，但仍维持较好扩张"],
                ["扣非归母净利润", "11.87 亿元", "8.97 亿元", "+32.32%", "扣非增速高于归母，主业改善信号较好"],
                ["经营现金流", "12.21 亿元", "7.32 亿元", "+66.83%", "现金回款改善，但仍低于净利润"],
                ["ROE", "13.97%", "12.65%", "+1.32 pct", "盈利效率改善，但以当前 PB 看估值要求很高"],
                ["研发投入", "10.92 亿元", "9.93 亿元", "+9.96%", "研发强度 7.60%，科技制造属性明确"],
                ["应收账款", "43.63 亿元", "49.25 亿元", "下降", "回款改善是财务亮点"],
                ["存货", "35.81 亿元", "26.21 亿元", "上升", "需关注库存周转和订单兑现"],
            ],
            [30 * mm, 28 * mm, 28 * mm, 25 * mm, 55 * mm],
            font_size=7.4,
            leading=10,
        )
    )
    story.append(
        p(
            "价值投资视角下，2025 年财务数据有两点值得肯定：一是扣非利润和经营现金流改善，说明增长并非完全依赖非经常性收益；"
            "二是应收账款下降，对光模块和装备类企业尤为重要。但存货显著上升，叠加光电器件毛利率偏低，说明后续仍要观察订单质量和产品结构改善。",
            st["base"],
        )
    )

    story.append(PageBreak())
    story.append(p("三、长期价值逻辑", st["h1"]))
    story.append(p("1. AI 光联接：高成长，但也高竞争", st["h2"]))
    story.extend(
        bullet(
            [
                "公司披露两年内完成从 400G 到 1.6T、3.2T 的产品迭代，并提到面向 3.2T 的单波 400G 光引擎。",
                "AI 数据中心带来高速光模块和光电集成需求，华工科技的联接业务是估值上行的最大解释。",
                "但光电器件系列产品毛利率仅 13.26%，即使收入高速增长，也需要高端产品放量、客户结构优化和规模效应共同兑现，才能支撑高估值。",
            ],
            st["base"],
        )
    )
    story.append(p("2. 智能感知：中速增长的稳定底盘", st["h2"]))
    story.extend(
        bullet(
            [
                "感知业务覆盖新能源汽车热管理、温度、压力、湿度、光、电气体传感等场景，2025 年收入 40.27 亿元。",
                "该业务增速不如光联接，但毛利率和稳定性更好，适合作为平台型公司的利润底盘。",
                "如果汽车电子和 AIoT 感知层持续渗透，感知业务有望提供中长期复合增长。",
            ],
            st["base"],
        )
    )
    story.append(p("3. 激光智能制造：产业地位强，但估值弹性有限", st["h2"]))
    story.extend(
        bullet(
            [
                "激光装备业务收入 36.36 亿元，毛利率 29.40%，是公司利润质量较好的板块。",
                "装备业务受制造业资本开支周期影响，新能源汽车、船舶、半导体等应用能提供增量，但整体弹性弱于 AI 光联接。",
                "价值投资应把该业务看作“确定性资产”，而非短线估值弹性的主要来源。",
            ],
            st["base"],
        )
    )

    story.append(p("四、估值与安全边际", st["h1"]))
    story.append(
        table(
            [
                ["估值项", "计算口径", "结果", "解读"],
                ["市值", "2026-06-26 收盘价 160.94 元，总股本约 10.05 亿股", "约 1617 亿元", "市场已按高成长科技股定价"],
                ["PE", "市值 / 2025 归母净利 14.71 亿元", "约 110 倍", "对未来利润增长要求非常高"],
                ["扣非 PE", "市值 / 2025 扣非净利 11.87 亿元", "约 136 倍", "主业视角估值更高"],
                ["PB", "市值 / 2025 归母净资产 110.57 亿元", "约 14.6 倍", "制造业公司中明显偏高"],
                ["PS", "市值 / 2025 收入 143.55 亿元", "约 11.3 倍", "已充分反映 AI 光联接预期"],
                ["经营现金流收益率", "2025 经营现金流 12.21 亿元 / 市值", "约 0.75%", "现金流角度安全边际不足"],
            ],
            [28 * mm, 58 * mm, 26 * mm, 54 * mm],
            font_size=7.4,
            leading=10,
        )
    )
    story.append(Spacer(1, 8 * mm))
    story.append(
        p(
            "估值结论：如果把华工科技仅看作传统激光装备和传感器公司，当前估值明显过高；如果按 AI 光联接平台型龙头定价，"
            "当前估值也已经要求未来三年以上保持较高增长。价值投资的关键不是证明公司好，而是判断价格是否留有错误空间。"
            "以当前估值看，安全边际偏低。",
            st["verdict"],
        )
    )
    story.append(
        table(
            [
                ["情景", "假设", "合理估值框架", "投资含义"],
                ["保守情景", "利润增速回到 10%-15%，光模块价格竞争压制毛利率", "25-35 倍 PE", "当前价格缺乏吸引力"],
                ["中性情景", "利润维持 20%-25% 增长，光联接和感知平稳兑现", "40-55 倍 PE", "需要等待估值消化"],
                ["乐观情景", "1.6T/3.2T 产品持续放量，毛利率改善，净利率提升", "60-80 倍 PE", "仍需业绩显著上修支撑"],
                ["极乐观情景", "成为 AI 光联接核心龙头，收入和利润连续高增", "80 倍以上 PE", "当前价格才可能被解释，但容错率低"],
            ],
            [25 * mm, 62 * mm, 34 * mm, 45 * mm],
            font_size=7.4,
            leading=10,
        )
    )

    story.append(PageBreak())
    story.append(p("五、核心风险", st["h1"]))
    story.extend(
        bullet(
            [
                "估值风险：当前静态 PE 约 110 倍，若 AI 光模块预期降温，估值弹性可能明显回落。",
                "毛利率风险：光电器件系列产品收入增长最快，但毛利率仅 13.26%，需警惕高增长低盈利。",
                "客户与价格竞争风险：光模块行业技术迭代快，客户集中度和价格竞争可能影响利润率。",
                "存货风险：2025 年存货升至 35.81 亿元，若需求节奏放缓，可能带来减值或周转压力。",
                "资本开支周期风险：激光智能制造业务受新能源汽车、船舶、半导体等下游投资节奏影响。",
                "研发资本化风险：研发资本化率从 11.60% 提高至 18.96%，需持续观察后续摊销和项目兑现。",
            ],
            st["base"],
        )
    )

    story.append(p("六、价值投资操作框架", st["h1"]))
    story.append(
        table(
            [
                ["状态", "判断标准", "策略"],
                ["不买区", "估值高、股价强、业绩尚未明显上修", "只跟踪，不追买"],
                ["观察区", "股价回撤或横盘，估值开始消化，季度利润继续高增", "建立观察清单，等待确认"],
                ["试仓区", "业绩超预期，毛利率改善，估值回到可解释区间", "小仓跟踪，设置财报验证点"],
                ["加仓区", "AI 光联接订单和利润持续兑现，估值和成长匹配", "按业绩趋势分批加仓"],
                ["退出区", "光模块预期转弱、毛利率下滑、估值压缩", "降低仓位，回到观察"],
            ],
            [24 * mm, 80 * mm, 62 * mm],
            font_size=7.6,
            leading=10.5,
        )
    )
    story.append(Spacer(1, 8 * mm))
    story.append(
        p(
            "建议的价值投资结论：华工科技值得长期跟踪，但以 2026-06-26 价格看，更像“好公司、贵价格”。"
            "若没有持仓，价值投资者不宜因为 AI 光模块情绪追高；若已有持仓，应把它当高估值成长股管理，"
            "用季度业绩、毛利率和现金流来不断验证，而不是单纯按主题信仰持有。",
            st["verdict"],
        )
    )

    story.append(p("七、后续跟踪指标", st["h1"]))
    story.append(
        table(
            [
                ["指标", "跟踪重点", "为何重要"],
                ["光电器件收入", "是否继续高于 40%-50% 增长", "决定 AI 光联接估值能否维持"],
                ["光电器件毛利率", "是否从 13.26% 向上改善", "决定高收入是否转化为高利润"],
                ["扣非净利润", "是否持续快于收入增长", "判断主业质量"],
                ["经营现金流", "是否接近或超过净利润", "验证利润含金量"],
                ["存货和应收", "存货是否继续上升，应收是否反弹", "判断需求和回款质量"],
                ["研发投入", "1.6T/3.2T、硅光/LPO/CPO 进展", "决定长期技术壁垒"],
                ["估值位置", "PE/PB/PS 是否回到可承受区间", "决定安全边际"],
            ],
            [30 * mm, 70 * mm, 66 * mm],
            font_size=7.6,
            leading=10.5,
        )
    )

    story.append(p("八、资料来源", st["h1"]))
    story.extend(
        bullet(
            [
                "华工科技产业股份有限公司《2025 年年度报告》，巨潮资讯，公告编号 1225031509，披露日期 2026-03-26。",
                "腾讯行情接口，华工科技 000988，2026-06-26 收盘价、市值、成交等行情数据。",
                "本报告所有估值测算均为基于公开数据的静态估算，不代表未来收益承诺。",
            ],
            st["note"],
        )
    )

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
