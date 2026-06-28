from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak


OUT = "output/pdf/大族激光价值投资报告.pdf"
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
            fontSize=23,
            leading=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#111827"),
            spaceAfter=10,
        ),
        "subtitle": ParagraphStyle(
            "SubtitleCN",
            parent=base,
            fontSize=11,
            leading=17,
            alignment=TA_CENTER,
            textColor=colors.HexColor("#4b5563"),
            spaceAfter=15,
        ),
        "h1": ParagraphStyle(
            "H1CN",
            parent=base,
            fontSize=15,
            leading=20,
            textColor=colors.HexColor("#0f172a"),
            spaceBefore=8,
            spaceAfter=8,
        ),
        "h2": ParagraphStyle(
            "H2CN",
            parent=base,
            fontSize=11.5,
            leading=17,
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
            fontSize=10.4,
            leading=16,
            textColor=colors.HexColor("#7f1d1d"),
            backColor=colors.HexColor("#fff1f2"),
            borderColor=colors.HexColor("#fecdd3"),
            borderWidth=0.5,
            borderPadding=8,
            spaceAfter=8,
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
    canvas.drawString(18 * mm, 12 * mm, "大族激光价值投资报告 | 资料来源：公司公告、巨潮资讯、腾讯行情")
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

    story.append(Spacer(1, 18 * mm))
    story.append(p("大族激光（002008）价值投资报告", st["title"]))
    story.append(p("从 AI PCB 设备、激光装备、锂电设备与半导体设备评估长期价值", st["subtitle"]))
    story.append(p("生成日期：2026-06-28<br/>报告性质：个人投研复盘与价值评估，不构成投资建议", st["subtitle"]))
    story.append(Spacer(1, 8 * mm))
    story.append(p("核心结论", st["h1"]))
    story.append(
        p(
            "大族激光是国内智能制造装备龙头，业务覆盖 PCB 智能制造装备、通用激光装备、消费电子、新能源、半导体及泛半导体设备。"
            "2025 年收入恢复增长，扣非净利润显著修复，经营现金流改善，AI 算力 PCB 设备成为最核心的增长曲线。"
            "但以 2026-06-26 收盘价 151.27 元、总市值约 1557 亿元估算，公司静态 PE 约 131 倍、扣非 PE 约 192 倍、"
            "PB 约 9.0 倍、PS 约 8.3 倍，估值已远高于传统装备公司的价值区间。价值投资角度适合长期跟踪，"
            "但当前更像“好资产、贵价格”，需要业绩连续超预期和估值消化来提供安全边际。",
            st["verdict"],
        )
    )
    story.append(
        table(
            [
                ["投资维度", "评价", "结论"],
                ["公司质地", "智能制造装备龙头，产品线覆盖 PCB、激光、锂电、半导体、消费电子", "优秀"],
                ["成长性", "2025 收入 +27.00%，PCB 智能制造装备收入 +72.68%", "较强"],
                ["盈利质量", "扣非净利 +82.28%，经营现金流 +30.48%，但归母净利同比 -29.77%", "修复中"],
                ["估值", "总市值约 1557 亿元，对应 2025 归母净利 PE 约 131 倍", "明显偏贵"],
                ["安全边际", "当前价格要求 AI PCB、半导体、海外业务多年持续兑现", "不足"],
                ["价值策略", "不按主题追高，等待估值回落或连续财报验证", "跟踪等待"],
            ],
            [30 * mm, 88 * mm, 46 * mm],
        )
    )
    story.append(PageBreak())

    story.append(p("一、公司业务画像", st["h1"]))
    story.extend(
        bullets(
            [
                "公司主营智能制造装备及关键器件，具备从基础器件、整机设备到工艺解决方案的垂直一体化能力。",
                "核心业务可以拆成四条线：AI PCB 与信息产业设备、通用工业激光装备、新能源锂电/光伏设备、半导体及泛半导体设备。",
                "2025 年最强增量来自 PCB 智能制造装备，收入 57.73 亿元，同比增长 72.68%，受益于 AI 服务器、高速交换机、高多层板、HDI、先进封装等投资扩张。",
                "公司不是单纯“光纤光棒”或“通信公司”，更准确的定位是高端装备平台，AI 方向主要通过 PCB 设备、消费电子创新设备和半导体设备体现。",
            ],
            st["base"],
        )
    )
    story.append(Spacer(1, 3 * mm))
    story.append(
        table(
            [
                ["业务/产品", "2025 收入", "占比", "同比", "毛利率", "价值判断"],
                ["PCB 智能制造装备", "57.73 亿元", "30.78%", "+72.68%", "35.12%", "AI 算力 PCB 是最强主线，毛利率高，决定估值弹性"],
                ["其他智能制造装备", "129.86 亿元", "69.22%", "+13.63%", "32.46%", "包含通用激光、消费电子、新能源、半导体等，构成收入底盘"],
                ["激光分部", "120.50 亿元", "-", "-", "约 32.37%", "传统主业体量大，竞争充分，偏周期与制造业投资属性"],
                ["境外收入", "22.06 亿元", "11.76%", "+4.72%", "36.33%", "海外毛利率较高，但收入占比仍不高"],
            ],
            [32 * mm, 24 * mm, 16 * mm, 18 * mm, 20 * mm, 56 * mm],
            font_size=7.3,
            leading=10,
        )
    )

    story.append(p("二、2025 年财务质量", st["h1"]))
    story.append(
        table(
            [
                ["指标", "2025", "2024", "同比/变化", "解读"],
                ["营业收入", "187.59 亿元", "147.71 亿元", "+27.00%", "收入恢复明显，PCB 与新能源设备贡献主要增量"],
                ["归母净利润", "11.90 亿元", "16.94 亿元", "-29.77%", "归母下滑，说明非经常性或结构因素拖累仍需拆分"],
                ["扣非归母净利润", "8.10 亿元", "4.45 亿元", "+82.28%", "主业盈利修复，是 2025 年财报最重要亮点之一"],
                ["经营现金流", "14.69 亿元", "11.26 亿元", "+30.48%", "现金流高于归母净利，利润含金量较好"],
                ["ROE", "7.19%", "10.95%", "-3.76 pct", "ROE 与当前 PB 不匹配，估值依赖未来成长"],
                ["研发投入", "20.84 亿元", "18.20 亿元", "+14.51%", "研发强度 11.11%，装备龙头的长期壁垒来源"],
                ["应收账款", "83.24 亿元", "84.88 亿元", "小幅下降", "占总资产 21.76%，设备公司仍需关注回款周期"],
                ["存货", "52.22 亿元", "39.61 亿元", "明显上升", "备货增加支撑交付，也带来订单兑现和减值观察点"],
            ],
            [30 * mm, 28 * mm, 28 * mm, 25 * mm, 55 * mm],
            font_size=7.3,
            leading=10,
        )
    )
    story.append(
        p(
            "财务结论：2025 年报不能简单用归母净利下滑判断公司变差，也不能只看 PCB 高增长就直接高估值。"
            "更平衡的看法是：主业确实修复，现金流也改善，但 ROE 下降、存货上升、应收账款体量较大，"
            "当前估值需要未来多个季度持续验证。",
            st["base"],
        )
    )

    story.append(PageBreak())
    story.append(p("三、长期价值逻辑", st["h1"]))
    story.append(p("1. AI PCB 设备：当前最强成长曲线", st["h2"]))
    story.extend(
        bullets(
            [
                "AI 服务器和高速交换机推动高多层板、高多层 HDI、先进封装载板需求上升，PCB 设备从传统电子周期转向 AI 基建投资周期。",
                "公司 PCB 智能制造装备 2025 年收入 57.73 亿元、毛利率 35.12%，同比增长 72.68%，是当前市场给高估值的核心理由。",
                "价值投资要跟踪的是订单质量、交付节奏、毛利率是否维持，以及 AI PCB 投资是否从短期扩产变成长期资本开支周期。",
            ],
            st["base"],
        )
    )
    story.append(p("2. 通用激光装备：确定性底盘，但估值弹性弱", st["h2"]))
    story.extend(
        bullets(
            [
                "通用工业激光加工设备收入 61.12 亿元，同比增长 2.37%，说明传统激光装备偏成熟、偏周期。",
                "该板块技术和品牌地位较强，但行业竞争充分，通常难以支撑百倍 PE 的长期估值。",
                "价值上可以视作现金流底盘，而不是当前股价的主要弹性来源。",
            ],
            st["base"],
        )
    )
    story.append(p("3. 新能源与半导体设备：提供第二增长曲线，但波动大", st["h2"]))
    story.extend(
        bullets(
            [
                "新能源设备收入 23.61 亿元，同比增长 53.36%，受益锂电客户国内外扩产，但行业资本开支波动较大。",
                "半导体设备收入 20.41 亿元，同比增长 15.00%，其中大族半导体收入 13.78 亿元，同比增长 23.89%。",
                "半导体设备有国产替代逻辑，但公司在该领域仍需用订单、客户验证和利润率证明持续性。",
            ],
            st["base"],
        )
    )

    story.append(p("四、估值与安全边际", st["h1"]))
    story.append(
        table(
            [
                ["估值项", "计算口径", "结果", "解读"],
                ["市值", "2026-06-26 收盘价 151.27 元，总股本约 10.30 亿股", "约 1557 亿元", "市场按 AI 装备成长股定价"],
                ["PE", "市值 / 2025 归母净利 11.90 亿元", "约 131 倍", "对未来利润增长要求很高"],
                ["扣非 PE", "市值 / 2025 扣非净利 8.10 亿元", "约 192 倍", "主业利润视角估值更高"],
                ["PB", "市值 / 2025 归母净资产 172.83 亿元", "约 9.0 倍", "对装备公司而言明显偏高"],
                ["PS", "市值 / 2025 收入 187.59 亿元", "约 8.3 倍", "已充分反映 AI PCB 预期"],
                ["经营现金流收益率", "2025 经营现金流 14.69 亿元 / 市值", "约 0.94%", "现金流角度安全边际不足"],
            ],
            [28 * mm, 58 * mm, 26 * mm, 54 * mm],
            font_size=7.3,
            leading=10,
        )
    )
    story.append(Spacer(1, 8 * mm))
    story.append(
        p(
            "估值结论：如果按传统激光装备公司看，大族激光当前估值明显过高；如果按 AI PCB 设备龙头看，"
            "当前价格已经要求 PCB 设备高增长、海外扩产、半导体设备突破共同兑现。价值投资的关键不是证明公司有逻辑，"
            "而是等待价格留下错误空间。以当前估值看，安全边际偏低。",
            st["verdict"],
        )
    )
    story.append(
        table(
            [
                ["情景", "假设", "合理估值框架", "投资含义"],
                ["保守情景", "PCB 设备增速回落，激光装备低速增长", "25-35 倍 PE", "当前价格吸引力不足"],
                ["中性情景", "PCB 维持高景气，新能源和半导体平稳贡献", "40-60 倍 PE", "需要业绩增长消化估值"],
                ["乐观情景", "AI PCB 订单持续超预期，半导体设备打开空间", "60-80 倍 PE", "仍需利润显著上修"],
                ["极乐观情景", "成为全球 AI PCB 核心设备龙头，利润连续高增", "80 倍以上 PE", "当前价格才可被解释，但容错率低"],
            ],
            [25 * mm, 62 * mm, 34 * mm, 45 * mm],
            font_size=7.3,
            leading=10,
        )
    )

    story.append(PageBreak())
    story.append(p("五、核心风险", st["h1"]))
    story.extend(
        bullets(
            [
                "估值风险：静态 PE 约 131 倍、扣非 PE 约 192 倍，若 AI PCB 或设备板块情绪降温，估值压缩会很剧烈。",
                "订单兑现风险：PCB 设备高增长来自 AI 资本开支，若客户扩产节奏放缓，会直接影响收入和利润。",
                "存货风险：2025 年存货升至 52.22 亿元，若需求变化，可能带来减值或周转压力。",
                "应收账款风险：应收账款 83.24 亿元，占总资产 21.76%，设备公司回款周期和客户信用质量需持续观察。",
                "传统激光竞争风险：通用激光装备竞争充分，价格战可能压制利润率。",
                "海外经营风险：公司计划加快海外运营中心和生产基地建设，但海外收入占比仍不高，地缘、贸易壁垒和本地化成本都需观察。",
            ],
            st["base"],
        )
    )

    story.append(p("六、价值投资操作框架", st["h1"]))
    story.append(
        table(
            [
                ["状态", "判断标准", "策略"],
                ["不买区", "估值高、股价强、财报尚未连续验证", "只跟踪，不追买"],
                ["观察区", "股价回撤或横盘，估值开始消化，PCB 订单仍强", "建立观察清单"],
                ["试仓区", "季度扣非利润继续高增，存货转收入，现金流稳定", "小仓跟踪，设置财报验证点"],
                ["加仓区", "AI PCB 与半导体设备双线兑现，估值和成长匹配", "按业绩趋势分批加仓"],
                ["退出区", "PCB 订单转弱、毛利率下滑、存货和应收恶化", "降低仓位，回到观察"],
            ],
            [24 * mm, 80 * mm, 62 * mm],
            font_size=7.5,
            leading=10.5,
        )
    )
    story.append(Spacer(1, 8 * mm))
    story.append(
        p(
            "建议的价值投资结论：大族激光值得长期跟踪，尤其要跟踪 AI PCB 设备的订单和毛利率。"
            "但以 2026-06-26 价格看，股价已经按高成长装备龙头定价，价值投资者不宜只因“AI PCB/海外扩产/半导体设备”主题追高。"
            "若已有持仓，应当按高估值成长股管理，用季度扣非利润、现金流、存货和应收来持续验证。",
            st["verdict"],
        )
    )

    story.append(p("七、后续跟踪指标", st["h1"]))
    story.append(
        table(
            [
                ["指标", "跟踪重点", "为何重要"],
                ["PCB 设备收入", "是否继续高增长，特别是 AI 服务器 PCB 订单", "决定估值弹性"],
                ["PCB 设备毛利率", "是否维持 35% 左右或继续改善", "决定高收入能否转为高利润"],
                ["扣非净利润", "是否持续快于收入增长", "判断主业质量"],
                ["经营现金流", "是否持续高于净利润", "验证利润含金量"],
                ["存货和应收", "存货是否转化为收入，应收是否回落", "判断订单兑现和回款质量"],
                ["海外收入", "东南亚运营中心、海外生产基地进展", "验证出海逻辑"],
                ["半导体设备", "先进封装、晶圆搬运、显示设备订单", "决定第二成长曲线"],
            ],
            [30 * mm, 70 * mm, 66 * mm],
            font_size=7.5,
            leading=10.5,
        )
    )

    story.append(p("八、资料来源", st["h1"]))
    story.extend(
        bullets(
            [
                "大族激光科技产业集团股份有限公司《2025 年年度报告》，巨潮资讯，公告编号 1225114033，披露日期 2026-04-17。",
                "腾讯行情接口，大族激光 002008，2026-06-26 收盘价、市值、成交等行情数据。",
                "截至 2026-06-28 查询，巨潮资讯未检索到大族激光 2026 年第一季度报告公告，本报告财务口径以 2025 年报为主。",
                "本报告所有估值测算均为基于公开数据的静态估算，不代表未来收益承诺。",
            ],
            st["note"],
        )
    )

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
