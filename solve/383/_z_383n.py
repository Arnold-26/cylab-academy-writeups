import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"C:\Users\arnol\AppData\Local\Temp\cylab_eps\383_disk.img"
OFF = 731136 * 512
with open(p, "rb") as f:
    f.seek(OFF + 56274 * 4096)
    data = f.read(4096)
slack = data[12:].rstrip(b"\x00").decode("ascii", "replace")
print("slack len:", len(slack))
print("debut:", slack[:80])
phi = (1 + 5 ** 0.5) / 2
tokens = [t for t in slack.split(".") if t]
print("tokens:", len(tokens))
chars = []
for t in tokens:
    n = len(t)
    val = sum(int(d) * phi ** (n - 1 - i) for i, d in enumerate(t) if d == "1")
    chars.append((round(val), chr(round(val)) if 32 <= round(val) < 127 else "?"))
s = "".join(c for _, c in chars)
print("decode:", s[:300])
m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", s)
print("FLAG:", m.group(0) if m else None)
