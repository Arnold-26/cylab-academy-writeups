import sys, re, time, socket, hashlib, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
names = [l.rstrip("\n") for l in (B / "474_cheese_list.txt").read_text(errors="replace").splitlines() if l.strip()]
HOST, PORT = "chatelaine.cylabacademy.net", 24956


def rd(s, t=2.0):
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


for attempt in range(3):
    s = socket.create_connection((HOST, PORT), timeout=25)
    time.sleep(0.5)
    banner = rd(s, 1.5)
    m = re.search(r"guess it:\s+([0-9a-f]{64})", banner)
    if not m:
        print("pas de hash:", banner[-200:])
        s.close()
        continue
    target = m.group(1)
    print("hash:", target)
    hit = None
    for name in names:
        for i in range(256):
            for salt in ("%02x" % i, "%02X" % i):
                for cand in (name + salt, salt + name):
                    if hashlib.sha256(cand.encode()).hexdigest() == target:
                        hit = (name, salt)
                        break
                if hit:
                    break
            if hit:
                break
        if hit:
            break
    print("MATCH:", hit)
    if not hit:
        s.close()
        continue
    name, salt = hit
    s.sendall(b"g\n")
    time.sleep(0.4)
    rd(s, 1.0)
    s.sendall((name + "\n").encode())
    time.sleep(0.4)
    p = rd(s, 1.2)
    print("prompt2:", p[-120:])
    s.sendall((salt + "\n").encode())
    time.sleep(0.6)
    fin = rd(s, 2.5)
    print("=== fin ===")
    print(fin[-500:])
    f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", fin)
    if f:
        print("FLAG:", f.group(0))
        s.close()
        break
    s.close()
