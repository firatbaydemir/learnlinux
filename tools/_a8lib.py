import json, re



def rw(p, fn):
    s = open(p, encoding='utf-8', newline='').read()
    crlf = '\r\n' in s
    d = json.loads(s); fn(d)
    o = json.dumps(d, ensure_ascii=False, indent=1)
    if crlf: o = o.replace('\n', '\r\n')
    if s.endswith('\n'): o += '\r\n' if crlf else '\n'
    open(p, 'w', encoding='utf-8', newline='').write(o)

def add_quiz(mid, items, start=5):
    """items: list of (answer_index, {'tr':(q,[opts],explain),'de':..,'en':..}); idempotent."""
    base = 'content/m%s/' % mid
    p = base + 'module.json'
    s = open(p, encoding='utf-8', newline='').read()
    nl = '\r\n' if '\r\n' in s else '\n'
    if re.search(r'"id":\s*"q%d"' % start, s):
        return
    ms = list(re.finditer(r'(\{"id": "q\d+", "answer": \d+\})(\r?\n)( *\])', s))
    if ms:
        m = ms[-1]
        new = m.group(1)
        for i, (a, _) in enumerate(items):
            new += ',' + nl + '  {"id": "q%d", "answer": %d}' % (start + i, a)
        s = s[:m.start()] + new + m.group(2) + m.group(3) + s[m.end():]
        open(p, 'w', encoding='utf-8', newline='').write(s)
    else:
        def g(d):
            for i, (a, _) in enumerate(items):
                d['quiz'].append({"id": "q%d" % (start + i), "answer": a})
        rw(p, g)
    for lg in ('tr', 'de', 'en'):
        def f(d):
            for i, (a, t) in enumerate(items):
                q, o, e = t[lg]
                assert len(o) == 4
                d['quiz']['q%d' % (start + i)] = {"q": q, "options": o, "explain": e}
        rw(base + lg + '.json', f)
