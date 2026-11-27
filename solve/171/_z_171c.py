import sys, re, json, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/171/instance/?source=library")
host = port = None
for _ in range(10):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/171/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"nc\s+(-v\s+)?([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
    if m:
        host, port = m.group(2), int(m.group(3))
        break
print("cible:", host, port)
a = "861836f13e3d627dfa375bdb8389214e"
b2 = bytes.fromhex("4a53477d41450354 5d025a0a5357450d 05005d55541001 0e4155574b455046".replace(" ", ""))
pw = "".join(chr(ord(c) ^ b2[i]) for i, c in enumerate(a))
print("mot de passe calcule:", pw, "| len", len(pw))
for cand in (pw, pw[::-1], "reversengineericanbarelyforward"):
    try:
        s = socket.create_connection((host, port), timeout=12)
        s.settimeout(6)
        time.sleep(0.4)
        try:
            banner = s.recv(500)
        except Exception:
            banner = b""
        s.sendall(cand.encode() + b"\n")
        time.sleep(0.6)
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
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", txt)
        print("%-34s -> %s" % (cand[:34], ("FLAG " + m.group(0)) if m else txt[:150].replace("\n", " ")))
        if m:
            break
    except Exception as e:
        print(cand[:20], "ERR", type(e).__name__)
