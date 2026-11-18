import re, json
# (modül, bölüm id, kartlar[tr,de,en])
def C(cmd, ex, tr, de, en):
    return dict(cmd=cmd, ex=ex, tr=tr, de=de, en=en)
DATA = {
 ('2.9', 'mount'): [
  C('mkswap', 'sudo mkswap /swapfile',
    ('Bir dosyayı veya bölümü takas (swap) alanı olarak biçimlendirir.', 'Swap alanı eklerken; önce `dd`/`fallocate` ile dosya, `chmod 600` ile izin.', 'RAM dolduğunda çekirdeğin az kullanılan sayfaları diske atabilmesi için.'),
    ('Formatiert eine Datei oder Partition als Swap-Bereich.', 'Beim Hinzufügen von Swap; vorher Datei anlegen und `chmod 600` setzen.', 'Damit der Kernel bei vollem RAM selten genutzte Seiten auslagern kann.'),
    ('Formats a file or partition as swap space.', 'When adding swap; first create the file and set `chmod 600`.', 'Lets the kernel move rarely used pages to disk when RAM is full.')),
  C('swapon', 'swapon --show',
    ('Swap alanını etkinleştirir; `--show` etkin swap alanlarını listeler.', 'Swap eklemeden sonra etkinleştirmek veya mevcut swap durumunu görmek için.', 'Kalıcı olması için `/etc/fstab` kaydı gerekir; `swapoff` alanı devreden çıkarır.'),
    ('Aktiviert Swap; `--show` listet aktive Swap-Bereiche.', 'Nach dem Anlegen zum Aktivieren oder um den Swap-Status zu sehen.', 'Dauerhaft nur mit Eintrag in `/etc/fstab`; `swapoff` deaktiviert.'),
    ('Enables swap; `--show` lists active swap areas.', 'After creating swap to enable it, or to check swap status.', 'Persistence needs an `/etc/fstab` entry; `swapoff` disables it.')),
 ],
 ('4.5', 'recipe'): [
  C('lsattr', 'lsattr file.txt',
    ('Dosya özniteliklerini (ör. `i` değiştirilemez, `a` yalnızca ekleme) listeler.', 'Root bile silemiyorsa izinlerden önce öznitelikleri kontrol etmek için.', 'İzin bitleri (rwx) ile öznitelikler ayrı mekanizmalardır.'),
    ('Listet Dateiattribute (z. B. `i` unveränderlich, `a` nur anhängen).', 'Wenn selbst root nicht löschen kann: erst Attribute prüfen.', 'Rechtebits (rwx) und Attribute sind getrennte Mechanismen.'),
    ('Lists file attributes (e.g. `i` immutable, `a` append-only).', 'When even root cannot delete a file, check attributes before permissions.', 'Permission bits (rwx) and attributes are separate mechanisms.')),
  C('chattr', 'sudo chattr +i file.txt',
    ('Dosya özniteliğini değiştirir; `+i` dosyayı değiştirilemez ve silinemez yapar.', 'Kritik bir dosyayı kazara değişikliğe karşı korumak için (ext4/xfs).', 'Geri almak için `sudo chattr -i dosya`.'),
    ('Ändert Dateiattribute; `+i` macht eine Datei unveränderlich und nicht löschbar.', 'Um kritische Dateien vor versehentlichen Änderungen zu schützen (ext4/xfs).', 'Rückgängig mit `sudo chattr -i datei`.'),
    ('Changes file attributes; `+i` makes a file immutable and undeletable.', 'To protect a critical file from accidental changes (ext4/xfs).', 'Undo with `sudo chattr -i file`.')),
 ],
 ('5.1', 'proc'): [
  C('lsof', 'sudo lsof -i :80',
    ('Açık dosyaları ve bu dosyaları açan süreçleri listeler; `-i :80` 80 portunu kullananı gösterir.', 'Bir port, silinemeyen dosya veya umount edilemeyen disk için kimin kullandığını bulmak için.', 'Linux’ta soket ve aygıt da dosyadır; bu yüzden lsof ağı da gösterir.'),
    ('Listet offene Dateien und die zugehörigen Prozesse; `-i :80` zeigt, wer Port 80 nutzt.', 'Um bei belegtem Port, nicht löschbarer Datei oder nicht aushängbarem Datenträger den Verursacher zu finden.', 'Sockets und Geräte sind unter Linux auch Dateien, daher zeigt lsof auch Netzwerk.'),
    ('Lists open files and the processes holding them; `-i :80` shows who uses port 80.', 'To find who holds a busy port, an undeletable file or a device that will not unmount.', 'Sockets and devices are files on Linux, so lsof also shows network use.')),
  C('fuser', 'fuser -v /var/log/syslog',
    ('Bir dosya, dizin veya portu kullanan süreçlerin PID’lerini gösterir.', '`umount` “target is busy” verdiğinde: `fuser -vm /mnt/disk`.', '`fuser -k` süreçleri öldürür; hedefi doğrulamadan kullanma.'),
    ('Zeigt PIDs der Prozesse, die eine Datei, ein Verzeichnis oder einen Port nutzen.', 'Bei `umount`-Fehler „target is busy“: `fuser -vm /mnt/disk`.', '`fuser -k` beendet Prozesse; nicht ohne Prüfung des Ziels verwenden.'),
    ('Shows PIDs of processes using a file, directory or port.', 'When `umount` says "target is busy": `fuser -vm /mnt/disk`.', '`fuser -k` kills processes; do not use it without verifying the target.')),
 ],
 ('1.2', 'host'): [
  C('lsmod', 'lsmod | head -n 5',
    ('Yüklü çekirdek modüllerini listeler.', 'Bir sürücünün (ör. `kvm`, `e1000`) yüklü olup olmadığını görmek için.', 'Modül, çekirdeğin çalışırken yüklenen parçasıdır.'),
    ('Listet geladene Kernelmodule.', 'Um zu prüfen, ob ein Treiber (z. B. `kvm`, `e1000`) geladen ist.', 'Ein Modul ist ein zur Laufzeit ladbarer Teil des Kernels.'),
    ('Lists loaded kernel modules.', 'To check whether a driver (e.g. `kvm`, `e1000`) is loaded.', 'A module is a part of the kernel loaded at runtime.')),
  C('modprobe', 'sudo modprobe dummy',
    ('Çekirdek modülünü bağımlılıklarıyla yükler; `-r` kaldırır.', 'Bir sürücüyü elle yüklemek veya denemek için (yönetici yetkisi gerekir).', 'Kalıcı yükleme `/etc/modules-load.d/` ile yapılır; `modprobe` ayarları `/etc/modprobe.d/` altındadır.'),
    ('Lädt ein Kernelmodul samt Abhängigkeiten; `-r` entfernt es.', 'Zum manuellen Laden oder Testen eines Treibers (root nötig).', 'Dauerhaft über `/etc/modules-load.d/`; Optionen in `/etc/modprobe.d/`.'),
    ('Loads a kernel module with its dependencies; `-r` removes it.', 'To load or test a driver by hand (needs root).', 'Persist via `/etc/modules-load.d/`; options live in `/etc/modprobe.d/`.')),
  C('sysctl', 'sysctl net.ipv4.ip_forward',
    ('Çekirdek parametrelerini okur ve değiştirir (`/proc/sys` üzerinden).', 'Ağ yönlendirme, `vm.swappiness` gibi ayarları görmek için; `sysctl -a` hepsini listeler.', '`sysctl -w` geçicidir; kalıcı için `/etc/sysctl.d/*.conf` dosyasına yaz.'),
    ('Liest und ändert Kernelparameter (über `/proc/sys`).', 'Um Einstellungen wie IP-Forwarding oder `vm.swappiness` zu sehen; `sysctl -a` listet alle.', '`sysctl -w` ist temporär; dauerhaft in `/etc/sysctl.d/*.conf` eintragen.'),
    ('Reads and changes kernel parameters (via `/proc/sys`).', 'To view settings such as IP forwarding or `vm.swappiness`; `sysctl -a` lists all.', '`sysctl -w` is temporary; persist it in `/etc/sysctl.d/*.conf`.')),
 ],
}
def j(s): return json.dumps(s, ensure_ascii=False)
for (m, sec), cards in DATA.items():
    for li, lang in enumerate(['tr', 'de', 'en']):
        p = f'content/m{m}/{lang}.json'
        t = open(p, encoding='utf-8', newline='').read()
        if all(('"cmd": ' + j(c['cmd']) in t or '"cmd":' + j(c['cmd']) in t) for c in cards):
            continue
        d = json.loads(t)
        s = [x for x in d['sections'] if x['id'] == sec][0]
        assert 'commands' in s, (m, sec)
        nl = '\r\n'
        objs = ''
        for c in cards:
            w, wh, wy = c[lang]
            objs += '{"cmd":%s,"what":%s,"where":%s,"why":%s,"example":%s,"nosim":true},' % (j(c['cmd']), j(w), j(wh), j(wy), j(c['ex']))
        mt = re.search(r'"id"\s*:\s*"%s".*?"commands"\s*:\s*\[' % re.escape(sec), t, re.S)
        assert mt, (m, sec, lang)
        t = t[:mt.end()] + objs + t[mt.end():]
        json.loads(t)
        open(p, 'w', encoding='utf-8', newline='').write(t)
print('ok')
