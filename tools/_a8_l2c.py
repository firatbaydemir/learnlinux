import sys; sys.path.insert(0, 'tools')
from _a8lib import add_quiz

def Q(a, tr, de, en):
    return (a, {'tr': tr, 'de': de, 'en': en})

add_quiz('2.7', [
Q(2,
 ("vim'de metin yazmaya başlamak için hangi moda geçilir?", ["Komut modu", "Görsel mod", "Ekleme modu (`i`)", "Ex modu (`:`)"], "Açılışta komut (normal) moddasın; `i` ekleme moduna geçirir, `Esc` normal moda döndürür."),
 ("In welchen Modus wechselt man in vim, um Text einzugeben?", ["Befehlsmodus", "Visueller Modus", "Einfügemodus (`i`)", "Ex-Modus (`:`)"], "Beim Start bist du im Normalmodus; `i` wechselt in den Einfügemodus, `Esc` zurück."),
 ("Which mode do you enter in vim to start typing text?", ["Command mode", "Visual mode", "Insert mode (`i`)", "Ex mode (`:`)"], "vim starts in normal mode; `i` enters insert mode, `Esc` returns.")),
Q(0,
 ("vim'de değişiklikleri KAYDEDİP çıkmak için ne yazılır?", [":wq", ":q!", ":w!q", "ZZZ"], "`:wq` yazar ve çıkar (`ZZ` de aynı işi görür); `:q!` kaydetmeden çıkar."),
 ("Was gibt man in vim ein, um zu SPEICHERN und zu beenden?", [":wq", ":q!", ":w!q", "ZZZ"], "`:wq` schreibt und beendet (`ZZ` ebenso); `:q!` beendet ohne Speichern."),
 ("What do you type in vim to SAVE and quit?", [":wq", ":q!", ":w!q", "ZZZ"], "`:wq` writes and quits (`ZZ` does too); `:q!` quits without saving.")),
Q(1,
 ("vim normal modda yanlış yaptığın son değişikliği geri almak için hangi tuş?", ["r", "u", "x", "p"], "`u` geri alır (undo), `Ctrl+R` yeniden uygular; `x` karakter siler, `p` yapıştırır."),
 ("Welche Taste macht im vim-Normalmodus die letzte Änderung rückgängig?", ["r", "u", "x", "p"], "`u` macht rückgängig (undo), `Ctrl+R` wiederholt; `x` löscht ein Zeichen, `p` fügt ein."),
 ("Which key undoes your last change in vim normal mode?", ["r", "u", "x", "p"], "`u` undoes, `Ctrl+R` redoes; `x` deletes a character, `p` pastes.")),
Q(3,
 ("vim'de bir kelimeyi dosya içinde aramak için normal modda ne yazılır?", [":kelime", "?? kelime", "find kelime", "/kelime"], "`/kelime` ileri arar, `n` sonraki eşleşmeye gider; `?kelime` geriye doğru arar."),
 ("Wie sucht man in vim im Normalmodus nach einem Wort?", [":wort", "?? wort", "find wort", "/wort"], "`/wort` sucht vorwärts, `n` springt zum nächsten Treffer; `?wort` sucht rückwärts."),
 ("How do you search for a word in vim from normal mode?", [":word", "?? word", "find word", "/word"], "`/word` searches forward, `n` jumps to the next match; `?word` searches backward.")),
])

add_quiz('2.8', [
Q(1,
 ("Bellek kullanımını insan okunur birimlerle hangi komut gösterir?", ["df -h", "free -h", "du -h", "uptime"], "`free -h` RAM ve swap'i özetler; `df` disk, `du` klasör boyutu, `uptime` yük ortalamasıdır."),
 ("Welcher Befehl zeigt die Speichernutzung in lesbaren Einheiten?", ["df -h", "free -h", "du -h", "uptime"], "`free -h` fasst RAM und Swap zusammen; `df` Datenträger, `du` Verzeichnisgröße, `uptime` die Last."),
 ("Which command shows memory usage in human-readable units?", ["df -h", "free -h", "du -h", "uptime"], "`free -h` summarises RAM and swap; `df` is disks, `du` directory size, `uptime` load.")),
Q(3,
 ("`uptime` çıktısındaki üç sayı (ör. 0.15, 0.10, 0.05) neyi gösterir?", ["Disk doluluğu", "Bellek kullanımı", "Ağ gecikmesi", "1, 5 ve 15 dakikalık yük ortalaması"], "Üç değer son 1, 5 ve 15 dakikanın ortalama sistem yüküdür; CPU çekirdek sayısıyla kıyaslanır."),
 ("Was zeigen die drei Zahlen in der `uptime`-Ausgabe (z. B. 0.15, 0.10, 0.05)?", ["Plattenbelegung", "Speichernutzung", "Netzwerklatenz", "Lastdurchschnitt der letzten 1, 5 und 15 Minuten"], "Die drei Werte sind die durchschnittliche Systemlast der letzten 1, 5 und 15 Minuten; Vergleich mit der CPU-Kernzahl."),
 ("What do the three numbers in `uptime` output (e.g. 0.15, 0.10, 0.05) show?", ["Disk usage", "Memory usage", "Network latency", "Load average over 1, 5 and 15 minutes"], "The three values are the average system load over the last 1, 5 and 15 minutes; compare with CPU core count.")),
Q(0,
 ("Bir hedefe giden ağ erişimini hızlıca sınamak için hangi komut kullanılır?", ["ping", "df", "free", "uname"], "`ping` ICMP yankı isteği gönderir; yanıt varsa hedefe ulaşım vardır. Bazı ağlar ICMP'yi engeller."),
 ("Womit prüft man schnell, ob ein Ziel im Netz erreichbar ist?", ["ping", "df", "free", "uname"], "`ping` sendet ICMP-Echo-Anfragen; kommt Antwort, ist das Ziel erreichbar. Manche Netze blockieren ICMP."),
 ("Which command quickly tests network reachability of a target?", ["ping", "df", "free", "uname"], "`ping` sends ICMP echo requests; a reply means the target is reachable. Some networks block ICMP.")),
Q(2,
 ("`df -h` çıktısında `Use%` 100 ise ne olur?", ["Hiçbir şey, normaldir", "Bellek dolmuştur", "O dosya sistemine artık yazılamaz", "Ağ kesilir"], "Dolu dosya sistemine yeni veri yazılamaz; servisler ve loglar hata verebilir. `du` ile yer kaplayanı bul."),
 ("Was bedeutet `Use%` 100 in der `df -h`-Ausgabe?", ["Nichts, ist normal", "Der Arbeitsspeicher ist voll", "Auf dieses Dateisystem kann nicht mehr geschrieben werden", "Das Netz fällt aus"], "In ein volles Dateisystem lässt sich nichts mehr schreiben; Dienste und Logs können fehlschlagen. Mit `du` den Platzfresser finden."),
 ("What does `Use%` at 100 in `df -h` mean?", ["Nothing, it's normal", "Memory is full", "No more data can be written to that filesystem", "The network goes down"], "A full filesystem cannot take new data; services and logs may fail. Use `du` to find what takes space.")),
])

