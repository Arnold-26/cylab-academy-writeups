import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
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


def conn():
    s = socket.create_connection((host, port), timeout=20)
    s.settimeout(5)
    time.sleep(0.2)
    try:
        s.recv(8192)
    except Exception:
        pass
    return s


def guess(s, tok):
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
        pass
    return buf.decode("utf-8", "replace")


# connexion 1 : consommer 50 tentatives
s1 = conn()
last = ""
for i in range(50):
    last = guess(s1, "X" * 20)
print("conn1 dernier message:", last[-120:].replace("\n", " "))
s1.close()

# connexion 2 : une seule tentative
s2 = conn()
r2 = guess(s2, "Y" * 20)
print("conn2 reponse:", r2[-160:].replace("\n", " "))
print("=> token PERSISTANT (partage entre connexions):", "exhausted" in r2)
s2.close()
