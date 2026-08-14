# -*- coding: utf-8 -*-
"""v5: 상세설명 셀 클리핑 해결 — 개요·이론적 준거만 셀에 남기고,
편성표 이후 전부를 서식3 앞 '상세설명 계속' 별지(본문 문단)로 이동 + 파란색 재적용."""
import sys, os, shutil
sys.stdout.reconfigure(encoding='utf-8')
from pyhwpx import Hwp

OUT = r'C:/Users/user/AppData/Local/Temp/제출서식_1_2_3호_최종_v3.hwp'
PDF = r'C:/Users/user/AppData/Local/Temp/제출서식_1_2_3호_최종_v3.pdf'

hwp = Hwp(new=True, visible=False)
assert hwp.open(OUT)

def curly(s):
    out, opening = '', True
    for ch in s:
        if ch == "'":
            out += '‘' if opening else '’'
            opening = not opening
        else:
            out += ch
    return out

def find_any(s):
    for v in ((s,) if "'" not in s else (s, curly(s), s.replace("'", '’'), s.replace("'", '‘'))):
        if hwp.find(v, direction='Forward'):
            return True
    return False

def repl_once(find_s, new_s):
    hwp.MovePos(2)
    if find_any(find_s):
        hwp.insert_text(new_s)
        return 1
    return 0

NL = '\r\n'
TBL_HEAD = '◈ 10차시 교육과정 편성표(차시│8단계 매핑│핵심 활동 ▶산출물)'
TBL = [
    '1차시│1단계 창업 가치 탐색(필수)│창업가처럼 세상 보기: 역량 온도 자기진단(웹 10문항), 강점 상보형 팀 빌딩(3~4인 역할제), 지역 문제 브레인스토밍 ▶팀 캔버스·역량 사전 데이터',
    "2차시│2단계 문제인식│데이터로 문제 찾기: 공공데이터 교차 확인+현장 실측(스톱워치·기록지), '셀 수 있는가' 숫자 게이트, 문제 정의문 조립기 ▶문제 정의문 v1",
    '3차시│3단계 시장분석Ⅰ│AI 모델 원리 탐구Ⅰ: KNN 수식 정의(거리함수·k-다수결), 카드 30장 언플러그드 실습, 모델 선택 매트릭스 ▶모델 선택 근거서',
    "4차시│3단계 시장분석Ⅱ│AI 모델 원리 탐구Ⅱ: K-means 군집 실습(목적함수 J 감소 관찰), '군집 중심은 왜 평균인가' 이차함수·미분 증명, 평균·상관·회귀 실습기 ▶데이터 검증 리포트",
    '5차시│2단계 아이디어 발굴│발산과 수렴: 브레인라이팅 4-3-4(타이머 내장), 아이디어 히치하이킹, 데이터 근거 가치제안문 ▶팀 가치제안문',
    "6차시│5단계 창업계획 수립(선택)│비즈니스 모델 수립: BMC 9블록 웹 캔버스, Customer Discovery 고객 인터뷰 설계, '숫자 지표 1개 이상' 규칙 ▶팀 BMC v1",
    "7차시│6단계 자원 활용(선택)│이펙추에이션 실행 전략: 수중의 새·감당 가능 손실, 자원 인벤토리('구할 곳'을 사람·기관으로 구체화) ▶실행 계획서",
    '8차시│4단계 아이디어 구현Ⅰ│MVP 바이브 코딩: 생성형 AI 협업 코딩으로 수학 모델 탑재 프로토타입 제작 ▶MVP v1',
    '9차시│4단계 아이디어 구현Ⅱ│검증과 개선: 극한 테스트, 트러블슈팅 로그, 미완성 30초 공개(심리적 안전 장치) ▶MVP v2·오류 로그',
    '10차시│7·8단계 가치 실천·재해석(필수)│피칭과 성찰: 3분 부스 피칭, 모의 크라우드펀딩(가상 투자권·투자 근거 한 줄), 메타 성찰, 역량 온도 재측정(1차시와 수미상관 비교) ▶최종 포스터·성찰 데이터',
]
STRAT = '◈ 교수·학습 전략 — 각 차시 도입-전개-정리 단계표에 교사 발문·자료(◈)·유의점(※)·평가 요소(✔)를 명기하고 차시별 디딤 영상·자료 패키지를 내장하여, 웹페이지 하나로 어느 교사든 동일 품질의 수업을 재현할 수 있다(교사 전문성 의존도 최소화 = 보급 가능성).'
TOOLS = '◈ 학습지원도구 — 웹 구동형 도구 10종 자체 개발(KNN 카드 실습·K-means 군집 실습·모델 선택 퀴즈·데이터 분석 실습기·역량 자기진단·문제 정의문 조립기·웹 BMC 캔버스·수업 타이머 3종)으로 교수자-학습자 상호작용을 실시간화하고, 인쇄형 활동지 12종은 웹에서 A4 인쇄·Word 저장을 지원하며 차시별 사용 위치가 안내된다.'
MATHF = '◈ 교과 정합성(수학적 엄밀성) — KNN·K-means를 수식으로 형식 정의하고 "군집의 중심은 왜 평균인가"를 이차함수·미분으로 증명하는 탐구를 내장하여, 기업가정신 활동이 교과 성취기준 [12인수03-01·02](분류·예측), [12인수04-01·02](최적화)의 성취로 직결되도록 설계했다.'
MAPPING = "◈ 역량-차시 매핑(관찰 장면) — 혁신성(5차시 히치하이킹)·진취성(2차시 데이터 빈틈 탐색)·위험감수성(4차시 가설 기각의 공개 수용, 7차시 감당 가능 손실)·창업의지(10차시 펀딩·교외 대회 연계)·자원활용능력(7차시 인벤토리)·기회탐색과 가치창출(2·5차시 숫자 게이트·가치제안)·데이터기반 의사결정(3·4·6차시 '숫자 없는 주장은 받지 않는다')·회복탄력성(9차시 트러블슈팅 로그)·융합적 실행력(8차시 수학+코딩+지역 자원 결합)."
EVAL = '◈ 평가 설계 — 과정 중심 평가: 매 차시 관찰 체크(차시당 1점, 학교 공식 평가계획 수행평가 70%와 차시 단위 연동), 산출물 루브릭 4축(문제 정의의 측정가능성·수학적 타당성·BMC 정합성·피칭 설득력), 1↔10차시 역량 온도 수미상관 비교로 정의적 성장까지 측정. AI 활용 4원칙(금지가 아니라 출처 표기)과 데이터 윤리 수칙 내장.'
CASE = "◈ 구체 수업 예시(위험감수성·회복탄력성 함양 장면) — 교내 Wi-Fi 병목 팀: '5층이 가장 느릴 것' 가설 → 4개 층 RSSI 직접 실측 → K-means 군집 분석으로 가설 기각 → 원인 재분석 후 공유기 재배치안 도출·검증. 가설이 뒤집힌 과정을 포스터에 그대로 기록하게 하여 '실패=검증의 성공' 태도를 체득."
PROOF = '◈ 실증 성과 — 학기당 100명 정규 교과 운영, 성과공유회 29팀, 공개 아카이브 80팀, 수상작 갤러리 21편(열람 전용), 정량 성과 30종(통학 위험 24.09%↓, 이동시간 5.97%↓ 등), 청소년 창업경진대회 지역 1·2위 등 교외 확장.'
SPREAD = '◈ 확산·일반화 — 단일 HTML 배포(설치 불요), 지역 데이터 교체만으로 전국 이식 가능, 축소(6~8차시)·확장(20차시)·중학교 변형 가이드 포함. 모든 자료의 무단 복제·배포 금지 및 출처 표기 원칙 명시.'

