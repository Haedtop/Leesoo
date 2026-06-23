from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
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
PUBLIC_DIR = ROOT / "public"
OUT_DIR.mkdir(parents=True, exist_ok=True)
PUBLIC_DIR.mkdir(parents=True, exist_ok=True)

PDF_PATH = OUT_DIR / "lee-jeongsu-portfolio-summary.pdf"
PUBLIC_PDF_PATH = PUBLIC_DIR / "portfolio-summary.pdf"

pdfmetrics.registerFont(TTFont("Malgun", r"C:\Windows\Fonts\malgun.ttf"))
pdfmetrics.registerFont(TTFont("MalgunBold", r"C:\Windows\Fonts\malgunbd.ttf"))

INK = colors.HexColor("#14201f")
MUTED = colors.HexColor("#5f6f6d")
TEAL = colors.HexColor("#245b52")
TEAL_DARK = colors.HexColor("#143b36")
BRONZE = colors.HexColor("#a66f2d")
SURFACE = colors.HexColor("#ffffff")
SURFACE_ALT = colors.HexColor("#eef2f4")
LINE = colors.HexColor("#d9e1e0")
BG = colors.HexColor("#f6f7f9")

PAGE_W, PAGE_H = A4

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        name="TitleKo",
        fontName="MalgunBold",
        fontSize=24,
        leading=30,
        textColor=INK,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="SectionKo",
        fontName="MalgunBold",
        fontSize=13,
        leading=17,
        textColor=TEAL_DARK,
        spaceBefore=2,
        spaceAfter=7,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="BodyKo",
        fontName="Malgun",
        fontSize=8.5,
        leading=12.6,
        textColor=INK,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="SmallKo",
        fontName="Malgun",
        fontSize=7.2,
        leading=10.4,
        textColor=MUTED,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="EyebrowKo",
        fontName="MalgunBold",
        fontSize=8,
        leading=11,
        textColor=BRONZE,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="WhiteKo",
        fontName="MalgunBold",
        fontSize=8.1,
        leading=11,
        textColor=colors.white,
        alignment=TA_CENTER,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="HeadKo",
        fontName="MalgunBold",
        fontSize=7.3,
        leading=10,
        textColor=colors.white,
        alignment=TA_CENTER,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="CellKo",
        fontName="Malgun",
        fontSize=6.65,
        leading=9.35,
        textColor=INK,
        wordWrap="CJK",
    )
)
styles.add(
    ParagraphStyle(
        name="CellBoldKo",
        fontName="MalgunBold",
        fontSize=6.8,
        leading=9.5,
        textColor=INK,
        wordWrap="CJK",
    )
)


def p(text: str, style: str = "BodyKo") -> Paragraph:
    safe = (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("\n", "<br/>")
    )
    return Paragraph(safe, styles[style])


def bullets(items: list[str]) -> Table:
    rows = [[p("-", "SmallKo"), p(item, "BodyKo")] for item in items]
    table = Table(rows, colWidths=[4.5 * mm, None], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 1.1),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 1.1),
                ("TEXTCOLOR", (0, 0), (0, -1), BRONZE),
            ]
        )
    )
    return table


def metric(label: str, value: str, note: str) -> Table:
    table = Table(
        [[p(label, "SmallKo")], [p(value, "CellBoldKo")], [p(note, "SmallKo")]],
        colWidths=[50 * mm],
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SURFACE_ALT),
                ("BOX", (0, 0), (-1, -1), 0.35, LINE),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return table


def pill(text: str) -> Table:
    table = Table([[p(text, "WhiteKo")]], colWidths=[31 * mm], rowHeights=[9 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), TEAL),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
            ]
        )
    )
    return table


def styled_table(data, col_widths):
    table = Table(data, colWidths=col_widths, repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), TEAL_DARK),
                ("BACKGROUND", (0, 1), (-1, -1), SURFACE),
                ("GRID", (0, 0), (-1, -1), 0.32, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BG)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.setFillColor(TEAL)
    canvas.rect(0, PAGE_H - 7 * mm, PAGE_W, 7 * mm, fill=1, stroke=0)
    canvas.setFont("Malgun", 7.2)
    canvas.setFillColor(MUTED)
    canvas.drawString(17 * mm, 10 * mm, "이정수 | MMORPG 시스템/밸런스 기획 포트폴리오 요약")
    canvas.drawRightString(PAGE_W - 17 * mm, 10 * mm, f"{doc.page}/3")
    canvas.restoreState()


