import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab
import random

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


s = socket.create_connection((host, port), timeout=20)
s.settimeout(6)
t0 = int(time.time() * 1000)
time.sleep(0.3)
try:
    s.recv(8192)
except Exception:
    pass
found = None
# 50 tentatives : seeds t0-25 .. t0+24
for delta in range(-25, 25):
    seed = t0 + delta
    tok = token_for(seed)
    s.sendall((tok + "\n").encode())
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
        found = (delta, tok)
        # lire le flag
        time.sleep(0.5)
        try:
            extra = s.recv(8192).decode("utf-8", "replace")
        except Exception:
            extra = ""
        print("TROUVE delta=%d token=%s" % (delta, tok))
        print((txt + extra)[:500])
        f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt + extra)
        if f:
            print("FLAG:", f.group(0))
        break
print("resultat:", found)
s.close()
