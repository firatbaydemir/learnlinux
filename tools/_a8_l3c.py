import sys; sys.path.insert(0, 'tools')
from _a8lib import add_quiz

def Q(a, tr, de, en):
    return (a, {'tr': tr, 'de': de, 'en': en})

add_quiz('3.6', [
Q(1,
 ("`sed 's/cat/dog/g' f` komutundaki `g` neyi değiştirir?", ["Dosyayı yerinde düzenler", "Satırdaki tüm eşleşmeleri değiştirir", "Büyük/küçük harfi yok sayar", "Yalnızca eşleşen satırları yazar"], "`g` (global) olmadan her satırda yalnızca ilk eşleşme değişir."),
 ("Was ändert das `g` in `sed 's/cat/dog/g' f`?", ["Bearbeitet die Datei direkt", "Ersetzt alle Treffer in der Zeile", "Ignoriert Groß-/Kleinschreibung", "Gibt nur passende Zeilen aus"], "Ohne `g` (global) wird pro Zeile nur der erste Treffer ersetzt."),
 ("What does `g` change in `sed 's/cat/dog/g' f`?", ["Edits the file in place", "Replaces all matches on the line", "Ignores case", "Prints only matching lines"], "Without `g` (global) only the first match on each line is replaced.")),
Q(2,
 ("`sed -n '2,4p' f` ne yazar?", ["Dosyanın tamamını", "2. ve 4. satırlar dışındakileri", "2. ile 4. arasındaki satırları", "Yalnızca 4. satırı"], "`-n` otomatik çıktıyı kapatır, `2,4p` yalnızca 2–4. satırları yazdırır."),
 ("Was gibt `sed -n '2,4p' f` aus?", ["Die ganze Datei", "Alles außer Zeile 2 und 4", "Die Zeilen 2 bis 4", "Nur Zeile 4"], "`-n` unterdrückt die automatische Ausgabe, `2,4p` druckt nur die Zeilen 2–4."),
 ("What does `sed -n '2,4p' f` print?", ["The whole file", "Everything except lines 2 and 4", "Lines 2 through 4", "Only line 4"], "`-n` turns off automatic output, `2,4p` prints only lines 2–4.")),
Q(0,
 ("`sed -i.bak 's/a/b/' f` içindeki `.bak` ne işe yarar?", ["Değişmeden önceki dosyanın yedeğini `f.bak` olarak saklar", "Çıktıyı ekrana yazar", "Değişikliği geri alır", "Dosyayı siler"], "`-i` sonekle birlikte kullanılırsa özgün dosya o sonekle yedeklenir, sonra yerinde düzenlenir."),
 ("Wozu dient `.bak` in `sed -i.bak 's/a/b/' f`?", ["Speichert vor der Änderung ein Backup als `f.bak`", "Gibt die Ausgabe auf dem Bildschirm aus", "Macht die Änderung rückgängig", "Löscht die Datei"], "Mit Suffix gibt `-i` die Originaldatei als Backup mit diesem Suffix aus, danach wird direkt bearbeitet."),
 ("What is `.bak` for in `sed -i.bak 's/a/b/' f`?", ["Keeps a backup of the original as `f.bak` before changing", "Prints the output to the screen", "Undoes the change", "Deletes the file"], "With a suffix, `-i` saves the original under that suffix, then edits in place.")),
Q(3,
 ("`awk '{print $1}' f` ne yazar?", ["Her satırın son alanını", "Dosyanın ilk satırını", "Satır numarasını", "Her satırın ilk alanını"], "`awk` satırları varsayılan olarak boşluklarla alanlara böler; `$1` ilk alandır, `$NF` sonuncudur."),
 ("Was gibt `awk '{print $1}' f` aus?", ["Das letzte Feld jeder Zeile", "Die erste Zeile der Datei", "Die Zeilennummer", "Das erste Feld jeder Zeile"], "`awk` teilt Zeilen standardmäßig an Leerraum in Felder; `$1` ist das erste, `$NF` das letzte."),
 ("What does `awk '{print $1}' f` print?", ["The last field of each line", "The first line of the file", "The line number", "The first field of each line"], "`awk` splits lines into fields on whitespace by default; `$1` is the first, `$NF` the last.")),
])
print('ok')
