import sys; sys.path.insert(0, 'tools')
from _a8lib import add_quiz

def Q(a, tr, de, en):
    return (a, {'tr': tr, 'de': de, 'en': en})

add_quiz('5.1', [
Q(1,
 ("`ps aux` içindeki `STAT` sütununda `S` ne demektir?", ["Durdurulmuş (stopped)", "Kesintisiz olmayan uyku; olay bekliyor", "Zombi", "Çalışıyor"], "`S` = interruptible sleep; `T` durdurulmuş, `Z` zombi, `R` çalışıyor/çalışmaya hazır."),
 ("Was bedeutet `S` in der Spalte `STAT` von `ps aux`?", ["Angehalten (stopped)", "Unterbrechbarer Schlaf, wartet auf Ereignis", "Zombie", "Läuft"], "`S` = interruptible sleep; `T` angehalten, `Z` Zombie, `R` läuft/lauffähig."),
 ("What does `S` in the `STAT` column of `ps aux` mean?", ["Stopped", "Interruptible sleep, waiting for an event", "Zombie", "Running"], "`S` = interruptible sleep; `T` stopped, `Z` zombie, `R` running/runnable.")),
Q(3,
 ("Ebeveyni sonlanan bir sürecin yeni ebeveyni kim olur?", ["Hiç ebeveyni kalmaz", "Kök kullanıcının kabuğu", "Çekirdek", "PID 1 (init/systemd)"], "Yetim süreçler PID 1 tarafından sahiplenilir; o da bitince onları `wait` ile toplar."),
 ("Wer wird neuer Elternprozess, wenn der Elternprozess endet?", ["Keiner", "Die Shell von root", "Der Kernel", "PID 1 (init/systemd)"], "Verwaiste Prozesse übernimmt PID 1; er räumt sie per `wait` ab."),
 ("Who becomes the parent of a process whose parent has exited?", ["Nobody", "root's shell", "The kernel", "PID 1 (init/systemd)"], "Orphans are adopted by PID 1, which reaps them with `wait`.")),
Q(0,
 ("Bir sürecin açık dosyalarını ve ortamını `/proc` altında nerede bulursun?", ["`/proc/<PID>/`", "`/var/run/<PID>`", "`/sys/proc/<PID>`", "`/etc/proc/<PID>`"], "Her süreç için `/proc/<PID>/` vardır: `fd/`, `environ`, `status`, `cmdline`."),
 ("Wo findest du offene Dateien und Umgebung eines Prozesses unter `/proc`?", ["`/proc/<PID>/`", "`/var/run/<PID>`", "`/sys/proc/<PID>`", "`/etc/proc/<PID>`"], "Pro Prozess gibt es `/proc/<PID>/`: `fd/`, `environ`, `status`, `cmdline`."),
 ("Where under `/proc` do you find a process's open files and environment?", ["`/proc/<PID>/`", "`/var/run/<PID>`", "`/sys/proc/<PID>`", "`/etc/proc/<PID>`"], "Each process has `/proc/<PID>/`: `fd/`, `environ`, `status`, `cmdline`.")),
Q(2,
 ("`ps -ef` ile `ps aux` arasındaki fark nedir?", ["`-ef` yalnızca kendi süreçlerini gösterir", "`aux` PID göstermez", "İkisi farklı sözdizimi (POSIX / BSD) kullanır, çoğu süreci listeler", "İkisi tamamen aynı çıktıyı verir"], "`-ef` UNIX/POSIX, `aux` BSD biçimidir; sütunlar farklıdır (`-ef` PPID verir, `aux` %CPU/%MEM)."),
 ("Was unterscheidet `ps -ef` von `ps aux`?", ["`-ef` zeigt nur eigene Prozesse", "`aux` zeigt keine PID", "Verschiedene Syntax (POSIX / BSD), beide listen fast alle Prozesse", "Beide liefern identische Ausgabe"], "`-ef` ist POSIX, `aux` BSD-Stil; Spalten unterscheiden sich (`-ef` hat PPID, `aux` %CPU/%MEM)."),
 ("How does `ps -ef` differ from `ps aux`?", ["`-ef` shows only your own processes", "`aux` shows no PID", "Different syntax (POSIX / BSD), both list nearly all processes", "They produce identical output"], "`-ef` is POSIX, `aux` BSD style; columns differ (`-ef` has PPID, `aux` %CPU/%MEM).")),
])

