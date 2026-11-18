import sys; sys.path.insert(0, 'tools')
from _a8lib import add_quiz

def Q(a, tr, de, en):
    return (a, {'tr': tr, 'de': de, 'en': en})

add_quiz('4.4', [
Q(2,
 ("`chmod 640 f` hangi izni verir?", ["rw-r-xr--", "rwxr-----", "rw-r-----", "r--rw----"], "6 = rw (sahip), 4 = r (grup), 0 = hiçbiri (diğerleri)."),
 ("Welche Rechte setzt `chmod 640 f`?", ["rw-r-xr--", "rwxr-----", "rw-r-----", "r--rw----"], "6 = rw (Besitzer), 4 = r (Gruppe), 0 = nichts (andere)."),
 ("Which permissions does `chmod 640 f` set?", ["rw-r-xr--", "rwxr-----", "rw-r-----", "r--rw----"], "6 = rw (owner), 4 = r (group), 0 = none (others).")),
Q(1,
 ("`chmod g+w f` ne yapar?", ["Herkese yazma izni verir", "Gruba yazma izni ekler, diğer izinleri korur", "Grubu değiştirir", "Yazma iznini kaldırır"], "Sembolik kipte `+` mevcut izinlere ekler; `u/g/o/a` kime uygulanacağını seçer."),
 ("Was bewirkt `chmod g+w f`?", ["Gibt allen Schreibrecht", "Fügt der Gruppe Schreibrecht hinzu, andere Rechte bleiben", "Ändert die Gruppe", "Entfernt das Schreibrecht"], "Im symbolischen Modus fügt `+` hinzu; `u/g/o/a` wählt den Adressaten."),
 ("What does `chmod g+w f` do?", ["Gives everyone write access", "Adds write for the group, keeping other bits", "Changes the group", "Removes write access"], "In symbolic mode `+` adds; `u/g/o/a` selects who it applies to.")),
Q(3,
 ("Dosya sahibini ve grubunu aynı anda değiştiren komut hangisidir?", ["`chmod alice:devs f`", "`chgrp alice:devs f`", "`chown :devs f`", "`chown alice:devs f`"], "`chown kullanıcı:grup` ikisini birden değiştirir; `chgrp` yalnızca grubu, `chown :grup` de yalnızca grubu."),
 ("Welcher Befehl ändert Besitzer und Gruppe gleichzeitig?", ["`chmod alice:devs f`", "`chgrp alice:devs f`", "`chown :devs f`", "`chown alice:devs f`"], "`chown benutzer:gruppe` ändert beides; `chgrp` und `chown :gruppe` nur die Gruppe."),
 ("Which command changes owner and group at once?", ["`chmod alice:devs f`", "`chgrp alice:devs f`", "`chown :devs f`", "`chown alice:devs f`"], "`chown user:group` changes both; `chgrp` and `chown :group` change only the group.")),
Q(0,
 ("`umask 022` iken yeni dizin hangi izinle oluşur?", ["755", "644", "777", "700"], "Dizinler 777'den, dosyalar 666'dan başlar; maske 022 çıkarılınca dizin 755, dosya 644 olur."),
 ("Welche Rechte hat ein neues Verzeichnis bei `umask 022`?", ["755", "644", "777", "700"], "Verzeichnisse starten bei 777, Dateien bei 666; mit Maske 022 ergibt sich 755 bzw. 644."),
 ("Which mode does a new directory get with `umask 022`?", ["755", "644", "777", "700"], "Directories start from 777, files from 666; subtracting mask 022 gives 755 and 644.")),
])

add_quiz('4.5', [
Q(1,
 ("`chmod u+s` bir çalıştırılabilir dosyada ne sağlar?", ["Dosyayı salt okunur yapar", "Dosya, çalıştıran değil sahibi olarak çalışır", "Dosyayı yalnızca grup çalıştırabilir", "Dosyanın silinmesini engeller"], "Setuid bit: süreç dosya sahibinin etkin UID'siyle çalışır; `passwd` buna örnektir."),
 ("Was bewirkt `chmod u+s` bei einer ausführbaren Datei?", ["Macht sie schreibgeschützt", "Sie läuft mit den Rechten des Besitzers statt des Aufrufers", "Nur die Gruppe darf sie ausführen", "Verhindert das Löschen"], "Setuid-Bit: der Prozess läuft mit der effektiven UID des Besitzers; Beispiel `passwd`."),
 ("What does `chmod u+s` do on an executable?", ["Makes it read-only", "It runs as the file owner rather than the caller", "Only the group can run it", "Prevents deletion"], "Setuid bit: the process runs with the owner's effective UID; `passwd` is an example.")),
Q(2,
 ("`chmod 2775 dir` içindeki baştaki `2` neyi ayarlar?", ["Sticky bit", "Setuid", "Setgid", "Hiçbirini"], "Baştaki rakam: 4 = setuid, 2 = setgid, 1 = sticky."),
 ("Was setzt die führende `2` in `chmod 2775 dir`?", ["Sticky-Bit", "Setuid", "Setgid", "Nichts davon"], "Die führende Ziffer: 4 = setuid, 2 = setgid, 1 = sticky."),
 ("What does the leading `2` in `chmod 2775 dir` set?", ["Sticky bit", "Setuid", "Setgid", "None of them"], "The leading digit: 4 = setuid, 2 = setgid, 1 = sticky.")),
Q(3,
 ("Sticky bit'li klasörde bir kullanıcı neyi silebilir?", ["Herkesin dosyasını", "Hiçbir dosyayı", "Yalnızca klasörün grubunun dosyalarını", "Yalnızca kendi dosyalarını (veya sahibi/root ise)"], "Sticky bit, silme/yeniden adlandırmayı dosya sahibi, klasör sahibi ve root ile sınırlar."),
 ("Was darf ein Benutzer in einem Verzeichnis mit Sticky-Bit löschen?", ["Dateien aller Benutzer", "Keine Datei", "Nur Dateien der Verzeichnisgruppe", "Nur eigene Dateien (oder als Verzeichnisbesitzer/root)"], "Das Sticky-Bit beschränkt Löschen/Umbenennen auf Dateibesitzer, Verzeichnisbesitzer und root."),
 ("What may a user delete in a directory with the sticky bit?", ["Everyone's files", "No files", "Only files of the directory's group", "Only their own files (or as directory owner/root)"], "The sticky bit limits deletion/renaming to the file owner, directory owner and root.")),
Q(0,
 ("`lsattr` çıktısındaki `i` özniteliği ne anlama gelir?", ["Dosya değiştirilemez ve silinemez (immutable)", "Dosya gizlidir", "Dosya sıkıştırılmıştır", "Dosya yalnızca eklenebilir"], "`chattr +i` root dahi olsa değiştirme/silmeyi engeller; yalnızca ekleme için `a` kullanılır."),
 ("Was bedeutet das Attribut `i` in der `lsattr`-Ausgabe?", ["Datei ist unveränderlich und nicht löschbar (immutable)", "Datei ist versteckt", "Datei ist komprimiert", "An die Datei darf nur angehängt werden"], "`chattr +i` verhindert Ändern/Löschen selbst für root; zum reinen Anhängen dient `a`."),
 ("What does the `i` attribute in `lsattr` output mean?", ["File is immutable and cannot be changed or deleted", "File is hidden", "File is compressed", "File is append-only"], "`chattr +i` blocks modification/deletion even for root; append-only is `a`.")),
])
print('ok')
