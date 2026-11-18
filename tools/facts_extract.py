import json,re,collections
inv=json.load(open('INVENTORY.json',encoding='utf-8'))
P={'sinyal':r'SIG[A-Z]+\s*\(?\s*-?\d+\)?|kill -\d+|signal \d+','port':r'(?:port|Port)\s+\d{1,5}(?:/\w+)?|\b\d{2,5}/(?:tcp|udp)\b','nice':r'-?\d+\s*(?:to|bis|ile|\.\.)\s*-?\d+','oktal':r'\bchmod\s+[0-7]{3,4}\b[^`"]{0,25}|umask\s+[0-7]{3,4}','yol':r'/(?:etc|var|proc|sys|usr|boot|dev|run)/[\w./*-]+','sayi_iddia':r'(?:default|varsayılan|standard|Standard)[^.]{0,40}\d+[^.]{0,30}'}
t=json.load(open('INVENTORY.json',encoding='utf-8'))
res={k:collections.defaultdict(set) for k in P}
for i in inv:
    en=json.load(open(f'content/m{i}/en.json',encoding='utf-8'))
    s=json.dumps(en,ensure_ascii=False)
    for k,p in P.items():
        for m in re.findall(p,s): res[k][m.strip()].add(i)
for k in res:
    print('##',k,len(res[k]))
    if k=='yol': continue
    for m,ms in sorted(res[k].items()): print(' ',m,'|',','.join(sorted(ms)))
json.dump({k:{m:sorted(v) for m,v in d.items()} for k,d in res.items()},open('facts_raw.json','w',encoding='utf-8'),ensure_ascii=False)
