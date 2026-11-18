import sys; sys.path.insert(0, 'tools')
from _a8lib import add_quiz

def Q(a, tr, de, en):
    return (a, {'tr': tr, 'de': de, 'en': en})

add_quiz('3.7', [
Q(2,
 ("`cmp a b` dosyalar farklıysa ne bildirir?", ["Tüm farkları satır satır", "Yalnızca ortak satırları", "İlk farkın bayt ve satır konumunu", "Birleştirilmiş yamayı"], "`cmp` bayt bayt karşılaştırır ve ilk farkı bildirip durur; ikili dosyalar için uygundur."),
 ("Was meldet `cmp a b`, wenn die Dateien verschieden sind?", ["Alle Unterschiede zeilenweise", "Nur gemeinsame Zeilen", "Byte- und Zeilenposition des ersten Unterschieds", "Einen fertigen Patch"], "`cmp` vergleicht byteweise und meldet den ersten Unterschied; geeignet für Binärdateien."),
 ("What does `cmp a b` report when the files differ?", ["All differences line by line", "Only common lines", "Byte and line position of the first difference", "A ready-made patch"], "`cmp` compares byte by byte and reports the first difference; suited for binary files.")),
Q(1,
 ("`diff -r dir_a dir_b` ne yapar?", ["Yalnızca dosya adlarını sıralar", "İki dizin ağacını alt dizinler dahil karşılaştırır", "Farkları tersine çevirir", "Dizinleri birleştirir"], "`-r` (recursive) alt dizinlere de iner; yalnızca birinde olan dosyalar `Only in ...` ile görünür."),
 ("Was macht `diff -r dir_a dir_b`?", ["Sortiert nur Dateinamen", "Vergleicht beide Verzeichnisbäume inklusive Unterverzeichnissen", "Kehrt die Unterschiede um", "Führt die Verzeichnisse zusammen"], "`-r` (rekursiv) geht in Unterverzeichnisse; Dateien nur in einer Seite erscheinen als `Only in ...`."),
 ("What does `diff -r dir_a dir_b` do?", ["Only sorts file names", "Compares both directory trees including subdirectories", "Reverses the differences", "Merges the directories"], "`-r` (recursive) descends into subdirectories; files present on one side only show as `Only in ...`.")),
Q(3,
 ("`comm -12 a b` ne gösterir (girdiler sıralı)?", ["Yalnızca a'daki satırları", "Yalnızca b'deki satırları", "İki dosyanın tüm satırlarını", "Her iki dosyada ortak olan satırları"], "`-1` ve `-2` yalnızca-a ve yalnızca-b sütunlarını gizler; geriye ortak satırlar (3. sütun) kalır."),
 ("Was zeigt `comm -12 a b` (sortierte Eingaben)?", ["Nur Zeilen aus a", "Nur Zeilen aus b", "Alle Zeilen beider Dateien", "Zeilen, die in beiden Dateien vorkommen"], "`-1` und `-2` blenden die Spalten nur-a und nur-b aus; es bleiben die gemeinsamen Zeilen (Spalte 3)."),
 ("What does `comm -12 a b` show (sorted input)?", ["Only lines from a", "Only lines from b", "All lines of both files", "Lines common to both files"], "`-1` and `-2` suppress the only-in-a and only-in-b columns, leaving common lines (column 3).")),
Q(0,
 ("`patch -p1 < fix.diff` içindeki `-p1` ne yapar?", ["Yamadaki dosya yollarının ilk dizin bileşenini atar", "Yamayı geri alır", "Önce yedek alır", "Yalnızca 1. parçayı uygular"], "`-pN` yoldaki ilk N bileşeni siler; `a/src/x.c` gibi önekleri hedef ağaca uydurur."),
 ("Was bewirkt `-p1` in `patch -p1 < fix.diff`?", ["Entfernt die erste Verzeichniskomponente der Pfade im Patch", "Macht den Patch rückgängig", "Legt zuerst ein Backup an", "Wendet nur den ersten Teil an"], "`-pN` entfernt die ersten N Pfadkomponenten; so passen Präfixe wie `a/src/x.c` zum Zielbaum."),
 ("What does `-p1` do in `patch -p1 < fix.diff`?", ["Strips the first directory component from paths in the patch", "Reverses the patch", "Makes a backup first", "Applies only the first hunk"], "`-pN` strips the first N path components so prefixes like `a/src/x.c` fit the target tree.")),
])

