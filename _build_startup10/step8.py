# -*- coding: utf-8 -*-
"""자립형 수업 완성: 활동지①·⑤, 투자권, 시나리오 보드, 함수 치트시트, 역설계 정답(교사용)"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
SP = os.path.dirname(os.path.abspath(__file__))

def rd(p): return open(os.path.join(SP, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(SP, p), 'w', encoding='utf-8').write(s)

ok, miss = [], []
def ins(text, anchor, addition, before=False, name=''):
    if anchor not in text:
        miss.append(name); return text
    ok.append(name)
    return text.replace(anchor, (addition + anchor) if before else (anchor + addition), 1)

# ================= part4: 활동지 4종 추가 =================
p4 = rd('part4_ws_canva_cases.html')

p4 = p4.replace('<div class="section-title"><div class="num">4</div> 학습지원도구 — 활동지 7종 (바로 인쇄해 쓰는 양식)</div>',
                '<div class="section-title"><div class="num">4</div> 학습지원도구 — 활동지·창업 도구 12종 (바로 인쇄해 쓰는 양식)</div>')
p4 = p4.replace('핵심 활동지 5종에 더해 <b>창업 도구 시트 2종(브레인라이팅 4-3-4 · 이해관계자 지도)</b>을 함께 제공합니다.',
                '활동지 ①~⑦ 전 양식과 <b>창업 도구 시트 5종(브레인라이팅·이해관계자 지도·자원 인벤토리·시나리오 보드·가상 투자권)</b>을 모두 제공합니다 — 이 페이지만으로 준비물이 끝납니다.')

p4 = ins(p4, "<button class=\"ws-tab on\" onclick=\"wsTab(this,'ws2')\">② 문제 정의문 · 5WHY</button>",
         "<button class=\"ws-tab\" onclick=\"wsTab(this,'ws1')\">① 역량 자기진단 (1차시)</button>\n    ", before=True, name='tab1')
p4 = ins(p4, "<button class=\"ws-tab\" onclick=\"wsTab(this,'ws6')\">⑥ AI 활용 기록지</button>",
         "<button class=\"ws-tab\" onclick=\"wsTab(this,'ws5')\">⑤ 동료 평가지 (10차시)</button>\n    ", before=True, name='tab5')
p4 = ins(p4, "<button class=\"ws-tab\" onclick=\"wsTab(this,'wsRI')\">➕ 자원 인벤토리 (7차시)</button>",
         "\n    <button class=\"ws-tab\" onclick=\"wsTab(this,'wsSB')\">➕ 시나리오 보드 (9차시)</button>\n    <button class=\"ws-tab\" onclick=\"wsTab(this,'wsIV')\">➕ 가상 투자권 (10차시)</button>", name='tabSBIV')

WS1 = """
  <!-- 활동지 ① -->
  <div class="ws-sheet" id="ws1">
    <h4>활동지 ① 역량 자기진단과 역할 정하기</h4>
    <div class="ws-meta">1차시 · 개인 → 모둠 | 기준: "잘한다"가 아니라 <b>"굳이 고르면 이게 낫다"</b> — 2개에 ✔ 하세요. 진단 결과는 성적이 아닙니다.</div>
    <div class="table-wrap" style="box-shadow:none; border:1px solid var(--line);">
      <table style="min-width:520px;">
        <thead><tr><th style="width:56px;">✔</th><th>굳이 고르면, 나는 이게 낫다</th><th style="width:170px;">어울리는 역할</th></tr></thead>
        <tbody>
          <tr><td class="td-c">☐</td><td>숫자·표를 다루고 출처를 확인하는 것</td><td>CDO (데이터 담당)</td></tr>
          <tr><td class="td-c">☐</td><td>손으로 만들고 조립하고 기기를 다루는 것</td><td>CTO (제작 담당)</td></tr>
          <tr><td class="td-c">☐</td><td>글로 정리하고 기록을 남기는 것</td><td>CEO (기록·조율)</td></tr>
          <tr><td class="td-c">☐</td><td>사람들 앞에서 말하고 설득하는 것</td><td>CMO (발표 담당)</td></tr>
          <tr><td class="td-c">☐</td><td>엉뚱한 아이디어를 내는 것</td><td>어느 역할이든 + 발상 촉진</td></tr>
          <tr><td class="td-c">☐</td><td>일정을 짜고 사람을 조율하는 것</td><td>CEO (기록·조율)</td></tr>
        </tbody>
      </table>
    </div>
    <div class="ws-grid2">
      <div class="ws-field"><label>팀명 (우리 회사 이름)</label><input class="ws-line"></div>
      <div class="ws-field"><label>나의 역할 <span class="hint">겸임 가능</span></label><input class="ws-line"></div>
    </div>
    <div class="ws-field"><label>팀 공동가치 · 공동규칙 한 줄 <span class="hint">예: "숫자 없는 주장은 하지 않는다"</span></label><input class="ws-line"></div>
    <div class="ws-field"><label>"창업가정신은 (&nbsp;&nbsp;&nbsp;&nbsp;)이다" <span class="hint">— 10차시에 다시 꺼내 비교합니다. 솔직하게!</span></label><input class="ws-line"></div>
    <div class="ws-example"><b>팀 구성 규칙</b> — 나와 <b>다른 항목</b>에 ✔한 친구를 찾아 3~4명 팀을 만드세요. 강점이 겹치는 팀은 약점도 겹칩니다.</div>
    <button class="print-btn" onclick="window.print()" style="margin-top:16px;">🖨 이 활동지 인쇄</button>
  </div>
