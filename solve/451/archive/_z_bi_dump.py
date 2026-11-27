import sys
lines = open('/tmp/bi/b1.asm', errors='replace').read().splitlines()
lo, hi = sys.argv[1], sys.argv[2]
started = False
n = 0
for ln in lines:
    if ':' in ln:
        a = ln.split(':')[0].strip()
        try:
            v = int(a, 16)
        except ValueError:
            continue
        if v < int(lo, 16):
            continue
        if v >= int(hi, 16):
            break
        print(ln)
        n += 1
        if n > 400:
            print("... (tronque)")
            break
