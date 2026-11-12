#!/usr/bin/env python3
"""Builds v3/<lang>/*.html and v3/index.html from v3/content. Run: python3 v3/tools/build.py"""
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
              "resetConfirm", "openTerminal", "closeTerminal", "continue", "startPath", "noResult", "soon", "overall"]


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
            '<link rel="stylesheet" href="%s/app.css">\n</head>\n') % (lang, esc(title), lang, depth_shared)


def topbar(lang, ui, page, extra=""):
    return ('<header class="top"><a class="brand" href="index.html">%s</a>'
            '<div class="topr">%s%s<button type="button" class="ibtn" id="themebtn" title="%s" aria-label="%s">◐</button></div></header>\n'
            % (esc(ui["siteName"]), extra, lang_switch(lang, page), esc(ui["theme"]), esc(ui["theme"])))


def linux_icon():
    return ('<svg class="tux-icon" viewBox="0 0 240 240" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false">'
            '<path fill="#172033" d="M120 24c-40 0-72 32-72 72v47c0 39 32 70 72 70s72-31 72-70V96c0-40-32-72-72-72Z"/>'
            '<ellipse cx="120" cy="111" rx="49" ry="39" fill="#fff"/>'
            '<ellipse cx="120" cy="171" rx="43" ry="34" fill="#f3f6fb"/>'
            '<ellipse cx="102" cy="104" rx="6" ry="9" fill="#172033"/>'
            '<ellipse cx="138" cy="104" rx="6" ry="9" fill="#172033"/>'
            '<path fill="#f2a900" d="m120 117 18 13-18 10-18-10 18-13Z"/>'
            '<path fill="#f2a900" d="M67 194c12 2 24-1 35-8-4 18-19 29-37 25-8-2-10-12 2-17Zm106 0c-12 2-24-1-35-8 4 18 19 29 37 25 8-2 10-12-2-17Z"/>'
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
           '<a class="btn primary" id="continue" href="#">%s <span aria-hidden="true">→</span></a>'
           '<input type="search" id="search" placeholder="%s" aria-label="%s"></div>'
           '<div class="hero-progress"><div class="bar" aria-hidden="true"><i id="totalbar"></i></div>'
           '<p class="muted" id="totaltxt"></p></div></div>'
           '<div class="hero-art" aria-hidden="true"><div class="hero-glow"></div>'
           '<div class="tux-mark">%s</div><div class="terminal-card">'
           '<div class="terminal-chrome"><i></i><i></i><i></i><span>terminal</span></div>'
           '<div class="terminal-lines"><p><span>~</span> uname -s</p><p class="terminal-output">Linux</p>'
           '<p><span>~</span> <b class="terminal-cursor"></b></p></div></div></div></section>\n'
           % (esc(ui["heroKicker"]), esc(ui["heroTitle"]), esc(ui["heroText"]), esc(ui["startPath"]),
              esc(ui["search"]), esc(ui["search"]), linux_icon())]
    out.append('<p id="noresult" class="muted" hidden>%s</p>\n' % esc(ui["noResult"]))
    for lv in sorted(levels, key=int):
        items = [m for m in mods_meta["modules"] if str(m["level"]) == lv]
        out.append('<section class="level"><h2>%s %s — %s</h2><ul class="mods">\n' % (esc(ui["level"]), lv, esc(levels[lv][lang])))
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
    simbtn = ('<button type="button" class="try small" data-try="%s" title="%s">▶ %s</button>' % (esc(text), esc(ui["tryHint"]), esc(ui["tryInSim"]))) if sim else ""
    return ('<div class="code"><pre><code>%s</code></pre><div class="codebtns">%s<button type="button" class="copy" data-copy="%s">%s</button></div></div>'
            % (body, simbtn, esc(raw), esc(ui["copy"])))


def callout(kind, label, text):
    icons = {"tip": "💡", "warn": "⚠️", "danger": "⛔"}
    return '<aside class="callout %s" role="note"><strong>%s %s</strong><p>%s</p></aside>\n' % (kind, icons[kind], esc(label), md(text))


