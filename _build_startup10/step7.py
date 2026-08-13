# -*- coding: utf-8 -*-
"""구동형 수업 도구(자기진단·정의문 조립기·BMC·타이머·프롬프트), 카드 하이퍼링크화, 링크 모음, 연구보고서 문법 박스"""
import sys, os, re
sys.stdout.reconfigure(encoding='utf-8')
SP = os.path.dirname(os.path.abspath(__file__))

def rd(p): return open(os.path.join(SP, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(SP, p), 'w', encoding='utf-8').write(s)

ok, miss = [], []
def ins(text, anchor, addition, before=False, name=''):
    global ok, miss
    if anchor not in text:
        miss.append(name or anchor[:50])
        return text
    ok.append(name)
    return text.replace(anchor, (addition + anchor) if before else (anchor + addition), 1)

# ============ part1: CSS ============
p1 = rd('part1_head.html')
CSS = """
  /* ---- 하이퍼링크 카드 / 타이머 / BMC / 진단 ---- */
  a.thumb-card { text-decoration: none; color: inherit; display: flex; }
  .timer { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; }
  .timer .tm-disp { font-size: 2.1em; font-weight: 900; color: var(--navy); font-variant-numeric: tabular-nums; min-width: 130px; }
  .timer.tm-done .tm-disp { color: #E63946; }
  .bmc-grid { display: grid; grid-template-columns: repeat(10, 1fr); gap: 7px; margin: 10px 0; }
  .bmc-cell { border: 1.5px solid var(--line); border-radius: 9px; padding: 8px; background: #FBFDFF; display: flex; flex-direction: column; }
  .bmc-cell b { font-size: 12px; color: var(--blue); margin-bottom: 4px; }
  .bmc-cell textarea { border: none; background: transparent; font-family: inherit; font-size: 12.5px; min-height: 66px; resize: vertical; outline: none; flex: 1; }
  .bmc-kp { grid-column: span 2; grid-row: span 2; } .bmc-ka { grid-column: span 2; } .bmc-vp { grid-column: span 2; grid-row: span 2; background: #FFF7EC; border-color: var(--orange); } .bmc-cr { grid-column: span 2; } .bmc-cs { grid-column: span 2; grid-row: span 2; }
  .bmc-kr { grid-column: span 2; } .bmc-ch { grid-column: span 2; }
  .bmc-cost { grid-column: span 5; } .bmc-rev { grid-column: span 5; }
  @media (max-width: 700px) { .bmc-grid { grid-template-columns: 1fr 1fr; } .bmc-grid > div { grid-column: span 1 !important; grid-row: auto !important; } .bmc-cost, .bmc-rev { grid-column: span 2 !important; } }
  .diag-list { list-style: none; display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 8px; margin: 10px 0; }
  .diag-list li { background: #F6F9FC; border: 1.5px solid var(--line); border-radius: 10px; padding: 10px 12px; font-size: 13.5px; display: flex; gap: 9px; align-items: flex-start; cursor: pointer; }
  .diag-list li.on { border-color: var(--orange); background: #FFF7EC; }
  .diag-list input { margin-top: 4px; accent-color: var(--orange); }
  .prompt-card { background: #14213D; color: #DCE9F7; border-radius: 10px; padding: 12px 14px; font-size: 13px; line-height: 1.7; margin: 8px 0; position: relative; }
  .prompt-card .copy-btn { position: absolute; top: 8px; right: 8px; background: rgba(255,255,255,.14); color: #FFD166; border: none; border-radius: 7px; padding: 5px 11px; font-size: 11.5px; font-weight: 800; cursor: pointer; font-family: inherit; }
  .prompt-card .copy-btn:hover { background: rgba(255,255,255,.26); }
"""
p1 = ins(p1, '  /* ---- PRINT (활동지 인쇄) ---- */', CSS + '\n  /* ---- PRINT (활동지 인쇄) ---- */', before=False, name='css')
p1 = p1.replace(CSS + '\n  /* ---- PRINT (활동지 인쇄) ---- */\n  /* ---- PRINT (활동지 인쇄) ---- */', CSS + '\n  /* ---- PRINT (활동지 인쇄) ---- */')  # 중복 방지
# 위 방식이 꼬이면 단순 삽입으로 재시도
if CSS not in p1:
    p1 = p1.replace('  /* ---- PRINT (활동지 인쇄) ---- */', CSS + '  /* ---- PRINT (활동지 인쇄) ---- */', 1)
wr('part1_head.html', p1)

# ============ part2: 연구보고서 문법 박스 (섹션1 끝) ============
p2 = rd('part2_design.html')
BOX = """

  <div class="sub-title">연구·선도학교 보고서 문법으로 본 이 수업 (YEEP 운영보고서 구조 반영)</div>
  <div class="grid g4">
    <div class="case-card"><div class="cs-top">🎯 <b>필요성</b></div><div class="cs-desc">교과 지식이 삶과 분리되고, 지역 문제는 말로만 지적되며, 학생은 불확실성 앞에서 도전을 주저한다 — 세 문제를 한 수업으로 푼다</div></div>
    <div class="case-card"><div class="cs-top">🧩 <b>운영 과제 3</b></div><div class="cs-desc">① 8단계 모형 기반 교육과정 재구성(10차시) ② 웹 구동형 학습지원도구 개발(위젯·활동지) ③ 성과의 전면 공개와 확산(아카이브·연수)</div></div>
    <div class="case-card"><div class="cs-top">📏 <b>성과 지표</b></div><div class="cs-desc">사전·사후 역량 온도 비교(1↔10차시 수미상관) · 과정평가 누적(차시당 1점) · 산출물 80팀 공개 · 교외 대회 성과</div></div>
    <div class="case-card"><div class="cs-top">📡 <b>일반화</b></div><div class="cs-desc">단일 HTML 배포(설치 불요) · 지역 데이터 교체만으로 타 학교 이식 · 축소(6~8차시)/확장(20차시)/중학교 변형 가이드 제공</div></div>
  </div>
"""
p2 = ins(p2, '<div class="case-card"><div class="cs-top">🔗 <b>융합적 실행력</b></div><div class="cs-desc">수학·AI·코딩·지역 자원을 엮어 실제로 구현</div></div>\n  </div>', BOX, before=False, name='p2-report-box')
wr('part2_design.html', p2)

# ============ part3: 차시별 구동형 도구 ============
p3 = rd('part3_lessons.html')

W_DIAG = """
          <div class="sub-title" style="margin-top:16px;">웹 도구 · 역량 자기진단 — 지금 이 화면에서 바로</div>
          <div class="wg" id="wg-diag">
            <p class="wg-help">"잘한다"가 아니라 <b>"굳이 고르면 이게 낫다"</b> 기준으로 2개를 고르세요. 고르면 추천 역할이 나옵니다.</p>
            <ul class="diag-list">
              <li onclick="diagToggle(this,0)"><input type="checkbox"><span>숫자·표를 다루는 게 낫다 (검색해서 자료 찾기 포함)</span></li>
              <li onclick="diagToggle(this,1)"><input type="checkbox"><span>손으로 만들고 조립하는 게 낫다 (도구·기기 다루기)</span></li>
              <li onclick="diagToggle(this,2)"><input type="checkbox"><span>글로 정리하고 기록하는 게 낫다</span></li>
              <li onclick="diagToggle(this,3)"><input type="checkbox"><span>사람들 앞에서 말하는 게 낫다</span></li>
              <li onclick="diagToggle(this,4)"><input type="checkbox"><span>엉뚱한 아이디어를 내는 게 낫다</span></li>
              <li onclick="diagToggle(this,5)"><input type="checkbox"><span>일정을 짜고 사람을 조율하는 게 낫다</span></li>
            </ul>
            <div class="wg-msg" id="diag-msg">2개를 고르면 결과가 나타납니다.</div>
          </div>
"""
p3 = ins(p3, '<div class="lp-eval"><b>✔ 평가 요소(과정중심)</b> — 자기 강점·약점을', W_DIAG + '          ', before=True, name='L1-diag')

W_DEF = """
          <div class="sub-title" style="margin-top:16px;">웹 도구 · 문제 정의문 조립기 — 4요소를 넣으면 문장이 완성됩니다</div>
          <div class="wg" id="wg-def">
            <div class="ws-grid2">
              <div class="ws-field"><label>언제</label><input class="ws-line" id="def-when" oninput="defBuild()" placeholder="등교 시간대"></div>
              <div class="ws-field"><label>어디서</label><input class="ws-line" id="def-where" oninput="defBuild()" placeholder="○○사거리에서"></div>
              <div class="ws-field"><label>누가</label><input class="ws-line" id="def-who" oninput="defBuild()" placeholder="초등학생이"></div>
              <div class="ws-field"><label>무엇 때문에 (불편)</label><input class="ws-line" id="def-why" oninput="defBuild()" placeholder="횡단보도 대기 시간이 길어 무단횡단을 한다"></div>
            </div>
            <div class="ws-field"><label>이 문제를 재는 숫자 <span class="hint">단위까지! 예: 대기 시간(초), 수신 강도(dBm)</span></label><input class="ws-line" id="def-num" oninput="defBuild()" placeholder="1회 평균 대기 시간(초)"></div>
            <div class="wg-msg" id="def-out">위 칸을 채우면 문제 정의문이 여기에 조립됩니다.</div>
            <div class="wg-toolbar"><button class="wg-btn" onclick="defCopy()">📋 문장 복사</button><span id="def-check" style="font-size:12.5px; color:var(--sub);"></span></div>
          </div>
"""
p3 = ins(p3, '<div class="lp-eval"><b>✔ 평가 요소</b> — 문제 정의문의 4요소 충족', W_DEF + '          ', before=True, name='L2-def')

W_TIMER5 = """
          <div class="wg timer" id="timer-5" data-sec="240">
            <span class="tm-disp">04:00</span>
            <button class="wg-btn" onclick="tmSet(this,240)">4분(회전)</button>
            <button class="wg-btn" onclick="tmSet(this,60)">1분</button>
            <button class="wg-btn alt" onclick="tmStart(this)">▶ 시작</button>
            <button class="wg-btn" onclick="tmPause(this)">⏸ 멈춤</button>
            <button class="wg-btn" onclick="tmReset(this)">⟲</button>
            <span style="font-size:12.5px; color:var(--sub);">브레인라이팅 회전 타이머 — 0이 되면 종이 울립니다. 시트를 왼쪽으로!</span>
          </div>
"""
p3 = ins(p3, '1~3페이지를 함께 넘기며 도입하세요.</p>\n          </div>', W_TIMER5, before=False, name='L5-timer')

W_BMC = """
          <div class="sub-title">웹 도구 · 비즈니스 모델 캔버스 — 팀별로 직접 채우고 인쇄</div>
          <div class="wg" id="wg-bmc">
            <p class="wg-help">칸을 채운 뒤 <b>[캔버스 인쇄]</b>를 누르면 작성한 내용 그대로 출력됩니다. 가운데 주황 칸(가치 제안)부터 채우는 것이 요령입니다.</p>
            <div class="bmc-grid">
              <div class="bmc-cell bmc-kp"><b>핵심 파트너</b><textarea placeholder="누구와 손잡아야 하나? (기관·멘토·업체)"></textarea></div>
              <div class="bmc-cell bmc-ka"><b>핵심 활동</b><textarea placeholder="반드시 해야 하는 일은?"></textarea></div>
              <div class="bmc-cell bmc-vp"><b>가치 제안 ★</b><textarea placeholder="누구의 어떤 불편을, 데이터 근거로, 어떻게 줄이나?"></textarea></div>
              <div class="bmc-cell bmc-cr"><b>고객 관계</b><textarea placeholder="고객과 어떻게 만나고 유지하나?"></textarea></div>
              <div class="bmc-cell bmc-cs"><b>고객군</b><textarea placeholder="누구를 위한 것인가? (세분화)"></textarea></div>
              <div class="bmc-cell bmc-kr"><b>핵심 자원</b><textarea placeholder="가진 것: 데이터·기능·도구·사람"></textarea></div>
              <div class="bmc-cell bmc-ch"><b>채널</b><textarea placeholder="어떤 경로로 전달하나?"></textarea></div>
              <div class="bmc-cell bmc-cost"><b>비용 구조</b><textarea placeholder="어디에 돈·시간이 드나? (고정/변동)"></textarea></div>
              <div class="bmc-cell bmc-rev"><b>수익 흐름</b><textarea placeholder="누가 왜 돈·시간·관심을 내나?"></textarea></div>
            </div>
            <div class="wg-toolbar"><button class="wg-btn alt" onclick="printEl('wg-bmc')">🖨 캔버스 인쇄</button><span style="font-size:12.5px; color:var(--sub);">지표 규칙: 수익·비용 칸에는 숫자 1개 이상!</span></div>
          </div>
"""
p3 = ins(p3, '<div class="pack"><span class="pk-label">자료 패키지</span><a class="pk" href="#canva">🎨 캔바 · 린 비즈니스 모델</a>', W_BMC + '          ', before=True, name='L6-bmc')

W_PROMPT = """
          <div class="sub-title" style="margin-top:16px;">바로 쓰는 프롬프트 카드 3장 — [복사]해서 생성형 AI에 붙여넣기</div>
          <div class="prompt-card">너는 고등학생 팀의 코딩 조수야. 우리는 [우리 동네 문제 한 줄]를 해결하려고 해. 아래 데이터로 산점도와 회귀선을 그리는 웹페이지를 HTML+JavaScript 한 파일로 만들어 줘. 코드에 한국어 주석을 달아 줘. 데이터: x=[ ], y=[ ]<button class="copy-btn" onclick="copyPrompt(this)">복사</button></div>
          <div class="prompt-card">이 코드를 실행했더니 아래 오류가 났어. 원인을 한 문장으로 설명하고, 고친 코드 전체를 다시 줘. [오류 메시지 붙여넣기]<button class="copy-btn" onclick="copyPrompt(this)">복사</button></div>
          <div class="prompt-card">네가 만든 코드가 계산한 [평균/상관계수/예측값]이 맞는지 검산하는 방법을 알려 줘. 손으로 계산할 수 있는 작은 예시 데이터(5개)도 만들어서, 손 계산 결과와 코드 결과를 비교하게 해 줘.<button class="copy-btn" onclick="copyPrompt(this)">복사</button></div>
"""
p3 = ins(p3, "<div class=\"lp-eval\"><b>✔ 평가 요소</b> — MVP의 '작동' 여부", W_PROMPT + '          ', before=True, name='L8-prompt')

W_TIMER9 = """
          <div class="wg timer" id="timer-9" data-sec="30">
            <span class="tm-disp">00:30</span>
            <button class="wg-btn" onclick="tmSet(this,30)">30초(중간 공개)</button>
            <button class="wg-btn alt" onclick="tmStart(this)">▶ 시작</button>
            <button class="wg-btn" onclick="tmPause(this)">⏸</button>
            <button class="wg-btn" onclick="tmReset(this)">⟲</button>
            <span style="font-size:12.5px; color:var(--sub);">미완성 공개 타이머 — 30초, 지금 상태 그대로.</span>
          </div>
"""
p3 = ins(p3, '<div class="lp-eval"><b>✔ 평가 요소</b> — 극한 테스트 대응 기록', W_TIMER9 + '          ', before=True, name='L9-timer')

W_TIMER10 = """
          <div class="wg timer" id="timer-10" data-sec="180">
            <span class="tm-disp">03:00</span>
            <button class="wg-btn" onclick="tmSet(this,180)">3분(피칭)</button>
            <button class="wg-btn" onclick="tmSet(this,60)">1분(Q&amp;A)</button>
            <button class="wg-btn alt" onclick="tmStart(this)">▶ 시작</button>
            <button class="wg-btn" onclick="tmPause(this)">⏸</button>
            <button class="wg-btn" onclick="tmReset(this)">⟲</button>
            <span style="font-size:12.5px; color:var(--sub);">부스 타이머 — 화면에 크게 띄우고 3분마다 종. 종이 동선을 만듭니다.</span>
          </div>
"""
p3 = ins(p3, '<div class="lp-eval"><b>✔ 평가 요소</b> — 피칭의 숫자 근거', W_TIMER10 + '          ', before=True, name='L10-timer')

# 자료 패키지 칩 추가
p3 = ins(p3, '🔗 YEEP 역량 진단</a>', '<a class="pk" href="#wg-diag">🎛 웹 자기진단(이 화면)</a>', name='chip-L1')
p3 = ins(p3, '🌏 구글 어스</a>', '<a class="pk" href="#wg-def">🎛 문제 정의문 조립기(이 화면)</a>', name='chip-L2')
p3 = ins(p3, '📖 BMC 읽을거리</a>', '<a class="pk" href="#wg-bmc">🎛 웹 BMC 캔버스(이 화면)</a>', name='chip-L6')
p3 = ins(p3, '🧰 예산 0원 운영 팁</a>', '<a class="pk" href="#wsRI">📄 자원 인벤토리 시트 (바로 인쇄)</a>', name='chip-L7')
wr('part3_lessons.html', p3)

# ============ part4: 자원 인벤토리 활동지 ============
p4 = rd('part4_ws_canva_cases.html')
p4 = ins(p4, '➕ 이해관계자 지도 (5차시)</button>', '\n    <button class="ws-tab" onclick="wsTab(this,\'wsRI\')">➕ 자원 인벤토리 (7차시)</button>', name='ws-tab-RI')
RI = """
  <!-- 자원 인벤토리 -->
  <div class="ws-sheet" id="wsRI">
    <h4>자원 인벤토리 — 가진 것으로 시작하기 (이펙추에이션)</h4>
    <div class="ws-meta">7차시 · 모둠 | '수중의 새' 원칙: 목표에서 역산하지 말고, 지금 가진 것부터 센다</div>
    <div class="table-wrap" style="box-shadow:none; border:1px solid var(--line);">
      <table style="min-width:520px;">
        <thead><tr><th style="width:110px;">자원</th><th>이미 가진 것</th><th>부족한 것</th><th>구할 곳 (사람·기관·대체재)</th></tr></thead>
        <tbody>
          <tr><td><b>기능</b><br><span style="font-size:10.5px;">코딩·디자인·측정·발표</span></td><td style="height:52px;"></td><td></td><td></td></tr>
          <tr><td><b>도구</b><br><span style="font-size:10.5px;">노트북·센서·시트</span></td><td style="height:52px;"></td><td></td><td></td></tr>
          <tr><td><b>데이터</b><br><span style="font-size:10.5px;">4차시 확보분</span></td><td style="height:52px;"></td><td></td><td></td></tr>
          <tr><td><b>사람</b><br><span style="font-size:10.5px;">멘토·기관·선배</span></td><td style="height:52px;"></td><td></td><td></td></tr>
        </tbody>
      </table>
    </div>
    <div class="ws-field"><label>완성 기준 서약 <span class="hint">— "다음 두 차시가 끝날 때 '작동'해야 하는 것 한 가지"</span></label><textarea class="ws-area"></textarea></div>
    <div class="ws-example"><b>제약 발문</b> — 대안이 거창해지면: "예산이 0원이라면?" · "하루 만에 해야 한다면?" — 이 두 질문이 이펙추에이션의 '감당 가능한 손실' 훈련입니다.</div>
    <button class="print-btn" onclick="window.print()" style="margin-top:16px;">🖨 이 활동지 인쇄</button>
  </div>
"""
p4 = ins(p4, '  </div>\n</div>\n\n<!-- ============ 5. 교사 개발 자료 (Canva) ============ -->', RI + '  </div>\n</div>\n\n<!-- ============ 5. 교사 개발 자료 (Canva) ============ -->', before=False, name='ws-sheet-RI')
p4 = p4.replace(RI + '  </div>\n</div>\n\n<!-- ============ 5. 교사 개발 자료 (Canva) ============ -->' + RI, RI + '  </div>\n</div>\n\n<!-- ============ 5. 교사 개발 자료 (Canva) ============ -->')
# 삽입 위치 교정: 시트는 탭 컨테이너 안(마지막 시트 뒤)에 있어야 함 → 위 앵커는 섹션 닫힘이므로 시트를 그 '앞'에 넣는다
if '<div class="ws-sheet" id="wsRI">' not in p4:
    p4 = p4.replace('</div>\n\n<!-- ============ 5. 교사 개발 자료 (Canva) ============ -->', RI + '</div>\n\n<!-- ============ 5. 교사 개발 자료 (Canva) ============ -->', 1)
wr('part4_ws_canva_cases.html', p4)

# ============ part4b: 카드 → 진짜 하이퍼링크 + 링크 모음 ============
p4b = rd('part4b_cases.html')
pat = re.compile(r'<div class="thumb-card" onclick="window\.open\(\'([^\']+)\',\'_blank\'\)">([\s\S]*?)</div>\n    </div>')
def conv(m):
    return '<a class="thumb-card" href="' + m.group(1) + '" target="_blank" rel="noopener">' + m.group(2) + '</div>\n    </a>'
p4b, n = pat.subn(conv, p4b)
print('thumb-card -> <a> converted:', n)

LINKHUB = """
  <div class="sub-title">동적 산출물 · 저장소 링크 모음 <span style="font-weight:400; font-size:.75em; color:var(--sub);">— 브라우저에서 바로 열리는 것만 모았습니다</span></div>
  <div class="pack" style="margin-bottom:6px;">
    <a class="pk" href="index.html" target="_blank" rel="noopener">🖥 성과 아카이브 — 80팀 보고서·포스터·AI 모델 열람(전용 뷰어)</a>
    <a class="pk" href="우리동네_AI모델_성과공유.html" target="_blank" rel="noopener">🏆 성과공유회 페이지</a>
    <a class="pk" href="https://github.com/hajinsu9951/2026-AI-MATH-PROJECT" target="_blank" rel="noopener">💻 GitHub 저장소(사이트·데이터 소스)</a>
    <a class="pk" href="https://drive.google.com/drive/folders/1tegaCUbhnFRawuKbWohP9Mx9SkarJ6uG" target="_blank" rel="noopener">🌊 어선 사고위험 예측 AI 웹 — 개발 자료 폴더(열람)</a>
    <a class="pk" href="#lessons-detail">🎛 이 페이지의 체험 위젯 8종 (3~4차시 실습·타이머·BMC 등)</a>
    <a class="pk" href="#canva">🎨 교사 개발 캔바 5종</a>
  </div>
  <p style="font-size:.85em; color:var(--sub); margin-bottom:14px;">※ 점균 시뮬레이션 등 실행형 산출물은 성과 아카이브 내 뷰어에서 열람됩니다. 학생 개인 저장소 링크는 개인정보 보호를 위해 아카이브 경유로만 공개합니다.</p>
"""
p4b = ins(p4b, '  <div class="xp-band">', LINKHUB + '  <div class="xp-band">', before=False, name='linkhub')
p4b = p4b.replace(LINKHUB + '  <div class="xp-band">' + LINKHUB, LINKHUB + '  <div class="xp-band">')
if '동적 산출물 · 저장소 링크 모음' not in p4b:
    p4b = p4b.replace('  <div class="xp-band">', LINKHUB + '  <div class="xp-band">', 1)
wr('part4b_cases.html', p4b)

# ============ build.py: part3c 포함 ============
b = rd('build.py')
if 'part3c' not in b:
    b = b.replace('p3b = rd("part3b_widgets.html")', 'p3b = rd("part3b_widgets.html")\np3c = rd("part3c_widgets2.html")')
    b = b.replace('html = "\\n".join([p1, p2, p3, p3b, p4, p4b, p5])', 'html = "\\n".join([p1, p2, p3, p3b, p3c, p4, p4b, p5])')
    wr('build.py', b)
    print('build.py: part3c added')

print('OK:', ok)
print('MISS:', miss if miss else 'none')
