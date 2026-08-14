# -*- coding: utf-8 -*-
"""step27: 보고서 뷰어(lbReport)에 이전/다음 넘김 — 같은 그리드의 학생 사례를 연속 열람"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
SP = os.path.dirname(os.path.abspath(__file__))

def rd(p): return open(os.path.join(SP, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(SP, p), 'w', encoding='utf-8').write(s)

# CSS: report 모드에서도 좌우 화살표 표시 (되돌아가기 버튼만 숨김)
p1 = rd('part1_head.html')
OLD = '#lb.report .lb-nav, #lb.report .lb-back { display: none; }'
NEW = '#lb.report .lb-back { display: none; }'
if OLD in p1:
    p1 = p1.replace(OLD, NEW, 1)
    wr('part1_head.html', p1)
    print('CSS ok')
else:
    assert NEW in p1
    print('CSS 이미 적용')

# JS: lbReport 목록형 + lbStep 분기
p5 = rd('part5_assess_end.html')
OLD_REP = """function lbReport(el) {
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
}"""
NEW_REP = """var lbRepList = [], lbRepIdx = 0;
function lbReport(el) {
  var view = el.getAttribute('data-view') || '';
  if (!view) return false;
  var container = el.closest('.thumb-grid, .hub-grid');
  if (container) {
    lbRepList = Array.prototype.filter.call(container.querySelectorAll('a[data-view]'), function (c) {
      return c.getAttribute('data-view');
    });
  } else lbRepList = [el];
  lbRepIdx = lbRepList.indexOf(el);
  if (lbRepIdx < 0) { lbRepList = [el]; lbRepIdx = 0; }
  lbRepShow();
  return false;
}
function lbRepShow() {
  var el = lbRepList[lbRepIdx];
  if (!el) return;
  var lb = document.getElementById('lb');
  lbList = []; lbIdx = 0;
  document.getElementById('lb-img').style.display = 'none';
  var cnt = lbRepList.length > 1 ? '  (' + (lbRepIdx + 1) + ' / ' + lbRepList.length + ')' : '';
  document.getElementById('lb-title').textContent = (el.getAttribute('data-title') || '') + cnt;
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
  lbViewUrl = el.getAttribute('data-view');
  document.getElementById('lb-frame').src = lbViewUrl;
  document.getElementById('lb-frame-wrap').style.display = 'block';
  lb.classList.add('report');
  lb.classList.add('on');
}"""
assert OLD_REP in p5, 'lbReport anchor missing'
p5 = p5.replace(OLD_REP, NEW_REP, 1)

OLD_STEP = "function lbStep(d) { if (!lbList.length) return; lbIdx = (lbIdx + d + lbList.length) % lbList.length; lbShow(); }"
NEW_STEP = """function lbStep(d) {
  if (document.getElementById('lb').classList.contains('report')) {
    if (lbRepList.length < 2) return;
    lbRepIdx = (lbRepIdx + d + lbRepList.length) % lbRepList.length;
    lbRepShow();
    return;
  }
  if (!lbList.length) return;
  lbIdx = (lbIdx + d + lbList.length) % lbList.length;
  lbShow();
}"""
assert OLD_STEP in p5, 'lbStep anchor missing'
p5 = p5.replace(OLD_STEP, NEW_STEP, 1)
wr('part5_assess_end.html', p5)
print('JS ok')
