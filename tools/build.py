#!/usr/bin/env python3
"""Builds the static pages and PWA precache manifest. Run: python3 tools/build.py"""
import hashlib
import html
import json
import re
from pathlib import Path

V3 = Path(__file__).resolve().parent.parent
CONTENT = V3 / "content"
LANGS = ["tr", "de", "en"]
LANG_NAMES = {"tr": "Türkçe", "de": "Deutsch", "en": "English"}
# UI keys needed by the browser runtime (lab.js / terminal-ui.js / core.js)
RUNTIME_UI = ["correct", "wrong", "taskDone", "moduleDone", "tasksDone", "welcome", "sandboxNote",
              "resetConfirm", "retryBadge", "retryBtn", "retryNote", "openTerminal", "closeTerminal", "continue", "startPath", "noResult", "soon", "overall"]


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def esc(s):
    return html.escape(str(s), quote=True)


def md(s):
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    return re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)


def mod_file(mid):
    return "modul-%s.html" % mid


def built_modules():
    return sorted(
        [d.name[1:] for d in CONTENT.iterdir() if d.is_dir() and d.name.startswith("m") and (d / "module.json").exists()],
        key=lambda x: [int(p) for p in x.split(".")])


def lang_switch(lang, page):
    links = []
    for l in LANGS:
        cur = ' aria-current="true"' if l == lang else ""
        links.append('<a href="../%s/%s" hreflang="%s" lang="%s" data-switch="%s"%s>%s</a>'
                     % (l, page, l, l, l, cur, l.upper()))
    return '<nav class="langsw" id="langsw" aria-label="Language">%s</nav>' % "".join(links)


def head(lang, title, depth_shared="../shared"):
    return ('<!doctype html>\n<html lang="%s">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width,initial-scale=1">\n<title>%s</title>\n'
            '<script>try{var t=localStorage.getItem("tla3:theme");if(t)document.documentElement.dataset.theme=t;'
            'localStorage.setItem("tla3:lang","%s")}catch(e){}</script>\n'
            '<meta name="theme-color" content="#060a08">\n'
            '<link rel="manifest" href="../manifest.webmanifest">\n'
            '<link rel="icon" href="../icons/icon.svg" type="image/svg+xml">\n'
            '<link rel="apple-touch-icon" href="../icons/icon-192.png">\n'
            '<script defer src="%s/pwa.js"></script>\n'
            '<link rel="stylesheet" href="%s/app.css">\n</head>\n') % (
                lang, esc(title), lang, depth_shared, depth_shared)



