#!/usr/bin/env python3
"""Dil arasi tutarlilik: gorev/quiz kod aralari (`...`) tr/de/en'de ayni mi; gorev kod aralarindaki
dosya adlari module.json check/solution'da geciyor mu. Cikti: bulgu listesi."""
import json, re, glob, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILE = re.compile(r'[\w~./-]+\.(?:txt|log|sh|conf|out|bak|csv|tar|gz|d|json|service|timer)\b')
CODE = re.compile(r'`([^`]+)`')
def load(p):
    return json.load(open(p, encoding="utf-8"))
def spans(s):
    return sorted(set(CODE.findall(s)))
def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, path + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from walk(v, path + "/%d" % i)
    elif isinstance(o, str):
        yield path, o
out = []
for d in sorted(glob.glob(os.path.join(ROOT, "content", "m*", "module.json"))):
    dd = os.path.dirname(d); mid = os.path.basename(dd)
    try:
        L = {l: dict(walk(load(os.path.join(dd, l + ".json")))) for l in ("tr", "de", "en")}
        mod = json.dumps(load(d), ensure_ascii=False)
    except Exception as e:
        out.append("%s: okunamadi %s" % (mid, e)); continue
    # 1) kod aralari ayni mi (yalniz yaprak yol ortaksa)
    for p in L["tr"]:
        if not p.startswith("/tasks/"):  # quiz metinleri yerellestirilmis ornek adlar icerir (yanlis pozitif)
            continue
        if p not in L["en"] or p not in L["de"]:
            continue
        a, b, c = spans(L["tr"][p]), spans(L["de"][p]), spans(L["en"][p])
        # yalniz dosya adi/yol iceren aralari karsilastir
        f = lambda xs: sorted(x for x in xs if FILE.search(x) or x.startswith(("/", "~")))
        if not (f(a) == f(b) == f(c)):
            out.append("%s %s: kod aralari farkli\n   tr=%s\n   de=%s\n   en=%s" % (mid, p, f(a), f(b), f(c)))
    # 1b) komut kartlari (cmd/example): tr/de/en birebir ayni olmali (ls yok / fehlt / missing gibi sapmalar)
    for p in L["tr"]:
        if (p.endswith("/example") or ("/blocks/" in p and p.endswith("/cmd"))) and p in L["de"] and p in L["en"]:
            code = lambda l: "\n".join(x for x in L[l][p].split("\n") if not x.lstrip().startswith("#"))
            if not (code("tr") == code("de") == code("en")):
                out.append("%s %s: komut farkli\n   tr=%r\n   de=%r\n   en=%r" % (mid, p, code("tr"), code("de"), code("en")))
    # 2) gorev metnindeki dosya adlari module.json'da var mi
    for p, s in L["en"].items():
        m = re.match(r"/tasks/(t\d+)/text$", p)
        if not m:
            continue
        for x in spans(s):
            for fn in FILE.findall(x):
                base = os.path.basename(fn)
                if base not in mod:
                    out.append("%s %s: '%s' module.json'da yok (en)" % (mid, m.group(1), base))
print("\n".join(out) if out else "temiz")
print("bulgu:", len(out))
