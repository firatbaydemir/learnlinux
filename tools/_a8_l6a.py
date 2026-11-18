import sys; sys.path.insert(0, 'tools')
from _a8lib import add_quiz

def Q(a, tr, de, en):
    return (a, {'tr': tr, 'de': de, 'en': en})

add_quiz('6.1', [
Q(1,
 ("`ip -br a` neyi gösterir?", ["Yalnızca yönlendirme tablosunu", "Arayüzleri ve adreslerini kısa tabloda", "Açık portları", "DNS sunucularını"], "`-br` (brief) arayüz durumu ve IP adreslerini tek satırda özetler."),
 ("Was zeigt `ip -br a`?", ["Nur die Routing-Tabelle", "Schnittstellen und Adressen als Kurztabelle", "Offene Ports", "DNS-Server"], "`-br` (brief) fasst Schnittstellenstatus und IP-Adressen einzeilig zusammen."),
 ("What does `ip -br a` show?", ["Only the routing table", "Interfaces and addresses in a brief table", "Open ports", "DNS servers"], "`-br` (brief) summarises interface state and IP addresses on one line each.")),
Q(3,
 ("`ss -tulpn` içindeki `-p` seçeneği ne ekler?", ["Protokol adını", "Port numarasını", "Paket sayacını", "Dinleyen süreci (PID/ad)"], "`-p` soketi açan süreci gösterir; başka kullanıcıların süreçleri için root gerekir."),
 ("Was fügt `-p` in `ss -tulpn` hinzu?", ["Den Protokollnamen", "Die Portnummer", "Paketzähler", "Den lauschenden Prozess (PID/Name)"], "`-p` zeigt den Prozess hinter dem Socket; für fremde Prozesse ist root nötig."),
 ("What does `-p` in `ss -tulpn` add?", ["The protocol name", "The port number", "Packet counters", "The listening process (PID/name)"], "`-p` shows the process owning the socket; other users' processes need root.")),
Q(0,
 ("Bir hizmet `0.0.0.0:80` yerine `127.0.0.1:80` dinliyorsa ne olur?", ["Yalnızca yerel makineden erişilir", "Herkes erişir", "Hizmet başlamaz", "Yalnızca IPv6 çalışır"], "`127.0.0.1` loopback'tir; dışarıdan gelen bağlantılar kabul edilmez."),
 ("Was passiert, wenn ein Dienst `127.0.0.1:80` statt `0.0.0.0:80` bindet?", ["Nur lokal erreichbar", "Für alle erreichbar", "Dienst startet nicht", "Nur IPv6 funktioniert"], "`127.0.0.1` ist Loopback; Verbindungen von außen werden nicht angenommen."),
 ("What happens if a service listens on `127.0.0.1:80` instead of `0.0.0.0:80`?", ["Reachable from the local host only", "Reachable by everyone", "The service fails to start", "Only IPv6 works"], "`127.0.0.1` is loopback; connections from outside are not accepted.")),
Q(2,
 ("`ip route` çıktısında `default via 10.0.0.1 dev eth0` ne anlama gelir?", ["eth0 arayüzü kapalıdır", "10.0.0.1 yerel adrestir", "Bilinmeyen hedefler 10.0.0.1 geçidine gider", "DNS sunucusu 10.0.0.1'dir"], "`default` satırı başka hiçbir yol eşleşmediğinde kullanılan geçittir."),
 ("Was bedeutet `default via 10.0.0.1 dev eth0` in `ip route`?", ["eth0 ist down", "10.0.0.1 ist die lokale Adresse", "Unbekannte Ziele gehen über Gateway 10.0.0.1", "10.0.0.1 ist der DNS-Server"], "Die `default`-Zeile gilt, wenn keine andere Route passt."),
 ("What does `default via 10.0.0.1 dev eth0` in `ip route` mean?", ["eth0 is down", "10.0.0.1 is the local address", "Unknown destinations go via gateway 10.0.0.1", "10.0.0.1 is the DNS server"], "The `default` line is used when no other route matches.")),
])

