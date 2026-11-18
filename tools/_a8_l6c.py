import sys; sys.path.insert(0, 'tools')
from _a8lib import add_quiz

def Q(a, tr, de, en):
    return (a, {'tr': tr, 'de': de, 'en': en})

add_quiz('6.6', [
Q(1,
 ("`for f in *.log; do ...; done` döngüsü neyin üzerinde döner?", ["Yalnızca ilk dosya", "Eşleşen her dosya adı", "Dosya içeriğindeki satırlar", "Alt dizinlerdeki tüm dosyalar"], "Glob eşleşen dosya adlarına genişler; değişkeni her zaman `\"$f\"` biçiminde tırnakla."),
 ("Worüber iteriert `for f in *.log; do ...; done`?", ["Nur die erste Datei", "Jeden passenden Dateinamen", "Zeilen im Dateiinhalt", "Alle Dateien in Unterverzeichnissen"], "Der Glob wird zu den passenden Dateinamen; Variable immer als `\"$f\"` quoten."),
 ("What does `for f in *.log; do ...; done` iterate over?", ["Only the first file", "Every matching file name", "Lines in the file content", "All files in subdirectories"], "The glob expands to matching file names; always quote the variable as `\"$f\"`.")),
Q(3,
 ("Fonksiyondan değer döndürmenin yaygın yolu hangisidir?", ["`return \"metin\"`", "`export` ile", "`exit` ile fonksiyon biter", "`echo` ile yazıp `$(...)` ile yakalamak"], "`return` yalnızca 0–255 çıkış kodu verir; metin için `echo` ve komut ikamesi kullanılır."),
 ("Wie gibt man üblicherweise einen Wert aus einer Funktion zurück?", ["`return \"text\"`", "Mit `export`", "`exit` beendet die Funktion", "Mit `echo` ausgeben und per `$(...)` erfassen"], "`return` liefert nur einen Exit-Code 0–255; für Text nutzt man `echo` und Kommandosubstitution."),
 ("What is the usual way to return a value from a function?", ["`return \"text\"`", "With `export`", "`exit` ends the function", "Print with `echo` and capture with `$(...)`"], "`return` only gives an exit code 0–255; for text use `echo` and command substitution.")),
Q(0,
 ("Döngüde `\"$@\"` ile `$*` (tırnaksız) arasındaki fark nedir?", ["`\"$@\"` her argümanı ayrı ve bozulmadan korur", "Fark yoktur", "`$*` boşlukları korur", "`\"$@\"` yalnızca ilk argümanı verir"], "`\"$@\"` boşluk içeren argümanları tek parça bırakır; tırnaksız `$*` kelimelere böler."),
 ("Was ist der Unterschied zwischen `\"$@\"` und unquotiertem `$*`?", ["`\"$@\"` erhält jedes Argument getrennt und unversehrt", "Kein Unterschied", "`$*` erhält Leerzeichen", "`\"$@\"` liefert nur das erste Argument"], "`\"$@\"` lässt Argumente mit Leerzeichen intakt; unquotiertes `$*` wird in Wörter zerlegt."),
 ("What is the difference between `\"$@\"` and unquoted `$*`?", ["`\"$@\"` keeps each argument separate and intact", "No difference", "`$*` preserves spaces", "`\"$@\"` yields only the first argument"], "`\"$@\"` keeps arguments with spaces whole; unquoted `$*` is word-split.")),
Q(2,
 ("`while read -r line; do ...; done < dosya` içindeki `-r` ne sağlar?", ["Satırları tersine çevirir", "Dosyayı salt okunur açar", "Ters eğik çizgileri yorumlamaz", "Boş satırları atlar"], "`-r` ters eğik çizgiyi kaçış olarak işlemez; satırlar olduğu gibi okunur."),
 ("Was bewirkt `-r` in `while read -r line; do ...; done < datei`?", ["Kehrt Zeilen um", "Öffnet die Datei schreibgeschützt", "Interpretiert Backslashes nicht", "Überspringt Leerzeilen"], "`-r` behandelt Backslashes nicht als Escape; Zeilen bleiben unverändert."),
 ("What does `-r` do in `while read -r line; do ...; done < file`?", ["Reverses lines", "Opens the file read-only", "Does not interpret backslashes", "Skips blank lines"], "`-r` does not treat backslash as an escape; lines are read as they are.")),
])

