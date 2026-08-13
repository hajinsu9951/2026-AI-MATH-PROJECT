# -*- coding: utf-8 -*-
"""수상작 21편 갤러리 + 라이트박스 확대, 차시 바로가기, 사용법 안내, 데이터 윤리"""
import sys, os, re, json
sys.stdout.reconfigure(encoding='utf-8')
SP = os.path.dirname(os.path.abspath(__file__))

def rd(p): return open(os.path.join(SP, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(SP, p), 'w', encoding='utf-8').write(s)

teams = {t['id']: t for t in json.load(open(os.path.join(SP, 'teams_summary.json'), encoding='utf-8'))}

# (id, tier, 표시제목, 수학태그)
CARDS = [
 ('T_택지_구승훈', '대상', '대전·충남 택지개발지구 입지 패턴과 인구 관계 분석', ''),
 ('T_교사이동_임종혁', '대상', '교사 이동부담 원인 분석과 재배치 최적화', 'QAP·담금질'),
 ('T_CMCS_송리안', '대상', '어린이 이동제약점수(CMCS) 기반 안전 통학경로 추천 AI', '가중합·파레토'),
 ('T_쿨링포그_김해환', '대상', 'AI 기반 쿨링포그 설치·운영 최적화 모델', ''),
 ('T_교실배치_이준석', '대상', '학생 이동시간 최소화 교실 배치 시뮬레이션·최적화', 'Dijkstra·어닐링'),
 ('T_통학로_이연호', '대상', '보차혼용 통학로 위험의 포아송 회귀 분석', '포아송 회귀'),
 ('T_버스배차_최예준', '대상', '시내버스 배차 적정성 분석 — 수요비례 재배분 모델', ''),
 ('T_빗물_이승찬', '대상', '집중호우 취약지역 임시 빗물저류 후보지 우선순위 추천 AI', ''),
 ('T_폭염_이동원', '대상', '버스 이용량·폭염 결합 도시 열환경 취약도 모델링', '정규화·회귀'),
 ('T_타슈점균_이상찬', '대상', '황색망사점균 알고리즘 기반 타슈 대여소 최적화', '생물 모방 최적화'),
 ('T_폐의약품_최민준', '최우수', '역물류 알고리즘 기반 폐의약품 수거 최적 경로 설계', '경로 최적화'),
 ('S30911', '최우수', 'K-means 기반 CCTV 사각지대 분석과 실시간 안심 가이드 지도', 'K-means'),
 ('T_호텔_임홍재', '최우수', '호텔 등급을 고려한 호텔 위치 프리미엄 분석', '회귀 분석'),
 ('T_입양_최지훈', '최우수', 'XGBoost 기반 유기동물 입양 여부 예측 모델', 'XGBoost'),
 ('S30717', '최우수', '하상주차장 위험예측 모델 제작', '위험 예측'),
 ('S30204', '최우수', '교통약자 인구분포·사고심각도 기반 교통사고 취약지역 예측·시각화', '공간 분석'),
 ('S30310', '최우수', '공영주차장 수요예측 모델과 입지 최적화 방안', '수요 예측'),
 ('S30719', '최우수', '트램 도입 이후 버스노선 최적화', '노선 최적화'),
 ('S30722', '최우수', '보차혼용 통학로 행동·환경 요인 분석과 통학 안전 개선', '포아송 회귀'),
 ('S30908', '최우수', '관광객 증가와 주민 이탈의 상관관계 분석 모델', '상관 분석'),
 ('S30910', '장려', '낚시 어선 사고위험 예측·안전항로 추천 AI 웹 제작', '웹 서비스 구현'),
]
TIER_CLS = {'대상': 'grand', '최우수': 'top', '장려': 'good'}

def prev_url(fid):
    if len(fid) > 40:
        return f'https://docs.google.com/document/d/{fid}/preview'
    return f'https://drive.google.com/file/d/{fid}/preview'

cards_html = []
for tid, tier, title, tag in CARDS:
    t = teams[tid]
    thumb = t.get('thumb') or t.get('poster_fid') or t.get('report_fid')
    pv = t.get('report_fid') or t.get('poster_fid') or thumb
    tag_html = f'<span class="tag math">{tag}</span>' if tag else ''
    if tid == 'S30910':
        tag_html = '<span class="tag lean">웹 서비스 구현</span>'
    cards_html.append(f'''    <a class="thumb-card" href="{prev_url(pv)}" target="_blank" rel="noopener" data-big="https://drive.google.com/thumbnail?id={thumb}&sz=w1600" data-title="{title}" data-tier="{tier}" onclick="return lbOpen(this)">
      <img class="tc-img" onerror="this.style.display='none'" src="https://drive.google.com/thumbnail?id={thumb}&sz=w480" alt="{title} 미리보기">
      <div class="tc-body"><div class="tc-tags"><span class="tag {TIER_CLS[tier]}">{tier}</span>{tag_html}</div><div class="tc-title">{title}</div></div>
    </a>''')
GRID = '<div class="thumb-grid">\n' + '\n'.join(cards_html) + '\n  </div>'

p4b = rd('part4b_cases.html')
m = re.search(r'<div class="thumb-grid">[\s\S]*?\n  </div>\n  <p style="font-size:', p4b)
assert m, 'thumb-grid block not found'
p4b = p4b[:m.start()] + GRID + '\n  <p style="font-size:' + p4b[m.end() - len('\n  <p style="font-size:'):]  # noqa
# 위 방식이 취약하므로 정확 재조립
p4b = re.sub(r'<div class="thumb-grid">[\s\S]*?\n  </div>(\n  <p style="font-size:)', GRID + r'\1', rd('part4b_cases.html'), count=1)
assert p4b.count('thumb-card') >= 21, 'card gen failed'

p4b = p4b.replace('<div class="sub-title">수상작 갤러리 — 대상 10편 전작 + 주목할 산출물</div>',
                  '<div class="sub-title">수상작 갤러리 21편 — 대상 10 · 최우수 10 · 웹 구현 사례 <span style="font-weight:400; font-size:.72em; color:var(--sub);">(카드를 누르면 크게 보기 · 원문 열람)</span></div>')
p4b = p4b.replace('<b>카드를 클릭하면 해당 팀의 보고서·포스터 원문이 열람 전용 미리보기</b>로 열립니다(다운로드 버튼 없는 보기 화면).',
                  '<b>카드를 클릭하면 확대 화면(라이트박스)</b>이 열리고, [원문 열람] 버튼으로 해당 팀 보고서 전문을 열람 전용으로 볼 수 있습니다(다운로드 버튼 없는 보기 화면).')
# 포스터·사진도 확대 대상으로
p4b = p4b.replace('<figure><span class="ro-badge">열람 전용</span>', '<figure style="cursor:zoom-in;" onclick="return lbOpen(this)"><span class="ro-badge">열람 전용</span>')
p4b = p4b.replace('<figure><img src="photo', '<figure style="cursor:zoom-in;" onclick="return lbOpen(this)"><img src="photo')
wr('part4b_cases.html', p4b)
print('cards:', p4b.count('thumb-card'))

# ---- part1: 라이트박스 CSS + 사용법 안내 ----
p1 = rd('part1_head.html')
LBCSS = """
  /* ---- 라이트박스(확대 보기) ---- */
  #lb {
    position: fixed; inset: 0; background: rgba(8,14,28,.93); z-index: 300;
    display: none; flex-direction: column; align-items: center; justify-content: center; gap: 14px; padding: 26px;
  }
  #lb.on { display: flex; }
  #lb-img { max-width: 92vw; max-height: 74vh; border-radius: 10px; background: #fff; box-shadow: 0 20px 60px rgba(0,0,0,.5); }
  .lb-cap { color: #fff; font-size: 15px; text-align: center; display: flex; align-items: center; gap: 10px; flex-wrap: wrap; justify-content: center; max-width: 90vw; }
  .lb-x { position: absolute; top: 14px; right: 18px; background: rgba(255,255,255,.14); color: #fff; border: none; border-radius: 50%; width: 42px; height: 42px; font-size: 18px; cursor: pointer; }
  .lb-nav { position: absolute; top: 50%; transform: translateY(-50%); background: rgba(255,255,255,.12); color: #fff; border: none; border-radius: 12px; font-size: 34px; padding: 10px 14px; cursor: pointer; }
  .lb-nav:hover, .lb-x:hover { background: rgba(255,255,255,.28); }
  .lb-prev { left: 14px; } .lb-next { right: 14px; }

"""
p1 = p1.replace('  /* ---- 이전 위치로 버튼 ---- */', LBCSS + '  /* ---- 이전 위치로 버튼 ---- */', 1)

QUICK = """

<!-- 사용법 안내 -->
<div class="section" style="padding: 26px 22px 0;">
  <div class="info-box" style="margin: 0;">
    <div class="box-title">🧭 이 페이지 사용법 — 교사는 이렇게 씁니다 (설치·준비물 없음)</div>
    <p>① 상단 메뉴 또는 <b>차시 바로가기</b>에서 오늘 차시를 열면, 도입-전개-정리 단계표에 발문(💬)·자료(◈)·유의점(※)·평가 요소(✔)가 그대로 있습니다 — 화면을 보며 진행하면 됩니다.</p>
    <p>② 각 차시의 <b>자료 패키지 칩</b>을 누르면 활동지·웹 도구가 바로 열리고, 우하단 <b>↩ 이전 위치로</b> 버튼으로 지도안에 복귀합니다.</p>
    <p>③ 활동지는 [🖨 인쇄]로 그대로 배부하고, 타이머·KNN/K-means 실습기·분석 실습기·BMC 캔버스는 <b>화면에 크게 띄워 수업 도구</b>로 씁니다. (브라우저 Ctrl+P는 지도안 전체 인쇄)</p>
  </div>
</div>"""
anchor = '<div class="meta-card"><div class="label">검증 실적</div><div class="value">학기당 100명 · 29팀</div></div>\n  </div>\n</div>'
assert anchor in p1
p1 = p1.replace(anchor, anchor + QUICK, 1)
wr('part1_head.html', p1)

# ---- part3: 차시 바로가기 ----
p3 = rd('part3_lessons.html')
NAVCHIPS = """
  <div class="pack" style="margin-top:10px;"><span class="pk-label">차시 바로가기</span>""" + ''.join(
    f'<a class="pk" href="#lesson-{n}">{n}차시</a>' for n in range(1, 11)) + '</div>\n'
p3 = p3.replace('<button class="btn-expand" onclick="toggleAll(this)">전체 펼치기 ▼</button>',
                '<button class="btn-expand" onclick="toggleAll(this)">전체 펼치기 ▼</button>\n' + NAVCHIPS, 1)
wr('part3_lessons.html', p3)

# ---- part5: 윤리 박스 + 라이트박스 마크업/JS ----
p5 = rd('part5_assess_end.html')
ETHICS = """
  <div class="info-box green">
    <div class="box-title">개인정보 · 데이터 윤리 수칙 (수업 운영 원칙)</div>
    <p>▪ 산출물·사진 공개 시 학생 실명·학번·얼굴을 비식별 처리(뒷모습·모자이크)하고, 공개 범위를 사전에 안내합니다.</p>
    <p>▪ 공공데이터는 출처·기준 연도·라이선스를 표기하고, 직접 측정 데이터에 개인 식별 정보(차량번호·위치 이력 등)를 담지 않습니다.</p>
    <p>▪ 설문·인터뷰는 목적 고지와 동의 후 진행하며, 수집 자료는 프로젝트 종료 후 폐기 원칙을 지킵니다.</p>
  </div>
"""
p5 = p5.replace('  <div class="info-box">\n    <div class="box-title">학교생활기록부(세특) 연계 팁</div>',
                ETHICS + '  <div class="info-box">\n    <div class="box-title">학교생활기록부(세특) 연계 팁</div>', 1)

LB = """
<!-- 라이트박스 -->
<div id="lb" onclick="if (event.target === this) lbClose()">
  <button class="lb-x" onclick="lbClose()">✕</button>
  <button class="lb-nav lb-prev" onclick="lbStep(-1)">‹</button>
  <img id="lb-img" alt="확대 보기">
  <button class="lb-nav lb-next" onclick="lbStep(1)">›</button>
  <div class="lb-cap"><span id="lb-tier" class="tag grand" style="display:none;"></span><b id="lb-title"></b><a id="lb-href" class="wg-btn alt" target="_blank" rel="noopener" style="display:none;">원문 열람 →</a></div>
</div>
"""
p5 = p5.replace('<button id="backBtn" onclick="backGo()">↩ 이전 위치로</button>',
                '<button id="backBtn" onclick="backGo()">↩ 이전 위치로</button>\n' + LB, 1)

LBJS = """
var lbList = [], lbIdx = 0;
function lbOpen(el) {
  lbList = Array.prototype.slice.call(document.querySelectorAll('[data-big], .poster-strip figure'));
  lbIdx = lbList.indexOf(el);
  if (lbIdx < 0) { lbList.push(el); lbIdx = lbList.length - 1; }
  lbShow();
  return false;
}
function lbShow() {
  var el = lbList[lbIdx];
  if (!el) return;
  var img = el.querySelector('img');
  var big = el.getAttribute('data-big') || (img ? img.src : '');
  var title = el.getAttribute('data-title');
  if (!title) { var fc = el.querySelector('figcaption'); title = fc ? fc.textContent.trim().slice(0, 80) : ''; }
  var tier = el.getAttribute('data-tier') || '';
  var href = el.getAttribute('data-title') ? el.getAttribute('href') : '';
  document.getElementById('lb-img').src = big;
  document.getElementById('lb-title').textContent = title;
  var tEl = document.getElementById('lb-tier');
  if (tier) {
    tEl.style.display = 'inline-block';
    tEl.textContent = tier;
    tEl.className = 'tag ' + (tier === '대상' ? 'grand' : tier === '최우수' ? 'top' : 'good');
  } else tEl.style.display = 'none';
  var hEl = document.getElementById('lb-href');
  if (href) { hEl.style.display = 'inline-block'; hEl.href = href; } else hEl.style.display = 'none';
  document.getElementById('lb').classList.add('on');
}
function lbStep(d) { if (!lbList.length) return; lbIdx = (lbIdx + d + lbList.length) % lbList.length; lbShow(); }
function lbClose() { document.getElementById('lb').classList.remove('on'); }
document.addEventListener('keydown', function (e) {
  var lb = document.getElementById('lb');
  if (!lb || !lb.classList.contains('on')) return;
  if (e.key === 'Escape') lbClose();
  if (e.key === 'ArrowLeft') lbStep(-1);
  if (e.key === 'ArrowRight') lbStep(1);
});
"""
p5 = p5.replace('var backStack = [];', LBJS + 'var backStack = [];', 1)
wr('part5_assess_end.html', p5)
print('done')
