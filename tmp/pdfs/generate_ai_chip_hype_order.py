from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics


OUT = "output/pdf/deepseek-zhipu-ai-chip-sector-hype-order.pdf"


FONT = "CNFont"
FONT_PATH = "/System/Library/Fonts/Supplemental/Songti.ttc"
pdfmetrics.registerFont(TTFont(FONT, FONT_PATH, subfontIndex=0))


def p(text, style):
    return Paragraph(text, style)


def cell(text, style):
    return Paragraph(text.replace("\n", "<br/>"), style)


styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="CNTitle",
        fontName=FONT,
        fontSize=22,
        leading=30,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#102A43"),
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="CNSubTitle",
        fontName=FONT,
        fontSize=10.5,
        leading=16,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#52616B"),
        spaceAfter=18,
    )
)
styles.add(
    ParagraphStyle(
        name="CNH1",
        fontName=FONT,
        fontSize=15,
        leading=22,
        textColor=colors.HexColor("#0B3954"),
        spaceBefore=12,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        name="CNH2",
        fontName=FONT,
        fontSize=12.5,
        leading=18,
        textColor=colors.HexColor("#214E34"),
        spaceBefore=8,
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="CNBody",
        fontName=FONT,
        fontSize=10.2,
        leading=16,
        alignment=TA_LEFT,
        textColor=colors.HexColor("#1F2933"),
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        name="CNSmall",
        fontName=FONT,
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#52616B"),
    )
)
styles.add(
    ParagraphStyle(
        name="CNTable",
        fontName=FONT,
        fontSize=8.7,
        leading=12.5,
        textColor=colors.HexColor("#1F2933"),
    )
)
styles.add(
    ParagraphStyle(
        name="CNTableHead",
        fontName=FONT,
        fontSize=9,
        leading=12.5,
        textColor=colors.white,
        alignment=TA_CENTER,
    )
)


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont(FONT, 8)
    canvas.setFillColor(colors.HexColor("#7B8794"))
    canvas.drawString(18 * mm, 12 * mm, "DeepSeek/智谱 AI 芯片主题资金扩散推演 - 仅作研究框架")
    canvas.drawRightString(192 * mm, 12 * mm, f"{doc.page}")
    canvas.restoreState()


doc = SimpleDocTemplate(
    OUT,
    pagesize=A4,
    rightMargin=16 * mm,
    leftMargin=16 * mm,
    topMargin=16 * mm,
    bottomMargin=18 * mm,
)

story = []
story.append(p("DeepSeek 与智谱 AI 芯片主题", styles["CNTitle"]))
story.append(p("利好板块、产业链扩散路径与资金炒作顺序推演", styles["CNSubTitle"]))
story.append(p("生成日期：2026-07-08 | 风险提示：本文为主题研究，不构成买卖建议。", styles["CNSmall"]))
story.append(Spacer(1, 8))

story.append(p("一、先把事实和推演分开", styles["CNH1"]))
facts = [
    [
        cell("事项", styles["CNTableHead"]),
        cell("公开信息强度", styles["CNTableHead"]),
        cell("对 A 股主题的含义", styles["CNTableHead"]),
    ],
    [
        cell("DeepSeek 自研 AI 推理芯片", styles["CNTable"]),
        cell("中等：外媒援引路透称仍在早期阶段，方向偏推理芯片，需外部伙伴和设计团队扩张验证。", styles["CNTable"]),
        cell("短线更容易刺激“国产 AI 芯片自主可控”风险偏好，核心是推理芯片、国产算力、半导体设计链。", styles["CNTable"]),
    ],
    [
        cell("智谱/GLM 与国产芯片生态", styles["CNTable"]),
        cell("中等偏高：公开信息更多指向 GLM 模型适配昇腾、寒武纪、摩尔线程等国产芯片；“智谱自研芯片”公开证据较弱。", styles["CNTable"]),
        cell("更像“模型厂商倒逼国产硬件和软件栈适配”的扩散逻辑，利好芯片生态、算力调度、云服务和应用端。", styles["CNTable"]),
    ],
    [
        cell("共性主线", styles["CNTable"]),
        cell("高：美国先进 GPU 限制、国内大模型推理需求增长、成本下降诉求同时存在。", styles["CNTable"]),
        cell("资金会从最硬的芯片环节，扩散到服务器、PCB/光模块、先进封装、数据中心、液冷电源、AI 应用。", styles["CNTable"]),
    ],
]
t = Table(facts, colWidths=[38 * mm, 65 * mm, 75 * mm])
t.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B3954")),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CBD2D9")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F8FAFC")),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]
    )
)
story.append(t)

