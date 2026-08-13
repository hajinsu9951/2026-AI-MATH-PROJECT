# -*- coding: utf-8 -*-
"""사례 카드 → 드라이브 미리보기 링크, 차시별 자료 칩 확장, build.py 파트 목록 갱신"""
import sys, os, re, json
sys.stdout.reconfigure(encoding='utf-8')
SP = os.path.dirname(os.path.abspath(__file__))

def rd(p): return open(os.path.join(SP, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(SP, p), 'w', encoding='utf-8').write(s)

# ---------- 1) part4b: 카드 클릭 → 해당 산출물 미리보기 ----------
p4b = rd('part4b_cases.html')
teams = json.load(open(os.path.join(SP, 'teams_summary.json'), encoding='utf-8'))
by_id = {t['id']: t for t in teams}

blocks = p4b.split('<div class="thumb-card"')
changed = 0
for i in range(1, len(blocks)):
    m = re.search(r'thumbnail\?id=([\w-]+)&', blocks[i])
    if not m:
        continue
    thumb = m.group(1)
    # 이 썸네일 fid를 가진 팀 찾기 (thumb → poster → report 순으로 매칭)
    team = None
    for t in teams:
        if thumb in (t.get('thumb'), t.get('poster_fid'), t.get('report_fid')):
            team = t
            break
    if not team:
        print('NO TEAM for thumb', thumb)
        continue
    target = team.get('report_fid') or team.get('poster_fid') or thumb
    new_url = f'https://drive.google.com/file/d/{target}/preview'
    before = blocks[i]
    blocks[i] = blocks[i].replace(
        "onclick=\"window.open('https://github.com/hajinsu9951/2026-AI-MATH-PROJECT','_blank')\"",
        f"onclick=\"window.open('{new_url}','_blank')\"", 1)
    if blocks[i] != before:
        changed += 1
p4b = '<div class="thumb-card"'.join(blocks)
print('card links changed:', changed)

p4b = p4b.replace(
    '아래 카드는 성과공유회 <b>실제 수상작</b>이며, 카드를 클릭하면 GitHub 프로젝트 저장소로 이동합니다.',
    '아래 카드는 성과공유회 <b>실제 수상작</b>이며, <b>카드를 클릭하면 해당 팀의 보고서·포스터 원문이 열람 전용 미리보기</b>로 열립니다(다운로드 버튼 없는 보기 화면). 전체 코드·아카이브는 하단 GitHub 버튼에서 볼 수 있습니다.')
wr('part4b_cases.html', p4b)

# ---------- 2) part3: 차시별 자료 칩 확장 ----------
p3 = rd('part3_lessons.html')
YT = 'https://www.youtube.com/results?search_query='
ADD = {
 '🔗 YEEP 역량 진단</a>':
   f'<a class="pk" href="{YT}%EC%A0%95%EC%A3%BC%EC%98%81+%EA%B8%B0%EC%97%85%EA%B0%80%EC%A0%95%EC%8B%A0+%EB%8F%84%EC%A0%84" target="_blank" rel="noopener">▶ 영상 검색: 정주영 도전 사례</a>'
   '<a class="pk" href="https://asan-nanum.org" target="_blank" rel="noopener">🔗 아산나눔재단(기업가정신)</a>',
 '🌏 구글 어스</a>':
   '<a class="pk" href="https://kosis.kr" target="_blank" rel="noopener">📊 KOSIS 국가통계포털</a>'
   '<a class="pk" href="https://app.diagrams.net" target="_blank" rel="noopener">🧭 draw.io(지도·순서도)</a>'
   f'<a class="pk" href="{YT}5WHY+%EA%B8%B0%EB%B2%95" target="_blank" rel="noopener">▶ 영상 검색: 5WHY 기법</a>',
 '🗂 사례 원문(아카이브)</a>':
   '<a class="pk" href="https://www.naftaliharris.com/blog/visualizing-k-means-clustering/" target="_blank" rel="noopener">🕹 K-means 시각화 놀이터(영문)</a>'
   '<a class="pk" href="https://ko.wikipedia.org/wiki/K-%EC%B5%9C%EA%B7%BC%EC%A0%91_%EC%9D%B4%EC%9B%83_%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98" target="_blank" rel="noopener">📖 KNN 원리(위키백과)</a>'
   '<a class="pk" href="https://ko.wikipedia.org/wiki/K-%ED%8F%89%EA%B7%A0_%EC%95%8C%EA%B3%A0%EB%A6%AC%EC%A6%98" target="_blank" rel="noopener">📖 K-평균 원리(위키백과)</a>'
   f'<a class="pk" href="{YT}KNN+K-means+%EC%89%BD%EA%B2%8C" target="_blank" rel="noopener">▶ 영상 검색: KNN·K-means 쉽게</a>',
 '📄 활동지③(완성)</a>':
   '<a class="pk" href="https://colab.research.google.com" target="_blank" rel="noopener">🧪 Google Colab</a>'
   '<a class="pk" href="https://kosis.kr" target="_blank" rel="noopener">📊 KOSIS 국가통계포털</a>'
   f'<a class="pk" href="{YT}%EA%B5%AC%EA%B8%80+%EC%8B%9C%ED%8A%B8+CORREL+%ED%9A%8C%EA%B7%80" target="_blank" rel="noopener">▶ 영상 검색: 시트 상관·회귀 함수</a>',
 '🧰 예산 0원 운영 팁</a>':
   '<a class="pk" href="https://www.arduino.cc" target="_blank" rel="noopener">🔌 아두이노 공식</a>'
   '<a class="pk" href="https://microbit.org/ko/" target="_blank" rel="noopener">🔌 마이크로비트 공식</a>'
   '<a class="pk" href="https://playentry.org" target="_blank" rel="noopener">🧱 엔트리</a>'
   f'<a class="pk" href="{YT}%EC%9D%B4%ED%8E%99%EC%B6%94%EC%97%90%EC%9D%B4%EC%85%98" target="_blank" rel="noopener">▶ 영상 검색: 이펙추에이션</a>',
 '🤖 AI 활용 4원칙</a>':
   '<a class="pk" href="https://teachablemachine.withgoogle.com" target="_blank" rel="noopener">🧠 티처블 머신(노코드 AI)</a>'
   '<a class="pk" href="https://chatgpt.com" target="_blank" rel="noopener">🤖 ChatGPT</a>'
   '<a class="pk" href="https://gemini.google.com" target="_blank" rel="noopener">🤖 Gemini</a>'
   '<a class="pk" href="https://colab.research.google.com" target="_blank" rel="noopener">🧪 Colab</a>',
 '🗣 피드백 어법 규칙</a>':
   '<a class="pk" href="https://www.miricanvas.com" target="_blank" rel="noopener">🎨 미리캔버스(피칭덱·포스터)</a>'
   f'<a class="pk" href="{YT}%EC%97%98%EB%A6%AC%EB%B2%A0%EC%9D%B4%ED%84%B0+%ED%94%BC%EC%B9%98+3%EB%B6%84" target="_blank" rel="noopener">▶ 영상 검색: 3분 엘리베이터 피치</a>',
 '🚀 후속 확장(외부 피칭·동아리)</a>':
   '<a class="pk" href="https://www.wadiz.kr" target="_blank" rel="noopener">💰 와디즈(펀딩 페이지 견학)</a>'
   '<a class="pk" href="https://tumblbug.com" target="_blank" rel="noopener">💰 텀블벅(펀딩 페이지 견학)</a>'
   f'<a class="pk" href="{YT}%EC%8A%A4%ED%83%80%ED%8A%B8%EC%97%85+IR+%ED%94%BC%EC%B9%AD" target="_blank" rel="noopener">▶ 영상 검색: 스타트업 IR 피칭</a>',
}
miss = []
for anchor, add in ADD.items():
    if anchor not in p3:
        miss.append(anchor)
        continue
    p3 = p3.replace(anchor, anchor + add, 1)
wr('part3_lessons.html', p3)
print('chip anchors missed:', miss if miss else 'none')

# ---------- 3) build.py: 위젯 파트 포함 ----------
b = rd('build.py')
if 'part3b_widgets' not in b:
    b = b.replace('p3 = rd("part3_lessons.html")',
                  'p3 = rd("part3_lessons.html")\np3b = rd("part3b_widgets.html")')
    b = b.replace('html = "\\n".join([p1, p2, p3, p4, p4b, p5])',
                  'html = "\\n".join([p1, p2, p3, p3b, p4, p4b, p5])')
    wr('build.py', b)
    print('build.py: widgets part added')
else:
    print('build.py: already includes widgets')