add_quiz('6.7', [
Q(0,
 ("Zamanlayıcıların listesini ve sonraki çalışma zamanını hangi komut gösterir?", ["`systemctl list-timers`", "`crontab -l`", "`journalctl --timers`", "`systemctl status cron`"], "`systemctl list-timers` NEXT, LEFT, LAST ve tetiklenen birimi listeler."),
 ("Welcher Befehl zeigt Timer und nächste Ausführung?", ["`systemctl list-timers`", "`crontab -l`", "`journalctl --timers`", "`systemctl status cron`"], "`systemctl list-timers` listet NEXT, LEFT, LAST und die ausgelöste Unit."),
 ("Which command lists timers and their next run?", ["`systemctl list-timers`", "`crontab -l`", "`journalctl --timers`", "`systemctl status cron`"], "`systemctl list-timers` lists NEXT, LEFT, LAST and the triggered unit.")),
Q(2,
 ("`OnCalendar=*-*-* 03:00:00` ne zaman çalışır?", ["Her saat", "Ayın ilk günü", "Her gün 03:00'te", "Yalnızca açılışta"], "Alanlar yıl-ay-gün saat biçimindedir; yıldız her değer anlamına gelir."),
 ("Wann läuft `OnCalendar=*-*-* 03:00:00`?", ["Jede Stunde", "Am Monatsersten", "Täglich um 03:00", "Nur beim Boot"], "Die Felder sind Jahr-Monat-Tag Uhrzeit; der Stern steht für jeden Wert."),
 ("When does `OnCalendar=*-*-* 03:00:00` fire?", ["Every hour", "On the first of the month", "Every day at 03:00", "Only at boot"], "Fields are year-month-day time; the asterisk means every value.")),
Q(3,
 ("Takvim ifadesini deploy etmeden doğrulamak için hangi komut kullanılır?", ["`systemctl cat`", "`timedatectl`", "`crontab -e`", "`systemd-analyze calendar \"...\"`"], "`systemd-analyze calendar` ifadeyi çözümler ve sonraki tetiklenme zamanını gösterir."),
 ("Mit welchem Befehl prüft man einen Kalenderausdruck vorab?", ["`systemctl cat`", "`timedatectl`", "`crontab -e`", "`systemd-analyze calendar \"...\"`"], "`systemd-analyze calendar` normalisiert den Ausdruck und zeigt den nächsten Zeitpunkt."),
 ("Which command validates a calendar expression before deploying?", ["`systemctl cat`", "`timedatectl`", "`crontab -e`", "`systemd-analyze calendar \"...\"`"], "`systemd-analyze calendar` normalises the expression and shows the next elapse.")),
Q(1,
 ("`.timer` birimi hangi birimi başlatır (varsayılan)?", ["Aynı adlı `.target`", "Aynı adlı `.service`", "`cron.service`", "Hiçbirini"], "`backup.timer` varsayılan olarak `backup.service`'i tetikler; `Unit=` ile değiştirilebilir."),
 ("Welche Unit startet eine `.timer`-Unit standardmäßig?", ["Das gleichnamige `.target`", "Den gleichnamigen `.service`", "`cron.service`", "Keine"], "`backup.timer` löst standardmäßig `backup.service` aus; mit `Unit=` änderbar."),
 ("Which unit does a `.timer` start by default?", ["The same-named `.target`", "The same-named `.service`", "`cron.service`", "None"], "`backup.timer` triggers `backup.service` by default; changeable with `Unit=`.")),
])

