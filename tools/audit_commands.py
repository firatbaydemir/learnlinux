#!/usr/bin/env python3
"""Komut denetimi: yalnızca okur, AUDIT.md üretir (tr içerik üzerinden).

Kullanım: python3 tools/audit_commands.py [--out AUDIT.md]
"""
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
NOTE_RE = re.compile(r"sonraki modül|ileride|modül \d\.\d", re.I)
OPS = ["2>&1", "&>", "2>>", "2>", ">>", ">", "<", "||", "&&", "|", ";"]
PLACEHOLDER_FIRST = {"cmd", "komut", "command"}
CMD_WORD = re.compile(r"^[a-z][\w.+-]*$")
SKIP_PREFIX = ("sudo",)


def load(p):
    return json.loads(p.read_text(encoding="utf-8"))


def parse_line(s):
    """Kabuk satırından (komutlar, operatörler) çıkarır; sezgiseldir."""
    cmds, ops = [], []
    inner = re.findall(r"\$\(([^)]*)\)", s)
    s = re.sub(r"\$\([^)]*\)", " ", s)
    for i in inner:
        c, o = parse_line(i)
        cmds += c
        ops += o
    s = re.sub(r'"[^"]*"|\'[^\']*\'', '""', s)
    pat = "(" + "|".join(re.escape(o) for o in OPS) + ")"
    parts = re.split(pat, s)
    expect_cmd = True
    for part in parts:
        if part in OPS:
            ops.append(part)
            expect_cmd = part in ("|", "||", "&&", ";")
            continue
        words = part.split()
        if not words:
            continue
        if not expect_cmd:  # yönlendirme hedefi
            expect_cmd = False
            continue
        words = [w for w in words if not re.match(r"^\w+=", w)]
        if not words:
            continue
        first = words[0]
        if CMD_WORD.match(first):
            cmds.append(first)
            if first in SKIP_PREFIX and len(words) > 1 and CMD_WORD.match(words[1]):
                cmds.append(words[1])
        expect_cmd = False
    return cmds, ops


def is_noncommand(cmd):
    w = cmd.split()
    if not w:
        return True
    f = w[0]
    return (
        not CMD_WORD.match(f)
        or f in PLACEHOLDER_FIRST
        or f.lower().startswith(("ctrl", "alt", "tab", "esc"))
        or f.startswith("--")
    )


