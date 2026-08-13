# -*- coding: utf-8 -*-
"""갤러리: 포스터 썸네일+탐구 설명 / 전용 뷰어(팝아웃 차단) / 차시별 현장 사진 10슬롯"""
import sys, re, json, os
sys.stdout.reconfigure(encoding='utf-8')
SP = os.path.dirname(os.path.abspath(__file__))
teams = {t['id']: t for t in json.load(open(os.path.join(SP, 'teams_summary.json'), encoding='utf-8'))}

CARDS = [
 ('T_택지_구승훈', '대상', '대전·충남 택지개발지구 입지 패턴과 인구 관계 분석', '', '입지 패턴과 인구의 상관을 공간 데이터·회귀로 분석'),
 ('T_교사이동_임종혁', '대상', '교사 이동부담 원인 분석과 재배치 최적화', 'QAP·담금질', '이동부담을 초 단위로 정량화하고 담금질로 재배치안 도출'),
 ('T_CMCS_송리안', '대상', '어린이 이동제약점수(CMCS) 기반 안전 통학경로 추천 AI', '가중합·파레토', '위험 요인 가중합 점수 + 파레토 경로 — 위험 24.09% 감소'),
 ('T_쿨링포그_김해환', '대상', 'AI 기반 쿨링포그 설치·운영 최적화 모델', '', '폭염 데이터를 결합해 설치 입지와 가동 시간을 최적화'),
 ('T_교실배치_이준석', '대상', '학생 이동시간 최소화 교실 배치 시뮬레이션·최적화', 'Dijkstra·어닐링', '평균 이동 52.28→49.16초, 혼잡 13% 감소 — 60,000회 탐색'),
 ('T_통학로_이연호', '대상', '보차혼용 통학로 위험의 포아송 회귀 분석', '포아송 회귀', '사고 건수를 포아송 회귀로 계수화해 위험 요인 서열화'),
 ('T_버스배차_최예준', '대상', '시내버스 배차 적정성 분석 — 수요비례 재배분 모델', '', '노선별 수요 대비 배차 간격의 불균형을 진단·재배분'),
 ('T_빗물_이승찬', '대상', '집중호우 취약지역 임시 빗물저류 후보지 우선순위 추천 AI', '', '침수 취약지 데이터를 랭킹 모델로 — 후보지 우선순위'),
 ('T_폭염_이동원', '대상', '버스 이용량·폭염 결합 도시 열환경 취약도 모델링', '정규화·회귀', '이용량×폭염일수를 정규화 결합해 취약도 지수화'),
 ('T_타슈점균_이상찬', '대상', '황색망사점균 알고리즘 기반 타슈 대여소 최적화', '생물 모방 최적화', '점균의 경로 형성 원리를 모방해 대여소 배치를 재설계'),
 ('T_폐의약품_최민준', '최우수', '역물류 알고리즘 기반 폐의약품 수거 최적 경로 설계', '경로 최적화', '20개 거점 거리 행렬로 최단 순회 — 교차·중복 제거'),
 ('S30911', '최우수', 'K-means 기반 CCTV 사각지대 분석과 실시간 안심 가이드 지도', 'K-means', '군집 중심에서 먼 공백 지대를 사각지대로 정의해 지도화'),
 ('T_호텔_임홍재', '최우수', '호텔 등급을 고려한 호텔 위치 프리미엄 분석', '회귀 분석', '등급·입지 변수로 가격 프리미엄을 회귀 분해'),
 ('T_입양_최지훈', '최우수', 'XGBoost 기반 유기동물 입양 여부 예측 모델', 'XGBoost', '입양 여부를 예측하고 특성 중요도로 개선점 제안'),
 ('S30717', '최우수', '하상주차장 위험예측 모델 제작', '위험 예측', '강수·수위 데이터로 하상주차장 침수 위험을 예측'),
 ('S30204', '최우수', '교통약자 인구분포·사고심각도 기반 교통사고 취약지역 예측·시각화', '공간 분석', '교통약자 분포와 사고 심각도를 겹쳐 취약지 예측·시각화'),
 ('S30310', '최우수', '공영주차장 수요예측 모델과 입지 최적화 방안', '수요 예측', '수요 예측 모델로 신규 공영주차장 입지를 제안'),
 ('S30719', '최우수', '트램 도입 이후 버스노선 최적화', '노선 최적화', '트램 개통 시나리오에서 중복 노선을 재설계'),
 ('S30722', '최우수', '보차혼용 통학로 행동·환경 요인 분석과 통학 안전 개선', '포아송 회귀', '행동·환경 요인을 포아송 모형으로 — 개선안 제시'),
 ('S30908', '최우수', '관광객 증가와 주민 이탈의 상관관계 분석 모델', '상관 분석', '관광객 증가와 주민 이탈 지표의 상관을 검정'),
 ('S30910', '장려', '낚시 어선 사고위험 예측·안전항로 추천 AI 웹 제작', '웹 서비스 구현', '사고위험 예측과 안전항로 추천을 웹 서비스로 구현'),
]
TIER_CLS = {'대상': 'grand', '최우수': 'top', '장려': 'good'}
D480 = 'https://drive.google.com/thumbnail?id={}&sz=w480'
D1600 = 'https://drive.google.com/thumbnail?id={}&sz=w1600'