add_quiz('3.8', [
Q(1,
 ("`tar -czf out.tar.gz dir` içinde `c`, `z`, `f` ne anlama gelir?", ["çıkar, zip, filtre", "oluştur, gzip ile sıkıştır, dosya adı", "kontrol et, sıfırla, zorla", "kopyala, zip, format"], "`c` create, `z` gzip, `f` ardından arşiv dosya adı gelir."),
 ("Was bedeuten `c`, `z`, `f` in `tar -czf out.tar.gz dir`?", ["extract, zip, filter", "create, gzip-Kompression, Dateiname", "check, zero, force", "copy, zip, format"], "`c` create, `z` gzip, `f` leitet den Archivdateinamen ein."),
 ("What do `c`, `z`, `f` mean in `tar -czf out.tar.gz dir`?", ["extract, zip, filter", "create, gzip compression, file name", "check, zero, force", "copy, zip, format"], "`c` is create, `z` is gzip, `f` introduces the archive file name.")),
Q(2,
 ("Özgün dosyayı silmeden sıkıştırmak için hangisi kullanılır?", ["`gzip -d f`", "`gzip -r f`", "`gzip -k f`", "`gunzip f`"], "`gzip` normalde özgün dosyayı `.gz` ile değiştirir; `-k` (keep) özgün dosyayı korur."),
 ("Womit komprimiert man, ohne die Originaldatei zu löschen?", ["`gzip -d f`", "`gzip -r f`", "`gzip -k f`", "`gunzip f`"], "`gzip` ersetzt das Original normalerweise durch `.gz`; `-k` (keep) behält es."),
 ("Which compresses without deleting the original file?", ["`gzip -d f`", "`gzip -r f`", "`gzip -k f`", "`gunzip f`"], "`gzip` normally replaces the original with `.gz`; `-k` (keep) preserves it.")),
Q(3,
 ("Arşivden yalnızca tek bir dosyayı çıkarmak için nasıl yazılır?", ["`tar -tf a.tar yol/dosya`", "`tar -cf a.tar yol/dosya`", "`tar -xzf a.tar` ve sil", "`tar -xf a.tar yol/dosya`"], "`-x` sonrasına arşivdeki tam yol verilirse yalnızca o üye çıkarılır; yolu `-tf` ile öğren."),
 ("Wie extrahiert man nur eine einzelne Datei aus einem Archiv?", ["`tar -tf a.tar pfad/datei`", "`tar -cf a.tar pfad/datei`", "`tar -xzf a.tar` und löschen", "`tar -xf a.tar pfad/datei`"], "Gibt man nach `-x` den Pfad im Archiv an, wird nur dieser Eintrag extrahiert; Pfad vorher mit `-tf` ermitteln."),
 ("How do you extract just one file from an archive?", ["`tar -tf a.tar path/file`", "`tar -cf a.tar path/file`", "`tar -xzf a.tar` then delete", "`tar -xf a.tar path/file`"], "Giving the in-archive path after `-x` extracts only that member; find the path with `-tf`.")),
Q(0,
 ("`zip -r out.zip dir` içindeki `-r` neden gerekir?", ["Dizinin içeriğini alt dizinlerle ekler", "Arşivi şifreler", "Özgün dosyaları siler", "Sıkıştırmayı artırır"], "`-r` olmadan zip yalnızca dizinin kendisini ekler, içindekileri değil."),
 ("Wozu braucht man `-r` in `zip -r out.zip dir`?", ["Nimmt den Verzeichnisinhalt samt Unterverzeichnissen auf", "Verschlüsselt das Archiv", "Löscht die Originaldateien", "Erhöht die Kompression"], "Ohne `-r` fügt zip nur den Verzeichniseintrag hinzu, nicht den Inhalt."),
 ("Why is `-r` needed in `zip -r out.zip dir`?", ["Adds the directory contents including subdirectories", "Encrypts the archive", "Deletes the original files", "Increases compression"], "Without `-r` zip adds only the directory entry itself, not its contents.")),
])

