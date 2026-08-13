# -*- coding: utf-8 -*-
"""startup10.html → startup10_제출용.html (블라인드 처리). build.py 후에 실행."""
import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')
DOCS = r"G:\다른 컴퓨터\학교컴퓨터\2026_AI_MATH\docs"
s = open(os.path.join(DOCS, 'startup10.html'), encoding='utf-8').read()

s = s.replace('<a class="pk" href="https://github.com/hajinsu9951/2026-AI-MATH-PROJECT" target="_blank" rel="noopener">💻 GitHub 저장소(사이트·데이터 소스)</a>', '')
s = re.sub(r'<a class="xp-btn" href="https://github\.com/hajinsu9951/2026-AI-MATH-PROJECT"[^>]*>[^<]*</a>', '', s)
s = s.replace(' 전체 코드·아카이브는 하단 GitHub 버튼에서 볼 수 있습니다.', ' 전체 산출물은 하단 성과 아카이브에서 열람할 수 있습니다.')
s = s.replace('app.notion.com/p/dshskr/', 'app.notion.com/p/')
s = re.sub(r' data-view="[^"]*"', '', s)  # 제출용: 원문 열람 비활성화(원문 내 실명 노출 차단)
s = re.sub(r'<button class="tc-open"[^>]*>[^<]*</button>', '', s)  # 제출용: 열람 비활성이므로 버튼 제거
s = s.replace('아산 티쳐프러너 6기 하진수 외 4명 제작', '아산 티쳐프러너 6기 교사 5인 공동 제작')  # 실명 블라인드
s = re.sub(r'href="https://daeshinmath\.my\.canva\.site/[^"]*"', 'href="#" onclick="return false"', s)  # 학교 식별 서브도메인 차단

out = os.path.join(DOCS, 'startup10_제출용.html')
open(out, 'w', encoding='utf-8').write(s)
print('written:', out, os.path.getsize(out) // 1024, 'KB')
for kw in ['하진수', '대신고', 'hajinsu', 'dshskr', 'GitHub', 'daeshinmath']:
    print(kw, ':', s.count(kw), '건')
