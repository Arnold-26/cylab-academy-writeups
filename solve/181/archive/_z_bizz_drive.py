import os, pty, sys, time, re, select, subprocess

BIN = sys.argv[1] if len(sys.argv) > 1 else "./_z_bizz"
MODE = sys.argv[2] if len(sys.argv) > 2 else "correct"
LIMIT = int(sys.argv[3]) if len(sys.argv) > 3 else 4000

def fizz(n):
    if n % 15 == 0:
        return b"fizzbuzz"
    if n % 3 == 0:
        return b"fizz"
    if n % 5 == 0:
        return b"buzz"
    return str(n).encode()

m, s = pty.openpty()
p = subprocess.Popen([BIN], stdin=s, stdout=s, stderr=s, close_fds=True)
os.close(s)
buf = b""
log = []
nq = 0
last = time.time()
deadline = time.time() + 60
while time.time() < deadline:
    r, _, _ = select.select([m], [], [], 0.25)
    if r:
        try:
            d = os.read(m, 65536)
        except OSError:
            break
        if not d:
            break
        buf += d
        last = time.time()
    else:
        if p.poll() is not None:
            break
        # stall?
        if time.time() - last > 1.0 and buf:
            tail = buf[-40:]
            # prompt en attente ?
            mm = re.search(rb"(\d+)\? $", buf)
            if mm:
                n = int(mm.group(1))
                if nq < LIMIT:
                    ans = fizz(n) if MODE == "correct" else b"x"
                    log.append((n, ans))
                    os.write(m, ans + b"\n")
                    buf = b""
                    nq += 1
                    last = time.time()
                    continue
            # sinon : c'est un fgets -> envoyer une ligne
            os.write(m, b"L\n")
            buf = b""
            last = time.time()
            continue
        if time.time() - last > 8:
            break

try:
    p.wait(timeout=2)
except Exception:
    p.kill()
os.close(m)
print("questions:", nq)
print("prompts:", [(n, a.decode()) for n, a in log[:40]])
print("...")
print("last:", [(n, a.decode()) for n, a in log[-20:]])
