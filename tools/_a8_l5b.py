import sys; sys.path.insert(0, 'tools')
from _a8lib import add_quiz

def Q(a, tr, de, en):
    return (a, {'tr': tr, 'de': de, 'en': en})

add_quiz('5.4', [
Q(1,
 ("Duraklatılmış işi arka planda çalışmaya devam ettiren komut hangisidir?", ["`fg %1`", "`bg %1`", "`nohup %1`", "`kill %1`"], "`bg` durdurulmuş işi arka planda sürdürür; `fg` ön plana getirir."),
 ("Welcher Befehl lässt einen angehaltenen Job im Hintergrund weiterlaufen?", ["`fg %1`", "`bg %1`", "`nohup %1`", "`kill %1`"], "`bg` setzt einen gestoppten Job im Hintergrund fort; `fg` holt ihn nach vorn."),
 ("Which command resumes a stopped job in the background?", ["`fg %1`", "`bg %1`", "`nohup %1`", "`kill %1`"], "`bg` resumes a stopped job in the background; `fg` brings it to the foreground.")),
Q(3,
 ("`sleep 100 &` komutundaki `&` ne yapar?", ["İşi sonlandırır", "Çıktıyı gizler", "İşi oturum kapansa da yaşatır", "Komutu arka planda başlatır"], "`&` işi arka planda başlatır; oturum kapanınca yaşaması için `nohup` gerekir."),
 ("Was bewirkt `&` in `sleep 100 &`?", ["Beendet den Job", "Blendet Ausgabe aus", "Hält den Job nach Logout am Leben", "Startet den Befehl im Hintergrund"], "`&` startet im Hintergrund; für Überleben nach Logout braucht man `nohup`."),
 ("What does `&` in `sleep 100 &` do?", ["Terminates the job", "Hides output", "Keeps the job alive after logout", "Starts the command in the background"], "`&` starts it in the background; surviving logout needs `nohup`.")),
Q(0,
 ("`jobs` çıktısında `+` işareti neyi gösterir?", ["Geçerli (varsayılan) işi", "Hatalı işi", "Root'a ait işi", "Arka plandaki tüm işleri"], "`+` varsayılan işi gösterir; `fg`/`bg` numara verilmezse ona uygulanır."),
 ("Was kennzeichnet `+` in der Ausgabe von `jobs`?", ["Den aktuellen (Standard-)Job", "Einen fehlerhaften Job", "Einen Job von root", "Alle Hintergrundjobs"], "`+` ist der Standardjob; `fg`/`bg` ohne Nummer wirken darauf."),
 ("What does the `+` mark in `jobs` output indicate?", ["The current (default) job", "A failed job", "A job owned by root", "All background jobs"], "`+` marks the default job; `fg`/`bg` without a number act on it.")),
Q(2,
 ("Başka bir terminalde çalışan sürece `fg` uygulanabilir mi?", ["Evet, PID ile", "Evet, root ise", "Hayır, `jobs` yalnızca o kabuğun işlerini bilir", "Evet, `jobs -a` ile"], "İş kontrolü kabuğa özeldir; başka terminaldeki süreç için `kill` gibi PID tabanlı araçlar gerekir."),
 ("Kann `fg` auf einen Prozess in einem anderen Terminal angewendet werden?", ["Ja, per PID", "Ja, als root", "Nein, `jobs` kennt nur Jobs dieser Shell", "Ja, mit `jobs -a`"], "Jobkontrolle ist shellspezifisch; für andere Terminals nutzt man PID-basierte Werkzeuge wie `kill`."),
 ("Can `fg` be used on a process running in another terminal?", ["Yes, by PID", "Yes, if root", "No, `jobs` only knows this shell's jobs", "Yes, with `jobs -a`"], "Job control is per shell; for other terminals use PID-based tools such as `kill`.")),
])

