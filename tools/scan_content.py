#!/usr/bin/env python3
"""Salt okunur içerik taraması -> SCAN.md (1 satır/modül)."""
import json, re, glob, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LANGS = ("tr", "de", "en")


def load(p):
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def key(mid):
    return tuple(int(x) for x in mid.split("."))


def texts(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from texts(v)
    elif isinstance(o, list):
        for v in o:
            yield from texts(v)


def shape(o):
    if isinstance(o, dict):
        return {k: shape(v) for k, v in o.items()}
    if isinstance(o, list):
        return [shape(v) for v in o]
    return None


def first_word(c):
    c = c.strip().lstrip("$ ").split()
    while c and c[0] in ("sudo",):
        c = c[1:]
    return c[0] if c else ""


mods = {}
for d in glob.glob(os.path.join(ROOT, "content", "m*")):
    mid = os.path.basename(d)[1:]
    try:
        mods[mid] = {"mod": load(os.path.join(d, "module.json")),
                     **{l: load(os.path.join(d, l + ".json")) for l in LANGS}}
    except FileNotFoundError:
        pass

taught = set()
rows = []
for mid in sorted(mods, key=key):
    m = mods[mid]
    tr = m["tr"]
    flags = []
    words = sum(len(t.split()) for s in tr["sections"] for t in
                (s.get("body") or []) if isinstance(t, str))
    tasks = len(m["mod"].get("tasks", []))
    quiz = len(m["mod"].get("quiz", []))
    if words < 250: flags.append("kısa")
    if tasks < 13: flags.append("görev<13")
    if quiz < 8: flags.append("quiz<8")
    if not any("warn" in s for s in tr["sections"]): flags.append("sık-hata-yok")
    cmds = [c for s in tr["sections"] for c in s.get("commands", [])]
    empty = sum(1 for c in cmds if not c.get("why") or not c.get("where"))
    if empty: flags.append(f"why/where-boş:{empty}")
    if any(shape(m[l]) != shape(tr) for l in ("de", "en")): flags.append("yapı-farkı")
    for c in cmds:
        taught.add(first_word(c.get("cmd", "")))
    late = set()
    for t in m["mod"].get("tasks", []):
        for sol in t.get("solution", []):
            for part in re.split(r"\s*(?:\|\||&&|\||;)\s*", sol):
                w = first_word(part)
                if w and w not in taught and w not in ("cd",):
                    late.add(w)
    if late: flags.append("öğretilmemiş:" + ",".join(sorted(late)[:5]))
    bad = set()
    for t in texts(tr):
        for r in re.findall(r"(?:modül|Modül)\s+(\d+\.\d+)", t):
            if r not in mods: bad.add(r)
    if bad: flags.append("kırık-atıf:" + ",".join(sorted(bad)))
    rows.append(f"| {mid} | {tr['title'][:40]} | {words} | {tasks} | {quiz} | "
                f"{len(cmds)} | {'; '.join(flags) or '-'} |")

out = ["# SCAN", "", "| id | başlık | kelime | görev | quiz | komut | bayraklar |",
       "|---|---|---|---|---|---|---|"] + rows
with open(os.path.join(ROOT, "SCAN.md"), "w", encoding="utf-8", newline="\r\n") as f:
    f.write("\n".join(out) + "\n")
print(len(rows), "modül; SCAN.md yazıldı")
