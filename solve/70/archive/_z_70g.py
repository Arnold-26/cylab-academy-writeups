import sys, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
p = r"/tmp/cylab_eps\70_investigative-reversing-0-mystery.png"
d = open(p, "rb").read()
raw = d[-26:]
print("brut:", raw)
buf = bytearray(raw)
for i in range(6, 15):
    buf[i] = (buf[i] - 5) & 0xFF
buf[15] = (buf[15] + 3) & 0xFF
flag = bytes(buf)
print("reconstruit:", flag)
try:
    print("texte:", flag.decode())
except Exception:
    pass
m = re.search(rb"(?:academy|picoCTF)\{[^}]*\}", flag)
print("FLAG:", m.group(0).decode() if m else None)
