import socket, sys, time, re, hashlib, random, os
import multiprocessing as mp
from flint import fmpz_mod_poly_ctx
from Crypto.Util.number import GCD

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = open(r"./_z_120url.txt").read().split()
PORT = int(PORT)

GLOBAL_PREFIX = b""
GLOBAL_TARGET = b""


def pow_worker(args):
    start, step = args
    prefix, target = GLOBAL_PREFIX, GLOBAL_TARGET
    i = start
    while True:
        h = hashlib.md5(prefix + str(i).encode()).digest()
        if h[-3:] == target:
            return prefix + str(i).encode()
        i += step


def solve_pow(prefix, target_hex, nproc=8):
    global GLOBAL_PREFIX, GLOBAL_TARGET
    GLOBAL_PREFIX = prefix.encode()
    GLOBAL_TARGET = bytes.fromhex(target_hex)
    t0 = time.time()
    with mp.Pool(nproc) as pool:
        for res in pool.imap_unordered(pow_worker, [(k, nproc) for k in range(nproc)], chunksize=1):
            pool.terminate()
            print("  PoW trouve en %.1fs : %r" % (time.time() - t0, res), flush=True)
            return res.decode()
    return None


def attack(n, e, L):
    R = fmpz_mod_poly_ctx(n)
    m = random.randint(2, n - 1)
    g = pow(m, e, n)
    cur = pow(m, -1, n)
    vs = []
    for b in range(L):
        vs.append(cur)
        cur = cur * g % n
    u = pow(g, L, n)
    t0 = time.time()
    polys = [R([-1, vs[b]]) for b in range(L)]
    while len(polys) > 1:
        nxt = []
        for i in range(0, len(polys) - 1, 2):
            nxt.append(polys[i] * polys[i + 1])
        if len(polys) % 2:
            nxt.append(polys[-1])
        polys = nxt
    P = polys[0]
    del polys
    print("  deg(P)=%d construit en %.1fs" % (P.degree(), time.time() - t0), flush=True)
    pts = []
    x = 1
    for a in range(L):
        pts.append(x)
        x = x * u % n
    t1 = time.time()
    vals = P.multipoint_evaluate(pts)
    print("  multipoint eval en %.1fs" % (time.time() - t1), flush=True)
    for a, val in enumerate(vals):
        gg = GCD(int(val), n)
        if 1 < gg < n:
            print("  facteur trouve a a=%d en %.1fs" % (a, time.time() - t0), flush=True)
            return gg
    return None


def main():
    s = socket.create_connection((HOST, PORT), timeout=60)
    s.settimeout(30)
    buf = b""

    def until(pat, timeout=120):
        nonlocal buf
        end = time.time() + timeout
        while pat not in buf:
            if time.time() > end:
                raise TimeoutError(pat)
            d = s.recv(65536)
            if not d:
                raise EOFError
            buf += d
        return buf

    until(b"hex digits: ")
    head = buf.decode("latin-1")
    m = re.search(r"starts with \"(\d{5})\".*?hex digits: ([0-9a-f]{6})", head, re.S)
    if not m:
        print("banner inattendu:", head[:300])
        return
    pfx, tgt = m.group(1), m.group(2)
    print("PoW: prefixe=%s cible=%s" % (pfx, tgt), flush=True)
    ans = solve_pow(pfx, tgt)
    s.sendall(ans.encode() + b"\n")
    buf = b""
    until(b"Clue : ")
    txt = buf.decode("latin-1")
    print(txt[:400], flush=True)
    mn = re.search(r"Public Modulus :\s+(\d+)", txt)
    me = re.search(r"Clue :\s+(\d+)", txt)
    n = int(mn.group(1)); e = int(me.group(1))
    print("n=%d bits, e=%d bits" % (n.bit_length(), e.bit_length()), flush=True)
    L = 1 << 18
    t0 = time.time()
    fac = attack(n, e, L)
    if not fac:
        print("!! echec de factorisation")
        return
    p, q = fac, n // fac
    print("p+q calcule en %.0fs" % (time.time() - t0), flush=True)
    s.sendall(str(p + q).encode() + b"\n")
    buf = b""
    until(b"}", timeout=60)
    out = buf.decode("latin-1", "replace")
    print(out[-500:], flush=True)
    mm = re.search(r"academy\{[^}]*\}", out)
    if mm:
        print("FLAG:", mm.group(0))
        open(r"./_z_120_flag.txt", "w").write(mm.group(0))
    s.close()


if __name__ == "__main__":
    main()
