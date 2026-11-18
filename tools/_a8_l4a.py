import sys; sys.path.insert(0, 'tools')
from _a8lib import add_quiz

def Q(a, tr, de, en):
    return (a, {'tr': tr, 'de': de, 'en': en})

add_quiz('4.1', [
Q(1,
 ("`id -nG` ne gösterir?", ["UID değerini", "Kullanıcının üyesi olduğu grupların adlarını", "Son girişleri", "Oturum açmış kullanıcıları"], "`-G` tüm grupları, `-n` sayı yerine adları yazar."),
 ("Was zeigt `id -nG`?", ["Die UID", "Die Namen aller Gruppen des Benutzers", "Letzte Anmeldungen", "Angemeldete Benutzer"], "`-G` gibt alle Gruppen aus, `-n` Namen statt Zahlen."),
 ("What does `id -nG` show?", ["The UID", "The names of all groups the user belongs to", "Recent logins", "Logged-in users"], "`-G` prints all groups, `-n` prints names instead of numbers.")),
Q(2,
 ("`w` komutu `who`'ya ek olarak ne gösterir?", ["Parola özetlerini", "Başarısız girişleri", "Oturumların o an çalıştırdığı komutu ve yük bilgisini", "Grup üyeliklerini"], "`w` her oturumun çalıştırdığı komutu, boşta kalma süresini ve load average'ı da verir."),
 ("Was zeigt `w` zusätzlich zu `who`?", ["Passwort-Hashes", "Fehlgeschlagene Anmeldungen", "Den aktuell ausgeführten Befehl und die Last", "Gruppenmitgliedschaften"], "`w` zeigt auch den Befehl jeder Sitzung, Leerlaufzeit und Load Average."),
 ("What does `w` show in addition to `who`?", ["Password hashes", "Failed logins", "The command each session is running and load info", "Group memberships"], "`w` also reports each session's current command, idle time and load average.")),
Q(0,
 ("`last` geçmiş girişleri hangi dosyadan okur?", ["`/var/log/wtmp`", "`/etc/passwd`", "`/etc/shadow`", "`/var/log/btmp`"], "`last` wtmp'yi, `lastb` ise başarısız denemeleri tutan btmp'yi okur."),
 ("Aus welcher Datei liest `last` frühere Anmeldungen?", ["`/var/log/wtmp`", "`/etc/passwd`", "`/etc/shadow`", "`/var/log/btmp`"], "`last` liest wtmp, `lastb` liest btmp mit den fehlgeschlagenen Versuchen."),
 ("Which file does `last` read for past logins?", ["`/var/log/wtmp`", "`/etc/passwd`", "`/etc/shadow`", "`/var/log/btmp`"], "`last` reads wtmp; `lastb` reads btmp, which holds failed attempts.")),
Q(3,
 ("`/etc/shadow`'da parola alanı `!` ile başlıyorsa ne anlama gelir?", ["Parola süresi dolmuş", "Hesap silinmiş", "Parola boş", "Parola ile giriş kilitli"], "`!` (veya `*`) geçerli bir parola özeti olmadığını gösterir; parola ile giriş yapılamaz."),
 ("Was bedeutet es, wenn das Passwortfeld in `/etc/shadow` mit `!` beginnt?", ["Passwort abgelaufen", "Konto gelöscht", "Passwort leer", "Anmeldung per Passwort gesperrt"], "`!` (oder `*`) heißt: kein gültiger Hash, Passwort-Anmeldung ist nicht möglich."),
 ("What does a `!` at the start of the password field in `/etc/shadow` mean?", ["Password expired", "Account deleted", "Password is empty", "Password login is locked"], "`!` (or `*`) means there is no valid hash, so password login is impossible.")),
])

