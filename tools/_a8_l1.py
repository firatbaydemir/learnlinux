import sys; sys.path.insert(0, 'tools')
from _a8lib import add_quiz

def Q(a, tr, de, en):
    return (a, {'tr': tr, 'de': de, 'en': en})

add_quiz('1.1', [
Q(2,
 ("Hangi komut insan okunur boyutlarla (K, M, G) ayrıntılı liste verir?", ["ls -a", "ls -R", "ls -lh", "ls -d"], "`-l` uzun biçim, `-h` okunur boyut; `-a` gizli dosyaları, `-R` alt dizinleri de listeler."),
 ("Welcher Befehl listet ausführlich mit lesbaren Größen (K, M, G)?", ["ls -a", "ls -R", "ls -lh", "ls -d"], "`-l` Langformat, `-h` lesbare Größen; `-a` zeigt versteckte Dateien, `-R` auch Unterverzeichnisse."),
 ("Which command gives a long listing with human-readable sizes (K, M, G)?", ["ls -a", "ls -R", "ls -lh", "ls -d"], "`-l` is the long format, `-h` human-readable sizes; `-a` shows hidden files, `-R` recurses.")),
Q(0,
 ("Hangisi mutlak (absolute) yoldur?", ["/etc/hosts", "etc/hosts", "../etc/hosts", "~etc/hosts"], "Mutlak yol `/` ile başlar ve her yerden aynı dosyayı gösterir; göreli yol bulunduğun dizine bağlıdır."),
 ("Welcher ist ein absoluter Pfad?", ["/etc/hosts", "etc/hosts", "../etc/hosts", "~etc/hosts"], "Ein absoluter Pfad beginnt mit `/` und zeigt von überall auf dieselbe Datei; relative Pfade hängen vom aktuellen Verzeichnis ab."),
 ("Which one is an absolute path?", ["/etc/hosts", "etc/hosts", "../etc/hosts", "~etc/hosts"], "An absolute path starts with `/` and points to the same file from anywhere; relative paths depend on the current directory.")),
Q(3,
 ("`cd -` ne yapar?", ["Ana dizine gider", "Kök dizine gider", "Bir üst dizine gider", "Önceki bulunduğun dizine döner"], "`cd -` `OLDPWD` dizinine geçer; ana dizin için `cd` veya `cd ~`, üst dizin için `cd ..`."),
 ("Was macht `cd -`?", ["Wechselt ins Home-Verzeichnis", "Wechselt ins Wurzelverzeichnis", "Wechselt ein Verzeichnis nach oben", "Kehrt ins zuletzt besuchte Verzeichnis zurück"], "`cd -` wechselt nach `OLDPWD`; Home mit `cd` oder `cd ~`, nach oben mit `cd ..`."),
 ("What does `cd -` do?", ["Goes to the home directory", "Goes to the root directory", "Goes up one directory", "Returns to the previous directory"], "`cd -` switches to `OLDPWD`; use `cd` or `cd ~` for home and `cd ..` for the parent.")),
Q(1,
 ("`.` ve `..` girdileri ne anlama gelir?", ["Gizli sistem dosyaları, silinmelidir", "Geçerli dizin ve üst dizin", "Kök ve ana dizin", "Boş dosyalar"], "Her dizinde `.` kendisini, `..` üst dizini gösterir; `ls -a` ile görünürler."),
 ("Was bedeuten die Einträge `.` und `..`?", ["Versteckte Systemdateien, sollten gelöscht werden", "Aktuelles und übergeordnetes Verzeichnis", "Wurzel- und Home-Verzeichnis", "Leere Dateien"], "In jedem Verzeichnis steht `.` für es selbst und `..` für das übergeordnete; mit `ls -a` sichtbar."),
 ("What do the entries `.` and `..` mean?", ["Hidden system files, should be deleted", "Current directory and parent directory", "Root and home directory", "Empty files"], "In every directory `.` is itself and `..` is the parent; `ls -a` shows them.")),
])

