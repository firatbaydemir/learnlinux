#!/usr/bin/env python3
"""Validates the v3 content and generated pages. Run: python3 v3/tools/validate.py  (exit 1 on errors)"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from html.parser import HTMLParser
from pathlib import Path

V3 = Path(__file__).resolve().parent.parent
CONTENT = V3 / "content"
LANGS = ["tr", "de", "en"]
errors, warnings = [], []


def err(m):
    errors.append(m)


def load(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except Exception as e:
        err("%s: invalid JSON (%s)" % (p, e))
        return None


def find_js():
    for c in ("node", "jsc", "/tmp/jsc",
              "/System/Library/Frameworks/JavaScriptCore.framework/Versions/A/Helpers/jsc"):
        p = shutil.which(c) or (c if os.path.exists(c) else None)
        if p:
            return p
    return None


BADCHARS = re.compile(r"[çğışöüÇĞİŞÖÜäöüÄÖÜß]")
BADWORDS = re.compile(r"\b(ogrenci|deneme|dosya|belgeler|masaustu|indirilenler|merhaba|eski|rapor|klasor|kullanici|benutzer|datei)\b", re.I)


def ident_scan(where, obj):
    """Identifiers (users, paths, files, hosts) must be English ASCII in every language."""
    if isinstance(obj, dict):
        for v in obj.values():
            ident_scan(where, v)
    elif isinstance(obj, list):
        for v in obj:
            ident_scan(where, v)
    elif isinstance(obj, str):
        obj = re.sub(r"\s*#.*$", "", obj, flags=re.M)
        if BADCHARS.search(obj) or BADWORDS.search(obj):
            err("%s: non-English/non-ASCII identifier in code text: %r" % (where, obj[:60]))


def check_content(meta, ui):
    for l in LANGS:
        if l not in ui:
            err("_ui.json: missing language %s" % l)
    if all(l in ui for l in LANGS):
        base = set(ui["tr"])
        for l in LANGS:
            if set(ui[l]) != base:
                err("_ui.json: key mismatch in %s: %s" % (l, sorted(set(ui[l]) ^ base)))
    ids = [m["id"] for m in meta["modules"]]
    if len(ids) != len(set(ids)):
        err("_modules.json: duplicate ids")
    for m in meta["modules"]:
        for l in LANGS:
            if not m["title"].get(l):
                err("_modules.json: %s missing %s title" % (m["id"], l))
    built = []
    for d in sorted(CONTENT.iterdir()):
        if not (d.is_dir() and d.name.startswith("m")):
            continue
        mid = d.name[1:]
        if mid not in ids:
            err("%s: module id not in _modules.json" % d.name)
        mod = load(d / "module.json")
        tx = {l: load(d / (l + ".json")) for l in LANGS}
        if mod is None or any(v is None for v in tx.values()):
            continue
        built.append(mid)
        tids = [t["id"] for t in mod["tasks"]]
        if tids != ["t%02d" % (i + 1) for i in range(len(tids))]:
            err("%s: task ids must be t01..tNN in order" % d.name)
        for t in mod["tasks"]:
            if not t.get("check") or not t.get("solution"):
                err("%s/%s: needs check and solution" % (d.name, t["id"]))
        kinds = {"warmup", "guided", "predict", "debug", "mini", "challenge", "ticket"}
        for t in mod["tasks"]:
            if t.get("kind") not in kinds or t.get("diff") not in (1, 2, 3):
                err("%s/%s: invalid kind/diff" % (d.name, t["id"]))
        miss = kinds - {t.get("kind") for t in mod["tasks"]}
        if miss:
            warnings.append("%s: missing task kinds: %s" % (d.name, ", ".join(sorted(miss))))
        vids = [v["id"] for v in mod.get("vm", [])]
        if vids != ["v%02d" % (i + 1) for i in range(len(vids))]:
            err("%s: vm ids must be v01..vNN in order" % d.name)
        for v in mod.get("vm", []):
            if v.get("expect"):
                try:
                    re.compile(v["expect"])
                except re.error:
                    err("%s/%s: expect regex invalid" % (d.name, v["id"]))
        ident_scan(d.name, {"setup": mod.get("setup"), "solution": [t["solution"] for t in mod["tasks"]]})
        qids = [q["id"] for q in mod["quiz"]]
        secs = None
        for l in LANGS:
            x = tx[l]
            for k in ("title", "lead", "objectives", "sections", "tasks", "quiz", "summary", "glossary"):
                if not x.get(k):
                    err("%s/%s.json: missing/empty '%s'" % (d.name, l, k))
            if set(x.get("tasks", {})) != set(tids):
                err("%s/%s.json: task ids differ from module.json" % (d.name, l))
            for tid, v in x.get("tasks", {}).items():
                if not v.get("text") or not v.get("hint"):
                    err("%s/%s.json: task %s needs text and hint" % (d.name, l, tid))
            if mod.get("vm") and (not x.get("vm") or set(x["vm"].get("tasks", {})) != set(vids)):
                err("%s/%s.json: vm tasks differ from module.json" % (d.name, l))
            for v in (x.get("vm") or {}).get("tasks", {}).values():
                for b in v.get("blocks", []):
                    ident_scan(d.name + "/" + l, b.get("cmd"))
            for s_ in x.get("sections", []):
                for c in s_.get("commands", []):
                    ident_scan(d.name + "/" + l, {"cmd": c.get("cmd"), "example": c.get("example")})
            for tv in x.get("tasks", {}).values():
                for span in re.findall(r"`([^`]+)`", tv.get("text", "") + " " + tv.get("hint", "")):
                    ident_scan(d.name + "/" + l, span)
            if set(x.get("quiz", {})) != set(qids):
                err("%s/%s.json: quiz ids differ from module.json" % (d.name, l))
            for q in mod["quiz"]:
                qq = x.get("quiz", {}).get(q["id"])
                if qq and not (0 <= q["answer"] < len(qq["options"])):
                    err("%s/%s.json: quiz %s answer out of range" % (d.name, l, q["id"]))
                if qq and len(qq["options"]) != len(tx["tr"]["quiz"][q["id"]]["options"]):
                    err("%s/%s.json: quiz %s option count differs" % (d.name, l, q["id"]))
            shape = [(s["id"], len(s.get("commands", []))) for s in x.get("sections", [])]
            if secs is None:
                secs = shape
            elif shape != secs:
                err("%s/%s.json: section ids / command counts differ from tr" % (d.name, l))
            for s in x.get("sections", []):
                for c in s.get("commands", []):
                    for k in ("cmd", "what", "where", "why", "example"):
                        if not c.get(k):
                            err("%s/%s.json: command in %s lacks %s" % (d.name, l, s["id"], k))
        if len(mod["tasks"]) < 5:
            warnings.append("%s: only %d tasks" % (d.name, len(mod["tasks"])))
    return built


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.hrefs, self.srcs, self.attrs_seen, self.langsw = [], [], [], set(), []
        self.in_sw = False
        self.in_header = False
        self.langsw_in_header = False
        self.html_lang = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for k in a:
            self.attrs_seen.add(k)
        if tag == "header":
            self.in_header = True
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "html":
            self.html_lang = a.get("lang")
        if tag == "nav" and a.get("id") == "langsw":
            self.in_sw = True
            self.langsw_in_header = self.in_header
        if tag == "a" and "href" in a:
            self.hrefs.append(a["href"])
            if self.in_sw:
                self.langsw.append(a)
        if tag == "script" and "src" in a:
            self.srcs.append(a["src"])
        if tag == "link" and "href" in a:
            self.srcs.append(a["href"])

    def handle_endtag(self, tag):
        if tag == "nav":
            self.in_sw = False
        if tag == "header":
            self.in_header = False


def check_pages(meta, built):
    pages = ["index.html"] + ["modul-%s.html" % m for m in built]
    for l in LANGS:
        for p in pages:
            f = V3 / l / p
            if not f.exists():
                err("missing page %s/%s (run build.py)" % (l, p))
                continue
            text = f.read_text(encoding="utf-8")
            rel = "%s/%s" % (l, p)
            if "data-lang" in text:
                err("%s: contains data-lang (languages must not be mixed)" % rel)
            pg = Page()
            pg.feed(text)
            if pg.html_lang != l:
                err("%s: <html lang> is %r, expected %r" % (rel, pg.html_lang, l))
            if len(pg.ids) != len(set(pg.ids)):
                err("%s: duplicate ids" % rel)
            if "langsw" not in pg.ids:
                err("%s: sticky language switcher (#langsw) missing" % rel)
            if not pg.langsw_in_header:
                err("%s: language switcher (#langsw) must be in the header" % rel)
            targets = {a.get("hreflang"): a.get("href") for a in pg.langsw}
            for t in LANGS:
                want = "../%s/%s" % (t, p)
                if targets.get(t) != want:
                    err("%s: language switch for %s must link to %s (got %s)" % (rel, t, want, targets.get(t)))
                if not (V3 / t / p).exists():
                    err("%s: counterpart %s/%s does not exist" % (rel, t, p))
            for h in pg.hrefs + pg.srcs:
                if re.match(r"(https?:|mailto:|#|javascript:)", h):
                    if h.startswith(("http:", "https:")):
                        err("%s: external URL %s (site must be CDN/offline free)" % (rel, h))
                    continue
                if not (f.parent / h.split("#")[0]).resolve().exists():
                    err("%s: broken link %s" % (rel, h))
            m = re.search(r'id="tla-config">(.*?)</script>', text, re.S)
            if not m:
                err("%s: tla-config missing" % rel)
            else:
                try:
                    json.loads(m.group(1))
                except Exception as e:
                    err("%s: tla-config invalid (%s)" % (rel, e))
            if p != "index.html":
                for need in ('id="termout"', 'id="terminput"', 'id="lab"', 'id="quiz"', 'data-task="'):
                    if need not in text:
                        err("%s: missing %s" % (rel, need))
    if not (V3 / "index.html").exists():
        err("v3/index.html (language chooser) missing")


def selftest(meta, built):
    js = find_js()
    if not js:
        warnings.append("no node/jsc found: engine selftest skipped")
        return
    mods = {m: load(CONTENT / ("m" + m) / "module.json") for m in built}
    engine = (V3 / "shared" / "terminal.js").read_text(encoding="utf-8")
    runner = r"""