_P = {
    "sprout": '<path d="M12 21v-9"/><path d="M12 12c0-4 3-6 7-6 0 4-3 6-7 6Z"/><path d="M12 14c0-3-2-5-6-5 0 3 2 5 6 5Z"/>',
    "terminal": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="m7 9 3 3-3 3M13 15h4"/>',
    "folder": '<path d="M3 7a2 2 0 0 1 2-2h4l2 2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2Z"/>',
    "file": '<path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8Z"/><path d="M14 3v5h5M9 13h6M9 17h6"/>',
    "lock": '<rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/>',
    "gear": '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1 7 17M17 7l2.1-2.1"/>',
    "wrench": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.2L3 17.8V21h3.2l6.3-6.3a4 4 0 0 0 5.2-5.4l-2.6 2.6-2.4-.6-.6-2.4Z"/>',
    "book": '<path d="M4 5a2 2 0 0 1 2-2h13v16H6a2 2 0 0 0-2 2Z"/><path d="M4 19V5M9 7h6"/>',
    "flame": '<path d="M12 3c1 4 5 5 5 10a5 5 0 0 1-10 0c0-2 1-3 2-4 0 2 1 3 2 3 0-4-1-6 1-9Z"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5Z"/>',
    "eye": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12Z"/><circle cx="12" cy="12" r="3"/>',
    "bug": '<rect x="8" y="8" width="8" height="12" rx="4"/><path d="M9 8a3 3 0 0 1 6 0M4 13h4M16 13h4M5 7l3 3M19 7l-3 3M5 20l3-3M19 20l-3-3"/>',
    "puzzle": '<path d="M10 4a2 2 0 1 1 4 0v2h4v4h-2a2 2 0 1 0 0 4h2v6h-6v-2a2 2 0 1 0-4 0v2H4v-6h2a2 2 0 1 0 0-4H4V6h6Z"/>',
    "trophy": '<path d="M8 4h8v6a4 4 0 0 1-8 0Z"/><path d="M8 6H4v2a3 3 0 0 0 4 3M16 6h4v2a3 3 0 0 1-4 3M12 14v4M8 21h8M10 18h4"/>',
    "ticket": '<path d="M3 8a2 2 0 0 0 0 8v2h18v-2a2 2 0 0 1 0-8V6H3Z"/><path d="M14 6v12" stroke-dasharray="2 2"/>',
    "bulb": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.7.7 1 1.5 1 2.5h6c0-1 .3-1.8 1-2.5A6 6 0 0 0 12 3Z"/>',
    "warn": '<path d="M12 3 2 20h20Z"/><path d="M12 10v5M12 17.5v.5"/>',
    "danger": '<circle cx="12" cy="12" r="9"/><path d="m5.6 5.6 12.8 12.8"/>',
    "target": '<circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/>',
    "monitor": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
    "flask": '<path d="M9 3h6M10 3v6L4.5 19a1.5 1.5 0 0 0 1.3 2h12.4a1.5 1.5 0 0 0 1.3-2L14 9V3"/><path d="M7.5 15h9"/>',
    "help": '<circle cx="12" cy="12" r="9"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.7.4-1 1-1 1.7M12 17v.5"/>',
    "check": '<circle cx="12" cy="12" r="9"/><path d="m8 12.5 3 3 5-6"/>',
    "theme": '<circle cx="12" cy="12" r="9"/><path d="M12 3a9 9 0 0 0 0 18Z" fill="currentColor"/>',
    "close": '<path d="M6 6l12 12M18 6 6 18"/>',
    "play": '<path d="M7 5v14l12-7Z"/>',
    "arrow-r": '<path d="M5 12h14m-6-6 6 6-6 6"/>',
    "arrow-l": '<path d="M19 12H5m6-6-6 6 6 6"/>',
}


def icon(name, cls="ico"):
    return '<svg class="%s" viewBox="0 0 24 24" aria-hidden="true" focusable="false">%s</svg>' % (cls, _P[name])


def _ic(s):
    return re.sub(r"@@([a-z-]+)@@", lambda m: icon(m.group(1)), s)


def ih(name, text):
    """icon + text for headings"""
    return icon(name) + " " + text

LEVEL_ICON = {"0": "sprout", "1": "terminal", "2": "folder", "3": "file", "4": "lock", "5": "gear", "6": "wrench"}
KIND_ICON = {"warmup": "flame", "guided": "compass", "predict": "eye", "debug": "bug", "mini": "puzzle", "challenge": "trophy", "ticket": "ticket"}


def topbar(lang, ui, page, extra=""):
    return _ic('<header class="top"><a class="brand" href="index.html">' + linux_icon() + '<span>%s</span></a>'
            '<div class="topr">%s%s<button type="button" class="ibtn" id="themebtn" title="%s" aria-label="%s">@@theme@@</button></div></header>\n'
            % (esc(ui["siteName"]), extra, lang_switch(lang, page), esc(ui["theme"]), esc(ui["theme"])))