cards_html = []
for tid, tier, title, tag, desc in CARDS:
    t = teams[tid]
    poster = t.get('poster_fid') or t.get('thumb') or t.get('report_fid')
    report = t.get('report_fid') or poster
    view = f'https://drive.google.com/file/d/{report}/preview' if len(report) <= 40 else f'https://docs.google.com/document/d/{report}/preview'
    tag_html = f'<span class="tag math">{tag}</span>' if tag else ''
    if tid == 'S30910':
        tag_html = '<span class="tag lean">웹 서비스 구현</span>'
    cards_html.append(
        f'''    <a class="thumb-card" href="#" data-view="{view}" data-big="{D1600.format(poster)}" data-title="{title}" data-tier="{tier}" data-desc="{desc}" onclick="return lbOpen(this)">
      <img class="tc-img" onerror="this.style.display='none'" src="{D480.format(poster)}" alt="{title} 포스터 미리보기">
      <div class="tc-body"><div class="tc-tags"><span class="tag {TIER_CLS[tier]}">{tier}</span>{tag_html}</div><div class="tc-title">{title}</div></div>
    </a>''')
GRID = '<div class="thumb-grid">\n' + '\n'.join(cards_html) + '\n  </div>'

p4b = open(os.path.join(SP, 'part4b_cases.html'), encoding='utf-8').read()
p4b = re.sub(r'<div class="thumb-grid">[\s\S]*?\n  </div>(\n  <p style="font-size:)', GRID + r'\1', p4b, count=1)
assert p4b.count('thumb-card') >= 21

# 갤러리 안내 문구
p4b = p4b.replace('[원문 열람]은 자동 다운로드가 없는 드라이브 뷰어로 열립니다.',
                  '확대 화면의 [원문 열람]은 <b>페이지 안 전용 뷰어</b>로만 열리며, 새 창·다운로드 진입 버튼은 차단됩니다.')

# ---- 현장 스케치: 차시별 사진 10슬롯 (photo-strip 대체) ----
LP = '\n'.join(
    f'''      <figure style="cursor:zoom-in;" onclick="return lbOpen(this)"><img src="lesson{n:02d}.jpg" alt="{n}차시 활동 사진" onerror="this.closest('figure').style.display='none'; photoCheck()"><figcaption><b style="color:var(--navy);">{n}차시</b> — 활동 설명을 여기에 적어 주세요</figcaption></figure>'''
    for n in range(1, 11))
pat = re.compile(r'(<div id="photo-strip">)[\s\S]*?(</div>\n  <script>)')
m = pat.search(p4b)
assert m, 'photo-strip not found'
NEW_PS = (m.group(1) + '\n    <div class="sub-title">차시별 실제 수업 사진 <span style="font-weight:400; font-size:.75em; color:var(--sub);">(lesson01.jpg~lesson10.jpg를 docs 폴더에 넣으면 자동 표시 · 클릭 확대 · 없으면 숨김)</span></div>\n'
          + '    <div class="poster-strip" oncontextmenu="return false">\n' + LP + '\n    </div>\n  ' + m.group(2))
p4b = p4b[:m.start()] + NEW_PS + p4b[m.end():]
open(os.path.join(SP, 'part4b_cases.html'), 'w', encoding='utf-8').write(p4b)
print('갤러리 21편(포스터 우선+설명) · 차시별 사진 10슬롯 완료')

# ---- part5: 전용 뷰어(iframe+차단막) + 설명 표시 ----
p5 = open(os.path.join(SP, 'part5_assess_end.html'), encoding='utf-8').read()

OLD_LB = '''  <img id="lb-img" alt="확대 보기">
  <button class="lb-nav lb-next" onclick="lbStep(1)">›</button>
  <div class="lb-cap"><span id="lb-tier" class="tag grand" style="display:none;"></span><b id="lb-title"></b><a id="lb-href" class="wg-btn alt" target="_blank" rel="noopener" style="display:none;">원문 열람 →</a></div>'''