add_quiz('1.2', [
Q(1,
 ("`id -u` çıktısı `0` ise bu ne demektir?", ["Kullanıcı yok", "root olarak çalışıyorsun", "Oturum kapalı", "Komut başarısız"], "UID 0 ayrıcalıklı root kullanıcısıdır; `id -u` yalnızca sayısal UID'yi yazar."),
 ("Was bedeutet die Ausgabe `0` bei `id -u`?", ["Kein Benutzer", "Du arbeitest als root", "Sitzung geschlossen", "Befehl fehlgeschlagen"], "UID 0 ist der privilegierte root-Benutzer; `id -u` gibt nur die numerische UID aus."),
 ("What does an output of `0` from `id -u` mean?", ["No user", "You are running as root", "Session closed", "Command failed"], "UID 0 is the privileged root user; `id -u` prints only the numeric UID.")),
Q(3,
 ("Çekirdek sürümü, mimari ve ana bilgisayar adını tek satırda hangi komut verir?", ["id -a", "df -h", "whoami -a", "uname -a"], "`uname -a` tüm sistem bilgisini birleştirir; `id` kullanıcı, `df` disk bilgisi verir."),
 ("Welcher Befehl liefert Kernel-Version, Architektur und Hostnamen in einer Zeile?", ["id -a", "df -h", "whoami -a", "uname -a"], "`uname -a` fasst alle Systeminfos zusammen; `id` zeigt den Benutzer, `df` Datenträger."),
 ("Which command gives kernel version, architecture and hostname on one line?", ["id -a", "df -h", "whoami -a", "uname -a"], "`uname -a` combines all system info; `id` shows the user, `df` shows disks.")),
Q(0,
 ("Bir dizinin toplam boyutunu özet olarak hangi komut verir?", ["du -sh dizin", "df -h dizin", "ls dizin", "uname dizin"], "`du` dosya/dizinin kullandığı alanı ölçer; `-s` özet, `-h` okunur birim. `df` ise dosya sistemi doluluğunu gösterir."),
 ("Welcher Befehl liefert die Gesamtgröße eines Verzeichnisses als Zusammenfassung?", ["du -sh verzeichnis", "df -h verzeichnis", "ls verzeichnis", "uname verzeichnis"], "`du` misst den belegten Platz; `-s` Summe, `-h` lesbar. `df` zeigt die Füllung des Dateisystems."),
 ("Which command gives a directory's total size as a summary?", ["du -sh dir", "df -h dir", "ls dir", "uname dir"], "`du` measures space used; `-s` summarises, `-h` is human-readable. `df` shows filesystem usage.")),
Q(2,
 ("Makinenin adını hangi komut gösterir?", ["whoami", "id", "hostname", "pwd"], "`hostname` makine adını yazar; `whoami`/`id` kullanıcıyı, `pwd` dizini gösterir."),
 ("Welcher Befehl zeigt den Namen des Rechners?", ["whoami", "id", "hostname", "pwd"], "`hostname` gibt den Rechnernamen aus; `whoami`/`id` zeigen den Benutzer, `pwd` das Verzeichnis."),
 ("Which command shows the machine's name?", ["whoami", "id", "hostname", "pwd"], "`hostname` prints the machine name; `whoami`/`id` show the user, `pwd` the directory.")),
])

add_quiz('1.3', [
Q(2,
 ("Ne yaptığını bilmediğin bir komutun kısa özetini hangi komut verir?", ["which", "pwd", "whatis", "history"], "`whatis komut` man sayfasının tek satırlık açıklamasını yazar; `which` yalnızca yolu bulur."),
 ("Welcher Befehl liefert eine Kurzbeschreibung eines unbekannten Befehls?", ["which", "pwd", "whatis", "history"], "`whatis befehl` gibt die Einzeiler-Beschreibung der man-Seite aus; `which` findet nur den Pfad."),
 ("Which command gives a one-line summary of a command you don't know?", ["which", "pwd", "whatis", "history"], "`whatis cmd` prints the man page's one-line description; `which` only finds the path.")),
Q(0,
 ("Adını tam hatırlamadığın komutu anahtar kelimeyle aramak için ne kullanılır?", ["man -k kelime (apropos)", "cd kelime", "pwd kelime", "echo kelime"], "`man -k` (= `apropos`) man sayfası başlık ve özetlerinde arama yapar."),
 ("Womit suchst du einen Befehl per Stichwort, dessen Namen du nicht genau kennst?", ["man -k stichwort (apropos)", "cd stichwort", "pwd stichwort", "echo stichwort"], "`man -k` (= `apropos`) durchsucht Titel und Kurzbeschreibungen der man-Seiten."),
 ("What do you use to search for a command by keyword when you don't remember its name?", ["man -k word (apropos)", "cd word", "pwd word", "echo word"], "`man -k` (= `apropos`) searches man page titles and summaries.")),
Q(3,
 ("`/etc/passwd` dosyasının biçimini anlatan man sayfasına hangi komutla ulaşırsın?", ["man passwd", "man 1 passwd.conf", "man 8 passwd", "man 5 passwd"], "`passwd` hem komut (bölüm 1) hem dosya biçimi (bölüm 5) adıdır; `man 5 passwd` dosya biçimini açar."),
 ("Wie erreichst du die man-Seite, die das Format von `/etc/passwd` beschreibt?", ["man passwd", "man 1 passwd.conf", "man 8 passwd", "man 5 passwd"], "`passwd` ist Befehl (Abschnitt 1) und Dateiformat (Abschnitt 5); `man 5 passwd` öffnet das Format."),
 ("How do you reach the man page describing the format of `/etc/passwd`?", ["man passwd", "man 1 passwd.conf", "man 8 passwd", "man 5 passwd"], "`passwd` is both a command (section 1) and a file format (section 5); `man 5 passwd` opens the format.")),
Q(1,
 ("Birçok komutta kısa kullanım özetini görmek için hangi seçenek yaygındır?", ["--run", "--help", "--quit", "--list-all"], "`komut --help` seçenekleri hızlıca listeler; ayrıntı için `man komut`."),
 ("Welche Option zeigt bei vielen Befehlen eine kurze Hilfe?", ["--run", "--help", "--quit", "--list-all"], "`befehl --help` listet die Optionen schnell auf; Details in `man befehl`."),
 ("Which option commonly shows a short usage summary?", ["--run", "--help", "--quit", "--list-all"], "`cmd --help` lists options quickly; use `man cmd` for details.")),
])

