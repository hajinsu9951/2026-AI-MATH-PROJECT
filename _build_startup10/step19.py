# -*- coding: utf-8 -*-
"""갤러리 제목형 재구성 · 현장 스케치 업로드 보드 · CUSTD 카드 삭제 · 링크 모음 명명"""
import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')
SP = os.path.dirname(os.path.abspath(__file__))

# ---------- part1: 갤러리 제목형 CSS + 스케치 폼 ----------
p1 = open(os.path.join(SP, 'part1_head.html'), encoding='utf-8').read()
OLD_TG = '''  .thumb-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(215px, 1fr)); gap: 14px; margin: 16px 0; }'''
NEW_TG = '''  .thumb-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(340px, 1fr)); gap: 10px; margin: 16px 0; }'''
assert OLD_TG in p1
p1 = p1.replace(OLD_TG, NEW_TG, 1)

OLD_TC = '''  .thumb-card {
    background: var(--card); border: 1px solid var(--line); border-radius: 13px; overflow: hidden;
    cursor: pointer; transition: transform .18s, box-shadow .18s; display: flex; flex-direction: column;
  }'''
NEW_TC = '''  .thumb-card {
    background: var(--card); border: 1px solid var(--line); border-radius: 13px; overflow: hidden;
    cursor: pointer; transition: transform .18s, box-shadow .18s; display: flex; flex-direction: row; align-items: stretch;
  }'''
assert OLD_TC in p1
p1 = p1.replace(OLD_TC, NEW_TC, 1)

OLD_TI = '''  .thumb-card .tc-img {
    width: 100%; aspect-ratio: 4/3; object-fit: cover; object-position: top; display: block;
    background: linear-gradient(135deg, #E8F0F8, #D6E4F0); pointer-events: none; user-select: none;
  }'''
NEW_TI = '''  .thumb-card .tc-img {
    width: 108px; min-width: 108px; aspect-ratio: auto; object-fit: cover; object-position: top; display: block;
    background: linear-gradient(135deg, #E8F0F8, #D6E4F0); pointer-events: none; user-select: none;
  }'''
assert OLD_TI in p1
p1 = p1.replace(OLD_TI, NEW_TI, 1)
p1 = p1.replace('  .thumb-card .tc-title { font-size: 13.5px;', '  .thumb-card .tc-title { font-size: 15px;', 1)
open(os.path.join(SP, 'part1_head.html'), 'w', encoding='utf-8').write(p1)
print('갤러리 제목형 CSS 완료')

# ---------- part4: CUSTD 카드 삭제 + 카운트 수정 ----------
p4 = open(os.path.join(SP, 'part4_ws_canva_cases.html'), encoding='utf-8').read()
pat = re.compile(r'\s*<div class="canva-card">\s*<img class="cv-img portrait" src="\{\{B64_CUSTD\}\}"[\s\S]*?</div>\n    </div>')
p4, n = pat.subn('', p4, count=1)
print('CUSTD 카드 삭제:', n)
p4 = p4.replace('교사 개발 수업 자료 · 온라인 자료실 — 한눈에 12종', '교사 개발 수업 자료 · 온라인 자료실 — 한눈에 11종')
p4 = p4.replace('교사가 직접 개발한 캔바 자료 5종과 노션 자료실 7종을', '교사가 직접 개발한 캔바 자료 4종과 노션 자료실 7종을')
open(os.path.join(SP, 'part4_ws_canva_cases.html'), 'w', encoding='utf-8').write(p4)

# ---------- part4b: 현장 스케치 업로드 보드 ----------
p4b = open(os.path.join(SP, 'part4b_cases.html'), encoding='utf-8').read()
s = p4b.find('  <!-- 📷 차시별 수업 사진')
if s < 0:
    s = p4b.find('<div id="photo-strip">')
