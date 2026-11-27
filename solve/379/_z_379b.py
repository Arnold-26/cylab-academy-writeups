import sys, json, re, time, socket, math
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.5)
cy.login()
cy.req("PUT", "/api/challenges/379/instance/?source=library")
host = port = None
for _ in range(10):
    time.sleep(1)
    st, b = cy.req("GET", "/api/challenges/379/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"nc\s+(-v\s+)?([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
    if m:
        host, port = m.group(2), int(m.group(3))
        break
print("cible:", host, port)
s = socket.create_connection((host, port), timeout=15)
s.settimeout(8)
buf = b""
t0 = time.time()
while b"vainglory" not in buf and time.time() - t0 < 8:
    try:
        c = s.recv(4096)
        if not c:
            break
        buf += c
    except socket.timeout:
        break
txt = buf.decode("latin-1", "replace")
print(txt[:300])
anger = int(re.search(r"anger\s*=\s*(\d+)", txt).group(1))
envy = int(re.search(r"envy\s*=\s*(\d+)", txt).group(1))
e = 65537
print("anger:", anger, "| envy:", envy)
# e*d - 1 = k * phi(n) ; on cherche k tel que phi donne un discriminant carre
ed1 = e * envy - 1
found = None
for k in range(1, e + 1):
    if ed1 % k:
        continue
    phi = ed1 // k
    # n inconnu... mais on peut retrouver n ? non : on a besoin de n
    pass
print("ed1 bits:", ed1.bit_length())
# Hmm : n n'est pas donne ; il faut le deduire autrement
s.close()
