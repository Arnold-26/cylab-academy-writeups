import random, sys, time
from flint import fmpz_mod_poly_ctx
from Crypto.Util.number import getPrime, inverse, GCD
from sympy.ntheory.modular import solve_congruence

sys.setrecursionlimit(10000)


def crt(a, m, b, n):
    val, mod = solve_congruence((a, m), (b, n))
    return val


def toy(bits_p=512, dp_bits=20):
    while True:
        p = getPrime(bits_p); q = getPrime(bits_p)
        if GCD(p - 1, q - 1) == 2:
            break
    while True:
        d_p = random.randint(1, 1 << dp_bits)
        d_q = random.randint(1, q - 1)
        if GCD(d_p, p - 1) != 1 or GCD(d_q, q - 1) != 1:
            continue
        if d_p % 2 == d_q % 2:
            d = crt(d_p, p - 1, d_q, q - 1)
            try:
                e = inverse(d, (p - 1) * (q - 1))
            except Exception:
                continue
            return p, q, d_p, e


def attack(n, e, L, verbose=True):
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
    t1 = time.time()
    if verbose:
        print("  deg(P)=%d construction %.1fs" % (P.degree(), t1 - t0))
    pts = []
    x = 1
    for a in range(L):
        pts.append(x)
        x = x * u % n
    vals = P.multipoint_evaluate(pts)
    t2 = time.time()
    if verbose:
        print("  multipoint %.1fs" % (t2 - t1))
    for a, val in enumerate(vals):
        gg = GCD(int(val), n)
        if 1 < gg < n:
            return gg, (t1 - t0, t2 - t1)
    return None, (t1 - t0, t2 - t1)


if __name__ == "__main__":
    dp_bits = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    p, q, d_p, e = toy(dp_bits=dp_bits)
    n = p * q
    L = 1 << ((dp_bits + 1) // 2)
    print("toy: p=%d bits, d_p=%d (<2^%d), L=%d" % (p.bit_length(), d_p, dp_bits, L))
    fac, tt = attack(n, e, L)
    print("facteur correct:", fac in (p, q) if fac else False, "| p =", p == fac)
    print("temps:", tt)
