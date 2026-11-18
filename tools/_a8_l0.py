import sys; sys.path.insert(0, 'tools')
from _a8lib import add_quiz

add_quiz('0.1', [
(2, {
 'tr': ("Çalışan çekirdeğin sürümünü hangi komut gösterir?", ["hostname", "whoami", "uname -r", "pwd"], "`uname -r` çekirdek sürümünü yazar; `hostname` makine adını, `whoami` kullanıcıyı gösterir."),
 'de': ("Welcher Befehl zeigt die Version des laufenden Kernels?", ["hostname", "whoami", "uname -r", "pwd"], "`uname -r` gibt die Kernel-Version aus; `hostname` den Rechnernamen, `whoami` den Benutzer."),
 'en': ("Which command shows the version of the running kernel?", ["hostname", "whoami", "uname -r", "pwd"], "`uname -r` prints the kernel release; `hostname` shows the machine name, `whoami` the user.")}),
(0, {
 'tr': ("`/etc/os-release` içinde `ID_LIKE=debian` görüyorsun. Hangi paket aracı muhtemelen vardır?", ["apt", "dnf", "pacman", "rpm-ostree"], "Debian ailesi `apt`/`dpkg` kullanır; `dnf` RHEL ailesine aittir."),
 'de': ("In `/etc/os-release` steht `ID_LIKE=debian`. Welches Paketwerkzeug ist wahrscheinlich vorhanden?", ["apt", "dnf", "pacman", "rpm-ostree"], "Die Debian-Familie nutzt `apt`/`dpkg`; `dnf` gehört zur RHEL-Familie."),
 'en': ("You see `ID_LIKE=debian` in `/etc/os-release`. Which package tool is most likely present?", ["apt", "dnf", "pacman", "rpm-ostree"], "The Debian family uses `apt`/`dpkg`; `dnf` belongs to the RHEL family.")}),
(3, {
 'tr': ("Sistem genelindeki yapılandırma dosyaları hangi dizinde durur?", ["/home", "/var", "/usr", "/etc"], "`/etc` yapılandırma, `/home` kullanıcı verisi, `/var` değişken veri (log vb.), `/usr` programlar içindir."),
 'de': ("In welchem Verzeichnis liegen die systemweiten Konfigurationsdateien?", ["/home", "/var", "/usr", "/etc"], "`/etc` enthält Konfiguration, `/home` Benutzerdaten, `/var` veränderliche Daten (Logs), `/usr` Programme."),
 'en': ("Which directory holds the system-wide configuration files?", ["/home", "/var", "/usr", "/etc"], "`/etc` holds configuration, `/home` user data, `/var` variable data (logs), `/usr` programs.")}),
(1, {
 'tr': ("Linux çekirdeği hangi lisansla dağıtılır?", ["Kapalı kaynak, ticari lisans", "GNU GPL (v2)", "Yalnızca Windows EULA", "Lisanssız, kamu malı"], "Çekirdek GPLv2 ile özgürdür: kaynak kodu görülebilir, değiştirilebilir ve aynı lisansla dağıtılır."),
 'de': ("Unter welcher Lizenz steht der Linux-Kernel?", ["Closed Source, kommerzielle Lizenz", "GNU GPL (v2)", "Nur Windows-EULA", "Lizenzfrei, gemeinfrei"], "Der Kernel ist unter GPLv2 frei: Quellcode einsehbar, änderbar und unter gleicher Lizenz weitergebbar."),
 'en': ("Under which license is the Linux kernel distributed?", ["Closed source, commercial license", "GNU GPL (v2)", "Windows EULA only", "No license, public domain"], "The kernel is free under GPLv2: source is viewable, modifiable and redistributed under the same license.")}),
])

