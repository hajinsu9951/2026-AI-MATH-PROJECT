# -*- coding: utf-8 -*-
"""성과 수치 30 · STEAM 2026 · 실적 증빙 클릭 · 파급 삭제 · 캔바 아코디언 · 고객분석/린 미니 모듈"""
import sys, os, re
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

# ---------------- part1: CSS ----------------
p1 = rd('part1_head.html')
CSS = """
  /* ---- 성과 수치 그리드 ---- */
  .num-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(158px, 1fr)); gap: 9px; margin: 14px 0; }
  .num-chip { background: var(--card); border: 1px solid var(--line); border-radius: 11px; padding: 11px 12px; }
  .num-chip .nv { font-size: 16.5px; font-weight: 900; color: var(--blue); line-height: 1.3; }
  .num-chip .nl { font-size: 11.5px; color: var(--sub); line-height: 1.5; margin-top: 2px; display: block; }
  .num-chip.hot .nv { color: var(--orange); }

  /* ---- 실적 증빙 ---- */
  .award-list li.has-ev { cursor: zoom-in; border-left-color: var(--green); }
  .award-list li.has-ev b::after { content: " 📎 증빙 보기"; font-size: 11px; color: var(--green); font-weight: 800; }

  /* ---- 교사 개발 자료 아코디언 ---- */
  .cv-acc { display: flex; flex-direction: column; gap: 10px; margin: 16px 0; }
  .cv-item { background: var(--card); border: 1px solid var(--line); border-radius: 13px; overflow: hidden; }
  .cv-item .cv-head { display: flex; align-items: center; gap: 10px; padding: 14px 18px; cursor: pointer; flex-wrap: wrap; user-select: none; }
  .cv-item .cv-head b { flex: 1; font-size: 15px; color: var(--navy); min-width: 220px; }
  .cv-item .cv-head .t-arrow { transition: transform .25s; color: var(--sub); }
  .cv-item.open .cv-head .t-arrow { transform: rotate(180deg); }
  .cv-item .cv-body2 { display: none; padding: 4px 18px 18px; border-top: 1px dashed var(--line); grid-template-columns: minmax(200px, 320px) 1fr; gap: 16px; align-items: start; }
  .cv-item.open .cv-body2 { display: grid; }
  .cv-item .cv-body2 img { width: 100%; border-radius: 10px; border: 1px solid var(--line); }
  .cv-item .cv-body2 img.portrait { max-height: 330px; object-fit: contain; background: #F4F0EC; }
  @media (max-width: 680px) { .cv-item .cv-body2 { grid-template-columns: 1fr; } }

"""
p1 = ins(p1, '  /* ---- 라이트박스(확대 보기) ---- */', CSS + '  /* ---- 라이트박스(확대 보기) ---- */', before=False, name='css')
if CSS not in p1:
    p1 = p1.replace('  /* ---- 이전 위치로 버튼 ---- */', CSS + '  /* ---- 이전 위치로 버튼 ---- */', 1)
wr('part1_head.html', p1)

# ---------------- part4b: 숫자 30 · 실적 증빙 · STEAM · 파급 삭제 ----------------
p4b = rd('part4b_cases.html')

