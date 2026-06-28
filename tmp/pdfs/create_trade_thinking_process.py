#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime as dt

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


OUT = "output/pdf/单笔股票交易系统思考流程.pdf"
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"


def esc(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def p(text, style):
    return Paragraph(esc(text), style)


def add_table(story, styles, headers, rows, widths, header_color="#1f4e79"):
    data = [[p(x, styles["HeadCN"]) for x in headers]]
    for row in rows:
        data.append([p(x, styles["CellCN"]) for x in row])
    t = Table(data, colWidths=widths, repeatRows=1)
    t.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(header_color)),
                ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#b7c9d8")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#f8fbfd")),
            ]
        )
    )
    story.append(t)


def build():
    pdfmetrics.registerFont(TTFont("CN", FONT))
    doc = SimpleDocTemplate(
        OUT,
        pagesize=A4,
        leftMargin=1.25 * cm,
        rightMargin=1.25 * cm,
        topMargin=1.2 * cm,
        bottomMargin=1.1 * cm,
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("TitleCN", fontName="CN", fontSize=19, leading=26, alignment=TA_CENTER, spaceAfter=10))
    styles.add(ParagraphStyle("H1CN", fontName="CN", fontSize=13.5, leading=19, spaceBefore=9, spaceAfter=6, textColor=colors.HexColor("#1f4e79")))
    styles.add(ParagraphStyle("BodyCN", fontName="CN", fontSize=9.2, leading=14, alignment=TA_LEFT, spaceAfter=4))
    styles.add(ParagraphStyle("SmallCN", fontName="CN", fontSize=7.6, leading=10.5, alignment=TA_LEFT))
    styles.add(ParagraphStyle("CellCN", fontName="CN", fontSize=6.9, leading=9.7, alignment=TA_LEFT))
    styles.add(ParagraphStyle("HeadCN", fontName="CN", fontSize=7.2, leading=9.8, alignment=TA_CENTER, textColor=colors.white))

    story = []
    story.append(p("单笔股票交易系统思考流程", styles["TitleCN"]))
    story.append(p(f"生成日期：{dt.date.today().isoformat()}；用途：A股个人交易前、中、后全过程检查；结论不构成投资建议。", styles["SmallCN"]))
    story.append(Spacer(1, 6))

    story.append(p("一、总原则", styles["H1CN"]))
    story.append(p("一笔交易不是从“这只票会不会涨”开始，而是从“当前市场允不允许我下注”开始。系统思考的目的不是预测涨跌，而是识别环境、等待优势、定义亏损、跟随确认、复盘修正。", styles["BodyCN"]))
    story.append(p("核心公式：市场状态 -> 仓位上限 -> 资金路径 -> 题材级别 -> 核心锚点 -> 个股强弱 -> 买点与止损 -> 盘中验证 -> 退出与复盘。", styles["BodyCN"]))

    story.append(p("二、完整思考链路", styles["H1CN"]))
    add_table(
        story,
        styles,
        ["顺序", "问题", "判断方法", "通过标准", "不通过动作"],
        [
            ("1", "市场能不能做？", "看指数、成交额、上涨家数、跌停/炸板、核心锚点。", "不是退潮，或退潮中只允许小仓试错。", "降仓、空仓、只观察。"),
            ("2", "仓位应该多大？", "按市场状态定上限，不按情绪定。", "退潮0-20%，弱抱团20-40%，放量修复40-65%，主升65-85%。", "任何超出仓位上限的交易都取消。"),
            ("3", "钱正往哪里去？", "看高低切、旧主线留存、新方向承接、容量锚主动性。", "资金路径清楚，且不是单日随机脉冲。", "不买后排，不追单点异动。"),
            ("4", "题材是不是够级别？", "拆产业逻辑、事件催化、业绩/涨价/政策/订单、持续时间。", "能解释资金为什么今天愿意定价。", "只按观察题材，不给重仓资格。"),
            ("5", "谁是核心锚？", "找容量锚、逻辑锚、情绪锚、补涨锚。", "至少一个容量锚主动走强，前排有承接。", "没有核心锚，只能小仓或不做。"),
            ("6", "这只票是不是阻力最小？", "比较同板块强弱、合肥/地方/客户/产品纯度、位置和量能。", "强于板块，强于同类，有辨识度。", "换到核心，或放弃后排。"),
            ("7", "买点是否清楚？", "低吸、分歧转强、突破确认、回踩不破分别定义。", "买点、止损点、验证点三者同时清楚。", "没有计划不下单。"),
            ("8", "错了亏多少？", "先按止损价和仓位计算最大亏损。", "单笔亏损在纪律线内。", "缩小仓位或取消。"),
            ("9", "盘中如何验证？", "看核心锚、板块梯队、成交额、分时承接、炸板反馈。", "买入理由继续成立，或分歧后有承接。", "减仓、止损、禁止补仓讲故事。"),
            ("10", "什么时候卖？", "逻辑证伪、锚点转弱、跌破验证线、仓位失控、盈利兑现。", "卖出规则提前写好。", "临盘不临时改长线。"),
        ],
        [0.75 * cm, 2.45 * cm, 4.2 * cm, 4.0 * cm, 3.3 * cm],
    )

    story.append(PageBreak())
    story.append(p("三、市场状态与仓位", styles["H1CN"]))
    add_table(
        story,
        styles,
        ["市场状态", "识别特征", "仓位上限", "适合动作", "禁止动作"],
        [
            ("退潮/缩量抢流动性", "指数弱、广度差、炸板多、核心锚转弱、热点轮动快。", "0%-20%", "空仓、观察、极小仓试错。", "追高、补跌股、重仓后排。"),
            ("弱抱团/局部轮动", "指数一般，但强势股集中在少数方向。", "20%-40%", "只做前排、容量锚、辨识度。", "铺多个题材、买边缘票。"),
            ("放量修复/低位反弹", "成交额改善，核心不弱，强势方向能分歧修复。", "40%-65%", "主攻阻力最小方向，核心加一阶扩散。", "追最末端补涨。"),
            ("主升/确认上升周期", "指数题材共振，容量锚持续强，分歧后快速修复。", "65%-85%", "集中主线核心，分歧不破可加仓。", "随意换股、满仓情绪化。"),
        ],
        [2.5 * cm, 4.5 * cm, 1.8 * cm, 3.7 * cm, 3.3 * cm],
    )

    story.append(p("四、题材拆解模板", styles["H1CN"]))
    add_table(
        story,
        styles,
        ["维度", "要问的问题", "好的答案", "风险信号"],
        [
            ("主因", "这次上涨的真正原因是什么？", "政策、涨价、订单、业绩、扩产、国产替代等能说清楚。", "只是名字联想或消息脉冲。"),
            ("资金路径", "钱从哪里来，往哪里去？", "旧主线分歧后有明确承接方向，或主线内部有序扩散。", "多方向随机拉，缺少持续性。"),
            ("产业层级", "它处在产业链哪个环节？", "上游设备/材料、中游制造、下游封测/模组分层清楚。", "只买板块名，不知道公司赚什么钱。"),
            ("核心锚点", "谁决定题材强弱？", "容量锚、逻辑锚、情绪锚都能列出来。", "只有小票涨，没有中军确认。"),
            ("交易阶段", "题材是启动、确认、分歧、修复还是退潮？", "阶段清楚，对应买法清楚。", "退潮时当启动，高潮后追后排。"),
            ("持续验证", "明天/下周要看什么？", "有具体锚点、价格、量能、板块反馈。", "只说看好，没有验证条件。"),
        ],
        [2.0 * cm, 4.0 * cm, 5.2 * cm, 4.2 * cm],
    )

    story.append(p("五、个股选择模板", styles["H1CN"]))
    add_table(
        story,
        styles,
        ["维度", "核心问题", "优先选择", "降级对象"],
        [
            ("辨识度", "市场一说这个方向，会不会先想到它？", "中军、龙头、前排、容量票。", "后排、跟风、名字相似。"),
            ("产业纯度", "公司业务与题材是否真的相关？", "主营、客户、订单、产品环节能对应。", "只有互动易模糊回复。"),
            ("位置阻力", "上涨空间是否被套牢盘压制？", "横盘突破、低位转强、主线分歧不破。", "高位加速后追涨。"),
            ("量能承接", "买盘是否主动？", "放量上涨、缩量回踩、分歧后承接。", "拉高无量、冲高回落。"),
            ("同类比较", "它比同板块谁更强？", "强于板块、强于同分支，回调更抗跌。", "板块涨它不涨，板块跌它先跌。"),
            ("可退出性", "错了能不能卖？", "流动性足、止损位清楚。", "成交差、T+1下容易被闷。"),
        ],
        [2.0 * cm, 4.0 * cm, 4.8 * cm, 4.8 * cm],
    )

    story.append(PageBreak())
    story.append(p("六、买入前必须写清楚的计划", styles["H1CN"]))
    add_table(
        story,
        styles,
        ["项目", "必须写出的内容", "示例"],
        [
            ("买入理由", "至少三条：市场状态、资金路径、个股强度。", "放量修复；半导体设备材料共振；个股强于同类。"),
            ("买点类型", "低吸、分歧转强、突破确认、回踩不破。", "10:00后回踩均线不破，核心锚继续红盘。"),
            ("验证点", "买入后哪些现象证明我对？", "板块中军不弱，成交额维持，前排不炸。"),
            ("证伪点", "哪些现象证明我错？", "核心锚翻绿，个股跌破昨日低点，板块冲高回落。"),
            ("止损价", "明确价格或条件止损。", "跌破验证线减半，跌破止损线清仓。"),
            ("仓位", "占总仓多少，单笔最多亏多少。", "试错5%-10%，确认15%-25%，单笔亏损不超纪律线。"),
            ("持有周期", "日内、隔日、波段，不能临时改。", "隔日验证，不符合预期第二天处理。"),
        ],
        [2.4 * cm, 6.0 * cm, 6.6 * cm],
    )

    story.append(p("七、盘中执行流程", styles["H1CN"]))
    add_table(
        story,
        styles,
        ["时间", "观察重点", "允许动作", "禁止动作"],
        [
            ("竞价", "高开兑现、低开承接、核心锚态度、量能预期。", "只观察，记录强弱。", "因为竞价强就冲动买。"),
            ("9:30-10:00", "谁能承接兑现，谁能主动修复，谁是假强。", "小仓试错或等待确认。", "追缩量后排。"),
            ("10:00-11:00", "胜出主线是否清楚，容量锚是否确认。", "确认后按计划买核心。", "在多个题材里乱切。"),
            ("午后", "成交额是否维持，2点后是否抢流动性。", "良性分歧做T或持有。", "缩量后继续追高。"),
            ("尾盘", "是否符合隔日持仓条件。", "保留强票，处理弱票。", "为了赌明天强行留弱票。"),
        ],
        [2.1 * cm, 5.0 * cm, 4.3 * cm, 4.2 * cm],
    )

    story.append(p("八、卖出与风控", styles["H1CN"]))
    add_table(
        story,
        styles,
        ["卖出类型", "触发条件", "处理方式"],
        [
            ("逻辑证伪", "买入主因消失，题材不再被资金定价。", "不补仓，直接减仓或清仓。"),
            ("锚点转弱", "容量锚、情绪锚、板块中军明显转弱。", "先降仓，再观察是否修复。"),
            ("个股弱于同类", "板块强它不强，板块弱它先跌。", "视为弱票，不讲故事。"),
            ("跌破验证线", "跌破买前定义的价格或结构。", "按计划执行，不临时改长线。"),
            ("盈利保护", "高潮、放量滞涨、后排补涨、核心分歧加大。", "分批兑现，保留最强核心。"),
            ("情绪失控", "亏损想扳回、卖飞想追回、空仓焦虑。", "停止交易，离开界面，写复盘。"),
        ],
        [2.8 * cm, 6.4 * cm, 6.2 * cm],
    )

    story.append(PageBreak())
    story.append(p("九、不同机会的适配方式", styles["H1CN"]))
    add_table(
        story,
        styles,
        ["机会类型", "主要看什么", "适合仓位", "关键风险"],
        [
            ("主线核心分歧转强", "大盘支持、容量锚不弱、核心回踩后主动修复。", "中高仓", "误把反抽当二波。"),
            ("低位新方向承接", "高位资金松动，新故事有容量票确认。", "中仓试错", "只有消息没有承接。"),
            ("业绩/涨价", "价格、订单、业绩预期、财报验证。", "中仓", "兑现后追高。"),
            ("超跌反弹", "历史辨识度、横盘放量、板块修复。", "小中仓", "弱反弹当反转。"),
            ("后排补涨", "核心已经确认，后排低位跟随。", "小仓", "主线分歧时后排先跌。"),
            ("情绪参股/概念", "前排强度、情绪连板、题材扩散。", "小仓快进快出", "把情绪票当产业核心。"),
        ],
        [3.1 * cm, 5.0 * cm, 2.2 * cm, 5.0 * cm],
    )

    story.append(p("十、交易后复盘模板", styles["H1CN"]))
    add_table(
        story,
        styles,
        ["复盘问题", "记录内容"],
        [
            ("这笔交易属于什么模式？", "主线核心、低位承接、业绩涨价、超跌反弹、后排补涨、情绪套利。"),
            ("买入前计划是否完整？", "有没有写清买点、止损、验证点、仓位、持有周期。"),
            ("市场状态判断对不对？", "大盘、成交额、广度、核心锚是否按预期走。"),
            ("个股是不是核心？", "是否强于板块，是否是容量锚/逻辑锚/情绪锚。"),
            ("执行是否变形？", "有没有追高、补仓、临时改计划、亏损后乱动。"),
            ("结果归因是什么？", "赚钱是模式正确还是运气；亏钱是环境错、选股错、买点错、仓位错还是执行错。"),
            ("下次如何改？", "沉淀一条可执行规则，而不是只写情绪。"),
        ],
        [4.0 * cm, 11.0 * cm],
    )

    story.append(p("十一、一页式交易清单", styles["H1CN"]))
    checklist = [
        "1. 大盘状态：退潮、弱抱团、放量修复、主升，属于哪一种？",
        "2. 仓位上限：今天最多允许几成仓？是否已超限？",
        "3. 资金路径：钱在旧主线、新方向、低位、业绩、涨价还是情绪？",
        "4. 题材级别：是主线、分支、轮动、补涨还是纯情绪？",
        "5. 核心锚点：容量锚、逻辑锚、情绪锚分别是谁？",
        "6. 个股地位：它是核心还是后排？强于同类还是弱于同类？",
        "7. 买点类型：低吸、转强、突破、回踩，哪一种？",
        "8. 止损条件：跌到哪里走？什么情况说明逻辑错？",
        "9. 仓位金额：这笔最多亏多少？是否符合纪律？",
        "10. 盘中验证：10点、午后、尾盘分别看什么？",
        "11. 卖出计划：盈利怎么卖，亏损怎么卖，隔日怎么处理？",
        "12. 情绪检查：这笔是计划内交易，还是手痒、卖飞、亏损后的冲动？",
    ]
    for item in checklist:
        story.append(p(item, styles["BodyCN"]))

    story.append(p("最终纪律", styles["H1CN"]))
    story.append(p("写不出三条买入理由，不买；算不清最大亏损，不买；没有核心锚点，不重仓；跌破证伪点，不讲故事；市场不给机会，空仓也是交易。", styles["BodyCN"]))

    def footer(canvas, doc_obj):
        canvas.saveState()
        canvas.setFont("CN", 8)
        canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawCentredString(A4[0] / 2, 0.58 * cm, f"第 {doc_obj.page} 页")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
    print(OUT)
