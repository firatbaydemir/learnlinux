/* core.js — shared by index and module pages: store, theme, language switcher, learning path. */
(function () {
  'use strict';
  var P = 'tla3:';
  var store = {
    get: function (k) { try { return localStorage.getItem(P + k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(P + k, v); } catch (e) {} },
    del: function (k) { try { localStorage.removeItem(P + k); } catch (e) {} }
  };
  var cfgEl = document.getElementById('tla-config');
  var cfg = cfgEl ? JSON.parse(cfgEl.textContent) : {};

  function doneCount(mid, tasks) {
    var n = 0;
    tasks.forEach(function (t) { if (store.get('p:' + mid + ':' + t) === '1') n++; });
    return n;
  }

  // Theme
  var tb = document.getElementById('themebtn');
  if (tb) tb.addEventListener('click', function () {
    var cur = document.documentElement.dataset.theme ||
      (window.matchMedia && matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    var nx = cur === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = nx;
    store.set('theme', nx);
  });

  // Language switcher: same page in another language; keeps #hash or scroll position.
  var sw = document.getElementById('langsw');
  var page = location.pathname.split('/').pop() || 'index.html';
  if (sw) {
    sw.addEventListener('click', function (ev) {
      var a = ev.target.closest('a[data-switch]');
      if (!a) return;
      store.set('lang', a.getAttribute('data-switch'));
      try {
        var max = document.documentElement.scrollHeight - window.innerHeight;
        sessionStorage.setItem('tla3:scroll', JSON.stringify({ page: page, r: max > 0 ? window.scrollY / max : 0 }));
      } catch (e) {}
      if (location.hash) a.href = a.getAttribute('href').split('#')[0] + location.hash;
    });
    try {
      var s = JSON.parse(sessionStorage.getItem('tla3:scroll') || 'null');
      if (s && s.page === page && !location.hash) {
        sessionStorage.removeItem('tla3:scroll');
        window.addEventListener('load', function () {
          var max = document.documentElement.scrollHeight - window.innerHeight;
          document.documentElement.style.scrollBehavior = 'auto';
          window.scrollTo(0, s.r * max);
          document.documentElement.style.scrollBehavior = '';
        });
      }
    } catch (e) {}
  }

  // Index: learning path
  if (document.body.classList.contains('page-index')) {
    var ids = cfg.ids || {}, tot = 0, done = 0;
    var firstOpen = null, last = store.get('last');
    cfg.built.forEach(function (m) {
      var names = ids[m] || [];
      var d = doneCount(m, names), n = names.length;
      tot += n; done += d;
      var li = document.querySelector('.mod[data-id="' + m + '"]');
      if (li) {
        li.querySelector('.pct').textContent = n ? d + '/' + n : '';
        if (n && d === n) li.classList.add('done');
      }
      if (!firstOpen && d < n) firstOpen = m;
    });
    var target = (last && cfg.built.indexOf(last) >= 0) ? last : (firstOpen || cfg.built[0]);
    var cont = document.getElementById('continue');
    if (cont && target) {
      cont.href = 'modul-' + target + '.html';
      if (last || done) cont.textContent = cfg.ui['continue'] + ' → ' + target;
    }
    var pct = tot ? Math.round(100 * done / tot) : 0;
    document.getElementById('totalbar').style.width = pct + '%';
    document.getElementById('totaltxt').textContent = cfg.ui.overall + ': ' + done + '/' + tot + ' (' + pct + '%)';
    var inp = document.getElementById('search');
    inp.addEventListener('input', function () {
      var q = inp.value.trim().toLowerCase(), shown = 0;
      var escaped = q.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      var match = q ? new RegExp('(^|[^\\p{L}\\p{N}_])' + escaped + '(?=$|[^\\p{L}\\p{N}_])', 'u') : null;
      document.querySelectorAll('.mod').forEach(function (li) {
        var ok = !q || li.getAttribute('data-q').indexOf(q) >= 0 ||
          match.test(li.getAttribute('data-commands') || '');
        li.hidden = !ok; if (ok) shown++;
      });
      document.querySelectorAll('.level').forEach(function (s) { s.hidden = !s.querySelector('.mod:not([hidden])'); });
      document.getElementById('noresult').hidden = shown > 0;
    });
  }
  // Copy buttons and table-of-contents highlight
  document.addEventListener('click', function (e) {
    var b = e.target.closest('.copy');
    if (!b) return;
    var txt = b.getAttribute('data-copy'), old = b.textContent;
    var done = function () { b.textContent = cfg.ui.copied; setTimeout(function () { b.textContent = old; }, 1500); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(txt).then(done, done);
    else { var ta = document.createElement('textarea'); ta.value = txt; document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); } catch (x) {} ta.remove(); done(); }
  });
  var tocLinks = document.querySelectorAll('.toc a');
  if (tocLinks.length && 'IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) {
        if (en.isIntersecting) tocLinks.forEach(function (a) { a.classList.toggle('active', a.getAttribute('href') === '#' + en.target.id); });
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    tocLinks.forEach(function (a) { var t = document.getElementById(a.getAttribute('href').slice(1)); if (t) io.observe(t); });
  }
  window.TLA = { store: store, cfg: cfg, doneCount: doneCount };
})();
