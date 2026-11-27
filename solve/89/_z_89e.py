import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=1.0)
cy.login()
cy.req("PUT", "/api/challenges/89/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/89/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d+)", d.get("description") or "")
        if m:
            host, port = m.group(1), int(m.group(2))
            break
print("cible:", host, port)


def recv_until(s, marker=b"guess?", timeout=4.0):
    s.settimeout(timeout)
    buf = b""
    t0 = time.time()
    while marker not in buf and time.time() - t0 < timeout:
        try:
            c = s.recv(4096)
            if not c:
                break
            buf += c
        except socket.timeout:
            break
    return buf


s = socket.create_connection((host, port), timeout=20)
s.settimeout(5)
recv_until(s, b"guess?")
# d'abord la valeur locale
for guess in [-815] + list(range(-1, -4095, -1)):
    s.sendall(f"{guess}\n".encode())
    r = recv_until(s, b"\n\n", 3.0)
    if b"New winner" in r or b"Congrats" in r:
        print("TROUVE:", guess, "|", r[:150].replace(b"\n", b" "))
        break
    if not r:
        print("connexion perdue a", guess)
        break
else:
    print("aucun")
s.close()