add_quiz('6.8', [
Q(2,
 ("Rocky'de `/srv/company/web` için kalıcı SELinux etiketi nasıl verilir?", ["`chcon` yeterlidir ve kalıcıdır", "`setenforce 0`", "`semanage fcontext` + `restorecon`", "`chmod 755`"], "`semanage fcontext` kuralı politikaya yazar, `restorecon` uygular; `chcon` yeniden etiketlemede kaybolur."),
 ("Wie setzt man auf Rocky dauerhaft das SELinux-Label für `/srv/company/web`?", ["`chcon` genügt und ist dauerhaft", "`setenforce 0`", "`semanage fcontext` + `restorecon`", "`chmod 755`"], "`semanage fcontext` trägt die Regel in die Richtlinie ein, `restorecon` wendet sie an; `chcon` geht bei Relabel verloren."),
 ("How do you set a persistent SELinux label for `/srv/company/web` on Rocky?", ["`chcon` is enough and permanent", "`setenforce 0`", "`semanage fcontext` + `restorecon`", "`chmod 755`"], "`semanage fcontext` stores the rule in policy, `restorecon` applies it; `chcon` is lost on relabel.")),
Q(0,
 ("Hizmeti taşırken en güvenli denetim sırası hangisidir?", ["Hizmet durumu → portlar (`ss`) → güvenlik duvarı → günlükler", "Önce sunucuyu yeniden başlat", "Önce SELinux'u kapat", "Önce tüm kuralları sil"], "Katman katman ilerlemek sorunu hızla daraltır; güvenlik mekanizmalarını kapatmak çözüm değildir."),
 ("Welche Prüfreihenfolge ist bei Dienstproblemen am sichersten?", ["Dienststatus → Ports (`ss`) → Firewall → Logs", "Erst den Server neu starten", "Erst SELinux abschalten", "Erst alle Regeln löschen"], "Schichtweises Vorgehen grenzt das Problem schnell ein; Sicherheitsmechanismen abzuschalten ist keine Lösung."),
 ("What is the safest order to troubleshoot a service?", ["Service status → ports (`ss`) → firewall → logs", "Reboot the server first", "Disable SELinux first", "Delete all rules first"], "Going layer by layer narrows the problem quickly; disabling security is not a fix.")),
Q(3,
 ("Yedekleme betiğinin cron/timer altında güvenilir çalışması için ne gerekir?", ["Göreli yollar kullanmak", "Çıktıyı yok saymak", "Yalnızca root'un ortamına güvenmek", "Mutlak yollar ve çıkış kodu denetimi"], "Zamanlanmış görevlerde PATH ve çalışma dizini sınırlıdır; mutlak yol ve `set -euo pipefail` güvenilirlik sağlar."),
 ("Was braucht ein Backup-Skript für zuverlässigen Lauf unter cron/Timer?", ["Relative Pfade", "Ausgabe ignorieren", "Nur auf root-Umgebung vertrauen", "Absolute Pfade und Exit-Code-Prüfung"], "In geplanten Jobs sind PATH und Arbeitsverzeichnis begrenzt; absolute Pfade und `set -euo pipefail` schaffen Zuverlässigkeit."),
 ("What makes a backup script run reliably under cron/timer?", ["Relative paths", "Ignoring output", "Trusting root's environment", "Absolute paths and exit-code checks"], "Scheduled jobs have a limited PATH and working directory; absolute paths and `set -euo pipefail` add reliability.")),
Q(1,
 ("Paylaşılan dizin için `2770` yerine `0770` kullanılırsa ne eksik kalır?", ["Grup yazma izni", "Yeni dosyaların dizin grubunu devralması", "Sahibin erişimi", "Diğerlerinin erişimi"], "Setgid biti (2) yeni dosyaların grubunu dizinin grubu yapar; yoksa ekip ortak erişimi kaybeder."),
 ("Was fehlt bei `0770` statt `2770` für ein Gruppenverzeichnis?", ["Gruppen-Schreibrecht", "Neue Dateien erben die Verzeichnisgruppe nicht", "Zugriff des Besitzers", "Zugriff der anderen"], "Das Setgid-Bit (2) lässt neue Dateien die Gruppe des Verzeichnisses erben; ohne verliert das Team den gemeinsamen Zugriff."),
 ("What is missing with `0770` instead of `2770` on a shared directory?", ["Group write permission", "New files inheriting the directory's group", "Owner access", "Others' access"], "The setgid bit (2) makes new files inherit the directory's group; without it the team loses shared access.")),
])
print('ok')