"""
p4 = ins(p4, '  <!-- 활동지 ② -->', WS1 + '\n  <!-- 활동지 ② -->', before=True, name='ws1')
p4 = p4.replace(WS1 + '\n  <!-- 활동지 ② -->' + WS1, WS1 + '\n  <!-- 활동지 ② -->')

WS5 = """
  <!-- 활동지 ⑤ -->
  <div class="ws-sheet" id="ws5">
    <h4>활동지 ⑤ 동료 평가지 (관람자용)</h4>
    <div class="ws-meta">10차시 · 부스 관람자 | 규칙: 팀마다 <b>질문 1개 의무</b> — "좋았어요"는 질문이 아닙니다. 질문의 질이 곧 나의 평가 점수입니다.</div>
    <div class="table-wrap" style="box-shadow:none; border:1px solid var(--line);">
      <table style="min-width:560px;">
        <thead><tr><th style="width:90px;">팀명</th><th style="width:110px;">숫자 근거</th><th>내가 던진 질문</th><th>장점 1 · 보완점 1</th></tr></thead>
        <tbody>
          <tr><td style="height:46px;"></td><td class="td-c">있다 ☐ 없다 ☐</td><td></td><td></td></tr>
          <tr><td style="height:46px;"></td><td class="td-c">있다 ☐ 없다 ☐</td><td></td><td></td></tr>
          <tr><td style="height:46px;"></td><td class="td-c">있다 ☐ 없다 ☐</td><td></td><td></td></tr>
          <tr><td style="height:46px;"></td><td class="td-c">있다 ☐ 없다 ☐</td><td></td><td></td></tr>
          <tr><td style="height:46px;"></td><td class="td-c">있다 ☐ 없다 ☐</td><td></td><td></td></tr>
          <tr><td style="height:46px;"></td><td class="td-c">있다 ☐ 없다 ☐</td><td></td><td></td></tr>
        </tbody>
      </table>
    </div>
    <div class="ws-field"><label>오늘 가장 투자하고 싶었던 팀과 그 이유 <span class="hint">데이터·실현 가능성 기준 한 줄</span></label><input class="ws-line"></div>
    <div class="ws-example"><b>좋은 질문의 예</b> — "그 수치의 출처는 어디인가요?" · "데이터가 반대로 나왔다면 어떻게 했을 건가요?" · "이 모델이 틀리는 경우는 언제인가요?"</div>
    <button class="print-btn" onclick="window.print()" style="margin-top:16px;">🖨 이 활동지 인쇄</button>
  </div>
