# -*- coding: utf-8 -*-
"""step21: 갤러리 v2 — 포스터 좌측 + 역량·수학 원리 칩 + 우하단 보고서 읽기전용 버튼,
CANDOISM 제작 크레딧, 안내문 갱신"""
import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')
SP = os.path.dirname(os.path.abspath(__file__))

def rd(p): return open(os.path.join(SP, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(SP, p), 'w', encoding='utf-8').write(s)

# 카드별: (data-view 식별 substring, 포스터 fid, 역량 칩, 수학 원리 칩)
CARDS = [
    ('1lgbUUzbqHhaJOfKYwWuIj7UylI2ltqq9', '1fZ_LsoZs8_RGepf1zLYs9cAb8uyyudb_', '데이터기반 의사결정', '상관·회귀분석'),
    ('1bmMkDEnpmLYZHmGAE7MA7LFOP6LpgF1R', '1bmMkDEnpmLYZHmGAE7MA7LFOP6LpgF1R', '혁신성', '시뮬레이티드 어닐링 최적화'),
    ('14Klvki1UfW_9ncH1VBOjMFhzksQpV7cS', '1Th97awtWLxLbtguA96gFIGJRSoBxu0DX', '기회탐색·가치창출', '가중합 점수·파레토 최적화'),
    ('1hlxT2Tt62vXS6Nr2RyEvL0ksz_X1WJoO', '1pDKBRVOkwh1LdhSg7lD4qZCX45TErLYw', '데이터기반 의사결정', '손실함수 최소화'),
    ('18V71EZuf4iRtErR2-6DgG2WxgT_PB4R_', '1DQWh4tUUtjyEFKhMFMLa_xD94-hAf3pq', '회복탄력성', '몬테카를로 시뮬레이션·조합 최적화'),
    ('1nlkDTe4bZTAYFQ81sBuu7D1-shvcjSCS', '1nlkDTe4bZTAYFQ81sBuu7D1-shvcjSCS', '위험감수성', '포아송 회귀'),
    ('1kPmvhYqjG9b7bQ_MuqLhFZWZncmXeuqb', '1PNqBHq8R_i849Xd1Szh_Ij2WEcDOc4h8', '자원활용능력', '수요 비례 배분·격차 지수'),
    ('1L3RqWH8To_QLlrmBIrPtB6PLEESGWTh4', '1L3RqWH8To_QLlrmBIrPtB6PLEESGWTh4', '진취성', '다기준 랭킹 모델'),
    ('1qLCocewAbKXHwf5e52nPtg6yWBecIUE1', '1qLCocewAbKXHwf5e52nPtg6yWBecIUE1', '기회탐색·가치창출', '정규화·가중 결합 지수'),
    ('1mw3t2_4HE4dTK0YSUbfHh_subtnbeedy', '1-ZYmqn3bIXDr6sWJGZwOx3dK-zZUahRH', '혁신성', '생물모방 네트워크 최적화'),
    ('1jdBMbv7E-rwGSTOR9BObJ2j7rdIUyVSF', '1v4I4xwCrPoy_ssLygfZS6GDXF4FMSosT', '융합적 실행력', '거리 행렬·최단 순회(TSP)'),
    ('1sB8yA-x7OMOf8IWtaEPJALh_08-ws9KA', '1sB8yA-x7OMOf8IWtaEPJALh_08-ws9KA', '위험감수성', 'K-means 군집'),
    ('1uNYaxDH9H2NxheewBJp0wrla0QIPK90i', '1NQXvAvS7wQVRry38PLtnBo8KzQfH-Lt0', '데이터기반 의사결정', '다중회귀 분해'),
    ('1Ogh8HOzdtu2JnF7oxCyIrZlGJj8ly7aa', '1BPisegoX8yuEq6W7RO19QnLh7LBodcP6', '기회탐색·가치창출', 'XGBoost·특성 중요도'),
    ('1ikdSFnCEHy88uuLvLwfWQ504MWOEQB2o', '1n8FvEKPXtCrbDoOASmC2Dqf9RvNdsyqC', '위험감수성', '분류·예측 모델'),
    ('1kzHySmQ1-IRvZcqgmY5SEGupXRrfpTb4s6NXNb2XyJc', '1J3CS7ozhzD8rBsYDM7N7aBBSLiIC4KQj', '기회탐색·가치창출', '공간 가중 결합·시각화'),
    ('1lGmpD3PKdQZcU6kIJDsLEBSuo_q-toyp', '1lGmpD3PKdQZcU6kIJDsLEBSuo_q-toyp', '진취성', '수요예측 회귀'),
    ('1gdzn_dM9Qt2UK8A27P-Vlw7LTLFMCEoeu25ZZe5dc6A', '1gdzn_dM9Qt2UK8A27P-Vlw7LTLFMCEoeu25ZZe5dc6A', '융합적 실행력', '네트워크 중복도 분석'),
    ('11PRtxC5jVr2I99nnCv80ri-9WUYhXRmv', '17OWhVZQdll1nlJGnM0FuakoK8ziVqcXG', '데이터기반 의사결정', '포아송 모형·요인 분석'),
    ('16jHgF8WBnnlQtMKpdDxzVW5FqByZnhh4', '1no-BVnE0IPFc-UfxIlW7KBaTmpHG-uof', '데이터기반 의사결정', '상관 검정'),
    ('19jCPiUmUtAaAJ1475RCpPTsn4RzF2eQ3', '19jCPiUmUtAaAJ1475RCpPTsn4RzF2eQ3', '융합적 실행력', '위험 예측 모델·웹 구현'),
]

# ---------- part1: CSS ----------
p1 = rd('part1_head.html')
if '.tag.cap' not in p1:
    m = re.search(r'(#lb\.report \.lb-nav, #lb\.report \.lb-back \{ display: none; \})', p1)
    assert m, 'lb.report css anchor'
    NEW = m.group(1) + '''
  .tag.cap { background: #FFF1E0; color: #C25E00; border: 1px solid #F4C28A; }
  .tag.mathp { background: #E8F0FB; color: #1F4E79; border: 1px solid #B9CCDD; }
  .thumb-card .tc-body { display: flex; flex-direction: column; gap: 5px; padding: 12px 14px; flex: 1; }
  button.tc-open { border: 1px solid var(--line); background: #F4F8FC; border-radius: 8px; padding: 5px 11px;
    cursor: pointer; margin-top: auto; align-self: flex-end; font-weight: 700; color: var(--blue);
    font-size: 12px; font-family: inherit; }
  button.tc-open:hover { background: #E8F0FB; }
  .cv-note { font-size: 11.5px; color: var(--sub); margin-top: 3px; }'''
    p1 = p1.replace(m.group(1), NEW, 1)
    wr('part1_head.html', p1)
    print('part1 CSS ok')

# ---------- part4b: 갤러리 카드 v2 ----------
p4b = rd('part4b_cases.html')

def tx(m):
    attrs, body = m.group(1), m.group(2)
    attrs = attrs.replace(' onclick="return lbReport(this)"', '')
    view = re.search(r'data-view="([^"]*)"', attrs)
    title = re.search(r'data-title="([^"]*)"', attrs)
    v = view.group(1) if view else ''
    t = title.group(1) if title else ''
    card = next((c for c in CARDS if c[0] in v), None)
    assert card, 'no card map for ' + v[:60]
    _, fid, cap, mathp = card
    img = ('<img class="tc-img" src="https://drive.google.com/thumbnail?id=%s&sz=w480" '
           'onerror="this.style.display=\'none\'" alt="%s 포스터 미리보기(열람 전용)">') % (fid, t)
    # 칩 교체: lean 칩 → 역량 + 수학 원리
    body = re.sub(r'<span class="tag lean">[^<]*</span>',
                  '<span class="tag cap">🧭 %s</span><span class="tag mathp">∑ %s</span>' % (cap, mathp),
                  body, count=1)
    body = body.replace('<div class="tc-desc">핵심 원리 — ', '<div class="tc-desc">')
    body = body.replace('<div class="tc-open">▶ 클릭 — 보고서 미리보기 (열람 전용)</div>',
                        '<button class="tc-open" onclick="event.stopPropagation(); return lbReport(this.closest(\'.thumb-card\'))">📄 보고서 읽기 전용 →</button>')
    return '<a class="thumb-card" href="#"' + attrs + ' onclick="return false">\n      ' + img + '\n      <div class="tc-body">' + body + '</div>\n    </a>'

p4b, n = re.subn(r'<a class="thumb-card txt" href="#"([^>]*)>\s*<div class="tc-body">([\s\S]*?)</div>\s*</a>', tx, p4b)
print('갤러리 v2 변환:', n)
assert n == 21, n

p4b = p4b.replace('※ 카드를 클릭하면 보고서 미리보기(열람 전용 뷰어)만 열립니다. 저장·다운로드 버튼은 잠겨 있으며, 원문 파일 접근은 교사 인증 시에만 해제됩니다.',
                  '※ 좌측 포스터는 열람 전용 썸네일입니다. 각 카드 우하단 [📄 보고서 읽기 전용] 버튼으로만 원문 미리보기가 열리며, 저장·다운로드 버튼은 잠겨 있습니다. 칩: 🧭 기업가정신 핵심 역량 · ∑ 핵심 수학 원리.')
wr('part4b_cases.html', p4b)
print('part4b ok')

# ---------- part4: CANDOISM 크레딧 ----------
p4 = rd('part4_ws_canva_cases.html')
OLD_CANDO = '<div class="cv-kind">CANVA · 8p 튜토리얼</div><div class="cv-title">CANDOISM — 지역사회 문제 해결 + AI수학 + BMC</div>'
NEW_CANDO = OLD_CANDO.replace('</div><div class="cv-title">CANDOISM — 지역사회 문제 해결 + AI수학 + BMC</div>',
    '</div><div class="cv-title">CANDOISM — 지역사회 문제 해결 + AI수학 + BMC</div><div class="cv-note">아산 티쳐프러너 6기 하진수 외 4명 제작</div>')
if '아산 티쳐프러너 6기' not in p4:
    assert OLD_CANDO in p4, 'CANDO card'
    p4 = p4.replace(OLD_CANDO, NEW_CANDO, 1)
    wr('part4_ws_canva_cases.html', p4)
    print('CANDOISM 크레딧 ok')
