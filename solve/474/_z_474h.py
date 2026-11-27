import sys, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "chatelaine.cylabacademy.net", 24956
s = socket.create_connection((HOST, PORT), timeout=25)
s.settimeout(8)
time.sleep(0.6)


def rd(t=2.0):
    s.settimeout(t)
    buf = b""
    t0 = time.time()
    while time.time() - t0 < t:
        try:
            c = s.recv(16384)
            if not c:
                break
            buf += c
        except socket.timeout:
            break
    return buf.decode("utf-8", "replace")


banner = rd(1.5)
m = re.search(r"guess it:\s+([0-9a-f]{64})", banner)
print("hash:", m.group(1) if m else None)
s.sendall(b"g\n")
time.sleep(0.5)
p1 = rd(1.5)
print("=== prompt 1 ===")
print(p1[:400])
s.sendall(b"Gouda\n")
time.sleep(0.5)
p2 = rd(1.5)
print("=== prompt 2 (apres le fromage) ===")
print(p2[:500])
s.close()
