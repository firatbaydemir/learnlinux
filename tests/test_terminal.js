/* Terminal motoru testi. Çalıştırma: node v3/tests/test_terminal.js  veya  jsc v3/shared/terminal.js v3/tests/test_terminal.js */
var E = (typeof require === 'function' && typeof module === 'object') ? require('../shared/terminal.js') : TLAEngine;
var log = typeof print === 'function' ? print : console.log;
var fails = 0, total = 0;

function sh() { return new E.Shell({ lang: 'en' }); }
function run(s, line) {
  var r = s.run(line);
  return { out: r.chunks.map(function (c) { return c.s; }).join(''), status: r.status };
}
function eq(name, got, want) {
  total++;
  if (got !== want) { fails++; log('FAIL ' + name + '\n  got:  ' + JSON.stringify(got) + '\n  want: ' + JSON.stringify(want)); }
}
function t(name, line, wantOut, wantStatus, s) {
  s = s || sh();
  var r = run(s, line);
  eq(name + ' out', r.out, wantOut);
  eq(name + ' status', r.status, wantStatus == null ? 0 : wantStatus);
  return s;
}

t('pwd', 'pwd', '/home/student\n');
t('whoami', 'whoami', 'student\n');
t('echo', 'echo "a  b" c', 'a  b c\n');
t('echo var', 'echo $USER $HOME', 'student /home/student\n');
t('echo single', "echo '$USER'", '$USER\n');
t('unknown', 'foobar', 'foobar: command not found\n', 127);
t('cd err', 'cd /yok', 'bash: cd: /yok: No such file or directory\n', 1);
t('id', 'id', 'uid=1000(student) gid=1000(student) groups=1000(student),10(wheel),2000(devs)\n');
t('uname', 'uname -r', '5.14.0-427.el9.x86_64\n');

var s = sh();
run(s, 'cd /tmp'); eq('cd tmp', run(s, 'pwd').out, '/tmp\n');
run(s, 'cd ..'); eq('cd ..', run(s, 'pwd').out, '/\n');
run(s, 'cd ~'); eq('cd ~', run(s, 'pwd').out, '/home/student\n');
run(s, 'cd /etc'); run(s, 'cd /tmp'); eq('cd -', run(s, 'cd -').out, '/etc\n');
run(s, 'cd'); eq('cd bare', run(s, 'pwd').out, '/home/student\n');

s = sh();
run(s, 'mkdir -p practice/a/b'); eq('mkdir -p', run(s, 'ls -R practice').out, 'practice:\na\n\npractice/a:\nb\n\npractice/a/b:\n');
eq('rmdir nonempty', run(s, 'rmdir practice').status, 1);
eq('rm dir no -r', run(s, 'rm practice').status, 1);
eq('rm -r', run(s, 'rm -r practice').status, 0);
eq('gone', run(s, 'ls practice').status, 2);
run(s, 'touch {a,b,c}.txt'); eq('brace', run(s, 'ls *.txt').out, 'a.txt  b.txt  c.txt  notes.txt\n');
eq('glob', run(s, 'echo ?.txt').out, 'a.txt b.txt c.txt\n');
eq('rm root', run(s, 'rm -rf /').status, 1);
eq('root intact', run(s, 'ls /').status, 0);

s = sh();
run(s, 'echo hello > f.txt'); run(s, 'echo world >> f.txt');
eq('redirect', run(s, 'cat f.txt').out, 'hello\nworld\n');
run(s, 'echo new > f.txt'); eq('overwrite', run(s, 'cat f.txt').out, 'new\n');
eq('2>', run(s, 'ls /yok 2> err.txt').out, '');
eq('2> content', run(s, 'cat err.txt').out, "ls: cannot access '/yok': No such file or directory\n");
eq('/dev/null', run(s, 'ls /yok 2> /dev/null').out, '');
eq('pipe', run(s, 'cat /etc/passwd | grep root | wc -l').out, '1\n');
eq('cut', run(s, 'cat /etc/passwd | cut -d: -f1 | head -n 2').out, 'root\nbin\n');
eq('sort uniq', run(s, 'printf "b\\na\\nb\\n" | sort | uniq -c').out, '      1 a\n      2 b\n');
eq('sort key', run(s, 'printf "name cpu\\nalice 2\\nbob 10\\n" | sort -k2 -nr').out, 'bob 10\nalice 2\nname cpu\n');
eq('grep -i', run(s, 'grep -i ERROR /var/log/messages | wc -l').out, '3\n');
eq('grep -c', run(s, 'grep -c conf /etc/hosts').out, '0\n');
eq('grep -q match', run(s, 'grep -q root /etc/passwd').out, '');
eq('grep -q status', run(s, 'grep -q root /etc/passwd').status, 0);
eq('grep -q miss', run(s, 'grep -q missing /etc/passwd').status, 1);
eq('grep status', run(s, 'grep zzz /etc/hosts').status, 1);
eq('tr delete escape', run(s, "printf 'a\\rb\\n' | tr -d '\\r'").out, 'ab\n');
eq('tr squeeze', run(s, "printf 'a  b\\n' | tr -s ' '").out, 'a b\n');
run(s, 'mkdir -p listdir'); run(s, 'touch listdir/a listdir/b');
eq('ls one per line in pipe', run(s, 'ls -1 listdir | wc -l').out, '2\n');
eq('tee', run(s, 'echo x | tee t.txt').out, 'x\n');
eq('tee file', run(s, 'cat t.txt').out, 'x\n');
eq('$?', run(s, 'false; echo $?').out, '1\n');
eq('&&', run(s, 'false && echo no').out, '');
eq('||', run(s, 'false || echo yes').out, 'yes\n');
eq('subst', run(s, 'echo $(whoami)').out, 'student\n');
eq('var assign', run(s, 'X=5; echo $X').out, '5\n');
eq('head', run(s, 'head -n 1 /etc/passwd').out, 'root:x:0:0:root:/root:/bin/bash\n');
eq('tail', run(s, 'tail -n 1 /etc/hostname').out, 'linux-lab\n');
eq('wc', run(s, 'wc -l /etc/hostname').out, '1 /etc/hostname\n');
eq('cat missing', run(s, 'cat /nope').out, 'cat: /nope: No such file or directory\n');
eq('shadow denied', run(s, 'cat /etc/shadow').out, 'cat: /etc/shadow: Permission denied\n');
eq('sudo shadow', run(s, 'sudo cat /etc/shadow | wc -l').out, '2\n');
eq('syntax', run(s, 'echo "abc').status, 2);

