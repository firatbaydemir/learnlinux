import sys; sys.path.insert(0, 'tools')
from _a8lib import add_quiz

def Q(a, tr, de, en):
    return (a, {'tr': tr, 'de': de, 'en': en})

add_quiz('2.4', [
Q(1,
 ("Bir klasörü içeriğiyle kopyalamak için hangi seçenek gerekir?", ["-i", "-r", "-n", "-v"], "`cp -r` klasörleri özyinelemeli kopyalar; `-i` sorar, `-n` üzerine yazmaz, `-v` ayrıntı gösterir."),
 ("Welche Option ist nötig, um ein Verzeichnis samt Inhalt zu kopieren?", ["-i", "-r", "-n", "-v"], "`cp -r` kopiert Verzeichnisse rekursiv; `-i` fragt nach, `-n` überschreibt nie, `-v` zeigt Details."),
 ("Which option is needed to copy a directory with its contents?", ["-i", "-r", "-n", "-v"], "`cp -r` copies directories recursively; `-i` prompts, `-n` never overwrites, `-v` is verbose.")),
Q(2,
 ("`mv a.txt b.txt` b.txt zaten varsa ve seçenek yoksa ne olur?", ["Hata verir", "Önce sorar", "b.txt sessizce üzerine yazılır", "İki dosya birleştirilir"], "`mv` ve `cp` varsayılan olarak sormadan üzerine yazar; korunmak için `-i` veya `-n` kullan."),
 ("Was passiert bei `mv a.txt b.txt`, wenn b.txt existiert und keine Option gesetzt ist?", ["Fehlermeldung", "Rückfrage", "b.txt wird stillschweigend überschrieben", "Beide Dateien werden zusammengeführt"], "`mv` und `cp` überschreiben standardmäßig ohne Nachfrage; Schutz mit `-i` oder `-n`."),
 ("What happens with `mv a.txt b.txt` if b.txt exists and no option is given?", ["It errors", "It asks first", "b.txt is silently overwritten", "The files are merged"], "`mv` and `cp` overwrite without asking by default; use `-i` or `-n` for protection.")),
Q(3,
 ("Hedefi mevcut dosyayı ASLA ezmeyen seçenek hangisidir?", ["-v", "-r", "-a", "-n"], "`-n` (no-clobber) var olan dosyanın üzerine yazmaz; `-i` ise her seferinde sorar."),
 ("Welche Option überschreibt eine vorhandene Zieldatei NIE?", ["-v", "-r", "-a", "-n"], "`-n` (no-clobber) überschreibt nie; `-i` fragt jedes Mal nach."),
 ("Which option NEVER overwrites an existing destination file?", ["-v", "-r", "-a", "-n"], "`-n` (no-clobber) never overwrites; `-i` prompts each time.")),
Q(0,
 ("`mv rapor.txt /tmp/` ne yapar?", ["Dosyayı /tmp içine taşır; eski yerinde kalmaz", "Dosyayı /tmp'ye kopyalar", "Dosyayı /tmp olarak yeniden adlandırır", "Hata verir"], "Hedef var olan bir dizinse `mv` dosyayı içine taşır; kaynak artık eski yerde değildir."),
 ("Was bewirkt `mv bericht.txt /tmp/`?", ["Verschiebt die Datei nach /tmp; am alten Ort ist sie weg", "Kopiert die Datei nach /tmp", "Benennt die Datei in /tmp um", "Gibt einen Fehler aus"], "Ist das Ziel ein vorhandenes Verzeichnis, verschiebt `mv` die Datei hinein; die Quelle existiert danach nicht mehr."),
 ("What does `mv report.txt /tmp/` do?", ["Moves the file into /tmp; it's gone from the old place", "Copies the file to /tmp", "Renames the file to /tmp", "Errors"], "If the target is an existing directory, `mv` moves the file into it; the source no longer exists.")),
])

