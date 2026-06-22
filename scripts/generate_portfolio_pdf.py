from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
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


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "output" / "pdf"
OUT_DIR.mkdir(parents=True, exist_ok=True)
PUBLIC_DIR = ROOT / "public"
PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

PDF_PATH = OUT_DIR / "lee-jeongsu-portfolio-summary.pdf"
PUBLIC_PDF_PATH = PUBLIC_DIR / "portfolio-summary.pdf"

pdfmetrics.registerFont(TTFont("Malgun", r"C:\Windows\Fonts\malgun.ttf"))
pdfmetrics.registerFont(TTFont("MalgunBold", r"C:\Windows\Fonts\malgunbd.ttf"))

PAGE_W, PAGE_H = A4
INK = colors.HexColor("#14201f")
MUTED = colors.HexColor("#5f6f6d")
TEAL = colors.HexColor("#245b52")
TEAL_DARK = colors.HexColor("#143b36")
BRONZE = colors.HexColor("#a66f2d")
SURFACE = colors.HexColor("#ffffff")
SURFACE_ALT = colors.HexColor("#eef2f4")
LINE = colors.HexColor("#d9e1e0")
BG = colors.HexColor("#f6f7f9")

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="KTitle",
        fontName="MalgunBold",
        fontSize=27,
        leading=33,
        textColor=INK,
        spaceAfter=8,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="KSubtitle",
        fontName="Malgun",
        fontSize=10.2,
        leading=15.5,
        textColor=MUTED,
        spaceAfter=10,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="KEyebrow",
        fontName="MalgunBold",
        fontSize=8.5,
        leading=11,
        textColor=BRONZE,
        spaceAfter=5,
        alignment=TA_LEFT,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="KSection",
        fontName="MalgunBold",
        fontSize=14.5,
        leading=18,
        textColor=TEAL_DARK,
        spaceBefore=4,
        spaceAfter=8,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="KBody",
        fontName="Malgun",
        fontSize=8.35,
        leading=12.4,
        textColor=INK,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="KSmall",
        fontName="Malgun",
        fontSize=7.3,
        leading=10.5,
        textColor=MUTED,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="KWhite",
        fontName="MalgunBold",
        fontSize=9.5,
        leading=12.5,
        textColor=colors.white,
        alignment=TA_CENTER,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="KTableHead",
        fontName="MalgunBold",
        fontSize=7.8,
        leading=10.5,
        textColor=colors.white,
        alignment=TA_CENTER,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="KTable",
        fontName="Malgun",
        fontSize=7.05,
        leading=9.7,
        textColor=INK,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="KTableBold",
        fontName="MalgunBold",
        fontSize=7.3,
        leading=10.1,
        textColor=INK,
        wordWrap="CJK",
    )
)


def p(text: str, style: str = "KBody") -> Paragraph:
    safe = (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )
    return Paragraph(safe, styles[style])


def bullets(items: list[str]) -> Table:
    rows = [[p("•", "KSmall"), p(item, "KBody")] for item in items]
    table = Table(rows, colWidths=[5 * mm, None], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 1.2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1.2),
                ("TEXTCOLOR", (0, 0), (0, -1), BRONZE),
            ]
        )
    )
    return table


def pill(text: str) -> Table:
    table = Table([[p(text, "KWhite")]], colWidths=[31 * mm], rowHeights=[9 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), TEAL),
                ("BOX", (0, 0), (-1, -1), 0.4, TEAL),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return table


def metric(label: str, value: str, note: str) -> Table:
    table = Table(
        [[p(label, "KSmall")], [p(value, "KTableBold")], [p(note, "KSmall")]],
        colWidths=[43 * mm],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SURFACE_ALT),
                ("BOX", (0, 0), (-1, -1), 0.4, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return table


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, PAGE_H - 8 * mm, PAGE_W, 8 * mm, fill=1, stroke=0)
    canvas.setFont("Malgun", 7.2)
    canvas.setFillColor(MUTED)
    canvas.drawString(18 * mm, 10 * mm, "이정수 | MMORPG 시스템/밸런스 기획 포트폴리오 요약")
    canvas.drawRightString(PAGE_W - 18 * mm, 10 * mm, f"{doc.page}/3")
    canvas.restoreState()


def styled_table(data, col_widths):
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), TEAL_DARK),
                ("BACKGROUND", (0, 1), (-1, -1), SURFACE),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4.5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4.5),
                ("TOPPADDING", (0, 0), (-1, -1), 4.2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4.2),
            ]
        )
    )
    return table


