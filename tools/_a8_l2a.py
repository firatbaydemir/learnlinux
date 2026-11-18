import sys; sys.path.insert(0, 'tools')
from _a8lib import add_quiz

def Q(a, tr, de, en):
    return (a, {'tr': tr, 'de': de, 'en': en})

add_quiz('2.1', [
Q(1,
 ("Linux'ta tüm dosya sisteminin başlangıç noktası nedir?", ["C:\\", "/ (kök dizin)", "/root", "/home"], "Linux'ta sürücü harfi yoktur; her şey tek bir ağaç olan `/` altında dallanır. `/root` yalnızca root'un ana dizinidir."),
 ("Was ist der Ausgangspunkt des gesamten Linux-Dateisystems?", ["C:\\", "/ (Wurzelverzeichnis)", "/root", "/home"], "Linux kennt keine Laufwerksbuchstaben; alles hängt in einem Baum unter `/`. `/root` ist nur das Home von root."),
 ("What is the starting point of the whole Linux filesystem?", ["C:\\", "/ (root directory)", "/root", "/home"], "Linux has no drive letters; everything branches from the single tree under `/`. `/root` is only root's home.")),
Q(3,
 ("Çalışan çekirdek ve süreç bilgisini dosya gibi gösteren sanal dizin hangisidir?", ["/opt", "/tmp", "/usr", "/proc"], "`/proc` diskte yer kaplamaz; çekirdek ve süreç durumunu dosya olarak sunar (ör. `/proc/cpuinfo`)."),
 ("Welches virtuelle Verzeichnis zeigt Kernel- und Prozessinfos als Dateien?", ["/opt", "/tmp", "/usr", "/proc"], "`/proc` belegt keinen Plattenplatz; es stellt Kernel- und Prozesszustand als Dateien bereit (z. B. `/proc/cpuinfo`)."),
 ("Which virtual directory exposes kernel and process info as files?", ["/opt", "/tmp", "/usr", "/proc"], "`/proc` uses no disk space; it presents kernel and process state as files (e.g. `/proc/cpuinfo`).")),
Q(0,
 ("Aygıt dosyaları (disk, terminal vb.) hangi dizindedir?", ["/dev", "/etc", "/var", "/bin"], "Donanım `/dev` altında dosya olarak görünür (ör. `/dev/sda`, `/dev/null`)."),
 ("In welchem Verzeichnis liegen Gerätedateien (Platte, Terminal usw.)?", ["/dev", "/etc", "/var", "/bin"], "Hardware erscheint unter `/dev` als Dateien (z. B. `/dev/sda`, `/dev/null`)."),
 ("Which directory holds device files (disk, terminal, etc.)?", ["/dev", "/etc", "/var", "/bin"], "Hardware appears as files under `/dev` (e.g. `/dev/sda`, `/dev/null`).")),
Q(2,
 ("Yeniden başlatmada içeriği silinebilen geçici dosyalar için hangi dizin kullanılır?", ["/etc", "/usr", "/tmp", "/boot"], "`/tmp` geçici dosyalar içindir; önemli veriyi orada tutma. Ayarlar `/etc`, programlar `/usr` altındadır."),
 ("Welches Verzeichnis ist für temporäre Dateien, die beim Neustart gelöscht werden können?", ["/etc", "/usr", "/tmp", "/boot"], "`/tmp` ist für temporäre Dateien; keine wichtigen Daten dort ablegen. Konfiguration liegt in `/etc`, Programme in `/usr`."),
 ("Which directory is for temporary files that may be wiped on reboot?", ["/etc", "/usr", "/tmp", "/boot"], "`/tmp` is for temporary files; don't keep important data there. Config lives in `/etc`, programs in `/usr`.")),
])

add_quiz('2.2', [
Q(0,
 ("`ls -l` çıktısında satır `d` ile başlıyorsa bu nedir?", ["Dizin", "Düzenli dosya", "Aygıt dosyası", "Soket"], "İlk harf türü gösterir: `-` düzenli dosya, `d` dizin, `l` sembolik link, `c`/`b` aygıt."),
 ("Was ist es, wenn eine Zeile in `ls -l` mit `d` beginnt?", ["Verzeichnis", "Reguläre Datei", "Gerätedatei", "Socket"], "Der erste Buchstabe zeigt den Typ: `-` reguläre Datei, `d` Verzeichnis, `l` symbolischer Link, `c`/`b` Gerät."),
 ("What is it when a line in `ls -l` starts with `d`?", ["Directory", "Regular file", "Device file", "Socket"], "The first letter shows the type: `-` regular file, `d` directory, `l` symlink, `c`/`b` device.")),
Q(3,
 ("`ln -s hedef link` komutu ne oluşturur?", ["Sert link", "Dosyanın kopyasını", "Yeni dizin", "Sembolik link"], "`-s` sembolik link yapar: hedef yolunu tutan bir işaretçi. `-s`'siz `ln` sert link kurar."),
 ("Was erzeugt `ln -s ziel link`?", ["Einen Hardlink", "Eine Kopie der Datei", "Ein neues Verzeichnis", "Einen symbolischen Link"], "`-s` erzeugt einen symbolischen Link: einen Zeiger auf den Zielpfad. `ln` ohne `-s` erzeugt einen Hardlink."),
 ("What does `ln -s target link` create?", ["A hard link", "A copy of the file", "A new directory", "A symbolic link"], "`-s` makes a symlink: a pointer holding the target path. `ln` without `-s` makes a hard link.")),
Q(1,
 ("`~` işareti neyi temsil eder?", ["Kök dizini", "Geçerli kullanıcının ana dizinini", "Üst dizini", "Geçici dizini"], "`~` kabuk tarafından ana dizine açılır (ör. `/home/student`); `cd ~` ile aynı sonuç `cd`'dir."),
 ("Wofür steht das Zeichen `~`?", ["Das Wurzelverzeichnis", "Das Home-Verzeichnis des aktuellen Benutzers", "Das übergeordnete Verzeichnis", "Das temporäre Verzeichnis"], "`~` wird von der Shell zum Home-Verzeichnis expandiert (z. B. `/home/student`); `cd` allein wirkt wie `cd ~`."),
 ("What does the `~` character represent?", ["The root directory", "The current user's home directory", "The parent directory", "The temp directory"], "The shell expands `~` to the home directory (e.g. `/home/student`); plain `cd` acts like `cd ~`.")),
Q(2,
 ("`/var/log` içindeyken `cd ../..` sonrası neredesin?", ["/var", "/var/log", "/", "/home"], "Her `..` bir üst dizine çıkar: `/var/log` → `/var` → `/`."),
 ("Wo bist du nach `cd ../..`, wenn du in `/var/log` warst?", ["/var", "/var/log", "/", "/home"], "Jedes `..` geht eine Ebene hoch: `/var/log` → `/var` → `/`."),
 ("Where are you after `cd ../..` when starting in `/var/log`?", ["/var", "/var/log", "/", "/home"], "Each `..` goes up one level: `/var/log` → `/var` → `/`.")),
])

