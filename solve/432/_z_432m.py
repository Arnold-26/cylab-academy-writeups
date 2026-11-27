import sys, socket, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST = "xebec.cylabacademy.net"
IMG = r"/tmp/cylab_eps\432_modified.jpg"
data = open(IMG, "rb").read()
print("image:", len(data), "octets")
for port in (11287, 11534):
    print("\n=== port %d ===" % port)
    try:
        s = socket.create_connection((HOST, port), timeout=20)
        s.settimeout(15)
        s.sendall(data)
        try:
            s.shutdown(socket.SHUT_WR)
        except Exception:
            pass
        out = b""
        t0 = time.time()
        while time.time() - t0 < 15:
            try:
                c = s.recv(8192)
                if not c:
                    break
                out += c
            except socket.timeout:
                break
        s.close()
        print(out.decode("latin-1", "replace")[:1500])
    except Exception as e:
        print("ERR", type(e).__name__, e)
