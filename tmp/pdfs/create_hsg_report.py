from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

OUT = "/Users/krauser/Documents/Obsidian Vault/trade/output/pdf/沪硅产业长期炒作价值投资报告.pdf"

FONT = "/System/Library/Fonts/STHeiti Medium.ttc"
pdfmetrics.registerFont(TTFont("CN", FONT))
pdfmetrics.registerFont(TTFont("CN-Bold", FONT))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="TitleCN",
    fontName="CN-Bold",
    fontSize=22,
    leading=28,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#0f172a"),
    spaceAfter=14,
))
styles.add(ParagraphStyle(
    name="SubTitleCN",
    fontName="CN",
    fontSize=10.5,
    leading=16,
    alignment=TA_CENTER,
    textColor=colors.HexColor("#475569"),
    spaceAfter=18,
))
styles.add(ParagraphStyle(
    name="H1CN",
    fontName="CN-Bold",
    fontSize=15,
    leading=20,
    textColor=colors.HexColor("#0f172a"),
    spaceBefore=12,
    spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="H2CN",
    fontName="CN-Bold",
    fontSize=12,
    leading=17,
    textColor=colors.HexColor("#1e293b"),
    spaceBefore=8,
    spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="BodyCN",
    fontName="CN",
    fontSize=9.8,
    leading=15.5,
    textColor=colors.HexColor("#1f2937"),
    alignment=TA_LEFT,
    spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="SmallCN",
    fontName="CN",
    fontSize=8.2,
    leading=12,
    textColor=colors.HexColor("#475569"),
    spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="CalloutCN",
    fontName="CN-Bold",
    fontSize=11,
    leading=17,
    textColor=colors.HexColor("#0f172a"),
    backColor=colors.HexColor("#eef6ff"),
    borderColor=colors.HexColor("#93c5fd"),
    borderWidth=0.5,
    borderPadding=8,
    spaceBefore=6,
    spaceAfter=10,
))


def p(text, style="BodyCN"):
    return Paragraph(text, styles[style])


def bullet(text):
    return p("• " + text)


