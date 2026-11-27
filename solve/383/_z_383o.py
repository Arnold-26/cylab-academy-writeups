import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"/tmp/cylab_eps\383_disk.img"
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
    v = sum(int(d) * phi ** (n - 1 - i) for i, d in enumerate(t) if d == "1")
    vals.append(v)
print("valeurs brutes (30):", [round(v, 2) for v in vals[:30]])
print("min/max:", round(min(vals), 2), round(max(vals), 2))
# hypothese : valeur = code ASCII direct ?
print("arrondis:", [round(v) for v in vals[:30]])
print("chars:", "".join(chr(round(v)) if 32 <= round(v) < 127 else "." for v in vals[:60]))
# longueurs des tokens
print("longueurs:", sorted(set(len(t) for t in tokens)))
