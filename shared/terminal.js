/* Temel Linux Akademisi v3 — simüle Linux motoru (tarayıcı + node). Gerçek sisteme dokunmaz. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.TLAEngine = factory();
})(typeof self !== 'undefined' ? self : this, function () {
  'use strict';

  /* ---------- Yardımcılar ---------- */
  function now() { return Date.now(); }
  function pad(n) { return (n < 10 ? '0' : '') + n; }
  var MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  function fmtDate(ms) {
    var d = new Date(ms);
    return MON[d.getMonth()] + ' ' + (d.getDate() < 10 ? ' ' : '') + d.getDate() + ' ' + pad(d.getHours()) + ':' + pad(d.getMinutes());
  }
  function modeStr(node) {
    var m = node.mode, t = node.t === 'd' ? 'd' : node.t === 'l' ? 'l' : node.t === 'c' ? 'c' : '-';
    var s = t, i, bits = 'rwxrwxrwx';
    for (i = 0; i < 9; i++) s += (m & (1 << (8 - i))) ? bits[i] : '-';
    if (m & 2048) s = s.slice(0, 3) + (s[3] === 'x' ? 's' : 'S') + s.slice(4);
    if (m & 1024) s = s.slice(0, 6) + (s[6] === 'x' ? 's' : 'S') + s.slice(7);
    if (m & 512) s = s.slice(0, 9) + (s[9] === 'x' ? 't' : 'T');
    return s;
  }
  function human(n) {
    if (n < 1024) return String(n);
    var u = ['K', 'M', 'G'], i = -1;
    do { n /= 1024; i++; } while (n >= 1024 && i < 2);
    return (n < 10 ? n.toFixed(1) : Math.round(n)) + u[i];
  }
  function sortNames(a, b) {
    var x = a.replace(/^\./, '').toLowerCase(), y = b.replace(/^\./, '').toLowerCase();
    return x < y ? -1 : x > y ? 1 : (a < b ? -1 : a > b ? 1 : 0);
  }
  function lines(s) {
    if (s === '') return [];
    var l = s.split('\n');
    if (l[l.length - 1] === '') l.pop();
    return l;
  }
  function esc(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }

  /* ---------- Sanal dosya sistemi ---------- */
  function dir(mode, owner, group) { return { t: 'd', mode: mode == null ? 493 : mode, owner: owner || 'root', group: group || owner || 'root', mtime: now(), c: {} }; }
  function file(data, mode, owner, group) { return { t: 'f', mode: mode == null ? 420 : mode, owner: owner || 'root', group: group || owner || 'root', mtime: now(), data: data || '' }; }

  function baseFS() {
    var root = dir(493, 'root');
    var fs = { root: root };
    function put(path, node) {
      var parts = path.split('/').filter(Boolean), cur = root, name = parts.pop();
      parts.forEach(function (p) { if (!cur.c[p]) cur.c[p] = dir(493, 'root'); cur = cur.c[p]; });
      cur.c[name] = node;
    }
    function mk(path, mode, owner, group) { put(path, dir(mode, owner, group)); }
    function wr(path, data, mode, owner, group) { put(path, file(data, mode, owner, group)); }
    ['bin', 'boot', 'dev', 'etc', 'home', 'opt', 'proc', 'run', 'srv', 'sys', 'usr', 'usr/bin', 'usr/sbin', 'usr/share', 'usr/local', 'var', 'var/log', 'var/lib', 'var/tmp', 'etc/ssh', 'etc/systemd'].forEach(function (p) { mk('/' + p); });
    delete root.c.bin; put('/bin', { t: 'l', mode: 511, owner: 'root', group: 'root', mtime: now(), target: 'usr/bin' });
    mk('/tmp', 1023, 'root'); mk('/root', 448, 'root'); mk('/var/tmp', 1023, 'root');
    root.c.dev.c['null'] = { t: 'c', mode: 438, owner: 'root', group: 'root', mtime: now(), name: 'null' };
    root.c.dev.c['zero'] = { t: 'c', mode: 438, owner: 'root', group: 'root', mtime: now(), name: 'zero' };
    wr('/etc/os-release', 'NAME="Red Hat Enterprise Linux"\nVERSION="9.4 (Plow)"\nID="rhel"\nID_LIKE="fedora"\nVERSION_ID="9.4"\nPLATFORM_ID="platform:el9"\nPRETTY_NAME="Red Hat Enterprise Linux 9.4 (Plow)"\n');
    wr('/etc/hostname', 'linux-lab\n');
    wr('/etc/hosts', '127.0.0.1   localhost localhost.localdomain\n::1         localhost\n');
    wr('/etc/passwd', 'root:x:0:0:root:/root:/bin/bash\nbin:x:1:1:bin:/bin:/sbin/nologin\ndaemon:x:2:2:daemon:/sbin:/sbin/nologin\nnobody:x:65534:65534:Kernel Overflow User:/:/sbin/nologin\nsshd:x:74:74:Privilege-separated SSH:/usr/share/empty.sshd:/sbin/nologin\nstudent:x:1000:1000:Student:/home/student:/bin/bash\nalice:x:1001:1001:Alice:/home/alice:/bin/bash\n');
    wr('/etc/group', 'root:x:0:\nwheel:x:10:student\nstudent:x:1000:\nalice:x:1001:\ndevs:x:2000:student,alice\n');
    wr('/etc/shadow', 'root:$6$xxxx:19000:0:99999:7:::\nstudent:$6$yyyy:19000:0:99999:7:::\n', 0, 'root');
    wr('/etc/shells', '/bin/sh\n/bin/bash\n/sbin/nologin\n');
    wr('/etc/fstab', '/dev/mapper/rhel-root /     xfs defaults 0 0\nUUID=1234-ABCD       /boot xfs defaults 0 0\n');
    wr('/etc/resolv.conf', 'nameserver 1.1.1.1\nsearch lab.local\n');
    wr('/etc/sysctl.conf', '# sysctl settings\nnet.ipv4.ip_forward = 0\n');
    wr('/etc/ssh/sshd_config', 'Port 22\nPermitRootLogin no\nPasswordAuthentication yes\n');
    wr('/etc/dnf.conf', '[main]\ngpgcheck=1\ninstallonly_limit=3\n');
    wr('/etc/motd', 'Linux Akademisi sanal laboratuvarına hoş geldin.\n');
    wr('/var/log/messages', 'Nov 12 08:00:01 linux-lab systemd[1]: Started Session 1.\nNov 12 08:01:12 linux-lab sshd[801]: error: PAM: Authentication failure for student\nNov 12 08:02:40 linux-lab kernel: EXT4-fs warning: mounting fs with errors\nNov 12 08:03:05 linux-lab systemd[1]: Started Daily Cleanup.\nNov 12 08:04:22 linux-lab httpd[950]: ERROR: cannot bind to port 80\nNov 12 08:05:00 linux-lab systemd[1]: Reloading.\n');
    wr('/var/log/secure', 'Nov 12 08:01:12 linux-lab sshd[801]: Failed password for student\n', 384, 'root');
    wr('/proc/cpuinfo', 'processor\t: 0\nmodel name\t: Virtual CPU @ 2.40GHz\n');
    var H = '/home/student', U = ['student', 'student'];
    mk('/home/alice', 448, 'alice');
    mk(H, 493, 'student');
    ['Documents', 'Downloads', 'Desktop'].forEach(function (d) { mk(H + '/' + d, 493, U[0], U[1]); });
    wr(H + '/.bashrc', '# ~/.bashrc\nalias ll="ls -l"\n', 420, U[0], U[1]);
    wr(H + '/.profile', '# ~/.profile\n', 420, U[0], U[1]);
    wr(H + '/notes.txt', 'Linux notes\nfirst line\nsecond line\n', 420, U[0], U[1]);
    wr(H + '/Documents/report.txt', 'Draft report\nJan: 10\nFeb: 20\n', 420, U[0], U[1]);
    wr(H + '/Documents/list.csv', 'name,city,score\nalice,london,80\nbob,paris,95\ncarol,london,70\n', 420, U[0], U[1]);
    wr(H + '/Downloads/archive.txt', 'hello\n', 420, U[0], U[1]);
    return fs;
  }

  function cloneNode(n) {
    var c = {}, k;
    for (k in n) if (k !== 'c') c[k] = n[k];
    if (n.c) { c.c = {}; for (k in n.c) c.c[k] = cloneNode(n.c[k]); }
    return c;
  }

  /* ---------- Komut belgeleri ---------- */
  var DOCS = {
    ls: ['ls [-alhR1d] [DOSYA]...', 'Dizin içeriğini listeler. -l ayrıntılı, -a gizli dosyalar, -h okunur boyut, -R özyinelemeli.', 'Listet Verzeichnisinhalte. -l Details, -a versteckte Dateien, -h lesbare Größen, -R rekursiv.', 'List directory contents. -l long format, -a hidden files, -h human sizes, -R recursive.'],
    cd: ['cd [DİZİN | - | ~]', 'Çalışma dizinini değiştirir. Argümansız cd ev dizinine, cd - önceki dizine gider.', 'Wechselt das Arbeitsverzeichnis. Ohne Argument ins Home, cd - ins vorherige.', 'Change the working directory. No argument goes home, cd - goes to the previous one.'],
    pwd: ['pwd', 'Bulunduğun dizinin tam yolunu yazar.', 'Gibt den vollständigen Pfad des aktuellen Verzeichnisses aus.', 'Print the full path of the current directory.'],
    cat: ['cat [-n] [DOSYA]...', 'Dosya içeriğini yazar; birden çok dosyayı birleştirir.', 'Gibt Dateiinhalt aus; verkettet mehrere Dateien.', 'Print file contents; concatenates several files.'],
    echo: ['echo [-ne] [METİN]...', 'Argümanları ekrana yazar. > ile dosyaya yönlendirilebilir.', 'Gibt Argumente aus. Mit > in Dateien umleitbar.', 'Print arguments. Redirect with > into files.'],
    mkdir: ['mkdir [-p] DİZİN...', 'Dizin oluşturur. -p ara dizinleri de oluşturur.', 'Erstellt Verzeichnisse. -p legt Zwischenverzeichnisse an.', 'Create directories. -p creates parents.'],
    rmdir: ['rmdir DİZİN...', 'Yalnızca boş dizinleri siler.', 'Löscht nur leere Verzeichnisse.', 'Remove empty directories only.'],
    touch: ['touch DOSYA...', 'Boş dosya oluşturur veya değişiklik zamanını günceller.', 'Erstellt leere Dateien oder aktualisiert die Zeit.', 'Create empty files or update timestamps.'],
    cp: ['cp [-r] KAYNAK... HEDEF', 'Dosya kopyalar. Dizin için -r gerekir.', 'Kopiert Dateien. Für Verzeichnisse -r nötig.', 'Copy files. Directories need -r.'],
    mv: ['mv KAYNAK... HEDEF', 'Dosya taşır veya yeniden adlandırır.', 'Verschiebt oder benennt um.', 'Move or rename files.'],
    rm: ['rm [-rf] DOSYA...', 'Dosya siler (geri dönüşü yok!). Dizin için -r. Burada yalnızca sanal dosyalar silinir.', 'Löscht Dateien (unwiderruflich!). Verzeichnisse mit -r. Hier nur virtuelle Dateien.', 'Delete files (no undo!). Directories need -r. Only virtual files here.'],
    ln: ['ln [-s] HEDEF BAĞ_ADI', 'Hard link veya (-s) sembolik link oluşturur.', 'Erstellt Hardlinks oder (-s) symbolische Links.', 'Create hard or (-s) symbolic links.'],
    grep: ['grep [-ivncrlwoE] DESEN [DOSYA]...', 'Metinde desen arar. -i büyük/küçük duyarsız, -v tersi, -n satır no, -c sayı, -r özyinelemeli.', 'Sucht Muster. -i Groß/Klein egal, -v invertiert, -n Zeilennummer, -c Anzahl, -r rekursiv.', 'Search for a pattern. -i ignore case, -v invert, -n line numbers, -c count, -r recursive.'],
    head: ['head [-n N] [DOSYA]', 'İlk N satırı (varsayılan 10) yazar.', 'Gibt die ersten N Zeilen aus (Standard 10).', 'Print the first N lines (default 10).'],
    tail: ['tail [-n N] [DOSYA]', 'Son N satırı (varsayılan 10) yazar.', 'Gibt die letzten N Zeilen aus (Standard 10).', 'Print the last N lines (default 10).'],
    wc: ['wc [-lwc] [DOSYA]', 'Satır, kelime, bayt sayar.', 'Zählt Zeilen, Wörter, Bytes.', 'Count lines, words, bytes.'],
    sort: ['sort [-rnu] [DOSYA]', 'Satırları sıralar. -r ters, -n sayısal, -u tekrarsız.', 'Sortiert Zeilen. -r umgekehrt, -n numerisch, -u eindeutig.', 'Sort lines. -r reverse, -n numeric, -u unique.'],
    uniq: ['uniq [-c] [DOSYA]', 'Ardışık tekrar eden satırları birleştirir. -c sayar. Önce sort kullan.', 'Fasst aufeinanderfolgende gleiche Zeilen zusammen. -c zählt.', 'Collapse adjacent duplicate lines. -c counts. Use sort first.'],
    cut: ['cut -d AYIRICI -f ALANLAR', 'Satırlardan alan keser: cut -d: -f1', 'Schneidet Felder: cut -d: -f1', 'Cut fields from lines: cut -d: -f1'],
    tr: ['tr SET1 SET2', 'Karakter çevirir: tr a-z A-Z', 'Übersetzt Zeichen: tr a-z A-Z', 'Translate characters: tr a-z A-Z'],
    tee: ['tee [-a] DOSYA', 'Girdiyi hem ekrana hem dosyaya yazar.', 'Schreibt Eingabe auf Bildschirm und Datei.', 'Write input to screen and file.'],
    chmod: ['chmod MOD DOSYA...', 'İzin değiştirir: chmod 755 f, chmod u+x f, chmod g-r f.', 'Ändert Rechte: chmod 755 f, chmod u+x f.', 'Change permissions: chmod 755 f, chmod u+x f, chmod g-r f.'],
    chown: ['chown KULLANICI[:GRUP] DOSYA...', 'Sahibi değiştirir. Yalnızca root (sudo) yapabilir.', 'Ändert den Besitzer. Nur root (sudo).', 'Change owner. Only root (sudo) may do it.'],
    umask: ['umask', 'Yeni dosyalar için varsayılan izin maskesini gösterir.', 'Zeigt die Standard-Rechtemaske.', 'Show the default permission mask for new files.'],
    id: ['id [KULLANICI]', 'Kullanıcı ve grup kimliklerini gösterir.', 'Zeigt Benutzer- und Gruppen-IDs.', 'Show user and group IDs.'],
    whoami: ['whoami', 'Geçerli kullanıcı adını yazar.', 'Gibt den aktuellen Benutzernamen aus.', 'Print the effective user name.'],
    groups: ['groups', 'Ait olduğun grupları yazar.', 'Gibt deine Gruppen aus.', 'Print the groups you belong to.'],
    hostname: ['hostname', 'Makine adını yazar.', 'Gibt den Rechnernamen aus.', 'Print the machine name.'],
    uname: ['uname [-asrm]', 'Sistem bilgisi: -r kernel, -m mimari, -a hepsi.', 'Systeminfo: -r Kernel, -m Architektur, -a alles.', 'System info: -r kernel, -m architecture, -a all.'],
    date: ['date', 'Tarih ve saati yazar.', 'Gibt Datum und Uhrzeit aus.', 'Print date and time.'],
    clear: ['clear', 'Ekranı temizler.', 'Löscht den Bildschirm.', 'Clear the screen.'],
    history: ['history', 'Komut geçmişini numaralı listeler.', 'Listet den Befehlsverlauf.', 'List command history.'],
    man: ['man KOMUT', 'Komutun kılavuz sayfasını gösterir.', 'Zeigt die Handbuchseite.', 'Show a command manual.'],
    help: ['help', 'Simülatörde desteklenen komutları listeler.', 'Listet unterstützte Befehle.', 'List supported commands.'],
    which: ['which KOMUT', 'Komutun nerede olduğunu gösterir.', 'Zeigt, wo ein Befehl liegt.', 'Show where a command lives.'],
    type: ['type KOMUT', 'Komutun türünü (yerleşik/dosya) söyler.', 'Zeigt den Befehlstyp.', 'Tell whether a command is builtin or a file.'],
    find: ['find [DİZİN] [-name DESEN] [-type f|d]', 'Dosya arar.', 'Sucht Dateien.', 'Search for files.'],
    stat: ['stat DOSYA', 'Dosya ayrıntılarını gösterir.', 'Zeigt Dateidetails.', 'Show file details.'],
    env: ['env', 'Ortam değişkenlerini listeler.', 'Listet Umgebungsvariablen.', 'List environment variables.'],
    export: ['export AD=DEĞER', 'Değişken tanımlar/dışa aktarır.', 'Definiert/exportiert Variablen.', 'Define/export variables.'],
    sudo: ['sudo KOMUT', 'Komutu root olarak çalıştırır (simülasyon; yalnızca wheel grubu).', 'Führt als root aus (Simulation; nur Gruppe wheel).', 'Run a command as root (simulated; wheel group only).'],
    test: ['test İFADE  veya  [ İFADE ]', 'Koşul sınar: -f -d -e -z -n, = !=, -eq -ne -lt -gt.', 'Prüft Bedingungen.', 'Evaluate conditions: -f -d -e -z -n, = !=, -eq -ne -lt -gt.'],
    basename: ['basename YOL', 'Yolun son bileşenini verir.', 'Letzter Pfadteil.', 'Last path component.'],
    dirname: ['dirname YOL', 'Yolun dizin kısmını verir.', 'Verzeichnisteil.', 'Directory part of a path.'],
    less: ['less DOSYA', 'Sayfa sayfa okuma (simülatörde cat gibi çalışır).', 'Seitenweises Lesen (hier wie cat).', 'Page through a file (acts like cat here).'],
    uptime: ['uptime', 'Sistemin ne kadar süredir açık olduğunu gösterir.', 'Zeigt die Laufzeit.', 'Show how long the system has been up.'],
    df: ['df [-h]', 'Disk kullanımını gösterir.', 'Zeigt Plattenbelegung.', 'Show disk usage.'],
    free: ['free [-h]', 'Bellek kullanımını gösterir.', 'Zeigt Speichernutzung.', 'Show memory usage.'],
    ps: ['ps', 'Süreçleri listeler (simüle).', 'Listet Prozesse (simuliert).', 'List processes (simulated).'],
    sleep: ['sleep N', 'Simülatörde bekleme yapmaz.', 'Wartet in der Simulation nicht.', 'Does not wait in the simulator.'],
    printf: ['printf BİÇİM [ARG]...', 'Biçimli yazdırır (%s %d \\n).', 'Formatierte Ausgabe.', 'Formatted print (%s %d \\n).'],
    true: ['true', 'Her zaman 0 (başarı) döner.', 'Liefert immer 0.', 'Always returns 0 (success).'],
    false: ['false', 'Her zaman 1 (hata) döner.', 'Liefert immer 1.', 'Always returns 1 (failure).'],
    exit: ['exit', 'Simülatörde oturumu kapatmaz.', 'Beendet die Sitzung nicht.', 'Does not close the session here.']
  };
  var UNSUPPORTED = 'sed awk vi vim nano emacs systemctl journalctl tar gzip ssh scp ping curl wget top htop ip ss dnf yum apt rpm kill pkill useradd usermod passwd su crontab diff mount lsblk fdisk nc ifconfig'.split(' ');

  /* ---------- Kabuk ---------- */
  function Shell(opts) {
    opts = opts || {};
    this.lang = opts.lang || 'tr';
    this.reset();
  }

  Shell.prototype.reset = function (setup) {
    this.fs = baseFS();
    this.users = {
      student: { name: 'student', uid: 1000, gid: 1000, groups: ['student', 'wheel', 'devs'], home: '/home/student' },
      root: { name: 'root', uid: 0, gid: 0, groups: ['root'], home: '/root' },
      alice: { name: 'alice', uid: 1001, gid: 1001, groups: ['alice', 'devs'], home: '/home/alice' }
    };
    this.groupIds = { root: 0, wheel: 10, student: 1000, alice: 1001, devs: 2000 };
    this.user = this.users.student;
    this.vars = { HOME: '/home/student', USER: 'student', SHELL: '/bin/bash', HOSTNAME: 'linux-lab', LANG: 'tr_TR.UTF-8', PATH: '/usr/local/bin:/usr/bin:/bin:/usr/sbin', PWD: '/home/student' };
    this.cwd = '/home/student';
    this.oldpwd = '/home/student';
    this.status = 0;
    this.umask = 18;
    this.history = [];
    this.log = [];
    if (setup) this.applySetup(setup);
  };

  Shell.prototype.applySetup = function (setup) {
    var self = this;
    (setup.dirs || []).forEach(function (p) { self.mkdirp(self.abs(p), 493, 'student'); });
    var f = setup.files || {};
    Object.keys(f).forEach(function (p) {
      var ap = self.abs(p), par = ap.slice(0, ap.lastIndexOf('/')) || '/';
      self.mkdirp(par, 493, 'student');
      var n = file(f[p], 420, 'student', 'student');
      self.parentOf(ap).c[ap.split('/').pop()] = n;
    });
    (setup.modes || []).forEach(function (m) { var n = self.lookup(self.abs(m[0])); if (n) n.mode = parseInt(m[1], 8); });
    if (setup.cwd) this.cwd = this.abs(setup.cwd);
  };

  Shell.prototype.serialize = function () {
    return JSON.stringify({ fs: this.fs.root, cwd: this.cwd, oldpwd: this.oldpwd, vars: this.vars, history: this.history.slice(-200), log: this.log.slice(-300), umask: this.umask, status: this.status });
  };
  Shell.prototype.restore = function (json) {
    var o = typeof json === 'string' ? JSON.parse(json) : json;
    if (!o || !o.fs || o.fs.t !== 'd') return false;
    this.fs = { root: o.fs };
    this.cwd = o.cwd || this.cwd; this.oldpwd = o.oldpwd || this.cwd;
    this.vars = o.vars || this.vars; this.history = o.history || []; this.log = o.log || [];
    this.umask = o.umask == null ? 18 : o.umask; this.status = o.status || 0;
    return true;
  };

  /* --- yol/dosya yardımcıları --- */
  Shell.prototype.abs = function (p, cwd) {
    if (p === '~' || p.indexOf('~/') === 0) p = this.user.home + p.slice(1);
    var full = p.charAt(0) === '/' ? p : (cwd || this.cwd) + '/' + p, out = [];
    full.split('/').forEach(function (s) {
      if (!s || s === '.') return;
      if (s === '..') out.pop(); else out.push(s);
    });
    return '/' + out.join('/');
  };
  Shell.prototype.lookup = function (abs, noFollow, depth) {
    depth = depth || 0;
    if (depth > 8) return null;
    var cur = this.fs.root, parts = abs.split('/').filter(Boolean), i;
    for (i = 0; i < parts.length; i++) {
      if (cur.t === 'l') cur = this.lookup(this.abs(cur.target, '/' + parts.slice(0, i - 1).join('/')), false, depth + 1);
      if (!cur || cur.t !== 'd') return null;
      cur = cur.c[parts[i]];
      if (!cur) return null;
    }
    if (cur.t === 'l' && !noFollow) {
      var base = '/' + parts.slice(0, -1).join('/');
      return this.lookup(this.abs(cur.target, base), false, depth + 1);
    }
    return cur;
  };
  Shell.prototype.parentOf = function (abs) {
    var i = abs.lastIndexOf('/'), p = abs.slice(0, i) || '/';
    var n = this.lookup(p);
    return n && n.t === 'd' ? n : null;
  };
  Shell.prototype.can = function (node, perm, user) {
    user = user || this.user;
    if (user.uid === 0) return perm !== 'x' || node.t === 'd' || (node.mode & 73) !== 0;
    var bit = perm === 'r' ? 4 : perm === 'w' ? 2 : 1, shift;
    if (node.owner === user.name) shift = 6;
    else if (user.groups.indexOf(node.group) !== -1) shift = 3;
    else shift = 0;
    return (node.mode >> shift & bit) !== 0;
  };
  Shell.prototype.mkdirp = function (abs, mode, owner) {
    var cur = this.fs.root;
    abs.split('/').filter(Boolean).forEach(function (p) {
      if (!cur.c[p]) cur.c[p] = dir(mode, owner || 'root', owner || 'root');
      cur = cur.c[p];
    });
  };
  Shell.prototype.groupOf = function () { return this.user.groups[0]; };
  Shell.prototype.newFile = function (data) { return file(data, 438 & ~this.umask, this.user.name, this.groupOf()); };
  Shell.prototype.newDir = function () { return dir(511 & ~this.umask, this.user.name, this.groupOf()); };
  Shell.prototype.size = function (n) { return n.t === 'f' ? Buffer_len(n.data) : n.t === 'd' ? 4096 : n.t === 'l' ? n.target.length : 0; };
  function Buffer_len(s) { var n = 0, i; for (i = 0; i < s.length; i++) { var c = s.charCodeAt(i); n += c < 128 ? 1 : c < 2048 ? 2 : 3; } return n; }

  /* Okuma/yazma yardımcıları — hata mesajı ya da null döner */
  Shell.prototype.readFile = function (p, cmd) {
    var abs = this.abs(p), n = this.lookup(abs);
    if (!n) return { err: cmd + ': ' + p + ': No such file or directory' };
    if (n.t === 'd') return { err: cmd + ': ' + p + ': Is a directory' };
    if (n.t === 'c') return { data: '' };
    if (!this.can(n, 'r')) return { err: cmd + ': ' + p + ': Permission denied' };
    return { data: n.data };
  };
  Shell.prototype.writeFile = function (p, data, append, cmd) {
    var abs = this.abs(p);
    if (abs === '/dev/null') return null;
    var n = this.lookup(abs), par;
    if (n) {
      if (n.t === 'd') return cmd + ': ' + p + ': Is a directory';
      if (!this.can(n, 'w')) return cmd + ': ' + p + ': Permission denied';
      n.data = append ? n.data + data : data; n.mtime = now();
      return null;
    }
    par = this.parentOf(abs);
    if (!par) return cmd + ': ' + p + ': No such file or directory';
    if (!this.can(par, 'w')) return cmd + ': ' + p + ': Permission denied';
    par.c[abs.split('/').pop()] = this.newFile(data);
    par.mtime = now();
    return null;
  };

  /* ---------- Ayrıştırıcı ---------- */
  function tokenize(line, sh) {
    var toks = [], i = 0, n = line.length, word = null;
    function start() { if (!word) word = { parts: [], quoted: false }; }
    function lit(s, q) {
      start();
      var last = word.parts[word.parts.length - 1];
      if (last && last.t === 'lit' && last.q === q) last.s += s; else word.parts.push({ t: 'lit', s: s, q: q });
      if (q) word.quoted = true;
    }
    function end() { if (word) { toks.push({ w: word }); word = null; } }
    function op(v) { end(); toks.push({ op: v }); }
    function readSub(open, close) {
      var depth = 1, s = '';
      while (i < n) {
        var c = line[i];
        if (c === open) depth++;
        else if (c === close) { depth--; if (!depth) { i++; return s; } }
        s += c; i++;
      }
      throw new Error("syntax error: unexpected end of file");
    }
    function readVar(q) {
      var c = line[i];
      if (c === '(') { i++; start(); word.parts.push({ t: 'cmd', s: readSub('(', ')'), q: q }); return; }
      if (c === '{') { i++; var nm = readSub('{', '}'); start(); word.parts.push({ t: 'var', name: nm, q: q }); return; }
      var m = /^([A-Za-z_]\w*|\?|\$|[0-9#@*])/.exec(line.slice(i));
      if (!m) { lit('$', q); return; }
      i += m[1].length; start(); word.parts.push({ t: 'var', name: m[1], q: q });
    }
    while (i < n) {
      var ch = line[i];
      if (ch === ' ' || ch === '\t') { end(); i++; continue; }
      if (ch === '#' && !word) break;
      if (ch === "'") { i++; var j = line.indexOf("'", i); if (j < 0) throw new Error('syntax error: unterminated quote'); lit(line.slice(i, j), true); start(); i = j + 1; continue; }
      if (ch === '"') {
        i++; start(); word.quoted = true;
        var closed = false;
        while (i < n) {
          var c = line[i];
          if (c === '"') { i++; closed = true; break; }
          if (c === '\\' && /["\\$`]/.test(line[i + 1] || '')) { lit(line[i + 1], true); i += 2; continue; }
          if (c === '$') { i++; readVar(true); continue; }
          if (c === '`') { i++; var e = line.indexOf('`', i); word.parts.push({ t: 'cmd', s: line.slice(i, e), q: true }); i = e + 1; continue; }
          lit(c, true); i++;
        }
        if (!closed) throw new Error('syntax error: unterminated quote');
        continue;
      }
      if (ch === '\\') { if (i + 1 < n) lit(line[i + 1], true); i += 2; continue; }
      if (ch === '$') { i++; readVar(false); continue; }
      if (ch === '`') { i++; var k = line.indexOf('`', i); if (k < 0) throw new Error('syntax error: unterminated `'); start(); word.parts.push({ t: 'cmd', s: line.slice(i, k), q: false }); i = k + 1; continue; }
      if (ch === '~' && !word) { lit('~', false); word.tilde = true; i++; continue; }
      if (ch === '|') { if (line[i + 1] === '|') { op('||'); i += 2; } else { op('|'); i++; } continue; }
      if (ch === '&') { if (line[i + 1] === '&') { op('&&'); i += 2; } else if (line[i + 1] === '>') { op('&>'); i += 2; } else { op('&'); i++; } continue; }
      if (ch === ';') { op(';'); i++; continue; }
      if (ch === '<') { op('<'); i++; continue; }
      if (ch === '>') {
        var fd = '';
        if (word && word.parts.length === 1 && word.parts[0].t === 'lit' && !word.parts[0].q && /^[12]$/.test(word.parts[0].s)) { fd = word.parts[0].s; word = null; } else end();
        if (line[i + 1] === '>') { toks.push({ op: fd + '>>' }); i += 2; }
        else if (line[i + 1] === '&' && /[12]/.test(line[i + 2] || '')) { toks.push({ op: fd + '>&' + line[i + 2] }); i += 3; }
        else { toks.push({ op: fd + '>' }); i++; }
        continue;
      }
      lit(ch, false); i++;
    }
    end();
    return toks;
  }

  function braceExpand(chars) {
    var i, depth = 0, open = -1;
    for (i = 0; i < chars.length; i++) {
      if (chars[i].q) continue;
      if (chars[i].c === '{') { if (!depth) open = i; depth++; }
      else if (chars[i].c === '}' && depth) {
        depth--;
        if (!depth) {
          var inner = chars.slice(open + 1, i), alts = [], d = 0, cur = [], k;
          for (k = 0; k < inner.length; k++) {
            var x = inner[k];
            if (!x.q && x.c === '{') d++;
            if (!x.q && x.c === '}') d--;
            if (!x.q && x.c === ',' && !d) { alts.push(cur); cur = []; } else cur.push(x);
          }
          alts.push(cur);
          var str = inner.map(function (x) { return x.c; }).join(''), range = /^(-?\d+)\.\.(-?\d+)$/.exec(str);
          if (range && !inner.some(function (x) { return x.q; })) {
            var a = +range[1], b = +range[2], st = a <= b ? 1 : -1;
            alts = [];
            for (var v = a; st > 0 ? v <= b : v >= b; v += st) alts.push(String(v).split('').map(function (c) { return { c: c, q: false }; }));
          } else if (alts.length < 2) continue;
          var pre = chars.slice(0, open), post = chars.slice(i + 1), res = [];
          alts.forEach(function (alt) { braceExpand(pre.concat(alt, post)).forEach(function (r) { res.push(r); }); });
          return res;
        }
      }
    }
    return [chars];
  }

  Shell.prototype.globMatch = function (chars) {
    var self = this;
    if (!chars.some(function (x) { return !x.q && /[*?\[]/.test(x.c); })) return null;
    var segs = [[]];
    chars.forEach(function (x) { if (x.c === '/' && !x.q) segs.push([]); else segs[segs.length - 1].push(x); });
    function toRe(seg) {
      var re = '^', i;
      for (i = 0; i < seg.length; i++) {
        var x = seg[i];
        if (x.q) re += esc(x.c);
        else if (x.c === '*') re += '.*';
        else if (x.c === '?') re += '.';
        else if (x.c === '[') {
          var j = i + 1, cls = '';
          while (j < seg.length && seg[j].c !== ']') { cls += seg[j].c; j++; }
          if (j < seg.length) { re += '[' + cls.replace(/^!/, '^') + ']'; i = j; } else re += '\\[';
        } else re += esc(x.c);
      }
      return new RegExp(re + '$');
    }
    var results = [];
    function walk(prefix, idx, absBase) {
      if (idx === segs.length) { results.push(prefix); return; }
      var seg = segs[idx], text = seg.map(function (x) { return x.c; }).join('');
      var special = seg.some(function (x) { return !x.q && /[*?\[]/.test(x.c); });
      var join = function (name) { return prefix === '' && idx === 0 && chars[0].c !== '/' ? name : (prefix === '/' ? '/' : prefix + '/') + name; };
      if (!special) {
        var p = idx === 0 && chars[0].c === '/' && text === '' ? '/' : join(text);
        if (text === '' && idx === 0) { walk('/', idx + 1, '/'); return; }
        var nn = self.lookup(self.abs(p));
        if (nn && (idx === segs.length - 1 || nn.t === 'd')) walk(p, idx + 1);
        return;
      }
      var base = prefix === '' ? self.cwd : self.abs(prefix), node = self.lookup(base);
      if (!node || node.t !== 'd') return;
      var re = toRe(seg);
      Object.keys(node.c).sort(sortNames).forEach(function (name) {
        if (name[0] === '.' && text[0] !== '.') return;
        if (!re.test(name)) return;
        var child = node.c[name];
        if (idx < segs.length - 1 && child.t !== 'd' && child.t !== 'l') return;
        walk(join(name), idx + 1);
      });
    }
    walk('', 0);
    return results.length ? results : null;
  };

  Shell.prototype.expandWord = function (word) {
    var self = this, fields = [[]], has = [false];
    function cur() { return fields[fields.length - 1]; }
    function addStr(s, q) { for (var i = 0; i < s.length; i++) cur().push({ c: s[i], q: q }); }
    word.parts.forEach(function (p, pi) {
      var val, q = p.q;
      if (p.t === 'lit') {
        if (word.tilde && pi === 0 && p.s.charAt(0) === '~' && !p.q) {
          var rest = p.s.slice(1);
          if (rest === '' || rest.charAt(0) === '/') { addStr(self.user.home, true); addStr(rest, false); has[has.length - 1] = true; return; }
        }
        addStr(p.s, p.q); if (p.q || p.s) has[has.length - 1] = true; return;
      }
      if (p.t === 'var') val = self.getVar(p.name);
      else val = self.captureRun(p.s);
      if (q) { addStr(val, true); has[has.length - 1] = true; return; }
      var pieces = val.split(/[ \t\n]+/), k;
      if (val === '') return;
      for (k = 0; k < pieces.length; k++) {
        if (k > 0) { fields.push([]); has.push(false); }
        if (pieces[k] !== '') { addStr(pieces[k], false); has[has.length - 1] = true; }
      }
    });
    var out = [];
    fields.forEach(function (f, idx) {
      if (!has[idx] && !f.length) return;
      braceExpand(f).forEach(function (b) {
        var g = self.globMatch(b);
        if (g) g.forEach(function (x) { out.push(x); });
        else out.push(b.map(function (x) { return x.c; }).join(''));
      });
    });
    return out;
  };

  Shell.prototype.getVar = function (name) {
    if (name === '?') return String(this.status);
    if (name === '$') return '4242';
    if (name === '0') return this.scriptName || 'bash';
    if (/^[1-9]$/.test(name)) return (this.posargs && this.posargs[+name - 1]) || '';
    if (name === '#') return String(this.posargs ? this.posargs.length : 0);
    if (name === '@' || name === '*') return (this.posargs || []).join(' ');
    return this.vars[name] != null ? this.vars[name] : '';
  };

  Shell.prototype.captureRun = function (cmdline) {
    var saved = this.chunks, out;
    this.chunks = [];
    var st = this.status;
    this.runLine(cmdline, true);
    out = this.chunks.filter(function (c) { return !c.e; }).map(function (c) { return c.s; }).join('');
    this.chunks = saved;
    this.status = st;
    return out.replace(/\n+$/, '');
  };

  /* --- yürütme --- */
  Shell.prototype.emit = function (s, isErr) { if (s !== '') this.chunks.push({ s: s, e: !!isErr }); };

  // Dönüş: { chunks, status } — chunks: [{s, e}]
  Shell.prototype.run = function (line) {
    var self = this;
    this.chunks = [];
    this.depth = 0;
    var trimmed = line.trim();
    if (trimmed === '') return { chunks: [], status: this.status };
    this.history.push(trimmed);
    var record = { cmd: trimmed.replace(/\s+/g, ' '), cwd: this.cwd, user: this.user.name, seq: [] };
    this.cmdRecords = record.seq;
    try { this.runLine(trimmed); }
    catch (e) { this.emit('bash: ' + e.message + '\n', true); this.status = 2; }
    record.status = this.status;
    record.out = this.chunks.map(function (c) { return c.s; }).join('');
    record.parts = record.seq;
    delete record.seq;
    this.log.push(record);
    if (this.log.length > 300) this.log.shift();
    this.cmdRecords = null;
    var res = { chunks: this.chunks, status: this.status };
    this.chunks = [];
    return res;
  };

  Shell.prototype.runLine = function (line, quiet) {
    if (++this.depth > 20) { this.emit('bash: max nesting depth\n', true); this.status = 1; return; }
    var toks = tokenize(line, this), i, list = [], cur = { pipe: [[]], conn: ';' };
    for (i = 0; i < toks.length; i++) {
      var t = toks[i];
      if (t.op === ';' || t.op === '&&' || t.op === '||' || t.op === '&') {
        if (cur.pipe[0].length || cur.pipe.length > 1) list.push(cur);
        cur = { pipe: [[]], conn: t.op === '&' ? ';' : t.op };
      } else if (t.op === '|') cur.pipe.push([]);
      else cur.pipe[cur.pipe.length - 1].push(t);
    }
    if (cur.pipe[0].length || cur.pipe.length > 1) list.push(cur);
    var prevConn = ';', ran = true;
    for (i = 0; i < list.length; i++) {
      var item = list[i];
      var conn = i === 0 ? ';' : list[i].conn;
      // conn belongs to the *following* item: ops stored on the item that starts after the operator
      if (conn === '&&' && this.status !== 0) continue;
      if (conn === '||' && this.status === 0) continue;
      this.runPipeline(item.pipe);
    }
    this.depth--;
  };

  Shell.prototype.runPipeline = function (stages) {
    var self = this, input = null, last = stages.length - 1, i;
    for (i = 0; i < stages.length; i++) {
      if (!stages[i].length) { this.emit('bash: syntax error near unexpected token `|\'\n', true); this.status = 2; return; }
      var r = this.runSimple(stages[i], input, i === last);
      if (r === null) return;
      input = r;
    }
  };

  Shell.prototype.runSimple = function (toks, stdin, isLast) {
    var self = this, words = [], redirs = [], assigns = [], i;
    for (i = 0; i < toks.length; i++) {
      var t = toks[i];
      if (t.op) {
        var tgt = toks[i + 1];
        if (/^(<|[12&]?>>?)$/.test(t.op) && (!tgt || !tgt.w)) { this.emit("bash: syntax error near unexpected token `newline'\n", true); this.status = 2; return null; }
        if (/^(<|[12&]?>>?)$/.test(t.op)) { redirs.push({ op: t.op, target: this.expandWord(tgt.w)[0] }); i++; }
        else if (/^[12]>&[12]$/.test(t.op)) redirs.push({ op: t.op });
        continue;
      }
      var w = t.w;
      if (!words.length) {
        var first = w.parts[0], m = first && first.t === 'lit' && !first.q && /^([A-Za-z_]\w*)=/.exec(first.s);
        if (m) {
          var copy = { parts: w.parts.map(function (p) { return p; }) };
          copy.parts[0] = { t: 'lit', s: first.s.slice(m[0].length), q: first.q };
          assigns.push([m[1], this.expandWord(copy).join(' ')]);
          continue;
        }
      }
      this.expandWord(w).forEach(function (x) { words.push(x); });
    }
    var argv = words;
    if (!argv.length) { assigns.forEach(function (a) { self.vars[a[0]] = a[1]; }); this.status = 0; return ''; }

    var outPath = null, append = false, errPath = null, errAppend = false, errToOut = false, outToErr = false, inData = stdin;
    for (i = 0; i < redirs.length; i++) {
      var r = redirs[i];
      if (r.op === '<') {
        var rd = this.readFile(r.target, 'bash');
        if (rd.err) { this.emit(rd.err.replace(/^bash: /, 'bash: ') + '\n', true); this.status = 1; return null; }
        inData = rd.data;
      } else if (r.op === '>' || r.op === '1>') { outPath = r.target; append = false; }
      else if (r.op === '>>' || r.op === '1>>') { outPath = r.target; append = true; }
      else if (r.op === '2>') { errPath = r.target; errAppend = false; }
      else if (r.op === '2>>') { errPath = r.target; errAppend = true; }
      else if (r.op === '&>') { outPath = r.target; errToOut = true; }
      else if (r.op === '2>&1') errToOut = true;
      else if (r.op === '1>&2') outToErr = true;
    }

    var saved = {}; assigns.forEach(function (a) { saved[a[0]] = self.vars[a[0]]; self.vars[a[0]] = a[1]; });
    var res = this.execCommand(argv, inData);
    assigns.forEach(function (a) { if (saved[a[0]] === undefined) delete self.vars[a[0]]; else self.vars[a[0]] = saved[a[0]]; });
    var out = res.out || '', err = res.err || '';
    this.status = res.code;
    if (this.cmdRecords) this.cmdRecords.push({ argv: argv, status: res.code });

    if (errToOut) { out += err; err = ''; }
    if (outToErr) { err += out; out = ''; }
    if (errPath !== null) {
      var e1 = this.writeFile(errPath, err, errAppend, 'bash');
      if (e1) { this.emit(e1.replace(/^bash: /, 'bash: ') + '\n', true); this.status = 1; }
      err = '';
    }
    if (outPath !== null) {
      var e2 = this.writeFile(outPath, out, append, 'bash');
      if (e2) { this.emit(e2 + '\n', true); this.status = 1; }
      out = '';
    }
    if (err) this.emit(err, true);
    if (isLastStage(isLast)) { this.emit(out, false); return ''; }
    return out;
  };
  function isLastStage(v) { return v; }

  Shell.prototype.execCommand = function (argv, stdin) {
    var name = argv[0], args = argv.slice(1), io = { out: '', err: '', stdin: stdin }, self = this;
    io.write = function (s) { io.out += s; };
    io.error = function (s) { io.err += s + '\n'; };
    var fn = COMMANDS[name];
    var code;
    if (name.indexOf('/') !== -1) code = this.runPath(name, args, io);
    else if (fn) {
      if (args.length === 1 && args[0] === '--help' && DOCS[name]) { this.printHelp(name, io); code = 0; }
      else code = fn.call(this, args, io);
    }
    else if (UNSUPPORTED.indexOf(name) !== -1) {
      io.error({ tr: name + ': bu komut simülatörde desteklenmiyor — gerçek sanal makinende dene.', de: name + ': Befehl im Simulator nicht unterstützt — probiere es auf einer echten VM.', en: name + ': not supported in the simulator — try it on a real VM.' }[this.lang]);
      code = 127;
    } else { io.error(name + ': command not found'); code = 127; }
    if (code === undefined || code === null) code = 0;
    return { out: io.out, err: io.err, code: code };
  };

  Shell.prototype.runPath = function (name, args, io) {
    var abs = this.abs(name), n = this.lookup(abs);
    if (!n) { io.error('bash: ' + name + ': No such file or directory'); return 127; }
    if (n.t === 'd') { io.error('bash: ' + name + ': Is a directory'); return 126; }
    if (!this.can(n, 'x')) { io.error('bash: ' + name + ': Permission denied'); return 126; }
    return this.runScript(n, name, args, io);
  };
  Shell.prototype.runScript = function (n, name, args, io) {
    if (this.scriptDepth > 3) { io.error('bash: max script depth'); return 1; }
    this.scriptDepth = (this.scriptDepth || 0) + 1;
    var savedChunks = this.chunks, savedArgs = this.posargs, savedName = this.scriptName, savedStatus = this.status;
    this.chunks = []; this.posargs = args; this.scriptName = name;
    var code = 0, self = this, depth = this.depth;
    lines(n.data).forEach(function (l) {
      if (/^#!/.test(l)) return;
      try { self.runLine(l); } catch (e) { self.emit('bash: ' + e.message + '\n', true); self.status = 2; }
      code = self.status;
    });
    this.depth = depth;
    this.chunks.forEach(function (c) { if (c.e) io.err += c.s; else io.out += c.s; });
    this.chunks = savedChunks; this.posargs = savedArgs; this.scriptName = savedName; this.status = savedStatus;
    this.scriptDepth--;
    return code;
  };

  Shell.prototype.printHelp = function (name, io) {
    var d = DOCS[name], li = { tr: 1, de: 2, en: 3 }[this.lang] || 1;
    io.write('Usage: ' + d[0] + '\n  ' + d[li] + '\n');
  };

  /* ---------- Komutlar ---------- */
  var COMMANDS = {};

  function parseOpts(args, spec) { // spec: string of boolean flags; returns {flags, rest}
    var flags = {}, rest = [], i, done = false;
    for (i = 0; i < args.length; i++) {
      var a = args[i];
      if (done || a === '-' || a[0] !== '-' || a.length < 2) { rest.push(a); continue; }
      if (a === '--') { done = true; continue; }
      if (a.slice(0, 2) === '--') { flags[a.slice(2)] = true; continue; }
      var bad = null;
      a.slice(1).split('').forEach(function (c) { if (spec.indexOf(c) === -1) bad = c; else flags[c] = true; });
      if (bad) return { bad: bad };
    }
    return { flags: flags, rest: rest };
  }
  function badOpt(io, name, c) { io.error(name + ": invalid option -- '" + c + "'"); io.error("Try '" + name + " --help' for more information."); return 2; }

  COMMANDS.pwd = function (a, io) { io.write(this.cwd + '\n'); };
  COMMANDS.echo = function (a, io) {
    var nl = true, interp = false;
    while (a.length && /^-[neE]+$/.test(a[0])) { if (a[0].indexOf('n') > 0) nl = false; if (a[0].indexOf('e') > 0) interp = true; a = a.slice(1); }
    var s = a.join(' ');
    if (interp) s = s.replace(/\\n/g, '\n').replace(/\\t/g, '\t').replace(/\\\\/g, '\\');
    io.write(s + (nl ? '\n' : ''));
  };
  COMMANDS.printf = function (a, io) {
    var f = a[0] || '', args = a.slice(1), k = 0;
    f = f.replace(/\\n/g, '\n').replace(/\\r/g, '\r').replace(/\\t/g, '\t');
    io.write(f.replace(/%[sd%]/g, function (m) { if (m === '%%') return '%'; return args[k++] || (m === '%d' ? '0' : ''); }));
  };
  COMMANDS.true = function () { return 0; };
  COMMANDS.false = function () { return 1; };
  COMMANDS.sleep = function () { return 0; };
  COMMANDS.clear = function (a, io) { io.write('\u001b[clear]'); };
  COMMANDS.exit = function (a, io) { io.error('logout (simulator: oturum kapatılmaz)'); return 0; };
  COMMANDS.whoami = function (a, io) { io.write(this.user.name + '\n'); };
  COMMANDS.hostname = function (a, io) { io.write('linux-lab\n'); };
  COMMANDS.date = function (a, io) {
    var d = new Date(), D = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    io.write(D[d.getDay()] + ' ' + MON[d.getMonth()] + ' ' + d.getDate() + ' ' + pad(d.getHours()) + ':' + pad(d.getMinutes()) + ':' + pad(d.getSeconds()) + ' CET ' + d.getFullYear() + '\n');
  };
  COMMANDS.uname = function (a, io) {
    var p = parseOpts(a, 'asrmnvo'); if (p.bad) return badOpt(io, 'uname', p.bad);
    var f = p.flags, parts = [];
    if (!Object.keys(f).length) parts = ['Linux'];
    else if (f.a) parts = ['Linux', 'linux-lab', '5.14.0-427.el9.x86_64', '#1 SMP PREEMPT_DYNAMIC', 'x86_64', 'GNU/Linux'];
    else { if (f.s) parts.push('Linux'); if (f.n) parts.push('linux-lab'); if (f.r) parts.push('5.14.0-427.el9.x86_64'); if (f.m) parts.push('x86_64'); if (f.o) parts.push('GNU/Linux'); }
    io.write(parts.join(' ') + '\n');
  };
  COMMANDS.uptime = function (a, io) { io.write(' 09:41:07 up 2 days,  3:12,  1 user,  load average: 0.08, 0.03, 0.01\n'); };
  COMMANDS.df = function (a, io) {
    var h = a.indexOf('-h') !== -1;
    io.write(h ? 'Filesystem               Size  Used Avail Use% Mounted on\n/dev/mapper/rhel-root     20G  4.1G   16G  21% /\n/dev/vda1               1014M  250M  765M  25% /boot\ntmpfs                    1.9G     0  1.9G   0% /dev/shm\n' : 'Filesystem           1K-blocks    Used Available Use% Mounted on\n/dev/mapper/rhel-root 20959232 4299210  16660022  21% /\n/dev/vda1              1038336  255872    782464  25% /boot\n');
  };
  COMMANDS.free = function (a, io) {
    var h = a.indexOf('-h') !== -1;
    io.write(h ? '               total        used        free      shared  buff/cache   available\nMem:           3.8Gi       612Mi       2.4Gi        12Mi       860Mi       3.0Gi\nSwap:          2.0Gi          0B       2.0Gi\n' : '               total        used        free\nMem:         3997360      626688     2516992\nSwap:        2097148           0     2097148\n');
  };
  COMMANDS.ps = function (a, io) { io.write('    PID TTY          TIME CMD\n   1203 pts/0    00:00:00 bash\n   1342 pts/0    00:00:00 ps\n'); };
  COMMANDS.env = COMMANDS.printenv = function (a, io) {
    var v = this.vars; Object.keys(v).sort().forEach(function (k) { io.write(k + '=' + v[k] + '\n'); });
  };
  COMMANDS.export = function (a, io) {
    var self = this;
    a.forEach(function (x) { var m = /^([A-Za-z_]\w*)=(.*)$/.exec(x); if (m) self.vars[m[1]] = m[2]; });
  };
  COMMANDS.umask = function (a, io) {
    if (a[0] && /^[0-7]{3,4}$/.test(a[0])) { this.umask = parseInt(a[0], 8); return 0; }
    io.write(('0000' + this.umask.toString(8)).slice(-4) + '\n');
  };

  COMMANDS.id = function (a, io) {
    var u = a[0] ? this.users[a[0]] : this.user, self = this;
    if (!u) { io.error('id: ‘' + a[0] + '’: no such user'); return 1; }
    io.write('uid=' + u.uid + '(' + u.name + ') gid=' + u.gid + '(' + u.groups[0] + ') groups=' + u.groups.map(function (g) { return self.groupIds[g] + '(' + g + ')'; }).join(',') + '\n');
  };
  COMMANDS.groups = function (a, io) { io.write(this.user.groups.join(' ') + '\n'); };

  COMMANDS.cd = function (a, io) {
    var target = a[0];
    if (a.length > 1) { io.error('bash: cd: too many arguments'); return 1; }
    if (target === undefined || target === '~') target = this.user.home;
    else if (target === '-') { target = this.oldpwd; io.write(target + '\n'); }
    var abs = this.abs(target), n = this.lookup(abs);
    if (!n) { io.error('bash: cd: ' + a[0] + ': No such file or directory'); return 1; }
    if (n.t !== 'd') { io.error('bash: cd: ' + a[0] + ': Not a directory'); return 1; }
    if (!this.can(n, 'x')) { io.error('bash: cd: ' + a[0] + ': Permission denied'); return 1; }
    this.oldpwd = this.cwd; this.cwd = abs; this.vars.PWD = abs; this.vars.OLDPWD = this.oldpwd;
  };

  COMMANDS.ls = function (a, io) {
    var p = parseOpts(a, 'alhR1dFrtS'); if (p.bad) return badOpt(io, 'ls', p.bad);
    var f = p.flags, self = this, code = 0, targets = p.rest.length ? p.rest : ['.'], files = [], dirs = [];
    targets.forEach(function (t) {
      var abs = self.abs(t), n = self.lookup(abs, true);
      if (n && n.t === 'l' && !f.l) n = self.lookup(abs);
      if (!n) { io.error("ls: cannot access '" + t + "': No such file or directory"); code = 2; return; }
      if (n.t === 'd' && !f.d) dirs.push([t, abs, n]); else files.push([t, abs, n]);
    });
    function line(name, n) {
      var suffix = f.F && n.t === 'd' ? '/' : f.F && n.t === 'f' && (n.mode & 73) ? '*' : '';
      if (!f.l) return name + suffix;
      var sz = self.size(n), when = fmtDate(n.mtime), nm = name + suffix + (n.t === 'l' ? ' -> ' + n.target : '');
      return { perm: modeStr(n), nl: n.nlink || (n.t === 'd' ? 2 : 1), o: n.owner, g: n.group, sz: f.h ? human(sz) : String(sz), when: when, nm: nm };
    }
    function render(entries) {
      if (!f.l) return entries.length ? (f['1'] || f.l ? entries.join('\n') : entries.join('  ')) + '\n' : '';
      var w = [0, 0, 0, 0];
      entries.forEach(function (e) { w[0] = Math.max(w[0], String(e.nl).length); w[1] = Math.max(w[1], e.o.length); w[2] = Math.max(w[2], e.g.length); w[3] = Math.max(w[3], e.sz.length); });
      return entries.map(function (e) {
        return e.perm + ' ' + String(e.nl).padStart(w[0]) + ' ' + e.o.padEnd(w[1]) + ' ' + e.g.padEnd(w[2]) + ' ' + e.sz.padStart(w[3]) + ' ' + e.when + ' ' + e.nm;
      }).join('\n') + '\n';
    }
    function listDir(abs, n, label) {
      if (!self.can(n, 'r')) { io.error("ls: cannot open directory '" + label + "': Permission denied"); code = 2; return; }
      var names = Object.keys(n.c).filter(function (k) { return f.a || k[0] !== '.'; });
      if (f.S) names.sort(function (x, y) { return self.size(n.c[y]) - self.size(n.c[x]); }); else names.sort(sortNames);
      if (f.t) names.sort(function (x, y) { return n.c[y].mtime - n.c[x].mtime; });
      if (f.r) names.reverse();
      var ents = [];
      if (f.a) { ents.push(line('.', n)); ents.push(line('..', n)); }
      names.forEach(function (k) { ents.push(line(k, n.c[k])); });
      if (f.l) {
        var blocks = 0; names.forEach(function (k) { blocks += Math.max(4, Math.ceil(self.size(n.c[k]) / 4096) * 4); });
        io.write('total ' + blocks + '\n');
      }
      io.write(render(ents));
      if (f.R) names.forEach(function (k) {
        if (n.c[k].t === 'd') { io.write('\n' + (label === '.' ? './' + k : label + '/' + k) + ':\n'); listDir(abs + '/' + k, n.c[k], label === '.' ? './' + k : label + '/' + k); }
      });
    }
    files.sort(function (x, y) { return sortNames(x[0], y[0]); });
    if (files.length) io.write(render(files.map(function (x) { return line(x[0], x[2]); })));
    dirs.sort(function (x, y) { return sortNames(x[0], y[0]); });
    dirs.forEach(function (d, i) {
      if (files.length || dirs.length > 1 || f.R) io.write((i || files.length ? '\n' : '') + d[0] + ':\n');
      listDir(d[1], d[2], d[0]);
    });
    return code;
  };

  function resolveInputs(sh, files, io, name, stdin) {
    if (!files.length) return [{ name: '-', data: stdin || '' }];
    var out = [], code = 0;
    files.forEach(function (f) {
      if (f === '-') { out.push({ name: '-', data: stdin || '' }); return; }
      var r = sh.readFile(f, name);
      if (r.err) { io.error(r.err); code = 1; } else out.push({ name: f, data: r.data });
    });
    out.code = code;
    return out;
  }

  COMMANDS.cat = COMMANDS.less = COMMANDS.more = function (a, io) {
    var p = parseOpts(a, 'nAbE'); if (p.bad) return badOpt(io, 'cat', p.bad);
    var ins = resolveInputs(this, p.rest, io, 'cat', io.stdin), k = 0;
    ins.forEach(function (x) {
      if (p.flags.n) { lines(x.data).forEach(function (l) { io.write(String(++k).padStart(6) + '\t' + l + '\n'); }); }
      else io.write(x.data);
    });
    return ins.code || 0;
  };
  COMMANDS.head = COMMANDS.tail = null;
  ['head', 'tail'].forEach(function (nm) {
    COMMANDS[nm] = function (a, io) {
      var n = 10, files = [], i;
      for (i = 0; i < a.length; i++) {
        if (a[i] === '-n' && a[i + 1] !== undefined) { n = parseInt(a[++i], 10); }
        else if (/^-n\d+$/.test(a[i])) n = parseInt(a[i].slice(2), 10);
        else if (/^-\d+$/.test(a[i])) n = parseInt(a[i].slice(1), 10);
        else files.push(a[i]);
      }
      if (isNaN(n)) { io.error(nm + ': invalid number of lines'); return 1; }
      var ins = resolveInputs(this, files, io, nm, io.stdin);
      ins.forEach(function (x) {
        var l = lines(x.data);
        if (ins.length > 1) io.write('==> ' + x.name + ' <==\n');
        io.write((nm === 'head' ? l.slice(0, n) : l.slice(Math.max(0, l.length - n))).map(function (s) { return s + '\n'; }).join(''));
      });
      return ins.code || 0;
    };
  });
  COMMANDS.wc = function (a, io) {
    var p = parseOpts(a, 'lwcm'); if (p.bad) return badOpt(io, 'wc', p.bad);
    var ins = resolveInputs(this, p.rest, io, 'wc', io.stdin), f = p.flags, any = f.l || f.w || f.c || f.m, tot = [0, 0, 0];
    function fmt(c, name) {
      var cols = [];
      if (!any || f.l) cols.push(c[0]); if (!any || f.w) cols.push(c[1]); if (!any || f.c || f.m) cols.push(c[2]);
      return cols.map(function (x) { return any && cols.length === 1 ? String(x) : String(x).padStart(7); }).join(' ') + (name && name !== '-' ? ' ' + name : '') + '\n';
    }
    ins.forEach(function (x) {
      var c = [(x.data.match(/\n/g) || []).length, (x.data.trim() ? x.data.trim().split(/\s+/).length : 0), Buffer_len(x.data)];
      tot[0] += c[0]; tot[1] += c[1]; tot[2] += c[2];
      io.write(fmt(c, x.name));
    });
    if (ins.length > 1) io.write(fmt(tot, 'total'));
    return ins.code || 0;
  };
  COMMANDS.sort = function (a, io) {
    var flags = {}, files = [], keyField = 1, i, j;
    for (i = 0; i < a.length; i++) {
      if (a[i] === '--') { files = files.concat(a.slice(i + 1)); break; }
      if (a[i] === '-k') {
        var key = a[++i];
        if (!key || !/^\d+$/.test(key) || +key < 1) { io.error("sort: option requires a positive field number after '-k'"); return 2; }
        keyField = +key;
      } else if (/^-k\d+$/.test(a[i])) keyField = +a[i].slice(2);
      else if (a[i].charAt(0) === '-' && a[i] !== '-') {
        for (j = 1; j < a[i].length; j++) {
          if ('rnu'.indexOf(a[i][j]) === -1) return badOpt(io, 'sort', a[i][j]);
          flags[a[i][j]] = true;
        }
      } else files.push(a[i]);
    }
    var ins = resolveInputs(this, files, io, 'sort', io.stdin), all = [];
    ins.forEach(function (x) { all = all.concat(lines(x.data)); });
    function keyOf(line) { return keyField === 1 ? line : (line.trim().split(/\s+/)[keyField - 1] || ''); }
    all.sort(function (x, y) {
      var X = keyOf(x), Y = keyOf(y), cmp;
      if (flags.n) cmp = (parseFloat(X) || 0) - (parseFloat(Y) || 0);
      else { X = X.toLowerCase(); Y = Y.toLowerCase(); cmp = X < Y ? -1 : X > Y ? 1 : 0; }
      if (!cmp) cmp = x < y ? -1 : x > y ? 1 : 0;
      return flags.r ? -cmp : cmp;
    });
    if (flags.u) all = all.filter(function (l, i) { return i === 0 || l !== all[i - 1]; });
    io.write(all.map(function (l) { return l + '\n'; }).join(''));
    return ins.code || 0;
  };
  COMMANDS.uniq = function (a, io) {
    var p = parseOpts(a, 'cdu'); if (p.bad) return badOpt(io, 'uniq', p.bad);
    var ins = resolveInputs(this, p.rest, io, 'uniq', io.stdin), out = [];
    ins.forEach(function (x) {
      lines(x.data).forEach(function (l) { var last = out[out.length - 1]; if (last && last[0] === l) last[1]++; else out.push([l, 1]); });
    });
    out.forEach(function (e) {
      if (p.flags.d && e[1] < 2) return; if (p.flags.u && e[1] > 1) return;
      io.write((p.flags.c ? String(e[1]).padStart(7) + ' ' : '') + e[0] + '\n');
    });
    return ins.code || 0;
  };
  COMMANDS.cut = function (a, io) {
    var d = '\t', fl = null, files = [], i;
    for (i = 0; i < a.length; i++) {
      if (a[i] === '-d') d = a[++i];
      else if (/^-d./.test(a[i])) d = a[i].slice(2);
      else if (a[i] === '-f') fl = a[++i];
      else if (/^-f./.test(a[i])) fl = a[i].slice(2);
      else files.push(a[i]);
    }
    if (fl === null) { io.error('cut: you must specify a list of bytes, characters, or fields'); return 1; }
    var want = [];
    fl.split(',').forEach(function (r) {
      var m = /^(\d*)-(\d*)$/.exec(r);
      if (m) { var lo = +m[1] || 1, hi = +m[2] || 999; for (var k = lo; k <= hi; k++) want.push(k); } else want.push(+r);
    });
    var ins = resolveInputs(this, files, io, 'cut', io.stdin);
    ins.forEach(function (x) {
      lines(x.data).forEach(function (l) {
        var cols = l.split(d);
        if (cols.length === 1 && l.indexOf(d) === -1) { io.write(l + '\n'); return; }
        io.write(want.filter(function (k) { return k <= cols.length; }).map(function (k) { return cols[k - 1]; }).join(d) + '\n');
      });
    });
    return ins.code || 0;
  };
  COMMANDS.tr = function (a, io) {
    var del = a[0] === '-d', squeeze = a[0] === '-s';
    var s1 = del || squeeze ? a[1] : a[0], s2 = del || squeeze ? a[2] : a[1];
    if (!s1) { io.error('tr: missing operand'); return 1; }
    function unescapeSet(s) {
      return (s || '').replace(/\\([\\nrt])/g, function (m, c) {
        return c === 'n' ? '\n' : c === 'r' ? '\r' : c === 't' ? '\t' : '\\';
      });
    }
    function expand(s) { return (s || '').replace(/([^\\])-(.)/g, function (m, x, y) { var r = '', c; for (c = x.charCodeAt(0); c <= y.charCodeAt(0); c++) r += String.fromCharCode(c); return r; }).replace(/^(.)-(.)/, function (m, x, y) { var r = '', c; for (c = x.charCodeAt(0); c <= y.charCodeAt(0); c++) r += String.fromCharCode(c); return r; }); }
    var e1 = expand(unescapeSet(s1).replace(/\[:upper:\]/g, 'A-Z').replace(/\[:lower:\]/g, 'a-z'));
    var e2 = expand(unescapeSet(s2).replace(/\[:upper:\]/g, 'A-Z').replace(/\[:lower:\]/g, 'a-z'));
    var squeezeSet = squeeze ? (e2 || e1) : '', out = '', data = io.stdin || '', i, idx, ch, previous = null;
    for (i = 0; i < data.length; i++) {
      ch = data[i];
      idx = e1.indexOf(ch);
      if (del && idx !== -1) continue;
      if (!del && idx !== -1) ch = e2.length ? e2[Math.min(idx, e2.length - 1)] : ch;
      if (squeezeSet.indexOf(ch) !== -1 && ch === previous) continue;
      out += ch;
      previous = ch;
    }
    io.write(out);
  };
  COMMANDS.tee = function (a, io) {
    var p = parseOpts(a, 'a'); if (p.bad) return badOpt(io, 'tee', p.bad);
    var self = this, code = 0;
    p.rest.forEach(function (f) { var e = self.writeFile(f, io.stdin || '', !!p.flags.a, 'tee'); if (e) { io.error(e); code = 1; } });
    io.write(io.stdin || '');
    return code;
  };
  COMMANDS.grep = function (a, io) {
    var p = parseOpts(a, 'ivncrlwoEFHhRq'); if (p.bad) return badOpt(io, 'grep', p.bad);
    var f = p.flags, pat = p.rest[0], files = p.rest.slice(1), self = this;
    if (pat === undefined) { io.error('Usage: grep [OPTION]... PATTERNS [FILE]...'); return 2; }
    var re;
    try { re = new RegExp(f.F ? esc(pat) : (f.w ? '\\b(?:' + pat + ')\\b' : pat), f.i ? 'i' : ''); } catch (e) { re = new RegExp(esc(pat), f.i ? 'i' : ''); }
    var sources = [], code = 0;
    if (!files.length && (f.r || f.R)) files = ['.'];
    if (!files.length) sources.push({ name: '(standard input)', data: io.stdin || '' });
    else {
      files.forEach(function (fl) {
        var abs = self.abs(fl), n = self.lookup(abs);
        if (n && n.t === 'd' && (f.r || f.R)) {
          (function walk(pth, node, shown) {
            Object.keys(node.c).sort(sortNames).forEach(function (k) {
              var c = node.c[k], sp = (shown === '.' ? '.' : shown) + '/' + k;
              if (c.t === 'd') walk(pth + '/' + k, c, sp);
              else if (c.t === 'f' && self.can(c, 'r')) sources.push({ name: sp.replace(/^\.\//, fl === '.' ? '' : './'), data: c.data });
            });
          })(abs, n, fl === '.' ? '.' : fl);
        } else {
          var r = self.readFile(fl, 'grep');
          if (r.err) { io.error(r.err.replace(': Is a directory', ': Is a directory')); code = 2; } else sources.push({ name: fl, data: r.data });
        }
      });
    }
    var multi = (files.length > 1 || f.r || f.R || f.H) && !f.h, matched = false;
    sources.forEach(function (s) {
      var count = 0;
      lines(s.data).forEach(function (l, i) {
        var m = re.test(l);
        if (f.v) m = !m;
        if (!m) return;
        count++; matched = true;
        if (f.c || f.l || f.q) return;
        var prefix = (multi ? s.name + ':' : '') + (f.n ? (i + 1) + ':' : '');
        if (f.o && !f.v) { var g = new RegExp(re.source, re.flags + 'g'), mm; while ((mm = g.exec(l))) { io.write(prefix + mm[0] + '\n'); if (!mm[0]) break; } }
        else io.write(prefix + l + '\n');
      });
      if (f.c) io.write((multi ? s.name + ':' : '') + count + '\n');
      if (f.l && count) io.write(s.name + '\n');
    });
    return code === 2 ? 2 : matched ? 0 : 1;
  };

  COMMANDS.mkdir = function (a, io) {
    var p = parseOpts(a, 'pv'); if (p.bad) return badOpt(io, 'mkdir', p.bad);
    if (!p.rest.length) { io.error('mkdir: missing operand'); return 1; }
    var self = this, code = 0;
    p.rest.forEach(function (d) {
      var abs = self.abs(d), ex = self.lookup(abs);
      if (ex) { if (!p.flags.p) { io.error("mkdir: cannot create directory '" + d + "': File exists"); code = 1; } return; }
      if (p.flags.p) {
        var parts = abs.split('/').filter(Boolean), cur = self.fs.root, ok = true;
        parts.forEach(function (s) {
          if (!ok) return;
          if (!cur.c[s]) {
            if (!self.can(cur, 'w')) { io.error("mkdir: cannot create directory '" + d + "': Permission denied"); code = 1; ok = false; return; }
            cur.c[s] = self.newDir();
          }
          cur = cur.c[s];
          if (cur.t === 'l') cur = self.lookup(self.abs(cur.target, '/'));
        });
        return;
      }
      var par = self.parentOf(abs);
      if (!par) { io.error("mkdir: cannot create directory '" + d + "': No such file or directory"); code = 1; return; }
      if (!self.can(par, 'w')) { io.error("mkdir: cannot create directory '" + d + "': Permission denied"); code = 1; return; }
      par.c[abs.split('/').pop()] = self.newDir(); par.mtime = now();
    });
    return code;
  };
  COMMANDS.touch = function (a, io) {
    var self = this, code = 0;
    if (!a.length) { io.error('touch: missing file operand'); return 1; }
    a.forEach(function (f) {
      if (f[0] === '-') return;
      var abs = self.abs(f), n = self.lookup(abs);
      if (n) { if (!self.can(n, 'w') && self.user.uid !== 0) { io.error("touch: cannot touch '" + f + "': Permission denied"); code = 1; } else n.mtime = now(); return; }
      var par = self.parentOf(abs);
      if (!par) { io.error("touch: cannot touch '" + f + "': No such file or directory"); code = 1; return; }
      if (!self.can(par, 'w')) { io.error("touch: cannot touch '" + f + "': Permission denied"); code = 1; return; }
      par.c[abs.split('/').pop()] = self.newFile(''); par.mtime = now();
    });
    return code;
  };
  COMMANDS.rmdir = function (a, io) {
    var self = this, code = 0;
    if (!a.length) { io.error('rmdir: missing operand'); return 1; }
    a.forEach(function (d) {
      var abs = self.abs(d), n = self.lookup(abs, true);
      if (!n) { io.error("rmdir: failed to remove '" + d + "': No such file or directory"); code = 1; }
      else if (n.t !== 'd') { io.error("rmdir: failed to remove '" + d + "': Not a directory"); code = 1; }
      else if (Object.keys(n.c).length) { io.error("rmdir: failed to remove '" + d + "': Directory not empty"); code = 1; }
      else if (!self.can(self.parentOf(abs), 'w')) { io.error("rmdir: failed to remove '" + d + "': Permission denied"); code = 1; }
      else { delete self.parentOf(abs).c[abs.split('/').pop()]; }
    });
    return code;
  };
  COMMANDS.rm = function (a, io) {
    var p = parseOpts(a, 'rRfdiv'); if (p.bad) return badOpt(io, 'rm', p.bad);
    var self = this, code = 0, rec = p.flags.r || p.flags.R || p.flags.recursive, force = p.flags.f;
    if (!p.rest.length) { if (!force) { io.error('rm: missing operand'); return 1; } return 0; }
    p.rest.forEach(function (f) {
      var abs = self.abs(f), n = self.lookup(abs, true);
      if (abs === '/' || /\/\.\.?$/.test(f) || f === '.' || f === '..') {
        io.error("rm: it is dangerous to operate recursively on '" + f + "'"); io.error('rm: (simulator: bu komut güvenlik için reddedildi)'); code = 1; return;
      }
      if (!n) { if (!force) { io.error("rm: cannot remove '" + f + "': No such file or directory"); code = 1; } return; }
      if (n.t === 'd' && !rec) { io.error("rm: cannot remove '" + f + "': Is a directory"); code = 1; return; }
      var par = self.parentOf(abs);
      if (!self.can(par, 'w')) { io.error("rm: cannot remove '" + f + "': Permission denied"); code = 1; return; }
      delete par.c[abs.split('/').pop()]; par.mtime = now();
    });
    return code;
  };
  function copyNode(sh, n) { var c = cloneNode(n); c.owner = sh.user.name; c.group = sh.groupOf(); c.mtime = now(); return c; }
  COMMANDS.cp = function (a, io) {
    var p = parseOpts(a, 'rRaipvf'); if (p.bad) return badOpt(io, 'cp', p.bad);
    var self = this, rec = p.flags.r || p.flags.R || p.flags.a;
    if (p.rest.length < 2) { io.error(p.rest.length ? "cp: missing destination file operand after '" + p.rest[0] + "'" : 'cp: missing file operand'); return 1; }
    var dst = p.rest[p.rest.length - 1], srcs = p.rest.slice(0, -1), dabs = this.abs(dst), dn = this.lookup(dabs), code = 0;
    if (srcs.length > 1 && !(dn && dn.t === 'd')) { io.error("cp: target '" + dst + "' is not a directory"); return 1; }
    srcs.forEach(function (s) {
      var sabs = self.abs(s), sn = self.lookup(sabs);
      if (!sn) { io.error("cp: cannot stat '" + s + "': No such file or directory"); code = 1; return; }
      if (sn.t === 'd' && !rec) { io.error("cp: -r not specified; omitting directory '" + s + "'"); code = 1; return; }
      if (sn.t === 'f' && !self.can(sn, 'r')) { io.error("cp: cannot open '" + s + "' for reading: Permission denied"); code = 1; return; }
      var target = dn && dn.t === 'd' ? dabs + '/' + sabs.split('/').pop() : dabs;
      if (target === sabs) { io.error("cp: '" + s + "' and '" + dst + "' are the same file"); code = 1; return; }
      if (sn.t === 'd' && (target + '/').indexOf(sabs + '/') === 0) { io.error("cp: cannot copy a directory, '" + s + "', into itself, '" + dst + "'"); code = 1; return; }
      var par = self.parentOf(target);
      if (!par) { io.error("cp: cannot create regular file '" + dst + "': No such file or directory"); code = 1; return; }
      if (!self.can(par, 'w')) { io.error("cp: cannot create regular file '" + dst + "': Permission denied"); code = 1; return; }
      var ex = self.lookup(target);
      if (ex && ex.t === 'f' && !self.can(ex, 'w')) { io.error("cp: cannot create regular file '" + dst + "': Permission denied"); code = 1; return; }
      par.c[target.split('/').pop()] = copyNode(self, sn);
    });
    return code;
  };
  COMMANDS.mv = function (a, io) {
    var p = parseOpts(a, 'fiv'); if (p.bad) return badOpt(io, 'mv', p.bad);
    var self = this;
    if (p.rest.length < 2) { io.error(p.rest.length ? "mv: missing destination file operand after '" + p.rest[0] + "'" : 'mv: missing file operand'); return 1; }
    var dst = p.rest[p.rest.length - 1], srcs = p.rest.slice(0, -1), dabs = this.abs(dst), dn = this.lookup(dabs), code = 0;
    if (srcs.length > 1 && !(dn && dn.t === 'd')) { io.error("mv: target '" + dst + "' is not a directory"); return 1; }
    srcs.forEach(function (s) {
      var sabs = self.abs(s), sn = self.lookup(sabs, true);
      if (!sn) { io.error("mv: cannot stat '" + s + "': No such file or directory"); code = 1; return; }
      var target = dn && dn.t === 'd' ? dabs + '/' + sabs.split('/').pop() : dabs;
      if (target === sabs) { io.error("mv: '" + s + "' and '" + dst + "' are the same file"); code = 1; return; }
      if (sn.t === 'd' && (target + '/').indexOf(sabs + '/') === 0) { io.error("mv: cannot move '" + s + "' to a subdirectory of itself, '" + dst + "'"); code = 1; return; }
      var sp = self.parentOf(sabs), tp = self.parentOf(target);
      if (!tp) { io.error("mv: cannot move '" + s + "' to '" + dst + "': No such file or directory"); code = 1; return; }
      if (!self.can(sp, 'w') || !self.can(tp, 'w')) { io.error("mv: cannot move '" + s + "' to '" + dst + "': Permission denied"); code = 1; return; }
      delete sp.c[sabs.split('/').pop()];
      tp.c[target.split('/').pop()] = sn;
    });
    return code;
  };
  COMMANDS.ln = function (a, io) {
    var p = parseOpts(a, 'sf'); if (p.bad) return badOpt(io, 'ln', p.bad);
    if (p.rest.length < 2) { io.error('ln: missing file operand'); return 1; }
    var tgt = p.rest[0], name = p.rest[1], abs = this.abs(name), ex = this.lookup(abs), self = this;
    if (ex && ex.t === 'd') abs = abs + '/' + tgt.split('/').pop();
    else if (ex) { io.error("ln: failed to create " + (p.flags.s ? 'symbolic' : 'hard') + " link '" + name + "': File exists"); return 1; }
    var par = this.parentOf(abs);
    if (!par) { io.error("ln: failed to create link '" + name + "': No such file or directory"); return 1; }
    if (!this.can(par, 'w')) { io.error("ln: failed to create link '" + name + "': Permission denied"); return 1; }
    if (p.flags.s) par.c[abs.split('/').pop()] = { t: 'l', mode: 511, owner: this.user.name, group: this.groupOf(), mtime: now(), target: tgt };
    else {
      var sn = this.lookup(this.abs(tgt));
      if (!sn) { io.error("ln: failed to access '" + tgt + "': No such file or directory"); return 1; }
      if (sn.t === 'd') { io.error("ln: '" + tgt + "': hard link not allowed for directory"); return 1; }
      sn.nlink = (sn.nlink || 1) + 1;
      par.c[abs.split('/').pop()] = sn;
    }
  };
  COMMANDS.stat = function (a, io) {
    var self = this, code = 0;
    a.forEach(function (f) {
      var n = self.lookup(self.abs(f), true);
      if (!n) { io.error("stat: cannot statx '" + f + "': No such file or directory"); code = 1; return; }
      io.write('  File: ' + f + '\n  Size: ' + self.size(n) + '\t' + (n.t === 'd' ? 'directory' : n.t === 'l' ? 'symbolic link' : 'regular file') + '\nAccess: (' + ('0000' + (n.mode & 4095).toString(8)).slice(-4) + '/' + modeStr(n) + ')  Uid: (' + (self.users[n.owner] ? self.users[n.owner].uid : 0) + '/' + n.owner + ')   Gid: (' + (self.groupIds[n.group] || 0) + '/' + n.group + ')\nModify: ' + new Date(n.mtime).toISOString().replace('T', ' ').slice(0, 19) + '\n');
    });
    return code;
  };
  function applyChmod(sh, spec, node) {
    if (/^[0-7]{1,4}$/.test(spec)) { node.mode = (node.mode & ~4095) | parseInt(spec, 8); return true; }
    var parts = spec.split(','), m = node.mode, ok = true;
    parts.forEach(function (p) {
      var mt = /^([ugoa]*)([-+=])([rwxXst]*)$/.exec(p);
      if (!mt) { ok = false; return; }
      var who = mt[1] || 'a', bits = 0;
      if (who.indexOf('a') !== -1) who = 'ugo';
      mt[3].split('').forEach(function (c) { bits |= { r: 4, w: 2, x: 1, X: (node.t === 'd' ? 1 : 0), s: 0, t: 0 }[c] || 0; });
      who.split('').forEach(function (w) {
        var sh2 = { u: 6, g: 3, o: 0 }[w], b = bits << sh2;
        if (mt[2] === '+') m |= b; else if (mt[2] === '-') m &= ~b; else m = (m & ~(7 << sh2)) | b;
        if (mt[3].indexOf('s') !== -1) m |= w === 'u' ? 2048 : w === 'g' ? 1024 : 0;
        if (mt[3].indexOf('t') !== -1) m |= 512;
      });
    });
    if (ok) node.mode = m;
    return ok;
  }
  COMMANDS.chmod = function (a, io) {
    var spec, files, self = this, code = 0, rec = a.indexOf('-R') !== -1;
    var args = a.filter(function (x) { return x !== '-R' && x !== '-v'; });
    if (args.length < 2) { io.error(args.length ? "chmod: missing operand after '" + args[0] + "'" : 'chmod: missing operand'); return 1; }
    spec = args[0]; files = args.slice(1);
    files.forEach(function (f) {
      var abs = self.abs(f), n = self.lookup(abs);
      if (!n) { io.error("chmod: cannot access '" + f + "': No such file or directory"); code = 1; return; }
      if (n.owner !== self.user.name && self.user.uid !== 0) { io.error("chmod: changing permissions of '" + f + "': Operation not permitted"); code = 1; return; }
      (function apply(x) {
        if (!applyChmod(self, spec, x)) { io.error("chmod: invalid mode: ‘" + spec + "’"); code = 1; return; }
        if (rec && x.t === 'd') Object.keys(x.c).forEach(function (k) { apply(x.c[k]); });
      })(n);
    });
    return code;
  };
  COMMANDS.chown = function (a, io) {
    var args = a.filter(function (x) { return x !== '-R'; }), rec = a.indexOf('-R') !== -1, self = this, code = 0;
    if (args.length < 2) { io.error(args.length ? "chown: missing operand after '" + args[0] + "'" : 'chown: missing operand'); return 1; }
    var spec = args[0].split(':'), owner = spec[0], group = spec[1];
    if (owner && !this.users[owner]) { io.error("chown: invalid user: ‘" + args[0] + "’"); return 1; }
    if (group && this.groupIds[group] == null) { io.error("chown: invalid group: ‘" + args[0] + "’"); return 1; }
    args.slice(1).forEach(function (f) {
      var n = self.lookup(self.abs(f));
      if (!n) { io.error("chown: cannot access '" + f + "': No such file or directory"); code = 1; return; }
      if (self.user.uid !== 0) { io.error("chown: changing ownership of '" + f + "': Operation not permitted"); code = 1; return; }
      (function apply(x) {
        if (owner) x.owner = owner; if (group) x.group = group;
        if (rec && x.t === 'd') Object.keys(x.c).forEach(function (k) { apply(x.c[k]); });
      })(n);
    });
    return code;
  };
  COMMANDS.chgrp = function (a, io) { return COMMANDS.chown.call(this, [':' + a[0]].concat(a.slice(1)), io); };

  COMMANDS.find = function (a, io) {
    var start = '.', i = 0, name = null, type = null, self = this;
    if (a[0] && a[0][0] !== '-') { start = a[0]; i = 1; }
    for (; i < a.length; i++) {
      if (a[i] === '-name' || a[i] === '-iname') { name = a[++i]; if (a[i - 1] === '-iname') name = '(?i)' + name; }
      else if (a[i] === '-type') type = a[++i];
    }
    var ci = name && name.indexOf('(?i)') === 0; if (ci) name = name.slice(4);
    var re = name ? new RegExp('^' + name.split('*').map(function (x) { return x.split('?').map(esc).join('.'); }).join('.*') + '$', ci ? 'i' : '') : null;
    var abs = this.abs(start), n = this.lookup(abs);
    if (!n) { io.error("find: ‘" + start + "’: No such file or directory"); return 1; }
    (function walk(node, shown, nm) {
      var ok = (!re || re.test(nm)) && (!type || (type === 'd' ? node.t === 'd' : type === 'f' ? node.t === 'f' : type === 'l' ? node.t === 'l' : true));
      if (ok) io.write(shown + '\n');
      if (node.t === 'd' && self.can(node, 'r')) Object.keys(node.c).sort(sortNames).forEach(function (k) { walk(node.c[k], (shown === '/' ? '' : shown) + '/' + k, k); });
    })(n, start, abs.split('/').pop() || '/');
  };
  COMMANDS.basename = function (a, io) { var p = (a[0] || '').replace(/\/+$/, ''); var b = p.split('/').pop() || '/'; if (a[1] && b.slice(-a[1].length) === a[1]) b = b.slice(0, -a[1].length); io.write(b + '\n'); };
  COMMANDS.dirname = function (a, io) { var p = (a[0] || '').replace(/\/+$/, ''), i = p.lastIndexOf('/'); io.write((i < 0 ? '.' : i === 0 ? '/' : p.slice(0, i)) + '\n'); };

  function testExpr(sh, a) {
    var neg = false;
    if (a[0] === '!') { neg = true; a = a.slice(1); }
    var r, n;
    if (a.length === 1) r = a[0] !== '';
    else if (a.length === 2) {
      n = sh.lookup(sh.abs(a[1]));
      switch (a[0]) {
        case '-e': r = !!n; break; case '-f': r = !!n && n.t === 'f'; break; case '-d': r = !!n && n.t === 'd'; break;
        case '-r': r = !!n && sh.can(n, 'r'); break; case '-w': r = !!n && sh.can(n, 'w'); break; case '-x': r = !!n && sh.can(n, 'x'); break;
        case '-s': r = !!n && sh.size(n) > 0; break; case '-z': r = a[1] === ''; break; case '-n': r = a[1] !== ''; break; default: r = false;
      }
    } else if (a.length === 3) {
      var x = a[0], y = a[2];
      switch (a[1]) {
        case '=': case '==': r = x === y; break; case '!=': r = x !== y; break;
        case '-eq': r = +x === +y; break; case '-ne': r = +x !== +y; break; case '-lt': r = +x < +y; break;
        case '-le': r = +x <= +y; break; case '-gt': r = +x > +y; break; case '-ge': r = +x >= +y; break; default: r = false;
      }
    } else r = false;
    return neg ? !r : r;
  }
  COMMANDS.test = function (a, io) { return testExpr(this, a) ? 0 : 1; };
  COMMANDS['['] = function (a, io) { if (a[a.length - 1] !== ']') { io.error("bash: [: missing `]'"); return 2; } return testExpr(this, a.slice(0, -1)) ? 0 : 1; };

  COMMANDS.history = function (a, io) {
    var h = this.history;
    if (a[0] === '-c') { this.history = []; return 0; }
    h.forEach(function (c, i) { io.write(String(i + 1).padStart(5) + '  ' + c + '\n'); });
  };
  COMMANDS.sudo = function (a, io) {
    if (!a.length) { io.error('usage: sudo command'); return 1; }
    if (this.user.groups.indexOf('wheel') === -1 && this.user.uid !== 0) { io.error(this.user.name + ' is not in the sudoers file.'); return 1; }
    var saved = this.user;
    this.user = this.users.root;
    var r;
    try { r = this.execCommand(a, io.stdin); } finally { this.user = saved; }
    io.write(r.out); io.err += r.err;
    return r.code;
  };
  COMMANDS.which = COMMANDS.type = function (a, io) {
    var code = 0;
    a.forEach(function (c) {
      var builtin = ['cd', 'echo', 'pwd', 'type', 'history', 'export', 'umask', 'test', 'printf', 'true', 'false', 'exit', 'help'].indexOf(c) !== -1;
      if (COMMANDS[c] && !builtin) io.write('/usr/bin/' + c + '\n');
      else if (builtin) io.write(c + ' is a shell builtin\n');
      else { io.error('bash: type: ' + c + ': not found'); code = 1; }
    });
    return code;
  };
  COMMANDS.help = function (a, io) {
    io.write(Object.keys(DOCS).sort().join('  ') + '\n');
  };
  COMMANDS.man = function (a, io) {
    var li = { tr: 1, de: 2, en: 3 }[this.lang] || 1;
    if (!a.length) { io.error('What manual page do you want?'); return 1; }
    var d = DOCS[a[0]];
    if (!d) { io.error('No manual entry for ' + a[0]); return 16; }
    io.write(a[0].toUpperCase() + '(1)\n\nNAME\n       ' + a[0] + '\n\nSYNOPSIS\n       ' + d[0] + '\n\nDESCRIPTION\n       ' + d[li] + '\n');
  };

  /* ---------- Tab tamamlama ---------- */
  Shell.prototype.complete = function (line) {
    var m = /(?:^|[|;&]\s*|\s)([^\s|;&]*)$/.exec(line), word = m ? m[1] : '';
    var before = line.slice(0, line.length - word.length);
    var isCmd = /^\s*$/.test(before) || /[|;&]\s*$/.test(before);
    var opts = [], self = this;
    if (isCmd && word.indexOf('/') === -1) {
      opts = Object.keys(COMMANDS).concat(Object.keys(DOCS)).filter(function (c, i, arr) { return arr.indexOf(c) === i && c.indexOf(word) === 0 && c !== '['; }).sort();
    } else {
      var slash = word.lastIndexOf('/'), dpart = slash >= 0 ? word.slice(0, slash + 1) : '', base = word.slice(slash + 1);
      var node = this.lookup(this.abs(dpart || '.'));
      if (node && node.t === 'd') {
        opts = Object.keys(node.c).filter(function (k) { return k.indexOf(base) === 0 && (base[0] === '.' || k[0] !== '.'); }).sort(sortNames).map(function (k) {
          var c = node.c[k], tgt = c.t === 'l' ? self.lookup(self.abs(dpart + k)) : c;
          return dpart + k + (tgt && tgt.t === 'd' ? '/' : '');
        });
      }
    }
    if (!opts.length) return { options: [], insert: '', word: word };
    var common = opts[0], i;
    for (i = 1; i < opts.length; i++) while (opts[i].indexOf(common) !== 0) common = common.slice(0, -1);
    var insert = common.slice(word.length);
    if (opts.length === 1 && opts[0].slice(-1) !== '/') insert += ' ';
    return { options: opts, insert: insert, word: word };
  };

  /* ---------- Doğrulama ---------- */
  // check: nesne (tüm anahtarlar sağlanmalı) veya dizi (hepsi) ; log: sh.log
  function cmdMatches(rec, re, ok) {
    if (!new RegExp(re).test(rec.cmd)) return false;
    if (ok === true) return rec.status === 0;
    if (ok === false) return rec.status !== 0;
    return true;
  }
  function verifyOne(sh, c) {
    var log = sh.log, k, ok = true;
    if (typeof c === 'function') return !!c(sh);
    if (Array.isArray(c)) return c.every(function (x) { return verifyOne(sh, x); });
    if (c.cmd !== undefined) ok = ok && log.some(function (r) { return cmdMatches(r, c.cmd, c.ok); });
    if (c.seq) {
      var idx = 0;
      log.forEach(function (r) { if (idx < c.seq.length && cmdMatches(r, c.seq[idx], c.ok)) idx++; });
      ok = ok && idx === c.seq.length;
    }
    if (c.out !== undefined) ok = ok && log.some(function (r) { return (!c.of || new RegExp(c.of).test(r.cmd)) && new RegExp(c.out).test(r.out); });
    if (c.exists) { var n = sh.lookup(sh.abs(c.exists), !!c.link); ok = ok && !!n && (!c.type || n.t === c.type); }
    if (c.absent) ok = ok && !sh.lookup(sh.abs(c.absent), true);
    if (c.contains) { var f = sh.lookup(sh.abs(c.contains[0])); ok = ok && !!f && f.t === 'f' && new RegExp(c.contains[1]).test(f.data); }
    if (c.equals) { var g = sh.lookup(sh.abs(c.equals[0])); ok = ok && !!g && g.t === 'f' && g.data === c.equals[1]; }
    if (c.mode) { var h = sh.lookup(sh.abs(c.mode[0])); ok = ok && !!h && (h.mode & 4095).toString(8) === c.mode[1]; }
    if (c.owner) { var o = sh.lookup(sh.abs(c.owner[0])); ok = ok && !!o && o.owner === c.owner[1] && (!c.owner[2] || o.group === c.owner[2]); }
    if (c.cwd) ok = ok && sh.cwd === sh.abs(c.cwd);
    if (c.linesMin) { var l = sh.lookup(sh.abs(c.linesMin[0])); ok = ok && !!l && l.t === 'f' && lines(l.data).length >= c.linesMin[1]; }
    return ok;
  }

  return {
    Shell: Shell,
    verify: verifyOne,
    docs: DOCS,
    commands: COMMANDS,
    tokenize: tokenize
  };
});