var out = (typeof print !== 'undefined') ? print : console.log;
var E = (typeof TLAEngine !== 'undefined') ? TLAEngine : module.exports;
var MODS = %s, res = [];
Object.keys(MODS).forEach(function (id) {
  var m = MODS[id], sh = new E.Shell({lang: 'en'}); sh.reset(m.setup || {});
  var done = {}, problems = [];
  m.tasks.forEach(function (t) { if (E.verify(sh, t.check)) problems.push(t.id + ' already true before any command'); });
  m.tasks.forEach(function (t) {
    t.solution.forEach(function (c) {
      sh.run(c);
      m.tasks.forEach(function (u) { if (!done[u.id] && E.verify(sh, u.check)) done[u.id] = true; });
    });
  });
  m.tasks.forEach(function (t) { if (!done[t.id]) problems.push(t.id + ' not satisfied by the solutions'); });
  res.push({id: id, problems: problems});
});
out('RESULT' + JSON.stringify(res));
""" % json.dumps(mods)
    tmp = Path(tempfile.mkdtemp()) / "selftest.js"
    if Path(js).name == "node":
        tmp.write_text(engine + "\n" + runner, encoding="utf-8")
    else:
        tmp.write_text(engine + "\n" + runner, encoding="utf-8")
    try:
        r = subprocess.run([js, str(tmp)], capture_output=True, text=True, timeout=120)
    finally:
        shutil.rmtree(tmp.parent, ignore_errors=True)
    m = re.search(r"RESULT(\[.*\])", r.stdout)
    if not m:
        err("selftest did not run: %s %s" % (r.stdout[-300:], r.stderr[-300:]))
        return
    for res in json.loads(m.group(1)):
        for p in res["problems"]:
            err("selftest m%s: %s" % (res["id"], p))


def main():
    meta = load(CONTENT / "_modules.json")
    ui = load(CONTENT / "_ui.json")
    if meta is None or ui is None:
        print("FAILED")
        return 1
    built = check_content(meta, ui)
    check_pages(meta, built)
    selftest(meta, built)
    for w in warnings:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print("modules built: %d | errors: %d | warnings: %d" % (len(built), len(errors), len(warnings)))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