def linux_icon():
    return ('<svg class="tux-icon" viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">'
                        '<ellipse cx="84" cy="220" rx="30" ry="11" fill="#f5a623" stroke="#b8730f" stroke-width="2"/>'
            '<ellipse cx="156" cy="220" rx="30" ry="11" fill="#f5a623" stroke="#b8730f" stroke-width="2"/>'
            '<ellipse cx="46" cy="150" rx="13" ry="40" transform="rotate(18 46 150)" fill="#23262e" stroke="#4a505e" stroke-width="2"/>'
            '<ellipse cx="194" cy="150" rx="13" ry="40" transform="rotate(-18 194 150)" fill="#23262e" stroke="#4a505e" stroke-width="2"/>'
            '<path fill="#23262e" stroke="#4a505e" stroke-width="3" stroke-linejoin="round" d="M120 18c-34 0-52 28-52 62 0 18-4 30-14 44-14 20-22 42-22 64 0 24 20 34 44 34h88c24 0 44-10 44-34 0-22-8-44-22-64-10-14-14-26-14-44 0-34-18-62-52-62Z"/>'
            '<path fill="#f4f1e8" d="M120 92c-30 0-48 30-48 68 0 36 18 56 48 56s48-20 48-56c0-38-18-68-48-68Z"/>'
            '<path fill="#ffffff" opacity=".14" d="M96 30c-14 8-22 22-24 40 6-14 16-24 30-30Z"/>'
            '<path fill="#dcd6c6" d="M120 150c-26 0-44 14-48 36 8 22 24 30 48 30s40-8 48-30c-4-22-22-36-48-36Z" opacity=".55"/>'
            '<ellipse cx="88" cy="84" rx="9" ry="6" fill="#ff8a7a" opacity=".35"/><ellipse cx="152" cy="84" rx="9" ry="6" fill="#ff8a7a" opacity=".35"/>'
            '<ellipse cx="103" cy="62" rx="10" ry="12" fill="#fff"/><ellipse cx="137" cy="62" rx="10" ry="12" fill="#fff"/>'
            '<ellipse cx="106" cy="64" rx="4.5" ry="6" fill="#111"/><ellipse cx="134" cy="64" rx="4.5" ry="6" fill="#111"/>'
            '<circle cx="108" cy="61" r="1.8" fill="#fff"/><circle cx="136" cy="61" r="1.8" fill="#fff"/>'
            '<path fill="#f5a623" stroke="#b8730f" stroke-width="2" stroke-linejoin="round" d="M94 80q26-14 52 0-4 14-26 16-22-2-26-16Z"/>'
            '<path fill="#e8901a" stroke="#b8730f" stroke-width="2" stroke-linejoin="round" d="M101 94q19 8 38 0-6 16-19 16t-19-16Z"/>'

            '</svg>')


def module_commands(lang, mid):
    translation = load(CONTENT / ("m" + mid) / (lang + ".json"))
    commands = []
    for section in translation["sections"]:
        for item in section.get("commands", []):
            command = item.get("cmd", "").strip().split()
            if command:
                commands.append(command[0])
    return " ".join(command for command in commands if command)


