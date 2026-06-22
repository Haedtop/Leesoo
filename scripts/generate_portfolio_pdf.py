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
        p("수치와 운영 리스크로\n시스템 구조를 정리하는 기획자 이정수", "KTitle"),
        p(
            "상위 업데이트 요구와 운영 지표를 전투, 성장, 보상, 경제 흐름으로 나눠 검토하고 실행 가능한 문서로 정리합니다. "
            "적용 결과형 사례와 정책/검토형 사례를 구분했습니다.",
            "KSubtitle",
        ),
        Spacer(1, 4 * mm),
    ]
    story.append(
        Table(
            [
                [
                    metric("업무 사례", "6개", "내부 업무 문서 기반"),
                    metric("문서 구조", "5단계", "배경-검토-역할-방향-산출"),
                    metric("성과 표기", "분리", "확인 지표와 의도한 효과 구분"),
                ]
            ],
            colWidths=[55 * mm, 55 * mm, 55 * mm],
            hAlign="LEFT",
        )
    )
    story.append(Spacer(1, 6 * mm))

    strength_table = Table(
        [
            [p("업무 판단 기준", "KTableHead"), p("검토 포인트", "KTableHead")],
            [
                p("목적/요구 정리", "KTableBold"),
                p("신규 기능인지, 개선 요청인지, 정책 검토인지에 따라 필요한 판단 기준을 먼저 분리합니다.", "KTable"),
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
    story.append(p("대표 업무 사례 구성", "KSection"))
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
                "지옥 성채, 길드 협동 보상, 길드 공허 소환체, 장신구 재련, 길드 연구/의뢰, PvP TTK 개선안을 대표 업무 사례로 구성했습니다.",
                "적용 결과형 사례와 탑다운 업데이트/정책 검토형 사례를 구분했습니다.",
                "검증되지 않은 매출, 리텐션, PU Ratio 문장은 제외했습니다.",
            ]
        )
    )
    story.append(PageBreak())

    story += [p("Work Cases", "KEyebrow"), p("대표 업무 사례 6개 요약", "KTitle")]
    project_rows = [
        [p("사례", "KTableHead"), p("검토 배경", "KTableHead"), p("담당 범위/방향", "KTableHead"), p("산출물/결과", "KTableHead")],
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
            p("보상 구조 산출물 중심", "KTable"),
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
            p("제안서/정책 문서 산출", "KTable"),
        ],
    ]
    story.append(styled_table(project_rows, [27 * mm, 47 * mm, 58 * mm, 36 * mm]))
    story.append(Spacer(1, 6 * mm))
    story.append(p("작성 원칙", "KSection"))
    story.append(
        bullets(
            [
                "내부 수치는 절대값 대신 범위, 구간, 상대 변화로 재가공했습니다.",
                "확인 가능한 지표와 제안 산출물을 구분했습니다.",
                "내부 수치와 민감 정보는 제출용으로 재가공했습니다.",
            ]
        )
    )
    story.append(PageBreak())

    story += [p("Deep Signal", "KEyebrow"), p("강하게 보여줄 판단 구조", "KTitle")]
    left = [
        p("지옥 성채 - 적용 결과형 사례", "KSection"),
        bullets(
            [
                "배경: 전체 유입은 늘었지만 하위권 진입과 계급 상승이 제한적이었습니다.",
                "검토: 전투력 구간, 계급별 인원, 계급 달성 소요 시간을 함께 비교했습니다.",
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
                "고투력 일부 구간에서 동투력 PvP가 2-4초대로 짧아지는 현상을 정리했습니다.",
                "대미지 공식의 공격력, 스킬 배율, PvP 보정, 절대 증감, 이중 공격 단계를 분해했습니다.",
                "대미지 한계값과 일괄 하향은 부작용이 커서 보조안으로 두고, 신규 PvP 대미지 억제 파라미터를 우선 검토안으로 제안했습니다.",
                "목표 TTK는 약 10-20초 범위로 두고, 상위 콘텐츠 보상에 점진 배분하는 정책을 정리했습니다.",
            ]
        ),
        Spacer(1, 4 * mm),
        p("업무 방식 요약", "KSection"),
        bullets(
            [
                "아이디어 나열보다 요구 정리, 판단 근거, 수치 기준, 리스크 제어 과정을 중시합니다.",
                "전투, 성장, 보상, 경제를 하나의 장기 유지 구조로 연결해 판단합니다.",
                "성과 지표와 정책/검토 산출물을 구분해 실무 신뢰도를 우선합니다.",
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
                p("https://haedtop.github.io/Leesoo/", "KTable"),
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
