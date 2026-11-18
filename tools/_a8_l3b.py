import sys; sys.path.insert(0, 'tools')
from _a8lib import add_quiz

def Q(a, tr, de, en):
    return (a, {'tr': tr, 'de': de, 'en': en})

add_quiz('3.4', [
Q(1,
 ("`grep -v INFO app.log` ne yazar?", ["Yalnızca INFO içeren satırları", "INFO içermeyen satırları", "INFO geçen satır sayısını", "INFO'nun satır numaralarını"], "`-v` eşleşmeyi tersine çevirir: desenle eşleşmeyen satırlar yazılır."),
 ("Was gibt `grep -v INFO app.log` aus?", ["Nur Zeilen mit INFO", "Zeilen ohne INFO", "Die Anzahl der INFO-Zeilen", "Die Zeilennummern von INFO"], "`-v` kehrt die Suche um: Es werden Zeilen ausgegeben, die nicht zum Muster passen."),
 ("What does `grep -v INFO app.log` print?", ["Only lines containing INFO", "Lines that do not contain INFO", "The number of INFO lines", "The line numbers of INFO"], "`-v` inverts the match: lines that do not match the pattern are printed.")),
Q(2,
 ("`grep -c ERROR app.log` neyi verir?", ["ERROR geçen tüm satırları", "ERROR kelimesinin kaç harf olduğunu", "ERROR içeren satırların sayısını", "Dosyadaki toplam satır sayısını"], "`-c` eşleşen satırları yazmaz, yalnızca sayısını yazar (kelime sayısını değil, satır sayısını)."),
 ("Was liefert `grep -c ERROR app.log`?", ["Alle Zeilen mit ERROR", "Die Buchstabenzahl von ERROR", "Die Anzahl der Zeilen mit ERROR", "Die Gesamtzahl der Zeilen"], "`-c` gibt nicht die Zeilen, sondern nur deren Anzahl aus (Zeilen, nicht Vorkommen)."),
 ("What does `grep -c ERROR app.log` return?", ["All lines containing ERROR", "How many letters ERROR has", "The number of lines containing ERROR", "The total number of lines"], "`-c` prints only the count of matching lines, not the lines themselves (lines, not occurrences).")),
Q(0,
 ("`find . -type d` neyi listeler?", ["Geçerli dizinin altındaki dizinleri", "Yalnızca düzenli dosyaları", "Yalnızca gizli dosyaları", "Silinmiş dosyaları"], "`-type d` dizinleri, `-type f` düzenli dosyaları seçer."),
 ("Was listet `find . -type d` auf?", ["Verzeichnisse unterhalb des aktuellen Verzeichnisses", "Nur reguläre Dateien", "Nur versteckte Dateien", "Gelöschte Dateien"], "`-type d` wählt Verzeichnisse, `-type f` reguläre Dateien."),
 ("What does `find . -type d` list?", ["Directories below the current directory", "Only regular files", "Only hidden files", "Deleted files"], "`-type d` selects directories, `-type f` regular files.")),
Q(3,
 ("`find . -name *.txt` yerine neden `-name '*.txt'` yazılır?", ["Tırnak aramayı hızlandırır", "Tırnaksız `-name` çalışmaz", "Tırnak büyük/küçük harfi yok sayar", "Kabuk deseni genişletmesin, `find` kendisi eşlesin diye"], "Tırnaksız `*.txt`'yi kabuk geçerli dizindeki dosyalara genişletebilir; tırnak deseni `find`'a olduğu gibi iletir."),
 ("Warum schreibt man `-name '*.txt'` statt `-name *.txt`?", ["Anführungszeichen beschleunigen die Suche", "Ohne Anführungszeichen läuft `-name` nicht", "Anführungszeichen ignorieren Groß-/Kleinschreibung", "Damit die Shell das Muster nicht expandiert und `find` es selbst auswertet"], "Ohne Anführungszeichen kann die Shell `*.txt` im aktuellen Verzeichnis expandieren; Anführungszeichen reichen das Muster unverändert an `find` weiter."),
 ("Why write `-name '*.txt'` instead of `-name *.txt`?", ["Quotes make the search faster", "`-name` does not work without quotes", "Quotes ignore case", "So the shell does not expand the pattern and `find` matches it itself"], "Unquoted, the shell may expand `*.txt` against the current directory; quotes pass the pattern to `find` unchanged.")),
])

