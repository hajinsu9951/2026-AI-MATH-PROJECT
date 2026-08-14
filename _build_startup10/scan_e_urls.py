# -*- coding: utf-8 -*-
"""E:\...\2026_인공지능 수학 전체에서 학생 제출 깃허브·웹 URL 전수 추출 → JSON"""
import os, re, json, zipfile, sys, time
sys.stdout.reconfigure(encoding='utf-8')
ROOT = r'E:\이것저것\학급관련\생활기록부 관련\2026_인공지능 수학'
OUT = r'C:\Users\user\AppData\Local\Temp\ntcap\e_urls.json'

PAT = re.compile(r'https?://(?:www\.)?(?:github\.com|[A-Za-z0-9\-]+\.github\.io|[A-Za-z0-9\-]+\.netlify\.app|[A-Za-z0-9\-]+\.vercel\.app|[A-Za-z0-9\-]+\.streamlit\.app|[A-Za-z0-9\-]+\.my\.canva\.site|[A-Za-z0-9\-]+\.pages\.dev)[^\s"\'<>\)\]\}\ucd9c]*', re.I)

found = {}

def add(url, f):
    url = url.rstrip('.,;\u3002\uff0c')
    found.setdefault(url, set()).add(os.path.relpath(f, ROOT))

def scan_text(t, f):
    for m in PAT.findall(t):
        add(m, f)

def read_zip_xmls(path):
    out = []
    try:
        z = zipfile.ZipFile(path)
        for n in z.namelist():
            if n.endswith(('.xml', '.rels', '.txt', '.html')) or 'sharedStrings' in n:
                try:
                    out.append(z.read(n).decode('utf-8', 'ignore'))
                except Exception:
                    pass
    except Exception:
        pass
    return '\n'.join(out)

t0 = time.time()
n_scanned = 0
pdf_fail = 0
import fitz
for dirpath, _, files in os.walk(ROOT):
    for fn in files:
        f = os.path.join(dirpath, fn)
        ext = fn.lower().rsplit('.', 1)[-1] if '.' in fn else ''
        try:
            if ext in ('txt', 'md', 'csv', 'html', 'htm', 'py', 'json', 'js'):
                scan_text(open(f, encoding='utf-8', errors='ignore').read(), f)
            elif ext in ('docx', 'pptx', 'xlsx'):
                scan_text(read_zip_xmls(f), f)
            elif ext == 'pdf':
                if os.path.getsize(f) > 60 * 1024 * 1024:
                    pdf_fail += 1
                    continue
                try:
                    d = fitz.open(f)
                    txt = ''.join(p.get_text() for p in d[:40])
                    d.close()
                    scan_text(txt, f)
                except Exception:
                    pdf_fail += 1
            elif ext == 'hwp':
                try:
                    import olefile, zlib
                    o = olefile.OleFileIO(f)
                    if o.exists('PrvText'):
                        scan_text(o.openstream('PrvText').read().decode('utf-16-le', 'ignore'), f)
                    o.close()
                except Exception:
                    pass
            else:
                continue
            n_scanned += 1
        except Exception:
            pass

res = {u: sorted(fs) for u, fs in found.items()}
json.dump({'scanned': n_scanned, 'pdf_fail': pdf_fail, 'elapsed_s': round(time.time() - t0),
           'urls': res}, open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('스캔:', n_scanned, '| URL 종수:', len(res), '| pdf 실패:', pdf_fail, '| 소요:', round(time.time() - t0), 's')
for u in sorted(res)[:40]:
    print(' ', u, '<-', res[u][0][:60])
