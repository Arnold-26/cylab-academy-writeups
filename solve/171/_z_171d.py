import sys, re, json, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

a = b"861836f13e3d627dfa375bdb8389214e"
dwords = [0x5d47534a, 0x54034541, 0x0a5a025d, 0x0d455753,
          0x555d0005, 0x0e011054, 0x4b575541, 0x01465045]
b2 = b"".join(d.to_bytes(4, "little") for d in dwords)
print("tableau1:", a.decode())
print("tableau2:", b2.hex())
pw = "".join(chr(a[i] ^ b2[i]) for i in range(32))
print("mot de passe:", pw, "| len", len(pw))
print("inverse     :", pw[::-1])

cy = CyLab(delay=0.4)
cy.login()
cy.req("PUT", "/api/challenges/171/instance/?source=library")
host = port = None
for _ in range(12):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/171/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"nc\s+(-v\s+)?([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
    if m:
        host, port = m.group(2), int(m.group(3))
        break
print("cible:", host, port)
if not host:
    print("desc:", (d.get("description") or "")[:300])
else:
    for cand in (pw, pw[::-1]):
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
            print("%-34s -> %s" % (cand[:34], ("FLAG " + m.group(0)) if m else txt.replace("\n", " ")[:200]))
            if m:
                break
        except Exception as e:
            print(cand[:20], "ERR", type(e).__name__)
