import json, glob, os, re
root = os.path.join(os.path.dirname(__file__), '..', 'content')
def L(p): return json.load(open(p, encoding='utf-8'))
cmdre = re.compile(r'\b(?:[a-z][a-z0-9]{1,}|-[a-zA-Z]+)\b')
out = []
for d in sorted(glob.glob(os.path.join(root, 'm*'))):
    mid = os.path.basename(d)
    m = L(d + '/module.json'); tr = L(d + '/tr.json')
    sols = ' '.join(' '.join(t.get('solution', [])) for t in m.get('tasks', []))
    vmt = L(d + '/tr.json').get('vm', {}).get('tasks', {}); sols += ' ' + ' '.join(b['cmd'] for v in vmt.values() for b in v.get('blocks', []))
    qs = tr.get('quiz', {})
    qtxt = ' '.join(json.dumps(v, ensure_ascii=False) for v in (qs.values() if isinstance(qs, dict) else qs))
    for q in m.get('quiz', []):
        qq = qs.get(q['id']) if isinstance(qs, dict) else None
        if qq and not (0 <= q['answer'] < len(qq['options'])):
            out.append(f'{mid} {q["id"]}: answer disinda')
    for i, o in enumerate(tr.get('objectives', [])):
        toks = set(re.findall(r'`([^`]+)`', o)) or set()
        toks = {t for t in re.findall(r'\b(?:[a-z]{2,}|-[a-zA-Z])\b', ' '.join(toks)) } if toks else set()
        if not toks:
            continue
        hit_t = [t for t in toks if re.search(r'(?<![\w-])' + re.escape(t) + r'(?![\w])', sols)]
        hit_q = [t for t in toks if t in qtxt]
        if not hit_t:
            out.append(f'{mid} hedef{i+1}: gorev cozumunde yok {sorted(toks)}')
        if not hit_q:
            out.append(f'{mid} hedef{i+1}: quizde yok {sorted(toks)}')
print('\n'.join(out)); print('bulgu:', len(out))
