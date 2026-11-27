import sys, socket, time, re, ctypes
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "chatelaine.cylabacademy.net", 44519
libc = ctypes.CDLL("libc.so.6")
libc.srand.argtypes = [ctypes.c_uint]
libc.rand.restype = ctypes.c_int


def gen(seed, n=30):
    libc.srand(ctypes.c_uint(seed))
    return [libc.rand() & 0xF for _ in range(n)]


def attempt(seed):
    s = socket.create_connection((HOST, PORT), timeout=15)
    s.settimeout(6)
    time.sleep(0.3)
    try:
        s.recv(65536)
    except Exception:
        pass
    vals = gen(seed)
    s.sendall(("".join(f"{v}\n" for v in vals)).encode())
    time.sleep(1.2)
    out = b""
    try:
        while True:
            c = s.recv(65536)
            if not c:
                break
            out += c
    except Exception:
        pass
    s.close()
    return out.decode("utf-8", "replace")


now = int(time.time())
for delta in (0, -1, 1, -2, 2, -3, 3, -4, 4, -5, 5, -6, 6):
    seed = now + delta
    txt = attempt(seed)
    m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
    print(f"seed {seed} (delta {delta}): len={len(txt)} flag={m.group(0) if m else None}")
    if m:
        break