add_quiz('3.5', [
Q(1,
 ("`sort -r` ne yapar?", ["Yinelenenleri siler", "Sıralamayı tersine çevirir", "Sayısal sıralar", "Dosyayı yerinde değiştirir"], "`-r` (reverse) sıralamayı ters çevirir; kaynak dosya değişmez."),
 ("Was bewirkt `sort -r`?", ["Entfernt Duplikate", "Kehrt die Sortierreihenfolge um", "Sortiert numerisch", "Ändert die Datei direkt"], "`-r` (reverse) kehrt die Reihenfolge um; die Quelldatei bleibt unverändert."),
 ("What does `sort -r` do?", ["Removes duplicates", "Reverses the sort order", "Sorts numerically", "Modifies the file in place"], "`-r` (reverse) reverses the order; the source file stays unchanged.")),
Q(2,
 ("`sort data.txt` komutu `data.txt` dosyasını değiştirir mi?", ["Evet, sıralı hâliyle üzerine yazar", "Evet, ama yedek alır", "Hayır, sonucu yalnızca ekrana yazar", "Yalnızca `-i` ile değiştirmez"], "`sort` çıktıyı stdout'a yazar; sonucu saklamak için `> yeni.txt` gibi yönlendirme gerekir."),
 ("Ändert `sort data.txt` die Datei `data.txt`?", ["Ja, sie wird sortiert überschrieben", "Ja, aber mit Backup", "Nein, das Ergebnis geht nur auf den Bildschirm", "Nur mit `-i` ändert es nichts"], "`sort` schreibt nach stdout; zum Speichern braucht man eine Umleitung wie `> neu.txt`."),
 ("Does `sort data.txt` modify `data.txt`?", ["Yes, it overwrites it sorted", "Yes, but it makes a backup", "No, it only prints the result", "Only without `-i`"], "`sort` writes to stdout; to keep the result you need a redirection such as `> new.txt`.")),
Q(3,
 ("`cut -d: -f1 /etc/passwd` ne yazar?", ["Her satırın son alanını", "Her satırın ilk karakterini", "Satır sayısını", "İki nokta ile ayrılmış ilk alanı (kullanıcı adı)"], "`-d:` ayırıcıyı `:` yapar, `-f1` birinci alanı seçer; `/etc/passwd`'de bu kullanıcı adıdır."),
 ("Was gibt `cut -d: -f1 /etc/passwd` aus?", ["Das letzte Feld jeder Zeile", "Das erste Zeichen jeder Zeile", "Die Zeilenanzahl", "Das erste durch Doppelpunkt getrennte Feld (Benutzername)"], "`-d:` setzt den Trenner auf `:`, `-f1` wählt das erste Feld; in `/etc/passwd` ist das der Benutzername."),
 ("What does `cut -d: -f1 /etc/passwd` print?", ["The last field of each line", "The first character of each line", "The line count", "The first colon-separated field (user name)"], "`-d:` sets the delimiter to `:`, `-f1` picks the first field; in `/etc/passwd` that is the user name.")),
Q(0,
 ("Hangi boru hattı en sık görülen değeri en üstte gösterir?", ["`sort | uniq -c | sort -nr`", "`uniq -c | sort`", "`sort -u | wc -l`", "`cut | tr`"], "`sort` eşitleri bir araya getirir, `uniq -c` sayar, `sort -nr` sayıya göre büyükten küçüğe dizer."),
 ("Welche Pipeline zeigt den häufigsten Wert zuoberst?", ["`sort | uniq -c | sort -nr`", "`uniq -c | sort`", "`sort -u | wc -l`", "`cut | tr`"], "`sort` gruppiert Gleiches, `uniq -c` zählt, `sort -nr` ordnet absteigend nach Zahl."),
 ("Which pipeline shows the most frequent value first?", ["`sort | uniq -c | sort -nr`", "`uniq -c | sort`", "`sort -u | wc -l`", "`cut | tr`"], "`sort` groups equal lines, `uniq -c` counts them, `sort -nr` orders by count, highest first.")),
])
print('ok')
