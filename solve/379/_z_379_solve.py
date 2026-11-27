import sys, time, re, subprocess, socket
import sympy

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
from Crypto.Util.number import inverse, bytes_to_long, long_to_bytes
from string import ascii_letters, digits

T127 = 1 << 127
T129 = 1 << 129
E = 65537
LIMIT = 1 << 129
CHARS = set((ascii_letters + digits).encode())
HOST, PORT = open("./_z_379url.txt").read().split()
PORT = int(PORT)


def log(*a):
    print("[%s]" % time.strftime("%H:%M:%S"), *a, flush=True)


def trial_divide(n, bound=1000000):
    fs = {}
    for p in sympy.primerange(2, bound):
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            fs[p] = e
        if n == 1:
            break
    return fs, n


def ecm_factor(n, b1, curves, timeout=60):
    try:
        r = subprocess.run(["ecm", "-c", str(curves), str(b1)], input=str(n).encode(),
                           capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None
    out = r.stdout.decode() + r.stderr.decode()
    for m in re.finditer(r"Factor found in step \d+: (\d+)", out):
        f = int(m.group(1))
        if 1 < f < n and n % f == 0:
            return f
    return None


def factorise(K, budget=240.0):
    fs, rem = trial_divide(K)
    t0 = time.time()
    stages = ((11000, 40, 20), (50000, 60, 40), (250000, 40, 80), (1000000, 30, 150))
    for b1, curves, to in stages:
        while time.time() - t0 < budget:
            if rem == 1 or sympy.isprime(rem):
                break
            if rem.bit_length() < 60:
                f = sympy.factorint(rem)
                for p2, e2 in f.items():
                    fs[p2] = fs.get(p2, 0) + e2
                rem = 1
                break
            f = ecm_factor(rem, b1, curves, timeout=to)
            if not f:
                break
            sub, subrem = trial_divide(f, 10000)
            for p2, e2 in sub.items():
                fs[p2] = fs.get(p2, 0) + e2
            rem = rem // f
            if subrem > 1:
                fs[subrem] = fs.get(subrem, 0) + 1
            log("    facteur %d bits (B1=%d) a %.0fs" % (f.bit_length(), b1, time.time() - t0))
        if rem == 1 or sympy.isprime(rem):
            break
    if rem > 1 and sympy.isprime(rem):
        fs[rem] = fs.get(rem, 0) + 1
        rem = 1
    log("    factorisation: %d facteurs distincts, reste %d bits, %.0fs"
        % (len(fs), rem.bit_length() if rem > 1 else 0, time.time() - t0))
    return fs, rem


def find_split(fs, rem, maxnodes=3000000):
    primes = []
    for p, e in fs.items():
        primes += [p] * e
    if rem > 1:
        primes.append(rem)
    primes.sort(reverse=True)
    n = len(primes)
    suffix = [1] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix[i] = suffix[i + 1] * primes[i]
    res = []
    nodes = [0]

    def dfs(i, A, B, h):
        nodes[0] += 1
        if nodes[0] > maxnodes:
            raise RuntimeError("explosion DFS")
        if A > LIMIT or B > LIMIT or h >= E:
            return
        if A * suffix[i] < T127 or B * suffix[i] < T127:
            return
        if i == n:
            if T127 <= A < T129 and T127 <= B < T129:
                res.append((A, B, h))
            return
        p = primes[i]
        if A * p <= LIMIT:
            dfs(i + 1, A * p, B, h)
        if B * p <= LIMIT:
            dfs(i + 1, A, B * p, h)
        if h * p < E:
            dfs(i + 1, A, B, h * p)

    dfs(0, 1, 1, 1)
    log("    DFS: %d noeuds, %d splits" % (nodes[0], len(res)))
    return res


def attempt():
    s = socket.create_connection((HOST, PORT), timeout=30)
    s.settimeout(15)
    buf = b""
    while b"vainglory?" not in buf:
        d = s.recv(65536)
        if not d:
            raise EOFError
        buf += d
    txt = buf.decode()
    ct = int(re.search(r"anger = (\d+)", txt).group(1))
    dval = int(re.search(r"envy = (\d+)", txt).group(1))
    log("ct=%d bits, d=%d bits" % (ct.bit_length(), dval.bit_length()))
    K = E * dval - 1
    t0 = time.time()
    try:
        fs, rem = factorise(K, budget=240.0)
        cands = find_split(fs, rem)
    except RuntimeError as ex:
        log("   ", ex)
        s.close()
        return None
    for A, B, h in cands:
        p, q = A + 1, B + 1
        if not (sympy.isprime(p) and sympy.isprime(q)):
            continue
        n = p * q
        b = long_to_bytes(pow(ct, dval, n))
        if len(b) == 16 and all(c in CHARS for c in b):
            msg = b.decode()
            log("PLAINTEXT:", msg, "(%.0fs)" % (time.time() - t0))
            s.sendall(msg.encode() + b"\n")
            out = b""
            try:
                end = time.time() + 20
                while time.time() < end:
                    dd = s.recv(65536)
                    if not dd:
                        break
                    out += dd
            except socket.timeout:
                pass
            s.close()
            return out.decode("latin-1", "replace")
    s.close()
    return None


for it in range(1, 61):
    log("=== tentative", it)
    try:
        res = attempt()
    except Exception as ex:
        log("   erreur:", repr(ex))
        res = None
    if res:
        log("REPONSE:", res[-400:])
        m = re.search(r"academy\{[^}]*\}", res)
        if m:
            log("FLAG:", m.group(0))
            open("./_z_379_flag.txt", "w").write(m.group(0))
            break
