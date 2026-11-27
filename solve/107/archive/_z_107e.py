import sys, re, json, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.set_int_max_str_digits(0)
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/107/instance/?source=library")
host = port = None
for _ in range(10):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/107/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
    if m:
        host, port = m.group(1), int(m.group(2))
        break
print("cible:", host, port)
s = socket.create_connection((host, port), timeout=20)
s.settimeout(15)
out = b""
t0 = time.time()
while time.time() - t0 < 14:
    try:
        c = s.recv(65536)
        if not c:
            break
        out += c
    except socket.timeout:
        break
txt = out.decode("latin-1", "replace")
print("taille recue:", len(out))
print("structure:", repr(txt[:120]))
print("...", repr(txt[-200:]))
nums = re.findall(r"\d{20,}", txt)
print("nombres longs:", len(nums), [len(x) for x in nums[:5]])
s.close()
