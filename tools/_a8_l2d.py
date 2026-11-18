import sys; sys.path.insert(0, 'tools')
from _a8lib import add_quiz

def Q(a, tr, de, en):
    return (a, {'tr': tr, 'de': de, 'en': en})

add_quiz('2.10', [
Q(2,
 ("SSH'ta varsayılan port nedir?", ["21", "80", "22", "443"], "SSH varsayılan olarak TCP 22 kullanır; farklı port için `ssh -p PORT`, `scp -P PORT` (büyük P)."),
 ("Welcher Standardport gilt für SSH?", ["21", "80", "22", "443"], "SSH nutzt standardmäßig TCP 22; anderer Port mit `ssh -p PORT`, `scp -P PORT` (großes P)."),
 ("What is the default SSH port?", ["21", "80", "22", "443"], "SSH uses TCP 22 by default; for another port use `ssh -p PORT`, `scp -P PORT` (capital P).")),
Q(0,
 ("`scp dosya.txt ali@sunucu:/tmp/` ne yapar?", ["dosya.txt'i uzak sunucudaki /tmp'ye kopyalar", "Sunucudan dosya indirir", "Sunucuda dosya siler", "Dosyayı eşitler ve fazlalıkları siler"], "`scp kaynak hedef`: kaynak yerelse yükler. İndirmek için sırayı çevir: `scp ali@sunucu:/tmp/x .`"),
 ("Was bewirkt `scp datei.txt ali@server:/tmp/`?", ["Kopiert datei.txt nach /tmp auf dem Server", "Lädt eine Datei vom Server herunter", "Löscht eine Datei auf dem Server", "Gleicht ab und löscht Überschüssiges"], "`scp quelle ziel`: lokale Quelle wird hochgeladen. Zum Herunterladen Reihenfolge umkehren: `scp ali@server:/tmp/x .`"),
 ("What does `scp file.txt ali@server:/tmp/` do?", ["Copies file.txt to /tmp on the server", "Downloads a file from the server", "Deletes a file on the server", "Syncs and deletes extras"], "`scp source target`: a local source is uploaded. To download, swap the order: `scp ali@server:/tmp/x .`")),
Q(1,
 ("`ssh` ilk bağlantıda \"host key\" parmak izi soruyorsa ne yapmalısın?", ["Körü körüne `yes` yazmak", "Parmak izini güvenilir bir kaynaktan doğrulamak", "Bağlantıyı hep kesmek", "Özel anahtarı göndermek"], "Parmak izi sunucunun kimliğidir; farklı çıkması ortadaki adam saldırısı işareti olabilir. Kabul edilenler `~/.ssh/known_hosts`'a yazılır."),
 ("Was tust du, wenn `ssh` beim ersten Verbinden nach dem Host-Key-Fingerprint fragt?", ["Blind `yes` eingeben", "Den Fingerprint über eine vertrauenswürdige Quelle prüfen", "Immer abbrechen", "Den privaten Schlüssel senden"], "Der Fingerprint ist die Identität des Servers; eine Abweichung kann auf Man-in-the-Middle hindeuten. Akzeptierte landen in `~/.ssh/known_hosts`."),
 ("What should you do when `ssh` asks about the host key fingerprint on first connect?", ["Blindly type `yes`", "Verify the fingerprint via a trusted source", "Always abort", "Send your private key"], "The fingerprint is the server's identity; a mismatch may signal a man-in-the-middle. Accepted keys go to `~/.ssh/known_hosts`.")),
Q(3,
 ("Anahtar tabanlı girişte sunucuya hangi dosya eklenir?", ["Özel anahtar (id_ed25519)", "known_hosts", "/etc/passwd", "Genel anahtar (`~/.ssh/authorized_keys` içine)"], "Genel anahtar sunucudaki `authorized_keys` dosyasına eklenir (`ssh-copy-id`); özel anahtar asla paylaşılmaz."),
 ("Welche Datei kommt bei der schlüsselbasierten Anmeldung auf den Server?", ["Privater Schlüssel (id_ed25519)", "known_hosts", "/etc/passwd", "Öffentlicher Schlüssel (in `~/.ssh/authorized_keys`)"], "Der öffentliche Schlüssel kommt in `authorized_keys` auf dem Server (`ssh-copy-id`); der private wird nie geteilt."),
 ("Which file goes onto the server for key-based login?", ["Private key (id_ed25519)", "known_hosts", "/etc/passwd", "Public key (into `~/.ssh/authorized_keys`)"], "The public key is added to `authorized_keys` on the server (`ssh-copy-id`); the private key is never shared.")),
])

