import sys, json, re, time, socket, random
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/468/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/468/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"([A-Za-z0-9][A-Za-z0-9.\-]*\.net)\s+`?(\d{4,5})", d.get("description") or "")
        if m:
            host, port = m.group(1), int(m.group(2))
            break
print("cible:", host, port, flush=True)
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def tok(seed):
    random.seed(seed)
    return "".join(random.choice(ALPHA) for _ in range(20))


def window(off):
    try:
        s = socket.create_connection((host, port), timeout=10)
        s.settimeout(6)
    except Exception:
        return None
    t0 = int(time.time() * 1000)
    payload = "\n".join(tok(t0 + off + k) for k in range(50)) + "\n"
    try:
        s.sendall(payload.encode())
    except Exception:
        s.close()
        return None
    out = b""
    t1 = time.time()
    while time.time() - t1 < 6:
        try:
            c = s.recv(65536)
            if not c:
                break
            out += c
            if b"exhausted" in out or b"Congratulations" in out:
                break
        except socket.timeout:
            break
    s.close()
    txt = out.decode("utf-8", "replace")
    if "Congratulations" in txt:
        return (off, txt)
    return None


t_start = time.time()
found = None
lo, hi, step = -10000, 10001, 50
for off in range(lo, hi, step):
    r = window(off)
    if r:
        found = r
        print("SUCCES offset=%d apres %.0fs" % (r[0], time.time() - t_start))
        print(r[1][:400])
        break
    if (off - lo) % 2000 == 0:
        print("  offset %+d (%.0fs)" % (off, time.time() - t_start), flush=True)
print("fin:", bool(found))
if found:
    f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", found[1])
    print("FLAG:", f.group(0) if f else None)
    open(r"./_z_468flag.txt", "w").write(f.group(0) if f else "")
