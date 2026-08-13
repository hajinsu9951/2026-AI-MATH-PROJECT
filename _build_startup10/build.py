# -*- coding: utf-8 -*-
import sys, os, base64, re
sys.stdout.reconfigure(encoding='utf-8')
SP = os.path.dirname(os.path.abspath(__file__))
OUT = r"G:\다른 컴퓨터\학교컴퓨터\2026_AI_MATH\docs\startup10.html"

def rd(p):
    return open(os.path.join(SP, p), encoding='utf-8').read()

p1 = rd("part1_head.html")
p2 = rd("part2_design.html")
p3 = rd("part3_lessons.html")
p3b = rd("part3b_widgets.html")
p3c = rd("part3c_widgets2.html")
p4 = rd("part4_ws_canva_cases.html")
p4b = rd("part4b_cases.html")
p5 = rd("part5_assess_end.html")

MARK = '<!-- ============ 6. 학생 사례 체험 ============ -->'
assert MARK in p4, "cases marker missing in part4"
p4 = p4.split(MARK)[0]

html = "\n".join([p1, p2, p3, p3b, p3c, p4, p4b, p5])

def b64(name, mime):
    data = base64.b64encode(open(os.path.join(SP, name), 'rb').read()).decode()
    return f"data:image/{mime};base64," + data

for ph, f, m in [
    ("{{B64_LEAN}}", "canva_lean.png", "png"),
    ("{{B64_BMC}}", "canva_bmc.png", "png"),
    ("{{B64_ABCDE}}", "canva_abcde.png", "png"),
    ("{{B64_ABCDE2}}", "canva_abcde2.png", "png"),
    ("{{B64_NT1}}", "nt1.jpg", "jpeg"),
    ("{{B64_NT2}}", "nt2.jpg", "jpeg"),
    ("{{B64_NT3}}", "nt3.jpg", "jpeg"),
    ("{{B64_NT4}}", "nt4.jpg", "jpeg"),
    ("{{B64_NT5}}", "nt5.jpg", "jpeg"),
    ("{{B64_NT6}}", "nt6.jpg", "jpeg"),
    ("{{B64_NT7}}", "nt7.jpg", "jpeg"),
    ("{{B64_FIGMA}}", "figma.jpg", "jpeg"),
    ("{{B64_TIKTOK}}", "tiktok.jpg", "jpeg"),
    ("{{B64_CVS1}}", "cvs1.jpg", "jpeg"),
    ("{{B64_CVS2}}", "cvs2.jpg", "jpeg"),
]:
    assert ph in html, f"placeholder missing: {ph}"
    html = html.replace(ph, b64(f, m))

# 활동지 인쇄 버튼 → 활동지 전용 인쇄 함수
n = html.count('onclick="window.print()"')
html = html.replace('onclick="window.print()"', 'onclick="printWS()"')
print("print buttons converted:", n)

# 가독성: 폰트 일괄 확대 (placeholder 2-pass, CSS의 px 값만)
bumps = [
    (r'font-size:\s*10\.5px', 'font-size: 11px'),
    (r'font-size:\s*11px',    'font-size: 12px'),
    (r'font-size:\s*11\.5px', 'font-size: 12.5px'),
    (r'font-size:\s*12px',    'font-size: 13px'),
    (r'font-size:\s*12\.5px', 'font-size: 13.5px'),
    (r'font-size:\s*13px',    'font-size: 14px'),
    (r'font-size:\s*\.82em',  'font-size: .88em'),
    (r'font-size:\s*\.85em',  'font-size: .9em'),
    (r'font-size:\s*\.88em',  'font-size: .93em'),
    (r'font-size:\s*\.9em',   'font-size: .95em'),
    (r'font-size:\s*\.92em',  'font-size: .96em'),
    (r'font-size:\s*\.95em',  'font-size: 1em'),
]
counts = []
for i, (pat, new) in enumerate(bumps):
    html, c = re.subn(pat, f'@@BUMP{i}@@', html)
    counts.append(c)
for i, (pat, new) in enumerate(bumps):
    html = html.replace(f'@@BUMP{i}@@', new)
print("font bumps:", counts)

with open(OUT, 'w', encoding='utf-8') as f:
    f.write(html)
print("written:", OUT, f"({len(html)/1024:.0f} KB)")
