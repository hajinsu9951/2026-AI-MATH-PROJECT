# -*- coding: utf-8 -*-
"""step23: 포스터 원본 → 포스터 부문 수상 38선(대상5·최우수10·우수23, 보고서 수상과 별개)
비율 이상·보고서 표지형 자동 제외(썸네일 프로브)"""
import sys, re, os, json, subprocess
sys.stdout.reconfigure(encoding='utf-8')
SP = os.path.dirname(os.path.abspath(__file__))
from PIL import Image

d = json.load(open(os.path.join(SP, 'teams_summary.json'), encoding='utf-8'))
teams = d if isinstance(d, list) else d.get('teams', [])
order = {'대상': 0, '최우수': 1, '우수': 2, '장려': 3}
cands = [t for t in teams if t.get('poster_fid') and t.get('tier') in order]
cands.sort(key=lambda x: order[x['tier']])

CACHE = os.path.join(SP, '_poster_probe')
os.makedirs(CACHE, exist_ok=True)

def probe(fid):
    fp = os.path.join(CACHE, fid + '.bin')
    if not os.path.exists(fp) or os.path.getsize(fp) < 500:
        url = 'https://drive.google.com/thumbnail?id=%s&sz=w220' % fid
        subprocess.run(['curl', '-skL', '--max-time', '25', '-o', fp, url], capture_output=True)
    try:
        im = Image.open(fp).convert('RGB')
    except Exception:
        return None
    w, h = im.size
    g = im.convert('L')
    px = list(g.getdata())
    white = sum(1 for v in px if v > 238) / len(px)
    hsv = im.convert('HSV')
    sat = list(hsv.getdata())
    mean_s = sum(p[1] for p in sat) / len(sat)
    return {'aspect': w / h, 'white': white, 'sat': mean_s}

kept, dropped = [], []
for t in cands:
    m = probe(t['poster_fid'])
    if not m:
        dropped.append((t['title'][:28], 'no-image'))
        continue
    a = m['aspect']
    ratio_ok = (0.50 <= a <= 0.90) or (1.10 <= a <= 2.00)
    coverish = m['white'] > 0.72 and m['sat'] < 22
    ok = ratio_ok and not coverish
    t['_score'] = (0 if ok else 1, m['white'])  # 폴백 정렬용
    (kept if ok else dropped).append(t if ok else (t['title'][:28], 'a=%.2f w=%.2f s=%.0f' % (a, m['white'], m['sat'])))
    if not ok:
        t['_fallback'] = True

print('후보 %d → 통과 %d, 제외 %d' % (len(cands), len(kept), len(dropped)))
for x in dropped:
    print('  제외:', x)

seen, pool = set(), []
for t in kept:
    if t['poster_fid'] in seen:
        continue
    seen.add(t['poster_fid'])
    pool.append(t)
if len(pool) < 38:  # 폴백: 제외분 중 덜 표지형인 것부터 채움
    fb = [t for t in cands if t.get('_fallback') and t['poster_fid'] not in seen and '_score' in t]
    fb.sort(key=lambda x: x['_score'][1])
    for t in fb:
        if len(pool) >= 38:
            break
        seen.add(t['poster_fid'])
        pool.append(t)
    print('폴백 보충 후:', len(pool))
assert len(pool) >= 38, '통과 포스터 부족: %d' % len(pool)

G1, G2, G3 = pool[:5], pool[5:15], pool[15:38]

def fig(t):
    fid, title = t['poster_fid'], t['title'].replace('"', '')
    return ('<figure style="cursor:zoom-in;" onclick="return lbOpen(this)" data-big="https://drive.google.com/thumbnail?id=%s&sz=w1600">'
            '<span class="ro-badge">열람 전용</span>'
            '<img src="https://drive.google.com/thumbnail?id=%s&sz=w800" onerror="this.closest(\'figure\').style.display=\'none\'" alt="%s 포스터 원본(열람 전용)">'
            '<figcaption><b style="color:var(--navy);">%s</b></figcaption></figure>') % (fid, fid, title, title)

def strip(tag, cls, items):
    return ('  <div class="ps-group %s">%s</div>\n  <div class="poster-strip" oncontextmenu="return false">\n    %s\n  </div>\n'
            % (cls, tag, '\n    '.join(fig(t) for t in items)))

NEW = ('<div class="sub-title">학생 포스터 원본 — 포스터 부문 수상작 38선 <span style="font-weight:400; font-size:.75em; color:var(--sub);">'
       '(대상 5 · 최우수 10 · 우수 23 — 포스터 시상은 보고서 시상과 별개 · 클릭 확대 · 열람 전용)</span></div>\n'
       + strip('🏆 포스터 대상 — 5선', 'g1', G1)
       + strip('🥇 포스터 최우수 — 10선', 'g2', G2)
       + strip('🥈 포스터 우수 — 23선', 'g3', G3)
       + '\n  ')

p4b = open(os.path.join(SP, 'part4b_cases.html'), encoding='utf-8').read()
s = p4b.find('<div class="sub-title">학생 포스터 원본')
e = p4b.find('<div class="sub-title">숫자로 보는 성과')
assert 0 < s < e, (s, e)
p4b = p4b[:s] + NEW + p4b[e:]
open(os.path.join(SP, 'part4b_cases.html'), 'w', encoding='utf-8').write(p4b)
print('포스터 38선(5/10/23) 반영')

# CSS: 그룹 헤더
p1 = open(os.path.join(SP, 'part1_head.html'), encoding='utf-8').read()
if '.ps-group' not in p1:
    m = re.search(r'(\.hub-card \.hc-t \{[^}]*\})', p1)
    assert m
    p1 = p1.replace(m.group(1), m.group(1) + '''
  .ps-group { font-weight: 800; font-size: 14.5px; color: var(--navy); margin: 14px 0 6px; }
  .ps-group.g1 { color: #C25E00; }
  .ps-group.g2 { color: #1F4E79; }''', 1)
    open(os.path.join(SP, 'part1_head.html'), 'w', encoding='utf-8').write(p1)
    print('ps-group css ok')

# build.py: 로컬 포스터 placeholder 제거 (이제 미사용)
b = open(os.path.join(SP, 'build.py'), encoding='utf-8').read()
for ph in ['POSTER1', 'POSTER2', 'POSTER3', 'POSTER4', 'POSTER5', 'POSTER6']:
    b = re.sub(r'\s*\("\{\{B64_%s\}\}", "[^"]+", "jpeg"\),' % ph, '', b)
open(os.path.join(SP, 'build.py'), 'w', encoding='utf-8').write(b)
print('build.py placeholder 정리')
