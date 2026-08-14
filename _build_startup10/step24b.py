# -*- coding: utf-8 -*-
"""step24b: 드라이브 미리보기 렌더 불가(렌더 썸네일 부재) 최우수 6편 → 렌더 가능한 우수 팀으로 교체.
명세민 웹 사례(장려)는 이전 지시대로 유지."""
import sys, re, os, json
sys.stdout.reconfigure(encoding='utf-8')
SP = os.path.dirname(os.path.abspath(__file__))

d = json.load(open(os.path.join(SP, 'teams_summary.json'), encoding='utf-8'))
teams = d if isinstance(d, list) else d.get('teams', [])

def render_ok(t):
    img = t.get('img') or ''
    return img.startswith('data:image') and len(img) > 3000

by_fid = {t['report_fid']: t for t in teams if t.get('report_fid')}
p = open(os.path.join(SP, 'part4b_cases.html'), encoding='utf-8').read()

gal_fids = []
for m in re.finditer(r'<a class="thumb-card" href="#"[^>]*data-view="([^"]*)"', p):
    fm = re.search(r'/d/([A-Za-z0-9_\-]+)/preview', m.group(1))
    gal_fids.append(fm.group(1) if fm else '')

REMOVE = []
for fid in gal_fids:
    t = by_fid.get(fid)
    if t and not render_ok(t) and '낚시 어선' not in t['title']:
        REMOVE.append(fid)
print('교체 대상:', len(REMOVE))

order = {'우수': 0, '장려': 1}
pool = [t for t in teams if t.get('report_fid') and t['report_fid'] not in gal_fids
        and t.get('tier') in order and render_ok(t)]
pool.sort(key=lambda x: order[x['tier']])
repl = pool[:len(REMOVE)]
assert len(repl) == len(REMOVE), (len(repl), len(REMOVE))

def chips(title):
    t = title.lower()
    if 'k-means' in t or '군집' in t: return ('위험감수성', 'K-means 군집')
    if '포아송' in t: return ('데이터기반 의사결정', '포아송 회귀')
    if 'xgboost' in t or '랜덤포레스트' in t or 'tf-idf' in t or '분류' in t: return ('기회탐색·가치창출', '분류 모델·특성 중요도')
    if '회귀' in t or '상관' in t or '시계열' in t: return ('데이터기반 의사결정', '상관·회귀분석')
    if '최적' in t or '경로' in t or '배치' in t or 'mclp' in t or 'greedy' in t or '동선' in t: return ('융합적 실행력', '최적화 알고리즘')
    if '예측' in t: return ('데이터기반 의사결정', '예측 모델')
    if 'gis' in t or '분포' in t or '지도' in t or '입지' in t or '접근성' in t: return ('기회탐색·가치창출', '공간 데이터 분석')
    return ('데이터기반 의사결정', '데이터 분석·모델링')

tiercls = {'대상': 'grand', '최우수': 'top', '우수': 'good', '장려': 'good'}

def new_card(t):
    fid = t['report_fid']
    title = t['title'].replace('"', '')
    tier = t['tier']
    cap, mathp = chips(title)
    pf = t.get('poster_fid') or t.get('thumb') or fid
    desc = '문제 정의→데이터 수집→모델링→검증 전 과정을 담은 탐구 보고서'
    return ('<a class="thumb-card" href="#" data-view="https://drive.google.com/file/d/%s/preview" data-title="%s" data-tier="%s" data-desc="%s" onclick="return false">\n'
            '      <img class="tc-img" src="https://drive.google.com/thumbnail?id=%s&sz=w480" onerror="this.style.display=\'none\'" alt="%s 미리보기(열람 전용)">\n'
            '      <div class="tc-body"><div class="tc-tags"><span class="tag %s">%s</span><span class="tag cap">🧭 %s</span><span class="tag mathp">∑ %s</span></div>'
            '<div class="tc-title">%s</div><div class="tc-desc">%s</div>'
            '<button class="tc-open" onclick="event.stopPropagation(); return lbReport(this.closest(\'.thumb-card\'))">📄 보고서 읽기 전용 →</button></div>\n    </a>')\
        % (fid, title, tier, desc, pf, title, tiercls[tier], tier, cap, mathp, title, desc)

for i, fid in enumerate(REMOVE):
    pat = re.compile(r'<a class="thumb-card" href="#"[^>]*data-view="[^"]*%s[^"]*"[\s\S]*?</a>' % re.escape(fid))
    p, n = pat.subn(new_card(repl[i]), p, count=1)
    assert n == 1, fid
    print('  교체:', by_fid[fid]['title'][:26], '→', repl[i]['tier'], repl[i]['title'][:30])

# 갤러리 부제 갱신
p = re.sub(r'수상작 갤러리 21편 — [^<(]*', '수상작 갤러리 21편 — 대상 10 · 최우수 4 · 우수 6 · 웹 구현 사례 ', p)

# 허브에서도 렌더 불가 카드 제거
hub_removed = 0
for m in list(re.finditer(r'<a class="hub-card" href="#" data-view="https://drive\.google\.com/file/d/([A-Za-z0-9_\-]+)/preview"[\s\S]*?</a>', p)):
    t = by_fid.get(m.group(1))
    if t and not render_ok(t):
        p = p.replace(m.group(0), '', 1)
        hub_removed += 1
n_hub = p.count('hub-card')
p = re.sub(r'▦ 팀별 산출물 \d+건 전체 펼치기', '▦ 팀별 산출물 %d건 전체 펼치기' % n_hub, p)
print('허브 렌더불가 제거:', hub_removed, '→ 남은 허브:', n_hub)

open(os.path.join(SP, 'part4b_cases.html'), 'w', encoding='utf-8').write(p)
print('완료')
