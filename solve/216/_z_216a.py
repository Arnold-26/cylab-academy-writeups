import sys, socket, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "mars.cylabacademy.net", 31890
try:
    s = socket.create_connection((HOST, PORT), timeout=15)
    s.settimeout(4)
    time.sleep(0.8)
    data = b""
    try:
        data = s.recv(8192)
    except Exception:
        pass
    print("=== banner ===")
    print(data.decode("utf-8", "replace")[:1500])
    s.sendall(b"A\n")
    time.sleep(0.8)
    try:
        print("=== apres A ===")
        print(s.recv(8192).decode("utf-8", "replace")[:800])
    except Exception:
        pass
    s.close()
except Exception as e:
    print("err", type(e).__name__, e)