NUMS = [
 ('−5.97%', '평균 이동시간 감소 (교실 배치, 52.28→49.16초)', 1),
 ('−470건', '장거리 이동 감소 (2,672→2,202건)', 0),
 ('−13.00%', '복도 누적 혼잡 부담 감소', 0),
 ('−13.63%', '배치 최적화 목적함수 개선', 0),
 ('60,000회', '담금질 탐색 (20 seed × 3,000회)', 0),
 ('0건', '최적 배치안의 제약 충돌·실패', 0),
 ('−24.09%', '통학로 위험도 감소 (파레토 경로)', 1),
 ('+2.34%', '수용한 거리 증가 (안전 우회 비용)', 0),
 ('48,767개', '보행 네트워크 노드 (전수 구축)', 0),
 ('139,634개', '보행 네트워크 유향 간선', 0),
 ('100%', '최적해 인증 통과 (6개 구간 검증)', 0),
 ('1.12%', '평균 근사 오차(gap) · p95 3.90%', 0),
 ('54→6개', '경로의 고위험 구간 통과 수 감소', 0),
 ('27,596명', '독거노인 전수 분석 (24개 행정동)', 1),
 ('9.7배', '동별 독거노인 밀집 격차', 0),
 ('10.07%', '쉼터 신설 시 접근성 손실 개선율', 0),
 ('949.61→854.01', '가중 접근성 손실함수 값 개선', 0),
 ('3종', '거리 산식 교차 검증 (하버사인·유클리드·맨해튼)', 0),
 ('224곳', '무더위쉼터 전수 조사', 0),
 ('64.4%', '공공자전거 반납률 — 문제의 출발 숫자', 1),
 ('2단계', '군집(비지도)→회귀(지도) 결합 예측 구조', 0),
 ('−32.5→−58.2', 'Wi-Fi 실측 신호 범위(dBm) — 데드존 없음 입증', 0),
 ('9·5·9', '교실 부하 3유형 군집 (혼잡·중간·안정)', 0),
 ('15개', '교내 AP 상호 수신 전수 분석', 0),
 ('20개', '폐의약품 수거 거점 최적 순회 설계', 0),
 ('100명', '학기당 정규 교과 참여 (3학년 전체)', 1),
 ('80팀', '공개 아카이브 수록 산출물', 0),
 ('70팀', '수상 (대상 10 · 최우수 10 · 우수 20 · 장려 30)', 0),
 ('8/8단계', '창업가정신 함양 모형 완주율', 0),
 ('12종·10종', '활동지 · 웹 수업 도구 (본 교안 내장)', 0),
]
numgrid = '\n  <div class="sub-title">성과 수치 30 — 우수 사례가 남긴 숫자들</div>\n  <div class="num-grid">\n' + '\n'.join(
    f'    <div class="num-chip{" hot" if hot else ""}"><div class="nv">{v}</div><span class="nl">{l}</span></div>'
    for v, l, hot in NUMS) + '\n  </div>\n'
p4b = ins(p4b, '  <div class="sub-title">수업 밖으로 이어진 실적', numgrid + '\n  ', before=True, name='num30')

# 실적: STEAM 2026 추가 + 증빙 클릭(ev-01~ev-11.jpg 규약)
OLD_AW = re.search(r'<ul class="award-list">[\s\S]*?</ul>', p4b)
AWARDS = [
 ('ev-01', '대한민국 청소년 창업경진대회', '지역 예선 1위·2위 — 수업 산출물이 그대로 출전작으로'),
 ('ev-02', '학생 창업유망팀 300+ 육성과정 (한국청년기업가정신재단)', '최종 선발'),
 ('ev-03', '제22회 전국 Junior 창업캠프 & 창업아이템 경진대회', '대상 · 우수상 · 장려상 수상'),
 ('ev-04', '제19회 전국학생창업발명 경진대회', '2차(대면) 심사 진출'),
 ('ev-05', '전국 발명 전람회', '2025 대통령상 · 2026 국무총리상 (STEAM 동아리 연계 심화)'),
 ('ev-06', '2025 STEAM 클럽', '전국 1위'),
 ('ev-07', '2026 STEAM 클럽', '현재 2개 동아리 운영 중 — 수업 우수 팀의 심화 무대'),
 ('ev-08', 'NEXT-창업인재성장 프로젝트 (창업중심대학)', '해커톤·창업아이디어 경진 참가'),
 ('ev-09', '도마켓 프로젝트 (청소년 비즈쿨 연계, 제3회)', '학생 주도 로컬 브랜딩 마켓 — 상권 분석·제품 기획·제작·판매·성과공유까지 자체 운영'),
 ('ev-10', '청소년 비즈쿨 모의투자대회 · 창업캠프 메이커톤', '교내 운영 — 10차시의 모의 크라우드펀딩이 실전 대회로 확장'),
 ('ev-11', '공공창업·봉사 연계 프로젝트', "지역 보육원 연계 'EC 봉사창업' — 봉사에서 발견한 문제를 창업 아이템으로"),
]
aw_html = '<!-- 📎 증빙 넣는 법: docs 폴더에 ev-01.jpg ~ ev-11.jpg (상장·공문·현장 사진)를 저장하면 해당 실적에 "증빙 보기"가 나타나고 클릭 시 확대됩니다. 번호는 아래 항목 순서와 같습니다. -->\n  <ul class="award-list">\n' + '\n'.join(
    f'    <li data-ev="{ev}.jpg" data-title="{t}" onclick="return evClick(this)"><b>{t}</b><span>{d}</span></li>'
    for ev, t, d in AWARDS) + '\n  </ul>'
