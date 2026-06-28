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


OUT = "output/pdf/大盘当日与隔日走势预判系统思考流程.pdf"
FONT = "/System/Library/Fonts/STHeiti Medium.ttc"


def esc(text):
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def p(text, style):
    return Paragraph(esc(text), style)


def table(story, styles, headers, rows, widths):
    data = [[p(x, styles["HeadCN"]) for x in headers]]
    for row in rows:
        data.append([p(x, styles["CellCN"]) for x in row])
    t = Table(data, colWidths=widths, repeatRows=1)
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


def build():
    pdfmetrics.registerFont(TTFont("CN", FONT))
    doc = SimpleDocTemplate(
        OUT,
        pagesize=A4,
        leftMargin=1.22 * cm,
        rightMargin=1.22 * cm,
        topMargin=1.15 * cm,
        bottomMargin=1.05 * cm,
    )
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle("TitleCN", fontName="CN", fontSize=18.5, leading=25, alignment=TA_CENTER, spaceAfter=10))
    styles.add(ParagraphStyle("H1CN", fontName="CN", fontSize=13.2, leading=18.5, spaceBefore=8, spaceAfter=5, textColor=colors.HexColor("#1f4e79")))
    styles.add(ParagraphStyle("BodyCN", fontName="CN", fontSize=9.0, leading=13.6, alignment=TA_LEFT, spaceAfter=4))
    styles.add(ParagraphStyle("SmallCN", fontName="CN", fontSize=7.4, leading=10.2, alignment=TA_LEFT))
    styles.add(ParagraphStyle("CellCN", fontName="CN", fontSize=6.75, leading=9.2, alignment=TA_LEFT))
    styles.add(ParagraphStyle("HeadCN", fontName="CN", fontSize=7.05, leading=9.4, alignment=TA_CENTER, textColor=colors.white))

    story = []
    story.append(p("大盘当日与隔日走势预判系统思考流程", styles["TitleCN"]))
    story.append(p(f"生成日期：{dt.date.today().isoformat()}；用途：盘后复盘、隔日预案、盘中验证；结论不构成投资建议。", styles["SmallCN"]))
    story.append(Spacer(1, 6))

    story.append(p("一、总原则", styles["H1CN"]))
    story.append(p("大盘和隔日预判不是猜明天涨跌，而是回答：今天市场选择了什么，明天最需要验证什么；验证通过怎么做，验证失败怎么退。", styles["BodyCN"]))
    story.append(p("核心公式：当日定性 -> 指数与量能 -> 主线锚点 -> 资金路径 -> 题材轮动 -> 隔日剧本 -> 仓位动作 -> 次日盘中验证。", styles["BodyCN"]))

    story.append(p("二、当日盘面定性", styles["H1CN"]))
    table(
        story,
        styles,
        ["盘面状态", "典型特征", "隔日核心问题", "仓位倾向"],
        [
            ("强修复", "指数收强，核心锚点修复，成交额改善，前排有承接。", "明天是延续还是高开兑现？分歧后谁能留下？", "中等偏积极，不追高潮。"),
            ("二次走强", "上午确认方向，午后继续有强方向，容量锚配合。", "明天高开后是否还能承接？是否进入高潮透支？", "保留核心，后排降级。"),
            ("分歧承接", "主线回落但核心不破，前排有承接，后排分化。", "明天核心是否修复？弱票是否继续补跌？", "去弱留强，等确认。"),
            ("高位分化", "核心尚可，后排冲高回落或补跌，赚钱效应收窄。", "资金是留在核心，还是开始找低位承接？", "降低后排，保留核心。"),
            ("放量轮动", "成交够，但方向多，国产链、海外链、非科技轮动。", "谁能经得住隔日淘汰？是否有容量锚确认？", "只做胜出方向。"),
            ("缩量抢流动性", "午后量能跟不上，后排乱拉，炸板增多。", "明天是否退潮？是否需要先防守？", "降低仓位。"),
            ("系统性杀跌", "指数和主线核心一起弱，跌停/大跌扩散。", "先止跌还是继续释放风险？", "空仓或极小观察仓。"),
        ],
        [2.25 * cm, 5.0 * cm, 5.2 * cm, 2.8 * cm],
    )

    story.append(p("三、指数与量能判断", styles["H1CN"]))
    table(
        story,
        styles,
        ["维度", "观察内容", "强势信号", "风险信号"],
        [
            ("指数结构", "上证、深成指、创业板、科创50谁强谁弱。", "弹性指数强，主板不拖累，风格一致。", "创业板/科创明显破位，主板护不住风险偏好。"),
            ("成交额", "两市成交额和日内量能曲线。", "早盘放量，午后不缩，2点后仍有资金进攻。", "午后急缩，后排乱拉，资金抢流动性。"),
            ("市场广度", "上涨家数、涨停数、跌停数、炸板率。", "上涨家数改善，涨停有梯队，炸板可控。", "指数红但多数票跌，炸板和大面扩散。"),
            ("风格温度", "大票、小票、20CM、北交、高位核心的反馈。", "容量锚和弹性票共振。", "小票乱涨但容量锚不动，容易假强。"),
            ("尾盘态度", "尾盘是否抢筹或抢跑。", "核心尾盘不回落，隔夜愿意留仓。", "尾盘跳水，强票回落，资金不愿隔夜。"),
        ],
        [2.2 * cm, 4.3 * cm, 4.7 * cm, 4.4 * cm],
    )

    story.append(PageBreak())
    story.append(p("四、主线锚点系统", styles["H1CN"]))
    table(
        story,
        styles,
        ["锚点类型", "作用", "看法", "隔日意义"],
        [
            ("指数锚", "判断风险偏好和风格。", "上证、创业板、科创50、北证等。", "决定仓位上限。"),
            ("量能锚", "判断能否支撑扩散。", "两市成交额、午后量能曲线。", "决定能不能多线轮动。"),
            ("容量锚", "判断大资金态度。", "方向内最大成交额中军。", "容量锚不弱，主线才有资格。"),
            ("情绪锚", "判断短线赚钱效应。", "弹性龙头、高标、20CM、连板。", "情绪锚转弱，后排先降级。"),
            ("逻辑锚", "判断产业解释是否被认可。", "最正宗产品、订单、涨价、国产替代环节。", "逻辑锚强，题材更容易延续。"),
            ("扩散锚", "判断主线是否从点到面。", "材料、设备、封测、模组、应用、下游。", "扩散有序才是主线，无序是轮动。"),
        ],
        [2.2 * cm, 3.6 * cm, 4.3 * cm, 4.7 * cm],
    )

    story.append(p("五、资金路径推演", styles["H1CN"]))
    table(
        story,
        styles,
        ["资金路径", "盘面表现", "隔日推演", "动作"],
        [
            ("主线延续", "核心锚继续强，分歧后有承接，后排有序扩散。", "明天优先看分歧承接，不追高开高潮。", "持核心，做一阶扩散。"),
            ("主线内部高低切", "高位核心钝化，低位同产业链补涨。", "看低位是否有容量锚，不把后排脉冲当新主线。", "小仓试错，确认再加。"),
            ("国产链到海外链", "当天国产替代强，海外链高位分歧或暂时休息。", "明天看海外链容量锚是否修复；若国产继续强，海外链只是轮动补充。", "先看锚点，不预设切换。"),
            ("海外链到国产链", "海外AI/CPO/PCB弱，国产半导体、材料、设备承接。", "看国产链是否有设备/材料中军确认，而非单纯避险。", "确认后做国产核心。"),
            ("科技到非科技", "科技高位回落，消费、医药、有色、金融等承接。", "非科技需容量票放量且下午站住，才是切换。", "先轻仓观察。"),
            ("轮动无主线", "多题材轮番拉升，涨幅榜很热但无中军。", "隔日容易淘汰，不能追热闹。", "空仓或只做最强核心。"),
            ("抢流动性", "缩量、后排乱拉、尾盘回落。", "隔日优先防守，看是否继续退潮。", "降仓，禁止随手单。"),
        ],
        [2.5 * cm, 4.3 * cm, 5.5 * cm, 2.9 * cm],
    )

    story.append(p("六、国产链与海外链轮动模型", styles["H1CN"]))
    story.append(p("“今天炒国产，明天是不是炒海外链”不能靠感觉判断。要先判断今天国产是主线确认、低位补涨，还是高位分歧后的避险承接；再看海外链明天有没有容量锚修复。", styles["BodyCN"]))
    table(
        story,
        styles,
        ["情景", "当天表现", "隔日判断", "操作原则"],
        [
            ("国产主线确认", "国产设备、材料、封测、核心中军共振。", "明天先看国产分歧承接，不急着切海外链。海外链只有容量锚主动修复才看。", "国产核心优先。"),
            ("国产低位补涨", "国产小票强，但设备/材料中军不够强。", "明天容易分化，海外链若容量锚修复，可能重新吸钱。", "不追国产后排。"),
            ("海外链高位分歧", "CPO/PCB/AI硬件高位回落，国产链承接。", "看海外链是否只是良性分歧；若核心不破，海外链可能回流。", "两手准备。"),
            ("海外链退潮", "海外链容量锚破位，后排大面，资金明显流出。", "国产链若有容量锚和产业解释，才可能升级承接。", "降低海外链，验证国产。"),
            ("国产与海外共振", "半导体国产替代与海外AI硬件同时强。", "说明科技风险偏好强，隔日重点看哪个分支抗分歧。", "做最强容量锚。"),
            ("两边都弱", "国产、海外链都冲高回落或补跌。", "科技线降级，资金可能去非科技或防守。", "降仓等待。"),
        ],
        [2.4 * cm, 4.3 * cm, 5.6 * cm, 3.0 * cm],
    )

    story.append(PageBreak())
    story.append(p("七、隔日剧本模板", styles["H1CN"]))
    table(
        story,
        styles,
        ["剧本", "确认条件", "隔日动作", "风险提示"],
        [
            ("A 强修复延续", "指数继续强，核心锚不杀，成交额支撑扩散。", "保留核心，适度提高仓位，只做核心和一阶扩散。", "不追高开高潮。"),
            ("B 高开兑现但承接强", "高开回落但10:30前无恐慌，核心锚不同时转弱。", "等待分歧承接，低吸强核心或做T。", "弱票先处理。"),
            ("C 分歧扩大", "核心锚翻绿，后排大面积回落，炸板增多。", "降后排，保现金，核心也要减。", "不要补仓讲故事。"),
            ("D 新方向承接", "旧主线弱，新方向有容量票放量且下午站住。", "小仓试错新方向，隔日抗跌再提高。", "承接没确认前不是新主线。"),
            ("E 缩量轮动", "指数小涨但成交不足，题材切很快。", "只看最强前排，仓位保持低。", "别在涨幅榜里乱切。"),
            ("F 系统性风险", "指数破位，核心补跌，涨停少跌停多。", "空仓或极小观察仓，等待止跌。", "不要接飞刀。"),
        ],
        [2.5 * cm, 5.1 * cm, 4.5 * cm, 3.2 * cm],
    )

    story.append(p("八、盘中时间验证", styles["H1CN"]))
    table(
        story,
        styles,
        ["时间", "观察内容", "判断重点", "动作"],
        [
            ("9:25竞价", "核心锚、昨日强票、新方向、外围消息。", "高开是否透支，低开是否低于预期。", "只观察，不急下结论。"),
            ("9:30-10:00", "高开兑现、低开修复、板块强度保留。", "谁被淘汰，谁主动修复。", "不追后排，等胜出方向。"),
            ("10:00-10:30", "指数风格、容量锚、新方向共振。", "第一次定性今天主线。", "看清后再开仓。"),
            ("11:00前", "前排承接、后排强弱、量能是否缩。", "上午强度是否真实。", "弱票先处理。"),
            ("13:30-14:30", "午后是否继续放量，是否二次走强。", "资金愿不愿意继续进攻。", "确认强线，降低弱线。"),
            ("尾盘", "隔夜意愿、尾盘抢筹或抢跑。", "强度是否透支明天。", "决定隔夜仓位。"),
        ],
        [2.1 * cm, 4.4 * cm, 4.5 * cm, 4.0 * cm],
    )

    story.append(p("九、隔日预案写法", styles["H1CN"]))
    table(
        story,
        styles,
        ["模块", "必须写清楚"],
        [
            ("当日定性", "今天是强修复、分歧承接、高位分化、放量轮动、缩量退潮还是系统性杀跌。"),
            ("核心锚点", "指数锚、量能锚、容量锚、情绪锚、逻辑锚分别是谁。"),
            ("资金路径", "钱是留在原主线，内部高低切，国产/海外链切换，还是流向非科技。"),
            ("明日剧本", "至少写A/B/C三种：延续、分歧、失败，每种对应动作。"),
            ("仓位计划", "不同剧本下仓位上限是多少，哪些仓位必须先降。"),
            ("观察清单", "竞价看什么，10点看什么，午后看什么，尾盘看什么。"),
            ("禁止动作", "不追高开高潮、不买后排脉冲、不把承接当主线、不在缩量日乱切。"),
        ],
        [3.2 * cm, 12.0 * cm],
    )

    story.append(PageBreak())
    story.append(p("十、适配到不同题材", styles["H1CN"]))
    table(
        story,
        styles,
        ["题材类型", "当日看什么", "隔日看什么", "容易犯错"],
        [
            ("半导体国产替代", "设备、材料、封测、存储是否共振。", "设备材料中军能否承接分歧。", "把合肥/国产后排当核心。"),
            ("海外AI硬件链", "CPO、PCB、液冷、服务器容量锚是否稳。", "高位分歧后核心是否修复。", "高潮后追后排补涨。"),
            ("消费/医药", "是否有容量票放量，不只是防守轮动。", "科技分歧后能否连续承接。", "把一日避险当新主线。"),
            ("有色/资源", "价格、期货、汇率、政策是否同步。", "涨价逻辑是否延续，龙头是否抗分歧。", "只看期货不看A股承接。"),
            ("军工/低空/机器人", "事件催化是否带出板块梯队。", "容量票是否能接住情绪票。", "把概念扩散当主线确认。"),
            ("金融地产", "指数护盘还是主动进攻。", "是否带动市场风险偏好。", "护盘拉升后追高。"),
        ],
        [3.0 * cm, 4.1 * cm, 4.2 * cm, 4.1 * cm],
    )

    story.append(p("十一、一页式隔日预判清单", styles["H1CN"]))
    checklist = [
        "1. 今天盘面定性是什么：确认、分歧、轮动、退潮，还是系统性杀跌？",
        "2. 指数强弱：上证、创业板、科创50谁强谁弱？风险偏好是扩张还是收缩？",
        "3. 成交额：全天放量还是缩量？2点后是否继续放量？",
        "4. 广度：上涨家数、涨停、跌停、炸板率是否支持扩散？",
        "5. 核心锚：容量锚、情绪锚、逻辑锚是否同时支持主线？",
        "6. 资金路径：原主线延续、内部高低切、国产/海外链切换，还是去非科技？",
        "7. 国产 vs 海外链：今天谁是主线，谁是补涨，谁是承接？明天看哪个容量锚验证？",
        "8. 明日剧本：延续、分歧承接、切换失败、系统性风险分别怎么处理？",
        "9. 仓位计划：每个剧本允许几成仓？哪些票必须先降级？",
        "10. 盘中验证：竞价、10点、午后、尾盘分别看什么？",
        "11. 禁止动作：不追高潮，不买无锚点后排，不在缩量轮动里乱切。",
        "12. 最终动作：验证通过再做，验证失败先退，没看懂就空仓。",
    ]
    for item in checklist:
        story.append(p(item, styles["BodyCN"]))

    story.append(p("最终纪律", styles["H1CN"]))
    story.append(p("隔日预判的价值不是押中明天，而是提前知道明天哪些信号可以做、哪些信号必须退。看不懂资金路径时，不要为了参与而参与。", styles["BodyCN"]))

    def footer(canvas, doc_obj):
        canvas.saveState()
        canvas.setFont("CN", 8)
        canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawCentredString(A4[0] / 2, 0.55 * cm, f"第 {doc_obj.page} 页")
        canvas.restoreState()

    doc.build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
    print(OUT)