add_quiz('5.2', [
Q(1,
 ("`free -h` çıktısında `buff/cache` bellek için hangisi doğrudur?", ["Kalıcı olarak ayrılmıştır, boşaltılamaz", "Gerekirse uygulamalara geri verilebilir", "Takas alanıdır", "Çekirdeğe aittir ve hiç serbest kalmaz"], "Sayfa önbelleği ihtiyaç olunca geri alınır; bu yüzden `available` asıl ölçüdür."),
 ("Was gilt für `buff/cache` in der Ausgabe von `free -h`?", ["Fest reserviert, nicht freigebbar", "Kann bei Bedarf an Anwendungen zurückgegeben werden", "Es ist der Swap", "Gehört dem Kernel und wird nie frei"], "Der Seitencache wird bei Bedarf freigegeben; deshalb ist `available` maßgeblich."),
 ("What is true of `buff/cache` in `free -h` output?", ["Permanently reserved, cannot be freed", "Can be reclaimed for applications when needed", "It is swap space", "Belongs to the kernel and is never freed"], "Page cache is reclaimed on demand, which is why `available` is the key figure.")),
Q(3,
 ("Hangi komut disk G/Ç istatistiklerini aygıt bazında gösterir?", ["`free`", "`uptime`", "`ps`", "`iostat -x`"], "`iostat` (sysstat paketi) aygıt başına verimi, bekleme süresini ve kullanımı gösterir."),
 ("Welcher Befehl zeigt E/A-Statistiken pro Gerät?", ["`free`", "`uptime`", "`ps`", "`iostat -x`"], "`iostat` (Paket sysstat) zeigt Durchsatz, Wartezeit und Auslastung je Gerät."),
 ("Which command shows per-device disk I/O statistics?", ["`free`", "`uptime`", "`ps`", "`iostat -x`"], "`iostat` (sysstat package) shows throughput, wait time and utilisation per device.")),
Q(0,
 ("`top` içinde `wa` değeri yüksekse en olası neden nedir?", ["Süreçler disk/G/Ç beklemesinde", "CPU aşırı ısınmış", "Bellek dolu", "Ağ bağlantısı kopmuş"], "`wa` = I/O wait: CPU boşta ama G/Ç tamamlanmasını bekliyor."),
 ("Was ist die wahrscheinlichste Ursache für hohes `wa` in `top`?", ["Prozesse warten auf Festplatten-E/A", "CPU überhitzt", "Speicher voll", "Netzwerk getrennt"], "`wa` = I/O wait: die CPU ist untätig und wartet auf E/A."),
 ("What is the most likely cause of a high `wa` value in `top`?", ["Processes are waiting on disk I/O", "CPU overheating", "Memory is full", "Network is down"], "`wa` = I/O wait: the CPU is idle waiting for I/O to complete.")),
Q(2,
 ("`uptime` üç yük ortalaması hangi aralıkları gösterir?", ["1, 5 ve 60 saniye", "1, 10 ve 30 dakika", "1, 5 ve 15 dakika", "5, 15 ve 60 dakika"], "Yük ortalamaları son 1, 5 ve 15 dakikadır."),
 ("Welche Zeiträume zeigen die drei Load-Werte von `uptime`?", ["1, 5 und 60 Sekunden", "1, 10 und 30 Minuten", "1, 5 und 15 Minuten", "5, 15 und 60 Minuten"], "Die Load-Averages gelten für 1, 5 und 15 Minuten."),
 ("Which intervals do the three load averages in `uptime` cover?", ["1, 5 and 60 seconds", "1, 10 and 30 minutes", "1, 5 and 15 minutes", "5, 15 and 60 minutes"], "Load averages cover the last 1, 5 and 15 minutes.")),
])

