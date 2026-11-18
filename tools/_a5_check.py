import json, glob, os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
L = ['tr', 'de', 'en']
BT = re.compile(r'`([^`]+)`')
NUM = re.compile(r'\d+')
out = []; cnt = {}

def add(m, kind, msg):
    cnt[kind] = cnt.get(kind, 0) + 1
    out.append(f'- **{m}** [{kind}] {msg}')

def cmds(s):
    return sorted(set(x.strip() for x in BT.findall(s)))

def words(items):
    w = set()
    for s in items:
        for c in BT.findall(s):
            t = c.split()
            if t: w.add(t[0])
    return w

for d in sorted(glob.glob('content/m*'), key=lambda p: [float(x) if x.replace('.', '').isdigit() else 0 for x in re.findall(r'\d+\.?\d*', p)]):
    m = os.path.basename(d)[1:]
    try:
        mod = json.load(open(f'{d}/module.json', encoding='utf-8'))
        c = {l: json.load(open(f'{d}/{l}.json', encoding='utf-8')) for l in L}
    except Exception as e:
        add(m, 'load', str(e)); continue
    tr = c['tr']
    mt = [t['id'] for t in mod.get('tasks', [])]
    # 1) yapı farkları
    for l in L[1:]:
        o = c[l]
        for k in ('objectives', 'sections', 'summary', 'glossary'):
            if len(o.get(k, [])) != len(tr.get(k, [])):
                add(m, 'yapı', f'{l}.{k} sayı {len(o.get(k,[]))} != tr {len(tr.get(k,[]))}')
        if sorted(o['tasks']) != sorted(tr['tasks']):
            add(m, 'yapı', f'{l}.tasks anahtarları farklı')
        if len(o['quiz']) != len(tr['quiz']):
            add(m, 'yapı', f'{l}.quiz sayı farklı')
        for i, (a, b) in enumerate(zip(tr['sections'], o['sections'])):
            ca, cb = [x if isinstance(x, str) else json.dumps(x) for x in a.get('commands', [])], [x if isinstance(x, str) else json.dumps(x) for x in b.get('commands', [])]
            if len(ca) != len(cb):
                add(m, 'yapı', f'{l}.sections[{i}].commands sayı {len(cb)} != {len(ca)}')
        # komut (backtick) farkı görevlerde
        for t in tr['tasks']:
            if t in o['tasks']:
                a = cmds(tr['tasks'][t]['text']); b = cmds(o['tasks'][t]['text'])
                if a != b:
                    add(m, 'komut', f'{l}.{t} backtick farkı tr={a} {l}={b}')
                na = NUM.findall(tr['tasks'][t]['text']); nb = NUM.findall(o['tasks'][t]['text'])
                if sorted(na) != sorted(nb):
                    add(m, 'sayı', f'{l}.{t} rakam farkı tr={na} {l}={nb}')
    # 2) module.json <-> tr görevleri
    ks = [k for k in tr['tasks']]
    if sorted(mt) != sorted(ks):
        add(m, 'eşleşme', f'module.json görev id != tr.tasks: yalnız json={sorted(set(mt)-set(ks))} yalnız tr={sorted(set(ks)-set(mt))}')
    # 3) hedef -> görev/bölüm komutları
    obj = tr.get('objectives', [])
    objs = [o if isinstance(o, str) else json.dumps(o, ensure_ascii=False) for o in obj]
    sol = set()
    for t in mod.get('tasks', []):
        for s in t.get('solution', []) or []:
            if isinstance(s, str) and s.split(): sol.add(s.split()[0])
    tw = words([tr['tasks'][t]['text'] for t in tr['tasks']]) | sol
    for i, o in enumerate(objs):
        ow = words([o])
        if ow and not (ow & tw):
            add(m, 'hedef', f'hedef[{i}] komutları {sorted(ow)} hiçbir görevde yok')
    # 4) quiz -> öğretilen komut
    secw = words([x if isinstance(x, str) else json.dumps(x) for s in tr['sections'] for x in s.get('commands', [])])
    allw = tw | secw | words(objs)
    for q, qq in tr['quiz'].items():
        qw = words([qq['q']] + list(qq['options']) + [qq['explain']])
        miss = qw - allw
        if miss:
            add(m, 'quiz', f'{q} komut(lar) {sorted(miss)} ne görevde ne bölümde')
    # 5) görev sayısı / tür dengesi
    kinds = {}
    for t in mod.get('tasks', []): kinds[t.get('kind')] = kinds.get(t.get('kind'), 0) + 1
    if len(mt) < 10:
        add(m, 'kapsam', f'{len(mt)} görev')

with open('CONSISTENCY.md', 'w', encoding='utf-8', newline='\r\n') as f:
    f.write('# CONSISTENCY\n\nÖzet: ' + ', '.join(f'{k}={v}' for k, v in sorted(cnt.items())) + '\n\n')
    f.write('\n'.join(out) + '\n')
print(cnt)
