import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from pathlib import Path
base = Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\pachinko")
pat = re.compile(rb"(?:academy|picoCTF|flag)\{[^}]{2,120}\}")
found = []
for p in base.rglob("*"):
    if not p.is_file():
        continue
    try:
        d = p.read_bytes()
    except Exception:
        continue
    for m in pat.finditer(d):
        found.append((str(p.relative_to(base)), m.group(0).decode("latin-1")))
for f, s in found:
    print("%-45s %s" % (f[:45], s))
if not found:
    print("aucun flag litteral")
    # chercher les mots 'flag' avec contexte
    for p in base.rglob("*"):
        if p.is_file() and p.stat().st_size < 200000:
            d = p.read_bytes()
            for m in re.finditer(rb"flag", d):
                seg = d[max(0,m.start()-60):m.start()+120]
                t = re.sub(rb"[^\x20-\x7e]", b".", seg).decode("latin-1")
                print("%-30s ... %s" % (str(p.relative_to(base))[:30], t[:150]))
                break