story.append(p("二、利好板块排序", styles["CNH1"]))
story.append(p("第一梯队：直接受益于“自研/国产 AI 芯片”的硬科技环节", styles["CNH2"]))
story.append(p("1. 国产 AI 芯片/GPU/NPU：寒武纪、海光信息、景嘉微、摩尔线程链条、昇腾生态。逻辑最直接，但估值弹性和波动也最大。", styles["CNBody"]))
story.append(p("2. 半导体设计服务、EDA、IP：华大九天、概伦电子、芯原股份等。自研芯片若进入设计、验证、流片，EDA/IP 是早期必要环节。", styles["CNBody"]))
story.append(p("3. 先进封装、Chiplet、测试：长电科技、通富微电、华天科技、甬矽电子、华峰测控、长川科技等。AI 芯片越来越依赖高带宽互连和封测能力。", styles["CNBody"]))

story.append(p("第二梯队：放量阶段会兑现订单的基础设施环节", styles["CNH2"]))
story.append(p("4. AI 服务器与整机：浪潮信息、中科曙光、工业富联、神州数码、拓维信息、软通动力等。若国产芯片生态成形，整机适配和集群交付会跟上。", styles["CNBody"]))
story.append(p("5. PCB、光模块、连接器：沪电股份、胜宏科技、深南电路、生益科技、中际旭创、新易盛、天孚通信、光迅科技、剑桥科技等。训练和推理集群都绕不开高速互连。", styles["CNBody"]))
story.append(p("6. 存储与内存接口：澜起科技、兆易创新、佰维存储、香农芯创等。推理芯片若强调低成本和高吞吐，内存带宽与容量仍是瓶颈。", styles["CNBody"]))

story.append(p("第三梯队：主题扩散和补涨环节", styles["CNH2"]))
story.append(p("7. 数据中心、算力租赁、云：润泽科技、数据港、奥飞数据、首都在线、云赛智联等。资金通常在芯片主线高位后扩散到“谁能承接推理需求”。", styles["CNBody"]))
story.append(p("8. 液冷、电源、温控：英维克、同飞股份、申菱环境、科华数据、科士达等。AI 集群密度提高后，液冷和电源弹性会被二次挖掘。", styles["CNBody"]))
story.append(p("9. AI 应用和 Agent：办公、金融、教育、政务、工业软件、客服营销等。若硬件叙事退潮，资金会转向“国产模型+国产算力+场景落地”。", styles["CNBody"]))

story.append(p("三、资金炒作顺序：从消息脉冲到产业兑现", styles["CNH1"]))
order = [
    [cell("阶段", styles["CNTableHead"]), cell("资金偏好", styles["CNTableHead"]), cell("常见表现", styles["CNTableHead"]), cell("观察信号", styles["CNTableHead"])],
    [
        cell("1. 消息发酵 0-2 天", styles["CNTable"]),
        cell("最正宗、辨识度最高的国产 AI 芯片和 GPU。", styles["CNTable"]),
        cell("龙头高开、成交额快速放大，低位同名概念跟随。", styles["CNTable"]),
        cell("是否出现一字板/大成交换手板；海外 Nvidia 走势是否共振。", styles["CNTable"]),
    ],
    [
        cell("2. 主线确认 2-5 天", styles["CNTable"]),
        cell("昇腾、寒武纪、摩尔线程、海光等生态伙伴；服务器整机。", styles["CNTable"]),
        cell("从“芯片本体”扩到“谁能卖系统、卖集群、卖适配”。", styles["CNTable"]),
        cell("龙头是否继续放量走趋势；应用端是否开始出现订单新闻。", styles["CNTable"]),
    ],
    [
        cell("3. 产业链扩散 1-2 周", styles["CNTable"]),
        cell("PCB、光模块、先进封装、EDA/IP、测试设备。", styles["CNTable"]),
        cell("资金挖掘“芯片做出来需要什么”，弹性从核心票向配套票扩散。", styles["CNTable"]),
        cell("强势股不再只集中于芯片；半导体设备材料是否轮动。", styles["CNTable"]),
    ],
    [
        cell("4. 成本下降叙事 2-4 周", styles["CNTable"]),
        cell("算力租赁、数据中心、液冷、电源、云服务。", styles["CNTable"]),
        cell("市场从“能不能自研”切到“推理成本下降后谁受益”。", styles["CNTable"]),
        cell("是否出现云厂商、政企项目、地方智算中心采购线索。", styles["CNTable"]),
    ],
    [
        cell("5. 应用补涨/退潮", styles["CNTable"]),
        cell("AI 应用、Agent、垂直行业软件。", styles["CNTable"]),
        cell("硬件高位震荡后，低位应用补涨；若无订单，主题开始退潮。", styles["CNTable"]),
        cell("核心龙头跌破 5 日/10 日线且扩散票冲高回落，要防退潮。", styles["CNTable"]),
    ],
]
t2 = Table(order, colWidths=[26 * mm, 48 * mm, 52 * mm, 52 * mm])
t2.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#214E34")),
            ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#CBD2D9")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#FBFDF8")),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]
    )
)
story.append(t2)

