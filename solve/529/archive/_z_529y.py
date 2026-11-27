import sys, re, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = pathlib.Path(r"/tmp/cylab_eps\pb529\dec\smali_classes3\com\example\picobank\MainActivity.smali")
txt = p.read_text(errors="replace")
# chaque transaction : new-instance ... const-string a / b / c ... invoke-direct {v4, X, Y, Z, W}
blocks = re.findall(r'new-instance[^\n]*Transaction;((?:\n.*?){0,40}?)invoke-direct \{v4, (v\d+), (v\d+), (v\d+), (v\d+)\}[^\n]*Transaction;-><init>', txt, re.S)
# reconstruire les const-string par registre
rows = []
for block, r1, r2, r3, r4 in blocks:
    regs = dict(re.findall(r'const-string (v\d+), "([^"]*)"', block))
    name, date, amount = regs.get(r1), regs.get(r2), regs.get(r3)
    rows.append((date, amount, name, r1, r2, r3))
print("transactions:", len(rows))
chars = []
for date, amount, name, r1, r2, r3 in rows:
    v = None
    if amount and re.fullmatch(r"\$ ([01]+)", amount):
        v = int(amount[2:], 2)
        chars.append(chr(v) if 32 <= v < 127 else "?")
    print("  %-12s %-12s %-22s -> %s" % (date, amount, (name or "")[:22], chr(v) if v and 32 <= v < 127 else ""))
print("\nCHAINE:", "".join(chars))
