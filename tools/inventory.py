import json,glob,os,re,subprocess,collections
ids=sorted([os.path.basename(os.path.dirname(f))[1:] for f in glob.glob('content/m*/module.json')],key=lambda x:[int(p) for p in x.split('.')])
inv={}
for i in ids:
    L={l:json.load(open(f'content/m{i}/{l}.json',encoding='utf-8')) for l in('tr','de','en')}
    m=json.load(open(f'content/m{i}/module.json',encoding='utf-8'))
    en=L['en']
    cmds=[(c['cmd'],c.get('example',''),bool(c.get('nosim'))) for s in en['sections'] for c in s.get('commands',[])]
    text=json.dumps(en,ensure_ascii=False)
    inv[i]=dict(level=m['level'],title=en['title'],objectives=en['objectives'],cmds=cmds,
      tasks=len(m['tasks']),quiz=len(m['quiz']),sol=[s for t in m['tasks'] for s in t['solution']],
      text=' '.join(re.findall(r'"([^"]{3,})"',text)).lower(),
      paths=sorted(set(re.findall(r'(?<![\w.])/(?:etc|var|usr|proc|sys|dev|boot|bin|sbin|opt|run)[\w./-]*',text))))
json.dump(inv,open('INVENTORY.json','w',encoding='utf-8'),ensure_ascii=False)
print(len(inv),sum(len(v['cmds']) for v in inv.values()),sum(len(v['sol']) for v in inv.values()))
