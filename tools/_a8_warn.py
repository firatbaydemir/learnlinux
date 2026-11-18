import sys
sys.path.insert(0, 'tools')
from _a8lib import rw
W = {
 ('0.1', 'family'): {
  'tr': "Sık hata: Ubuntu'daki `apt` komutunu Rocky/RHEL'de denemek. Önce `cat /etc/os-release` ile dağıtımı doğrula; paket yöneticisi aileye göre değişir (`apt` / `dnf`).",
  'de': "Häufiger Fehler: `apt` von Ubuntu auf Rocky/RHEL zu versuchen. Prüfe zuerst mit `cat /etc/os-release` die Distribution; der Paketmanager hängt von der Familie ab (`apt` / `dnf`).",
  'en': "Common mistake: trying Ubuntu's `apt` on Rocky/RHEL. Check the distribution first with `cat /etc/os-release`; the package manager depends on the family (`apt` / `dnf`)."},
 ('0.3', 'prompt'): {
  'tr': "Sık hata: Prompttaki `$` işaretini komutla birlikte yazmak. `$` yalnızca bir göstergedir; örneklerde yalnızca ondan sonrasını yaz. Komutlar büyük/küçük harfe duyarlıdır: `LS` ≠ `ls`.",
  'de': "Häufiger Fehler: das `$` des Prompts mitzutippen. `$` ist nur eine Anzeige; tippe in Beispielen nur, was danach steht. Befehle sind groß-/kleinschreibungsabhängig: `LS` ≠ `ls`.",
  'en': "Common mistake: typing the prompt's `$` along with the command. `$` is only an indicator; type just what follows it. Commands are case-sensitive: `LS` ≠ `ls`."},
}
for (m, sid), t in W.items():
    for lg in ('tr', 'de', 'en'):
        def f(d):
            for s in d['sections']:
                if s['id'] == sid:
                    s['warn'] = t[lg]; return
            raise AssertionError(sid)
        rw('content/m%s/%s.json' % (m, lg), f)