add_quiz('5.3', [
Q(2,
 ("Bir sürece SIGTERM'i neden önce denemelisin?", ["Daha hızlıdır", "Yalnızca root gönderebilir", "Süreç temizlik yapıp düzgün kapanabilir", "Süreç yeniden başlar"], "SIGTERM (15) yakalanabilir: süreç dosyaları kapatıp geçici verileri temizler; SIGKILL (9) bunu engeller."),
 ("Warum solltest du zuerst SIGTERM versuchen?", ["Es ist schneller", "Nur root darf es senden", "Der Prozess kann aufräumen und sauber beenden", "Der Prozess startet neu"], "SIGTERM (15) ist abfangbar: Dateien schließen, Temporäres aufräumen; SIGKILL (9) verhindert das."),
 ("Why try SIGTERM first?", ["It is faster", "Only root can send it", "The process can clean up and exit gracefully", "The process restarts"], "SIGTERM (15) can be caught: the process closes files and removes temp data; SIGKILL (9) prevents that.")),
Q(0,
 ("Çalışan bir süreci durdurmadan yapılandırmayı yeniden okutmak için genelde hangi sinyal kullanılır?", ["SIGHUP", "SIGSTOP", "SIGKILL", "SIGINT"], "Birçok servis SIGHUP alınca yapılandırmasını yeniden yükler (`kill -HUP PID`)."),
 ("Welches Signal lässt einen laufenden Prozess üblicherweise seine Konfiguration neu lesen?", ["SIGHUP", "SIGSTOP", "SIGKILL", "SIGINT"], "Viele Dienste laden bei SIGHUP die Konfiguration neu (`kill -HUP PID`)."),
 ("Which signal commonly makes a running process reload its configuration?", ["SIGHUP", "SIGSTOP", "SIGKILL", "SIGINT"], "Many daemons reload their config on SIGHUP (`kill -HUP PID`).")),
Q(1,
 ("Normal kullanıcı bir süreci nasıl daha düşük öncelikli başlatır?", ["`renice -20 cmd`", "`nice -n 10 cmd`", "`kill -n 10 cmd`", "`nice -n -10 cmd`"], "Pozitif nice değeri önceliği düşürür; negatif değer için root gerekir."),
 ("Wie startet ein normaler Benutzer einen Prozess mit niedrigerer Priorität?", ["`renice -20 cmd`", "`nice -n 10 cmd`", "`kill -n 10 cmd`", "`nice -n -10 cmd`"], "Ein positiver Nice-Wert senkt die Priorität; negative Werte erfordern root."),
 ("How does a regular user start a process with lower priority?", ["`renice -20 cmd`", "`nice -n 10 cmd`", "`kill -n 10 cmd`", "`nice -n -10 cmd`"], "A positive nice value lowers priority; negative values need root.")),
Q(3,
 ("Çalışan bir sürecin nice değerini hangi komut değiştirir?", ["`nice -p PID`", "`chnice PID`", "`ps -n PID`", "`renice -n 5 -p PID`"], "`renice` çalışan sürecin önceliğini değiştirir; `nice` yeni süreç başlatırken kullanılır."),
 ("Welcher Befehl ändert den Nice-Wert eines laufenden Prozesses?", ["`nice -p PID`", "`chnice PID`", "`ps -n PID`", "`renice -n 5 -p PID`"], "`renice` ändert die Priorität eines laufenden Prozesses; `nice` startet neue."),
 ("Which command changes the nice value of a running process?", ["`nice -p PID`", "`chnice PID`", "`ps -n PID`", "`renice -n 5 -p PID`"], "`renice` changes a running process's priority; `nice` is for launching new ones.")),
])
print('ok')
