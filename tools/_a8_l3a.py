import sys; sys.path.insert(0, 'tools')
from _a8lib import add_quiz

def Q(a, tr, de, en):
    return (a, {'tr': tr, 'de': de, 'en': en})

add_quiz('3.1', [
Q(2,
 ("`ls x 2>&1 | wc -l` içinde hatalar neden de sayılır?", ["`wc` hataları kendisi yakalar", "Pipe stderr'i her zaman taşır", "`2>&1` stderr'i stdout'a yönlendirir, pipe ise stdout'u taşır", "`-l` hata satırlarını ekler"], "Pipe yalnızca stdout'u taşır; `2>&1` stderr'i stdout'un gittiği yere yönlendirdiği için hata satırları da `wc`'ye ulaşır."),
 ("Warum werden in `ls x 2>&1 | wc -l` auch Fehler gezählt?", ["`wc` fängt Fehler selbst ab", "Die Pipe transportiert immer stderr", "`2>&1` leitet stderr auf stdout um, und die Pipe transportiert stdout", "`-l` fügt Fehlerzeilen hinzu"], "Die Pipe transportiert nur stdout; `2>&1` schickt stderr dorthin, wohin stdout geht, daher erreichen auch Fehlerzeilen `wc`."),
 ("Why are errors also counted in `ls x 2>&1 | wc -l`?", ["`wc` catches errors itself", "A pipe always carries stderr", "`2>&1` redirects stderr to stdout, and the pipe carries stdout", "`-l` adds error lines"], "A pipe carries only stdout; `2>&1` sends stderr to wherever stdout goes, so error lines reach `wc` too.")),
Q(1,
 ("`echo x >> file` ile `echo x > file` arasındaki fark nedir?", ["Fark yoktur", "`>>` sona ekler, `>` içeriği silip üzerine yazar", "`>>` hata çıktısını yönlendirir", "`>` sona ekler, `>>` üzerine yazar"], "`>` dosyayı keser (truncate) ve yazar; `>>` mevcut içeriği korur ve sona ekler."),
 ("Was ist der Unterschied zwischen `echo x >> file` und `echo x > file`?", ["Kein Unterschied", "`>>` hängt an, `>` überschreibt den Inhalt", "`>>` leitet die Fehlerausgabe um", "`>` hängt an, `>>` überschreibt"], "`>` leert die Datei und schreibt neu; `>>` behält den Inhalt und hängt an."),
 ("What is the difference between `echo x >> file` and `echo x > file`?", ["No difference", "`>>` appends, `>` overwrites the contents", "`>>` redirects error output", "`>` appends, `>>` overwrites"], "`>` truncates the file and writes; `>>` keeps the existing content and appends.")),
Q(0,
 ("`wc -l < dosya` komutunda `<` ne yapar?", ["Dosyayı komutun stdin'i olarak verir", "Dosyayı siler", "Çıktıyı dosyaya yazar", "Hata çıktısını gizler"], "`<` bir dosyanın içeriğini komutun standart girdisine (0) bağlar; çıktı dosya adı içermez."),
 ("Was bewirkt `<` in `wc -l < datei`?", ["Gibt die Datei als stdin des Befehls", "Löscht die Datei", "Schreibt die Ausgabe in die Datei", "Blendet Fehlerausgabe aus"], "`<` verbindet den Dateiinhalt mit der Standardeingabe (0); die Ausgabe enthält keinen Dateinamen."),
 ("What does `<` do in `wc -l < file`?", ["Feeds the file as the command's stdin", "Deletes the file", "Writes the output to the file", "Hides error output"], "`<` connects a file's content to standard input (0); the output contains no file name.")),
Q(3,
 ("Hataları gürültü olmasın diye tamamen atmak için hangisi kullanılır?", ["`cmd > /dev/null`", "`cmd 2> /dev/zero`", "`cmd | /dev/null`", "`cmd 2> /dev/null`"], "`2> /dev/null` yalnızca stderr'i atar; `> /dev/null` normal çıktıyı atar. `/dev/null`'a boru kurulmaz."),
 ("Womit wirfst du Fehlermeldungen komplett weg?", ["`cmd > /dev/null`", "`cmd 2> /dev/zero`", "`cmd | /dev/null`", "`cmd 2> /dev/null`"], "`2> /dev/null` verwirft nur stderr; `> /dev/null` verwirft die normale Ausgabe. In `/dev/null` leitet man nicht per Pipe."),
 ("Which discards error messages entirely?", ["`cmd > /dev/null`", "`cmd 2> /dev/zero`", "`cmd | /dev/null`", "`cmd 2> /dev/null`"], "`2> /dev/null` discards only stderr; `> /dev/null` discards normal output. You cannot pipe into `/dev/null`.")),
])