def build_module(lang, ui, mods_meta, mid, built):
    mod = load(CONTENT / ("m" + mid) / "module.json")
    tx = load(CONTENT / ("m" + mid) / (lang + ".json"))
    meta = next(m for m in mods_meta["modules"] if m["id"] == mid)
    page = mod_file(mid)
    title = "%s %s — %s" % (mid, tx["title"], ui["siteName"])
    toggle = '<button type="button" class="btn" id="termbtn" aria-expanded="false">&gt;_ %s</button>' % esc(ui["terminalOptional"])
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
    o.append('<div class="module-hero"><p class="crumb"><a href="index.html">%s</a> <span aria-hidden="true">/</span> %s %s</p>\n'
             '<h1><span class="module-id">%s</span> %s</h1>\n<p class="lead">%s</p>\n<p class="muted" id="modtxt"></p></div>\n'
             % (esc(ui["home"]), esc(ui["level"]), meta["level"], mid, esc(tx["title"]), md(tx["lead"])))
    o.append('<section class="card" id="objectives"><h2>%s</h2><ul>%s</ul></section>\n'
             % (esc(ui["objectives"]), "".join("<li>%s</li>" % md(x) for x in tx["objectives"])))
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
        o.append('<section id="vm"><h2>%s <span class="gcount" data-g="vm"></span></h2><p>%s</p><p>%s</p>\n' % (esc(ui["vmTitle"]), md(ui["vmIntro"]), md(tx["vm"]["intro"])))
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
        o.append('<section id="lab"><h2>%s</h2><p>%s</p><p>%s</p><p><button type="button" class="btn" data-openterm>&gt;_ %s</button></p>\n'
                 % (esc(ui["simTitle"]), md(ui["simIntro"]), md(ui["labIntro"]), esc(ui["openTerminal"])))
        for kind in KINDS:
            ts = [t for t in mod["tasks"] if t.get("kind", "guided") == kind]
            if not ts:
                continue
            o.append('<h3 class="kind k-%s">%s <span class="gcount" data-g="%s"></span></h3><ol class="tasks">\n' % (kind, esc(ui["kind_" + kind]), kind))
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
    o.append('<section id="quiz"><h2>%s</h2>\n' % esc(ui["quizTitle"]))
    for q in mod["quiz"]:
        qt = tx["quiz"][q["id"]]
        opts = "".join('<button type="button" class="opt" data-i="%d">%s</button>' % (i, md(x)) for i, x in enumerate(qt["options"]))
        o.append('<div class="q card" data-q="%s"><p><strong>%s</strong></p><div class="opts">%s</div><p class="explain" hidden>%s</p></div>\n'
                 % (q["id"], md(qt["q"]), opts, md(qt["explain"])))
    o.append("</section>\n")
    o.append('<section id="summary" class="card"><h2>%s</h2><ul>%s</ul></section>\n' % (esc(ui["summary"]), "".join("<li>%s</li>" % md(x) for x in tx["summary"])))
    o.append('<section id="glossary"><h2>%s</h2><dl class="gl">%s</dl></section>\n' % (esc(ui["glossary"]),
             "".join("<dt>%s</dt><dd>%s</dd>" % (esc(g["term"]), md(g["meaning"])) for g in tx["glossary"])))
    order = [m["id"] for m in mods_meta["modules"]]
    i = order.index(mid)
    nav = []
    if i > 0 and order[i - 1] in built:
        nav.append('<a class="btn" href="%s">← %s</a>' % (mod_file(order[i - 1]), esc(ui["prev"])))
    if i + 1 < len(order) and order[i + 1] in built:
        nav.append('<a class="btn primary" href="%s">%s →</a>' % (mod_file(order[i + 1]), esc(ui["next"])))
    o.append('<nav class="pn">%s</nav>\n</main>\n' % "".join(nav))
    o.append('<aside class="term" id="term" aria-label="%s" hidden><div class="termhead"><strong>%s</strong>'
             '<button type="button" class="ibtn" id="termclose" aria-label="%s">✕</button></div>'
             '<div class="termout" id="termout" role="log"></div>'
             '<div class="termin"><span id="termprompt"></span><input id="terminput" autocomplete="off" autocapitalize="off" spellcheck="false" aria-label="%s"></div></aside></div>\n'
             % (esc(ui["terminal"]), esc(ui["terminalOptional"]), esc(ui["closeTerminal"]), esc(ui["terminal"])))
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
            '<title>Linux Academy — Choose your language</title><link rel="stylesheet" href="shared/app.css">'
            '</head><body class="page-root"><main class="wrap chooser" aria-labelledby="language-title">'
            '<div class="chooser-mark">%s</div><p class="hero-kicker"><span></span>LINUX • LEARN BY DOING</p>'
            '<h1 id="language-title">Hoş geldin / Willkommen / Welcome</h1>'
            '<p class="chooser-prompt">Dilini seç <span>• Sprache wählen • Choose your language</span></p>'
            '<div class="heroact">%s</div></main></body></html>\n' % (linux_icon(), links))


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
    print("built %d pages (modules: %s)" % (n + 1, ", ".join(built)))


if __name__ == "__main__":
    main()