add_quiz('3.9', [
Q(2,
 ("`xargs` ne yapar?", ["Dosyaları paralel kopyalar", "Komutu arka planda çalıştırır", "Standart girdiyi başka komuta argüman olarak verir", "Çıktıyı dosyaya yazar"], "`xargs` stdin'den okuduğu öğeleri bir komutun argümanlarına dönüştürür; `find | xargs` kalıbının temelidir."),
 ("Was macht `xargs`?", ["Kopiert Dateien parallel", "Startet Befehle im Hintergrund", "Übergibt Standardeingabe als Argumente an einen Befehl", "Schreibt die Ausgabe in eine Datei"], "`xargs` macht aus Elementen von stdin Argumente eines Befehls; Grundlage von `find | xargs`."),
 ("What does `xargs` do?", ["Copies files in parallel", "Runs a command in the background", "Passes standard input as arguments to a command", "Writes output to a file"], "`xargs` turns items read from stdin into a command's arguments; the basis of `find | xargs`.")),
Q(1,
 ("Hem çıktıyı hem hatayı `o.txt`'ye yazan doğru sıra hangisidir?", ["`cmd 2>&1 > o.txt`", "`cmd > o.txt 2>&1`", "`cmd 2> o.txt 1`", "`cmd &1>2 o.txt`"], "Yönlendirmeler soldan sağa işlenir: önce stdout dosyaya, sonra stderr stdout'un yeni hedefine gider."),
 ("Welche Reihenfolge schreibt Ausgabe und Fehler nach `o.txt`?", ["`cmd 2>&1 > o.txt`", "`cmd > o.txt 2>&1`", "`cmd 2> o.txt 1`", "`cmd &1>2 o.txt`"], "Umleitungen werden von links nach rechts ausgewertet: erst stdout in die Datei, dann stderr dorthin, wohin stdout zeigt."),
 ("Which order sends both output and errors to `o.txt`?", ["`cmd 2>&1 > o.txt`", "`cmd > o.txt 2>&1`", "`cmd 2> o.txt 1`", "`cmd &1>2 o.txt`"], "Redirections are processed left to right: stdout goes to the file first, then stderr follows stdout's new target.")),
Q(3,
 ("`cmd1 && cmd2` ne anlama gelir?", ["cmd2 her zaman çalışır", "cmd2, cmd1 başarısızsa çalışır", "İkisi aynı anda çalışır", "cmd2 yalnızca cmd1 başarılıysa (çıkış kodu 0) çalışır"], "`&&` başarıya bağlı zincirler; `||` ise başarısızlıkta çalıştırır."),
 ("Was bedeutet `cmd1 && cmd2`?", ["cmd2 läuft immer", "cmd2 läuft, wenn cmd1 fehlschlägt", "Beide laufen gleichzeitig", "cmd2 läuft nur, wenn cmd1 erfolgreich war (Exit-Code 0)"], "`&&` verkettet bei Erfolg; `||` führt bei Misserfolg aus."),
 ("What does `cmd1 && cmd2` mean?", ["cmd2 always runs", "cmd2 runs if cmd1 fails", "Both run at the same time", "cmd2 runs only if cmd1 succeeded (exit code 0)"], "`&&` chains on success; `||` runs on failure.")),
Q(0,
 ("`ls | tee liste.txt` ne yapar?", ["Çıktıyı hem ekrana yazar hem `liste.txt`'ye kaydeder", "Çıktıyı yalnızca dosyaya yazar", "Dosyayı ekrana kopyalar", "Hataları dosyaya ayırır"], "`tee` standart girdiyi hem stdout'a hem dosyaya iletir; `-a` ile dosyaya ekleme yapılır."),
 ("Was macht `ls | tee liste.txt`?", ["Zeigt die Ausgabe an und speichert sie in `liste.txt`", "Schreibt die Ausgabe nur in die Datei", "Kopiert die Datei auf den Bildschirm", "Trennt Fehler in eine Datei"], "`tee` leitet stdin an stdout und an eine Datei weiter; mit `-a` wird angehängt."),
 ("What does `ls | tee liste.txt` do?", ["Shows the output and also saves it to `liste.txt`", "Writes the output to the file only", "Copies the file to the screen", "Splits errors into a file"], "`tee` forwards stdin to both stdout and a file; `-a` appends.")),
])
print('ok')
