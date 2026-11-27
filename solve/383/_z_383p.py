import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\383_disk.img"
OFF = 731136 * 512
with open(p, "rb") as f:
    f.seek(OFF + 56274 * 4096)
    data = f.read(4096)
slack = data[12:].rstrip(b"\x00").decode("ascii", "replace")
phi = (1 + 5 ** 0.5) / 2
tokens = [t for t in slack.split(".") if t]
vals = []
for t in tokens:
    n = len(t)
    vals.append(sum(int(d) * phi ** (n - 1 - i) for i, d in enumerate(t) if d == "1"))
hexd = "0123456789abcdef"
for label, fn in (("mod16", lambda v: round(v) % 16),
                  ("int16", lambda v: round(v) % 16 if round(v) < 16 else None)):
    s = "".join(hexd[fn(v)] if fn(v) is not None else "?" for v in vals)
    print("%s: %s" % (label, s[:128]))
    try:
        raw = bytes.fromhex(s[:len(s) // 2 * 2])
        print("   ascii:", raw.decode("latin-1", "replace")[:150])
    except Exception as e:
        print("   hex err", e)
# valeurs telles quelles : peut-on voir des octets ?
b = bytes([round(v) % 256 for v in vals])
print("\nmod256 ascii:", b.decode("latin-1", "replace")[:150])
print("mod256 hex:", b.hex()[:150])