add_quiz('1.4', [
Q(1,
 ("`A || B` satırında B ne zaman çalışır?", ["A başarılı olursa", "A başarısız olursa", "Her zaman", "Hiçbir zaman"], "`||` \"yoksa\" demektir: B yalnızca A sıfırdan farklı çıkış kodu verirse çalışır."),
 ("Wann läuft B in der Zeile `A || B`?", ["Wenn A erfolgreich ist", "Wenn A fehlschlägt", "Immer", "Nie"], "`||` heißt „sonst“: B läuft nur, wenn A einen Exit-Status ungleich 0 liefert."),
 ("When does B run in the line `A || B`?", ["If A succeeds", "If A fails", "Always", "Never"], "`||` means \"otherwise\": B runs only if A returns a non-zero exit status.")),
Q(2,
 ("`A ; B` ile `A && B` arasındaki fark nedir?", ["Fark yoktur", "`;` yalnızca A başarısızsa B'yi çalıştırır", "`;` A'nın sonucuna bakmadan B'yi çalıştırır", "`&&` komutları paralel çalıştırır"], "`;` komutları sırayla, sonuca bakmadan çalıştırır; `&&` B'yi yalnızca A başarılıysa çalıştırır."),
 ("Was ist der Unterschied zwischen `A ; B` und `A && B`?", ["Kein Unterschied", "`;` startet B nur, wenn A fehlschlägt", "`;` startet B unabhängig vom Ergebnis von A", "`&&` führt Befehle parallel aus"], "`;` führt nacheinander aus, ohne das Ergebnis zu prüfen; `&&` startet B nur nach Erfolg von A."),
 ("What is the difference between `A ; B` and `A && B`?", ["No difference", "`;` runs B only if A fails", "`;` runs B regardless of A's result", "`&&` runs commands in parallel"], "`;` runs commands in sequence regardless of result; `&&` runs B only if A succeeded.")),
Q(3,
 ("Çıkış kodu 126 genellikle neyi gösterir?", ["Komut bulunamadı", "Başarılı", "Sözdizimi hatası yok", "Komut bulundu ama çalıştırılamadı (ör. izin yok)"], "126: bulundu ama çalıştırılamadı (çalıştırma izni yok vb.); 127: komut bulunamadı."),
 ("Worauf deutet Exit-Status 126 meist hin?", ["Befehl nicht gefunden", "Erfolg", "Kein Syntaxfehler", "Befehl gefunden, aber nicht ausführbar (z. B. keine Berechtigung)"], "126: gefunden, aber nicht ausführbar (fehlendes x-Recht o. Ä.); 127: Befehl nicht gefunden."),
 ("What does exit status 126 usually indicate?", ["Command not found", "Success", "No syntax error", "Command found but not executable (e.g. no permission)"], "126: found but could not be executed (missing execute permission etc.); 127: command not found.")),
Q(0,
 ("`ls /yok 2>&1` komutunda `2>&1` ne yapar?", ["Hata çıktısını standart çıktıya yönlendirir", "Çıktıyı siler", "Dosyayı 2 kez listeler", "Çıkış kodunu 1 yapar"], "`2>&1` stderr (2) akışını stdout (1) ile aynı yere gönderir; böylece hatalar da boru/dosyaya akar."),
 ("Was bewirkt `2>&1` in `ls /nix 2>&1`?", ["Leitet die Fehlerausgabe auf die Standardausgabe um", "Löscht die Ausgabe", "Listet die Datei zweimal", "Setzt den Exit-Status auf 1"], "`2>&1` schickt stderr (2) dorthin, wohin stdout (1) geht; so landen auch Fehler in Pipe/Datei."),
 ("What does `2>&1` do in `ls /nope 2>&1`?", ["Redirects error output to standard output", "Deletes the output", "Lists the file twice", "Sets the exit status to 1"], "`2>&1` sends stderr (2) to wherever stdout (1) goes, so errors also flow into a pipe/file.")),
])

