import sys, time, re, subprocess, socket, json
import sympy
from Crypto.Util.number import getPrime, inverse, bytes_to_long, long_to_bytes
from string import ascii_letters, digits

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
T127 = 1 << 127
T129 = 1 << 129
E = 65537
LIMIT = 1 << 129
CHARS = set((ascii_letters + digits).encode())


# ---------- factorisation ----------
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
        out = r.stdout.decode() + r.stderr.decode()
        for m in re.finditer(r"Factor found in step \d+: (\d+)", out):
            f = int(m.group(1))
            if 1 < f < n and n % f == 0:
                return f
    except subprocess.TimeoutExpired:
        pass
    return None


def factorise(n, budget=90.0, verbose=True):
    """retourne (dict prime->exp, reste non factorise)"""
    fs, rem = trial_divide(n)
    t0 = time.time()
    for b1, curves, to in ((11000, 60, 20), (50000, 120, 40), (250000, 150, 90)):
        if sympy.isprime(rem):
            break
        while time.time() - t0 < budget:
            f = ecm_factor(rem, b1, curves, timeout=to)
            if not f:
                break
            sub, subrem = trial_divide(f, 10000)
            for p, e in sub.items():
                fs[p] = fs.get(p, 0) + e
            rem = subrem
            if rem > 1:
                rem = rem  # f est entierement absorbe
            fs2 = {}
            if verbose:
                print("    facteur %d bits (B1=%d, %.0fs)" % (f.bit_length(), b1, time.time() - t0), flush=True)
            # reessaie sur le nouveau rem
        if sympy.isprime(rem):
            break
    if sympy.isprime(rem) and rem > 1:
        fs[rem] = fs.get(rem, 0) + 1
        rem = 1
    if verbose:
        print("    factorisation: %d facteurs distincts, reste %d bits (%.0fs)"
              % (len(fs), rem.bit_length() if rem > 1 else 0, time.time() - t0), flush=True)
    return fs, rem


# ---------- recherche du split ----------
def find_split(fs, rem):
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

    def dfs(i, A, B, h):
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
    return res


def try_solve(ct, d, fs, rem, verbose=True):
    cands = find_split(fs, rem)
    if verbose:
        print("    %d splits candidats" % len(cands), flush=True)
    for A, B, h in cands:
        p, q = A + 1, B + 1
        if not (sympy.isprime(p) and sympy.isprime(q)):
            continue
        n = p * q
        m = pow(ct, d, n)
        b = long_to_bytes(m)
        if len(b) == 16 and all(c in CHARS for c in b):
            return b.decode()
    return None


# ---------- test synthetique ----------
def selftest():
    while True:
        p = getPrime(128); q = getPrime(128)
        if p == q:
            continue
        n = p * q
        phi = (p - 1) * (q - 1)
        try:
            d = inverse(E, phi)
        except Exception:
            continue
        break
    msg = "".join(__import__("random").choice(ascii_letters + digits) for _ in range(16))
    ct = pow(bytes_to_long(msg.encode()), E, n)
    K = E * d - 1
    print("test: message =", msg, " K bits:", K.bit_length())
    fs = {}
    for x in (p - 1, q - 1):
        for pr, ex in sympy.factorint(x).items():
            fs[pr] = fs.get(pr, 0) + ex
    h = K // phi
    fs[h] = fs.get(h, 0) + 1 if h > 1 else fs.get(h, 0)
    # h est deja dans phi? non : K = h*phi
    # on retire h de la factorisation totale si present
    tot = {}
    for pr, ex in fs.items():
        tot[pr] = ex
    # K = h * prod(phi) ; on a mis phi plus h, donc on a K exactement
    print("facteurs:", len(tot))
    t0 = time.time()
    got = try_solve(ct, d, tot, 1)
    print("split trouve:", got, "en %.2fs" % (time.time() - t0))


if __name__ == "__main__":
    selftest()