add_quiz('6.2', [
Q(2,
 ("`ls -Z` ne gösterir?", ["Dosya boyutunu sıkıştırılmış olarak", "Sahiplik bilgisini", "SELinux bağlamını (etiketini)", "ACL listesini"], "`-Z` user:role:type:level biçiminde SELinux bağlamını gösterir; `ps -Z` süreçler için aynısını yapar."),
 ("Was zeigt `ls -Z`?", ["Komprimierte Dateigröße", "Besitzerinformationen", "Den SELinux-Kontext (Label)", "Die ACL-Liste"], "`-Z` zeigt den Kontext als user:role:type:level; `ps -Z` tut dasselbe für Prozesse."),
 ("What does `ls -Z` show?", ["Compressed file size", "Ownership info", "The SELinux context (label)", "The ACL list"], "`-Z` shows the context as user:role:type:level; `ps -Z` does the same for processes.")),
Q(0,
 ("Hangi komut dosyanın etiketini varsayılan politikaya göre sıfırlar?", ["`restorecon -Rv /srv/web`", "`chmod -R 755 /srv/web`", "`setenforce 0`", "`chcon -u root /srv/web`"], "`restorecon` etiketi dosya bağlamı politikasına göre geri yükler."),
 ("Welcher Befehl setzt das Label einer Datei gemäß Standardrichtlinie zurück?", ["`restorecon -Rv /srv/web`", "`chmod -R 755 /srv/web`", "`setenforce 0`", "`chcon -u root /srv/web`"], "`restorecon` stellt das Label gemäß Dateikontext-Richtlinie wieder her."),
 ("Which command resets a file's label to the policy default?", ["`restorecon -Rv /srv/web`", "`chmod -R 755 /srv/web`", "`setenforce 0`", "`chcon -u root /srv/web`"], "`restorecon` restores the label from the file-context policy.")),
Q(3,
 ("`setenforce 0` sonucunda SELinux hangi moda geçer?", ["Disabled", "Enforcing", "Kapanır ve silinir", "Permissive"], "`setenforce 0` anlık Permissive moduna alır (ihlaller loglanır, engellenmez); yeniden başlatmada yapılandırma dosyası geçerlidir."),
 ("In welchen Modus wechselt SELinux nach `setenforce 0`?", ["Disabled", "Enforcing", "Wird entfernt", "Permissive"], "`setenforce 0` setzt sofort Permissive (nur Logging); nach Neustart gilt die Konfigurationsdatei."),
 ("Which mode does SELinux switch to after `setenforce 0`?", ["Disabled", "Enforcing", "It is removed", "Permissive"], "`setenforce 0` switches to Permissive immediately (log only); after reboot the config file applies.")),
Q(1,
 ("AVC reddi kayıtlarını nerede ararsın?", ["`/etc/selinux/config`", "`/var/log/audit/audit.log` (`ausearch -m avc`)", "`/proc/selinux`", "`/etc/passwd`"], "Reddedilen erişimler audit alt sisteminde `type=AVC` olarak kaydedilir."),
 ("Wo suchst du AVC-Denials?", ["`/etc/selinux/config`", "`/var/log/audit/audit.log` (`ausearch -m avc`)", "`/proc/selinux`", "`/etc/passwd`"], "Verweigerte Zugriffe stehen im Audit-Subsystem als `type=AVC`."),
 ("Where do you look for AVC denials?", ["`/etc/selinux/config`", "`/var/log/audit/audit.log` (`ausearch -m avc`)", "`/proc/selinux`", "`/etc/passwd`"], "Denied accesses are recorded by the audit subsystem as `type=AVC`.")),
])

