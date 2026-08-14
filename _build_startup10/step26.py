# -*- coding: utf-8 -*-
"""step26: '학생 깃허브·웹 산출물' 섹션을 숫자로 보는 성과 위에 삽입.
웹 카드 7(로컬 호스팅 마스킹본, 썸네일 b64) + 깃허브 카드(스캔 JSON + CMCS)."""
import sys, re, os, json
sys.stdout.reconfigure(encoding='utf-8')
SP = os.path.dirname(os.path.abspath(__file__))

WEB = [
    ('SW1', 'physarum-routing.html', '점균 최적 경로 시뮬레이션', '황색망사점균의 경로 형성 원리를 웹에서 재현 — 네트워크 최적화'),
    ('SW2', 'quake-shelter.html', '지진 대피소 배정 시뮬레이션', '대피소 수용량·거리 기반 배정 시각화'),
    ('SW3', 'tashu-kmeans-map.html', '타슈 대여소 K-means 수요 예측 지도', '대여·반납 데이터 군집으로 수요 우세 지역 예측'),
    ('SW4', 'sports-facility-map.html', '공공체육시설 입지 분석 지도', '행정동별 수요 점수로 부족 지역 진단'),
    ('SW5', 'aed-goldentime.html', '골든타임 — 서울 AED 인터랙티브 리포트', '심정지 신고 97,810건 × AED 도달 시간 분석'),
    ('SW6', 'tashu-optimal-map.html', '타슈 대여소 최적 배치 지도', '최적화 결과를 지도 위에 표시(leaflet)'),
    ('SW7', 'timetable-tool.html', '시간표 기반 교사 이동동선 도구', '교사 이동부담 최적화 연구의 실측 도구'),
    ('SW8', 'https://myungsemin.github.io/aisuhang/', '어선 사고위험 예측·안전항로 추천 AI 웹(장려)', '학생이 직접 배포한 GitHub Pages 라이브 서비스'),
]

GH_FIXED = [
    ('WE-ON-ARK/AiMath-CMCS', 'CMCS 안전 통학경로 추천 AI — 팀 저장소(대상)', 'FastAPI·Docker까지 갖춘 실서비스형 프로젝트'),
    ('myungsemin/aisuhang', '어선 사고위험 예측 AI — 개인 저장소(장려)', 'GitHub Pages로 직접 배포한 웹 서비스의 소스'),
]
EXCLUDE_OWNERS = {'hajinsu9951', 'southkorea', 'junmokim08', 'teddylee777'}  # 교사·외부 인용·삭제된 저장소

# 스캔 JSON에서 추가 깃허브 저장소 수집
gh = list(GH_FIXED)
scan_p = r'C:\Users\user\AppData\Local\Temp\ntcap\e_urls.json'
if os.path.exists(scan_p):
    data = json.load(open(scan_p, encoding='utf-8'))
    seen = {g[0].lower() for g in gh}
    for url in sorted(data.get('urls', {})):
        m = re.match(r'https?://(?:www\.)?github\.com/([A-Za-z0-9_.\-]+)/([A-Za-z0-9_.\-]+)', url)
        if not m:
            continue
        owner, repo = m.group(1), m.group(2).removesuffix('.git')
        key = f'{owner}/{repo}'.lower()
        if key in seen or owner.lower() in EXCLUDE_OWNERS:
            continue
        seen.add(key)
        gh.append((f'{owner}/{repo}', f'{repo} — 학생 저장소', '보고서·수행 자료에 기재된 팀/개인 저장소'))
    print('스캔 반영 후 깃허브 카드:', len(gh))
else:
    print('스캔 JSON 없음 — 고정 카드만')

def web_card(ph, fn, title, desc):
    href = fn if fn.startswith('http') else 'student-web/' + fn
    return ('<a class="hub-card" href="%s" target="_blank" rel="noopener">'
            '<img src="{{B64_%s}}" alt="%s 실행 화면">'
            '<div class="hc-t"><b>%s</b><br><span style="color:var(--sub);">%s · 클릭 시 새 탭 실행</span></div></a>') % (href, ph, title, title, desc)

def gh_card(slug, title, desc):
    return ('<a class="hub-card gh-card" href="https://github.com/%s" target="_blank" rel="noopener">'
            '<img src="https://opengraph.githubassets.com/1/%s" loading="lazy" onerror="this.style.display=\'none\'" alt="%s 저장소 카드">'
            '<div class="hc-t"><b>💻 %s</b><br><span style="color:var(--sub);">%s</span></div></a>') % (slug, slug, title, title, desc)

SECTION = ('<div class="sub-title">학생 깃허브·웹 산출물 — 클릭하면 바로 실행됩니다 '
           '<span style="font-weight:400; font-size:.75em; color:var(--sub);">(웹 산출물은 본 교안에 직접 호스팅한 개인정보 마스킹본 · 새 탭 실행 · 무단 복제·배포 금지)</span></div>\n'
           '  <div class="hub-grid" style="grid-template-columns: repeat(auto-fill, minmax(215px, 1fr)); margin-bottom: 16px;">\n    '
           + '\n    '.join(web_card(*w) for w in WEB) + '\n    '
           + '\n    '.join(gh_card(*g) for g in gh) + '\n  </div>\n\n  ')

p4b = open(os.path.join(SP, 'part4b_cases.html'), encoding='utf-8').read()
ANCHOR = '<div class="sub-title">숫자로 보는 성과'
assert ANCHOR in p4b
if '학생 깃허브·웹 산출물 — 클릭하면' in p4b:
    s = p4b.find('<div class="sub-title">학생 깃허브·웹 산출물')
    e = p4b.find(ANCHOR)
    p4b = p4b[:s] + SECTION + p4b[e:]
    print('기존 섹션 갱신')
else:
    p4b = p4b.replace(ANCHOR, SECTION + ANCHOR, 1)
    print('섹션 신규 삽입')
open(os.path.join(SP, 'part4b_cases.html'), 'w', encoding='utf-8').write(p4b)

# build.py placeholder 등록
b = open(os.path.join(SP, 'build.py'), encoding='utf-8').read()
if '{{B64_SW1}}' not in b:
    NEW = ''.join('    ("{{B64_SW%d}}", "sw%d.jpg", "jpeg"),\n' % (i, i) for i in range(1, 9))
    b = b.replace('    ("{{B64_CVS2}}", "cvs2.jpg", "jpeg"),\n', '    ("{{B64_CVS2}}", "cvs2.jpg", "jpeg"),\n' + NEW, 1)
    open(os.path.join(SP, 'build.py'), 'w', encoding='utf-8').write(b)
    print('build.py placeholder 7건 추가')
print('완료')
