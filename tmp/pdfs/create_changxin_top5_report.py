#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt
import gzip
import io
import json
import textwrap
import urllib.request

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


OUT = "output/pdf/长鑫存储产业链最受益5家公司投资报告.pdf"
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"

STOCKS = [
    {
        "rank": 1,
        "name": "兆易创新",
        "code": "603986",
        "sina": "sh603986",
        "secid": "1.603986",
        "f10": "SH603986",
        "layer": "参股 + 存储产品映射",
        "position": "长鑫产业高度锚",
        "logic": "同时具备长鑫参股、国产存储产品映射和市场辨识度。若长鑫线从纯参股情绪升级为产业主线，兆易创新通常是最容易被资金用来确认产业高度的标的。",
        "watch": "重点看它是否强于普通存储股、是否能与设备材料同步走强。若只有华安证券、合百集团强而兆易不强，说明题材仍偏参股情绪。",
        "risk": "参股价值不等于利润兑现；存储周期、产品价格和估值弹性会放大波动。",
    },
    {
        "rank": 2,
        "name": "北方华创",
        "code": "002371",
        "sina": "sz002371",
        "secid": "0.002371",
        "f10": "SZ002371",
        "layer": "半导体设备",
        "position": "设备平台中军",
        "logic": "覆盖刻蚀、薄膜、清洗、热处理等关键设备。长鑫扩产首先会拉动晶圆制造资本开支，平台型设备公司比单一弹性票更能承接机构资金。",
        "watch": "若北方华创与中微公司同步走强，说明市场开始交易国产存储扩产的设备订单，而不是只炒名字和参股。",
        "risk": "市值和估值已较大，订单兑现节奏、验收周期和半导体设备板块整体风险偏好会影响弹性。",
    },
    {
        "rank": 3,
        "name": "中微公司",
        "code": "688012",
        "sina": "sh688012",
        "secid": "1.688012",
        "f10": "SH688012",
        "layer": "刻蚀设备",
        "position": "设备技术锚",
        "logic": "刻蚀是存储制造的关键工艺环节，中微公司是国产刻蚀设备核心代表。长鑫扩产若被市场理解为国产设备替代，它是设备线最重要的技术锚之一。",
        "watch": "和北方华创一起观察。二者同时强，设备线才有主线资格；若只有小设备票强，更多是后排弹性。",
        "risk": "科创板波动大，设备订单确认和海外限制因素可能影响市场预期。",
    },
    {
        "rank": 4,
        "name": "安集科技",
        "code": "688019",
        "sina": "sh688019",
        "secid": "1.688019",
        "f10": "SH688019",
        "layer": "CMP 材料/耗材",
        "position": "材料中军",
        "logic": "CMP 抛光液和相关材料属于晶圆制造持续消耗品。相比一次性设备订单，材料的优势在于产线放量后具备持续耗材需求，适合承接长鑫扩产后的国产材料替代想象。",
        "watch": "设备确认后，看安集科技、雅克科技、江化微、鼎龙股份是否扩散。如果材料不跟，长鑫线容易停留在设备和情绪层。",
        "risk": "客户认证不等于大比例供货，收入贡献需要看量产规模、产品结构和毛利变化。",
    },
    {
        "rank": 5,
        "name": "雅克科技",
        "code": "002409",
        "sina": "sz002409",
        "secid": "0.002409",
        "f10": "SZ002409",
        "layer": "前驱体/半导体材料",
        "position": "材料平台",
        "logic": "原始产业链线索指向公司前驱体材料供应合肥长鑫。严格按长鑫扩产受益顺序，材料端比封测端更靠近晶圆制造，且具备从产线放量中持续受益的耗材属性。",
        "watch": "和安集科技、江化微、鼎龙股份、中船特气一起观察。若材料线强于封测线，雅克科技应排在通富微电之前。",
        "risk": "前驱体具体供货品类、供货比例和收入贡献需要以公告、年报、互动易或招股书口径继续核验。",
    },
]


def fetch_json(url):
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept-Encoding": "gzip",
            "Referer": "https://quote.eastmoney.com/",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        raw = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
    text = raw.decode("utf-8", errors="ignore")
    if text.startswith("jQuery"):
        text = text[text.find("(") + 1 : text.rfind(")")]
    return json.loads(text)


