import sys; sys.path.insert(0, 'tools')
from _a8lib import add_quiz

def Q(a, tr, de, en):
    return (a, {'tr': tr, 'de': de, 'en': en})

add_quiz('6.4', [
Q(1,
 ("`pvcreate /dev/sdb1` ne yapar?", ["Dosya sistemi oluşturur", "Bölümü LVM için fiziksel hacim (PV) olarak hazırlar", "Mantıksal hacim oluşturur", "Disk bölümünü siler"], "`pvcreate` aygıta LVM meta verisi yazar; VG ve LV daha sonra gelir."),
 ("Was macht `pvcreate /dev/sdb1`?", ["Erstellt ein Dateisystem", "Bereitet die Partition als LVM-Physical-Volume (PV) vor", "Erstellt ein Logical Volume", "Löscht die Partition"], "`pvcreate` schreibt LVM-Metadaten auf das Gerät; VG und LV folgen danach."),
 ("What does `pvcreate /dev/sdb1` do?", ["Creates a filesystem", "Prepares the partition as an LVM physical volume (PV)", "Creates a logical volume", "Deletes the partition"], "`pvcreate` writes LVM metadata to the device; VG and LV come afterwards.")),
Q(3,
 ("Hangi komut VG'de ne kadar boş alan kaldığını gösterir?", ["`lsblk -f`", "`pvs -a`", "`df -h`", "`vgs` (VFree sütunu)"], "`vgs` VSize ve VFree gösterir; `lvextend` öncesi buraya bakılır."),
 ("Welcher Befehl zeigt den freien Platz in der VG?", ["`lsblk -f`", "`pvs -a`", "`df -h`", "`vgs` (Spalte VFree)"], "`vgs` zeigt VSize und VFree; vor `lvextend` schaut man dorthin."),
 ("Which command shows how much free space the VG has?", ["`lsblk -f`", "`pvs -a`", "`df -h`", "`vgs` (VFree column)"], "`vgs` shows VSize and VFree; check it before `lvextend`.")),
Q(0,
 ("`lvextend -L +100M` çalıştı ama `df` boyutu değişmedi. Neden?", ["Dosya sistemi de büyütülmedi (`-r` veya `resize2fs`/`xfs_growfs`)", "VG dolu", "LV küçüldü", "Yeniden başlatma gerekir"], "LV büyür, dosya sistemi ayrı büyütülür; `-r` ikisini birlikte yapar."),
 ("`lvextend -L +100M` lief, aber `df` zeigt dieselbe Größe. Warum?", ["Das Dateisystem wurde nicht mitvergrößert (`-r` oder `resize2fs`/`xfs_growfs`)", "VG ist voll", "LV wurde kleiner", "Neustart nötig"], "Das LV wächst, das Dateisystem muss separat wachsen; `-r` erledigt beides."),
 ("`lvextend -L +100M` succeeded but `df` shows the old size. Why?", ["The filesystem was not grown as well (`-r` or `resize2fs`/`xfs_growfs`)", "The VG is full", "The LV shrank", "A reboot is required"], "The LV grows, the filesystem must be grown separately; `-r` does both.")),
Q(2,
 ("XFS dosya sistemi için hangi işlem desteklenmez?", ["Çevrimiçi büyütme", "`xfs_growfs` ile büyütme", "Küçültme", "LV üzerine kurulum"], "XFS yalnızca büyütülebilir; küçültmek için yedekle, yeniden oluştur, geri yükle gerekir."),
 ("Welche Operation wird bei XFS nicht unterstützt?", ["Online-Vergrößerung", "Vergrößern mit `xfs_growfs`", "Verkleinern", "Einrichtung auf einem LV"], "XFS kann nur wachsen; zum Verkleinern sichern, neu anlegen, wiederherstellen."),
 ("Which operation is not supported on XFS?", ["Online growing", "Growing with `xfs_growfs`", "Shrinking", "Installing on an LV"], "XFS can only grow; to shrink, back up, recreate, restore.")),
])

