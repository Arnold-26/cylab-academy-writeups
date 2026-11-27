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
print("cible:", host, port)
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def token_for(seed):
    random.seed(seed)
    return "".join(random.choice(ALPHA) for _ in range(20))


def try_window(offset):
    """teste 50 seeds consecutifs a partir de (t0 + offset)"""
    try:
        s = socket.create_connection((host, port), timeout=15)
        s.settimeout(4)
    except Exception as e:
        return None
    t0 = int(time.time() * 1000)
    try:
        s.recv(8192)
    except Exception:
        pass
    res = None
    for k in range(50):
        seed = t0 + offset + k
        s.sendall((token_for(seed) + "\n").encode())
        buf = b""
        try:
            while True:
                c = s.recv(8192)
                if not c:
                    break
                buf += c
                if b"Enter your guess" in buf or b"Congratulations" in buf or b"exhausted" in buf:
                    break
        except socket.timeout:
            break
        txt = buf.decode("utf-8", "replace")
        if "Congratulations" in txt:
            time.sleep(0.4)
            try:
                txt += s.recv(8192).decode("utf-8", "replace")
            except Exception:
                pass
            res = (offset + k, txt)
            break
        if "exhausted" in txt:
            break
    s.close()
    return res


found = None
t_start = time.time()
for off in range(-3000, 3001, 50):
    r = try_window(off)
    if r:
        found = r
        print("SUCCES offset=%d apres %.0fs" % (r[0], time.time() - t_start))
        print(r[1][:400])
        f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r[1])
        if f:
            print("FLAG:", f.group(0))
        break
    if off % 500 == 0:
        print("  offset %+d testé (%.0fs)" % (off, time.time() - t_start), flush=True)
print("fin:", bool(found))
