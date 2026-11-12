/* terminal-ui.js — terminal panel for module pages. Scrollback persists per module (shared across languages). */
(function () {
  'use strict';
  var T = window.TLA, store = T.store, ui = T.cfg.ui;
  var panel = document.getElementById('term'), out = document.getElementById('termout');
  var input = document.getElementById('terminput'), promptEl = document.getElementById('termprompt');
  var mid = T.cfg.module, KEY = 'out:' + mid;
  var scroll = [], shell = null, onRun = null, hist = -1, draft = '';
  try { scroll = JSON.parse(store.get(KEY) || '[]'); } catch (e) { scroll = []; }

  function line(text, cls, persist) {
    var d = document.createElement('span');
    if (cls) d.className = cls;
    d.textContent = text;
    out.appendChild(d);
    if (persist !== false) {
      scroll.push([text, cls || '']);
      if (scroll.length > 300) scroll = scroll.slice(-300);
      store.set(KEY, JSON.stringify(scroll));
    }
    out.scrollTop = out.scrollHeight;
  }
  function promptText() {
    var c = shell.cwd, h = shell.user.home;
    if (c === h) c = '~'; else if (c.indexOf(h + '/') === 0) c = '~' + c.slice(h.length);
    return shell.user.name + '@linux-lab:' + c + (shell.user.name === 'root' ? '# ' : '$ ');
  }
  function refreshPrompt() { promptEl.textContent = promptText(); }
  function clearAll() { out.textContent = ''; scroll = []; store.set(KEY, '[]'); }

  function exec(cmd) {
    line(promptText() + cmd + '\n', 'p');
    var r = shell.run(cmd);
    r.chunks.forEach(function (c) {
      if (c.s === '\u001b[clear]') { clearAll(); return; }
      line(c.s, c.e ? 'e' : '');
    });
    if (r.chunks.length && !/\n$/.test(r.chunks[r.chunks.length - 1].s)) line('\n', '', false);
    refreshPrompt();
    if (onRun) onRun(cmd, r);
  }

  function setOpen(open) {
    panel.hidden = !open;
    document.body.classList.toggle('term-open', open);
    document.getElementById('termbtn').setAttribute('aria-expanded', open ? 'true' : 'false');
    store.set('term', open ? '1' : '0');
    if (open) { input.focus({ preventScroll: true }); out.scrollTop = out.scrollHeight; }
  }

  input.addEventListener('keydown', function (e) {
    var h = shell.history;
    if (e.key === 'Enter') {
      var v = input.value; input.value = ''; hist = -1;
      exec(v);
    } else if (e.key === 'ArrowUp') {
      e.preventDefault();
      if (!h.length) return;
      if (hist === -1) { draft = input.value; hist = h.length; }
      if (hist > 0) hist--;
      input.value = h[hist];
    } else if (e.key === 'ArrowDown') {
      e.preventDefault();
      if (hist === -1) return;
      hist++;
      if (hist >= h.length) { hist = -1; input.value = draft; } else input.value = h[hist];
    } else if (e.key === 'Tab') {
      e.preventDefault();
      var r = shell.complete(input.value);
      if (r.insert) input.value = input.value.slice(0, input.value.length - r.word.length) + r.insert;
      else if (r.options && r.options.length > 1) { line(promptText() + input.value + '\n', 'p', false); line(r.options.join('  ') + '\n', 'n', false); }
    } else if (e.ctrlKey && e.key.toLowerCase() === 'l') {
      e.preventDefault(); clearAll();
    } else if (e.ctrlKey && e.key.toLowerCase() === 'c') {
      e.preventDefault(); line(promptText() + input.value + '^C\n', 'p', false); input.value = '';
    }
  });
  out.addEventListener('click', function () { if (!getSelection().toString()) input.focus({ preventScroll: true }); });
  document.getElementById('termbtn').addEventListener('click', function () { setOpen(panel.hidden); });
  document.getElementById('termclose').addEventListener('click', function () { setOpen(false); });
  document.addEventListener('click', function (e) {
    var o = e.target.closest('[data-openterm]');
    if (o) { setOpen(true); return; }
    var b = e.target.closest('[data-try]');
    if (!b) return;
    setOpen(true);
    input.value = b.getAttribute('data-try');
    input.focus();
  });

  window.TLATerm = {
    attach: function (sh, cb) {
      shell = sh; onRun = cb;
      scroll.forEach(function (s) { line(s[0], s[1], false); });
      if (!scroll.length) line(ui.welcome + '\n\n', 'n', true);
      refreshPrompt();
      if (store.get('term') === '1') setOpen(true);
    },
    clear: clearAll,
    refreshPrompt: refreshPrompt
  };
})();