story.append(p("四、最可能的扩散路径", styles["CNH1"]))
story.append(p("路径 A：DeepSeek 自研推理芯片 -> 国产 AI 芯片 -> EDA/IP -> 先进封装/测试 -> AI 服务器 -> 数据中心/液冷 -> AI 应用。", styles["CNBody"]))
story.append(p("路径 B：智谱模型适配国产芯片 -> 昇腾/寒武纪/摩尔线程生态 -> 整机和软件适配 -> 政企云和行业大模型 -> 应用落地。", styles["CNBody"]))
story.append(p("路径 C：国产推理成本下降 -> 推理 token 价格下降 -> Agent 和垂直应用调用量提升 -> 云服务、存储、网络、运维安全同步受益。", styles["CNBody"]))

story.append(p("五、交易上更重要的三条线", styles["CNH1"]))
story.append(p("1. 正宗度线：越靠近“芯片设计/国产 GPU/NPU/模型适配”的标的，消息初期越强；越靠后端应用，通常靠扩散和补涨。", styles["CNBody"]))
story.append(p("2. 兑现度线：短炒看辨识度，波段看是否有真实订单、适配认证、流片进展、客户导入和营收占比。", styles["CNBody"]))
story.append(p("3. 位置线：高位硬件股适合看趋势和量能，不适合因消息盲目追高；低位扩散股要防“概念贴标签”后冲高回落。", styles["CNBody"]))

story.append(p("六、退潮信号", styles["CNH1"]))
story.append(p("1. 核心芯片龙头放巨量滞涨，后排票继续冲高但封不住。", styles["CNBody"]))
story.append(p("2. 消息没有进一步订单、适配、流片、量产信息，只剩重复解读。", styles["CNBody"]))
story.append(p("3. 资金从硬件扩散到纯概念应用后，应用端也无法继续放量。", styles["CNBody"]))
story.append(p("4. 半导体、算力、应用三条线开始同时回落，说明不是轮动而是退潮。", styles["CNBody"]))

story.append(p("七、结论", styles["CNH1"]))
story.append(p("这条主线的核心不是“DeepSeek 或智谱马上卖芯片”，而是国内头部模型厂商正在把推理成本、芯片可得性、国产生态适配变成更紧迫的产业问题。资金最先炒国产 AI 芯片和 GPU，然后扩散到 EDA/IP、封测、服务器、PCB/光模块、数据中心和液冷，最后才轮到 AI 应用。短线看辨识度，中线看订单和适配进度。", styles["CNBody"]))

story.append(p("主要参考来源", styles["CNH1"]))
sources = [
    "Times of India 转述 Reuters：DeepSeek 正在开发面向推理的 AI 芯片，项目仍处早期，目标是降低对 Nvidia、华为等外部芯片依赖。",
    "Barron's：DeepSeek 自研推理芯片消息对 Nvidia 股价形成扰动，并指出 DeepSeek 近期使用华为处理器。",
    "Z.ai/智谱公开资料与 GLM 系列资料：智谱 GLM 模型持续迭代，公开信息显示其模型与国产芯片生态存在适配推进。",
    "DeepSeek 技术报告与相关研究：DeepSeek 低成本训练、MoE、推理优化和工程效率是市场关注国产 AI 算力链的基础。",
]
for s in sources:
    story.append(p("· " + s, styles["CNSmall"]))

story.append(Spacer(1, 8))
story.append(p("免责声明：本文仅为公开资料整理和市场资金行为推演，不构成任何证券投资建议。个股仅作为产业链示例，不代表推荐买入。", styles["CNSmall"]))

doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(OUT)