e_marker = '</script>'
e = p4b.find(e_marker, s)
assert s > 0 and e > s, 'photo region'
e += len(e_marker)
BOARD = '''  <div id="photo-strip">
    <div class="sub-title">현장 스케치 — 사진을 올리고 설명을 달아 직접 기록하세요 <span style="font-weight:400; font-size:.75em; color:var(--sub);">(이 브라우저에 저장 · 클릭 확대 · 얼굴 비식별 후 업로드)</span></div>
    <div class="st-form">
      <input type="file" id="sk-file" accept="image/*" multiple>
      <input class="st-title" id="sk-cap" placeholder="설명 입력 (예: 2차시 ○○사거리 현장 측정)">
      <button class="wg-btn alt" onclick="skAdd()">＋ 사진 추가</button>
      <span style="font-size:11px; color:var(--sub);">※ 여기 올린 사진은 이 브라우저에만 저장됩니다. 제출본·모든 PC에 영구 반영하려면 docs 폴더에 lesson01~10.jpg로 넣거나 파일을 전달해 주세요.</span>
    </div>
    <div class="poster-strip" id="sk-board" oncontextmenu="return false"></div>
  </div>
'''
p4b = p4b[:s] + BOARD + p4b[e:]

p4b = p4b.replace('<div class="sub-title">동적 산출물 · 저장소 링크 모음', '<div class="sub-title">웹·깃허브 형태 산출물 링크 모음')
open(os.path.join(SP, 'part4b_cases.html'), 'w', encoding='utf-8').write(p4b)
print('현장 스케치 업로드 보드 완료')

# ---------- part5: 스케치 보드 JS ----------
p5 = open(os.path.join(SP, 'part5_assess_end.html'), encoding='utf-8').read()
JS = '''
function skLoad() {
  try { return JSON.parse(localStorage.getItem('sketch-board') || '[]'); } catch (e) { return []; }
}
function skSave(list) {
  try { localStorage.setItem('sketch-board', JSON.stringify(list)); }
  catch (e) { alert('저장 공간이 가득 찼습니다 — 사진 수를 줄이거나 기존 사진을 삭제해 주세요.'); }
}
function skRender() {
  var board = document.getElementById('sk-board');
  if (!board) return;
  var list = skLoad();
  board.innerHTML = list.map(function (it, i) {
    return '<figure style="cursor:zoom-in; position:relative;" onclick="return lbOpen(this)">' +
      '<img src="' + it.img + '" alt="현장 사진">' +
      '<button class="st-x" style="position:absolute;top:6px;right:6px;" onclick="event.stopPropagation(); skDel(' + i + ')" title="삭제">✕</button>' +
      '<figcaption><b style="color:var(--navy);">' + (it.cap || '현장 스케치') + '</b></figcaption></figure>';
  }).join('');
}
function skDel(i) {
  var list = skLoad();
  list.splice(i, 1);
  skSave(list);
  skRender();
}
function skAdd() {
  var inp = document.getElementById('sk-file');
  var cap = (document.getElementById('sk-cap').value || '').trim();
  if (!inp.files || !inp.files.length) { inp.click(); return; }
  Array.prototype.forEach.call(inp.files, function (file) {
    var rd = new FileReader();
    rd.onload = function () {
      var im = new Image();
      im.onload = function () {
        var c = document.createElement('canvas');
        var scale = Math.min(1, 900 / im.width);
        c.width = Math.round(im.width * scale);
        c.height = Math.round(im.height * scale);
        c.getContext('2d').drawImage(im, 0, 0, c.width, c.height);
        var list = skLoad();
        list.push({ img: c.toDataURL('image/jpeg', 0.78), cap: cap });
        skSave(list);
        skRender();
      };
      im.src = rd.result;
    };
    rd.readAsDataURL(file);
  });
  inp.value = '';
  document.getElementById('sk-cap').value = '';
}
document.addEventListener('DOMContentLoaded', skRender);
'''
if 'function skAdd' not in p5:
    p5 = p5.replace('var ctaN = 1;', JS + 'var ctaN = 1;', 1)
    open(os.path.join(SP, 'part5_assess_end.html'), 'w', encoding='utf-8').write(p5)
    print('스케치 보드 JS 완료')
