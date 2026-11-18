import json
# 0.2: t09-t12 ekle (idempotent)
R=[
("guided",2,[{"exists":"~/whoami.txt","type":"f"},{"contains":["~/whoami.txt","student"]}],["whoami > ~/whoami.txt"]),
("mini",2,[{"exists":"~/kernel.txt","type":"f"},{"contains":["~/kernel.txt","uname"]}],["echo 'uname -r shows the kernel version' > ~/kernel.txt"]),
("debug",2,{"contains":["~/vm-pitfalls.txt","snapshot"]},["echo 'Mistake: changing the VM without a snapshot first' > ~/vm-pitfalls.txt"]),
("challenge",3,{"contains":["~/net-note.txt","bridged"]},["echo 'NAT: VM behind host; bridged: VM gets own LAN IP' > ~/net-note.txt"]),
]
T={
"tr":[("Adım adım: `whoami > ~/whoami.txt` mantığıyla kullanıcı adını `~/whoami.txt` dosyasına yaz.","`>` çıktıyı dosyaya yazar."),
("Kendi notun: `uname -r` neyi gösterir? Kısa notu (içinde `uname`) `~/kernel.txt` dosyasına yaz.","`echo '...' > ~/kernel.txt`"),
("Sık hata: VM'de değişiklik yapmadan önce ne unutulur? Notu (içinde `snapshot`) `~/vm-pitfalls.txt` dosyasına yaz.","Geri dönüş noktası = anlık görüntü (snapshot)."),
("Meydan okuma: NAT ile bridged ağ farkını bir cümleyle `~/net-note.txt` dosyasına yaz (`bridged` geçsin).","NAT: VM ana makinenin arkasında; bridged: VM LAN'dan kendi IP'sini alır.")],
"de":[("Schritt für Schritt: Schreibe den Benutzernamen nach dem Muster `whoami > ~/whoami.txt` in `~/whoami.txt`.","`>` schreibt die Ausgabe in eine Datei."),
("Eigene Notiz: Was zeigt `uname -r`? Schreibe eine kurze Notiz (mit `uname`) in `~/kernel.txt`.","`echo '...' > ~/kernel.txt`"),
("Häufiger Fehler: Was wird vor Änderungen an der VM vergessen? Schreibe die Notiz (mit `snapshot`) in `~/vm-pitfalls.txt`.","Rückkehrpunkt = Snapshot."),
("Herausforderung: Beschreibe den Unterschied zwischen NAT und Bridged in einem Satz in `~/net-note.txt` (mit `bridged`).","NAT: VM hinter dem Host; Bridged: VM erhält eine eigene IP im LAN.")],
"en":[("Step by step: write your user name into `~/whoami.txt` using `whoami > ~/whoami.txt`.","`>` writes output to a file."),
("Your own note: what does `uname -r` show? Write a short note (including `uname`) into `~/kernel.txt`.","`echo '...' > ~/kernel.txt`"),
("Common mistake: what is forgotten before changing a VM? Write the note (including `snapshot`) into `~/vm-pitfalls.txt`.","A rollback point = snapshot."),
("Challenge: describe the difference between NAT and bridged networking in one sentence in `~/net-note.txt` (include `bridged`).","NAT: VM behind the host; bridged: VM gets its own LAN IP.")],
}
def rw(p,fn):
    s=open(p,encoding='utf-8',newline='').read()
    crlf='\r\n' in s
    d=json.loads(s); fn(d)
    o=json.dumps(d,ensure_ascii=False,indent=1)
    if crlf: o=o.replace('\n','\r\n')
    if s.endswith('\n'): o+='\r\n' if crlf else '\n'
    open(p,'w',encoding='utf-8',newline='').write(o)
def mod(d):
    if any(t['id']=='t09' for t in d['tasks']): return
    for i,(k,df,c,sol) in enumerate(R):
        d['tasks'].append({"id":"t%02d"%(9+i),"kind":k,"diff":df,"check":c,"solution":sol})
rw('content/m0.2/module.json',mod)
for lg in T:
    def f(d):
        if 't09' in d['tasks']: return
        for i,(t,h) in enumerate(T[lg]): d['tasks']["t%02d"%(9+i)]={"text":t,"hint":h}
    rw('content/m0.2/%s.json'%lg,f)
