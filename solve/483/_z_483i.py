import sys, socket, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "xebec.cylabacademy.net", 47902


def submit(data, label, delay=0.3):
    print("=== %s ===" % label)
    try:
        s = socket.create_connection((HOST, PORT), timeout=30)
        s.settimeout(45)
        s.sendall(data)
        time.sleep(delay)
        s.shutdown(socket.SHUT_WR)
        out = b""
        t0 = time.time()
        while time.time() - t0 < 45:
            try:
                c = s.recv(16384)
                if not c:
                    break
                out += c
            except socket.timeout:
                break
        s.close()
        print(out.decode("utf-8", "replace")[:600])
    except Exception as e:
        print("ERR", type(e).__name__)


submit(b"rule A { condition: true }\n", "regle minimale")
submit(b"rule A { condition: true }", "sans newline final")
submit(b"", "vide")
