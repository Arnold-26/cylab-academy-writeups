import sys, socket, time, ctypes, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "chatelaine.cylabacademy.net", 44519
libc = ctypes.CDLL("libc.so.6")
libc.srand.argtypes = [ctypes.c_uint]
libc.rand.restype = ctypes.c_int


def attempt(seed, wait=4.0):
    s = socket.create_connection((HOST, PORT), timeout=15)
    s.settimeout(10)
    time.sleep(0.4)
    try:
        s.recv(65536)
    except Exception:
        pass
    libc.srand(ctypes.c_uint(seed))
    vals = [libc.rand() & 0xF for _ in range(30)]
    s.sendall(("".join(f"{v}\n" for v in vals)).encode())
    time.sleep(wait)
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
for delta in (0, -1, 1, -2, 2):
    txt = attempt(now + delta)
    m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
    last = txt.strip().split("\n")[-3:] if txt.strip() else []
    print(f"seed {now+delta}: len={len(txt)} | fin={last} | flag={m.group(0) if m else None}")
    if m:
        break
