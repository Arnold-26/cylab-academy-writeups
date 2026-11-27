import sys, re, time, socket, hashlib, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"C:\Users\arnol\AppData\Local\Temp\cylab_eps")
names = [l.rstrip("\n") for l in (B / "474_cheese_list.txt").read_text(errors="replace").splitlines() if l.strip()]
HOST, PORT = "chatelaine.cylabacademy.net", 24956
s = socket.create_connection((HOST, PORT), timeout=25)
s.settimeout(10)
time.sleep(0.8)
buf = b""
t0 = time.time()
while time.time() - t0 < 3:
    try:
        c = s.recv(16384)
        if not c:
            break
        buf += c
    except socket.timeout:
        break
m = re.search(rb"guess it:\s+([0-9a-f]{64})", buf)
target = m.group(1).decode()
print("hash:", target)
hit = None
n = 0
t0 = time.time()
for i in range(65536):
    salt = "%04x" % i
    for name in names:
        for cand in (name + salt, salt + name):
            n += 1
            if hashlib.sha256(cand.encode()).hexdigest() == target:
                hit = (name, salt)
                break
        if hit:
            break
    if hit:
        break
print("essais:", n, "en %.1fs" % (time.time() - t0))
print("MATCH:", hit)
if hit:
    name, salt = hit
    s.sendall(b"g\n"); time.sleep(0.4)
    buf = b""
    try:
        buf = s.recv(8192)
    except Exception:
        pass
    s.sendall((name + "\n").encode()); time.sleep(0.4)
    try:
        buf = s.recv(8192)
    except Exception:
        pass
    s.sendall((salt + "\n").encode()); time.sleep(0.6)
    fin = b""
    try:
        fin = s.recv(16384)
    except Exception:
        pass
    txt = fin.decode("utf-8", "replace")
    print(txt[-400:])
    f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
    if f:
        print("FLAG:", f.group(0))
s.close()
