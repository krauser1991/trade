import json
import gzip
import urllib.request
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


OUT_DIR = Path("/Users/krauser/Documents/Obsidian Vault/trade/output/pdf")
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"

pdfmetrics.registerFont(TTFont("CN", FONT))
pdfmetrics.registerFont(TTFont("CN-Bold", FONT))

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleCN", fontName="CN-Bold", fontSize=21, leading=28, alignment=TA_CENTER, textColor=colors.HexColor("#0f172a"), spaceAfter=12))
styles.add(ParagraphStyle(name="SubTitleCN", fontName="CN", fontSize=10, leading=15, alignment=TA_CENTER, textColor=colors.HexColor("#475569"), spaceAfter=16))
styles.add(ParagraphStyle(name="H1CN", fontName="CN-Bold", fontSize=15, leading=20, textColor=colors.HexColor("#0f172a"), spaceBefore=12, spaceAfter=8))
styles.add(ParagraphStyle(name="H2CN", fontName="CN-Bold", fontSize=12, leading=17, textColor=colors.HexColor("#1e293b"), spaceBefore=8, spaceAfter=5))
styles.add(ParagraphStyle(name="BodyCN", fontName="CN", fontSize=9.7, leading=15.3, textColor=colors.HexColor("#1f2937"), alignment=TA_LEFT, spaceAfter=6))
styles.add(ParagraphStyle(name="SmallCN", fontName="CN", fontSize=8.0, leading=11.5, textColor=colors.HexColor("#475569"), spaceAfter=4))
styles.add(ParagraphStyle(name="CalloutCN", fontName="CN-Bold", fontSize=10.8, leading=16.8, textColor=colors.HexColor("#0f172a"), backColor=colors.HexColor("#eef6ff"), borderColor=colors.HexColor("#93c5fd"), borderWidth=0.5, borderPadding=8, spaceBefore=6, spaceAfter=10))


