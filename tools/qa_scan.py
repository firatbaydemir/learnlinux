#!/usr/bin/env python3
"""Kalite taramasi: dil karisimi, mojibake, yer tutucu, kopya/cevrilmemis metin,
bicim, uzunluk orani, HTML erisilebilirlik, PWA onbellek tutarliligi.
Kullanim: python tools/qa_scan.py [--verbose]. Cikis kodu: ERROR varsa 1."""
import json, re, sys, glob, os, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VERBOSE = '--verbose' in sys.argv
res = collections.defaultdict(list)  # (seviye, kontrol) -> [mesaj]


def add(level, check, msg):
    res[(level, check)].append(msg)


def walk(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, f'{path}/{k}')
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, f'{path}[{i}]')
    elif isinstance(o, str):
        yield path, o


TR_CH = set('çğışöüÇĞİŞÖÜ')
DE_CH = set('äöüßÄÖÜ')
TR_W = set('ve bir bu için ile olarak değil gibi ama çok daha veya komut dosya kullanıcı yazın görev'.split())
DE_W = set('und der die das ist nicht ein eine mit für auf wie wenn oder wird den dem Datei Befehl'.split())
EN_W = set('the and is of to for with not this that you are use file command when your'.split())
MOJI = re.compile('Ã[¤¶¼Ÿ‡±]|Ä[±Ÿ°]|Å[ŸžÂ]|â€|ï¿½|\ufffd|Ã‡|Ã–|Ãœ')
PLACE = re.compile(r'\b(FIXME|XXX|lorem ipsum|TBD)\b')
SKIP = ('/commands', '/output', '/solution', '/cmd', '/expected', '/blocks', '/differs', '/setup')


def skip(p):
    return any(x in p for x in SKIP)


def lang_score(s):
    w = re.findall(r"[A-Za-zÇĞİŞÖÜçğışöüäßÄ]+", s)
    lw = [x.lower() for x in w]
    return (sum(x in TR_W for x in lw), sum(x in DE_W or x in {y.lower() for y in DE_W} for x in lw),
            sum(x in EN_W for x in lw), len(w))


def guess(s):
    s = re.sub(r'`[^`]*`|\'[^\']*\'|"[^"]*"', ' ', s)
    t, d, e, n = lang_score(s)
    if n < 6:
        return None
    # Turkce ozel harfler guclu isaret
    tr_c = sum(c in 'çğışÇĞİŞ' for c in s)
    sc = {'tr': t + tr_c * 0.5, 'de': d, 'en': e}
    best = max(sc, key=sc.get)
    if sc[best] < 2 or sorted(sc.values())[-2] * 2 > sc[best]:
        return None
    return best


# ---- 1) icerik JSON'lari
mods = sorted(glob.glob(os.path.join(ROOT, 'content', 'm*')))
for md in mods:
    mid = os.path.basename(md)
    data = {}
    for lg in ('tr', 'de', 'en'):
        fp = os.path.join(md, lg + '.json')
        raw = open(fp, 'rb').read()
        if raw.startswith(b'\xef\xbb\xbf'):
            add('ERROR', 'BOM', f'{mid}/{lg}.json')
        if b'\r\n' not in raw:
            add('WARN', 'CRLF-yok', f'{mid}/{lg}.json')
        try:
            data[lg] = json.loads(raw.decode('utf-8'))
        except Exception as ex:
            add('ERROR', 'JSON', f'{mid}/{lg}: {ex}')
            continue
        strs = dict(walk(data[lg]))
        for p, s in strs.items():
            if MOJI.search(s):
                add('ERROR', 'mojibake', f'{mid}/{lg}{p}: {s[:50]!r}')
            if PLACE.search(s):
                add('ERROR', 'yer-tutucu', f'{mid}/{lg}{p}: {s[:50]!r}')
            if not s.strip():
                add('WARN', 'bos-metin', f'{mid}/{lg}{p}')
            if s != s.strip() and len(s) > 0 and '\n' not in s:
                add('WARN', 'bosluk-kenar', f'{mid}/{lg}{p}')
            if '  ' in s and '\n' not in s and '<pre' not in s:
                add('WARN', 'cift-bosluk', f'{mid}/{lg}{p}: {s[:40]!r}')
            if s.count('`') % 2 and not skip(p):
                add('ERROR', 'backtick-dengesiz', f'{mid}/{lg}{p}: {s[:50]!r}')
            if re.search(r'<(?!/?(code|b|strong|em|br|kbd|i|a|span|pre)\b)[a-z]+[^>]*>', s) and not skip(p) and '`' not in s:
                add('WARN', 'html-beklenmeyen-etiket', f'{mid}/{lg}{p}: {s[:50]!r}')
            # dil karisimi (komut/kod alanlarini atla)
            if skip(p):
                continue
            g = guess(s)
            if g and g != lg and not (lg == 'tr' and g == 'en' and 'command not found' in s):
               
                add('ERROR', 'yanlis-dil', f'{mid}/{lg}{p}: {g} gibi: {s[:60]!r}')
            if lg != 'tr' and re.search('[çğışÇĞİŞ]', s) and len(s) > 20 and '|' not in s:
                add('ERROR', 'tr-karakter', f'{mid}/{lg}{p}: {s[:60]!r}')
    # tr ile ayni (cevrilmemis) ve uzunluk orani
    if 'tr' in data:
        trs = dict(walk(data['tr']))
        for lg in ('de', 'en'):
            if lg not in data:
                continue
            os_ = dict(walk(data[lg]))
            same = 0
            for p, s in trs.items():
                o = os_.get(p)
                if o is None:
                    add('ERROR', 'eksik-anahtar', f'{mid}/{lg}{p}')
                    continue
                if skip(p):
                    continue
                if len(s) > 40 and s == o and not re.search(r'[A-Za-z]{4,}', re.sub(r'`[^`]*`', '', s)):
                    same += 1
                    add('ERROR', 'cevrilmemis', f'{mid}/{lg}{p}: {s[:50]!r}')
                if len(s) > 80:
                    r = len(o) / len(s)
                    if r < 0.5 or r > 2.2:
                        add('WARN', 'uzunluk-orani', f'{mid}/{lg}{p}: {r:.2f}')
            for p in os_:
                if p not in trs:
                    add('ERROR', 'fazla-anahtar', f'{mid}/{lg}{p}')