add_quiz('5.5', [
Q(2,
 ("Kurmadan önce paket bilgisini hangi komut gösterir (Debian)?", ["`apt list --all`", "`dpkg -r pkg`", "`apt show pkg`", "`apt clean pkg`"], "`apt show` ayrıntı, bağımlılık ve boyutu gösterir; RHEL'de karşılığı `dnf info`."),
 ("Welcher Befehl zeigt vor der Installation Paketinformationen (Debian)?", ["`apt list --all`", "`dpkg -r pkg`", "`apt show pkg`", "`apt clean pkg`"], "`apt show` zeigt Details, Abhängigkeiten und Größe; unter RHEL `dnf info`."),
 ("Which command shows package details before installing (Debian)?", ["`apt list --all`", "`dpkg -r pkg`", "`apt show pkg`", "`apt clean pkg`"], "`apt show` shows details, dependencies and size; on RHEL it is `dnf info`.")),
Q(0,
 ("Bir dosyanın hangi RPM paketine ait olduğunu hangi komut bulur?", ["`rpm -qf /yol/dosya`", "`rpm -ql dosya`", "`dnf clean dosya`", "`rpm -e dosya`"], "`rpm -qf` dosyadan pakete, `rpm -ql` paketten dosya listesine gider."),
 ("Welcher Befehl findet das RPM-Paket, zu dem eine Datei gehört?", ["`rpm -qf /pfad/datei`", "`rpm -ql datei`", "`dnf clean datei`", "`rpm -e datei`"], "`rpm -qf` geht von Datei zu Paket, `rpm -ql` von Paket zur Dateiliste."),
 ("Which command finds the RPM package that owns a file?", ["`rpm -qf /path/file`", "`rpm -ql file`", "`dnf clean file`", "`rpm -e file`"], "`rpm -qf` maps file to package, `rpm -ql` lists a package's files.")),
Q(3,
 ("`apt remove` ile `apt purge` arasındaki fark nedir?", ["Fark yoktur", "`purge` yalnızca bağımlılıkları siler", "`remove` kullanıcı verisini de siler", "`purge` yapılandırma dosyalarını da siler"], "`remove` paketi kaldırır ama `/etc` yapılandırmasını bırakır; `purge` onu da siler."),
 ("Was unterscheidet `apt remove` von `apt purge`?", ["Kein Unterschied", "`purge` löscht nur Abhängigkeiten", "`remove` löscht auch Benutzerdaten", "`purge` entfernt auch Konfigurationsdateien"], "`remove` lässt die Konfiguration in `/etc`; `purge` löscht sie ebenfalls."),
 ("What is the difference between `apt remove` and `apt purge`?", ["None", "`purge` removes only dependencies", "`remove` also deletes user data", "`purge` also removes configuration files"], "`remove` keeps config in `/etc`; `purge` deletes it too.")),
Q(1,
 ("`dpkg -i paket.deb` neyi yapmaz?", ["Paketi kurar", "Eksik bağımlılıkları kendiliğinden indirir", "Paketi veritabanına işler", "Paket dosyalarını açar"], "`dpkg` depo kullanmaz; bağımlılıkları çözmez. `apt install ./paket.deb` bunu yapar."),
 ("Was tut `dpkg -i paket.deb` nicht?", ["Das Paket installieren", "Fehlende Abhängigkeiten selbst herunterladen", "Das Paket in die Datenbank eintragen", "Paketdateien entpacken"], "`dpkg` nutzt keine Repos und löst keine Abhängigkeiten; `apt install ./paket.deb` tut das."),
 ("What does `dpkg -i package.deb` NOT do?", ["Install the package", "Download missing dependencies itself", "Record the package in the database", "Unpack package files"], "`dpkg` uses no repositories and does not resolve dependencies; `apt install ./package.deb` does.")),
])

add_quiz('5.6', [
Q(2,
 ("Bir servisin çalışıp çalışmadığını ve son log satırlarını hangi komut verir?", ["`systemctl enable ssh`", "`journalctl -k`", "`systemctl status ssh`", "`systemctl list-units`"], "`status` durum, PID ve son journal satırlarını birlikte gösterir."),
 ("Welcher Befehl zeigt, ob ein Dienst läuft, samt letzten Logzeilen?", ["`systemctl enable ssh`", "`journalctl -k`", "`systemctl status ssh`", "`systemctl list-units`"], "`status` zeigt Zustand, PID und letzte Journalzeilen."),
 ("Which command shows whether a service runs, plus recent log lines?", ["`systemctl enable ssh`", "`journalctl -k`", "`systemctl status ssh`", "`systemctl list-units`"], "`status` shows state, PID and the latest journal lines.")),
Q(0,
 ("`journalctl -u ssh -f` ne yapar?", ["ssh unit'inin loglarını canlı izler", "ssh'ı yeniden başlatır", "Logları siler", "Yalnızca çekirdek mesajlarını gösterir"], "`-u` unit seçer, `-f` yeni girdileri takip eder (`tail -f` gibi)."),
 ("Was macht `journalctl -u ssh -f`?", ["Verfolgt die Logs der ssh-Unit live", "Startet ssh neu", "Löscht Logs", "Zeigt nur Kernelmeldungen"], "`-u` wählt die Unit, `-f` folgt neuen Einträgen (wie `tail -f`)."),
 ("What does `journalctl -u ssh -f` do?", ["Follows the ssh unit's logs live", "Restarts ssh", "Deletes logs", "Shows only kernel messages"], "`-u` selects the unit, `-f` follows new entries (like `tail -f`).")),
Q(3,
 ("Journal'ı yeniden başlatmalar arasında kalıcı yapmak için ne gerekir?", ["`journalctl --keep`", "`systemctl enable journal`", "Hiçbir şey, zaten kalıcıdır", "`/var/log/journal` dizini veya `Storage=persistent`"], "Dizin yoksa journal `/run` altında tutulur ve açılışta silinir; dizin oluşturmak ya da `Storage=persistent` yeter."),
 ("Was macht das Journal über Neustarts hinweg persistent?", ["`journalctl --keep`", "`systemctl enable journal`", "Nichts, es ist immer persistent", "Verzeichnis `/var/log/journal` oder `Storage=persistent`"], "Fehlt das Verzeichnis, liegt das Journal in `/run` und geht beim Neustart verloren."),
 ("What makes the journal persistent across reboots?", ["`journalctl --keep`", "`systemctl enable journal`", "Nothing, it is always persistent", "A `/var/log/journal` directory or `Storage=persistent`"], "Without the directory the journal lives in `/run` and is lost at reboot.")),
Q(1,
 ("`systemctl mask` ne yapar?", ["Servisi gizler", "Unit'in hiçbir şekilde başlatılmasını engeller", "Logları maskeler", "Servisi yeniden yükler"], "`mask` unit'i `/dev/null`'a bağlar; elle ya da bağımlılıkla başlatılamaz."),
 ("Was bewirkt `systemctl mask`?", ["Versteckt den Dienst", "Verhindert jeden Start der Unit", "Maskiert Logs", "Lädt den Dienst neu"], "`mask` verlinkt die Unit auf `/dev/null`; sie lässt sich weder manuell noch als Abhängigkeit starten."),
 ("What does `systemctl mask` do?", ["Hides the service", "Prevents the unit from being started at all", "Masks logs", "Reloads the service"], "`mask` links the unit to `/dev/null`; it cannot be started manually or as a dependency.")),
])
print('ok')