add_quiz('0.2', [
(1, {
 'tr': ("İndirdiğin ISO'nun SHA-256 toplamını Linux'ta nasıl hesaplarsın?", ["cat dosya.iso", "sha256sum dosya.iso", "ls -l dosya.iso", "uname dosya.iso"], "`sha256sum` özeti hesaplar; sonucu sitedeki değerle karşılaştır."),
 'de': ("Wie berechnest du unter Linux die SHA-256-Summe einer heruntergeladenen ISO?", ["cat datei.iso", "sha256sum datei.iso", "ls -l datei.iso", "uname datei.iso"], "`sha256sum` berechnet die Prüfsumme; vergleiche sie mit dem Wert der Webseite."),
 'en': ("How do you compute the SHA-256 sum of a downloaded ISO on Linux?", ["cat file.iso", "sha256sum file.iso", "ls -l file.iso", "uname file.iso"], "`sha256sum` computes the digest; compare it with the value on the download page.")}),
(3, {
 'tr': ("Hangi ağ modunda VM yerel ağdan kendi IP adresini alır ve diğer cihazlarla aynı ağda görünür?", ["NAT", "Host-only", "Internal", "Bridged"], "Bridged, VM'i fiziksel ağa köprüler; NAT'ta VM ana makinenin arkasında gizlenir."),
 'de': ("In welchem Netzwerkmodus erhält die VM eine eigene IP im lokalen Netz und ist wie andere Geräte sichtbar?", ["NAT", "Host-only", "Internal", "Bridged"], "Bridged verbindet die VM mit dem physischen Netz; bei NAT liegt sie hinter dem Host."),
 'en': ("In which network mode does the VM get its own LAN IP and appear like any other device?", ["NAT", "Host-only", "Internal", "Bridged"], "Bridged attaches the VM to the physical network; with NAT it sits behind the host.")}),
(0, {
 'tr': ("Ana bilgisayardan VM'e SSH ile bağlanmanın bir avantajı nedir?", ["Tanıdık terminal, kopyala-yapıştır ve VM penceresi olmadan çalışma", "İşlemciyi hızlandırır", "ISO'yu gereksiz kılar", "Snapshot almak için zorunludur"], "SSH rahat bir terminal ve kolay kopyalama sağlar; hız veya snapshot ile ilgisi yoktur."),
 'de': ("Was ist ein Vorteil, sich vom Host per SSH mit der VM zu verbinden?", ["Gewohntes Terminal, Copy & Paste und Arbeiten ohne VM-Fenster", "Beschleunigt die CPU", "Macht die ISO überflüssig", "Ist für Snapshots Pflicht"], "SSH bietet ein komfortables Terminal und einfaches Kopieren; mit Tempo oder Snapshots hat es nichts zu tun."),
 'en': ("What is one advantage of connecting to the VM over SSH from the host?", ["Familiar terminal, copy-paste and working without the VM window", "It speeds up the CPU", "It makes the ISO unnecessary", "It is required for snapshots"], "SSH gives a comfortable terminal and easy copying; it has nothing to do with speed or snapshots.")}),
(2, {
 'tr': ("Snapshot'a geri döndüğünde, snapshot'tan sonra yaptığın değişikliklere ne olur?", ["Korunur", "Ana bilgisayara taşınır", "Atılır", "Şifrelenir"], "Geri dönmek VM'i snapshot anındaki duruma getirir; sonraki değişiklikler kaybolur."),
 'de': ("Was passiert beim Zurücksetzen auf einen Snapshot mit Änderungen, die danach gemacht wurden?", ["Sie bleiben erhalten", "Sie wandern auf den Host", "Sie werden verworfen", "Sie werden verschlüsselt"], "Die Wiederherstellung bringt die VM in den Zustand des Snapshots; spätere Änderungen gehen verloren."),
 'en': ("When you roll back to a snapshot, what happens to changes made after it was taken?", ["They are kept", "They move to the host", "They are discarded", "They are encrypted"], "Rolling back restores the VM to the snapshot state; later changes are lost.")}),
])

add_quiz('0.3', [
(1, {
 'tr': ("`whoami` ne yazar?", ["Makine adını", "Geçerli kullanıcı adını", "Çalışma dizinini", "Çekirdek sürümünü"], "`whoami` etkin kullanıcıyı gösterir; makine adı için `hostname`, dizin için `pwd`."),
 'de': ("Was gibt `whoami` aus?", ["Den Rechnernamen", "Den aktuellen Benutzernamen", "Das Arbeitsverzeichnis", "Die Kernel-Version"], "`whoami` zeigt den aktiven Benutzer; `hostname` den Rechnernamen, `pwd` das Verzeichnis."),
 'en': ("What does `whoami` print?", ["The machine name", "The current user name", "The working directory", "The kernel version"], "`whoami` shows the active user; use `hostname` for the machine and `pwd` for the directory.")}),
(3, {
 'tr': ("`man` sayfasından hangi tuşla çıkarsın?", ["Esc", "Enter", "Ctrl+D", "q"], "`man` bir sayfalayıcı kullanır; `q` çıkar, `/kelime` arar."),
 'de': ("Mit welcher Taste verlässt du eine `man`-Seite?", ["Esc", "Enter", "Ctrl+D", "q"], "`man` nutzt einen Pager; `q` beendet, `/wort` sucht."),
 'en': ("Which key quits a `man` page?", ["Esc", "Enter", "Ctrl+D", "q"], "`man` uses a pager; `q` quits and `/word` searches.")}),
(0, {
 'tr': ("Terminalde ↑ (yukarı ok) tuşuna basınca ne olur?", ["Önceki komut satıra gelir", "Ekran temizlenir", "Üst dizine çıkılır", "Oturum kapanır"], "Ok tuşları komut geçmişinde gezinir; `history` tüm listeyi gösterir."),
 'de': ("Was passiert im Terminal beim Drücken von ↑ (Pfeil hoch)?", ["Der vorherige Befehl erscheint in der Zeile", "Der Bildschirm wird geleert", "Es geht ins übergeordnete Verzeichnis", "Die Sitzung endet"], "Pfeiltasten blättern durch die Befehlshistorie; `history` zeigt die ganze Liste."),
 'en': ("What happens when you press ↑ (up arrow) in the terminal?", ["The previous command appears on the line", "The screen is cleared", "You go to the parent directory", "The session ends"], "Arrow keys browse the command history; `history` lists it all.")}),
(2, {
 'tr': ("`history` komutu ne yapar?", ["Ekranı temizler", "Disk kullanımını gösterir", "Daha önce yazdığın komutları listeler", "Kullanıcıları listeler"], "`history` numaralı komut geçmişini gösterir; `!N` ile N. komutu yeniden çalıştırabilirsin."),
 'de': ("Was macht der Befehl `history`?", ["Leert den Bildschirm", "Zeigt die Festplattenbelegung", "Listet zuvor eingegebene Befehle auf", "Listet Benutzer auf"], "`history` zeigt die nummerierte Befehlshistorie; mit `!N` führst du Befehl N erneut aus."),
 'en': ("What does the `history` command do?", ["Clears the screen", "Shows disk usage", "Lists commands you typed earlier", "Lists users"], "`history` shows the numbered command history; `!N` re-runs command N.")}),
])