NEW_LB = '''  <img id="lb-img" alt="확대 보기">
  <div id="lb-frame-wrap">
    <iframe id="lb-frame" title="원문 전용 뷰어" allow=""></iframe>
    <div class="lb-shield" title="열람 전용"></div>
    <button class="lb-back" onclick="lbFrameClose()">← 확대 이미지로</button>
  </div>
  <button class="lb-nav lb-next" onclick="lbStep(1)">›</button>
  <div class="lb-cap"><span id="lb-tier" class="tag grand" style="display:none;"></span><b id="lb-title"></b><span id="lb-desc"></span><button id="lb-href" class="wg-btn alt" onclick="lbFrame()" style="display:none;">원문 열람 (전용 뷰어)</button></div>'''
assert OLD_LB in p5
p5 = p5.replace(OLD_LB, NEW_LB, 1)

OLD_SHOW = '''  var hEl = document.getElementById('lb-href');
  if (href) { hEl.style.display = 'inline-block'; hEl.href = href; } else hEl.style.display = 'none';
  document.getElementById('lb').classList.add('on');'''
NEW_SHOW = '''  var hEl = document.getElementById('lb-href');
  lbViewUrl = href || '';
  hEl.style.display = href ? 'inline-block' : 'none';
  var dEl = document.getElementById('lb-desc');
  var desc = el.getAttribute('data-desc') || '';
  dEl.textContent = desc ? ' · ' + desc : '';
  lbFrameClose();
  document.getElementById('lb').classList.add('on');'''
assert OLD_SHOW in p5
p5 = p5.replace(OLD_SHOW, NEW_SHOW, 1)

p5 = p5.replace('var lbList = [], lbIdx = 0;', '''var lbList = [], lbIdx = 0, lbViewUrl = '';
function lbFrame() {
  if (!lbViewUrl) return;
  document.getElementById('lb-frame').src = lbViewUrl;
  document.getElementById('lb-img').style.display = 'none';
  document.getElementById('lb-frame-wrap').style.display = 'block';
}
function lbFrameClose() {
  var w = document.getElementById('lb-frame-wrap');
  if (!w) return;
  w.style.display = 'none';
  document.getElementById('lb-frame').src = 'about:blank';
  document.getElementById('lb-img').style.display = '';
}
''', 1)
p5 = p5.replace("function lbClose() { document.getElementById('lb').classList.remove('on'); }",
                "function lbClose() { lbFrameClose(); document.getElementById('lb').classList.remove('on'); }", 1)
open(os.path.join(SP, 'part5_assess_end.html'), 'w', encoding='utf-8').write(p5)
print('전용 뷰어 JS 완료')

# ---- part1: 뷰어 CSS ----
p1 = open(os.path.join(SP, 'part1_head.html'), encoding='utf-8').read()
CSS = '''  #lb-frame-wrap { display: none; position: relative; width: min(920px, 92vw); height: 74vh; }
  #lb-frame { width: 100%; height: 100%; border: none; border-radius: 10px; background: #fff; }
  .lb-shield { position: absolute; top: 0; right: 0; width: 76px; height: 76px; z-index: 3; cursor: not-allowed;
    background: linear-gradient(225deg, rgba(20,33,61,.92) 0 46%, transparent 47%); border-radius: 0 10px 0 0; }
  .lb-shield::after { content: "열람 전용"; position: absolute; top: 12px; right: 6px; color: #FFD166; font-size: 10px; font-weight: 800; transform: rotate(45deg); }
  .lb-back { position: absolute; bottom: 10px; left: 10px; z-index: 3; background: rgba(20,33,61,.85); color: #fff; border: none; border-radius: 9px; padding: 9px 15px; font-size: 12.5px; font-weight: 700; cursor: pointer; font-family: inherit; }
  #lb-desc { color: #C9DDF2; font-size: 13px; }
'''
if '#lb-frame-wrap' not in p1:
    p1 = p1.replace('  /* ---- 이전 위치로 버튼 ---- */', CSS + '  /* ---- 이전 위치로 버튼 ---- */', 1)
    open(os.path.join(SP, 'part1_head.html'), 'w', encoding='utf-8').write(p1)
    print('뷰어 CSS 완료')

# ---- make_blind: 제출용에서 원문 열람 자체 제거 ----
mb = open(os.path.join(SP, 'make_blind.py'), encoding='utf-8').read()
if 'data-view' not in mb:
    mb = mb.replace("s = s.replace('app.notion.com/p/dshskr/', 'app.notion.com/p/')",
                    "s = s.replace('app.notion.com/p/dshskr/', 'app.notion.com/p/')\n"
                    "s = re.sub(r' data-view=\"[^\"]*\"', '', s)  # 제출용: 원문 열람(실명 노출 소지) 비활성화")
    open(os.path.join(SP, 'make_blind.py'), 'w', encoding='utf-8').write(mb)
    print('make_blind: data-view 제거 추가')