def build_index(lang, ui, mods_meta, built):
    levels = mods_meta["levels"]
    search_terms = {mid: module_commands(lang, mid) for mid in built}
    out = [head(lang, ui["siteName"]), '<body class="page-index">\n', topbar(lang, ui, "index.html"),
           '<main class="wrap index-wrap">\n',
           '<section class="hero"><div class="hero-copy"><p class="hero-kicker"><span></span>%s</p>'
           '<h1>%s</h1><p class="hero-description">%s</p><div class="heroact">'
           '<a class="btn primary" id="continue" href="#">%s %s</a>'
           '<input type="search" id="search" placeholder="%s" aria-label="%s"></div>'
           '<div class="hero-progress"><div class="bar" aria-hidden="true"><i id="totalbar"></i></div>'
           '<p class="muted" id="totaltxt"></p></div></div>'
           '<div class="hero-art" aria-hidden="true"><div class="hero-glow"></div>'
           '<div class="tux-mark">%s</div><div class="terminal-card">'
           '<div class="terminal-chrome"><i></i><i></i><i></i><span>terminal</span></div>'
           '<div class="terminal-lines"><p><span>~</span> uname -s</p><p class="terminal-output">Linux</p>'
           '<p><span>~</span> <b class="terminal-cursor"></b></p></div></div></div></section>\n'
           % (esc(ui["heroKicker"]), esc(ui["heroTitle"]), esc(ui["heroText"]), esc(ui["startPath"]), icon("arrow-r"),
              esc(ui["search"]), esc(ui["search"]), linux_icon())]
    out.append('<p id="noresult" class="muted" hidden>%s</p>\n' % esc(ui["noResult"]))
    for lv in sorted(levels, key=int):
        items = [m for m in mods_meta["modules"] if str(m["level"]) == lv]
        out.append('<section class="level" data-level="%s"><h2><span class="lvl-ico">%s</span>%s %s — %s</h2><ul class="mods">\n' % (lv, icon(LEVEL_ICON.get(lv, "book")), esc(ui["level"]), lv, esc(levels[lv][lang])))
        for m in items:
            t = m["title"][lang]
            if m["id"] in built:
                out.append('<li class="mod" data-id="%s" data-q="%s" data-commands="%s"><a href="%s"><b>%s</b> %s</a><span class="pct" data-pct="%s"></span></li>\n'
                           % (m["id"], esc((m["id"] + " " + t).lower()), esc(search_terms[m["id"]].lower()),
                              mod_file(m["id"]), m["id"], esc(t), m["id"]))
            else:
                out.append('<li class="mod soon" data-q="%s"><span><b>%s</b> %s</span><em>%s</em></li>\n'
                           % (esc((m["id"] + " " + t).lower()), m["id"], esc(t), esc(ui["soon"])))
        out.append("</ul></section>\n")
    ids = {}
    for m in built:
        mj = load(CONTENT / ("m" + m) / "module.json")
        ids[m] = [t["id"] for t in mj["tasks"]] + [v["id"] for v in mj.get("vm", [])]
    cfg = {"lang": lang, "built": built, "ids": ids, "order": [m["id"] for m in mods_meta["modules"]],
           "ui": {k: ui[k] for k in RUNTIME_UI}}
    out.append('</main>\n<script type="application/json" id="tla-config">%s</script>\n' % json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/"))
    out.append('<script src="../shared/core.js"></script>\n</body>\n</html>\n')
    return "".join(out)


KINDS = ["warmup", "guided", "predict", "debug", "mini", "challenge", "ticket"]
RUNTIME_UI += ["copied", "pasteOk", "pasteBad", "iDidIt", "undo", "groupDone", "vmDone"]
TOKEN = re.compile(r"(?P<c>#.*$)|(?P<s>\"[^\"]*\"|'[^']*')|(?P<o>\|\||&&|[|;<>]+)|(?P<w>\s+)|(?P<x>\S+)")


def hl(line):
    out, expect = [], True
    for m in TOKEN.finditer(line):
        t, k = m.group(0), m.lastgroup
        if k == "c":
            out.append('<span class="tc">%s</span>' % esc(t))
        elif k == "s":
            out.append('<span class="ts">%s</span>' % esc(t))
        elif k == "o":
            out.append('<span class="to">%s</span>' % esc(t)); expect = True
        elif k == "w":
            out.append(t)
        elif expect and not re.match(r"^[A-Za-z_]+=", t):
            out.append('<span class="tk">%s</span>' % esc(t)); expect = False
        elif re.match(r"^--?[A-Za-z]", t):
            out.append('<span class="tf">%s</span>' % esc(t))
        elif t.startswith(("$", "~", "/", "./")) or "/" in t:
            out.append('<span class="tp">%s</span>' % esc(t))
        else:
            out.append(esc(t))
    return "".join(out)


def code_block(text, ui, sim=False):
    lines = text.split("\n")
    body = "".join('<span class="ln">%s</span>\n' % hl(l) for l in lines)
    raw = "\n".join(re.sub(r"\s+#.*$", "", l) for l in lines)
    simbtn = _ic('<button type="button" class="try small" data-try="%s" title="%s">@@play@@ %s</button>' % (esc(text), esc(ui["tryHint"]), esc(ui["tryInSim"]))) if sim else ""
    return ('<div class="code"><pre><code>%s</code></pre><div class="codebtns">%s<button type="button" class="copy" data-copy="%s">%s</button></div></div>'
            % (body, simbtn, esc(raw), esc(ui["copy"])))


def callout(kind, label, text):
    icons = {"tip": icon("bulb"), "warn": icon("warn"), "danger": icon("danger")}
    return '<aside class="callout %s" role="note"><strong>%s %s</strong><p>%s</p></aside>\n' % (kind, icons[kind], esc(label), md(text))


def build_module(lang, ui, mods_meta, mid, built):
    mod = load(CONTENT / ("m" + mid) / "module.json")
    tx = load(CONTENT / ("m" + mid) / (lang + ".json"))
    meta = next(m for m in mods_meta["modules"] if m["id"] == mid)
    page = mod_file(mid)
    title = "%s %s — %s" % (mid, tx["title"], ui["siteName"])
    toggle = _ic('<button type="button" class="btn" id="termbtn" aria-expanded="false">@@terminal@@ %s</button>' % esc(ui["terminalOptional"]))
    toc = [(s["id"], s["title"]) for s in tx["sections"]]
    if mod.get("vm"):
        toc.append(("vm", ui["vmTitle"]))
    if mod["tasks"]:
        toc.append(("lab", ui["labTitle"]))
    toc += [("quiz", ui["quizTitle"]), ("summary", ui["summary"]), ("glossary", ui["glossary"])]
    toclinks = "".join('<li><a href="#%s">%s</a></li>' % (esc(i), esc(t)) for i, t in toc)
    o = [head(lang, title), '<body class="page-module" data-module="%s">\n' % mid, topbar(lang, ui, page, toggle),
         '<div class="topprog" role="progressbar" aria-label="%s"><i id="modbar"></i></div>\n' % esc(ui["overall"]),
         '<div class="layout">\n',
         '<aside class="toc" aria-label="%s"><strong>%s</strong><ol>%s</ol></aside>\n' % (esc(ui["toc"]), esc(ui["toc"]), toclinks),
         '<main class="content" id="main">\n']
    o.append('<details class="tocm"><summary>%s</summary><ol>%s</ol></details>\n' % (esc(ui["toc"]), toclinks))
    o.append('<div class="module-hero" data-level="%s"><div class="hero-tux" aria-hidden="true">%s</div><p class="crumb"><a href="index.html">%s</a> <span aria-hidden="true">/</span> %s %s</p>\n'
             '<h1><span class="module-id">%s</span> %s</h1>\n<p class="lead">%s</p>\n<p class="muted" id="modtxt"></p></div>\n'
             % (meta["level"], linux_icon(), esc(ui["home"]), esc(ui["level"]), meta["level"], mid, esc(tx["title"]), md(tx["lead"])))
    o.append('<section class="card" id="objectives"><h2>%s %s</h2><ul>%s</ul></section>\n'
             % (icon("target"), esc(ui["objectives"]), "".join("<li>%s</li>" % md(x) for x in tx["objectives"])))
    for sec in tx["sections"]:
        o.append('<section id="%s"><h2>%s</h2>\n' % (esc(sec["id"]), esc(sec["title"])))
        for p in sec["body"]:
            o.append("<p>%s</p>\n" % md(p))
        for c in sec.get("commands", []):
            o.append('<article class="cmd"><h3><code>%s</code></h3><dl>'
                     '<dt>%s</dt><dd>%s</dd><dt>%s</dt><dd>%s</dd><dt>%s</dt><dd>%s</dd></dl>%s</article>\n'
                     % (esc(c["cmd"]), esc(ui["what"]), md(c["what"]), esc(ui["where"]), md(c["where"]),
                        esc(ui["why"]), md(c["why"]), code_block(c["example"], ui, sim=not c.get("nosim"))))
        for k in ("tip", "warn", "danger"):
            if sec.get(k):
                o.append(callout(k, ui[k], sec[k]))
        o.append("</section>\n")
    vm = mod.get("vm", [])
    if vm:
        o.append('<section id="vm"><h2>%s %s <span class="gcount" data-g="vm"></span></h2><p>%s</p><p>%s</p>\n' % (icon("monitor"), esc(ui["vmTitle"]), md(ui["vmIntro"]), md(tx["vm"]["intro"])))
        for v in vm:
            t = tx["vm"]["tasks"][v["id"]]
            o.append('<article class="vmt card" data-vm="%s" data-expect="%d"><header><h3>%s</h3><span class="status" aria-hidden="true"></span></header><p>%s</p>\n'
                     % (v["id"], 1 if v["expect"] else 0, esc(t["title"]), md(t["text"])))
            for b in t["blocks"]:
                o.append(code_block(b["cmd"], ui))
                if b.get("expected"):
                    o.append('<p class="lbl">%s</p><pre class="out">%s</pre>\n' % (esc(ui["expected"]), esc(b["expected"])))
            if t.get("differs"):
                o.append('<details class="differs"><summary>%s</summary><ul>%s</ul></details>\n' % (esc(ui["differs"]), "".join("<li>%s</li>" % md(x) for x in t["differs"])))
            if v["expect"]:
                o.append('<label class="lbl">%s</label><textarea rows="4" spellcheck="false"></textarea><p><button type="button" class="btn check">%s</button></p><p class="fb" aria-live="polite"></p>\n' % (esc(ui["pasteLabel"]), esc(ui["check"])))
            else:
                o.append('<p><button type="button" class="btn primary done">%s</button> <button type="button" class="btn undo" hidden>%s</button></p>\n' % (esc(ui["iDidIt"]), esc(ui["undo"])))
            o.append("</article>\n")
        o.append("</section>\n")
    if mod["tasks"]:
        o.append('<section id="lab"><h2>%s %s</h2><p>%s</p><p>%s</p><p><button type="button" class="btn" data-openterm>%s %s</button></p>\n'
                 % (icon("flask"), esc(ui["simTitle"]), md(ui["simIntro"]), md(ui["labIntro"]), icon("terminal"), esc(ui["openTerminal"])))
        for kind in KINDS:
            ts = [t for t in mod["tasks"] if t.get("kind", "guided") == kind]
            if not ts:
                continue
            o.append('<h3 class="kind k-%s">%s %s <span class="gcount" data-g="%s"></span></h3>%s<ol class="tasks">\n'
                     % (kind, icon(KIND_ICON[kind]), esc(ui["kind_" + kind]), kind,
                        ('<p class="predict-note">%s</p>' % md(ui["predictNote"])) if kind == "predict" else ""))
            for t in ts:
                tt = tx["tasks"][t["id"]]
                d = t.get("diff", 2)
                o.append('<li class="task" data-task="%s" data-kind="%s"><span class="tcheck" aria-hidden="true"></span><div>'
                         '<p class="badges"><span class="badge b-%s">%s</span><span class="badge d%d">%s</span></p><p>%s</p>'
                         '<details><summary>%s</summary><p>%s</p></details>'
                         '<details><summary>%s</summary>%s</details></div></li>\n'
                         % (t["id"], kind, kind, esc(ui["kind_" + kind]), d, esc(ui["diff%d" % d]), md(tt["text"]),
                            esc(ui["hint"]), md(tt["hint"]), esc(ui["solution"]), code_block("\n".join(t["solution"]), ui)))
            o.append("</ol>\n")
        o.append('<p><button type="button" class="btn" id="resetlab">%s</button></p></section>\n' % esc(ui["resetLab"]))
    o.append('<section id="quiz"><h2>%s %s</h2>\n' % (icon("help"), esc(ui["quizTitle"])))
    for q in mod["quiz"]:
        qt = tx["quiz"][q["id"]]
        opts = "".join('<button type="button" class="opt" data-i="%d">%s</button>' % (i, md(x)) for i, x in enumerate(qt["options"]))
        o.append('<div class="q card" data-q="%s"><p><strong>%s</strong></p><div class="opts">%s</div><p class="explain" hidden>%s</p></div>\n'
                 % (q["id"], md(qt["q"]), opts, md(qt["explain"])))
    o.append('<p class="retry-bar" hidden><span>%s</span> <button type="button" class="btn" id="retryq">%s</button></p>\n' % (esc(ui["retryNote"]), esc(ui["retryBtn"])))
    o.append("</section>\n")
    o.append('<section id="summary" class="card"><h2>%s %s</h2><ul>%s</ul></section>\n' % (icon("check"), esc(ui["summary"]), "".join("<li>%s</li>" % md(x) for x in tx["summary"])))
    o.append('<section id="recall" class="card recall"><h2>%s %s</h2><p>%s</p><details><summary>%s</summary><ol>%s</ol></details></section>\n'
             % (icon("bulb"), esc(ui["recallTitle"]), esc(ui["recallPrompt"]), esc(ui["recallShow"]),
                "".join("<li>%s</li>" % md(x) for x in tx["summary"][:3])))
    o.append('<section id="glossary"><h2>%s %s</h2><dl class="gl">%s</dl></section>\n' % (icon("book"), esc(ui["glossary"]),
             "".join("<dt>%s</dt><dd>%s</dd>" % (esc(g["term"]), md(g["meaning"])) for g in tx["glossary"])))
    order = [m["id"] for m in mods_meta["modules"]]
    i = order.index(mid)
    nav = []
    if i > 0 and order[i - 1] in built:
        nav.append('<a class="btn" href="%s">%s %s</a>' % (mod_file(order[i - 1]), icon("arrow-l"), esc(ui["prev"])))
    if i + 1 < len(order) and order[i + 1] in built:
        nav.append('<a class="btn primary" href="%s">%s %s</a>' % (mod_file(order[i + 1]), esc(ui["next"]), icon("arrow-r")))
    o.append('<nav class="pn">%s</nav>\n</main>\n' % "".join(nav))
    o.append(_ic('<aside class="term" id="term" aria-label="%s" hidden><div class="termhead"><span class="tdots" aria-hidden="true"><i></i><i></i><i></i></span><strong>%s</strong>'
             '<button type="button" class="ibtn" id="termclose" aria-label="%s">@@close@@</button></div>'
             '<div class="termout" id="termout" role="log"></div>'
             '<div class="termin"><span id="termprompt"></span><input id="terminput" autocomplete="off" autocapitalize="off" spellcheck="false" aria-label="%s"></div></aside></div>\n'
             % (esc(ui["terminal"]), esc(ui["terminalOptional"]), esc(ui["closeTerminal"]), esc(ui["terminal"]))))
    cfg = {"lang": lang, "module": mid, "setup": mod.get("setup", {}),
           "tasks": [{"id": t["id"], "kind": t.get("kind", "guided"), "check": t["check"]} for t in mod["tasks"]],
           "vm": [{"id": v["id"], "expect": v["expect"]} for v in vm],
           "quiz": {q["id"]: q["answer"] for q in mod["quiz"]},
           "ui": {k: ui[k] for k in RUNTIME_UI}}
    o.append('<script type="application/json" id="tla-config">%s</script>\n' % json.dumps(cfg, ensure_ascii=False).replace("</", "<\\/"))
    o.append('<script src="../shared/terminal.js"></script>\n<script src="../shared/core.js"></script>\n'
             '<script src="../shared/terminal-ui.js"></script>\n<script src="../shared/lab.js"></script>\n</body>\n</html>\n')
    return "".join(o)


def build_root(ui_all):
    links = "".join('<a class="btn primary" href="%s/index.html" hreflang="%s" lang="%s">%s</a>' % (l, l, l, LANG_NAMES[l]) for l in LANGS)
    return ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            '<title>Linux Academy — Choose your language</title><meta name="theme-color" content="#060a08">'
            '<link rel="manifest" href="manifest.webmanifest"><link rel="icon" href="icons/icon.svg" type="image/svg+xml">'
            '<link rel="apple-touch-icon" href="icons/icon-192.png">'
            '<link rel="stylesheet" href="shared/app.css"><script defer src="shared/pwa.js"></script>'
            '</head><body class="page-root"><main class="wrap chooser" aria-labelledby="language-title">'
            '<div class="chooser-mark">%s</div><p class="hero-kicker"><span></span>LINUX • LEARN BY DOING</p>'
            '<h1 id="language-title">Hoş geldin / Willkommen / Welcome</h1>'
            '<p class="chooser-prompt">Dilini seç <span>• Sprache wählen • Choose your language</span></p>'
            '<div class="heroact">%s</div></main></body></html>\n' % (linux_icon(), links))


