#!/usr/bin/env python3
# 136 Clouds — differential cryptanalysis of Nimbus (Furman's delta = 2^63-2)
#
# round i:  y = g(x ^ k_i) * (k_i | 1)  mod 2^64      (g = bit reversal of 64 bits)
#
# For a pair with x ^ x' = DELTA and a_i,a_i' even:
#     a_i ^ a_i' = DELTA  =>  a_i + a_i' = DELTA (Lemma 1)
#     y + y' = DELTA * o_i          o_i = k_i | 1
# =>  o_i mod 2^63 = ((y+y')/2) * inv(DELTA/2)  mod 2^63
# The mode over many pairs gives o_i; the surviving fraction is 2^-(i-1) per level,
# so a few thousand pairs are plenty.
import os, sys, random, struct, time

MASK64 = (1 << 64) - 1
MASK63 = (1 << 63) - 1
DELTA = (1 << 63) - 2
HALF = DELTA >> 1
INV_HALF = pow(HALF, -1, 1 << 63)
G = [None]
def g(x):
    x &= MASK64
    x = ((x & 0x5555555555555555) << 1) | ((x >> 1) & 0x5555555555555555)
    x = ((x & 0x3333333333333333) << 2) | ((x >> 2) & 0x3333333333333333)
    x = ((x & 0x0F0F0F0F0F0F0F0F) << 4) | ((x >> 4) & 0x0F0F0F0F0F0F0F0F)
    x = ((x & 0x00FF00FF00FF00FF) << 8) | ((x >> 8) & 0x00FF00FF00FF00FF)
    x = ((x & 0x0000FFFF0000FFFF) << 16) | ((x >> 16) & 0x0000FFFF0000FFFF)
    return ((x << 32) | (x >> 32)) & MASK64

def enc_block(block, key):
    r = int.from_bytes(block, 'big')
    for i in range(5):
        k = int.from_bytes(key[8 * i:8 * i + 8], 'big')
        r ^= k
        r = g(r)
        r = (r * (k | 1)) & MASK64
    return r

def dec_round(y, o, k):
    a = (y * pow(o, -1, 1 << 64)) & MASK64
    return g(a) ^ k

def best_oi(pairs):
    hist = {}
    for y, y2 in pairs:
        s = (y + y2) & MASK64
        if s & 1:
            continue
        c = ((s >> 1) * INV_HALF) & MASK63
        hist[c] = hist.get(c, 0) + 1
    if not hist:
        return None, 0
    b = max(hist, key=hist.get)
    return b, hist[b]

def recover_key(pairs, fam, plain, verbose=True, beam=6, mincnt=6):
    """pairs: [(c1,c2)] ciphertext blocks with P ^ P' = DELTA
       fam:   bit63 of the plaintext of each pair  (round-1 degeneracy workaround)
       plain: [(p1,p2)] the plaintexts (for final verification)
       returns list of [k1..k5] verified against the plaintexts"""
    frontier = [([], list(pairs))]            # ([k5..k_i], pairs at current level)
    for level in (5, 4, 3, 2):
        cand = []
        for keys, pr in frontier:
            b, cnt = best_oi(pr)
            if b is None or cnt < mincnt:
                continue
            for o in (b | 1, (b | (1 << 63)) | 1):
                inv = pow(o, -1, 1 << 64)
                for k in (o, o ^ 1):
                    np_ = [((g((y * inv) & MASK64) ^ k), (g((y2 * inv) & MASK64) ^ k))
                           for y, y2 in pr]
                    cand.append(([k] + keys, np_))
        scored = []
        for keys, pr in cand:
            _, c = best_oi(pr)
            scored.append((c, keys, pr))
        scored.sort(key=lambda t: -t[0])
        if verbose:
            print("  after level %d: %d candidates, top counts %r" %
                  (level, len(scored), [c for c, _, _ in scored[:4]]))
        frontier = [(keys, pr) for c, keys, pr in scored[:beam]]
        if not frontier:
            return []

    # ---- level 1: the input difference is DELTA for every pair, so Lemma 1 makes
    # P+P' = DELTA and the histogram degenerates to o1 == 1.  a1 = g(P^k1) has a
    # constant LSB (= bit63(P) ^ bit63(k1)); only the family with even a1 is usable.
    good = []
    for keys, pr in frontier:
        for want in (0, 1):
            sel = [pr[i] for i in range(len(pr)) if fam[i] == want]
            if len(sel) < 8:
                continue
            b, cnt = best_oi(sel)
            if b is None or b == 1:            # degenerate family
                continue
            if verbose:
                print("  level 1: family bit63=%d -> o1 cnt=%d val=%#x" % (want, cnt, b))
            for o in (b | 1, (b | (1 << 63)) | 1):
                inv = pow(o, -1, 1 << 64)
                for k in (o, o ^ 1):
                    cand = [k] + keys
                    kb = b''.join(x.to_bytes(8, 'big') for x in cand)
                    ok = all((g(((pr[i][0] * inv) & MASK64)) ^ k) == plain[i][0]
                             for i in range(min(4, len(pr))))
                    if ok:
                        good.append(cand)
    return good

# ---------------- self test ----------------
def make_pair_blocks(npairs):
    """P_j with bit0=0 and bit63 alternating; returns (P_j, P_j^DELTA)"""
    out = []
    for j in range(npairs):
        p = (((j & 1) << 63) | ((j >> 1) << 2)) & MASK64
        out.append((p, p ^ DELTA))
    return out

def selftest(npairs=4096):
    random.seed(int(os.environ.get('SEED', '1234')))
    key = bytes(random.randrange(256) for _ in range(40))
    bl = make_pair_blocks(npairs)
    fam = [(p >> 63) & 1 for p, _ in bl]
    plain = bl
    ct = [(enc_block(p.to_bytes(8, 'big'), key), enc_block(p2.to_bytes(8, 'big'), key))
          for p, p2 in bl]
    t0 = time.time()
    keys = recover_key(ct, fam, plain)
    print("selftest: %d verified key candidates in %.1fs" % (len(keys), time.time() - t0))
    real = [int.from_bytes(key[8 * i:8 * i + 8], 'big') for i in range(5)]
    ok = any(all(k[i] == real[i] for i in range(5)) for k in keys)
    print("selftest: correct key found:", ok)
    if keys:
        print("selftest: first candidate:", [hex(k) for k in keys[0]])
        print("selftest: real key        :", [hex(k) for k in real])
    return ok

if __name__ == '__main__':
    if sys.argv[1:2] == ['selftest']:
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 4096
        sys.exit(0 if selftest(n) else 1)