assert OLD_AW, 'award-list not found'
p4b = p4b[:OLD_AW.start()] + aw_html + p4b[OLD_AW.end():]
ok.append('awards-ev')

# 파급 박스 삭제
PGB = re.search(r'\s*<div class="info-box green">\s*<div class="box-title">타 교육자에게로 — 파급</div>[\s\S]*?</div>\n', p4b)
if PGB:
    p4b = p4b[:PGB.start()] + '\n' + p4b[PGB.end():]
    ok.append('remove-spread')
else:
    miss.append('remove-spread')
wr('part4b_cases.html', p4b)

# ---------------- part4: 캔바 아코디언 ----------------
p4 = rd('part4_ws_canva_cases.html')
CANVA = [
 ('CANVA · 프레젠테이션', '린 비즈니스 모델 수업 — Lean Startup 방법론 적용', '{{B64_LEAN}}', '',
  '만들기–측정–학습 루프를 고교 수업 언어로 풀어낸 본 수업의 이론 백본 자료. 6차시 BMC와 8~10차시 루프 운영의 교사용 가이드.',
  'https://www.canva.com/design/DAG59VshAUw/ctm8JX5xY45lsaq9OV0VjA/view', 'style="aspect-ratio:2/1; object-fit:cover; object-position:top;"'),
 ('CANVA · 8p 튜토리얼', '지역사회 문제 해결 + 인공지능수학 + BMC 구성 (CANDOISM)', '{{B64_BMC}}', 'portrait',
  "CANDOISM('할 수 있는 마음가짐')에서 출발해 비즈니스 아이디어 발굴 → 비즈니스 모델 캔버스 구성까지, 5~6차시 학생 배포용 튜토리얼.",
  'https://www.canva.com/design/DAGpXuCYJ08/l1VDf026d15chyFm2v1pGg/view', ''),
 ('CANVA · 39p 사례집', '첨단산업 ABCDE 수업에 비즈니스모델 적용하기', '{{B64_ABCDE}}', '',
  'AI·Bio·Culture·Defense·Energy 5대 첨단산업 프로젝트(음성 안내 자판기, 안심 급식 앱, 전통시장 숏폼, 구조 드론, 에너지 절약)에 BMC를 적용한 확장 사례집.',
  'https://www.canva.com/design/DAG50iD_pY8/i82pASm9Bku02mZGLkIClg/view', ''),
 ('CANVA · 프레젠테이션', '첨단ABCDE 산업과 AI 비즈니스 모델 수업 (Customer Discovery)', '{{B64_ABCDE2}}', '',
  '고객 탐색(Customer Discovery)과 린 스타트업 방법론을 첨단산업 프로젝트에 접목한 수업 개요 자료. 6차시 도입 프레젠테이션.',
  'https://www.canva.com/design/DAG5qv542Uc/H6CyJYDxJOS-BSaUDAjPJg/view', 'style="aspect-ratio:2/1; object-fit:cover; object-position:top;"'),
 ('CANVA · 인포그래픽', '고객 탐색을 결합한 프로젝트 설계도 구성하기', '{{B64_CUSTD}}', 'portrait',
  '5대 산업별 고객 탐색 활동과 수업·학생 사례를 QR로 연결한 한 장짜리 설계도. 교사 연수·수업 안내용.',
  'https://www.canva.com/d/REi1XwFLZRg3l2k', ''),
]
acc = '<div class="cv-acc">\n' + '\n'.join(
    f'''  <div class="cv-item{' open' if i == 0 else ''}">
    <div class="cv-head" onclick="cvToggle(this)"><span class="cv-kind">{k}</span><b>{t}</b><span class="t-arrow">▼</span></div>
    <div class="cv-body2">
      <img class="{'portrait' if por else ''}" {extra} src="{img}" alt="{t} 미리보기">
      <div><p style="font-size:14px; color:#33404d; line-height:1.75;">{d}</p><a class="cv-link" href="{u}" target="_blank" rel="noopener" style="display:inline-block; margin-top:12px;">캔바에서 열기 →</a></div>
    </div>
  </div>''' for i, (k, t, img, por, d, u, extra) in enumerate(CANVA)) + '\n</div>'

