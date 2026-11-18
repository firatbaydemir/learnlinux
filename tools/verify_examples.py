import json,re,subprocess,shlex,collections
BASH=r"C:\Program Files\Git\usr\bin\bash.exe"
inv=json.load(open('INVENTORY.json',encoding='utf-8'))
syn=[];opt=[];seen=set()
helpcache={}
def help_(c):
    if c not in helpcache:
        try:
            r=subprocess.run([BASH,'-c',f'{c} --help 2>&1 | head -200'],capture_output=True,text=True,timeout=10,encoding='utf-8',errors='replace')
            helpcache[c]=r.stdout if len(r.stdout)>40 else None
        except Exception: helpcache[c]=None
    return helpcache[c]
GNU={'ls','cp','mv','rm','mkdir','rmdir','touch','cat','head','tail','wc','sort','uniq','cut','tr','grep','sed','find','tar','diff','cmp','comm','date','df','du','ln','stat','chmod','chown','chgrp','gzip','xargs','tee','basename','dirname','readlink','realpath','env','printenv','sha256sum','file','id','whoami','uname','sleep','true','false','nproc','truncate','printf','echo'}
for i,v in inv.items():
    for s in v['sol']+[x[1] for x in v['cmds']]:
        if not s or (i,s) in seen: continue
        seen.add((i,s))
        r=subprocess.run([BASH,'-n','-c',s],capture_output=True,text=True,encoding='utf-8',errors='replace')
        if r.returncode: syn.append((i,s,r.stderr.strip()[:80]))
        for seg in re.split(r'\||&&|\|\||;|\n',s):
            w=seg.strip().split()
            while w and (w[0]=='sudo' or '=' in w[0]): w=w[1:]
            if not w or w[0] not in GNU: continue
            h=help_(w[0])
            if not h: continue
            for a in w[1:]:
                if re.match(r'^--[a-z][\w-]+',a):
                    o=a.split('=')[0]
                    if o not in h: opt.append((i,w[0],o))
                elif re.match(r'^-[A-Za-z]+$',a) and w[0] not in('tar','find','echo','printf','sed'):
                    for ch in a[1:]:
                        if not re.search(r'(?<![\w-])-' + ch + r'(?![\w-])', h): opt.append((i, w[0], '-' + ch))

print('syntax',len(syn));[print(' ',*x) for x in syn[:40]]
print('cached',sum(1 for v in helpcache.values() if v),'/',len(helpcache));print('opt',len(opt));[print(' ',*x) for x in sorted(set(opt))[:40]]