add_quiz('2.3', [
Q(2,
 ("`touch dosya` dosya zaten varsa ne yapar?", ["Hata verir", "İçeriğini siler", "İçeriğine dokunmadan zaman damgasını günceller", "Dosyayı yeniden adlandırır"], "`touch` yoksa boş dosya oluşturur, varsa yalnızca değiştirilme zamanını günceller; içerik korunur."),
 ("Was macht `touch datei`, wenn die Datei schon existiert?", ["Gibt einen Fehler aus", "Löscht den Inhalt", "Aktualisiert nur den Zeitstempel, Inhalt bleibt", "Benennt die Datei um"], "`touch` legt eine leere Datei an, falls sie fehlt, sonst aktualisiert es nur die Änderungszeit; der Inhalt bleibt."),
 ("What does `touch file` do if the file already exists?", ["Gives an error", "Erases its content", "Updates the timestamp, content is kept", "Renames the file"], "`touch` creates an empty file if missing, otherwise only updates the modification time; content stays.")),
Q(0,
 ("`touch rapor{1..3}.txt` kaç dosya oluşturur?", ["3 (rapor1.txt, rapor2.txt, rapor3.txt)", "1 (rapor{1..3}.txt)", "0, hata verir", "2"], "Süslü parantez (brace) açılımını kabuk yapar: `rapor1.txt rapor2.txt rapor3.txt` olur."),
 ("Wie viele Dateien erzeugt `touch bericht{1..3}.txt`?", ["3 (bericht1.txt, bericht2.txt, bericht3.txt)", "1 (bericht{1..3}.txt)", "0, Fehler", "2"], "Die Shell führt die Brace-Expansion aus: `bericht1.txt bericht2.txt bericht3.txt`."),
 ("How many files does `touch report{1..3}.txt` create?", ["3 (report1.txt, report2.txt, report3.txt)", "1 (report{1..3}.txt)", "0, error", "2"], "The shell performs brace expansion: `report1.txt report2.txt report3.txt`.")),
Q(3,
 ("İçinde dosya olan bir klasörü içeriğiyle birlikte silmek için ne kullanılır?", ["rmdir klasor", "rm klasor", "mkdir -d klasor", "rm -r klasor"], "`rmdir` yalnızca boş klasörü siler, `rm` tek başına klasörü silmez; özyinelemeli silme `rm -r`. Dikkatli kullan: geri dönüş yoktur."),
 ("Womit löschst du ein Verzeichnis samt Inhalt?", ["rmdir verzeichnis", "rm verzeichnis", "mkdir -d verzeichnis", "rm -r verzeichnis"], "`rmdir` löscht nur leere Verzeichnisse, `rm` allein keine Verzeichnisse; rekursiv mit `rm -r`. Vorsicht: kein Papierkorb."),
 ("What deletes a directory together with its contents?", ["rmdir dir", "rm dir", "mkdir -d dir", "rm -r dir"], "`rmdir` removes only empty directories, plain `rm` won't remove directories; recursive is `rm -r`. Careful: no undo.")),
Q(1,
 ("`rm -rf` komutunu çalıştırmadan önce en güvenli alışkanlık hangisidir?", ["Hemen çalıştırmak", "Aynı kalıbı önce `ls` ile listeleyip doğrulamak", "Önce `sudo` eklemek", "Hata mesajını gizlemek"], "Silmeden önce `ls` ile aynı yolu/joker karakteri kontrol et; `rm -rf` onay sormaz ve geri alınamaz."),
 ("Welche Gewohnheit ist vor `rm -rf` am sichersten?", ["Sofort ausführen", "Dasselbe Muster vorher mit `ls` auflisten und prüfen", "Zuerst `sudo` voranstellen", "Fehlermeldungen unterdrücken"], "Prüfe Pfad/Wildcard vorher mit `ls`; `rm -rf` fragt nicht nach und ist nicht rückgängig zu machen."),
 ("What is the safest habit before running `rm -rf`?", ["Run it right away", "List the same pattern with `ls` first and verify", "Prefix it with `sudo`", "Hide error messages"], "Check the same path/wildcard with `ls` first; `rm -rf` doesn't ask and can't be undone.")),
])
print('ok')