# ---- 2) uretilen HTML
for lg in ('tr', 'de', 'en'):
    for fp in glob.glob(os.path.join(ROOT, lg, '*.html')):
        h = open(fp, encoding='utf-8').read()
        h = re.sub(r'<script\b.*?</script>', '', h, flags=re.S)
        n = os.path.relpath(fp, ROOT)
        if not re.search(r'<html[^>]+lang="%s' % lg, h):
            add('ERROR', 'html-lang', n)
        if not re.search(r'<title>[^<]+</title>', h):
            add('ERROR', 'html-title', n)
        if 'name="viewport"' not in h:
            add('ERROR', 'html-viewport', n)
        for m in re.finditer(r'<img\b(?![^>]*\balt=)[^>]*>', h):
            add('ERROR', 'img-alt-yok', n)
        ids = re.findall(r'\bid="([^"]+)"', h)
        for i, c in collections.Counter(ids).items():
            if c > 1:
                add('ERROR', 'yinelenen-id', f'{n}: {i}')
        if MOJI.search(h):
            add('ERROR', 'mojibake-html', n)
        for m in re.finditer(r'<(?:a|link|script)\b[^>]*(?:href|src)="([^"#?]+)', h):
            u = m.group(1)
            if re.match(r'(https?:|mailto:|data:|javascript:)', u):
                if u.startswith('http'):
                    add('WARN', 'dis-baglanti', f'{n}: {u}')
                continue
            t = os.path.normpath(os.path.join(os.path.dirname(fp), u))
            if not os.path.exists(t):
                add('ERROR', 'kirik-baglanti', f'{n}: {u}')
        for hn in range(1, 6):
            pass
        hs = [int(x) for x in re.findall(r'<h([1-6])\b', h)]
        for a, b in zip(hs, hs[1:]):
            if b - a > 1:
                add('WARN', 'baslik-atlama', n)
                break
        if hs.count(1) != 1:
            add('WARN', 'h1-sayisi', f'{n}: {hs.count(1)}')

# ---- 3) PWA onbellek manifesti
pm = os.path.join(ROOT, 'precache-manifest.js')
if os.path.exists(pm):
    txt = open(pm, encoding='utf-8').read()
    files = re.findall(r'"([^"]+\.[a-z0-9]+)"', txt)
    for f in files:
        if f.startswith('http'):
            continue
        p = os.path.join(ROOT, f.lstrip('./'))
        if not os.path.exists(p):
            add('ERROR', 'precache-eksik-dosya', f)
    pages = {os.path.relpath(p, ROOT).replace('\\', '/') for lg in ('tr', 'de', 'en')
             for p in glob.glob(os.path.join(ROOT, lg, '*.html'))}
    listed = {f.lstrip('./') for f in files}
    for pg in sorted(pages - listed):
        add('ERROR', 'precache-sayfa-yok', pg)
else:
    add('ERROR', 'precache', 'precache-manifest.js yok')
for need in ('manifest.webmanifest', 'service-worker.js'):
    if not glob.glob(os.path.join(ROOT, need)) and not glob.glob(os.path.join(ROOT, '**', need), recursive=True):
        add('WARN', 'pwa-dosya', need + ' bulunamadi')

# ---- rapor
err = sum(len(v) for (l, _), v in res.items() if l == 'ERROR')
warn = sum(len(v) for (l, _), v in res.items() if l == 'WARN')
for (lvl, chk), v in sorted(res.items()):
    print(f'{lvl:5} {chk}: {len(v)}')
    for m in v[: (len(v) if VERBOSE else 3)]:
        print('      ', m)
print(f'TOPLAM: {err} ERROR, {warn} WARN, {len(mods)} modul')
sys.exit(1 if err else 0)
