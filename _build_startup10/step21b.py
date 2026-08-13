# -*- coding: utf-8 -*-
"""step21b: 칩 미삽입 카드 20장에 역량·수학 칩 보정 삽입"""
import sys, re, os
sys.stdout.reconfigure(encoding='utf-8')
SP = os.path.dirname(os.path.abspath(__file__))
_src = open(os.path.join(SP, 'step21.py'), encoding='utf-8').read()
_ns = {'__file__': os.path.join(SP, 'step21.py')}
exec(_src.split('# ---------- part1')[0], _ns)  # CARDS 정의부만 실행
CARDS = _ns['CARDS']

p = open(os.path.join(SP, 'part4b_cases.html'), encoding='utf-8').read()

def tx(m):
    block = m.group(0)
    if 'tag cap' in block:
        return block
    vm = re.search(r'data-view="([^"]*)"', block)
    v = vm.group(1) if vm else ''
    card = next((c for c in CARDS if c[0] in v), None)
    if not card:
        raise AssertionError('no map: ' + v[:60])
    _, fid, cap, mathp = card
    chips = '<span class="tag cap">🧭 %s</span><span class="tag mathp">∑ %s</span>' % (cap, mathp)
    block2, n = re.subn(r'(<span class="tag (?:grand|top|good)">[^<]*</span>)', r'\1' + chips, block, count=1)
    assert n == 1, 'tier span not found'
    return block2

p, n = re.subn(r'<a class="thumb-card" href="#"[\s\S]*?</a>', tx, p)
print('검사한 카드:', n)
assert p.count('tag cap') == 21, p.count('tag cap')
open(os.path.join(SP, 'part4b_cases.html'), 'w', encoding='utf-8').write(p)
print('칩 21개 확인 완료')
