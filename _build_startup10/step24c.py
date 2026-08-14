# -*- coding: utf-8 -*-
"""step24c: 보고서 fid의 드라이브 렌더 썸네일 존재 여부로 미리보기 가용성 판정 →
불능 카드만 가용 팀으로 교체 (명세민 웹 사례 포함 전 카드 동일 기준)"""
import sys, re, os, json, subprocess
sys.stdout.reconfigure(encoding='utf-8')
SP = os.path.dirname(os.path.abspath(__file__))

d = json.load(open(os.path.join(SP, 'teams_summary.json'), encoding='utf-8'))
teams = d if isinstance(d, list) else d.get('teams', [])
by_fid = {t['report_fid']: t for t in teams if t.get('report_fid')}

CACHE = os.path.join(SP, '_rt_probe')
os.makedirs(CACHE, exist_ok=True)

def render_ok(fid):
    fp = os.path.join(CACHE, fid + '.bin')
    if not os.path.exists(fp):
        subprocess.run(['curl', '-skL', '--max-time', '25', '-o', fp,
                        'https://drive.google.com/thumbnail?id=%s&sz=w160' % fid], capture_output=True)
    try:
        head = open(fp, 'rb').read(4)
    except Exception:
        return False
    return head[:3] == b'\xff\xd8\xff' or head[:4] == b'\x89PNG' or head[:4] == b'RIFF' or head[:3] == b'GIF'

p = open(os.path.join(SP, 'part4b_cases.html'), encoding='utf-8').read()

gal = []
for m in re.finditer(r'<a class="thumb-card" href="#"[^>]*data-view="([^"]*)"[^>]*data-title="([^"]*)"[^>]*data-tier="([^"]*)"', p):
    fm = re.search(r'/d/([A-Za-z0-9_\-]+)/preview', m.group(1))
    gal.append({'fid': fm.group(1) if fm else '', 'view': m.group(1), 'title': m.group(2), 'tier': m.group(3)})
print('갤러리:', len(gal))

REMOVE = []
for g in gal:
    ok = render_ok(g['fid']) if g['fid'] else True  # docs.google 문서형은 통과 취급 후 개별 확인
    if 'docs.google.com' in g['view']:
        ok = True
    if not ok:
        REMOVE.append(g)
        print('  ✗ 미리보기 불능:', g['tier'], g['title'][:36])
print('제거 대상:', len(REMOVE))

used = {g['fid'] for g in gal}
order = {'최우수': 0, '우수': 1, '장려': 2}
pool = [t for t in teams if t.get('report_fid') and t['report_fid'] not in used and t.get('tier') in order]
pool.sort(key=lambda x: order[x['tier']])
repl = []
for t in pool:
    if len(repl) >= len(REMOVE):
        break
    if render_ok(t['report_fid']):
        repl.append(t)
print('교체 확보:', len(repl))
assert len(repl) == len(REMOVE)

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
    pf = t.get('poster_fid') or fid
    desc = '문제 정의→데이터 수집→모델링→검증 전 과정을 담은 탐구 보고서'
    return ('<a class="thumb-card" href="#" data-view="https://drive.google.com/file/d/%s/preview" data-title="%s" data-tier="%s" data-desc="%s" onclick="return false">\n'
            '      <img class="tc-img" src="https://drive.google.com/thumbnail?id=%s&sz=w480" onerror="this.style.display=\'none\'" alt="%s 미리보기(열람 전용)">\n'
            '      <div class="tc-body"><div class="tc-tags"><span class="tag %s">%s</span><span class="tag cap">🧭 %s</span><span class="tag mathp">∑ %s</span></div>'
            '<div class="tc-title">%s</div><div class="tc-desc">%s</div>'
            '<button class="tc-open" onclick="event.stopPropagation(); return lbReport(this.closest(\'.thumb-card\'))">📄 보고서 읽기 전용 →</button></div>\n    </a>')\
        % (fid, title, tier, desc, pf, title, tiercls[tier], tier, cap, mathp, title, desc)

for i, g in enumerate(REMOVE):
    pat = re.compile(r'<a class="thumb-card" href="#"[^>]*data-view="[^"]*%s[^"]*"[\s\S]*?</a>' % re.escape(g['fid']))
    p, n = pat.subn(new_card(repl[i]), p, count=1)
    assert n == 1, g['fid']
    print('  교체 →', repl[i]['tier'], repl[i]['title'][:34])

# 갤러리 부제 실측 갱신
tiers = re.findall(r'<a class="thumb-card" href="#"[^>]*data-tier="([^"]*)"', p)
from collections import Counter
cnt = Counter(tiers)
label = ' · '.join('%s %d' % (k, cnt[k]) for k in ['대상', '최우수', '우수', '장려'] if cnt.get(k))
p = re.sub(r'수상작 갤러리 21편 — [^<(]*', '수상작 갤러리 21편 — %s · 웹 구현 사례 포함 ' % label, p)
print('부제:', label)

# 허브에서도 렌더 불능 제거
hub_removed = 0
for m in list(re.finditer(r'<a class="hub-card" href="#" data-view="https://drive\.google\.com/file/d/([A-Za-z0-9_\-]+)/preview"[\s\S]*?</a>', p)):
    if not render_ok(m.group(1)):
        p = p.replace(m.group(0), '', 1)
        hub_removed += 1
n_hub = p.count('hub-card')
p = re.sub(r'▦ 팀별 산출물 \d+건 전체 펼치기', '▦ 팀별 산출물 %d건 전체 펼치기' % n_hub, p)
print('허브 제거:', hub_removed, '→', n_hub)

open(os.path.join(SP, 'part4b_cases.html'), 'w', encoding='utf-8').write(p)
print('완료')
