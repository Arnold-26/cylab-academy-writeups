import sys, socket, time, re, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31890
for n in (256, 512, 1024, 4096):
    try:
        s = socket.create_connection((HOST, PORT), timeout=12)
        s.settimeout(4)
        time.sleep(0.6)
        try:
            s.recv(8192)
        except Exception:
            pass
        s.sendall(b"A" * n + b"\n")
        time.sleep(0.8)
        out = b""
        try:
            out = s.recv(8192)
        except Exception:
            pass
        txt = out.decode("utf-8", "replace")
        print(f"--- n={n} ---")
        print(txt[-200:])
        s.close()
    except Exception as e:
        print(n, "err", type(e).__name__)
