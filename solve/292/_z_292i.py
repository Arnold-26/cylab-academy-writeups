import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
F = r"/tmp/cylab_eps\292_vuln"
d = open(F, "rb").read()
OFF, VA, SZ = 0x1000, 0x08049000, 0x663b0
t = d[OFF:OFF + SZ]
out = []
i = 0
while True:
    i = t.find(b"\xcd\x80", i)
    if i < 0:
        break
    nxt = t[i + 2:i + 8].hex()
    out.append((VA + i, nxt))
    i += 1
print("int 0x80 trouves:", len(out))
for a, nxt in out:
    ok = nxt.startswith("c3")
    print("  %s  suivants: %s %s" % (hex(a), nxt, "<-- RET OK" if ok else ""))
