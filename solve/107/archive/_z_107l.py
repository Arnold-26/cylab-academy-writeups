import sys, re, json, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.set_int_max_str_digits(0)
sys.path.insert(0, r".")
from cylab2 import CyLab

cy = CyLab(delay=0.3)
cy.login()
cy.req("PUT", "/api/challenges/107/instance/?source=library")
host = port = None
for _ in range(10):
    time.sleep(0.8)
    st, b = cy.req("GET", "/api/challenges/107/instance/")
    d = json.loads(b) if b.startswith("{") else {}
    m = re.search(r"nc\s+([A-Za-z0-9.\-]+)\s+(\d{2,5})", d.get("description") or "")
    if m:
        host, port = m.group(1), int(m.group(2))
        break
alpha = [chr(c) for c in range(32, 127)]
s = socket.create_connection((host, port), timeout=20)
s.settimeout(3)
banner = b""
t0 = time.time()
while time.time() - t0 < 3:
    try:
        c = s.recv(65536)
        if not c:
            break
        banner += c
        if b"give me" in banner:
            break
    except socket.timeout:
        break
flagnum = re.search(r"flag:\s*(\d+)", banner.decode("latin-1", "replace")).group(1)
codebook = {}
for ch in alpha:
    s.sendall(ch.encode() + b"\n")
    time.sleep(0.2)
    r = b""
    t0 = time.time()
    while time.time() - t0 < 1.2:
        try:
            c = s.recv(65536)
            if not c:
                break
            r += c
        except socket.timeout:
            break
    m = re.search(rb"(\d{20,})", r)
    if m:
        codebook[ch] = int(m.group(1))
s.close()
fb = int(flagnum).to_bytes((int(flagnum).bit_length() + 7) // 8, "big")
print("flag bytes:", len(fb), "| codebook:", len(codebook))
best = None
for bs in (126, 127, 128, 129, 130, 256):
    rev = {v.to_bytes(bs, "big"): ch for ch, v in codebook.items() if v.bit_length() <= bs * 8}
    for off in range(0, 4 * bs):
        pos = off
        out = []
        while pos + bs <= len(fb):
            blk = fb[pos:pos + bs]
            if blk in rev:
                out.append(rev[blk])
                pos += bs
            else:
                break
        if len(out) > 2:
            res = "".join(out)
            if best is None or len(res) > len(best[2]):
                best = (bs, off, res)
            print("bs=%d off=%d -> %r" % (bs, off, res[:60]))
if best:
    print("MEILLEUR:", best[0], best[1], best[2])
    m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", best[2])
    print("FLAG:", m.group(0) if m else None)