def write_precache_manifest():
    urls = ["./", "index.html", "manifest.webmanifest", "service-worker.js"]
    urls.extend(sorted(p.relative_to(V3).as_posix() for lang in LANGS for p in (V3 / lang).glob("*.html")))
    urls.extend(sorted(p.relative_to(V3).as_posix() for folder in ("shared", "icons")
                       for p in (V3 / folder).rglob("*") if p.is_file()))
    revision = hashlib.sha256()
    for url in urls:
        if url == "./":
            continue
        path = V3 / url
        revision.update(url.encode("utf-8"))
        revision.update(path.read_bytes())
    manifest = "self.PRECACHE_REVISION = %s;\nself.PRECACHE_URLS = %s;\n" % (
        json.dumps(revision.hexdigest()[:16]), json.dumps(urls))
    (V3 / "precache-manifest.js").write_text(manifest, encoding="utf-8")


def main():
    mods_meta = load(CONTENT / "_modules.json")
    ui_all = load(CONTENT / "_ui.json")
    built = built_modules()
    n = 0
    for lang in LANGS:
        d = V3 / lang
        d.mkdir(exist_ok=True)
        ui = ui_all[lang]
        (d / "index.html").write_text(build_index(lang, ui, mods_meta, built), encoding="utf-8")
        n += 1
        for mid in built:
            (d / mod_file(mid)).write_text(build_module(lang, ui, mods_meta, mid, built), encoding="utf-8")
            n += 1
    (V3 / "index.html").write_text(build_root(ui_all), encoding="utf-8")
    write_precache_manifest()
    print("built %d pages (modules: %s)" % (n + 1, ", ".join(built)))


if __name__ == "__main__":
    main()