"""
p4 = ins(p4, '  <!-- 활동지 ⑥ -->', WS5 + '\n  <!-- 활동지 ⑥ -->', before=True, name='ws5')
p4 = p4.replace(WS5 + '\n  <!-- 활동지 ⑥ -->' + WS5, WS5 + '\n  <!-- 활동지 ⑥ -->')

WSSB = """
  <!-- 시나리오 보드 -->
  <div class="ws-sheet" id="wsSB">
    <h4>사용자 시나리오 보드 — 적용 전 → 후, 네 장면</h4>
    <div class="ws-meta">9차시 · 모둠 | 그림+한 줄로 충분합니다. 이 보드가 10차시 포스터의 뼈대가 됩니다.</div>
    <div class="ws-grid2">
      <div class="ws-field"><label>① 지금의 문제 장면 <span class="hint">누가, 어디서, 어떤 불편</span></label><textarea class="ws-area" style="min-height:110px;"></textarea></div>
      <div class="ws-field"><label>② 우리 MVP를 만나는 장면 <span class="hint">사용자가 처음 쓰는 순간</span></label><textarea class="ws-area" style="min-height:110px;"></textarea></div>
      <div class="ws-field"><label>③ 달라진 장면 <span class="hint">숫자로 표현 — 몇 초/몇 건/몇 % 개선?</span></label><textarea class="ws-area" style="min-height:110px;"></textarea></div>
      <div class="ws-field"><label>④ 확산 장면 <span class="hint">누구에게까지 퍼질 수 있나 (다음 단계)</span></label><textarea class="ws-area" style="min-height:110px;"></textarea></div>
    </div>
    <div class="ws-example"><b>작성 예시 · 무더위쉼터 팀</b> — ① 폭염 속 어르신이 먼 쉼터까지 걷는다 → ② 최적 입지 지도가 신설 위치를 제안한다 → ③ 평균 접근 거리 손실 10.07% 개선 → ④ 다른 자치구 24개 동에도 같은 계산 적용.</div>
    <button class="print-btn" onclick="window.print()" style="margin-top:16px;">🖨 이 활동지 인쇄</button>
  </div>
"""
WSIV = """
  <!-- 가상 투자권 -->
  <div class="ws-sheet" id="wsIV">
    <h4>가상 투자권 — 모의 크라우드펀딩 (모둠당 1,000만 원)</h4>
    <div class="ws-meta">10차시 · 모둠 | 규칙: 반드시 <b>서로 다른 2개 팀</b>에 분산 투자 · 미투자 시 잔액 절반 삭감 · 투자처는 개표 전까지 비밀</div>
    <div class="ws-grid2">
      <div style="border:2px dashed var(--orange); border-radius:12px; padding:16px;">
        <div style="font-weight:900; color:var(--orange); font-size:15px;">💵 투자권 A — 금액: (&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;) 만 원</div>
        <div class="ws-field"><label>투자할 팀</label><input class="ws-line"></div>
        <div class="ws-field"><label>투자 근거 한 줄 <span class="hint">느낌 말고 데이터·실현 가능성</span></label><input class="ws-line"></div>
      </div>
      <div style="border:2px dashed var(--blue); border-radius:12px; padding:16px;">
        <div style="font-weight:900; color:var(--blue); font-size:15px;">💵 투자권 B — 금액: (&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;) 만 원</div>
        <div class="ws-field"><label>투자할 팀</label><input class="ws-line"></div>
        <div class="ws-field"><label>투자 근거 한 줄</label><input class="ws-line"></div>
      </div>
    </div>
    <div class="ws-field"><label>투자한 모둠명 (서명)</label><input class="ws-line" style="max-width:280px;"></div>
    <div class="ws-example"><b>교사 운영</b> — A+B 합이 1,000만 원이 되게 안내(예: 700+300). 개표 후 팀별 유치액을 칠판에 집계하면 그대로 '시장의 평가' 데이터가 됩니다.</div>
    <button class="print-btn" onclick="window.print()" style="margin-top:16px;">🖨 이 활동지 인쇄</button>
  </div>