add_quiz('6.5', [
Q(2,
 ("Betikte `name=\"Ali\"` yerine `name = \"Ali\"` yazılırsa ne olur?", ["Aynı sonucu verir", "Değişken boş kalır", "Bash `name` adlı komutu çalıştırmaya çalışır", "Sözdizimi hatası ile kapanır"], "Atamada `=` çevresinde boşluk olamaz; aksi halde `name` komut sayılır."),
 ("Was passiert bei `name = \"Ali\"` statt `name=\"Ali\"`?", ["Gleiches Ergebnis", "Variable bleibt leer", "Bash versucht, ein Kommando `name` auszuführen", "Abbruch mit Syntaxfehler"], "Bei Zuweisungen darf um `=` kein Leerzeichen stehen; sonst ist `name` ein Befehl."),
 ("What happens with `name = \"Ali\"` instead of `name=\"Ali\"`?", ["Same result", "The variable stays empty", "Bash tries to run a command called `name`", "It aborts with a syntax error"], "No spaces are allowed around `=` in assignments; otherwise `name` is treated as a command.")),
Q(1,
 ("`$?` neyi içerir?", ["Betiğin PID'ini", "Son komutun çıkış kodunu", "Argüman sayısını", "Tüm argümanları"], "`0` başarı, sıfırdan farklı değer hatadır; `$$` PID, `$#` argüman sayısıdır."),
 ("Was enthält `$?`?", ["Die PID des Skripts", "Den Exit-Code des letzten Befehls", "Die Anzahl der Argumente", "Alle Argumente"], "`0` heißt Erfolg, alles andere Fehler; `$$` ist die PID, `$#` die Argumentzahl."),
 ("What does `$?` contain?", ["The script's PID", "The exit code of the last command", "The number of arguments", "All arguments"], "`0` means success, non-zero means failure; `$$` is the PID, `$#` the argument count.")),
Q(3,
 ("Dosyanın varlığını denetleyen doğru koşul hangisidir?", ["`if [ -d dosya ]`", "`if [ -z dosya ]`", "`if [ dosya ]`", "`if [ -e dosya ]`"], "`-e` varlık, `-f` normal dosya, `-d` dizin denetler; `-z` boş dizgi testidir."),
 ("Welche Bedingung prüft, ob eine Datei existiert?", ["`if [ -d datei ]`", "`if [ -z datei ]`", "`if [ datei ]`", "`if [ -e datei ]`"], "`-e` prüft Existenz, `-f` reguläre Datei, `-d` Verzeichnis; `-z` testet leere Strings."),
 ("Which condition checks that a file exists?", ["`if [ -d file ]`", "`if [ -z file ]`", "`if [ file ]`", "`if [ -e file ]`"], "`-e` tests existence, `-f` a regular file, `-d` a directory; `-z` tests an empty string.")),
Q(0,
 ("Betiğin ilk satırındaki `#!/bin/bash` ne işe yarar?", ["Betiği hangi yorumlayıcının çalıştıracağını belirtir", "Yorum satırıdır, etkisizdir", "Çalıştırma iznini verir", "Betiği yedekler"], "Shebang çekirdeğe yorumlayıcıyı söyler; çalıştırma izni için yine `chmod +x` gerekir."),
 ("Wozu dient `#!/bin/bash` in der ersten Zeile?", ["Legt den Interpreter des Skripts fest", "Ist nur ein Kommentar ohne Wirkung", "Erteilt das Ausführungsrecht", "Sichert das Skript"], "Der Shebang nennt dem Kernel den Interpreter; das Ausführungsrecht braucht weiterhin `chmod +x`."),
 ("What is `#!/bin/bash` on the first line for?", ["It names the interpreter that runs the script", "It is a comment with no effect", "It grants execute permission", "It backs up the script"], "The shebang tells the kernel the interpreter; execute permission still needs `chmod +x`.")),
])
print('ok')
