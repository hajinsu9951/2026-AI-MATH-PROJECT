# -*- coding: utf-8 -*-
"""step28: 현장 스케치 — 차시별 실제 수업 사진 18장 임베드(제목 순), 클릭 확대"""
import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')
SP = os.path.dirname(os.path.abspath(__file__))

def rd(p): return open(os.path.join(SP, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(SP, p), 'w', encoding='utf-8').write(s)

PHOTOS = [
    ('PH01', '1차시', '창업 가치 탐색과 C-level 팀빌딩', '역량 자기진단을 근거로 CEO·CTO·CMO 역할을 나누는 롤플레잉 팀빌딩'),
    ('PH02', '2차시', '우리동네 문제 정의 — 액션러닝', '"이건 셀 수 있나요?" 숫자 게이트를 통과시키며 문제 정의문을 조립'),
    ('PH03', '3차시', 'K-means 원리 탐구 — 플립러닝', 'XOR 연산·거리 개념 판서와 함께 군집의 수학적 원리를 몸으로 익히기'),
    ('PH04', '3차시', 'CNN 필터 구성 수업 ①', '샤프닝·블러 필터의 합성곱 원리를 단계별로 탐구'),
    ('PH05', '3차시', 'CNN 필터 구성 수업 ②', '채널 조절 필터(1×1 Convolution)까지 — 모델 속 수학을 직접 확인'),
    ('PH06', '3차시', 'CNN 도구 활용 학생 사례', 'LayerCAM 시각화로 모델이 무엇을 보는지 학생이 직접 검증'),
    ('PH07', '4차시', '데이터로 가설 검증 — 문제중심학습', '독립·종속변수 가설을 세우고 실측 데이터로 1차 검증'),
    ('PH08', '5차시', '캔두이즘 아이디어 발굴', '분석 결과를 기회로 재해석 — 브레인라이팅과 히치하이킹'),
    ('PH09', '6차시', '비즈니스 모델 캔버스 구성', 'AI 기반 음성 안내 자판기 BMC — 9블록을 팀별로 조립'),
    ('PH10', '6차시', 'BMC 수업 — 린 스타트업 기반', 'CANDOISM 자료로 가치 제안과 고객 세그먼트를 검증'),
    ('PH11', '7차시', '이펙추에이션 — MVP 설계 ①', '수중의 새 원리로 가진 자원부터 세는 자원 인벤토리'),
    ('PH12', '7차시', 'MVP 설계·메이커톤 운영', '방과후 메이커톤으로 이어진 실행 — 감당 가능한 손실만 걸고 시작'),
    ('PH13', '8차시', '바이브 프로토타이핑', '"AI와 함께, 판단은 우리가" — 생성형 AI 협업 코딩으로 MVP 제작'),
    ('PH14', '9차시', '고도화·미완성 공개 — 애자일', '30초 공개와 트러블슈팅 로그로 실패를 학습 데이터로 전환'),
    ('PH15', '10차시', '성과공유회·모의 크라우드펀딩 ①', 'A3 포스터 부스 — 관람자마다 질문 하나가 의무'),
    ('PH16', '10차시', '성과공유회·모의 크라우드펀딩 ②', '가상 투자권과 투자 근거 한 줄로 시장의 평가를 경험'),
    ('PH17', '10차시', '성과공유회·모의 크라우드펀딩 ③', '포스터 전시장 전경 — 서로의 산출물을 검증하는 시간'),
    ('PH18', '수업 밖', '교육부 주관 창업교육 우수사례 발표 (2026.04.23)', '이 수업의 설계와 성과를 전국 교원 앞에서 공유'),
]

# ---------- part1: CSS ----------
p1 = rd('part1_head.html')
if '.ph-grid' not in p1:
    m = re.search(r'(\.ps-group\.g2 \{[^}]*\})', p1)
    assert m, 'ps-group anchor'
    CSS = m.group(1) + '''
  .ph-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(255px, 1fr)); gap: 12px; margin: 12px 0 18px; }
  .ph-grid figure { margin: 0; background: var(--card); border: 1px solid var(--line); border-radius: 12px;
    overflow: hidden; cursor: zoom-in; position: relative; transition: transform .15s, box-shadow .15s; }
  .ph-grid figure:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(20,45,80,.14); }
  .ph-grid img { width: 100%; aspect-ratio: 4/3; object-fit: cover; display: block; pointer-events: none; user-select: none; }
  .ph-tag { position: absolute; top: 8px; left: 8px; background: rgba(20,33,61,.88); color: #FFD166;
    font-weight: 800; font-size: 11.5px; padding: 4px 9px; border-radius: 999px; }
  .ph-grid figcaption { padding: 9px 11px 10px; font-size: 12px; line-height: 1.5; color: var(--sub); }
  .ph-grid figcaption b { display: block; color: var(--navy); font-size: 12.5px; margin-bottom: 2px; }'''
    p1 = p1.replace(m.group(1), CSS, 1)
    wr('part1_head.html', p1)
    print('CSS ok')

# ---------- part4b: 사진 그리드 삽입 ----------
p4b = rd('part4b_cases.html')
figs = []
for ph, tag, title, desc in PHOTOS:
    figs.append(('<figure onclick="return lbOpen(this)"><span class="ph-tag">%s</span>'
                 '<img src="{{B64_%s}}" alt="%s — %s 현장 사진">'
                 '<figcaption><b>%s</b>%s</figcaption></figure>') % (tag, ph, tag, title, title, desc))
GRID = '<div class="ph-grid">\n    ' + '\n    '.join(figs) + '\n  </div>\n  '
ANCHOR = '<div class="st-form">\n    <input type="file" id="sk-file"'
assert ANCHOR in p4b, 'st-form anchor'
if 'ph-grid' not in p4b:
    p4b = p4b.replace(ANCHOR, GRID + ANCHOR, 1)
    print('사진 그리드 삽입 (18장)')
p4b = p4b.replace('(사진 업로드 · 설명 기록 · 클릭 확대 · 얼굴 비식별 후 업로드)',
                  '(1~10차시 실제 수업 사진 · 클릭 확대 · 추가 사진은 아래 업로드)')
wr('part4b_cases.html', p4b)

# ---------- part5: lbOpen 목록에 ph-grid 포함 ----------
p5 = rd('part5_assess_end.html')
OLD = "lbList = Array.prototype.slice.call(document.querySelectorAll('[data-big], .poster-strip figure'));"
NEW = "lbList = Array.prototype.slice.call(document.querySelectorAll('[data-big], .poster-strip figure, .ph-grid figure'));"
if OLD in p5:
    p5 = p5.replace(OLD, NEW, 1)
    wr('part5_assess_end.html', p5)
    print('lbOpen 선택자 확장')
else:
    assert NEW in p5

# ---------- build.py placeholder ----------
b = rd('build.py')
if '{{B64_PH01}}' not in b:
    NEWB = ''.join('    ("{{B64_PH%02d}}", "ph%02d.jpg", "jpeg"),\n' % (i, i) for i in range(1, 19))
    b = b.replace('    ("{{B64_SW8}}", "sw8.jpg", "jpeg"),\n', '    ("{{B64_SW8}}", "sw8.jpg", "jpeg"),\n' + NEWB, 1)
    wr('build.py', b)
    print('build.py placeholder 18건')
print('완료')