m = re.search(r'<div class="grid g3">\s*<div class="canva-card">[\s\S]*?</div>\n  </div>\n(  <div class="info-box" style="margin-top:18px;">)', p4)
assert m, 'canva grid not found'
p4 = p4[:m.start()] + acc + '\n' + m.group(1) + p4[m.end():]
ok.append('canva-acc')
p4 = p4.replace('<div class="section-lead">본 수업을 위해 교사가 직접 개발한 프레젠테이션·튜토리얼 자료입니다. 링크에서 원본을 열람하고 수업에 바로 활용할 수 있습니다.</div>',
                '<div class="section-lead">본 수업을 위해 교사가 직접 개발한 프레젠테이션·튜토리얼 자료입니다. <b>제목을 누르면 하나씩 펼쳐집니다</b> — 미리보기 확인 후 [캔바에서 열기]로 원본을 수업에 바로 띄우세요.</div>')
wr('part4_ws_canva_cases.html', p4)

# ---------------- part3: 고객 분석 모듈(5차시) + 린 미니 강의(6차시) ----------------
p3 = rd('part3_lessons.html')
CD = """
          <div class="sub-title" style="margin-top:16px;">고객 분석(Customer Discovery) 미니 모듈 — 인터뷰로 가설을 확인한다</div>
          <div class="grid g2">
            <div class="info-box orange" style="margin:0;">
              <div class="box-title">미니 강의 판서안 (5분)</div>
              <p><b>고객 ≠ 사용자</b> — 고객은 우리 해결책에 돈·시간·관심을 실제로 내는 사람이다. "모두를 위한 것"은 아무도의 것이 아니다 → 세그먼트를 좁혀라.</p>
              <p><b>문제 인터뷰 3원칙</b> — ① 해결책을 먼저 말하지 않는다 ② 의견이 아니라 <b>과거의 행동</b>을 묻는다 ③ 유도 질문 금지("이런 앱 있으면 쓰실 거죠?"는 반칙).</p>
              <p><b>판정 기준(문제-해결 fit)</b> — 고객이 문제를 스스로 인정했는가? + 이미 어떻게든 해결하려 시도했는가? 둘 다 '예'일 때만 다음 단계로.</p>
            </div>
            <div class="info-box" style="margin:0;">
              <div class="box-title">문제 인터뷰 스크립트 5문항 (학생 배포용)</div>
              <p>① 최근에 (문제 상황)을 겪은 적이 있으세요? 언제, 어디서였나요?</p>
              <p>② 그때 실제로 어떻게 하셨나요? <span style="color:var(--sub);">(과거 행동)</span></p>
              <p>③ 그 과정에서 가장 불편했던 순간은 무엇이었나요?</p>
              <p>④ 해결해 보려고 시도한 방법이 있나요? 왜 계속 쓰지 않으셨나요?</p>
              <p>⑤ 이 문제가 사라지면 무엇이 가장 달라질까요?</p>
              <p style="font-size:.88em; color:var(--sub);">기록법: 응답자/핵심 문장/횟수 표로 정리 — 3명 중 2명 이상이 같은 불편을 말하면 '패턴'으로 인정하고 가치 가설을 갱신한다.</p>
            </div>
          </div>
"""
p3 = ins(p3, '<div class="lp-eval"><b>✔ 평가 요소</b> — 발산 아이디어 수', CD + '          ', before=True, name='L5-cd')