add_quiz('6.3', [
Q(0,
 ("`firewall-cmd --get-active-zones` ne listeler?", ["Arayüz/kaynak atanmış etkin zone'ları", "Tüm tanımlı zone'ları", "Açık portları", "Reddedilen paketleri"], "Yalnızca en az bir arayüz veya kaynağı olan zone'lar listelenir."),
 ("Was listet `firewall-cmd --get-active-zones`?", ["Aktive Zonen mit Schnittstellen/Quellen", "Alle definierten Zonen", "Offene Ports", "Verworfene Pakete"], "Nur Zonen mit mindestens einer Schnittstelle oder Quelle erscheinen."),
 ("What does `firewall-cmd --get-active-zones` list?", ["Zones with assigned interfaces/sources", "All defined zones", "Open ports", "Dropped packets"], "Only zones with at least one interface or source are listed.")),
Q(2,
 ("`firewall-cmd --permanent --add-port=8080/tcp` sonrası kural ne zaman etkinleşir?", ["Hemen", "Hiçbir zaman", "`--reload` veya yeniden başlatmadan sonra", "Yalnızca `ufw` ile"], "`--permanent` yalnızca kalıcı yapılandırmayı değiştirir; runtime için `--reload` gerekir."),
 ("Wann wird die Regel nach `firewall-cmd --permanent --add-port=8080/tcp` aktiv?", ["Sofort", "Nie", "Nach `--reload` oder Neustart", "Nur mit `ufw`"], "`--permanent` ändert nur die dauerhafte Konfiguration; für Runtime ist `--reload` nötig."),
 ("When does the rule take effect after `firewall-cmd --permanent --add-port=8080/tcp`?", ["Immediately", "Never", "After `--reload` or reboot", "Only with `ufw`"], "`--permanent` only changes the persistent config; runtime needs `--reload`.")),
Q(1,
 ("Ubuntu'da SSH ile bağlıyken güvenli ufw sırası hangisidir?", ["`ufw enable`, sonra `ufw allow ssh`", "`ufw allow ssh`, sonra `ufw enable`", "`ufw reset`, sonra `ufw enable`", "`ufw deny all`, sonra `ufw enable`"], "Önce SSH'a izin ver; aksi halde varsayılan reddet kuralı oturumunu keser."),
 ("Welche ufw-Reihenfolge ist per SSH sicher?", ["`ufw enable`, dann `ufw allow ssh`", "`ufw allow ssh`, dann `ufw enable`", "`ufw reset`, dann `ufw enable`", "`ufw deny all`, dann `ufw enable`"], "Erst SSH erlauben; sonst kappt die Default-Deny-Regel die Sitzung."),
 ("Which ufw order is safe over SSH?", ["`ufw enable`, then `ufw allow ssh`", "`ufw allow ssh`, then `ufw enable`", "`ufw reset`, then `ufw enable`", "`ufw deny all`, then `ufw enable`"], "Allow SSH first; otherwise the default-deny rule cuts your session.")),
Q(3,
 ("Çalışma zamanındaki geçici kuralı kalıcı yapmanın doğru yolu hangisidir?", ["`firewall-cmd --reload`", "`systemctl enable firewalld`", "`firewall-cmd --panic-on`", "`firewall-cmd --runtime-to-permanent`"], "`--reload` runtime'ı kalıcıdan yeniden yükler (geçici kuralı siler); runtime'ı kalıcıya kaydeden `--runtime-to-permanent`'tır."),
 ("Wie macht man eine Runtime-Regel dauerhaft?", ["`firewall-cmd --reload`", "`systemctl enable firewalld`", "`firewall-cmd --panic-on`", "`firewall-cmd --runtime-to-permanent`"], "`--reload` lädt Runtime aus der dauerhaften Konfiguration (verwirft Temporäres); `--runtime-to-permanent` speichert."),
 ("What is the right way to make a runtime rule permanent?", ["`firewall-cmd --reload`", "`systemctl enable firewalld`", "`firewall-cmd --panic-on`", "`firewall-cmd --runtime-to-permanent`"], "`--reload` reloads runtime from permanent (dropping temporary rules); `--runtime-to-permanent` saves it.")),
])
print('ok')