def strings_of(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings_of(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings_of(v)


def main():
    out_path = ROOT / "AUDIT.md"
    if "--out" in sys.argv:
        out_path = Path(sys.argv[sys.argv.index("--out") + 1])

    order = load(CONTENT / "_modules.json")["modules"]
    ids = [m["id"] for m in order]
    idx = {m: i for i, m in enumerate(ids)}
    titles = {m["id"]: m["title"]["tr"] for m in order}

    tr, mj = {}, {}
    for m in ids:
        tr[m] = load(CONTENT / f"m{m}" / "tr.json")
        mj[m] = load(CONTENT / f"m{m}" / "module.json")

    # 1) Kartlar: öğretilen komutlar
    taught = {}                       # anahtar -> ilk modül
    taught_in = defaultdict(set)      # anahtar -> modüller (ilk kelime)
    exact = defaultdict(set)          # tam cmd -> modüller
    noncmd, nosim = [], []
    cards_by_mod = defaultdict(list)
    for m in ids:
        for s in tr[m].get("sections", []):
            for c in s.get("commands", []):
                cmd = c["cmd"].strip()
                exact[cmd].add(m)
                cards_by_mod[m].append((s, cmd))
                if c.get("nosim"):
                    nosim.append((m, cmd))
                if is_noncommand(cmd):
                    noncmd.append((m, cmd))
                    for o in parse_line(cmd.replace("cmd", "x"))[1]:
                        taught.setdefault(o, m)
                        taught_in[o].add(m)
                    continue
                cs, _ = parse_line(cmd)
                if cs:
                    k = cs[0]
                    taught.setdefault(k, m)
                    taught_in[k].add(m)
    known = set(taught)

    # 2) Kullanımlar
    usages = []  # (modül, anahtar, yer)

    def add(m, line, where, only_known=False):
        cs, ops = parse_line(line)
        for k in cs + ops:
            if only_known and k not in known:
                continue
            usages.append((m, k, where))

    for m in ids:
        for t in mj[m].get("tasks", []):
            for sol in t.get("solution", []):
                add(m, sol, f"{t['id']} çözüm")
        trd = tr[m]
        for tid, t in trd.get("tasks", {}).items():
            for fld in ("text", "hint"):
                for span in re.findall(r"`([^`]+)`", t.get(fld, "")):
                    add(m, span, f"{tid} {fld}", only_known=True)
        for vid, v in trd.get("vm", {}).get("tasks", {}).items():
            for b in v.get("blocks", []):
                for ln in b.get("cmd", "").split("\n"):
                    add(m, ln, f"{vid} vm")
        for s in trd.get("sections", []):
            for c in s.get("commands", []):
                add(m, c.get("example", ""), f"kart:{c['cmd'][:24]}")

    # Not var mı? (modül içinde komutu anan ve not kalıbı taşıyan metin)
    def has_note(m, key):
        for st in strings_of(tr[m]):
            if NOTE_RE.search(st) and re.search(r"(?<![\w-])" + re.escape(key) + r"(?![\w-])", st):
                return True
        return False

    early = defaultdict(lambda: defaultdict(list))   # m -> key -> yerler
    untaught = defaultdict(lambda: defaultdict(list))
    for m, k, where in usages:
        if k not in taught:
            untaught[m][k].append(where)
        elif idx[taught[k]] > idx[m]:
            early[m][k].append(where)

    L = []
    w = L.append
    w("# AUDIT.md — Komut denetimi (otomatik üretildi)")
    w("")
    w("> Üretici: `python3 tools/audit_commands.py`. Elle düzenleme. Kaynak: `content/` (tr).")
    w("> Not: ayrıştırma sezgiseldir; yanlış pozitifler olabilir. `kart:` = kartın örneği.")
    w("")
    n_early = sum(len(v) for v in early.values())
    w("## Özet")
    w(f"- Modül: {len(ids)} | öğretilen komut/operatör anahtarı: {len(taught)}")
    w(f"- Erken kullanım (modül, komut) çifti: {n_early}")
    w(f"- Komut olmayan kart `cmd`: {len(noncmd)} | `nosim`: {len(nosim)}")
    w("")

    w("## 1. Erken kullanım (öğretilmeden önce)")
    w("| Modül | Komut | Öğretildiği | Yerler | Not? |")
    w("|---|---|---|---|---|")
    for m in ids:
        for k, wh in sorted(early[m].items(), key=lambda x: idx[taught[x[0]]]):
            where = ", ".join(sorted(set(wh))[:4]) + (" …" if len(set(wh)) > 4 else "")
            w(f"| {m} | `{k}` | {taught[k]} | {where} | {'var' if has_note(m, k) else 'YOK'} |")
    w("")

    w("## 2. Hiçbir kartta öğretilmeyen ama kullanılan komutlar")
    w("| Modül | Komut | Yerler |")
    w("|---|---|---|")
    for m in ids:
        for k, wh in sorted(untaught[m].items()):
            where = ", ".join(sorted(set(wh))[:4]) + (" …" if len(set(wh)) > 4 else "")
            w(f"| {m} | `{k}` | {where} |")
    w("")

    w("## 3. Çift öğretim")
    w("Aynı tam `cmd` birden fazla modülde kartta:")
    dup = {c: sorted(ms, key=idx.get) for c, ms in exact.items() if len(ms) > 1}
    for c, ms in sorted(dup.items(), key=lambda x: idx[x[1][0]]):
        w(f"- `{c}`: {', '.join(ms)}")
    w("")
    w("Aynı komut (ilk kelime) 3+ modülde kartta:")
    for k, ms in sorted(taught_in.items(), key=lambda x: -len(x[1])):
        if len(ms) >= 3:
            w(f"- `{k}`: {', '.join(sorted(ms, key=idx.get))}")
    w("")

    w("## 4. Komut olmayan kart `cmd` değerleri (`kind` alanı adayı)")
    for m, c in noncmd:
        w(f"- {m}: `{c}`")
    w("")

    w("## 5. `nosim: true` kartlar")
    by = defaultdict(list)
    for m, c in nosim:
        by[m].append(f"`{c}`")
    for m in ids:
        if by[m]:
            w(f"- {m}: {', '.join(by[m])}")
    w("")

    w("## 6. Başlıkta geçmeyen kart komutları (başlık uyumsuzluğu ipucu)")
    w("Modül başlığı + bölüm başlıklarında adı geçmeyen komut sayısı yüksekse konu dağınık olabilir.")
    w("| Modül | Başlık | Geçmeyen/Toplam | Geçmeyenler |")
    w("|---|---|---|---|")
    for m in ids:
        hay = (titles[m] + " " + tr[m].get("title", "") + " " +
               " ".join(s.get("title", "") for s in tr[m].get("sections", []))).lower()
        keys, miss = [], []
        for s, cmd in cards_by_mod[m]:
            if is_noncommand(cmd):
                continue
            k = parse_line(cmd)[0][:1]
            if k and k[0] not in keys:
                keys.append(k[0])
        for k in keys:
            if k.lower() not in hay:
                miss.append(k)
        if keys:
            w(f"| {m} | {titles[m][:34]} | {len(miss)}/{len(keys)} | {', '.join(f'`{x}`' for x in miss[:10])} |")
    w("")

    out_path.write_text("\n".join(L) + "\n", encoding="utf-8")
    print(f"{out_path} yazıldı: {len(L)} satır, erken kullanım çifti: {n_early}")


if __name__ == "__main__":
    main()
