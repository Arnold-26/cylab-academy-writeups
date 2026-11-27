import sys, socket, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST = "xebec.cylabacademy.net"
IMG = r"/tmp/cylab_eps\432_patched.jpg"
data = open(IMG, "rb").read()
for port in (11534, 11287):
    print("\n=== port %d ===" % port)
    out = b""
    try:
        s = socket.create_connection((HOST, port), timeout=30)
        s.settimeout(25)
        s.sendall(data)
        try:
            s.shutdown(socket.SHUT_WR)
        except Exception:
            pass
        t0 = time.time()
        while time.time() - t0 < 25:
            try:
                c = s.recv(8192)
                if not c:
                    break
                out += c
            except socket.timeout:
                break
            except ConnectionResetError:
                print("  (reset apres %d octets)" % len(out))
                break
        s.close()
    except Exception as e:
        print("  ERR", type(e).__name__, e)
    print(out.decode("latin-1", "replace")[-1500:])
