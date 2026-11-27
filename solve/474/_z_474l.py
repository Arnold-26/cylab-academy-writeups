import sys, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "chatelaine.cylabacademy.net", 24956
s = socket.create_connection((HOST, PORT), timeout=25)
s.settimeout(8)
time.sleep(0.8)
buf = b""
t0 = time.time()
while time.time() - t0 < 4:
    try:
        c = s.recv(16384)
        if not c:
            break
        buf += c
    except socket.timeout:
        break
print("=== BANNER COMPLET (%d octets) ===" % len(buf))
print(buf.decode("utf-8", "replace"))
s.close()
