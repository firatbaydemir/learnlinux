import json,re
# (kind,diff,check,solution) per module; texts per lang
def g(pat,f): return "^grep %s \\S*%s$" % (pat,f)
M={
"5.3":[
 ("predict",2,{"out":"3305","of":g("java","ps_snapshot\\.txt")},"grep java ~/lab/ps_snapshot.txt"),
 ("predict",2,{"out":"1","of":"^grep -c alice \\S*ps_snapshot\\.txt$"},"grep -c alice ~/lab/ps_snapshot.txt"),
 ("guided",2,{"out":"1203","of":g("bash","ps_snapshot\\.txt")},"grep bash ~/lab/ps_snapshot.txt"),
 ("debug",2,{"contains":["~/lab/pkill_check.txt","pgrep -a"]},"echo 'pgrep -a -x worker before pkill -TERM -x worker' > ~/lab/pkill_check.txt"),
 ("mini",2,{"contains":["~/lab/renice_plan.txt","renice"]},"echo 'renice 10 -p 2210' > ~/lab/renice_plan.txt"),
 ("ticket",3,{"contains":["~/lab/pitfalls_5301.txt","pkill -f"]},"echo 'Mistake: pkill -f with a short pattern can match unrelated processes' > ~/lab/pitfalls_5301.txt"),
],
"5.4":[
 ("predict",2,{"out":"report","of":g("Done","jobs_snapshot\\.txt")},"grep Done ~/lab/jobs_snapshot.txt"),
 ("predict",2,{"out":"1","of":"^grep -c Running \\S*jobs_snapshot\\.txt$"},"grep -c Running ~/lab/jobs_snapshot.txt"),
 ("guided",2,{"out":"Done","of":g("report","jobs_snapshot\\.txt")},"grep report ~/lab/jobs_snapshot.txt"),
 ("debug",2,{"contains":["~/lab/disown_note.txt","disown"]},"echo 'disown -h %2 detaches a job from SIGHUP' > ~/lab/disown_note.txt"),
 ("mini",2,[{"contains":["~/lab/stop_plan.txt","Ctrl+Z"]},{"contains":["~/lab/stop_plan.txt","bg"]}],"echo 'Ctrl+Z stops the job; bg %1 resumes it in the background' > ~/lab/stop_plan.txt"),
 ("ticket",3,{"contains":["~/lab/pitfalls_5401.txt","kill %2"]},"echo 'Mistake: plain job number 2 is not %2; use kill %2 for job 2' > ~/lab/pitfalls_5401.txt"),
],
"5.5":[
 ("predict",2,{"out":"apache2","of":g("Debian","package_notes\\.txt")},"grep Debian ~/lab/package_notes.txt"),
 ("predict",2,{"out":"2","of":"^grep -c RHEL \\S*package_notes\\.txt$"},"grep -c RHEL ~/lab/package_notes.txt"),
 ("guided",2,{"out":"Ubuntu","of":g("dpkg","package_notes\\.txt")},"grep dpkg ~/lab/package_notes.txt"),
 ("debug",2,{"contains":["~/lab/search_plan.txt","apt search"]},"echo 'apt search nginx; dnf search nginx' > ~/lab/search_plan.txt"),
 ("mini",2,{"contains":["~/lab/query_plan.txt","rpm -qa"]},"echo 'rpm -qa on RHEL family; dpkg -l on Debian family' > ~/lab/query_plan.txt"),
 ("ticket",3,{"contains":["~/lab/pitfalls_5501.txt","-y"]},"echo 'Mistake: -y skips the confirmation; read the package list first' > ~/lab/pitfalls_5501.txt"),
],
}
T={
"5.3":{
"tr":[("`~/lab/ps_snapshot.txt` içinde `java` satırını bul; PID kaçtır?","`grep java ~/lab/ps_snapshot.txt` dene. (`grep` → modül 3.4.)"),
("Tahmin et: dosyada `alice` kaç satırda geçiyor? Sonra `grep -c` ile doğrula.","`grep -c alice ~/lab/ps_snapshot.txt` dene. (`grep` → modül 3.4.)"),
("`bash` sürecinin PID'sini bul.","`grep bash ~/lab/ps_snapshot.txt`; ikinci alan PID'dir. (`grep` → modül 3.4.)"),
("Hata önleme: `pkill` öncesi `pgrep -a` ile eşleşmeyi doğrulama adımını `~/lab/pkill_check.txt` içine yaz.","`echo '...' > ~/lab/pkill_check.txt`; metinde `pgrep -a` olsun. (`>` → modül 3.2.)"),
("PID 2210 için nice değerini 10 yapan `renice` komutunu `~/lab/renice_plan.txt` içine yaz.","Biçim: `renice 10 -p PID`. (`>` → modül 3.2.)"),
("Sık hata: `pkill -f` neden riskli? Ticket #5301 için kısa notu `~/lab/pitfalls_5301.txt` içine yaz.","Notta `pkill -f` ifadesi geçsin. (`>` → modül 3.2.)")],
"de":[("Suche in `~/lab/ps_snapshot.txt` die Zeile mit `java`; wie lautet die PID?","Probiere `grep java ~/lab/ps_snapshot.txt`. (`grep` → Modul 3.4.)"),
("Schätze: In wie vielen Zeilen kommt `alice` vor? Prüfe dann mit `grep -c`.","Probiere `grep -c alice ~/lab/ps_snapshot.txt`. (`grep` → Modul 3.4.)"),
("Finde die PID des `bash`-Prozesses.","`grep bash ~/lab/ps_snapshot.txt`; das zweite Feld ist die PID. (`grep` → Modul 3.4.)"),
("Fehlervermeidung: Schreibe den Schritt, vor `pkill` mit `pgrep -a` die Treffer zu prüfen, in `~/lab/pkill_check.txt`.","`echo '...' > ~/lab/pkill_check.txt`; der Text enthält `pgrep -a`. (`>` → Modul 3.2.)"),
("Schreibe den `renice`-Befehl, der den Nice-Wert von PID 2210 auf 10 setzt, in `~/lab/renice_plan.txt`.","Format: `renice 10 -p PID`. (`>` → Modul 3.2.)"),
("Häufiger Fehler: Warum ist `pkill -f` riskant? Schreibe für Ticket #5301 eine kurze Notiz in `~/lab/pitfalls_5301.txt`.","Die Notiz enthält `pkill -f`. (`>` → Modul 3.2.)")],
"en":[("Find the `java` line in `~/lab/ps_snapshot.txt`; what is its PID?","Try `grep java ~/lab/ps_snapshot.txt`. (`grep` → module 3.4.)"),
("Predict: on how many lines does `alice` appear? Then verify with `grep -c`.","Try `grep -c alice ~/lab/ps_snapshot.txt`. (`grep` → module 3.4.)"),
("Find the PID of the `bash` process.","`grep bash ~/lab/ps_snapshot.txt`; the second field is the PID. (`grep` → module 3.4.)"),
("Error prevention: write the step of checking matches with `pgrep -a` before `pkill` into `~/lab/pkill_check.txt`.","`echo '...' > ~/lab/pkill_check.txt`; include `pgrep -a` in the text. (`>` → module 3.2.)"),
("Write the `renice` command that sets PID 2210 to nice value 10 into `~/lab/renice_plan.txt`.","Format: `renice 10 -p PID`. (`>` → module 3.2.)"),
("Common mistake: why is `pkill -f` risky? Write a short note for ticket #5301 into `~/lab/pitfalls_5301.txt`.","Mention `pkill -f` in the note. (`>` → module 3.2.)")]},
"5.4":{
"tr":[("`~/lab/jobs_snapshot.txt` içinde `Done` olan işi bul; komutu nedir?","`grep Done ~/lab/jobs_snapshot.txt` dene. (`grep` → modül 3.4.)"),
("Tahmin et: kaç iş `Running`? Sonra `grep -c` ile doğrula.","`grep -c Running ~/lab/jobs_snapshot.txt` dene. (`grep` → modül 3.4.)"),
("`report` komutunun durumunu bul.","`grep report ~/lab/jobs_snapshot.txt` dene. (`grep` → modül 3.4.)"),
("Oturum kapanınca işin SIGHUP almaması için `disown` notunu `~/lab/disown_note.txt` içine yaz.","Notta `disown` geçsin. (`>` → modül 3.2.)"),
("`Ctrl+Z` ile durdurup `bg` ile arka planda sürdürme adımlarını `~/lab/stop_plan.txt` içine yaz.","Notta `Ctrl+Z` ve `bg` geçsin. (`>` → modül 3.2.)"),
("Sık hata: iş numarası `%` olmadan verilirse PID sanılır. Ticket #5401 için notu `~/lab/pitfalls_5401.txt` içine yaz.","Notta `kill %2` geçsin. (`>` → modül 3.2.)")],
"de":[("Finde in `~/lab/jobs_snapshot.txt` den Job mit `Done`; wie lautet der Befehl?","Probiere `grep Done ~/lab/jobs_snapshot.txt`. (`grep` → Modul 3.4.)"),
("Schätze: Wie viele Jobs sind `Running`? Prüfe dann mit `grep -c`.","Probiere `grep -c Running ~/lab/jobs_snapshot.txt`. (`grep` → Modul 3.4.)"),
("Finde den Status des Befehls `report`.","Probiere `grep report ~/lab/jobs_snapshot.txt`. (`grep` → Modul 3.4.)"),
("Schreibe eine `disown`-Notiz, damit der Job beim Beenden der Sitzung kein SIGHUP erhält, in `~/lab/disown_note.txt`.","Die Notiz enthält `disown`. (`>` → Modul 3.2.)"),
("Schreibe die Schritte „mit `Ctrl+Z` stoppen, mit `bg` im Hintergrund fortsetzen“ in `~/lab/stop_plan.txt`.","Die Notiz enthält `Ctrl+Z` und `bg`. (`>` → Modul 3.2.)"),
("Häufiger Fehler: Eine Jobnummer ohne `%` wird als PID verstanden. Schreibe für Ticket #5401 eine Notiz in `~/lab/pitfalls_5401.txt`.","Die Notiz enthält `kill %2`. (`>` → Modul 3.2.)")],
"en":[("Find the `Done` job in `~/lab/jobs_snapshot.txt`; what is its command?","Try `grep Done ~/lab/jobs_snapshot.txt`. (`grep` → module 3.4.)"),
("Predict: how many jobs are `Running`? Then verify with `grep -c`.","Try `grep -c Running ~/lab/jobs_snapshot.txt`. (`grep` → module 3.4.)"),
("Find the state of the `report` command.","Try `grep report ~/lab/jobs_snapshot.txt`. (`grep` → module 3.4.)"),
("Write a `disown` note so the job does not receive SIGHUP when the session ends into `~/lab/disown_note.txt`.","Include `disown` in the note. (`>` → module 3.2.)"),
("Write the steps \"stop with `Ctrl+Z`, resume in the background with `bg`\" into `~/lab/stop_plan.txt`.","Include `Ctrl+Z` and `bg`. (`>` → module 3.2.)"),
("Common mistake: a job number without `%` is read as a PID. Write a note for ticket #5401 into `~/lab/pitfalls_5401.txt`.","Include `kill %2` in the note. (`>` → module 3.2.)")]},
"5.5":{
"tr":[("`~/lab/package_notes.txt` içinde `Debian` satırını bul; web paketinin adı nedir?","`grep Debian ~/lab/package_notes.txt` dene. (`grep` → modül 3.4.)"),
("Tahmin et: dosyada `RHEL` kaç satırda geçiyor? Sonra `grep -c` ile doğrula.","`grep -c RHEL ~/lab/package_notes.txt` dene. (`grep` → modül 3.4.)"),
("`dpkg` hangi dağıtım ailesine ait? Satırı bul.","`grep dpkg ~/lab/package_notes.txt` dene. (`grep` → modül 3.4.)"),
("Paket aramak için `apt search` ve `dnf search` örneğini `~/lab/search_plan.txt` içine yaz.","Notta `apt search` geçsin. (`>` → modül 3.2.)"),
("Kurulu paketleri listeleme komutlarını (`rpm -qa`, `dpkg -l`) `~/lab/query_plan.txt` içine yaz.","Notta `rpm -qa` geçsin. (`>` → modül 3.2.)"),
("Sık hata: `-y` neden dikkatli kullanılmalı? Ticket #5501 için notu `~/lab/pitfalls_5501.txt` içine yaz.","Notta `-y` geçsin. (`>` → modül 3.2.)")],
"de":[("Finde in `~/lab/package_notes.txt` die Zeile `Debian`; wie heißt das Webpaket?","Probiere `grep Debian ~/lab/package_notes.txt`. (`grep` → Modul 3.4.)"),
("Schätze: In wie vielen Zeilen steht `RHEL`? Prüfe dann mit `grep -c`.","Probiere `grep -c RHEL ~/lab/package_notes.txt`. (`grep` → Modul 3.4.)"),
("Zu welcher Distributionsfamilie gehört `dpkg`? Finde die Zeile.","Probiere `grep dpkg ~/lab/package_notes.txt`. (`grep` → Modul 3.4.)"),
("Schreibe ein Beispiel mit `apt search` und `dnf search` in `~/lab/search_plan.txt`.","Die Notiz enthält `apt search`. (`>` → Modul 3.2.)"),
("Schreibe die Befehle zum Auflisten installierter Pakete (`rpm -qa`, `dpkg -l`) in `~/lab/query_plan.txt`.","Die Notiz enthält `rpm -qa`. (`>` → Modul 3.2.)"),
("Häufiger Fehler: Warum sollte `-y` mit Vorsicht benutzt werden? Schreibe für Ticket #5501 eine Notiz in `~/lab/pitfalls_5501.txt`.","Die Notiz enthält `-y`. (`>` → Modul 3.2.)")],
"en":[("Find the `Debian` line in `~/lab/package_notes.txt`; what is the web package called?","Try `grep Debian ~/lab/package_notes.txt`. (`grep` → module 3.4.)"),
("Predict: on how many lines does `RHEL` appear? Then verify with `grep -c`.","Try `grep -c RHEL ~/lab/package_notes.txt`. (`grep` → module 3.4.)"),
("Which distribution family uses `dpkg`? Find the line.","Try `grep dpkg ~/lab/package_notes.txt`. (`grep` → module 3.4.)"),
("Write an example using `apt search` and `dnf search` into `~/lab/search_plan.txt`.","Include `apt search` in the note. (`>` → module 3.2.)"),
("Write the commands for listing installed packages (`rpm -qa`, `dpkg -l`) into `~/lab/query_plan.txt`.","Include `rpm -qa` in the note. (`>` → module 3.2.)"),
("Common mistake: why should `-y` be used carefully? Write a note for ticket #5501 into `~/lab/pitfalls_5501.txt`.","Include `-y` in the note. (`>` → module 3.2.)")]},
}
def rw(path,fn):
    s=open(path,encoding='utf-8',newline='').read()
    s=fn(s); open(path,'w',encoding='utf-8',newline='').write(s)
