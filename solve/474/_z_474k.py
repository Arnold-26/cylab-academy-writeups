import sys, re, time, socket, hashlib, pathlib, string
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
names = [l.rstrip("\n") for l in (B / "474_cheese_list.txt").read_text(errors="replace").splitlines() if l.strip()]
HOST, PORT = "chatelaine.cylabacademy.net", 24956
CH = string.ascii_lowercase + string.digits + string.ascii_uppercase
sals = [a + b for a in CH for b in CH]
print("sels:", len(sals))


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


s = socket.create_connection((HOST, PORT), timeout=25)
time.sleep(0.5)
banner = rd(s, 1.5)
m = re.search(r"guess it:\s+([0-9a-f]{64})", banner)
target = m.group(1)
print("hash:", target)
hit = None
for name in names:
    for salt in sals:
        for cand in (name + salt, salt + name):
            if hashlib.sha256(cand.encode()).hexdigest() == target:
                hit = (name, salt)
                break
        if hit:
            break
    if hit:
        break
print("MATCH:", hit)
if hit:
    name, salt = hit
    s.sendall(b"g\n"); time.sleep(0.4); rd(s, 1.0)
    s.sendall((name + "\n").encode()); time.sleep(0.4); rd(s, 1.2)
    s.sendall((salt + "\n").encode()); time.sleep(0.6)
    fin = rd(s, 2.5)
    print(fin[-400:])
    f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", fin)
    if f:
        print("FLAG:", f.group(0))
s.close()