def quote(stock):
    fields = "f43,f44,f45,f46,f47,f48,f60,f116,f117,f162,f167,f168,f170,f171,f292"
    url = (
        "https://push2.eastmoney.com/api/qt/stock/get?"
        f"secid={stock['secid']}&fields={fields}&ut=fa5fd1943c7b386f172d6893dbfba10b"
    )
    data = fetch_json(url).get("data") or {}
    div100 = lambda x: None if x in (None, "-") else x / 100
    div1e8 = lambda x: None if x in (None, "-") else x / 100000000
    return {
        "price": div100(data.get("f43")),
        "pct": div100(data.get("f170")),
        "high": div100(data.get("f44")),
        "low": div100(data.get("f45")),
        "turnover": div1e8(data.get("f48")),
        "mcap": div1e8(data.get("f116")),
        "pe": div100(data.get("f162")),
        "pb": div100(data.get("f167")),
        "status": data.get("f292"),
    }


def sina_quote(stock):
    url = f"https://hq.sinajs.cn/list={stock['sina']}"
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://finance.sina.com.cn/",
        },
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        text = resp.read().decode("gbk", errors="ignore")
    raw = text.split('"')[1].split(",")
    return {
        "open": float(raw[1]),
        "prev_close": float(raw[2]),
        "price": float(raw[3]),
        "high": float(raw[4]),
        "low": float(raw[5]),
        "volume": float(raw[8]),
        "amount": float(raw[9]),
        "date": raw[30],
        "time": raw[31],
    }


def survey(stock):
    url = f"https://emweb.securities.eastmoney.com/PC_HSF10/CompanySurvey/PageAjax?code={stock['f10']}"
    data = fetch_json(url)
    info = {}
    for key in ("jbzl", "zygcfx", "jyps"):
        val = data.get(key)
        if isinstance(val, list) and val:
            info[key] = val[0]
        elif isinstance(val, dict):
            info[key] = val
    return info


def fmt_num(x, suffix=""):
    if x is None:
        return "-"
    return f"{x:.2f}{suffix}"


def clean(text, limit=260):
    if not text:
        return "-"
    text = str(text).replace("\n", " ").replace("\r", " ").strip()
    text = " ".join(text.split())
    return text[:limit] + ("..." if len(text) > limit else "")


