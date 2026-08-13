# -*- coding: utf-8 -*-
import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')
BS = '\\'
html = open(r'G:\다른 컴퓨터\학교컴퓨터\2026_AI_MATH\docs\index.html', encoding='utf-8').read()
i = html.find('TEAMS'); i = html.find('[', i)
depth = 0; end = None; ins = False; esc = False
for j in range(i, len(html)):
    c = html[j]
    if ins:
        if esc: esc = False
        elif c == BS: esc = True
        elif c == '"': ins = False
    else:
        if c == '"': ins = True
        elif c == '[': depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                end = j + 1
                break
teams = json.loads(html[i:end])
pat = re.compile(r'https?://[^\s"\')\]]+')
DOM = ('github', 'netlify', 'vercel', 'streamlit', 'youtu', 'replit', 'glitch', 'web.app', 'firebase', 'huggingface', 'colab', 'tistory')
rows = []
for t in teams:
    blob = json.dumps(t, ensure_ascii=False)
    for m in pat.finditer(blob):
        u = m.group(0)
        if any(d in u for d in DOM):
            rows.append({'tier': t.get('tier', ''), 'title': t.get('title', '')[:50], 'url': u[:150]})
print('team-linked dynamic urls:', len(rows))
for r in rows[:25]:
    print(r['tier'], '|', r['title'], '|', r['url'])
allm = sorted(set(u for u in pat.findall(html) if any(d in u for d in DOM)))
print('--- whole-file distinct (top 25) ---')
for u in allm[:25]:
    print(u[:150])
json.dump(rows, open(r'G:\다른 컴퓨터\학교컴퓨터\2026_AI_MATH\_build_startup10\dynamic_links.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
