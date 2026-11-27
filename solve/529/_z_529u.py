import sys, re, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = pathlib.Path(r"/tmp/cylab_eps\pb529\dec\smali_classes3\com\example\picobank\MainActivity.smali")
txt = p.read_text(errors="replace")
allb = re.findall(r'"\$ ([^"]*)"', txt)
print("tous les montants:", len(allb))
for v in allb:
    n = None
    if re.fullmatch(r"[01]+", v):
        n = int(v, 2)
    print("  %-12r -> %s %s" % (v, n, repr(chr(n)) if n and 32 <= n < 127 else ""))