add_quiz('3.2', [
Q(1,
 ("`sort | uniq -c` ne üretir?", ["Yalnızca tekrar eden satırları siler", "Her benzersiz satırın kaç kez geçtiğini", "Satırları rastgele karıştırır", "Dosyadaki karakter sayısını"], "`sort` aynı satırları yan yana getirir, `uniq -c` her grubun önüne tekrar sayısını yazar."),
 ("Was liefert `sort | uniq -c`?", ["Nur das Löschen doppelter Zeilen", "Wie oft jede eindeutige Zeile vorkommt", "Zufällig gemischte Zeilen", "Die Zeichenanzahl der Datei"], "`sort` bringt gleiche Zeilen zusammen, `uniq -c` stellt jeder Gruppe die Anzahl voran."),
 ("What does `sort | uniq -c` produce?", ["Only removes repeated lines", "How many times each unique line occurs", "Randomly shuffled lines", "The character count of the file"], "`sort` groups identical lines, `uniq -c` prefixes each group with its count.")),
Q(2,
 ("Dosyanın ilk 3 satırını hangi komut yazar?", ["`tail -n 3 f`", "`cat -3 f`", "`head -n 3 f`", "`wc -3 f`"], "`head -n N` ilk N satırı, `tail -n N` son N satırı yazar."),
 ("Welcher Befehl gibt die ersten 3 Zeilen einer Datei aus?", ["`tail -n 3 f`", "`cat -3 f`", "`head -n 3 f`", "`wc -3 f`"], "`head -n N` gibt die ersten N Zeilen aus, `tail -n N` die letzten N."),
 ("Which command prints the first 3 lines of a file?", ["`tail -n 3 f`", "`cat -3 f`", "`head -n 3 f`", "`wc -3 f`"], "`head -n N` prints the first N lines, `tail -n N` the last N.")),
Q(0,
 ("`cmd | tee -a log.txt` ile `tee log.txt` farkı nedir?", ["`-a` dosyaya ekler, yoksa üzerine yazar", "`-a` hataları da yakalar", "`-a` çıktıyı ekrandan gizler", "Fark yoktur"], "`tee` varsayılan olarak dosyanın üzerine yazar; `-a` (append) mevcut içeriğe ekler."),
 ("Was ist der Unterschied zwischen `cmd | tee -a log.txt` und `tee log.txt`?", ["`-a` hängt an, sonst wird überschrieben", "`-a` fängt auch Fehler ab", "`-a` blendet die Ausgabe aus", "Kein Unterschied"], "`tee` überschreibt standardmäßig; `-a` (append) hängt an den bestehenden Inhalt an."),
 ("What is the difference between `cmd | tee -a log.txt` and `tee log.txt`?", ["`-a` appends, otherwise it overwrites", "`-a` also captures errors", "`-a` hides output from the screen", "No difference"], "`tee` overwrites by default; `-a` (append) adds to the existing content.")),
Q(3,
 ("`sort -n` ile düz `sort` arasındaki fark nedir?", ["`-n` ters sıralar", "`-n` tekrarları siler", "`-n` büyük/küçük harf farkını yok sayar", "`-n` sayıları sayısal değerine göre sıralar"], "Düz `sort` metin olarak sıralar (`10` < `2`); `-n` sayısal sıralar (`2` < `10`)."),
 ("Was ist der Unterschied zwischen `sort -n` und `sort`?", ["`-n` sortiert umgekehrt", "`-n` entfernt Duplikate", "`-n` ignoriert Groß-/Kleinschreibung", "`-n` sortiert Zahlen nach ihrem numerischen Wert"], "Einfaches `sort` sortiert als Text (`10` < `2`); `-n` sortiert numerisch (`2` < `10`)."),
 ("What is the difference between `sort -n` and plain `sort`?", ["`-n` reverses the order", "`-n` removes duplicates", "`-n` ignores case", "`-n` sorts numbers by numeric value"], "Plain `sort` sorts as text (`10` < `2`); `-n` sorts numerically (`2` < `10`).")),
])