LEAN = """
          <div class="info-box orange">
            <div class="box-title">린 스타트업 5분 미니 강의 (판서안) — BMC에 들어가기 전에</div>
            <p><b>한 줄 정의</b> — "완벽한 계획을 세우는 대신, <b>작게 만들어 빨리 배우는</b> 창업 방법." (에릭 리스, 『린 스타트업』)</p>
            <p><b>판서 구조</b> — 아이디어 →[만들기 Build]→ MVP →[측정 Measure]→ 데이터 →[학습 Learn]→ 유지(persevere) 또는 방향 전환(pivot) → 다시 만들기…</p>
            <p><b>학생용 용어 4</b> — MVP(핵심 가치 하나만 증명하는 최소 제품) · BML 루프(만들고-재고-배우는 반복) · 피벗(데이터가 가설을 기각하면 방향 전환 — 실패가 아니라 진전) · 혁신 회계(느낌이 아니라 숫자로 진척을 재기: 우리 수업에선 J값·오차·투자액·질문 수)</p>
            <p><b>고전 사례 1분</b> — 드롭박스는 제품을 만들기 전에 <b>데모 영상 하나</b>로 수요를 검증했다. 완성보다 검증이 먼저다 — 우리 수업의 '미완성 30초 공개'가 정확히 같은 장치다.</p>
          </div>
"""
p3 = ins(p3, '          <div class="sub-title">비즈니스 모델 체험 — 단계별 상세 지도안', LEAN + '          ', before=True, name='L6-lean')
wr('part3_lessons.html', p3)

# ---------------- part5: evClick JS ----------------
p5 = rd('part5_assess_end.html')
EV = """
function evClick(li) {
  if (!li.classList.contains('has-ev')) return true;
  li.setAttribute('data-big', li.getAttribute('data-ev'));
  return lbOpen(li);
}
function evProbe() {
  document.querySelectorAll('.award-list li[data-ev]').forEach(function (li) {
    var im = new Image();
    im.onload = function () { li.classList.add('has-ev'); };
    im.src = li.getAttribute('data-ev');
  });
}
document.addEventListener('DOMContentLoaded', evProbe);
function cvToggle(head) {
  var item = head.parentElement, acc = item.parentElement;
  var wasOpen = item.classList.contains('open');
  acc.querySelectorAll('.cv-item').forEach(function (i) { i.classList.remove('open'); });
  if (!wasOpen) item.classList.add('open');
}
"""
p5 = p5.replace('var lbList = [], lbIdx = 0;', EV + 'var lbList = [], lbIdx = 0;', 1)
wr('part5_assess_end.html', p5)
ok.append('ev-js')