def table(data, widths=None, font_size=8.5):
    wrapped = []
    header_style = ParagraphStyle(
        name=f"TableHeader{font_size}",
        fontName="CN-Bold",
        fontSize=font_size,
        leading=font_size + 4,
        textColor=colors.HexColor("#0f172a"),
    )
    cell_style = ParagraphStyle(
        name=f"TableCell{font_size}",
        fontName="CN",
        fontSize=font_size,
        leading=font_size + 4,
        textColor=colors.HexColor("#1f2937"),
    )
    for r, row in enumerate(data):
        wrapped.append([
            Paragraph(str(cell), header_style if r == 0 else cell_style)
            for cell in row
        ])
    t = Table(wrapped, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "CN"),
        ("FONTSIZE", (0, 0), (-1, -1), font_size),
        ("LEADING", (0, 0), (-1, -1), font_size + 4),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#0f172a")),
        ("FONTNAME", (0, 0), (-1, 0), "CN-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cbd5e1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return t


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("CN", 8)
    canvas.setFillColor(colors.HexColor("#64748b"))
    canvas.drawString(1.7 * cm, 1.0 * cm, "沪硅产业长期炒作价值投资报告 - 个人交易研究，不构成投资建议")
    canvas.drawRightString(19.3 * cm, 1.0 * cm, f"第 {doc.page} 页")
    canvas.restoreState()


story = []
story.append(p("沪硅产业（688126）长期炒作价值投资报告", "TitleCN"))
story.append(p("生成日期：2026-06-27 | 研究对象：上海硅产业集团股份有限公司 | 报告属性：个人交易研究，不构成投资建议", "SubTitleCN"))
story.append(p("核心结论：当前约 1152 亿元总市值，沪硅产业仍具备长期主题炒作价值，但更适合作为半导体硅片国产替代的“中军/趋势锚”，不是小市值高弹性票。若只看当前利润，估值并不便宜；若看国产 12 英寸硅片、先进制程材料平台和科创半导体材料稀缺性，它仍可能在产业催化和科技主线共振时被资金反复定价。", "CalloutCN"))

story.append(p("一、关键数据与结论", "H1CN"))
story.append(table([
    ["项目", "数据", "解读"],
    ["收盘价", "34.86 元", "来自东方财富行情接口，2026-06-26 收盘口径"],
    ["总市值", "约 1152.13 亿元", "已进入千亿市值区间，炒作弹性更多来自行业 Beta 与稀缺溢价"],
    ["流通市值", "约 990.76 亿元", "流动性充足，适合大资金参与，但短线拉升阻力也更大"],
    ["2025 年营收", "37.16 亿元，同比 +9.69%", "收入仍在增长，但体量尚未匹配千亿市值的传统估值逻辑"],
    ["2025 年归母净利", "-15.08 亿元", "利润端处于压力区，当前估值主要买预期而非买利润"],
    ["2026Q1 营收", "10.84 亿元，同比 +35.22%", "需求和产能利用率可能改善，是积极信号"],
    ["2026Q1 归母净利", "-4.83 亿元", "亏损仍未扭转，盈利拐点需要继续验证"],
], [3.1*cm, 4.0*cm, 9.2*cm]))

story.append(p("我的判断：沪硅产业具备长期炒作价值，但“长期炒作价值”不等同于“当前就是长期投资性价比最高”。它当前的市场定价已经给了国产替代、12 英寸大硅片、半导体材料平台化和科创板稀缺性的较高权重，后续必须用营收放量、毛利率修复、亏损收窄和大客户验证来消化估值。", "BodyCN"))

story.append(p("二、市值是否适合继续炒作", "H1CN"))
story.append(p("从 A 股交易角度，沪硅产业当前 1152 亿元总市值具有两面性。", "BodyCN"))
story.append(bullet("有利面：千亿市值说明它已经被市场视为半导体硅片核心资产，具备机构资金容量、科创板辨识度和主线锚点属性。半导体材料行情来临时，资金需要一个能容纳大资金的中军，沪硅产业正好符合。"))
story.append(bullet("不利面：千亿市值也意味着它不再是轻盘子弹性票。若没有半导体材料板块共振、科创 50 风险偏好提升、国产替代催化或公司盈利改善，单靠故事推动持续翻倍的阻力很大。"))
story.append(bullet("交易定位：更像“硅片中军 + 国产替代锚 + 半导体材料情绪温度计”，不是短线后排补涨。"))

story.append(p("结论：从市值角度看，它仍有长期主题炒作资格，但后续每一轮上涨都要有更强的产业或财务验证。当前更适合观察“趋势波段”和“主线共振”，而不适合用小票思维追高。", "BodyCN"))

story.append(p("三、公司产业位置", "H1CN"))
story.append(p("沪硅产业专注半导体硅材料产业，目标是提升我国半导体硅片产业综合竞争力，并打造一站式半导体材料服务平台。半导体硅片是晶圆制造最底层材料之一，产业位置靠前，国产替代意义强。", "BodyCN"))
story.append(table([
    ["维度", "判断"],
    ["产业环节", "半导体硅材料，重点在 300mm/200mm 硅片及相关硅基材料生态。"],
    ["A 股稀缺性", "半导体硅片主线标的有限，沪硅产业是最容易被市场拿来代表“国产大硅片”的公司之一。"],
    ["资金角色", "当半导体设备、封测、存储、材料共振时，沪硅产业可作为材料链中军；当材料线弱时，它容易变成观察仓而非主攻仓。"],
    ["产业弹性", "来自国产替代、客户验证、产能爬坡、300mm 硅片放量、先进制程和功率/存储周期修复。"],
], [4.0*cm, 12.3*cm]))

story.append(p("四、长期炒作逻辑", "H1CN"))
story.append(p("1. 国产替代逻辑：半导体硅片长期由海外厂商占据较高份额，国内晶圆厂扩产和供应链安全诉求，会持续给国产硅片企业估值溢价。沪硅产业作为 A 股少数能代表这一环节的公司，容易成为政策和产业安全主题的承载标的。", "BodyCN"))
story.append(p("2. 12 英寸硅片放量逻辑：真正决定长期空间的是 300mm 大硅片的客户导入、稳定供货和产能利用率。如果公司能证明高端产品放量并带动毛利率回升，市值有望从“预期驱动”切到“业绩驱动”。", "BodyCN"))
story.append(p("3. 半导体材料主线共振：A 股资金通常不会孤立炒硅片，而是与存储、封测、设备、光刻胶、电子特气、CMP、靶材等材料线共振。沪硅产业的持续性要看材料链是否形成板块效应。", "BodyCN"))
story.append(p("4. 科创 50 风险偏好：沪硅产业是典型科创半导体资产。当科创 50、半导体设备、存储、封测趋势改善时，沪硅产业更容易被动获得风险偏好溢价。", "BodyCN"))
story.append(p("5. 硅光/CPO 延伸想象：硅光、CPO、先进封装对硅基材料、SOI、晶圆制造、封装测试生态有映射空间。但这部分对沪硅产业更偏“主题加分”，需要防止过度外推。", "BodyCN"))

story.append(p("五、估值约束：为什么不能只讲故事", "H1CN"))
story.append(p("当前最大矛盾是：公司市值已经很高，但利润端仍然亏损。2025 年营收 37.16 亿元、归母净利亏损 15.08 亿元；2026Q1 营收同比增长 35.22%，但仍亏损 4.83 亿元。也就是说，市场当前买的是“未来国产替代成功后的利润曲线”，不是当前财务报表。", "BodyCN"))
story.append(table([
    ["观察项", "正面解释", "负面约束"],
    ["收入增长", "2026Q1 收入同比明显改善，说明需求或产能利用率有恢复迹象", "收入体量距离支撑千亿市值仍有差距"],
    ["毛利率", "若产能利用率提升，毛利率可能修复", "2025 年和 2026Q1 毛利率仍为负，盈利拐点未确认"],
    ["净利润", "亏损阶段可能是产能爬坡期的典型现象", "亏损扩大将削弱长期投资逻辑"],
    ["市值", "千亿市值带来资金容量和核心资产标签", "估值对业绩兑现非常敏感，业绩不达预期容易杀估值"],
], [3.2*cm, 6.7*cm, 6.4*cm]))

story.append(p("六、交易框架：什么时候值得提高仓位", "H1CN"))
story.append(p("沪硅产业不能单独看，必须放在半导体材料和科创风险偏好里看。", "BodyCN"))
story.append(table([
    ["情景", "触发条件", "交易含义"],
    ["强观察", "沪硅强于科创50，强于半导体材料指数，成交额放大且收盘站稳关键均线", "可从观察仓升级为交易仓"],
    ["主线确认", "半导体设备、封测、存储、材料共振，沪硅成为材料链前排之一", "可按半导体材料中军参与趋势波段"],
    ["只观察", "材料线不强，沪硅只是跟随科创反弹", "保留观察，不追高不补弱"],
    ["降级", "科创50强而沪硅弱，或半导体材料强而沪硅弱于同题材核心", "说明资金不认可，降级为弱票"],
    ["退出", "放量冲高回落、跌破关键支撑、毛利/亏损继续恶化", "主题逻辑仍在，但交易逻辑失效"],
], [3.0*cm, 8.0*cm, 5.2*cm]))

story.append(p("七、长期跟踪指标", "H1CN"))
story.append(bullet("收入：季度收入是否持续放大，尤其 300mm 硅片相关收入是否放量。"))
story.append(bullet("毛利率：负毛利是否收窄并转正，这是从主题炒作走向业绩重估的关键。"))
story.append(bullet("亏损：归母净利和扣非净利是否连续收窄。"))
story.append(bullet("客户验证：国内主流晶圆厂导入、认证、稳定供货节奏。"))
story.append(bullet("产能利用率：扩产后的爬坡速度和单位成本下降。"))
story.append(bullet("板块强度：半导体设备、存储、封测、材料是否共同走强。"))
story.append(bullet("相对强弱：沪硅产业是否强于科创50和半导体材料同类标的。"))

story.append(PageBreak())
story.append(p("八、风险清单", "H1CN"))
story.append(table([
    ["风险", "影响"],
    ["盈利拐点推迟", "市场可能从“国产替代溢价”转向“亏损资产折价”。"],
    ["产能爬坡不及预期", "折旧、人工、能耗等成本压力持续，毛利率修复慢。"],
    ["客户验证慢", "高端硅片导入周期长，收入兑现滞后。"],
    ["行业周期波动", "晶圆厂资本开支、库存周期和价格变化会影响硅片需求。"],
    ["估值过高", "当前市值已包含较多预期，业绩不达预期时回撤可能较大。"],
    ["主题错配", "若市场主线转向 PCB、CPO、封测或设备，沪硅可能只是跟随而非主攻。"],
], [4.0*cm, 12.3*cm]))

story.append(p("九、综合评级", "H1CN"))
story.append(table([
    ["维度", "评分", "说明"],
    ["长期主题炒作价值", "8/10", "国产大硅片稀缺中军，政策和产业安全逻辑强。"],
    ["当前基本面兑现度", "4/10", "收入改善但盈利仍弱，亏损尚未拐头。"],
    ["市值弹性", "5/10", "千亿市值降低弹性，但提升资金容量和核心标签。"],
    ["波段交易价值", "7/10", "适合在半导体材料共振时做趋势波段。"],
    ["长期投资安全边际", "5/10", "需要等待毛利率、亏损、客户验证改善。"],
], [4.5*cm, 2.5*cm, 9.3*cm]))

story.append(p("最终结论：沪硅产业当前市值仍具备长期炒作价值，但它的正确定位是“半导体硅片国产替代中军”，不是“低位小票弹性”。如果后续半导体材料线、科创50、存储/封测/设备共振，并且公司收入高增延续、毛利率改善、亏损收窄，则 1152 亿市值仍可能被市场继续向上重估。反过来，如果盈利拐点迟迟不来，当前市值对财务报表并不便宜，容易出现主题涨完后的估值回撤。", "CalloutCN"))

story.append(p("十、资料来源", "H1CN"))
story.append(p("1. 东方财富行情接口：688126.SH，收盘价、总市值、流通市值等行情数据。接口地址：https://push2.eastmoney.com/api/qt/stock/get?secid=1.688126", "SmallCN"))
story.append(p("2. 东方财富 F10 财务摘要接口：2025 年报、2026 一季报主要财务指标。接口地址：https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/ZYZBAjaxNew?type=0&code=SH688126", "SmallCN"))
story.append(p("3. 东方财富 F10 公司概况接口：公司名称、上市板块、主营描述、公司简介。接口地址：https://emweb.securities.eastmoney.com/PC_HSF10/CompanySurvey/CompanySurveyAjax?code=SH688126", "SmallCN"))
story.append(p("4. 本地交易复盘资料：weekly-reviews/2026-06-22至2026-06-26交易周总结.md、watchlists/2026-06-20-A股硅片相关核心个股.md、daily-reviews/2026-06-26-盘后复盘与下一个交易日策略指引.md。", "SmallCN"))

doc = SimpleDocTemplate(
    OUT,
    pagesize=A4,
    rightMargin=1.5 * cm,
    leftMargin=1.5 * cm,
    topMargin=1.45 * cm,
    bottomMargin=1.55 * cm,
)
doc.build(story, onFirstPage=footer, onLaterPages=footer)
print(OUT)