def build_pdf():
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        rightMargin=17 * mm,
        leftMargin=17 * mm,
        topMargin=18 * mm,
        bottomMargin=17 * mm,
    )

    story = []

    story += [
        p("MMORPG 시스템/밸런스 기획자", "KEyebrow"),
        p("수치로 확인하고 구조로 해결하는\n기획자 이정수", "KTitle"),
        p(
            "전투, 성장, 보상, 경제 흐름을 분리해서 보지 않고 하나의 플레이 구조로 연결해 설계합니다. "
            "포트폴리오 문장은 실제 결과와 기대 효과를 분리하고, 내부 수치는 제출용으로 범위화했습니다.",
            "KSubtitle",
        ),
        Spacer(1, 4 * mm),
    ]
    story.append(
        Table(
            [
                [
                    metric("대표 사례", "6개", "원문/업무 맥락 기반"),
                    metric("문서 구조", "5단계", "문제-분석-내 역할-설계-결과"),
                    metric("성과 표기", "분리", "실제 결과와 기대 효과 구분"),
                ]
            ],
            colWidths=[55 * mm, 55 * mm, 55 * mm],
            hAlign="LEFT",
        )
    )
    story.append(Spacer(1, 6 * mm))

    strength_table = Table(
        [
            [p("핵심 역량", "KTableHead"), p("면접관이 확인해야 할 포인트", "KTableHead")],
            [
                p("목적 우선 설계", "KTableBold"),
                p("기능을 먼저 늘리지 않고 어떤 문제를 해결할지, 어떤 유저 판단을 만들지 먼저 정의합니다.", "KTable"),
            ],
            [
                p("수치 기반 검증", "KTableBold"),
                p(
                    "TTK, 보상 기대값, 포인트 허들, 공급량, 계급 분포를 함께 보며 구조가 실제로 작동할지 확인합니다.",
                    "KTable",
                ),
            ],
            [
                p("리스크 제어", "KTableBold"),
                p("상위 유저 독점, 신규/복귀 유저 진입 장벽, 인플레이션, BM 가치 훼손을 함께 검토합니다.", "KTable"),
            ],
            [
                p("협업 문서화", "KTableBold"),
                p("피드백 반영 이력, 신규 개발 요청, 예외 처리 조건을 문서로 남겨 구현 단계의 판단 비용을 낮춥니다.", "KTable"),
            ],
        ],
        colWidths=[42 * mm, 124 * mm],
    )
    strength_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), TEAL_DARK),
                ("BACKGROUND", (0, 1), (-1, -1), SURFACE),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6),
                ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(strength_table)
    story.append(Spacer(1, 6 * mm))
    story.append(p("대표 프로젝트 구성", "KSection"))
    story.append(
        Table(
            [[pill("전투"), pill("성장"), pill("보상"), pill("경제"), pill("정책")]],
            colWidths=[33 * mm] * 5,
            hAlign="LEFT",
        )
    )
    story.append(Spacer(1, 5 * mm))
    story.append(
        bullets(
            [
                "지옥 성채, 길드 협동 보상, 길드 공허 소환체, 장신구 재련, 길드 연구/의뢰, PvP TTK 개선안을 대표 사례로 구성했습니다.",
                "정량 성과가 확인된 지옥 성채는 실제 결과로 표기하고, 나머지는 설계 산출물과 기대 효과를 분리했습니다.",
                "검증되지 않은 매출, 리텐션, PU Ratio 문장은 제외했습니다.",
            ]
        )
    )
    story.append(PageBreak())

    story += [p("Case Studies", "KEyebrow"), p("대표 프로젝트 6개 요약", "KTitle")]
    project_rows = [
        [p("프로젝트", "KTableHead"), p("문제", "KTableHead"), p("내 역할/설계", "KTableHead"), p("결과 구분", "KTableHead")],
        [
            p("지옥 성채", "KTableBold"),
            p("하위권 유입 저조, 계급 분포 공백, 포인트 허들 과다", "KTable"),
            p("계급 분포 분석, 포인트 조정, 정예 몬스터 보상/공급량 설계", "KTable"),
            p("실제: 1천명대 초반 -> 2천명대 초반, 일부 공백 계급 80명대 형성", "KTable"),
        ],
        [
            p("길드 협동 보상", "KTableBold"),
            p("소수 인원 보상 독점 가능성, 다인 길드 참여 가치 약화", "KTable"),
            p("기본/핵심 보상 이원화, 귀속/제한/단계 차등으로 공급량 제어", "KTable"),
            p("실제 KPI 미기재, 기대 효과로 분리", "KTable"),
        ],
        [
            p("길드 공허 소환체", "KTableBold"),
            p("저투력 빗나감, 상위 길드의 낮은 챕터 보스 단기 처치", "KTable"),
            p("회피값 하향, 3-5챕터 HP 상향, 15명 기준 1-3분 목표", "KTable"),
            p("전투 밸런싱 모델 산출물로 표기", "KTable"),
        ],
        [
            p("장신구 재련", "KTableBold"),
            p("강화 정체 구간, 캐시 장신구 수요 감소, 경제 리스크", "KTable"),
            p("재련 단계, 옵션 그룹, 재련석 귀속 공급, 피드백 반영", "KTable"),
            p("설계/피드백 산출물로 표기", "KTable"),
        ],
        [
            p("길드 연구/의뢰", "KTableBold"),
            p("길드 주화 흐름, 미션 후보 부족, 스킵/소급 예외", "KTable"),
            p("Achievement/Quest 후보 분류, 신규 개발 요청, 일일/주간 역할 분리", "KTable"),
            p("업데이트 방향 문서와 FB 엑셀 산출", "KTable"),
        ],
        [
            p("PvP TTK", "KTableBold"),
            p("고투력 구간 TTK 단축, 제어기 선점 의존, PvE 부작용 우려", "KTable"),
            p("대미지 공식 분해, 3개 개선안 비교, PvP 억제 파라미터 제안", "KTable"),
            p("제안서 V4/정책 문서 산출, KPI 미기재", "KTable"),
        ],
    ]
    story.append(styled_table(project_rows, [27 * mm, 47 * mm, 58 * mm, 36 * mm]))
    story.append(Spacer(1, 6 * mm))
    story.append(p("작성 원칙", "KSection"))
    story.append(
        bullets(
            [
                "내부 수치는 절대값 대신 범위, 구간, 상대 변화로 재가공했습니다.",
                "실제 결과는 출처가 확인된 자료만 사용했습니다.",
                "검증되지 않은 성과는 기대 효과로 낮춰 표기했습니다.",
            ]
        )
    )
    story.append(PageBreak())

    story += [p("Deep Signal", "KEyebrow"), p("강하게 보여줄 판단 구조", "KTitle")]
    left = [
        p("지옥 성채 - 실제 결과가 있는 사례", "KSection"),
        bullets(
            [
                "문제: 전체 유입은 늘었지만 하위권 진입과 계급 상승이 제한적이었습니다.",
                "분석: 전투력 구간, 계급별 인원, 계급 달성 소요 시간을 함께 비교했습니다.",
                "설계: 일반 몬스터 포인트 상향, 정예 몬스터 보상, 귀속/공급량 제어를 함께 적용했습니다.",
                "결과: 계급 집계 인원은 1천명대 초반에서 2천명대 초반으로 확대되었고, 일부 공백 계급에 80명대 인원이 형성되었습니다.",
            ]
        ),
        Spacer(1, 4 * mm),
        p("길드 연구/의뢰 - 업무 과정의 맥락", "KSection"),
        bullets(
            [
                "QuestMission만으로는 길드 의뢰 구성이 부족하다는 점을 확인했습니다.",
                "AchievementMission 후보를 함께 검토하고 길드/솔로/BM 성격으로 분류했습니다.",
                "스킵, 초기화, 수락 전 진행 같은 예외를 개발 요청 전에 정리했습니다.",
            ]
        ),
    ]
    right = [
        p("PvP TTK - 전투 공식 기반 제안", "KSection"),
        bullets(
            [
                "고투력 일부 구간에서 동투력 PvP가 2-4초대로 짧아지는 문제를 정의했습니다.",
                "대미지 공식의 공격력, 스킬 배율, PvP 보정, 절대 증감, 이중 공격 단계를 분해했습니다.",
                "대미지 한계값과 일괄 하향은 부작용이 커서 보조안으로 두고, 신규 PvP 대미지 억제 파라미터를 채택안으로 제안했습니다.",
                "목표 TTK는 약 10-20초 범위로 두고, 상위 콘텐츠 보상에 점진 배분하는 정책을 정리했습니다.",
            ]
        ),
        Spacer(1, 4 * mm),
        p("면접관 관점 핵심 문장", "KSection"),
        bullets(
            [
                "아이디어 나열이 아니라 문제 정의, 원인 분석, 수치 기준, 리스크 제어 과정을 보여줍니다.",
                "전투, 성장, 보상, 경제를 하나의 장기 유지 구조로 연결해 판단합니다.",
                "성과를 과장하지 않고 실제 결과와 기대 효과를 분리해 실무 신뢰도를 우선합니다.",
            ]
        ),
    ]
    columns = Table([[left, right]], colWidths=[82 * mm, 82 * mm])
    columns.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 0), (-1, -1), SURFACE),
                ("BOX", (0, 0), (-1, -1), 0.4, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(columns)
    story.append(Spacer(1, 5 * mm))
    contact = Table(
        [
            [
                p("연락처", "KTableBold"),
                p("jjangsoo8571@gmail.com / 010-8048-8571", "KTable"),
                p("웹 포트폴리오", "KTableBold"),
                p("https://lee-soo-portfolio.vercel.app/", "KTable"),
            ]
        ],
        colWidths=[22 * mm, 62 * mm, 27 * mm, 57 * mm],
    )
    contact.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SURFACE_ALT),
                ("GRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(contact)

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    PUBLIC_PDF_PATH.write_bytes(PDF_PATH.read_bytes())
    print(PDF_PATH)
    print(PUBLIC_PDF_PATH)


if __name__ == "__main__":
    build_pdf()
