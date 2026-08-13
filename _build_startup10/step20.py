# -*- coding: utf-8 -*-
"""step20: 갤러리 텍스트형(보고서 미리보기 전용) · 현장 스케치 업로드 일원화 ·
노션 7종 썸네일 · 신규 자료 4종(피그마/틱톡/캔바사이트2) · 문구 수정"""
import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')
SP = os.path.dirname(os.path.abspath(__file__))

def rd(p): return open(os.path.join(SP, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(SP, p), 'w', encoding='utf-8').write(s)

# ============ part1: CSS ============
p1 = rd('part1_head.html')
if '.thumb-card.txt' not in p1:
    m = re.search(r'(\.thumb-card \.tc-title \{[^}]*\})', p1)
    assert m, 'tc-title css'
    NEW_CSS = m.group(1) + '''
  .thumb-card.txt { flex-direction: column; }
  .thumb-card.txt .tc-body { padding: 13px 15px 12px; display: flex; flex-direction: column; gap: 5px; }
  .thumb-card.txt .tc-desc { font-size: 13px; color: var(--sub); line-height: 1.55; }
  .thumb-card.txt .tc-open { font-size: 12px; color: var(--blue); font-weight: 700; }
  #lb.report .lb-nav, #lb.report .lb-back { display: none; }'''
    p1 = p1.replace(m.group(1), NEW_CSS, 1)
    wr('part1_head.html', p1)
    print('part1 CSS ok')

# ============ part4: 자료 그리드 15종 ============
p4 = rd('part4_ws_canva_cases.html')
p4 = p4.replace('교사 개발 수업 자료 · 온라인 자료실 — 한눈에 11종', '교사 개발 수업 자료 · 온라인 자료실 — 한눈에 15종')
p4 = p4.replace('교사가 직접 개발한 캔바 자료 4종과 노션 자료실 7종을 한 그리드에 모았습니다.',
                '교사가 직접 개발한 캔바 자료 4종, 노션 BMC 자료실 7종, 그리고 피그마 앱 프로토타입·트렌드 리포트·캔바 퍼블리시 웹 2종까지 총 15종을 한 그리드에 모았습니다.')

NT_IMG = '<img class="cv-img" style="aspect-ratio:2/1; object-fit:cover; object-position:top;" src="{{B64_NT%d}}" alt="%s 노션 페이지 미리보기">'
for tile, n, alt in [
    ('<div class="cv-img tile">📚</div>', 1, '인공지능 수학 차시별 전체 자료실'),
    ('<div class="cv-img tile">💼</div>', 2, 'ABCDE 첨단산업 프로젝트 비즈니스 모델 수업 구성'),
    ('<div class="cv-img tile">🤖</div>', 3, 'AI — 시각장애인 음성 안내 자판기 BMC'),
    ('<div class="cv-img tile">🧬</div>', 4, 'Bio — 알레르기 안심 급식 앱 BMC'),
    ('<div class="cv-img tile">🎬</div>', 5, 'Culture&Content — 전통시장 숏폼 BMC'),
    ('<div class="cv-img tile">🚁</div>', 6, 'Defense&Aerospace — 소방관 구조 드론 BMC'),
    ('<div class="cv-img tile">⚡</div>', 7, 'Energy — 교실 에너지 절약 BMC'),
]:
    assert tile in p4, tile
    p4 = p4.replace(tile, NT_IMG % (n, alt), 1)

ENERGY_END = '''<a class="cv-link" href="https://app.notion.com/p/dshskr/3-5-Energy-2797f8928da3806280d9d7f5a60fbaf0" target="_blank" rel="noopener">열기 →</a></div>
    </div>'''
NEW_CARDS = ENERGY_END + '''
    <div class="canva-card">
      <img class="cv-img" style="aspect-ratio:2/1; object-fit:cover; object-position:top;" src="{{B64_FIGMA}}" alt="Safe Meal 알레르기 안심 급식 앱 피그마 프로토타입 미리보기">
      <div class="cv-body"><div class="cv-kind">FIGMA MAKE · 앱 프로토타입</div><div class="cv-title">Safe Meal — 알레르기 안심 급식 앱 프로토타입 (Bio BMC 연계)</div>
      <a class="cv-link" href="https://www.figma.com/make/23IibBpEdvVcc9o5kOiKwb/Safe-Meal-App-for-Allergic-Students?node-id=0-4" target="_blank" rel="noopener">열기 →</a></div>
    </div>
    <div class="canva-card">
      <img class="cv-img" style="aspect-ratio:2/1; object-fit:cover; object-position:top;" src="{{B64_TIKTOK}}" alt="TikTok What's Next 2025 트렌드 리포트 표지 미리보기">
      <div class="cv-body"><div class="cv-kind">PDF · 트렌드 리포트 38p</div><div class="cv-title">TikTok What&#39;s Next 2025 — 숏폼 트렌드 리포트 (Culture BMC 연계)</div>
      <a class="cv-link" href="https://ads.tiktok.com/business/library/TikTok_Whats_Next_2025_Trend_Report_ko_KR_v2.pdf" target="_blank" rel="noopener">열기 →</a></div>
    </div>
    <div class="canva-card">
      <img class="cv-img" style="aspect-ratio:2/1; object-fit:cover; object-position:top;" src="{{B64_CVS1}}" alt="캔바 퍼블리시 웹 앱 미리보기">
      <div class="cv-body"><div class="cv-kind">CANVA 퍼블리시 · 웹 앱</div><div class="cv-title">{{CVS1_TITLE}}</div>
      <a class="cv-link" href="https://daeshinmath.my.canva.site/untitled-app" target="_blank" rel="noopener">열기 →</a></div>
    </div>
    <div class="canva-card">
      <img class="cv-img" style="aspect-ratio:2/1; object-fit:cover; object-position:top;" src="{{B64_CVS2}}" alt="ABCDE 프로젝트 캔바 퍼블리시 웹 미리보기">
      <div class="cv-body"><div class="cv-kind">CANVA 퍼블리시 · 수업 허브</div><div class="cv-title">{{CVS2_TITLE}}</div>
      <a class="cv-link" href="https://daeshinmath.my.canva.site/abcde" target="_blank" rel="noopener">열기 →</a></div>
    </div>'''
if '{{B64_FIGMA}}' not in p4:
    assert ENERGY_END in p4
    p4 = p4.replace(ENERGY_END, NEW_CARDS, 1)
wr('part4_ws_canva_cases.html', p4)
print('part4 15종 ok')

# ============ part4b: 갤러리 텍스트형 + 스케치 일원화 + 문구 ============
p4b = rd('part4b_cases.html')

def tx(m):
    attrs, body = m.group(1), m.group(2)
    attrs = re.sub(r'\s+data-big="[^"]*"', '', attrs)
    attrs = attrs.replace('lbOpen(this)', 'lbReport(this)')
    dm = re.search(r'data-desc="([^"]*)"', attrs)
    d = dm.group(1) if dm else ''
    body += '<div class="tc-desc">핵심 원리 — ' + d + '</div><div class="tc-open">▶ 클릭 — 보고서 미리보기 (열람 전용)</div>'
    return '<a class="thumb-card txt"' + attrs + '>\n      <div class="tc-body">' + body + '</div>\n    </a>'

p4b, n = re.subn(r'<a class="thumb-card"([^>]*)>\s*<img class="tc-img"[^>]*>\s*<div class="tc-body">([\s\S]*?)</div>\s*</a>', tx, p4b)
print('갤러리 텍스트형 변환:', n)
assert n == 21, n

p4b = p4b.replace('※ 카드 클릭은 확대 보기만 실행되며 파일이 내려받아지지 않습니다. 미리보기 이미지는 구글 드라이브 열람 전용 썸네일입니다. 원문 열람은 아래 성과 아카이브에서 가능하며, 저장·다운로드는 잠겨 있습니다(교사 인증 시에만 해제).',
                  '※ 카드를 클릭하면 보고서 미리보기(열람 전용 뷰어)만 열립니다. 저장·다운로드 버튼은 잠겨 있으며, 원문 파일 접근은 교사 인증 시에만 해제됩니다.')

# 현장 스케치: 일러스트 삭제 → 업로드 보드로 교체
p4b = p4b.replace('현장 스케치 — 수업은 이렇게 흘러갑니다 <span style="font-weight:400; font-size:.75em; color:var(--sub);">(활동 재구성 일러스트)</span>',
                  '현장 스케치 — 수업은 이렇게 흘러갑니다 <span style="font-weight:400; font-size:.75em; color:var(--sub);">(사진 업로드 · 설명 기록 · 클릭 확대 · 얼굴 비식별 후 업로드)</span>')
s = p4b.find('  <div class="gal-grid">')
e = p4b.find('<div class="sub-title">학생 포스터 원본')
assert s > 0 and e > s, 'gal-grid range'
BOARD = '''  <div class="st-form">
    <input type="file" id="sk-file" accept="image/*" multiple>
    <input class="st-title" id="sk-cap" placeholder="사진 설명 입력 (예: 2차시 ○○사거리 현장 측정)">
    <button class="wg-btn alt" onclick="skAdd()">＋ 사진 추가</button>
    <span style="font-size:11px; color:var(--sub);">※ 올린 사진·설명은 이 브라우저에 저장됩니다. 모든 PC에 영구 반영하려면 docs 폴더에 lesson01~10.jpg로 넣거나 파일을 전달해 주세요.</span>
  </div>
  <div class="poster-strip" id="sk-board" oncontextmenu="return false"></div>

  '''
p4b = p4b[:s] + BOARD + p4b[e:]

# 하단 별도 기록 보드(photo-strip) 삭제
s2 = p4b.find('<div id="photo-strip">')
e2 = p4b.find('<div class="sub-title">숫자로 보는 성과')
assert s2 > 0 and e2 > s2, 'photo-strip range'
line_start = p4b.rfind('\n', 0, s2) + 1
p4b = p4b[:line_start] + p4b[e2:]
assert 'photo-strip' not in p4b
assert '사진을 올리고 설명을 달아 직접 기록하세요' not in p4b

# 문구: 응용 사례 선정
p4b = p4b.replace('지역 예선 1위·2위 — 수업 산출물이 그대로 출전작으로',
                  '지역 예선 1위·2위 — 수업 산출물 응용 사례로 선정')
wr('part4b_cases.html', p4b)
print('part4b ok / sk-board:', p4b.count('sk-board'))

# ============ part5: lbReport JS + lbClose + 빈 보드 안내 ============
p5 = rd('part5_assess_end.html')
LBOPEN = '''function lbOpen(el) {
  lbList = Array.prototype.slice.call(document.querySelectorAll('[data-big], .poster-strip figure'));
  lbIdx = lbList.indexOf(el);
  if (lbIdx < 0) { lbList.push(el); lbIdx = lbList.length - 1; }
  lbShow();
  return false;
}'''
LBREPORT = LBOPEN + '''
function lbReport(el) {
  var view = el.getAttribute('data-view') || '';
  if (!view) return false;
  var lb = document.getElementById('lb');
  lbList = []; lbIdx = 0;
  document.getElementById('lb-img').style.display = 'none';
  document.getElementById('lb-title').textContent = el.getAttribute('data-title') || '';
  var tier = el.getAttribute('data-tier') || '';
  var tEl = document.getElementById('lb-tier');
  if (tier) {
    tEl.style.display = 'inline-block';
    tEl.textContent = tier;
    tEl.className = 'tag ' + (tier === '대상' ? 'grand' : tier === '최우수' ? 'top' : 'good');
  } else tEl.style.display = 'none';
  var desc = el.getAttribute('data-desc') || '';
  document.getElementById('lb-desc').textContent = desc ? ' · ' + desc : '';
  document.getElementById('lb-href').style.display = 'none';
  lbViewUrl = view;
  document.getElementById('lb-frame').src = view;
  document.getElementById('lb-frame-wrap').style.display = 'block';
  lb.classList.add('report');
  lb.classList.add('on');
  return false;
}'''
if 'function lbReport' not in p5:
    assert LBOPEN in p5, 'lbOpen anchor'
    p5 = p5.replace(LBOPEN, LBREPORT, 1)

OLD_CLOSE = "function lbClose() { lbFrameClose(); document.getElementById('lb').classList.remove('on'); }"
NEW_CLOSE = "function lbClose() { lbFrameClose(); var lb = document.getElementById('lb'); lb.classList.remove('on'); lb.classList.remove('report'); }"
if OLD_CLOSE in p5:
    p5 = p5.replace(OLD_CLOSE, NEW_CLOSE, 1)

OLD_JOIN = """'</b></figcaption></figure>';
  }).join('');
}"""
NEW_JOIN = """'</b></figcaption></figure>';
  }).join('');
  if (!list.length) board.innerHTML = '<p style="font-size:12.5px; color:var(--sub); margin:4px 0;">아직 사진이 없습니다 — 위 [＋ 사진 추가] 버튼으로 수업 사진을 올리고 설명을 달아 현장을 기록해 보세요.</p>';
}"""
if OLD_JOIN in p5 and '아직 사진이 없습니다' not in p5:
    p5 = p5.replace(OLD_JOIN, NEW_JOIN, 1)
wr('part5_assess_end.html', p5)
print('part5 ok / lbReport:', 'function lbReport' in p5)
