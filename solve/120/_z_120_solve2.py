import socket, sys, time, re, hashlib, random, os
import multiprocessing as mp
from flint import fmpz_mod_poly_ctx
from Crypto.Util.number import GCD

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HOST, PORT = open(r"./_z_120url.txt").read().split()
PORT = int(PORT)
LOG = open("./_z_120_log.txt", "w", buffering=1)


def log(*a):
    msg = " ".join(str(x) for x in a)
    print(msg, flush=True)
    LOG.write("[%s] %s\n" % (time.strftime("%H:%M:%S"), msg))


def pow_worker(args):
    prefix, target, start, step = args
    i = start
    while True:
        if hashlib.md5(prefix + str(i).encode()).digest()[-3:] == target:
            return prefix + str(i).encode()
        i += step


def solve_pow(prefix, target_hex, nproc=8):
    prefix_b = prefix.encode()
    target = bytes.fromhex(target_hex)
    t0 = time.time()
    ctx = mp.get_context("fork")
    with ctx.Pool(nproc) as pool:
        for res in pool.imap_unordered(pow_worker,
                                       [(prefix_b, target, k, nproc) for k in range(nproc)],
                                       chunksize=1):
            log("  PoW trouve en %.1fs : %r" % (time.time() - t0, res))
            pool.terminate()
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
    log("  deg(P)=%d construit en %.1fs" % (P.degree(), time.time() - t0))
    pts = []
    x = 1
    for a in range(L):
        pts.append(x)
        x = x * u % n
    t1 = time.time()
    vals = P.multipoint_evaluate(pts)
    log("  multipoint eval en %.1fs" % (time.time() - t1))
    for a, val in enumerate(vals):
        gg = GCD(int(val), n)
        if 1 < gg < n:
            log("  facteur trouve a a=%d, total %.1fs" % (a, time.time() - t0))
            return gg
    return None


def main():
    s = socket.create_connection((HOST, PORT), timeout=60)
    s.settimeout(30)
    buf = b""

    def until(pat, timeout=3600):
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

    log("cible", HOST, PORT)
    until(b"hex digits: ")
    head = buf.decode("latin-1")
    m = re.search(r"starts with \"(\d{5})\".*?hex digits: ([0-9a-f]{6})", head, re.S)
    log("PoW prefixe=%s cible=%s" % (m.group(1), m.group(2)))
    ans = solve_pow(m.group(1), m.group(2))
    s.sendall(ans.encode() + b"\n")
    buf = b""
    until(b"Clue : ")
    txt = buf.decode("latin-1")
    n = int(re.search(r"Public Modulus :\s+(\d+)", txt).group(1))
    e = int(re.search(r"Clue :\s+(\d+)", txt).group(1))
    log("n=%d bits e=%d bits" % (n.bit_length(), e.bit_length()))
    t0 = time.time()
    fac = attack(n, e, 1 << 18)
    if not fac:
        log("!! echec")
        return
    p, q = fac, n // fac
    log("p*q verifie:", p * q == n, "attaque en %.0fs" % (time.time() - t0))
    s.sendall(str(p + q).encode() + b"\n")
    log("p+q envoye")
    buf = b""
    until(b"}", timeout=120)
    out = buf.decode("latin-1", "replace")
    mm = re.search(r"academy\{[^}]*\}", out)
    log("reponse:", out[-300:])
    if mm:
        log("FLAG:", mm.group(0))
        open("./_z_120_flag.txt", "w").write(mm.group(0))
    s.close()


main()