add_quiz('1.5', [
Q(3,
 ("Tab tuşu terminalde ne işe yarar?", ["Komutu çalıştırır", "Ekranı temizler", "Oturumu kapatır", "Komut ve dosya adlarını tamamlar"], "Tab otomatik tamamlama yapar; belirsizse iki kez basınca seçenekleri listeler."),
 ("Wozu dient die Tab-Taste im Terminal?", ["Führt den Befehl aus", "Leert den Bildschirm", "Beendet die Sitzung", "Vervollständigt Befehls- und Dateinamen"], "Tab vervollständigt automatisch; bei Mehrdeutigkeit listet zweimaliges Drücken die Optionen."),
 ("What is the Tab key for in the terminal?", ["Runs the command", "Clears the screen", "Ends the session", "Completes command and file names"], "Tab auto-completes; if ambiguous, pressing it twice lists the options.")),
Q(1,
 ("Önceki komutlar arasında geriye doğru arama yapmak için hangi kısayol kullanılır?", ["Ctrl+L", "Ctrl+R", "Ctrl+Z", "Ctrl+A"], "`Ctrl+R` geçmişte artımlı arama başlatır; `Ctrl+L` ekranı temizler, `Ctrl+A` satır başına gider."),
 ("Mit welchem Kürzel durchsuchst du frühere Befehle rückwärts?", ["Ctrl+L", "Ctrl+R", "Ctrl+Z", "Ctrl+A"], "`Ctrl+R` startet die inkrementelle Suche in der Historie; `Ctrl+L` leert den Bildschirm, `Ctrl+A` springt zum Zeilenanfang."),
 ("Which shortcut searches backwards through previous commands?", ["Ctrl+L", "Ctrl+R", "Ctrl+Z", "Ctrl+A"], "`Ctrl+R` starts an incremental history search; `Ctrl+L` clears the screen, `Ctrl+A` jumps to line start.")),
Q(0,
 ("`echo \"Bugün: $(date +%F)\"` ne yapar?", ["`date` çıktısını metne yerleştirir", "`$(date +%F)` metnini aynen yazar", "Hata verir", "Tarihi değiştirir"], "`$(...)` komut ikamesidir: içindeki komut çalışır, çıktısı yerine konur. Çift tırnak bunu engellemez, tek tırnak engeller."),
 ("Was bewirkt `echo \"Heute: $(date +%F)\"`?", ["Setzt die Ausgabe von `date` in den Text ein", "Gibt `$(date +%F)` wörtlich aus", "Gibt einen Fehler aus", "Ändert das Datum"], "`$(...)` ist Befehlsersetzung: der Befehl läuft, seine Ausgabe wird eingesetzt. Doppelte Anführungszeichen verhindern das nicht, einfache schon."),
 ("What does `echo \"Today: $(date +%F)\"` do?", ["Inserts the output of `date` into the text", "Prints `$(date +%F)` literally", "Gives an error", "Changes the date"], "`$(...)` is command substitution: the command runs and its output is inserted. Double quotes allow it, single quotes block it.")),
Q(2,
 ("Geçerli oturumda `ll` adlı kısayolu `ls -l` olarak tanımlamak için ne yazılır?", ["export ll=ls -l", "set ll ls -l", "alias ll='ls -l'", "ln ll ls -l"], "`alias ad='komut'` kısayol tanımlar; kalıcı olması için `~/.bashrc` dosyasına yazılır. `export` değişken içindir."),
 ("Wie definierst du in der aktuellen Sitzung `ll` als Kurzform für `ls -l`?", ["export ll=ls -l", "set ll ls -l", "alias ll='ls -l'", "ln ll ls -l"], "`alias name='befehl'` definiert eine Kurzform; dauerhaft per Eintrag in `~/.bashrc`. `export` ist für Variablen."),
 ("How do you define `ll` as a shortcut for `ls -l` in the current session?", ["export ll=ls -l", "set ll ls -l", "alias ll='ls -l'", "ln ll ls -l"], "`alias name='cmd'` defines a shortcut; make it permanent in `~/.bashrc`. `export` is for variables.")),
])
print('ok')