add_quiz('4.2', [
Q(2,
 ("`useradd -m bob` içindeki `-m` ne yapar?", ["Kullanıcıyı kilitler", "Posta kutusu açar", "Ev dizinini oluşturur", "Parolayı sıfırlar"], "`-m` `/home/bob` dizinini oluşturur ve `/etc/skel` içeriğini kopyalar."),
 ("Was bewirkt `-m` in `useradd -m bob`?", ["Sperrt den Benutzer", "Legt ein Postfach an", "Erstellt das Home-Verzeichnis", "Setzt das Passwort zurück"], "`-m` legt `/home/bob` an und kopiert den Inhalt von `/etc/skel`."),
 ("What does `-m` do in `useradd -m bob`?", ["Locks the user", "Creates a mailbox", "Creates the home directory", "Resets the password"], "`-m` creates `/home/bob` and copies the contents of `/etc/skel`.")),
Q(1,
 ("`passwd -l alice` ne yapar?", ["Hesabı siler", "Parolayı kilitler; SSH anahtarıyla giriş yine mümkün olabilir", "Parolayı süresiz yapar", "Kullanıcıyı oturumdan atar"], "Shadow'daki özetin başına `!` ekler; tam erişim kesmek için `usermod -e 1` veya kabuğu `nologin` yapmak gerekir."),
 ("Was bewirkt `passwd -l alice`?", ["Löscht das Konto", "Sperrt das Passwort; SSH-Key-Login kann weiter möglich sein", "Macht das Passwort unbegrenzt gültig", "Wirft den Benutzer aus der Sitzung"], "Setzt `!` vor den Hash in shadow; für vollständige Sperre `usermod -e 1` oder Shell `nologin`."),
 ("What does `passwd -l alice` do?", ["Deletes the account", "Locks the password; SSH key login may still work", "Makes the password never expire", "Kicks the user out of the session"], "It prefixes the shadow hash with `!`; to fully cut access use `usermod -e 1` or a `nologin` shell.")),
Q(3,
 ("`usermod -aG devs alice` ne yapar?", ["alice'in tüm gruplarını `devs` ile değiştirir", "alice'i siler", "`devs` grubunu siler", "alice'i mevcut gruplarına dokunmadan `devs`'e ekler"], "`-a` ile `-G` birlikte kullanılınca ek gruplar korunur; `-a` unutulursa liste ezilir."),
 ("Was macht `usermod -aG devs alice`?", ["Ersetzt alle Gruppen von alice durch `devs`", "Löscht alice", "Löscht die Gruppe `devs`", "Fügt alice zu `devs` hinzu, ohne andere Gruppen anzutasten"], "`-a` mit `-G` behält die übrigen Gruppen; ohne `-a` wird die Liste überschrieben."),
 ("What does `usermod -aG devs alice` do?", ["Replaces all of alice's groups with `devs`", "Deletes alice", "Deletes the `devs` group", "Adds alice to `devs` without touching her other groups"], "`-a` with `-G` keeps existing supplementary groups; without `-a` the list is overwritten.")),
Q(0,
 ("`chage -d 0 alice` ne sağlar?", ["Bir sonraki girişte parola değiştirmeyi zorunlu kılar", "Hesabı kilitler", "Parolayı siler", "Hesabı bugün sona erdirir"], "Son parola değişim tarihini 0 yaparak parolayı süresi dolmuş sayar; ilk girişte yeni parola istenir."),
 ("Was bewirkt `chage -d 0 alice`?", ["Erzwingt Passwortwechsel bei der nächsten Anmeldung", "Sperrt das Konto", "Löscht das Passwort", "Lässt das Konto heute enden"], "Setzt das letzte Änderungsdatum auf 0, das Passwort gilt als abgelaufen; beim Login wird ein neues verlangt."),
 ("What does `chage -d 0 alice` do?", ["Forces a password change at next login", "Locks the account", "Deletes the password", "Expires the account today"], "It sets the last-change date to 0 so the password counts as expired; a new one is required at login.")),
])

