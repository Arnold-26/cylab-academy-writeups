import sys, socket, time, re
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "xebec.cylabacademy.net", 42968
s = socket.create_connection((HOST, PORT), timeout=20)
s.settimeout(10)
time.sleep(0.5)
buf = b""
try:
    buf = s.recv(65536)
except Exception:
    pass
print("banner:", buf.decode("utf-8", "replace")[:200])
found = None
for guess in range(1, 4097):
    s.sendall(f"{guess}\n".encode())
    time.sleep(0.004)
    try:
        s.settimeout(0.05)
        d = s.recv(65536)
        if b"New winner" in d or b"Congrats" in d:
            print("TROUVE:", guess, "|", d[:200])
            found = guess
            break
    except socket.timeout:
        continue
    except Exception:
        pass
print("resultat:", found)
s.close()