MOVE = [TBL_HEAD] + TBL + [STRAT, TOOLS, MATHF, MAPPING, EVAL, CASE, PROOF, SPREAD]

# 1) 셀에서 이동 대상 문단 삭제
deleted = 0
for p in MOVE:
    deleted += repl_once(p, '')
print('셀에서 제거:', deleted, '/', len(MOVE))

# 셀 끝에 이어지는 안내 한 줄 추가 (이론적 준거 문단 뒤)
hwp.MovePos(2)
if find_any('더블 다이아몬드(발산↔수렴 2회)와 Gold Standard PBL 7요소가 활동의 질을 보증한다.'):
    hwp.HAction.Run('Cancel')
    hwp.HAction.Run('MoveLineEnd')
    hwp.insert_text(NL + '※ 10차시 교육과정 편성표·교수학습 전략·역량 매핑·평가 설계는 다음 쪽 [상세설명 계속] 참조.')
    print('셀 안내문 ok')

# 2) 서식3 제목 앞에 별지 삽입
hwp.MovePos(2)
if hwp.find('[서식 제3호] 개인정보 수집·활용 동의서', direction='Forward'):
    hwp.HAction.Run('Cancel')
    hwp.HAction.Run('MoveLineBegin')
    block = NL.join(['[상세설명 계속]', ''] + MOVE) + NL + NL
    hwp.insert_text(block)
    print('별지 삽입 ok')
else:
    print('서식3 제목 못 찾음!')

# 3) 파란색 재적용 (이동 문단 + 핵심)
blue_targets = [TBL_HEAD] + TBL + [MAPPING, EVAL, '[상세설명 계속]']
b = 0
for t in blue_targets:
    hwp.MovePos(2)
    if find_any(t):
        try:
            hwp.CharShapeTextColorBlue()
            b += 1
        except Exception:
            pass
hwp.HAction.Run('Cancel')
print('파란색:', b, '/', len(blue_targets))

# 4) 저장·PDF·배포
hwp.save_as(OUT)
hwp.save_as(PDF, format='PDF')
hwp.quit()
print('저장 ok', os.path.getsize(OUT) // 1024, 'KB')
for dst in [r'G:/다른 컴퓨터/학교컴퓨터/2026_AI_MATH/2026_창업교육_우수사례/제출서식_1_2_3호_최종_v3.hwp',
            r'E:/이것저것/수학관련/2026_창업/2026_창업/2026_창업 우수 사례 발표(교육부-2026.04.23)/제출서식_1_2_3호_최종_v3.hwp']:
    shutil.copyfile(OUT, dst)
print('배포 ok')

import fitz
d = fitz.open(PDF)
print('pages:', len(d))
tags = {}
for i in range(7, len(d)):
    t = d[i].get_text()
    if '교육과정 편성표' in t: tags.setdefault('편성표', i)
    if '역량-차시 매핑' in t: tags.setdefault('역량매핑', i)
    if '평가 설계' in t and '루브릭' in t: tags.setdefault('평가', i)
    if '개인정보 수집' in t and '작성자' in t: tags.setdefault('서식3', i)
    pix = d[i].get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
    pix.save(r'C:/Users/user/AppData/Local/Temp/ntcap/fin_p%02d.png' % i)
print('위치:', tags)