"""
p4 = ins(p4, '  <!-- 브레인라이팅 시트 -->', WSSB + WSIV + '\n  <!-- 브레인라이팅 시트 -->', before=True, name='wsSB-IV')
p4 = p4.replace(WSSB + WSIV + '\n  <!-- 브레인라이팅 시트 -->' + WSSB + WSIV, WSSB + WSIV + '\n  <!-- 브레인라이팅 시트 -->')
wr('part4_ws_canva_cases.html', p4)

# ================= part3: 치트시트·역설계 정답·칩 연결 =================
p3 = rd('part3_lessons.html')

CHEAT = """
          <div class="info-box purple">
            <div class="box-title">스프레드시트 함수 치트시트 — 칠판에 그대로 판서</div>
            <p><code>=AVERAGE(범위)</code> 평균 · <code>=MEDIAN(범위)</code> 중앙값 · <code>=STDEV(범위)</code> 표준편차 · <code>=CORREL(x범위, y범위)</code> 상관계수 r</p>
            <p><code>=SLOPE(y범위, x범위)</code> 회귀 기울기 a · <code>=INTERCEPT(y범위, x범위)</code> 절편 b · <code>=TREND(y범위, x범위, 새x)</code> 예측값</p>
            <p>산점도 그리기: 두 열 선택 → 삽입 → 차트 → 분산형(산점도) → 추세선 표시. 구글 시트·엑셀 공통이며, 아래 실습기가 같은 계산을 화면에서 보여 줍니다.</p>
          </div>
"""
p3 = ins(p3, '          <div class="sub-title" style="margin-top:16px;">웹 체험 ④ 데이터 분석 실습기', CHEAT + '          ', before=True, name='L4-cheat')

ANSWER = """
          <div class="info-box purple">
            <div class="box-title">교사용 · BMC 역설계 게임 정답 예시 (도입 10분)</div>
            <p><b>진행</b>: "이 회사의 고객은 누구일까?"만 먼저 공개하고 나머지 블록을 모둠이 거꾸로 채우게 한 뒤, 아래 예시와 대조합니다.</p>
            <p><b>배달 플랫폼</b> — 고객군: 주문 고객 + 입점 식당(양면 시장) / 가치제안: 빠른 배달·넓은 선택(고객), 신규 손님(식당) / 채널: 앱 / 수익: 중개 수수료·광고·배달비 / 비용: 라이더·마케팅·서버 / 핵심자원: 플랫폼·라이더망 / 핵심활동: 주문 매칭·평점 관리 / 파트너: 식당·결제사 / 고객관계: 리뷰·쿠폰</p>
            <p><b>카페 프랜차이즈</b> — 고객군: 직장인·학생 / 가치제안: 어디서나 같은 맛·머물 공간 / 채널: 매장·앱 주문 / 수익: 음료+굿즈+멤버십 / 비용: 임대·원두·인건비 / 핵심자원: 브랜드·입지 / 핵심활동: 로스팅·신메뉴 / 파트너: 원두 농가·물류 / 고객관계: 멤버십 적립</p>
            <p style="font-size:.88em; color:var(--sub);">포인트 발문: "두 회사 모두 <b>돈을 내는 사람과 가치를 받는 사람이 같은가?</b>" — 양면 시장 개념이 자연스럽게 나옵니다.</p>
          </div>
"""
p3 = ins(p3, '          <div class="sub-title" id="bm-examples"', ANSWER + '          ', before=True, name='L6-answer')

p3 = ins(p3, '🎛 웹 자기진단(이 화면)</a>', '<a class="pk" href="#ws1">📄 활동지① (바로 인쇄)</a>', name='chip-ws1')
p3 = p3.replace('<a class="pk" href="#worksheets">📄 활동지①</a>', '<a class="pk" href="#ws1">📄 활동지①</a>')
p3 = p3.replace('<a class="pk" href="#worksheets">📄 시나리오 보드</a>', '<a class="pk" href="#wsSB">📄 시나리오 보드 (바로 인쇄)</a>')
p3 = p3.replace('<a class="pk" href="#worksheets">📄 활동지⑤·⑦</a>', '<a class="pk" href="#ws5">📄 활동지⑤ 동료 평가지</a><a class="pk" href="#ws7">📄 활동지⑦ 성찰지</a><a class="pk" href="#wsIV">💵 가상 투자권 (바로 인쇄)</a>')
wr('part3_lessons.html', p3)

print('OK:', ok)
print('MISS:', miss if miss else 'none')