for m,rows in M.items():
    d=f'content/m{m}/'
    def mod(s):
        if '"t13"' in s: return s
        ls=[]
        for i,(k,df,c,sol) in enumerate(rows):
            ls.append('    {"id": "t%02d", "kind": "%s", "diff": %d, "check": %s, "solution": [%s]}'%(8+i,k,df,json.dumps(c,ensure_ascii=False),json.dumps(sol,ensure_ascii=False)))
        a='}]\r\n  ],\r\n  "vm"'
        old='}\r\n  ],\r\n  "vm"'
        assert old in s
        return s.replace(old,'},\r\n'+',\r\n'.join(ls)+'\r\n  ],\r\n  "vm"',1)
    rw(d+'module.json',mod)
    for lg in ('tr','de','en'):
        def f(s):
            if '"t13"' in s: return s
            ls=['    "t%02d": {"text": %s, "hint": %s}'%(8+i,json.dumps(t,ensure_ascii=False),json.dumps(h,ensure_ascii=False)) for i,(t,h) in enumerate(T[m][lg])]
            m_=re.search(r'("t07": \{.*?\})\r\n  \},\r\n  "vm"',s)
            assert m_
            return s[:m_.end(1)]+',\r\n'+',\r\n'.join(ls)+s[m_.end(1):]
        rw(d+lg+'.json',f)