COMPANIES = [
    {
        "name": "通富微电",
        "code": "002156",
        "secu": "SZ002156",
        "secid": "0.002156",
        "theme": "先进封装/封测扩散核心",
        "position": "封测弹性核心，适合在存储、先进封装、长鑫链和国产算力封测共振时观察。相比长电科技更偏弹性和周期修复交易，不适合在封测主线不强时单独重仓。",
        "logic": [
            "先进封装与高性能计算封测需求提升，会提高封测环节的市场关注度。",
            "存储、国产算力、长鑫链和 Chiplet/高端封装主题共振时，通富微电容易成为封测扩散核心。",
            "相比封测龙头中军，通富微电的交易弹性通常更强，但波动和业绩周期敏感度也更高。",
            "若封测板块中长电科技、通富微电、华天科技形成梯队，通富微电具备趋势波段价值。"
        ],
        "watch": [
            "封测板块是否与存储、半导体设备、材料共振。",
            "通富微电是否强于长电科技和封测指数，而不是被动跟涨。",
            "收入增速、毛利率和扣非利润能否体现周期修复。",
            "先进封装相关订单、产能利用率和大客户需求变化。"
        ],
        "rating": [
            ["长期主题炒作价值", "7.5/10", "封测和先进封装方向有持续主题，但需板块共振。"],
            ["当前基本面兑现度", "6/10", "需看利润率和封测周期修复程度。"],
            ["市值弹性", "7/10", "通常比封测中军更有弹性，但也更受周期波动影响。"],
            ["波段交易价值", "7.5/10", "适合先进封装、存储、长鑫线共振时做趋势波段。"],
            ["长期投资安全边际", "5.5/10", "封测行业资本开支重，利润弹性需验证。"],
        ],
    },
    {
        "name": "长电科技",
        "code": "600584",
        "secu": "SH600584",
        "secid": "1.600584",
        "theme": "封测容量核心/先进封装中军",
        "position": "封测容量核心，更适合作为半导体封测和先进封装强弱锚。长期炒作价值来自先进封装、AI 芯片封装、存储复苏和半导体周期回暖，但它不是小票弹性，核心是趋势和中军溢价。",
        "logic": [
            "封测是半导体国产链中最容易与存储、AI 芯片、先进封装共同被资金定价的环节。",
            "长电科技流动性和辨识度高，适合机构资金作为封测板块锚点。",
            "当半导体设备、存储、封测同步走强时，长电科技可成为板块中军。",
            "长期价值要看先进封装占比、盈利能力修复和全球封测周期回升。"
        ],
        "watch": [
            "是否强于封测板块和半导体指数。",
            "毛利率和扣非利润是否随行业复苏改善。",
            "先进封装业务占比、客户结构和产能利用率。",
            "涨停或大涨后是否仍有承接，而不是高位兑现。"
        ],
        "rating": [
            ["长期主题炒作价值", "8/10", "封测中军和先进封装核心标签清晰。"],
            ["当前基本面兑现度", "6.5/10", "相对成熟，但仍受半导体周期影响。"],
            ["市值弹性", "6/10", "容量大、辨识度高，但弹性弱于小市值封测票。"],
            ["波段交易价值", "8/10", "适合当作封测/先进封装主线锚做趋势波段。"],
            ["长期投资安全边际", "6/10", "需要利润率和先进封装兑现继续支撑估值。"],
        ],
    },
    {
        "name": "英维克",
        "code": "002837",
        "secu": "SZ002837",
        "secid": "0.002837",
        "theme": "液冷/CDU/数据中心温控中军",
        "position": "AI 数据中心液冷和温控中军，长期炒作价值来自 AI 服务器功耗提升、液冷渗透率上行、CDU 和机房侧热管理需求扩张。它更适合作为液冷方向的容量锚，不是后排概念票。",
        "logic": [
            "AI 服务器功耗提升使数据中心热管理从风冷向冷板液冷、CDU、换热和机房侧系统升级。",
            "Rubin 代高温 Direct-to-Chip 冷板液冷提升了 CDU、监测、控压、换热和系统集成价值。",
            "英维克在数据中心温控和液冷方向具有较高辨识度，容易成为液冷板块中军。",
            "长期价值取决于液冷收入占比、AI 数据中心客户订单和盈利能力持续性。"
        ],
        "watch": [
            "液冷板块是否由英维克、申菱环境等中军确认，而不是小票乱拉。",
            "液冷收入占比、CDU 订单和 AI 数据中心客户变化。",
            "毛利率是否能在竞争加剧下保持稳定。",
            "是否与 CPO、PCB、服务器、电源等 AI 硬件链共振。"
        ],
        "rating": [
            ["长期主题炒作价值", "8/10", "AI 液冷渗透率提升逻辑强，且中军属性明显。"],
            ["当前基本面兑现度", "6.5/10", "需看液冷收入和订单兑现速度。"],
            ["市值弹性", "6.5/10", "容量和弹性相对均衡，强于传统大票但弱于小票。"],
            ["波段交易价值", "8/10", "适合在 AI 硬件扩散和液冷中军确认时做趋势波段。"],
            ["长期投资安全边际", "6/10", "需警惕订单兑现、竞争和估值透支。"],
        ],
    },
]


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip, deflate"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip" or raw[:2] == b"\x1f\x8b":
            raw = gzip.decompress(raw)
        return json.loads(raw.decode("utf-8"))


def quote(secid):
    fields = "f43,f57,f58,f116,f117,f84,f85,f60,f44,f45,f46,f47,f48,f170"
    return fetch_json(f"https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields={fields}")["data"]


def finance(secu, typ=0):
    return fetch_json(f"https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/ZYZBAjaxNew?type={typ}&code={secu}")["data"]


def survey(secu):
    return fetch_json(f"https://emweb.securities.eastmoney.com/PC_HSF10/CompanySurvey/CompanySurveyAjax?code={secu}")["jbzl"]


def yuan(v, scale=1):
    if v is None:
        return "--"
    return f"{v / scale:.2f}"


def pct(v):
    if v is None:
        return "--"
    return f"{v:.2f}%"


def q_price(v):
    if v is None:
        return "--"
    return f"{v / 100:.2f} 元"


def p(text, style="BodyCN"):
    return Paragraph(text, styles[style])


def bullet(text):
    return p("• " + text)


def table(data, widths=None, font_size=8.3):
    header_style = ParagraphStyle(name=f"TH{font_size}", fontName="CN-Bold", fontSize=font_size, leading=font_size + 4, textColor=colors.HexColor("#0f172a"))
    cell_style = ParagraphStyle(name=f"TC{font_size}", fontName="CN", fontSize=font_size, leading=font_size + 4, textColor=colors.HexColor("#1f2937"))
    wrapped = []
    for r, row in enumerate(data):
        wrapped.append([Paragraph(str(cell), header_style if r == 0 else cell_style) for cell in row])
    t = Table(wrapped, colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "CN"),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
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
    canvas.drawString(1.7 * cm, 1.0 * cm, f"{doc.title_text} - 个人交易研究，不构成投资建议")
    canvas.drawRightString(19.3 * cm, 1.0 * cm, f"第 {doc.page} 页")
    canvas.restoreState()


