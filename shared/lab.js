/* lab.js — virtual shell per module, automatic task verification (latched), quiz and progress. */
(function () {
  'use strict';
  var T = window.TLA, store = T.store, cfg = T.cfg, ui = cfg.ui, mid = cfg.module;
  var E = window.TLAEngine;
  var shell = new E.Shell({ lang: cfg.lang });
  var SK = 'sh:' + mid;
  var saved = store.get(SK);
  try { if (saved) shell.restore(saved); else shell.reset(cfg.setup); } catch (e) { shell.reset(cfg.setup); }
  shell.lang = cfg.lang;
  store.set('last', mid);

  var tasks = cfg.tasks, vms = cfg.vm || [];
  function pk(id) { return 'p:' + mid + ':' + id; }
  var allIds = tasks.map(function (t) { return t.id; }).concat(vms.map(function (v) { return v.id; }));

  function setGroup(g, d, n) {
    var el = document.querySelector('.gcount[data-g="' + g + '"]');
    if (el) el.textContent = d + '/' + n + ' ' + ui.groupDone;
  }
  function renderProgress() {
    var n = 0, groups = {};
    tasks.forEach(function (t) {
      var done = store.get(pk(t.id)) === '1';
      if (done) n++;
      var g = groups[t.kind] = groups[t.kind] || [0, 0];
      g[1]++; if (done) g[0]++;
      var li = document.querySelector('.task[data-task="' + t.id + '"]');
      if (li) li.classList.toggle('done', done);
    });
    var vd = 0;
    vms.forEach(function (v) {
      var done = store.get(pk(v.id)) === '1';
      if (done) { n++; vd++; }
      var el = document.querySelector('.vmt[data-vm="' + v.id + '"]');
      if (el) {
        el.classList.toggle('done', done);
        var u = el.querySelector('.undo'), d = el.querySelector('.done.btn, button.done');
        if (u) u.hidden = !done;
        if (d) d.hidden = done;
      }
    });
    Object.keys(groups).forEach(function (g) { setGroup(g, groups[g][0], groups[g][1]); });
    if (vms.length) setGroup('vm', vd, vms.length);
    var total = allIds.length || 1;
    document.getElementById('modbar').style.width = Math.round(100 * n / total) + '%';
    document.getElementById('modtxt').textContent = n + '/' + allIds.length + ' ' + ui.tasksDone + (n === allIds.length ? ' — ' + ui.moduleDone : '');
    return n;
  }

  function verifyAll(announce) {
    tasks.forEach(function (t) {
      if (store.get(pk(t.id)) === '1') return;
      var ok = false;
      try { ok = E.verify(shell, t.check); } catch (e) { ok = false; }
      if (ok) {
        store.set(pk(t.id), '1');
        if (announce) window.TLATermNote('✔ ' + ui.taskDone + ': ' + t.id + '\n');
      }
    });
    renderProgress();
  }
  window.TLATermNote = function (s) {
    var o = document.getElementById('termout');
    var d = document.createElement('span'); d.className = 'p'; d.textContent = s; o.appendChild(d); o.scrollTop = o.scrollHeight;
  };

  window.TLATerm.attach(shell, function () {
    store.set(SK, shell.serialize());
    verifyAll(true);
  });
  // Tasks may be satisfied by a restored session (e.g. progress made on another language page).
  verifyAll(false);

  var rl = document.getElementById('resetlab');
  if (rl) rl.addEventListener('click', function () {
    if (!confirm(ui.resetConfirm)) return;
    shell.reset(cfg.setup);
    store.del(SK);
    window.TLATerm.clear();
    window.TLATerm.refreshPrompt();
    window.TLATermNote(ui.welcome + '\n\n');
  });

  // VM tasks: pasted output is matched locally against a pattern, or the learner confirms.
  vms.forEach(function (v) {
    var el = document.querySelector('.vmt[data-vm="' + v.id + '"]');
    if (!el) return;
    var fb = el.querySelector('.fb');
    var chk = el.querySelector('.check'), dn = el.querySelector('button.done'), un = el.querySelector('.undo');
    if (chk) chk.addEventListener('click', function () {
      var txt = el.querySelector('textarea').value, ok = false;
      try { ok = txt.trim().length > 0 && new RegExp(v.expect, 'i').test(txt); } catch (e) { ok = false; }
      fb.textContent = ok ? ui.pasteOk : ui.pasteBad;
      fb.className = 'fb ' + (ok ? 'ok' : 'bad');
      if (ok) { store.set(pk(v.id), '1'); renderProgress(); }
    });
    if (dn) dn.addEventListener('click', function () { store.set(pk(v.id), '1'); renderProgress(); });
    if (un) un.addEventListener('click', function () { store.del(pk(v.id)); renderProgress(); });
  });

  // Quiz
  document.querySelectorAll('.q').forEach(function (q) {
    var id = q.getAttribute('data-q'), ans = cfg.quiz[id], key = 'q:' + mid + ':' + id;
    var ex = q.querySelector('.explain');
    var opts = q.querySelectorAll('.opt');
    if (store.get(key) === '1') { opts[ans].classList.add('right'); ex.hidden = false; }
    opts.forEach(function (b) {
      b.addEventListener('click', function () {
        if (+b.getAttribute('data-i') === ans) {
          b.classList.add('right'); ex.hidden = false; store.set(key, '1');
        } else { b.classList.add('wrong'); b.setAttribute('aria-label', ui.wrong); }
      });
    });
  });

  renderProgress();
})();
