# -*- coding: utf-8 -*-
"""step24: 갤러리 21편 미리보기 가용성 검사 → 불능 카드 교체(동일 매수 유지),
허브에서 불능 카드 제거, xp-band 무단복제 금지 문구"""
import sys, re, os, json, subprocess
sys.stdout.reconfigure(encoding='utf-8')
SP = os.path.dirname(os.path.abspath(__file__))

def rd(p): return open(os.path.join(SP, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(SP, p), 'w', encoding='utf-8').write(s)

CACHE = os.path.join(SP, '_view_probe.json')
cache = json.load(open(CACHE, encoding='utf-8')) if os.path.exists(CACHE) else {}

def viewable(url):
    if url in cache:
        return cache[url]
    r = subprocess.run(['curl', '-skL', '--max-time', '25', '-w', '@@%{http_code}@@', url],
                       capture_output=True, text=True, encoding='utf-8', errors='ignore')
    out = r.stdout or ''
    code = re.search(r'@@(\d{3})@@\s*$', out)
    code = int(code.group(1)) if code else 0
    body = out[:4000]
    bad = code >= 400 or 'ServiceLogin' in body or 'accounts.google.com/v3/signin' in body or '권한이 필요' in body
    ok = (code == 200 or code == 0) and not bad
    cache[url] = ok
    json.dump(cache, open(CACHE, 'w', encoding='utf-8'))
    return ok

p4b = rd('part4b_cases.html')

# --- 갤러리 카드 21 스캔 ---
gal = re.findall(r'<a class="thumb-card" href="#"([^>]*)>[\s\S]*?</a>', p4b)
views = []
for attrs in gal:
    v = re.search(r'data-view="([^"]*)"', attrs)
    t = re.search(r'data-title="([^"]*)"', attrs)
    views.append((v.group(1) if v else '', t.group(1) if t else ''))
print('갤러리 카드:', len(views))
broken = [(v, t) for v, t in views if v and not viewable(v)]
print('미리보기 불능:', len(broken))
for v, t in broken:
    print('  ✗', t[:34], v[:60])

d = json.load(open(os.path.join(SP, 'teams_summary.json'), encoding='utf-8'))
teams = d if isinstance(d, list) else d.get('teams', [])
used_fids = set(re.findall(r'/d/([A-Za-z0-9_\-]+)/preview', ' '.join(v for v, _ in views)))

def chips(title):
    t = title.lower()
    if 'k-means' in t or '군집' in t or 'kmeans' in t: return ('위험감수성', 'K-means 군집')
    if '포아송' in t: return ('데이터기반 의사결정', '포아송 회귀')
    if 'xgboost' in t or '랜덤포레스트' in t or 'tf-idf' in t or '분류' in t: return ('기회탐색·가치창출', '분류 모델·특성 중요도')
    if '회귀' in t or '상관' in t: return ('데이터기반 의사결정', '상관·회귀분석')
    if '최적' in t or '경로' in t or '배치' in t or 'mclp' in t or 'greedy' in t: return ('융합적 실행력', '최적화 알고리즘')
    if '예측' in t: return ('데이터기반 의사결정', '예측 모델')
    if 'gis' in t or '분포' in t or '지도' in t or '입지' in t: return ('기회탐색·가치창출', '공간 데이터 분석')
    return ('데이터기반 의사결정', '데이터 분석·모델링')

tiercls = {'대상': 'grand', '최우수': 'top', '우수': 'good', '장려': 'good'}
order = {'대상': 0, '최우수': 1, '우수': 2, '장려': 3}
pool = [t for t in teams if t.get('report_fid') and t['report_fid'] not in used_fids and t.get('tier') in order]
pool.sort(key=lambda x: order[x['tier']])

repl = []
for t in pool:
    if len(repl) >= len(broken):
        break
    url = 'https://drive.google.com/file/d/%s/preview' % t['report_fid']
    if viewable(url):
        repl.append(t)
print('교체 후보 확보:', len(repl))
assert len(repl) >= len(broken), '교체 후보 부족'

def new_card(t):
    fid = t['report_fid']
    title = t['title'].replace('"', '')
    tier = t['tier']
    cap, mathp = chips(title)
    pf = t.get('poster_fid') or t.get('thumb') or fid
    return ('<a class="thumb-card" href="#" data-view="https://drive.google.com/file/d/%s/preview" data-title="%s" data-tier="%s" data-desc="문제 정의→데이터 수집→모델링→검증 전 과정을 담은 탐구 보고서" onclick="return false">\n'
            '      <img class="tc-img" src="https://drive.google.com/thumbnail?id=%s&sz=w480" onerror="this.style.display=\'none\'" alt="%s 미리보기(열람 전용)">\n'
            '      <div class="tc-body"><div class="tc-tags"><span class="tag %s">%s</span><span class="tag cap">🧭 %s</span><span class="tag mathp">∑ %s</span></div>'
            '<div class="tc-title">%s</div><div class="tc-desc">문제 정의→데이터 수집→모델링→검증 전 과정을 담은 탐구 보고서</div>'
            '<button class="tc-open" onclick="event.stopPropagation(); return lbReport(this.closest(\'.thumb-card\'))">📄 보고서 읽기 전용 →</button></div>\n    </a>')\
        % (fid, title, tier, pf, title, tiercls[tier], tier, cap, mathp, title)

for i, (v, _) in enumerate(broken):
    esc = re.escape(v)
    pat = re.compile(r'<a class="thumb-card" href="#"[^>]*data-view="%s"[^>]*>[\s\S]*?</a>' % esc)
    p4b, n = pat.subn(new_card(repl[i]), p4b, count=1)
    assert n == 1, v

# --- 허브에서 불능 카드 제거 ---
hub_removed = 0
for m in list(re.finditer(r'<a class="hub-card" href="#" data-view="([^"]*)"[\s\S]*?</a>', p4b)):
    if not viewable(m.group(1)):
        p4b = p4b.replace(m.group(0), '', 1)
        hub_removed += 1
print('허브 제거:', hub_removed)
n_hub = p4b.count('hub-card')
p4b = re.sub(r'▦ 팀별 산출물 \d+건 전체 펼치기', '▦ 팀별 산출물 %d건 전체 펼치기' % n_hub, p4b)

# --- xp-band 문구 ---
OLD_XP = '아카이브 문서는 <b>미리보기 전용(다운로드 잠금)</b>이며, 공개를 전제로 하니 학생들이 완성도를 스스로 끌어올렸습니다 — 공개 자체가 교육 장치입니다.'
NEW_XP = '아카이브 문서는 <b>미리보기 전용(다운로드 절대 불가·저장 버튼 차단)</b>이며, 공개를 전제로 하니 학생들이 완성도를 스스로 끌어올렸습니다 — 공개 자체가 교육 장치입니다. <b>모든 학생 산출물의 무단 복제·배포를 금합니다.</b>'
if OLD_XP in p4b:
    p4b = p4b.replace(OLD_XP, NEW_XP, 1)
    print('xp-band 문구 ok')
else:
    assert '무단 복제·배포를 금합니다' in p4b

wr('part4b_cases.html', p4b)
print('part4b ok / 갤러리 교체:', len(broken))
