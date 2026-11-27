import sys, socket, time, ctypes
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "chatelaine.cylabacademy.net", 44519
libc = ctypes.CDLL("libc.so.6")
libc.srand.argtypes = [ctypes.c_uint]
libc.rand.restype = ctypes.c_int
s = socket.create_connection((HOST, PORT), timeout=15)
s.settimeout(6)
time.sleep(0.4)
banner = b""
try:
    banner = s.recv(65536)
except Exception:
    pass
print("=== BANNIERE ===")
print(banner.decode("utf-8", "replace")[:600])
seed = int(time.time())
libc.srand(ctypes.c_uint(seed))
vals = [libc.rand() & 0xF for _ in range(30)]
print("valeurs predites (seed now):", vals[:10])
s.sendall(("".join(f"{v}\n" for v in vals)).encode())
time.sleep(1.0)
out = b""
try:
    while True:
        c = s.recv(65536)
        if not c:
            break
        out += c
except Exception:
    pass
print("=== REPONSE ===")
print(out.decode("utf-8", "replace")[:600])
s.close()
