import sys, re, time, socket, hashlib, pathlib
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
B = pathlib.Path(r"/tmp/cylab_eps")
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
SALTS = ["squeexy", "Squeexy", "SQUEEXY", "rat", "RAT", "clone", "CLONE", "cloned", "Lacktoes",
         "DrLacktoes", "drlacktoes", "imposter", "secret", "salt", "cheese", "Cheese", "3f", "00",
         "cylab", "CyLab", "academy", "pico", "player", "squeak", "SQUEAK"]
hit = None
for name in names:
    for sal in SALTS:
        for cand in (name + sal, sal + name):
            if hashlib.sha256(cand.encode()).hexdigest() == target:
                hit = (name, sal)
                break
        if hit:
            break
    if hit:
        break
# variante : sans sel du tout
if not hit:
    for name in names:
        if hashlib.sha256(name.encode()).hexdigest() == target:
            hit = (name, "")
            break
print("MATCH:", hit)
s.close()
