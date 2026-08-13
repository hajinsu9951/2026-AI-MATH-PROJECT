# -*- coding: utf-8 -*-
"""활동지 12종에 진행 순서(STEP) 안내 삽입"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
SP = os.path.dirname(os.path.abspath(__file__))

STEPS = {
 'ws1': '① 혼자 6항목 중 <b>2개만</b> ✔ (1분) → ② 결과를 들고 <b>나와 다른 항목</b>에 ✔한 친구 찾기 (3분) → ③ 3~4명 팀 확정, 팀명·역할·공동규칙 합의 (5분) → ④ "창업가정신은 ( )이다" 각자 솔직하게 쓰고 제출 — 10차시에 다시 만납니다.',
 'ws2': '① 맨 위 칸에 문제를 <b>4요소 문장</b>으로 (조립기 도구를 써도 좋음) → ② 재는 숫자 → 공공데이터 → 직접 셀 것 순서로 채움 → ③ 두 출처가 다르면 "왜?"를 반드시 기록 → ④ 5WHY는 막히는 곳까지만(막힌 곳 = 측정할 곳) → ⑤ 사분면에 ✔ 하고 교사 확인 받기.',
 'ws3': '① 모델 4종 표에서 우리 문제 유형에 ✔ → ② 웹 실습 기록: KNN 표 → K-means 한 줄 순서로 → ③ 증명 빈칸(f′(μ)=0)을 모둠이 함께 유도 → ④ 고른 모델+이유 3문장 → ⑤ <b>"틀릴 수 있는 경우"</b>까지 써야 완성(상 기준) — 교사 확인 도장.',
 'ws4': '① 대안 3개에 이름 붙이기(A/B/C) → ② 지표 3개 합의 — <b>최소 1개는 숫자</b> → ③ 칸을 채우고 종합 판단 → ④ 옆 모둠 지적을 <b>반박 없이</b> 그대로 받아 적기 → ⑤ 별표 받은 위험 가정을 7차시 검증 대상으로.',
 'ws5': '① 부스 출발 전 방문할 팀명 6칸을 미리 기입 → ② 부스마다 숫자 근거 있다/없다 ✔ → ③ <b>질문 1개</b> 기록("좋았어요"는 반려) → ④ 장점 1·보완점 1 → ⑤ 마지막 줄: 가장 투자하고 싶은 팀과 이유.',
 'ws6': '① 사용한 도구 이름부터 → ② 프롬프트는 <b>복사-붙여넣기 원문 그대로</b> → ③ 어디에 얼마나 반영했는지 → ④ 내가 검증·수정한 부분 → ⑤ 교사의 두 질문에 답을 쓰면 완성 — 쓴 만큼 정확히 적으면 감점 없음.',
 'ws7': '① 1차시 활동지①을 옆에 펴 놓기 → ② 1~5번을 순서대로(구체적 사건으로) → ③ 재진단 표의 <b>지금</b> 열에 다시 ✔ → ④ 1차시와 달라진 항목마다 변화 한 줄 → ⑤ 제출 전에 "막힌 지점-극복"이 구체적인지 스스로 검사.',
 'wsBW': '① 맨 위에 우리 팀 문제 정의문을 옮겨 적기 → ② 1회전: 말없이 내 아이디어 3개 → ③ 종이 울리면 시트를 <b>왼쪽으로</b> → ④ 2~4회전: 앞사람 것에 덧붙이거나 사칙연산(＋−×÷)으로 변형 → ⑤ 별점 스티커로 상위 3개 선정(차용은 출처 팀명 기록).',
 'wsSH': '① 세 부류(수혜자/운영·결정자/반대·경쟁)에 <b>구체적인 사람</b> 채우기 → ② 그 사람이 할 법한 "한 마디"를 상상해 쓰기 → ③ 확인 방법(인터뷰·관찰·데이터) 정하기 → ④ 아래 문장틀로 가치 제안 조립 — 이게 6차시 BMC의 가운데 칸이 됩니다.',
 'wsRI': '① <b>가진 것</b>부터 센다(부족한 것 먼저 쓰지 않기!) → ② 기능·도구·데이터·사람 4행 채우기 → ③ 구할 곳은 실명·기관명으로 → ④ 완성 기준을 "버튼을 누르면 ~가 뜬다" 형식 한 문장으로 쓰고 전원 서명.',
 'wsSB': '① 지금의 문제 장면(누가·어디서·어떤 불편) → ② 우리 MVP를 처음 만나는 장면 → ③ 달라진 장면은 <b>숫자로</b>(몇 초·몇 건·몇 %) → ④ 확산 장면 — 이 네 칸 순서가 그대로 10차시 포스터의 뼈대입니다.',
 'wsIV': '① 부스를 <b>전부 돈 후</b>에 기입 → ② A+B 합계가 1,000만 원이 되게 배분 → ③ 반드시 서로 다른 두 팀 → ④ 근거는 느낌이 아니라 데이터·실현 가능성 한 줄 → ⑤ 접어서 마감함에 — 개표 전까지 비밀.',
}

p4 = open(os.path.join(SP, 'part4_ws_canva_cases.html'), encoding='utf-8').read()
cnt = 0
for wid, steps in STEPS.items():
    i = p4.find('id="' + wid + '"')
    if i < 0:
        print('MISS sheet', wid)
        continue
    m = p4.find('<div class="ws-meta">', i)
    e = p4.find('</div>', m) + len('</div>')
    block = '\n    <div class="ws-steps"><b>진행 순서</b> — ' + steps + '</div>'
    if '<div class="ws-steps">' not in p4[i:i+600]:
        p4 = p4[:e] + block + p4[e:]
        cnt += 1
open(os.path.join(SP, 'part4_ws_canva_cases.html'), 'w', encoding='utf-8').write(p4)
print('진행 순서 삽입:', cnt, '/ 12')

p1 = open(os.path.join(SP, 'part1_head.html'), encoding='utf-8').read()
CSS = '''  .ws-steps { background: #EEF5FB; border: 1.5px dashed var(--light-blue); border-radius: 10px;
    padding: 11px 14px; font-size: 13px; color: #27435F; margin: 0 0 14px; line-height: 1.85; }
  .ws-steps b { color: var(--blue); }
'''
if '.ws-steps' not in p1:
    p1 = p1.replace('  /* ---- 사례 썸네일 그리드 ---- */', CSS + '  /* ---- 사례 썸네일 그리드 ---- */', 1)
    open(os.path.join(SP, 'part1_head.html'), 'w', encoding='utf-8').write(p1)
    print('ws-steps CSS 완료')