add_quiz('2.9', [
Q(0,
 ("Aygıtların dosya sistemi türünü ve UUID'sini hangi komut gösterir?", ["blkid", "uname", "free", "ping"], "`blkid` (ve `lsblk -f`) dosya sistemi türü, etiket ve UUID'yi yazar."),
 ("Welcher Befehl zeigt Dateisystemtyp und UUID von Geräten?", ["blkid", "uname", "free", "ping"], "`blkid` (und `lsblk -f`) gibt Dateisystemtyp, Label und UUID aus."),
 ("Which command shows the filesystem type and UUID of devices?", ["blkid", "uname", "free", "ping"], "`blkid` (and `lsblk -f`) prints filesystem type, label and UUID.")),
Q(2,
 ("`umount` ile bağlı bir dosya sistemi \"busy\" hatası veriyorsa en olası neden nedir?", ["Disk bozuktur", "fstab hatalıdır", "Bir süreç veya kabuk o dizini kullanıyordur", "Dosya sistemi boştur"], "Bir kabuğun çalışma dizini veya açık dosya `busy` nedenidir; önce dizinden çık, `lsof`/`fuser` ile kullananı bul."),
 ("Warum meldet `umount` oft „busy“?", ["Die Platte ist defekt", "fstab ist fehlerhaft", "Ein Prozess oder eine Shell nutzt das Verzeichnis noch", "Das Dateisystem ist leer"], "Ein Arbeitsverzeichnis oder eine offene Datei verursacht `busy`; erst das Verzeichnis verlassen, Nutzer mit `lsof`/`fuser` finden."),
 ("Why does `umount` often say \"busy\"?", ["The disk is broken", "fstab is wrong", "A process or shell is still using that directory", "The filesystem is empty"], "A shell's working directory or an open file causes `busy`; leave the directory, find users with `lsof`/`fuser`.")),
Q(3,
 ("Yeniden başlatmadan sonra da otomatik bağlanması için bağlama bilgisi nereye yazılır?", ["/etc/hosts", "/etc/passwd", "/proc/mounts", "/etc/fstab"], "`/etc/fstab` açılışta bağlanacak dosya sistemlerini tanımlar. Hatalı satır açılışı bozabilir; önce `mount -a` ile dene."),
 ("Wohin gehört der Mount-Eintrag, damit er auch nach dem Neustart gilt?", ["/etc/hosts", "/etc/passwd", "/proc/mounts", "/etc/fstab"], "`/etc/fstab` definiert beim Boot einzuhängende Dateisysteme. Fehlerhafte Zeilen können den Start stören; vorher mit `mount -a` testen."),
 ("Where does the mount entry go so it persists after reboot?", ["/etc/hosts", "/etc/passwd", "/proc/mounts", "/etc/fstab"], "`/etc/fstab` defines filesystems mounted at boot. A bad line can break booting; test with `mount -a` first.")),
Q(1,
 ("`mkfs.ext4 /dev/sdb1` komutu ne yapar?", ["Bölümü bağlar", "Bölümde yeni bir ext4 dosya sistemi oluşturur (veriyi siler)", "Bölümü kontrol eder", "Disk boyutunu gösterir"], "`mkfs` biçimlendirir; mevcut veri erişilemez olur. Önce `lsblk` ile doğru aygıtı doğrula."),
 ("Was bewirkt `mkfs.ext4 /dev/sdb1`?", ["Hängt die Partition ein", "Erstellt ein neues ext4-Dateisystem auf der Partition (löscht Daten)", "Prüft die Partition", "Zeigt die Plattengröße"], "`mkfs` formatiert; vorhandene Daten sind danach unerreichbar. Erst mit `lsblk` das richtige Gerät prüfen."),
 ("What does `mkfs.ext4 /dev/sdb1` do?", ["Mounts the partition", "Creates a new ext4 filesystem on the partition (destroys data)", "Checks the partition", "Shows disk size"], "`mkfs` formats; existing data becomes inaccessible. Verify the right device with `lsblk` first.")),
])
print('ok')