def build_pdf():
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=A4,
        rightMargin=17 * mm,
        leftMargin=17 * mm,
        topMargin=17 * mm,
        bottomMargin=16 * mm,
    )

    story = []

    story += [
        p("MMORPG SYSTEM / BALANCE PLANNER", "EyebrowKo"),
        p("성장, 보상, 전투 구조를 운영 가능한 규칙으로 정리하는 기획자", "TitleKo"),
        p(
            "라이온하트 스튜디오에서 2023.11부터 2026.06.21까지 오딘: 발할라 라이징의 시스템/밸런스 기획 업무를 수행했습니다. 콘텐츠 추가보다 반복 동기, 재화 흐름, 성장 체감, 운영 리스크가 맞물리는 구조를 중요하게 봅니다.",
            "BodyKo",
        ),
        Spacer(1, 4 * mm),
        Table(
            [
                [
                    metric("대표 업무", "6개", "실제 업무 문서 기반"),
                    metric("정리 구조", "6단계", "소개/배경/분석/역할/결과/효과"),
                    metric("성과 표기", "분리", "실제 결과와 기대 효과 구분"),
                ]
            ],
            colWidths=[55 * mm, 55 * mm, 55 * mm],
            hAlign="LEFT",
        ),
        Spacer(1, 6 * mm),
        p("핵심 업무 방식", "SectionKo"),
    ]

    story.append(
        styled_table(
            [
                [p("기준", "HeadKo"), p("설명", "HeadKo")],
                [
                    p("목적과 제약 분리", "CellBoldKo"),
                    p("상위 방향을 기능 목록으로 옮기기 전에 해결해야 할 문제와 건드리면 안 되는 제약을 나눕니다.", "CellKo"),
                ],
                [
                    p("수치와 체감 연결", "CellBoldKo"),
                    p("포인트, HP, TTK, 보상 공급량을 유저 진행 속도와 반복 동기 기준으로 해석합니다.", "CellKo"),
                ],
                [
                    p("운영 리스크 점검", "CellBoldKo"),
                    p("상위 유저 독점, 신규/복귀 유저 진입 장벽, 거래소 영향, 재화 인플레이션 가능성을 함께 확인합니다.", "CellKo"),
                ],
                [
                    p("성과 표기 원칙", "CellBoldKo"),
                    p("확인된 지표와 제안 단계의 기대 효과를 분리하고, 내부 수치는 범위화합니다.", "CellKo"),
                ],
            ],
            [42 * mm, 124 * mm],
        )
    )
    story.append(Spacer(1, 6 * mm))
    story.append(p("업무 범위", "SectionKo"))
    story.append(
        Table(
            [[pill("전투"), pill("성장"), pill("보상"), pill("경제"), pill("길드")]],
            colWidths=[33 * mm] * 5,
            hAlign="LEFT",
        )
    )
    story.append(Spacer(1, 5 * mm))
    story.append(
        bullets(
            [
                "전투 시간, 성장 정체 구간, 보상 기대값, 재화 수급/소모, 길드 반복 동기를 함께 검토했습니다.",
                "문서 구조는 시스템 소개, 업무 배경, 분석 기준, 내 역할, 실제 결과, 기대 효과로 통일했습니다.",
                "검증되지 않은 매출, 리텐션, 과장 성과 문장은 제외했습니다.",
            ]
        )
    )
    story.append(PageBreak())

    story += [p("PROJECT SUMMARY", "EyebrowKo"), p("대표 프로젝트 6개 요약", "TitleKo")]
    story.append(
        styled_table(
            [
                [p("프로젝트", "HeadKo"), p("시스템 소개/배경", "HeadKo"), p("내 역할", "HeadKo"), p("결과/효과", "HeadKo")],
                [
                    p("지옥 성채", "CellBoldKo"),
                    p("월드 던전 계급 포인트와 보상 공급량을 조정한 사례입니다. 일부 계급 공백과 도달 시간 문제를 확인했습니다.", "CellKo"),
                    p("계급별 필요 포인트, 정예 몬스터 보상, 핵심 재료 공급 리스크를 정리했습니다.", "CellKo"),
                    p("집계 인원 1천대 초반 -> 2천대 초반. 일부 공백 계급 80명대 형성.", "CellKo"),
                ],
                [
                    p("길드 협동 보상", "CellBoldKo"),
                    p("소수 인원 효율과 다인 참여 동기가 충돌하지 않도록 보상 구조를 검토했습니다.", "CellKo"),
                    p("기본/특수 보상 분리, 귀속/제한/차등 기준을 정리했습니다.", "CellKo"),
                    p("보상 구조 산출물 중심. 검증되지 않은 운영 성과는 제외.", "CellKo"),
                ],
                [
                    p("길드 공허 소환체", "CellBoldKo"),
                    p("길드 보스의 회피값, HP, 기준 인원 전투 시간을 조정한 PvE 밸런싱 사례입니다.", "CellKo"),
                    p("보스 회피값 조정, 챕터별 HP 재산정, 15명 기준 전투 시간 산정표를 정리했습니다.", "CellKo"),
                    p("약 1-3분 전투 시간 목표. 저전투력 길드원의 명중 체감 보완.", "CellKo"),
                ],
                [
                    p("장신구 재련", "CellBoldKo"),
                    p("장신구 강화 이후 추가 성장축을 검토한 시스템입니다.", "CellKo"),
                    p("재련 조건, 옵션 그룹, 재련석 수급처, 거래소/BM 영향, 피드백 반영안을 정리했습니다.", "CellKo"),
                    p("성장 정체 구간에 보조 목표를 제공하고 재련석 소비처를 연결.", "CellKo"),
                ],
                [
                    p("길드 연구/의뢰", "CellBoldKo"),
                    p("탑다운 방향을 길드 주화 흐름, 미션 후보, 예외 처리 기준으로 구체화한 업무입니다.", "CellKo"),
                    p("Achievement/Quest 후보 검토, 일일/주간 의뢰 분리, 스킵/초기화/소급 예외를 정리했습니다.", "CellKo"),
                    p("미션 후보 Achievement 70개대 / Quest 10개대 검토.", "CellKo"),
                ],
                [
                    p("PvP TTK", "CellBoldKo"),
                    p("고전투력 구간에서 전투 시간이 짧아지는 문제를 대미지 공식 기준으로 검토했습니다.", "CellKo"),
                    p("대미지 상한, 일괄 하향, 신규 PvP 방어 파라미터 3개 안을 비교했습니다.", "CellKo"),
                    p("일부 2-4초대 문제 구간을 약 10-20초대 목표로 완화하는 제안.", "CellKo"),
                ],
            ],
            [25 * mm, 53 * mm, 53 * mm, 36 * mm],
        )
    )
    story.append(Spacer(1, 5 * mm))
    story.append(
        bullets(
            [
                "실제 결과가 확인된 지옥 성채 외 사례는 산출물과 기대 효과 중심으로 표기했습니다.",
                "내부 수치는 원자료 대신 범위와 요약값만 사용했습니다.",
            ]
        )
    )
    story.append(PageBreak())

    story += [p("DEEP SIGNAL", "EyebrowKo"), p("면접에서 먼저 설명하기 좋은 사례", "TitleKo")]
    left = [
        p("지옥 성채 - 적용 결과가 있는 사례", "SectionKo"),
        bullets(
            [
                "문제: 일부 계급 구간 공백과 포인트 도달 시간 부담이 있었습니다.",
                "분석: 전투력 구간, 계급 분포, 포인트 획득량, 계급 달성 시간을 함께 봤습니다.",
                "역할: 포인트 조정안, 정예 몬스터 보상 구조, 핵심 재료 공급 리스크를 정리했습니다.",
                "결과: 집계 인원은 1천대 초반에서 2천대 초반으로 확대되었고, 일부 공백 계급에 80명대 분포가 형성되었습니다.",
            ]
        ),
        Spacer(1, 4 * mm),
        p("길드 연구/의뢰 - 탑다운 업무 구체화", "SectionKo"),
        bullets(
            [
                "상위 방향을 길드 연구, 길드 주화, 길드 의뢰 구조로 나누어 정리했습니다.",
                "QuestMission/AchievementMission 후보를 나누고, 신규 개발이 필요한 예외 케이스를 분리했습니다.",
                "일일 의뢰는 개인 플레이, 주간 의뢰는 길드 협동 목표 중심으로 성격을 구분했습니다.",
            ]
        ),
    ]
    right = [
        p("PvP TTK - 전투 공식 기반 제안", "SectionKo"),
        bullets(
            [
                "문제: 고전투력 구간에서 동급 PvP 전투 시간이 과도하게 짧아졌습니다.",
                "분석: 대미지 공식을 공격력, 스킬 배율, PvP 보정, 피해 증가, 이중 공격 단계로 나누어 확인했습니다.",
                "제안: 대미지 상한, 일괄 하향, 신규 PvP 방어 파라미터를 비교하고 세 번째 안을 우선 검토안으로 제시했습니다.",
                "기대 효과: PvE 영향은 최소화하면서 PvP 전투 판단 시간을 확보할 수 있습니다.",
            ]
        ),
        Spacer(1, 4 * mm),
        p("연락처", "SectionKo"),
        bullets(
            [
                "이메일: jjangsoo8571@gmail.com",
                "전화: 010-8048-8571",
                "웹 포트폴리오: https://haedtop.github.io/Leesoo/",
            ]
        ),
    ]
    columns = Table([[left, right]], colWidths=[82 * mm, 82 * mm])
    columns.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SURFACE),
                ("BOX", (0, 0), (-1, -1), 0.35, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(columns)

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    PUBLIC_PDF_PATH.write_bytes(PDF_PATH.read_bytes())
    print(PDF_PATH)
    print(PUBLIC_PDF_PATH)


if __name__ == "__main__":
    build_pdf()
