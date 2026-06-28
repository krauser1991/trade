#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt
import gzip
import json
import urllib.request

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


OUT = "output/pdf/长鑫存储产业链全受益链炒作方案.pdf"
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"


SECTIONS = [
    {
        "name": "参股与合肥国资情绪",
        "trade": "题材启动、含鑫量弹性、短线情绪观察",
        "rank": "先看华安证券和合百集团，后看合肥城建、国风新材",
        "risk": "主营不在半导体，不能当产业订单兑现。",
        "stocks": [
            ("华安证券", "600909", "sh600909", "1.600909", "参股情绪", "交易映射", "合肥注册/办公"),
            ("合百集团", "000417", "sz000417", "0.000417", "低市值含鑫量", "交易映射", "合肥注册/国资"),
            ("合肥城建", "002208", "sz002208", "0.002208", "合肥国资扩散", "交易映射", "合肥注册/国资"),
            ("国风新材", "000859", "sz000859", "0.000859", "合肥国资后排", "交易映射", "合肥注册/国资"),
        ],
    },
    {
        "name": "产业高度与存储产品",
        "trade": "判断长鑫线是否从纯参股情绪升级为存储产业主线",
        "rank": "兆易创新是高度锚，江波龙和德明利看产品端弹性",
        "risk": "产品端更容易受存储价格、业绩预期和短线情绪影响。",
        "stocks": [
            ("兆易创新", "603986", "sh603986", "1.603986", "参股+存储产品", "产业核心/交易映射", "非合肥"),
            ("江波龙", "301308", "sz301308", "0.301308", "存储模组", "交易映射", "非合肥"),
            ("德明利", "001309", "sz001309", "0.001309", "存储弹性", "交易映射", "非合肥"),
            ("佰维存储", "688525", "sh688525", "1.688525", "存储情绪", "交易映射", "非合肥"),
            ("澜起科技", "688008", "sh688008", "1.688008", "内存接口芯片", "产业相关", "非合肥"),
        ],
    },
    {
        "name": "半导体设备",
        "trade": "扩产资本开支最先兑现的主线层",
        "rank": "北方华创/中微公司为中军，拓荆/盛美/华海清科为扩散确认",
        "risk": "不能把所有设备票都当长鑫订单；以设备板块共振和订单披露为准。",
        "stocks": [
            ("北方华创", "002371", "sz002371", "0.002371", "平台型设备", "产业强相关", "非合肥"),
            ("中微公司", "688012", "sh688012", "1.688012", "刻蚀设备", "产业强相关", "非合肥"),
            ("拓荆科技", "688072", "sh688072", "1.688072", "薄膜沉积", "产业强相关", "非合肥"),
            ("盛美上海", "688082", "sh688082", "1.688082", "清洗设备", "产业相关/线索", "非合肥"),
            ("华海清科", "688120", "sh688120", "1.688120", "CMP设备", "产业强相关", "非合肥"),
            ("中科飞测", "688361", "sh688361", "1.688361", "检测量测", "产业相关", "非合肥"),
            ("芯源微", "688037", "sh688037", "1.688037", "涂胶显影", "产业相关", "非合肥"),
            ("精智达", "688627", "sh688627", "1.688627", "存储测试", "产业线索", "非合肥"),
            ("京仪装备", "688652", "sh688652", "1.688652", "温控设备", "产业线索", "非合肥"),
        ],
    },
    {
        "name": "材料与电子化学品",
        "trade": "设备确认后的第二层，核心看耗材国产替代和产线放量",
        "rank": "安集科技/雅克科技为材料核心，江化微/鼎龙/中船特气做扩散",
        "risk": "客户认证、供货品类、供货比例和收入贡献必须二次核验。",
        "stocks": [
            ("安集科技", "688019", "sh688019", "1.688019", "CMP抛光液", "产业强相关/线索", "非合肥"),
            ("雅克科技", "002409", "sz002409", "0.002409", "前驱体材料", "产业强相关/线索", "非合肥"),
            ("江化微", "603078", "sh603078", "1.603078", "湿电子化学品", "产业线索", "非合肥"),
            ("鼎龙股份", "300054", "sz300054", "0.300054", "CMP抛光垫", "产业线索", "非合肥"),
            ("中船特气", "688146", "sh688146", "1.688146", "电子特气", "产业相关/线索", "非合肥"),
            ("金宏气体", "688106", "sh688106", "1.688106", "电子特气", "产业相关/线索", "非合肥"),
            ("广钢气体", "688548", "sh688548", "1.688548", "电子特气", "产业相关/线索", "非合肥"),
            ("晶瑞电材", "300655", "sz300655", "0.300655", "电子化学品", "产业相关/线索", "非合肥"),
        ],
    },
    {
        "name": "封测、模组与代理",
        "trade": "产业扩散层，适合看强度和弹性，不应排在设备材料之前",
        "rank": "通富微电看长鑫/合肥封测扩散，长电科技看封测整体风险偏好，江波龙/德明利看模组产品端",
        "risk": "封测和模组受景气周期、客户结构、存储价格影响大。",
        "stocks": [
            ("通富微电", "002156", "sz002156", "0.002156", "封测/先进封装", "产业相关/扩散", "合肥生产基地"),
            ("长电科技", "600584", "sh600584", "1.600584", "封测龙头/先进封装", "泛封测中军", "非合肥"),
            ("华天科技", "002185", "sz002185", "0.002185", "封测", "产业相关/扩散", "非合肥"),
            ("深科技", "000021", "sz000021", "0.000021", "存储封测/代工", "产业线索", "合肥沛顿/双基地"),
            ("汇成股份", "688403", "sh688403", "1.688403", "封测", "产业线索", "合肥注册"),
            ("颀中科技", "688352", "sh688352", "1.688352", "封测/显示驱动", "合肥生态映射", "合肥注册"),
            ("商络电子", "300975", "sz300975", "0.300975", "代理", "交易映射", "非合肥"),
            ("中电港", "001287", "sz001287", "0.001287", "代理平台", "交易映射", "非合肥"),
            ("力源信息", "300184", "sz300184", "0.300184", "代理", "交易映射", "非合肥"),
        ],
    },
    {
        "name": "洁净室、厂务与合肥半导体生态",
        "trade": "后排扩散层，适合题材发酵后的补涨和工程订单线索",
        "rank": "柏诚/亚翔/深桑达/正帆看厂务，晶合/芯碁看合肥半导体生态",
        "risk": "工程订单弹性和半导体主线强度相关，容易后排轮动。",
        "stocks": [
            ("柏诚股份", "601133", "sh601133", "1.601133", "洁净室工程", "产业线索", "项目线索"),
            ("亚翔集成", "603929", "sh603929", "1.603929", "洁净室工程", "产业线索", "项目线索"),
            ("深桑达A", "000032", "sz000032", "0.000032", "洁净室/厂务", "产业线索", "项目线索"),
            ("正帆科技", "688596", "sh688596", "1.688596", "高纯工艺系统", "产业线索", "项目线索"),
            ("晶合集成", "688249", "sh688249", "1.688249", "合肥晶圆制造", "生态映射", "合肥注册"),
            ("芯碁微装", "688630", "sh688630", "1.688630", "合肥设备", "生态映射", "合肥注册"),
            ("皖仪科技", "688600", "sh688600", "1.688600", "仪器检测", "合肥生态映射", "合肥注册"),
        ],
    },
]