add_quiz('3.3', [
Q(1,
 ("`ls [ab]*` hangi dosyalarla eşleşir?", ["Adında a ve b olanlarla", "Adı a veya b ile başlayanlarla", "Adı ab ile bitenlerle", "Yalnızca adı `[ab]` olanla"], "`[ab]` tek karakterlik kümedir (a veya b); `*` ardından gelen her şeyi karşılar."),
 ("Welche Dateien passen auf `ls [ab]*`?", ["Solche mit a und b im Namen", "Solche, deren Name mit a oder b beginnt", "Solche, die auf ab enden", "Nur die Datei `[ab]`"], "`[ab]` ist eine Ein-Zeichen-Menge (a oder b); `*` steht für alles Folgende."),
 ("Which files does `ls [ab]*` match?", ["Names containing both a and b", "Names starting with a or b", "Names ending in ab", "Only a file named `[ab]`"], "`[ab]` is a one-character set (a or b); `*` matches whatever follows.")),
Q(2,
 ("Joker karakterleri (`*`, `?`) kim genişletir?", ["`ls` komutu", "Çekirdek", "Kabuk (shell), komut çalışmadan önce", "Dosya sistemi"], "Genişletmeyi kabuk yapar; komut desen değil, genişletilmiş dosya adı listesini alır."),
 ("Wer expandiert Platzhalter (`*`, `?`)?", ["Der Befehl `ls`", "Der Kernel", "Die Shell, bevor der Befehl startet", "Das Dateisystem"], "Die Shell expandiert; der Befehl erhält nicht das Muster, sondern die Liste der Dateinamen."),
 ("Who expands wildcards (`*`, `?`)?", ["The `ls` command", "The kernel", "The shell, before the command runs", "The file system"], "The shell expands them; the command receives the list of file names, not the pattern.")),
Q(0,
 ("`echo \"$(whoami)\"` ile `echo '$(whoami)'` çıktıları nasıl farklıdır?", ["Çift tırnak kullanıcı adını yazar, tek tırnak metni aynen yazar", "İkisi de kullanıcı adını yazar", "İkisi de metni aynen yazar", "Çift tırnak hata verir"], "Çift tırnak `$`, `$(...)` ve ters eğik çizgiyi çalıştırır; tek tırnak her şeyi düz metin yapar."),
 ("Wie unterscheiden sich `echo \"$(whoami)\"` und `echo '$(whoami)'`?", ["Doppelte Anführungszeichen geben den Benutzernamen aus, einfache den Text wörtlich", "Beide geben den Benutzernamen aus", "Beide geben den Text wörtlich aus", "Doppelte Anführungszeichen erzeugen einen Fehler"], "In doppelten Anführungszeichen werden `$`, `$(...)` und Backslash ausgewertet; einfache machen alles zu Text."),
 ("How do the outputs of `echo \"$(whoami)\"` and `echo '$(whoami)'` differ?", ["Double quotes print the user name, single quotes print the text literally", "Both print the user name", "Both print the text literally", "Double quotes give an error"], "Double quotes still evaluate `$`, `$(...)` and backslash; single quotes make everything literal.")),
Q(3,
 ("`rm *.log` çalıştırmadan önce güvenli bir ön kontrol nedir?", ["`rm -f *.log`", "`rm *.log &`", "`touch *.log`", "Önce `ls *.log` ile eşleşenleri görmek"], "Aynı deseni önce `ls` veya `echo` ile çalıştırarak neyin silineceğini görürsün."),
 ("Was ist eine sichere Vorabprüfung vor `rm *.log`?", ["`rm -f *.log`", "`rm *.log &`", "`touch *.log`", "Erst mit `ls *.log` die Treffer ansehen"], "Führe dasselbe Muster zuerst mit `ls` oder `echo` aus, um zu sehen, was gelöscht würde."),
 ("What is a safe pre-check before running `rm *.log`?", ["`rm -f *.log`", "`rm *.log &`", "`touch *.log`", "First view the matches with `ls *.log`"], "Run the same pattern with `ls` or `echo` first to see what would be deleted.")),
])
print('ok')