add_quiz('2.5', [
Q(1,
 ("Bir dosyanın uzantısı `.txt` ama içeriği ikili (binary). Gerçek türü hangi komut söyler?", ["ls -l", "file", "wc", "touch"], "Uzantı yalnızca isimdir; `file` içeriğin ilk baytlarına (magic number) bakarak türü belirler."),
 ("Eine Datei heißt `.txt`, enthält aber Binärdaten. Welcher Befehl nennt den echten Typ?", ["ls -l", "file", "wc", "touch"], "Die Endung ist nur ein Name; `file` prüft die ersten Bytes (Magic Number) des Inhalts."),
 ("A file is named `.txt` but holds binary data. Which command reveals its real type?", ["ls -l", "file", "wc", "touch"], "The extension is just a name; `file` inspects the first bytes (magic number) of the content.")),
Q(3,
 ("Hangi komut izin, sahip, boyut ve üç zaman damgasını (Access/Modify/Change) birlikte gösterir?", ["ls", "file", "du", "stat"], "`stat` bir dosyanın inode bilgilerini ayrıntılı yazar; `ls -l` yalnızca özet verir."),
 ("Welcher Befehl zeigt Rechte, Besitzer, Größe und drei Zeitstempel (Access/Modify/Change)?", ["ls", "file", "du", "stat"], "`stat` gibt die Inode-Infos detailliert aus; `ls -l` liefert nur eine Kurzfassung."),
 ("Which command shows permissions, owner, size and three timestamps (Access/Modify/Change)?", ["ls", "file", "du", "stat"], "`stat` prints inode details; `ls -l` only gives a summary.")),
Q(0,
 ("Bir sembolik linkin işaret ettiği hedefi hangi komut yazar?", ["readlink link", "cat link", "stat -f link", "ln link"], "`readlink` linkin tuttuğu yolu gösterir; `readlink -f` zinciri çözüp mutlak yolu verir (`realpath` gibi)."),
 ("Welcher Befehl gibt das Ziel eines symbolischen Links aus?", ["readlink link", "cat link", "stat -f link", "ln link"], "`readlink` zeigt den im Link gespeicherten Pfad; `readlink -f` löst alles auf und liefert den absoluten Pfad (wie `realpath`)."),
 ("Which command prints the target of a symbolic link?", ["readlink link", "cat link", "stat -f link", "ln link"], "`readlink` shows the path stored in the link; `readlink -f` resolves everything to an absolute path (like `realpath`).")),
Q(2,
 ("Hedefi silinmiş sembolik linke ne denir ve `ls` nasıl gösterir?", ["Sert link; normal", "Boş dosya; siyah", "Kırık (dangling) link; hedef bulunamaz", "Dizin; mavi"], "Link hedefi silinirse link kalır ama boşa işaret eder: kırık link. `cat` \"No such file\" hatası verir."),
 ("Wie heißt ein symbolischer Link, dessen Ziel gelöscht wurde?", ["Hardlink; normal", "Leere Datei; schwarz", "Defekter (dangling) Link; Ziel nicht auffindbar", "Verzeichnis; blau"], "Wird das Ziel gelöscht, bleibt der Link, zeigt aber ins Leere: defekter Link. `cat` meldet „No such file“."),
 ("What is a symlink whose target was deleted called?", ["Hard link; normal", "Empty file; black", "Dangling (broken) link; target not found", "Directory; blue"], "If the target is deleted the link remains but points nowhere: a dangling link. `cat` reports \"No such file\".")),
])

add_quiz('2.6', [
Q(0,
 ("Küçük bir dosyayı tek seferde tamamen ekrana basmak için hangisi uygundur?", ["cat", "less", "tail -f", "wc -l"], "`cat` dosyanın tamamını yazar; büyük dosyada `less` gibi sayfalayıcı daha güvenlidir."),
 ("Womit gibst du eine kleine Datei komplett auf einmal aus?", ["cat", "less", "tail -f", "wc -l"], "`cat` gibt die ganze Datei aus; bei großen Dateien ist ein Pager wie `less` sicherer."),
 ("Which is suited to dump a small file to the screen in one go?", ["cat", "less", "tail -f", "wc -l"], "`cat` prints the whole file; for large files a pager like `less` is safer.")),
Q(3,
 ("`less` içinde çıkmak için hangi tuşa basılır?", ["x", "Ctrl+X", "Esc", "q"], "`q` less'ten çıkar. Arama için `/kelime`, sonraki eşleşme için `n` kullanılır."),
 ("Mit welcher Taste verlässt man `less`?", ["x", "Ctrl+X", "Esc", "q"], "`q` beendet less. Suchen mit `/wort`, nächster Treffer mit `n`."),
 ("Which key quits `less`?", ["x", "Ctrl+X", "Esc", "q"], "`q` quits less. Search with `/word`, next match with `n`.")),
Q(2,
 ("Bir log dosyasının son 20 satırını hangi komut gösterir?", ["head -n 20 log", "cat -20 log", "tail -n 20 log", "wc -n 20 log"], "`tail -n N` son N satırı, `head -n N` ilk N satırı gösterir."),
 ("Welcher Befehl zeigt die letzten 20 Zeilen einer Logdatei?", ["head -n 20 log", "cat -20 log", "tail -n 20 log", "wc -n 20 log"], "`tail -n N` zeigt die letzten N Zeilen, `head -n N` die ersten N."),
 ("Which command shows the last 20 lines of a log file?", ["head -n 20 log", "cat -20 log", "tail -n 20 log", "wc -n 20 log"], "`tail -n N` shows the last N lines, `head -n N` the first N.")),
Q(1,
 ("`grep -c ERROR app.log` ne verir?", ["ERROR içeren satırların kendisini", "ERROR içeren satırların sayısını", "Dosyadaki toplam satırı", "ERROR kelimesinin konumunu"], "`-c` eşleşen satırların sayısını yazar; satırları görmek için `-c`'siz `grep` kullan."),
 ("Was liefert `grep -c ERROR app.log`?", ["Die Zeilen mit ERROR selbst", "Die Anzahl der Zeilen mit ERROR", "Die Gesamtzahl der Zeilen", "Die Position des Wortes ERROR"], "`-c` gibt die Anzahl passender Zeilen aus; die Zeilen selbst sieht man mit `grep` ohne `-c`."),
 ("What does `grep -c ERROR app.log` output?", ["The ERROR lines themselves", "The number of lines containing ERROR", "The total number of lines", "The position of the word ERROR"], "`-c` prints the count of matching lines; to see the lines use `grep` without `-c`.")),
])
print('ok')
