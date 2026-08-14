# -*- coding: utf-8 -*-
"""step25: 아카이브(index.html) — 학번·실명 마스킹 + 드라이브 다운로드성 링크 가드 주입"""
import re, os, shutil, sys
sys.stdout.reconfigure(encoding='utf-8')
DOCS = r'G:\다른 컴퓨터\학교컴퓨터\2026_AI_MATH\docs'
IDX = os.path.join(DOCS, 'index.html')
GUARD = open(r'C:/Users/user/AppData/Local/Temp/claude/G---------------2026-AI-MATH/8668fdc0-64f1-4643-a441-b82f20b523a7/scratchpad/dlguard.html', encoding='utf-8').read()

s = open(IDX, encoding='utf-8').read()
bak = IDX + '.bak-step25'
if not os.path.exists(bak):
    shutil.copyfile(IDX, bak)

# 1) members 마스킹: ["31002","구승훈"] → ["3····","구○○"]
def mask(m):
    sid, name = m.group(1), m.group(2)
    return '["%s····","%s○○"]' % (sid[0], name[0])
s, n = re.subn(r'\["(\d{4,6})","([가-힣]{2,4})"\]', mask, s)
print('학번·실명 마스킹:', n)

# 잔여 실명 노출 패턴(리더명 등 문자열 필드) 점검용 카운트만 출력
# 2) 가드 주입
if 'dl-guard-v1' not in s:
    assert '</body>' in s
    s = s.replace('</body>', GUARD + '\n</body>', 1)
    print('가드 주입 ok')

open(IDX, 'w', encoding='utf-8').write(s)
print('index.html 갱신 완료, 백업:', os.path.basename(bak))