def p(text, style):
    return Paragraph(str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"), style)


def first_present(mapping, keys):
    for key in keys:
        value = mapping.get(key)
        if value not in (None, ""):
            return value
    return None


def build_pdf(rows):
    pdfmetrics.registerFont(TTFont("CN", FONT))
    doc = SimpleDocTemplate(
        OUT,
        pagesize=A4,
        leftMargin=1.45 * cm,
        rightMargin=1.45 * cm,
        topMargin=1.35 * cm,
        bottomMargin=1.25 * cm,
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("TitleCN", fontName="CN", fontSize=20, leading=28, alignment=TA_CENTER, spaceAfter=12))
    styles.add(ParagraphStyle("H1CN", fontName="CN", fontSize=14, leading=20, spaceBefore=12, spaceAfter=8, textColor=colors.HexColor("#1f4e79")))
    styles.add(ParagraphStyle("BodyCN", fontName="CN", fontSize=9.5, leading=15, alignment=TA_LEFT, spaceAfter=5))
    styles.add(ParagraphStyle("SmallCN", fontName="CN", fontSize=8, leading=12, alignment=TA_LEFT))
    styles.add(ParagraphStyle("CellCN", fontName="CN", fontSize=7.2, leading=10.5, alignment=TA_LEFT))
    styles.add(ParagraphStyle("HeadCN", fontName="CN", fontSize=7.5, leading=10, alignment=TA_CENTER, textColor=colors.white))

    story = []
    today = dt.date.today().isoformat()
    story.append(p("长鑫存储产业链最受益 5 家公司投资报告", styles["TitleCN"]))
    story.append(p(f"生成日期：{today}；用途：A 股交易研究与复盘沉淀；结论不构成投资建议。", styles["SmallCN"]))
    story.append(Spacer(1, 8))

    story.append(p("一、核心结论", styles["H1CN"]))
    story.append(
        p(
            "复核结论：上一版报告中的行情数据经东方财富与新浪行情交叉核对，价格、涨跌幅方向和收盘日期一致；但产业关系表述需要更严谨。尤其“通富微电具备合肥控股背景”不成立，应删除。严格按长鑫扩产受益链条，前五名修正为：兆易创新、北方华创、中微公司、安集科技、雅克科技。",
            styles["BodyCN"],
        )
    )
    story.append(
        p(
            "本报告把关系强度分为三类：一是行情和公司基础资料，按行情/F10数据处理；二是公司主营与产业环节，按公开业务范围处理；三是与长鑫的客户、供货、参股关系，若无法在本次复核中形成公告级证据，则降级为“产业链线索/交易映射”，不写成确定订单。",
            styles["BodyCN"],
        )
    )
    story.append(
        p(
            "合肥属性复核：前五名中没有合肥注册地公司，排序仍以产业距离和扩产受益为主。合肥本地或合肥子公司是加分项，主要提升通富微电、深科技、汇成股份、颀中科技、晶合集成、芯碁微装等扩散层标的的优先级，但不让其越级替代设备材料核心。长电科技虽是封测龙头，但缺少合肥属性，在长鑫/合肥单线里不如通富微电贴近。",
            styles["BodyCN"],
        )
    )
    story.append(
        p(
            "一句话框架：兆易创新决定长鑫产业辨识度；北方华创和中微公司决定扩产设备订单想象；安集科技和雅克科技决定材料耗材国产替代想象；通富微电、江波龙、德明利放在封测和产品端扩散层观察。",
            styles["BodyCN"],
        )
    )

    story.append(p("二、最受益 5 家公司总表", styles["H1CN"]))
    table_data = [[p(x, styles["HeadCN"]) for x in ["排名", "公司", "层级", "交易定位", "现价", "总市值", "PE", "涨跌幅"]]]
    for r in rows:
        q = r["quote"]
        sq = r["sina_quote"]
        table_data.append(
            [
                p(r["rank"], styles["CellCN"]),
                p(f"{r['name']} {r['code']}", styles["CellCN"]),
                p(r["layer"], styles["CellCN"]),
                p(r["position"], styles["CellCN"]),
                p(fmt_num(q.get("price")), styles["CellCN"]),
                p(fmt_num(q.get("mcap"), " 亿"), styles["CellCN"]),
                p(fmt_num(q.get("pe")), styles["CellCN"]),
                p(fmt_num(q.get("pct"), "%"), styles["CellCN"]),
            ]
        )
    t = Table(table_data, colWidths=[0.8 * cm, 1.75 * cm, 2.5 * cm, 2.5 * cm, 1.35 * cm, 1.55 * cm, 1.2 * cm, 1.35 * cm], repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#b7c9d8")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fbfd")),
            ]
        )
    )
    story.append(t)

    story.append(p("三、逐家公司详细理由", styles["H1CN"]))
    for r in rows:
        q = r["quote"]
        sq = r["sina_quote"]
        s = r.get("survey", {})
        jbzl = s.get("jbzl", {})
        intro = clean(first_present(jbzl, ["INTRODUCE", "ZYYW", "MAINBUSIN", "BUSINESS_SCOPE", "ORG_PROFILE"]), 220)
        story.append(p(f"{r['rank']}. {r['name']}（{r['code']}）：{r['position']}", styles["H1CN"]))
        story.append(p(f"当前市场参考：截至新浪行情 {sq.get('date')} {sq.get('time')}，现价 {fmt_num(q.get('price'))}，涨跌幅 {fmt_num(q.get('pct'), '%')}，总市值 {fmt_num(q.get('mcap'), ' 亿')}，PE {fmt_num(q.get('pe'))}，PB {fmt_num(q.get('pb'))}。", styles["BodyCN"]))
        story.append(p(f"公司业务摘要：{intro}", styles["BodyCN"]))
        story.append(p(f"入选原因：{r['logic']}", styles["BodyCN"]))
        story.append(p(f"盘中观察：{r['watch']}", styles["BodyCN"]))
        story.append(p(f"主要风险：{r['risk']}", styles["BodyCN"]))

    story.append(PageBreak())
    story.append(p("四、交易验证框架", styles["H1CN"]))
    scenarios = [
        ("参股情绪", "华安证券、合百集团、合肥城建强，但兆易创新、设备、材料、封测不强。结论：只是参股估值弹性，适合按情绪套利处理。"),
        ("产业确认", "兆易创新强，北方华创和中微公司同步强，安集科技等材料跟随。结论：市场开始交易长鑫扩产和国产替代。"),
        ("材料确认", "安集科技、雅克科技、江化微、鼎龙股份跟随。结论：市场从设备订单想象扩散到材料耗材国产替代。"),
        ("扩散质量", "通富微电、江波龙、德明利、华天科技跟随。结论：长鑫线从制造端扩散到封测和存储模组端，但这层应排在设备材料之后。"),
    ]
    for title, body in scenarios:
        story.append(p(f"{title}：{body}", styles["BodyCN"]))

    story.append(p("五、未入选但需跟踪的备选标的", styles["H1CN"]))
    alt_data = [[p(x, styles["HeadCN"]) for x in ["公司", "定位", "合肥属性", "没有进入前五的原因", "优先级上升条件"]]]
    alts = [
        ("通富微电", "封测/先进封装扩散", "合肥生产基地", "不应写成合肥控股；但F10显示拥有合肥生产基地，长鑫/合肥单线辨识度强于长电科技。", "长鑫/合肥封测扩散时，作为封测层优先观察位。"),
        ("长电科技", "封测龙头/先进封装", "非合肥", "封测综合实力强，但F10显示注册/办公在江苏江阴，缺少合肥本地或合肥基地加分；长鑫/合肥单线不如通富贴近。", "市场主炒封测整体、先进封装、AI封装时，长电可强于通富。"),
        ("深科技", "存储封测/代工", "合肥沛顿/合肥封测基地", "产业层级偏扩散，不如设备材料直接承接扩产。", "合肥沛顿、存储封测和国产材料导入线索共振时优先级上升。"),
        ("汇成股份", "封测/微电子", "合肥注册/办公", "合肥属性强，但长鑫单线确定性弱于设备材料核心。", "合肥半导体生态和封测扩散同时强时观察。"),
        ("颀中科技", "封测/显示驱动", "合肥注册", "更偏合肥封测生态扩散，长鑫单线映射较弱。", "合肥本地半导体生态扩散时观察。"),
        ("江波龙/德明利", "存储产品弹性", "非合肥", "更偏产品端和存储涨价弹性。", "市场主炒存储涨价、模组业绩和产品端补涨时优先级上升。"),
        ("华安证券/合百集团", "参股含鑫量情绪", "合肥注册/国资", "含鑫量弹性强，但主营不是半导体产业链，产业兑现弱。", "题材启动、参股估值弹性阶段可作为情绪风向标。"),
    ]
    for row in alts:
        alt_data.append([p(x, styles["CellCN"]) for x in row])
    t2 = Table(alt_data, colWidths=[1.8 * cm, 2.2 * cm, 2.2 * cm, 4.3 * cm, 4.3 * cm], repeatRows=1)
    t2.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#b7c9d8")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]
        )
    )
    story.append(t2)

    story.append(p("六、资料口径与风险提示", styles["H1CN"]))
    story.append(p("资料来源：本地 Obsidian 交易研究文档《2026-06-24 二长产业链炒作思路与核心股》《2026-06-25 合肥本地与长鑫相关 A 股梳理》；东方财富行情/F10；新浪行情。行情日期以新浪行情返回的 2026-06-26 收盘数据为准。", styles["SmallCN"]))
    story.append(p("本报告用于交易复盘和观察池建设，不构成买卖建议。涉及客户关系、供货比例、参股比例、订单规模等信息，未能公告级确认的统一按交易映射处理，应继续以公司公告、年报、招股书、互动易或监管披露为准。", styles["SmallCN"]))

    def footer(canvas, doc_obj):
        canvas.saveState()
        canvas.setFont("CN", 8)
        canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawCentredString(A4[0] / 2, 0.65 * cm, f"第 {doc_obj.page} 页")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def main():
    rows = []
    for stock in STOCKS:
        item = dict(stock)
        item["quote"] = quote(stock)
        item["sina_quote"] = sina_quote(stock)
        if item["quote"].get("price") is not None and abs(item["quote"]["price"] - item["sina_quote"]["price"]) > 0.02:
            raise RuntimeError(f"行情交叉核对失败: {stock['name']} Eastmoney={item['quote']['price']} Sina={item['sina_quote']['price']}")
        try:
            item["survey"] = survey(stock)
        except Exception:
            item["survey"] = {}
        rows.append(item)
    build_pdf(rows)
    print(OUT)


if __name__ == "__main__":
    main()
