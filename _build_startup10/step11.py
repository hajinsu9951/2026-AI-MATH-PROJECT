# -*- coding: utf-8 -*-
"""차시별 디딤 영상 블록 추가"""
import sys, os
sys.stdout.reconfigure(encoding='utf-8')
SP = os.path.dirname(os.path.abspath(__file__))

def rd(p): return open(os.path.join(SP, p), encoding='utf-8').read()
def wr(p, s): open(os.path.join(SP, p), 'w', encoding='utf-8').write(s)

YT = 'https://www.youtube.com/results?search_query='
STEP = [
 ('팀 캔버스(팀명·공동가치·역할) + "창업가정신은 (&nbsp;&nbsp;)이다" 문장</div>',
  '기업가정신이란 무엇인가 (5분)', '도전과 회복탄력성이 드러나는 창업가 인물 이야기 1편을 보고 온다',
  '영상 속 인물이 감수한 위험 1가지는?', '%EA%B8%B0%EC%97%85%EA%B0%80%EC%A0%95%EC%8B%A0+5%EB%B6%84+%ED%8A%B9%EA%B0%95'),
 ('문제 정의문("누가·언제·어디서·무엇 때문에" 포함) + 측정 지표 1개 이상</div>',
  '공공데이터포털 검색법 (5분)', '데이터 검색 → 미리보기 → 내려받기까지의 화면 흐름을 눈에 익힌다',
  '우리 동네 이름으로 검색했을 때 나온 데이터 1개는?', '%EA%B3%B5%EA%B3%B5%EB%8D%B0%EC%9D%B4%ED%84%B0%ED%8F%AC%ED%84%B8+%EC%82%AC%EC%9A%A9%EB%B2%95'),
 ('모델 선택 근거서 초안(모델명 + 이유 3문장 + "언제 틀릴 수 있나")</div>',
  'KNN·K-평균 맛보기 (각 5분)', '원리 암기가 아니라 "언제 쓰는 도구인지" 한 줄로 말할 준비만 하고 온다',
  'KNN과 K-means 중 정답 라벨이 필요한 쪽은?', 'KNN+K-means+%EC%89%BD%EA%B2%8C+%EC%84%A4%EB%AA%85'),
 ('검증 리포트(수치 3개 이상 + 출처) + 모델 선택 근거서 완성</div>',
  '스프레드시트로 상관·추세선 (5분)', 'CORREL 함수와 차트 추세선을 실제로 넣는 장면을 본다',
  '상관계수 r가 0에 가까우면 무슨 뜻인가?', '%EA%B5%AC%EA%B8%80%EC%8B%9C%ED%8A%B8+%EC%83%81%EA%B4%80%EA%B3%84%EC%88%98+%EC%B6%94%EC%84%B8%EC%84%A0'),
 ('가치 제안 초안 1문장 + 이해관계자 지도</div>',
  '디자인씽킹 사례 한 편 (5분)', "'공감 → 문제 정의 → 아이디어'가 실제로 흘러가는 사례를 본다",
  "영상에서 '공감' 단계가 왜 맨 앞이었나?", '%EB%94%94%EC%9E%90%EC%9D%B8%EC%94%BD%ED%82%B9+%EC%82%AC%EB%A1%80'),
 ('팀 BMC 1장 + 대안 3개 비교표(숫자 지표 1개 이상)</div>',
  '비즈니스 모델 캔버스 5분 정리', '9블록의 이름과 위치를 눈에 익히고 온다 (외울 필요 없음)',
  '9블록 중 기억나는 3개는?', '%EB%B9%84%EC%A6%88%EB%8B%88%EC%8A%A4+%EB%AA%A8%EB%8D%B8+%EC%BA%94%EB%B2%84%EC%8A%A4+5%EB%B6%84'),
 ('MVP 설계도(화면 스케치 또는 회로도) + 완성 기준 1문장</div>',
  'MVP란 무엇인가 (5분)', '최소 기능 제품이 완제품과 어떻게 다른지 사례로 본다',
  '영상 속 MVP가 증명하려 한 "한 가지"는 무엇이었나?', 'MVP+%EC%B5%9C%EC%86%8C%EA%B8%B0%EB%8A%A5%EC%A0%9C%ED%92%88+%EC%82%AC%EB%A1%80'),
 ('작동하는 MVP v1 + AI 활용 기록지</div>',
  '프롬프트 잘 쓰는 법 (5분)', '역할·조건·출력 형식을 지정하는 프롬프트 작성 요령을 본다',
  '좋은 프롬프트에 꼭 들어가는 3요소는?', '%ED%94%84%EB%A1%AC%ED%94%84%ED%8A%B8+%EC%9E%91%EC%84%B1%EB%B2%95+%EA%B8%B0%EC%B4%88'),
 ('MVP v2 + 사용자 시나리오 보드 + 피칭덱 초안</div>',
  '엘리베이터 피치 3분 구조 (5분)', '문제→해결→근거 순서로 말하는 짧은 피칭 예시를 본다',
  '피칭에서 가장 먼저 말해야 하는 것은?', '%EC%97%98%EB%A6%AC%EB%B2%A0%EC%9D%B4%ED%84%B0+%ED%94%BC%EC%B9%98+3%EB%B6%84'),
 ('3분 피칭 + 동료 평가 + 투자 결과 + 메타 성찰지 + 개선 로드맵</div>',
  '크라우드펀딩이란 (5분)', '후원형 펀딩 페이지가 어떤 요소(스토리·목표액·리워드)로 구성되는지 본다',
  '후원을 결심하게 만든 페이지 요소는 무엇이었나?', '%ED%81%AC%EB%9D%BC%EC%9A%B0%EB%93%9C%ED%8E%80%EB%94%A9%EC%9D%B4%EB%9E%80'),
]

p3 = rd('part3_lessons.html')
n = 0
for anchor_tail, topic, desc, q, query in STEP:
    anchor = anchor_tail + '\n          </div>'
    if anchor not in p3:
        print('MISS:', topic)
        continue
    block = f'''
          <div class="stepping">📺 <b>디딤 영상 · {topic}</b> — {desc}. <b>확인 질문</b>: "{q}" <a class="pk" href="{YT}{query}" target="_blank" rel="noopener">▶ 영상 찾기</a><span class="st-note">※ 링크는 유튜브 검색으로 연결됩니다 — 학급 플랫폼(구글 클래스룸·노션)에 올린 자체 디딤 영상 링크로 교체해 쓰세요. 확인 질문은 수업 첫 3분 짝 점검용입니다.</span></div>'''
    p3 = p3.replace(anchor, anchor + block, 1)
    n += 1
wr('part3_lessons.html', p3)
print('stepping blocks:', n)

p1 = rd('part1_head.html')
SCSS = """
  /* ---- 디딤 영상 ---- */
  .stepping {
    background: #F0F6FB; border: 1.5px dashed var(--light-blue); border-radius: 10px;
    padding: 11px 14px; font-size: 13.5px; color: #2b3948; margin: 10px 0; line-height: 1.7;
  }
  .stepping .pk { margin-left: 6px; }
  .stepping .st-note { display: block; font-size: 11.5px; color: var(--sub); margin-top: 4px; }

"""
p1 = p1.replace('  /* ---- 성과 수치 그리드 ---- */', SCSS + '  /* ---- 성과 수치 그리드 ---- */', 1)
wr('part1_head.html', p1)
print('done')