def make_report(cfg):
    q = quote(cfg["secid"])
    fq = finance(cfg["secu"], 0)
    fy = finance(cfg["secu"], 1)
    sv = survey(cfg["secu"])
    latest = fq[0]
    year = fy[0]
    story = []

    price = q_price(q.get("f43"))
    mcap = yuan(q.get("f116"), 1e8)
    float_mcap = yuan(q.get("f117"), 1e8)
    last_rev = yuan(latest.get("TOTALOPERATEREVE"), 1e8)
    last_np = yuan(latest.get("PARENTNETPROFIT"), 1e8)
    last_rev_yoy = pct(latest.get("TOTALOPERATEREVETZ"))
    last_np_yoy = pct(latest.get("PARENTNETPROFITTZ"))
    y_rev = yuan(year.get("TOTALOPERATEREVE"), 1e8)
    y_np = yuan(year.get("PARENTNETPROFIT"), 1e8)
    y_rev_yoy = pct(year.get("TOTALOPERATEREVETZ"))
    y_np_yoy = pct(year.get("PARENTNETPROFITTZ"))
    gross = pct(latest.get("XSMLL"))
    roe = pct(latest.get("ROEJQ"))

    story.append(p(f"{cfg['name']}（{cfg['code']}）详细投资报告", "TitleCN"))
    story.append(p(f"生成日期：2026-06-27 | 研究主题：{cfg['theme']} | 报告属性：个人交易研究，不构成投资建议", "SubTitleCN"))
    story.append(p(f"核心结论：{cfg['position']}", "CalloutCN"))

    story.append(p("一、关键数据", "H1CN"))
    story.append(table([
        ["项目", "数据", "解读"],
        ["收盘价", price, "东方财富行情接口，最近交易日收盘口径"],
        ["总市值", f"约 {mcap} 亿元", "判断资金容量和炒作弹性的核心指标"],
        ["流通市值", f"约 {float_mcap} 亿元", "流通盘越大，越偏趋势中军；越小，越偏弹性"],
        [f"{year.get('REPORT_DATE_NAME')}营收", f"{y_rev} 亿元，同比 {y_rev_yoy}", "年度收入体量和景气度参考"],
        [f"{year.get('REPORT_DATE_NAME')}归母净利", f"{y_np} 亿元，同比 {y_np_yoy}", "年度盈利质量参考"],
        [f"{latest.get('REPORT_DATE_NAME')}营收", f"{last_rev} 亿元，同比 {last_rev_yoy}", "最新季度/报告期增长趋势"],
        [f"{latest.get('REPORT_DATE_NAME')}归母净利", f"{last_np} 亿元，同比 {last_np_yoy}", "最新利润趋势"],
        ["最新毛利率/ROE", f"{gross} / {roe}", "判断是否已经从主题走向业绩兑现"],
    ], [3.5*cm, 4.3*cm, 8.4*cm]))

    story.append(p("二、公司定位与产业角色", "H1CN"))
    story.append(p(sv.get("gsjj", "").strip() or "公司概况以公开 F10 信息为准。", "BodyCN"))
    story.append(table([
        ["维度", "判断"],
        ["上市板块/行业", f"{sv.get('zqlb', '--')}；所属行业：{sv.get('sshy', '--')}"],
        ["交易定位", cfg["position"]],
        ["主线属性", cfg["theme"]],
        ["资金角色", "当所属主线共振时可作为中军/锚点；当主线不强时不宜按孤立题材硬做。"],
    ], [4.0*cm, 12.3*cm]))

    story.append(p("三、长期炒作逻辑", "H1CN"))
    for i, item in enumerate(cfg["logic"], 1):
        story.append(p(f"{i}. {item}", "BodyCN"))

    story.append(p("四、估值与基本面约束", "H1CN"))
    story.append(p(f"当前总市值约 {mcap} 亿元。市值越高，越需要利润、订单、毛利率和行业景气来消化估值；市值越低，越依赖题材弹性和风险偏好。{cfg['name']}当前应把主题逻辑和财务兑现分开看。", "BodyCN"))
    story.append(table([
        ["观察项", "正面解释", "负面约束"],
        ["收入", f"最新报告期营收 {last_rev} 亿元，同比 {last_rev_yoy}", "若收入增长不能持续，主题空间会被压缩"],
        ["利润", f"最新归母净利 {last_np} 亿元，同比 {last_np_yoy}", "利润波动会直接影响中线估值稳定性"],
        ["毛利率", f"最新毛利率 {gross}", "若毛利率下滑，说明竞争或成本压力上升"],
        ["市值", f"总市值约 {mcap} 亿元", "市值越大，单靠故事推动的持续翻倍阻力越大"],
    ], [3.0*cm, 6.6*cm, 6.7*cm]))

    story.append(p("五、交易框架：什么时候值得提高仓位", "H1CN"))
    story.append(table([
        ["情景", "触发条件", "交易含义"],
        ["强观察", f"{cfg['name']}强于所属板块和核心指数，成交额放大且收盘站稳关键均线", "可从观察仓升级为交易仓"],
        ["主线确认", "所属主线与相关上游/下游共同走强，并出现容量锚和梯队", "可按主线中军参与趋势波段"],
        ["只观察", "个股只是跟随指数或板块反弹，未强于同题材核心", "保留观察，不追高不补弱"],
        ["降级", "板块强但个股弱，或个股冲高回落无承接", "说明资金不认可，降级为弱票"],
        ["退出", "跌破关键支撑、放量冲高回落、业绩或订单不及预期", "主题仍在，但交易逻辑失效"],
    ], [3.0*cm, 7.6*cm, 5.7*cm]))

    story.append(p("六、长期跟踪指标", "H1CN"))
    for item in cfg["watch"]:
        story.append(bullet(item))

    story.append(p("七、风险清单", "H1CN"))
    story.append(table([
        ["风险", "影响"],
        ["主线退潮", "即使公司逻辑存在，股价也可能跟随板块估值回落。"],
        ["业绩不及预期", "主题炒作无法转成业绩重估，容易杀估值。"],
        ["竞争加剧", "价格、毛利率和订单质量可能承压。"],
        ["市值已含预期", "如果市值已经提前反映乐观预期，后续涨幅需要更强催化。"],
        ["高开兑现", "强题材日追高容易买到一致性兑现点。"],
    ], [4.0*cm, 12.3*cm]))

    story.append(p("八、综合评级", "H1CN"))
    story.append(table([["维度", "评分", "说明"]] + cfg["rating"], [4.5*cm, 2.5*cm, 9.3*cm]))

    story.append(p(f"最终结论：{cfg['name']}具备长期主题炒作价值，但必须放在所属主线、财务趋势和相对强弱里判断。若所属主线共振、公司收入和利润质量改善、个股强于板块，它可以作为趋势波段核心观察；若只是题材热闹但个股弱于同类核心，则应降级为观察，不应按长期信仰仓处理。", "CalloutCN"))

    story.append(p("九、资料来源", "H1CN"))
    story.append(p(f"1. 东方财富行情接口：{cfg['code']}，收盘价、总市值、流通市值等行情数据。https://push2.eastmoney.com/api/qt/stock/get?secid={cfg['secid']}", "SmallCN"))
    story.append(p(f"2. 东方财富 F10 财务摘要接口：最新报告期和年度主要财务指标。https://emweb.securities.eastmoney.com/PC_HSF10/NewFinanceAnalysis/ZYZBAjaxNew?type=0&code={cfg['secu']}", "SmallCN"))
    story.append(p(f"3. 东方财富 F10 公司概况接口：公司名称、上市板块、主营描述、公司简介。https://emweb.securities.eastmoney.com/PC_HSF10/CompanySurvey/CompanySurveyAjax?code={cfg['secu']}", "SmallCN"))
    story.append(p("4. 本地交易复盘资料：拆哥盘面与隔日思考模式、2026-06-18 当前市场主线关系与大盘观察框架、2026-06-23 英伟达高温液冷新技术与 A 股炒作顺序、weekly-reviews/2026-06-22至2026-06-26交易周总结。", "SmallCN"))

    out = OUT_DIR / f"{cfg['name']}详细投资报告.pdf"
    doc = SimpleDocTemplate(str(out), pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=1.45*cm, bottomMargin=1.55*cm)
    doc.title_text = f"{cfg['name']}详细投资报告"
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    return out


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for cfg in COMPANIES:
        print(make_report(cfg))


if __name__ == "__main__":
    main()