s = sh();
run(s, 'echo "echo Hello" > script.sh');
eq('no x', run(s, './script.sh').out, 'bash: ./script.sh: Permission denied\n');
eq('no x status', run(s, './script.sh').status, 126);
run(s, 'chmod 755 script.sh'); eq('x ok', run(s, './script.sh').out, 'Hello\n');
run(s, 'chmod 600 script.sh'); eq('ls -l perm', /^-rw-------/.test(run(s, 'ls -l script.sh').out), true);
run(s, 'chmod u+x script.sh'); eq('u+x', /^-rwx------/.test(run(s, 'ls -l script.sh').out), true);
run(s, 'touch belge.txt'); run(s, 'chmod g-r belge.txt'); eq('g-r', /^-rw----r--/.test(run(s, 'ls -l belge.txt').out), true);
eq('umask', run(s, 'umask').out, '0022\n');
eq('chown denied', run(s, 'chown root belge.txt').status, 1);
run(s, 'sudo chown root belge.txt'); eq('chown sudo', /root student/.test(run(s, 'ls -l belge.txt').out), true);
eq('write denied', run(s, 'echo x >> belge.txt').status, 1);
run(s, 'mkdir gizli'); run(s, 'chmod 700 gizli'); eq('ls -ld', /^drwx------/.test(run(s, 'ls -ld gizli').out), true);

s = sh();
run(s, 'cp /etc/hostname h.bak'); eq('cp', run(s, 'cat h.bak').out, 'linux-lab\n');
run(s, 'mkdir k'); eq('cp dir no -r', run(s, 'cp k k2').status, 1);
eq('cp -r', run(s, 'cp -r k k2').status, 0);
run(s, 'mv h.bak k2/'); eq('mv', run(s, 'ls k2').out, 'h.bak\n');
run(s, 'ln -s /etc/os-release sis'); eq('symlink', /^lrwx.* sis -> \/etc\/os-release/m.test(run(s, 'ls -l sis').out), true);
eq('verify symlink type', E.verify(s, { exists: 'sis', type: 'l', link: true }), true);
eq('cat symlink', /Red Hat/.test(run(s, 'cat sis').out), true);
run(s, 'touch o.txt'); run(s, 'ln o.txt hard'); eq('hardlink count', /^-rw-r--r-- 2/.test(run(s, 'ls -l hard').out), true);
eq('find', run(s, 'find . -name "*.txt"').out.indexOf('./o.txt') >= 0, true);
eq('man', /SYNOPSIS/.test(run(s, 'man ls').out), true);
eq('help flag', /^Usage: ls/.test(run(s, 'ls --help').out), true);
eq('history', /1  mkdir k|cp \/etc\/hostname/.test(run(s, 'history').out), true);
eq('unsupported', run(s, 'sed x').status, 127);

// Tab tamamlama
s = sh();
eq('complete cmd', s.complete('whoa').insert, 'mi ');
eq('complete path', s.complete('cat /etc/os-r').insert, 'elease ');
eq('complete dir', s.complete('cd Docu').insert, 'ments/');
eq('complete multi', s.complete('ls /e').options.indexOf('/etc/') >= 0, true);

// Seri hale getirme
s = sh(); run(s, 'mkdir x'); run(s, 'cd x');
var s2 = sh(); s2.restore(s.serialize());
eq('restore cwd', s2.cwd, '/home/student/x');
eq('restore log', s2.log.length, 2);

// Doğrulayıcı
s = sh();
run(s, 'mkdir -p a/b'); run(s, 'touch a/b/f.txt'); run(s, 'chmod 640 a/b/f.txt');
eq('verify exists', E.verify(s, { exists: 'a/b/f.txt', type: 'f' }), true);
eq('verify mode', E.verify(s, { mode: ['a/b/f.txt', '640'] }), true);
eq('verify cmd', E.verify(s, { cmd: '^touch a/b/f\\.txt$', ok: true }), true);
eq('verify seq', E.verify(s, { seq: ['^mkdir', '^touch', '^chmod'] }), true);
eq('verify seq order', E.verify(s, { seq: ['^chmod', '^mkdir'] }), false);
eq('verify absent', E.verify(s, { absent: 'nope' }), true);
run(s, 'rmdir a'); eq('verify cmd fail', E.verify(s, { cmd: '^rmdir a$', ok: false }), true);

log(fails ? ('FAILED ' + fails + '/' + total) : ('OK ' + total + ' assertions'));
if (typeof process !== 'undefined' && fails) process.exit(1);
