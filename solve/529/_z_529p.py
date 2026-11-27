import sys, re, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\pb529\dec\smali_classes3\com\example\picobank\MainActivity.smali")
txt = p.read_text(errors="replace")
vals = re.findall(r'\$ ([01]{5,9})', txt)
print("valeurs:", len(vals))
chars = []
for v in vals:
    n = int(v, 2)
    chars.append(chr(n) if 32 <= n < 127 else "?")
    print("  %-9s -> %3d %r" % (v, n, chr(n) if 32 <= n < 127 else ""))
s = "".join(chars)
print("\nCHAINE:", s)
m = re.search(r"academy\{[^}]*\}", s)
print("FLAG?:", m.group(0) if m else None)