add_quiz('4.3', [
Q(1,
 ("`sudo -l` ne yapar?", ["Oturumu kapatır", "Geçerli kullanıcının sudo ile çalıştırabileceği komutları listeler", "sudoers dosyasını düzenler", "Sudo günlüğünü gösterir"], "`-l` (list) kullanıcının izinlerini gösterir; kural yazdıktan sonra sınamak için idealdir."),
 ("Was bewirkt `sudo -l`?", ["Beendet die Sitzung", "Listet die per sudo erlaubten Befehle des Benutzers", "Bearbeitet die sudoers-Datei", "Zeigt das sudo-Log"], "`-l` (list) zeigt die Rechte des Benutzers; ideal, um neue Regeln zu testen."),
 ("What does `sudo -l` do?", ["Logs out", "Lists the commands the current user may run via sudo", "Edits the sudoers file", "Shows the sudo log"], "`-l` (list) shows the user's privileges; ideal for testing a new rule.")),
Q(2,
 ("`alice ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx` kuralı ne verir?", ["alice'e tam root yetkisi", "alice'in sudo'yu hiç kullanamamasını", "alice'in yalnızca bu komutu parolasız çalıştırmasını", "Tüm kullanıcılara nginx yetkisi"], "Komut tam yolla sınırlandığı için en az yetki ilkesine uyar."),
 ("Was gewährt die Regel `alice ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx`?", ["Volle Root-Rechte für alice", "Dass alice sudo nicht nutzen darf", "Dass alice nur diesen Befehl ohne Passwort ausführt", "nginx-Rechte für alle Benutzer"], "Der Befehl ist per vollem Pfad begrenzt; das entspricht dem Least-Privilege-Prinzip."),
 ("What does `alice ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart nginx` grant?", ["Full root rights to alice", "That alice cannot use sudo", "That alice may run only this command without a password", "nginx rights to all users"], "The command is limited by full path, which follows least privilege.")),
Q(3,
 ("`su alice` ile `su - alice` arasındaki fark nedir?", ["Fark yoktur", "İkincisi root olur", "İlki parola sormaz", "İkincisi alice'in login ortamını (HOME, PATH) yükler"], "`-` login kabuğu başlatır; ortam değişkenleri ve çalışma dizini hedef kullanıcıya göre ayarlanır."),
 ("Worin unterscheiden sich `su alice` und `su - alice`?", ["Kein Unterschied", "Das zweite macht root", "Das erste fragt kein Passwort", "Das zweite lädt die Login-Umgebung von alice (HOME, PATH)"], "`-` startet eine Login-Shell; Umgebung und Arbeitsverzeichnis folgen dem Zielbenutzer."),
 ("What is the difference between `su alice` and `su - alice`?", ["None", "The second becomes root", "The first asks no password", "The second loads alice's login environment (HOME, PATH)"], "`-` starts a login shell; environment and working directory follow the target user.")),
Q(0,
 ("`/etc/sudoers.d/` altına dosya koymanın yararı nedir?", ["Ana dosyaya dokunmadan modüler kural eklenir; yine de `visudo -f` ile düzenlenmeli", "Sözdizimi denetimi gerekmez", "Kurallar yalnızca root için geçerli olur", "Dosya izinleri önemsizdir"], "Dosyalar ayrı yönetilir ama hatalı bir dosya sudo'yu bozabilir; `visudo -f` ile denetle, izin 0440 olsun."),
 ("Was ist der Vorteil von Dateien in `/etc/sudoers.d/`?", ["Modulare Regeln ohne die Hauptdatei anzufassen; trotzdem mit `visudo -f` bearbeiten", "Keine Syntaxprüfung nötig", "Regeln gelten nur für root", "Dateirechte sind egal"], "Regeln lassen sich getrennt verwalten, doch eine fehlerhafte Datei kann sudo lahmlegen; mit `visudo -f` prüfen, Modus 0440."),
 ("What is the benefit of files under `/etc/sudoers.d/`?", ["Modular rules without touching the main file; still edit with `visudo -f`", "No syntax check needed", "Rules apply only to root", "File permissions don't matter"], "Rules are managed separately, but a bad file can break sudo; check with `visudo -f`, mode 0440.")),
])
print('ok')