add_quiz('2.11', [
Q(1,
 ("`*/5 * * * *` ne zaman çalışır?", ["Her saat başı", "Her 5 dakikada bir", "Her gün 5'te", "Her ayın 5'inde"], "`*/5` dakika alanında \"5'in katları\" demektir: 0, 5, 10... Her dakika için `* * * * *`."),
 ("Wann läuft `*/5 * * * *`?", ["Zu jeder vollen Stunde", "Alle 5 Minuten", "Täglich um 5 Uhr", "Am 5. jedes Monats"], "`*/5` im Minutenfeld bedeutet „alle 5“: 0, 5, 10 ... Jede Minute wäre `* * * * *`."),
 ("When does `*/5 * * * *` run?", ["Every hour on the hour", "Every 5 minutes", "Daily at 5", "On the 5th of each month"], "`*/5` in the minute field means \"every 5\": 0, 5, 10... Every minute would be `* * * * *`.")),
Q(2,
 ("Kendi cron görevlerini düzenlemek için hangi komut kullanılır?", ["cron -e", "vim /etc/cron", "crontab -e", "at -e"], "`crontab -e` kullanıcının kendi tablosunu düzenler, `crontab -l` listeler; `crontab -r` hepsini siler."),
 ("Womit bearbeitest du deine eigenen Cron-Jobs?", ["cron -e", "vim /etc/cron", "crontab -e", "at -e"], "`crontab -e` bearbeitet die eigene Tabelle, `crontab -l` listet; `crontab -r` löscht alles."),
 ("Which command edits your own cron jobs?", ["cron -e", "vim /etc/cron", "crontab -e", "at -e"], "`crontab -e` edits your own table, `crontab -l` lists it; `crontab -r` deletes everything.")),
Q(0,
 ("`crontab -r` komutunun tehlikesi nedir?", ["Tüm cron görevlerini onay sormadan siler", "Görevleri yeniden başlatır", "Yalnızca son satırı siler", "Hiçbir şey yapmaz"], "`-r` kullanıcının tüm tablosunu sorusuz siler; `-e` yanına çok yakın olduğundan sık yapılan bir hatadır. Önce `crontab -l` ile yedekle."),
 ("Worin liegt die Gefahr von `crontab -r`?", ["Löscht alle Cron-Jobs ohne Rückfrage", "Startet die Jobs neu", "Löscht nur die letzte Zeile", "Tut nichts"], "`-r` löscht die gesamte Tabelle ohne Nachfrage; liegt neben `-e`, daher häufiger Fehler. Vorher mit `crontab -l` sichern."),
 ("What is the danger of `crontab -r`?", ["It deletes all cron jobs without asking", "It restarts the jobs", "It deletes only the last line", "It does nothing"], "`-r` wipes your whole table without confirmation; it sits next to `-e`, so it's a common slip. Back up with `crontab -l` first.")),
Q(3,
 ("Cron görevinin çıktısını kaybetmemek için ne yapılır?", ["Hiçbir şey; cron kaydeder", "Görevi root yapmak", "`sleep` eklemek", "Çıktıyı bir dosyaya yönlendirmek (`>> /tmp/job.log 2>&1`)"], "Cron çıktıyı e-postaya yollamaya çalışır; kayıt için `>> dosya 2>&1` ile hem stdout hem stderr'i bir log dosyasına yönlendir."),
 ("Wie verhindert man, dass die Ausgabe eines Cron-Jobs verloren geht?", ["Gar nicht nötig; cron speichert sie", "Den Job als root laufen lassen", "`sleep` hinzufügen", "Ausgabe in eine Datei umleiten (`>> /tmp/job.log 2>&1`)"], "Cron versucht, die Ausgabe per Mail zu senden; zum Protokollieren stdout und stderr mit `>> datei 2>&1` in eine Logdatei leiten."),
 ("How do you avoid losing a cron job's output?", ["Nothing; cron stores it", "Run the job as root", "Add `sleep`", "Redirect output to a file (`>> /tmp/job.log 2>&1`)"], "Cron tries to mail the output; to keep it, redirect stdout and stderr to a log file with `>> file 2>&1`.")),
])
print('ok')