# ---------------- part2: 역량 9종 카드 클릭 확장 ----------------
p2 = rd('part2_design.html')
COMP = {
 '혁신성': ('해결하고자 하는 문제에 새롭고 창의적인 방식으로 접근해 가치 있는 대안을 제시할 수 있다.',
   '5차시 브레인라이팅 4-3-4와 히치하이킹(타 모둠 아이디어 차용·변형), 6차시 대안 3개 비교',
   '차용한 아이디어를 무엇으로 바꿨는지 말할 수 있는가 — "다르게"의 근거'),
 '진취성': ('외부 변화에서 기회를 발견하고 능동적·선제적으로 대응할 수 있다.',
   '2차시 공공데이터 교차 확인에서 남들이 지나친 빈틈 찾기, 4차시 데이터가 다르면 즉시 계획 수정',
   '교사가 시키기 전에 다음 데이터를 찾으러 가는가'),
 '위험감수성': ('기회의 가치와 위험을 함께 따져 일정 수준의 위험을 감수하고 적극적으로 도전할 수 있다.',
   '4차시 가설 기각의 공개적 수용, 7차시 "감당 가능한 손실"만 걸고 시작, 9차시 미완성 30초 공개',
   '틀릴 수 있는 지점을 스스로 먼저 말하는가(활동지③ "언제 틀리나")'),
 '창업의지': ('창업을 진로의 실질적 선택지로 인식하고 실행 의지를 형성한다.',
   '10차시 부스 피칭·모의 크라우드펀딩, 우수 팀의 교외 대회·동아리 연계(섹션 8)',
   '개선 로드맵에 "다음 단계"가 구체적 일정으로 적히는가'),
 '자원활용능력': ('목표 달성에 필요한 인적·물적·기술·정보 자원을 발굴하고 효율적으로 동원할 수 있다(Bricolage).',
   '7차시 자원 인벤토리 — 가진 것부터 세고, 부족한 것은 "구할 곳"으로 연결(지역 멘토 포함)',
   '인벤토리의 "구할 곳" 칸이 사람 이름·기관명으로 채워지는가'),
 '기회탐색·가치창출': ('일상에서 새로운 기회를 적극 탐색하고 창의적 방식으로 가치 있는 대안을 창출할 수 있다.',
   '2차시 "이건 셀 수 있나요?" 숫자 게이트, 5차시 가치 제안 문장(누구의 어떤 불편을 데이터 근거로)',
   '불편(현상)과 기회(가치)를 구분해 말하는가'),
 '데이터기반 의사결정': ('감이 아니라 수치·근거로 판단하고, 지표로 대안을 비교해 결정할 수 있다.',
   '3~4차시 모델 선택·검증 리포트, 6차시 숫자 지표 1개 이상 규칙, 10차시 투자 근거 한 줄',
   '주장 옆에 수치와 출처가 붙어 있는가 — "숫자 없는 주장은 받지 않는다"'),
 '회복탄력성': ('실패에 좌절하지 않고 원래의 목표를 향해 다시 시작할 수 있다.',
   '9차시 극한 테스트와 트러블슈팅, 미완성 공개 후 보완점 반영, 활동지⑦ "막힌 지점-극복 과정"',
   '지적·오류 이후의 행동이 기록으로 남는가(오류 로그, v2 계획)'),
 '융합적 실행력': ('공동의 목표를 위해 소통하며 여러 교과·자원을 연계해 실제 작동하는 결과로 구현할 수 있다.',
   '8차시 바이브 코딩 — 수학 모델+데이터+센서+웹을 한 산출물에서 작동시키기',
   '산출물 안에서 수학이 어디에 쓰였는지 짚어 설명할 수 있는가'),
}
comp_n = 0
for name, (defi, scene, obs) in COMP.items():
    pat = re.compile(r'<div class="case-card"><div class="cs-top">([^<]*)<b>' + re.escape(name) + r'</b></div><div class="cs-desc">([^<]*)</div></div>')
    m2 = pat.search(p2)
    if not m2:
        miss.append('comp-' + name)
        continue
    icon, desc = m2.group(1), m2.group(2)
    new = (f'<div class="case-card" onclick="this.classList.toggle(\'open\')" style="cursor:pointer;">'
           f'<div class="cs-top">{icon}<b>{name}</b><span class="comp-hint">▾ 자세히</span></div>'
           f'<div class="cs-desc">{desc}</div>'
           f'<div class="cs-more"><b>정의</b> — {defi}<br><b>기르는 장면</b> — {scene}<br><b>관찰 포인트</b> — {obs}</div></div>')
    p2 = p2[:m2.start()] + new + p2[m2.end():]
    comp_n += 1
wr('part2_design.html', p2)
ok.append(f'comp-cards({comp_n}/9)')

# 역량 확장 CSS
p1 = rd('part1_head.html')
CCSS = """
  .case-card .cs-more { display: none; border-top: 1px dashed var(--line); margin-top: 9px; padding-top: 9px; font-size: 12.5px; color: #3a4652; line-height: 1.7; }
  .case-card.open .cs-more { display: block; }
  .comp-hint { margin-left: auto; font-size: 11px; color: var(--orange); font-weight: 800; }

"""
p1 = p1.replace('  /* ---- 성과 수치 그리드 ---- */', CCSS + '  /* ---- 성과 수치 그리드 ---- */', 1)
wr('part1_head.html', p1)

print('OK:', ok)
print('MISS:', miss if miss else 'none')