HEFEI_BONUS = [
    ("硬合肥本地", "华安证券、合百集团、合肥城建、国风新材、晶合集成、芯碁微装、汇成股份、皖仪科技、颀中科技", "注册地址或办公地址在合肥，适合作为合肥本地/合肥半导体生态加分。"),
    ("合肥子公司/基地", "通富微电、深科技", "通富微电F10显示在南通、合肥、厦门、苏州、马来西亚槟城拥有生产基地；深科技F10显示深圳、合肥半导体封测双基地，合肥沛顿为重要线索。"),
    ("项目线索加分", "柏诚股份、亚翔集成、深桑达A、正帆科技", "不是合肥本地股，但在洁净室、厂务、高纯工艺系统等方向可按长鑫/合肥项目线索观察。"),
    ("无合肥加分但产业优先", "兆易创新、北方华创、中微公司、安集科技、雅克科技、长电科技", "前五名主要由产业距离和扩产受益决定；长电科技虽无合肥属性，但可作为封测整体风险偏好锚。"),
]


def fetch_json(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0", "Accept-Encoding": "gzip", "Referer": "https://quote.eastmoney.com/"})
    with urllib.request.urlopen(req, timeout=18) as resp:
        raw = resp.read()
        if resp.headers.get("Content-Encoding") == "gzip":
            raw = gzip.decompress(raw)
    return json.loads(raw.decode("utf-8", errors="ignore"))


def em_quote(secid):
    fields = "f43,f58,f60,f116,f162,f167,f170"
    data = fetch_json(f"https://push2.eastmoney.com/api/qt/stock/get?secid={secid}&fields={fields}&ut=fa5fd1943c7b386f172d6893dbfba10b").get("data") or {}
    div100 = lambda x: None if x in (None, "-") else x / 100
    div1e8 = lambda x: None if x in (None, "-") else x / 100000000
    return {"price": div100(data.get("f43")), "prev": div100(data.get("f60")), "mcap": div1e8(data.get("f116")), "pe": div100(data.get("f162")), "pb": div100(data.get("f167")), "pct": div100(data.get("f170"))}


def sina_quote(sina):
    req = urllib.request.Request(f"https://hq.sinajs.cn/list={sina}", headers={"User-Agent": "Mozilla/5.0", "Referer": "https://finance.sina.com.cn/"})
    with urllib.request.urlopen(req, timeout=18) as resp:
        text = resp.read().decode("gbk", errors="ignore")
    raw = text.split('"')[1].split(",")
    return {"price": float(raw[3]), "prev": float(raw[2]), "date": raw[30], "time": raw[31]}


def fmt(x, suffix=""):
    if x is None:
        return "-"
    return f"{x:.2f}{suffix}"


def esc(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def p(text, style):
    return Paragraph(esc(text), style)


def collect():
    out = []
    for sec in SECTIONS:
        for name, code, sina, secid, role, level, hefei in sec["stocks"]:
            em = em_quote(secid)
            sq = sina_quote(sina)
            if abs((em.get("price") or 0) - sq["price"]) > 0.02:
                raise RuntimeError(f"行情不一致: {name} {code} Eastmoney={em.get('price')} Sina={sq['price']}")
            out.append({
                "section": sec["name"], "name": name, "code": code, "role": role, "level": level,
                "hefei": hefei,
                "price": em["price"], "pct": em["pct"], "mcap": em["mcap"], "pe": em["pe"], "date": sq["date"], "time": sq["time"],
            })
    return out


def build(rows):
    pdfmetrics.registerFont(TTFont("CN", FONT))
    doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=1.3 * cm, rightMargin=1.3 * cm, topMargin=1.25 * cm, bottomMargin=1.15 * cm)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("TitleCN", fontName="CN", fontSize=19, leading=26, alignment=TA_CENTER, spaceAfter=10))
    styles.add(ParagraphStyle("H1CN", fontName="CN", fontSize=13.5, leading=19, spaceBefore=10, spaceAfter=6, textColor=colors.HexColor("#1f4e79")))
    styles.add(ParagraphStyle("BodyCN", fontName="CN", fontSize=9.2, leading=14, alignment=TA_LEFT, spaceAfter=4))
    styles.add(ParagraphStyle("SmallCN", fontName="CN", fontSize=7.5, leading=10.5, alignment=TA_LEFT))
    styles.add(ParagraphStyle("CellCN", fontName="CN", fontSize=6.8, leading=9.5, alignment=TA_LEFT))
    styles.add(ParagraphStyle("HeadCN", fontName="CN", fontSize=7, leading=9.5, alignment=TA_CENTER, textColor=colors.white))
    story = []
    story.append(p("长鑫存储产业链全受益链炒作方案", styles["TitleCN"]))
    story.append(p(f"生成日期：{dt.date.today().isoformat()}；行情复核：东方财富 + 新浪双源收盘价一致；用途：A股交易研究，不构成投资建议。", styles["SmallCN"]))
    story.append(Spacer(1, 6))
    story.append(p("一、复核结论", styles["H1CN"]))
    story.append(p("本次复核后，最受益 5 家公司维持修正版：兆易创新、北方华创、中微公司、安集科技、雅克科技。通富微电不再列入前五，原因是上一版“合肥控股背景”表述不准确；它应放在封测/先进封装扩散层观察。", styles["BodyCN"]))
    story.append(p("硬数据口径：本报告所有表格中的现价、涨跌幅、总市值、PE来自东方财富行情，并用新浪行情逐一核对收盘价。产业链关系口径：无法公告级确认的长鑫客户/供货关系，只写为产业线索或交易映射。", styles["BodyCN"]))
    story.append(p("合肥属性口径：合肥本地或有合肥子公司/基地是加分项，不是替代产业逻辑的主因。前五名仍看产业受益；同一层级里，合肥注册、合肥基地、合肥项目线索可提高盘中辨识度。", styles["BodyCN"]))
    story.append(p("二、总炒作路径", styles["H1CN"]))
    story.append(p("长鑫线不是一条直线，而是从情绪到产业、再到后排扩散的链条：参股含鑫量 -> 兆易创新/存储产品 -> 半导体设备 -> 材料和电子化学品 -> 封测/模组/代理 -> 洁净室厂务和合肥生态。真正能走成主线，必须看到兆易创新、设备中军、材料中军和封测产品端共振。", styles["BodyCN"]))
    story.append(p("三、核心观察顺序", styles["H1CN"]))
    table = [[p(x, styles["HeadCN"]) for x in ["顺序", "阶段", "核心观察", "交易含义", "风险"]]]
    for i, sec in enumerate(SECTIONS, 1):
        table.append([p(i, styles["CellCN"]), p(sec["name"], styles["CellCN"]), p(sec["rank"], styles["CellCN"]), p(sec["trade"], styles["CellCN"]), p(sec["risk"], styles["CellCN"])])
    t = Table(table, colWidths=[0.8 * cm, 3.0 * cm, 4.4 * cm, 4.2 * cm, 3.3 * cm], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")), ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#b7c9d8")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fbfd"))]))
    story.append(t)
    story.append(p("四、合肥属性加分清单", styles["H1CN"]))
    htable = [[p(x, styles["HeadCN"]) for x in ["加分类别", "涉及公司", "使用方式"]]]
    for row in HEFEI_BONUS:
        htable.append([p(row[0], styles["CellCN"]), p(row[1], styles["CellCN"]), p(row[2], styles["CellCN"])])
    ht = Table(htable, colWidths=[2.4 * cm, 6.2 * cm, 6.8 * cm], repeatRows=1)
    ht.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")), ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#b7c9d8")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fbfd"))]))
    story.append(ht)
    story.append(p("长电科技与通富微电的封测排序", styles["H1CN"]))
    story.append(p("长电科技是封测综合龙头和先进封装中军，F10显示注册/办公在江苏江阴，在封测整体、先进封装、AI封装行情里可能强于通富微电。但长鑫/合肥单线里，通富微电F10显示拥有合肥生产基地，更容易被资金归入长鑫/合肥封测承接，所以通富微电在长鑫/合肥扩散层优先级高于长电科技。", styles["BodyCN"]))
    story.append(p("简单说：炒封测整体看长电科技，炒长鑫 + 合肥封测扩散看通富微电。二者都属于封测扩散层，不能越级替代兆易创新、设备和材料核心。", styles["BodyCN"]))
    story.append(PageBreak())
    story.append(p("五、全链路股票池与行情复核", styles["H1CN"]))
    for sec in SECTIONS:
        story.append(p(sec["name"], styles["H1CN"]))
        story.append(p(f"炒作定位：{sec['trade']}。排序：{sec['rank']}。风险：{sec['risk']}", styles["BodyCN"]))
        data = [[p(x, styles["HeadCN"]) for x in ["公司", "代码", "角色", "关系等级", "合肥属性", "现价", "涨跌幅", "总市值"]]]
        for r in [x for x in rows if x["section"] == sec["name"]]:
            data.append([p(r["name"], styles["CellCN"]), p(r["code"], styles["CellCN"]), p(r["role"], styles["CellCN"]), p(r["level"], styles["CellCN"]), p(r["hefei"], styles["CellCN"]), p(fmt(r["price"]), styles["CellCN"]), p(fmt(r["pct"], "%"), styles["CellCN"]), p(fmt(r["mcap"], "亿"), styles["CellCN"])])
        tt = Table(data, colWidths=[1.55 * cm, 1.25 * cm, 2.6 * cm, 2.0 * cm, 2.25 * cm, 1.15 * cm, 1.1 * cm, 1.55 * cm], repeatRows=1)
        tt.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f4e79")), ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#b7c9d8")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
        story.append(tt)
    story.append(PageBreak())
    story.append(p("六、盘中交易方案", styles["H1CN"]))
    rules = [
        ("情绪启动", "华安证券/合百集团先动，但兆易创新、设备、材料不动。处理：只按情绪套利，不把后排当产业主线追。"),
        ("产业确认", "兆易创新强，北方华创/中微公司同步强。处理：长鑫线从参股情绪升级为产业观察，优先看设备中军。"),
        ("主线共振", "兆易创新 + 北方华创/中微公司 + 安集科技/雅克科技 + 封测/模组至少一组跟随。处理：才有主线资格，可以围绕核心低吸或分歧转强。封测里长鑫/合肥扩散优先看通富微电，封测整体风险偏好看长电科技。"),
        ("合肥加分", "同一层级内优先看合肥注册、合肥基地、合肥子公司线索，例如汇成股份、颀中科技、晶合集成、芯碁微装、通富微电、深科技。处理：加分但不越级。"),
        ("后排扩散", "洁净室、代理、合肥生态开始补涨。处理：只能做强度确认后的低位轮动，不可替代核心。"),
        ("失败信号", "参股股冲高回落，兆易创新不强，设备材料走弱。处理：长鑫线退回情绪题材，降低仓位，避免追后排。"),
    ]
    for title, body in rules:
        story.append(p(f"{title}：{body}", styles["BodyCN"]))
    story.append(p("七、仓位与风控", styles["H1CN"]))
    story.append(p("核心仓只考虑产业确认后的前五和设备材料中军；弹性仓看江波龙、德明利、通富微电、长电科技、华天科技、深科技、汇成股份、颀中科技等扩散。长电科技用于观察封测整体风险偏好，通富微电用于观察长鑫/合肥封测扩散。情绪仓只做华安证券、合百集团等前排。合肥属性只在同一层级内加分，不能让后排票越级替代核心票。", styles["BodyCN"]))
    story.append(p("资料来源：东方财富行情/F10、新浪行情、本地交易研究文档《2026-06-24 二长产业链炒作思路与核心股》《2026-06-25 合肥本地与长鑫相关 A 股梳理》。客户关系、供货比例、订单规模需继续以公司公告、年报、招股书、互动易或监管披露为准。", styles["SmallCN"]))

    def footer(canvas, doc_obj):
        canvas.saveState()
        canvas.setFont("CN", 8)
        canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawCentredString(A4[0] / 2, 0.6 * cm, f"第 {doc_obj.page} 页")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    rows = collect()
    build(rows)
    print(OUT)
