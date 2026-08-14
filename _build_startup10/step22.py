# -*- coding: utf-8 -*-
"""step22: 갤러리 포스터 잘림 수정(contain) · 포스터 원본 33선 확장 · 학생 산출물 통합 허브(전 팀 전수)"""
import sys, re, os, json
sys.stdout.reconfigure(encoding='utf-8')
SP = os.path.dirname(os.path.abspath(__file__))

def rd(p): return open(os.path.join(SP, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(SP, p), 'w', encoding='utf-8').write(s)

d = json.load(open(os.path.join(SP, 'teams_summary.json'), encoding='utf-8'))
teams = d if isinstance(d, list) else d.get('teams', [])

# ---------- part1: CSS ----------
p1 = rd('part1_head.html')
OLD_TI = '''  .thumb-card .tc-img {
    width: 108px; min-width: 108px; aspect-ratio: auto; object-fit: cover; object-position: top; display: block;
    background: linear-gradient(135deg, #E8F0F8, #D6E4F0); pointer-events: none; user-select: none;
  }'''
NEW_TI = '''  .thumb-card .tc-img {
    width: 126px; min-width: 126px; aspect-ratio: 707/1000; object-fit: contain; object-position: center; display: block;
    background: #FFFFFF; border-right: 1px solid var(--line); align-self: center; pointer-events: none; user-select: none;
  }'''
if OLD_TI in p1:
    p1 = p1.replace(OLD_TI, NEW_TI, 1)
    print('tc-img contain ok')
else:
    assert NEW_TI in p1, 'tc-img css missing'

if '.hub-grid' not in p1:
    m = re.search(r'(\.cv-note \{[^}]*\})', p1)
    assert m, 'cv-note anchor'
    HUB_CSS = m.group(1) + '''
  details.hub-wrap { margin: 8px 0 4px; }
  details.hub-wrap summary { cursor: pointer; font-weight: 700; color: var(--blue); padding: 9px 12px;
    border: 1px dashed var(--line); border-radius: 10px; background: #F7FAFD; font-size: 13.5px; }
  details.hub-wrap[open] summary { margin-bottom: 10px; }
  .hub-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(172px, 1fr)); gap: 10px; }
  .hub-card { border: 1px solid var(--line); border-radius: 10px; overflow: hidden; background: var(--card);
    text-decoration: none; color: inherit; display: flex; flex-direction: column; transition: transform .15s, box-shadow .15s; }
  .hub-card:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(20,45,80,.12); }
  .hub-card img { width: 100%; aspect-ratio: 4/3; object-fit: cover; object-position: top; display: block;
    background: #EFF4FA; pointer-events: none; user-select: none; }
  .hub-card .hc-t { font-size: 12px; padding: 8px 9px 9px; line-height: 1.45; }'''
    p1 = p1.replace(m.group(1), HUB_CSS, 1)
    print('hub css ok')
wr('part1_head.html', p1)

# ---------- part4b ----------
p4b = rd('part4b_cases.html')

# (1) 포스터 원본 33선
p4b = p4b.replace('학생 포스터 원본 11편 — 실물로 확인하는 완성도',
                  '학생 포스터 원본 — 우수 사례 33선, 실물로 확인하는 완성도')
EXCL = {'1fZ_LsoZs8_RGepf1zLYs9cAb8uyyudb_', '1Th97awtWLxLbtguA96gFIGJRSoBxu0DX',
        '1pDKBRVOkwh1LdhSg7lD4qZCX45TErLYw', '1PNqBHq8R_i849Xd1Szh_Ij2WEcDOc4h8',
        '1-ZYmqn3bIXDr6sWJGZwOx3dK-zZUahRH', '1DQWh4tUUtjyEFKhMFMLa_xD94-hAf3pq',
        '1v4I4xwCrPoy_ssLygfZS6GDXF4FMSosT'}
order = {'대상': 0, '최우수': 1, '우수': 2, '장려': 3}
cand, seen = [], set()
for t in sorted([t for t in teams if t.get('poster_fid')], key=lambda x: order.get(x.get('tier'), 9)):
    fid = t['poster_fid']
    if fid in EXCL or fid in seen or t.get('tier') not in order:
        continue
    seen.add(fid)
    cand.append(t)
ADD = cand[:22]
print('추가 포스터:', len(ADD))
assert len(ADD) == 22

figs = []
for t in ADD:
    fid, title, tier = t['poster_fid'], t['title'], t['tier']
    title_esc = title.replace('"', '')
    figs.append(('<figure style="cursor:zoom-in;" onclick="return lbOpen(this)" data-big="https://drive.google.com/thumbnail?id=%s&sz=w1600">'
                 '<span class="ro-badge">열람 전용</span>'
                 '<img src="https://drive.google.com/thumbnail?id=%s&sz=w800" onerror="this.closest(\'figure\').style.display=\'none\'" alt="%s 포스터 원본(열람 전용)">'
                 '<figcaption><b style="color:var(--navy);">%s</b> — %s</figcaption></figure>') % (fid, fid, title_esc, title_esc, tier))
K_END = '황색망사점균 타슈 최적화</b> — 생물 모방 네트워크 최적화 (대상)</figcaption></figure>'
assert K_END in p4b
p4b = p4b.replace(K_END, K_END + '\n    ' + '\n    '.join(figs), 1)

# (2) 학생 산출물 통합 허브
HUB_ANCHOR = '학생 개인 저장소 링크는 개인정보 보호를 위해 아카이브 경유로만 공개합니다.</p>'
assert HUB_ANCHOR in p4b
e = p4b.find(HUB_ANCHOR) + len(HUB_ANCHOR)
p4b = p4b[:e] + '\n\n  ' + '@@HUB@@' + p4b[e:]
e = p4b.find('@@HUB@@')
tiercls = {'대상': 'grand', '최우수': 'top', '우수': 'good', '장려': 'good'}
n_teams = len(teams)
n_members = sum(int(t.get('n_members') or 0) for t in teams)
hub_cards = []
for t in teams:
    fid = t.get('report_fid') or t.get('poster_fid')
    if not fid:
        continue
    thumb = t.get('thumb') or t.get('poster_fid') or fid
    tier = t.get('tier') or '출품'
    cls = tiercls.get(tier, 'lean')
    title = (t.get('title') or '').replace('"', '')
    hub_cards.append(('<a class="hub-card" href="#" data-view="https://drive.google.com/file/d/%s/preview" data-title="%s" data-tier="%s" onclick="return lbReport(this)">'
                      '<img src="https://drive.google.com/thumbnail?id=%s&sz=w300" loading="lazy" onerror="this.style.display=\'none\'" alt="%s 미리보기(열람 전용)">'
                      '<div class="hc-t"><span class="tag %s">%s</span> %s</div></a>')
                     % (fid, title, tier if tier != '출품' else '', thumb, title, cls, tier, title))
HUB = ('<div class="sub-title">학생 산출물 통합 허브 — 전 %d팀(%d명) 전수 열람 <span style="font-weight:400; font-size:.75em; color:var(--sub);">(카드 클릭 → 페이지 안 열람 전용 뷰어 · 저장·다운로드 잠금 · 깃허브 형태 산출물은 위 링크 모음)</span></div>\n'
       '  <details class="hub-wrap"><summary>▦ 팀별 산출물 %d건 전체 펼치기 — 보고서·포스터 열람 전용 뷰어로 바로 열립니다</summary>\n'
       '  <div class="hub-grid">\n    %s\n  </div></details>') % (n_teams, n_members, len(hub_cards), '\n    '.join(hub_cards))
p4b = p4b.replace('@@HUB@@', HUB, 1)
print('허브 카드:', len(hub_cards))

wr('part4b_cases.html', p4b)
print('part4b ok')
