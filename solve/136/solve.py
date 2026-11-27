#!/usr/bin/env python3
# 136 - Clouds  (Cryptography, picoCTF 2021)
# Flag: not archived
# Write-up: ../../../writeups/cryptography/136-clouds.md
# This is the script that produced the flag; historical variants are in archive/.
#
# 136 Clouds — differential cryptanalysis of Nimbus (Furman delta = 2^63-2)
#
# round i:   y = g(x ^ k_i) * (k_i | 1)  mod 2^64        (g = 64-bit bit reversal)
#
# (1) k5..k2  : pairs with x ^ x' = DELTA.  If the difference reaches the multiplication
#               then (Lemma 1, a,a' even)  a+a' = DELTA  =>  y+y' = DELTA*o_i  =>
#               o_i mod 2^63 = ((y+y')/2) * inv(DELTA/2) mod 2^63.  The mode over
#               thousands of pairs is the answer; surviving fraction is 2^-(i-1).
# (2) k1      : the DELTA difference always survives round 1 (probability 1), so the sum
#               equation degenerates to o1 = 1.  Use instead plaintexts P and P ^ 2^63:
#               u = g(P^k1) and u^1, so  y' - y = +-o1  exactly  =>  o1 = +-d.
import os, sys, random, struct, time

MASK64 = (1 << 64) - 1
MASK63 = (1 << 63) - 1
DELTA = (1 << 63) - 2
HALF = DELTA >> 1
INV_HALF = pow(HALF, -1, 1 << 63)
TOP = 1 << 63

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

def dec_block(c, key):
    x = c
    for i in (4, 3, 2, 1, 0):
        k = int.from_bytes(key[8 * i:8 * i + 8], 'big')
        x = g((x * pow(k | 1, -1, 1 << 64)) & MASK64) ^ k
    return x

def best_oi(pairs):
    """o_i mod 2^63 from the mode of ((y+y')/2)*inv(DELTA/2).
    Pairs whose multiplicand a_i is ODD satisfy a+a' = 2^63 (=DELTA+2) instead of DELTA,
    which polls for the constant 2^62; drop it (o_i is odd so it can never be 2^62)."""
    hist = {}
    for y, y2 in pairs:
        s = (y + y2) & MASK64
        if s & 1:
            continue
        c = ((s >> 1) * INV_HALF) & MASK63
        if c == 0x4000000000000000:
            continue
        hist[c] = hist.get(c, 0) + 1
    if not hist:
        return None, 0
    b = max(hist, key=hist.get)
    return b, hist[b]

def recover_key(blocks, cts, pairs_idx, comp_idx, verbose=True, beam=8, mincnt=6):
    ct_pairs = [(cts[i], cts[j]) for i, j in pairs_idx]
    frontier = [([], ct_pairs)]                       # ([k5..k_i], pairs at current level)
    for level in (5, 4, 3, 2):
        cand = []
        for keys, pr in frontier:
            b, cnt = best_oi(pr)
            if b is None or cnt < mincnt:
                continue
            for o in (b | 1, (b | TOP) | 1):
                inv = pow(o, -1, 1 << 64)
                for k in (o, o ^ 1):
                    np_ = [((g((y * inv) & MASK64) ^ k), (g((y2 * inv) & MASK64) ^ k))
                           for y, y2 in pr]
                    cand.append(([k] + keys, np_))
        if level == 2:
            # the pairs are now round-1 outputs, where the histogram is degenerate
            # (see the k1 remark at the top): keep every branch, score nothing.
            frontier = cand
            if verbose:
                print("  level %d: %d branches kept for the k1 step" % (level, len(frontier)))
        else:
            scored = []
            for keys, pr in cand:
                _, c = best_oi(pr)
                scored.append((c, keys, pr))
            scored.sort(key=lambda t: -t[0])
            if verbose:
                print("  level %d: %d branches, top counts %r" %
                      (level, len(scored), [c for c, _, _ in scored[:4]]))
            frontier = [(keys, pr) for c, keys, pr in scored[:beam]]
        if not frontier:
            return []

    results = []
    for keys, pr in frontier:                          # keys = [k2,k3,k4,k5] (prepended)
        k2, k3, k4, k5 = keys
        y1 = []
        for c in cts:
            x = c
            for k in (k5, k4, k3, k2):
                x = g((x * pow(k | 1, -1, 1 << 64)) & MASK64) ^ k
            y1.append(x)
        for i, j in comp_idx:
            d = (y1[j] - y1[i]) & MASK64
            for o in (d, (-d) & MASK64):
                if not (o & 1):
                    continue
                k1 = g((y1[i] * pow(o, -1, 1 << 64)) & MASK64) ^ blocks[i]
                if (k1 | 1) != o:
                    continue
                cand = [k1, k2, k3, k4, k5]
                kb = b''.join(k.to_bytes(8, 'big') for k in cand)
                # blocks 0..2 are 0 / DELTA / 2^63: too structured, several key variants
                # agree on them.  Check a spread of generic blocks instead.
                chk = sorted({0, 1, len(blocks) // 7, len(blocks) // 3, len(blocks) // 2,
                              2 * len(blocks) // 3, len(blocks) - 1})
                if all(enc_block(blocks[t].to_bytes(8, 'big'), kb) == cts[t] for t in chk):
                    if verbose:
                        print("  KEY  " + ' '.join('%016x' % k for k in cand))
                    results.append(kb)
                    break
    return results

# ------------------------------------------------------------------ data layout
def build_blocks(npairs, maxnote=512):
    """4 plaintext blocks per unit j: A, A^DELTA, A^TOP, (A^TOP)^DELTA   (A = j<<2)"""
    blocks, pairs_idx, comp_idx = [], [], []
    for j in range(npairs):
        a = (j << 2) & MASK64
        group = [a, a ^ DELTA, a ^ TOP, (a ^ TOP) ^ DELTA]
        base = len(blocks)
        blocks.extend(group)
        pairs_idx.append((base + 0, base + 1))
        pairs_idx.append((base + 2, base + 3))
        comp_idx.append((base + 0, base + 2))
        comp_idx.append((base + 1, base + 3))
    return blocks, pairs_idx, comp_idx

def notes_from_blocks(blocks, maxnote=512):
    per = maxnote // 8
    return [blocks[i:i + per] for i in range(0, len(blocks), per)]

# ------------------------------------------------------------------ client
def run_client(host, port, npairs, verbose=True):
    from pwn import remote, process, context
    context.log_level = 'error'
    if host == 'local':
        p = process([sys.executable, os.path.abspath(__file__), '--server'], cwd='/tmp')
    else:
        p = remote(host, int(port))

    def store(hexstr):
        # the menu prompt "Selection? " has already been consumed by the previous action
        p.sendline(b'1')
        p.recvuntil(b'Give me a note to encrypt: ')
        p.sendline(hexstr.encode())
        p.recvuntil(b'Selection? ')
    def read(idx):
        p.sendline(b'2')
        p.recvuntil(b'What index would you like to read? ')
        p.sendline(str(idx).encode())
        line = p.recvline(timeout=10).strip()
        p.recvuntil(b'Selection? ')
        return line.decode()

    p.recvuntil(b'Selection? ', timeout=20)
    flag_hex = read(0)
    if verbose:
        print("[*] flag ciphertext: %s (%d bytes)" % (flag_hex, len(flag_hex) // 2))

    blocks, pairs_idx, comp_idx = build_blocks(npairs)
    notes = notes_from_blocks(blocks)
    if verbose:
        print("[*] storing %d notes (%d blocks, %d delta pairs)" %
              (len(notes), len(blocks), len(pairs_idx)))
    t0 = time.time()
    for n in notes:
        store(b''.join(x.to_bytes(8, 'big') for x in n).hex())
    if verbose:
        print("[*] stored in %.1fs; reading back" % (time.time() - t0))
    cts = []
    for i in range(1, len(notes) + 1):
        h = read(i)
        for j in range(0, len(h) - 15, 16):
            cts.append(int(h[j:j + 16], 16))
    if verbose:
        print("[*] read %d note ciphertexts in %.1fs" % (len(cts), time.time() - t0))
    assert len(cts) >= len(blocks), (len(cts), len(blocks))
    cts = cts[:len(blocks)]

    keys = recover_key(blocks, cts, pairs_idx, comp_idx, verbose=verbose)
    if not keys:
        print("[-] key recovery failed")
        return None
    best = None
    for key in keys:
        ct = int(flag_hex, 16)
        nb = len(flag_hex) // 16
        out = b''
        for i in range(nb):
            b_i = (ct >> (64 * (nb - 1 - i))) & MASK64
            out += dec_block(b_i, key).to_bytes(8, 'big')
        out = out.rstrip(b'\x00')
        score = sum(1 for b in out if 32 <= b < 127)
        if verbose:
            print("[*] candidate (%d/%d printable): %r" % (score, len(out), out[:64]))
        if best is None or score > best[0]:
            best = (score, out)
    out = best[1]
    print("FLAG: %s" % out.decode('latin1'))
    return out

# ------------------------------------------------------------------ local server
def serve():
    key = bytes(random.randrange(256) for _ in range(40))
    open('/tmp/key', 'wb').write(key)
    flag = os.environ.get('FAKEFLAG', 'academy{clouds_local_test_flag_1234567890}')
    print("Welcome to the Sice Cream Store!\n...\nWhats your name?\n> ")
    sys.stdout.flush()
    notes = []
    def enc(msg):
        if len(msg) % 8:
            msg += b'\x00' * (8 - len(msg) % 8)
        return b''.join(enc_block(msg[i:i + 8], key).to_bytes(8, 'big')
                        for i in range(0, len(msg), 8)).hex()
    notes.append(enc(flag.encode()))
    while True:
        print("\n1) Store\n2) Retrieve\nAnything else to quit\n")
        sys.stdout.flush()
        sys.stdout.write("Selection? "); sys.stdout.flush()
        ui = sys.stdin.readline().strip()
        if ui == "1":
            sys.stdout.write("Give me a note to encrypt: "); sys.stdout.flush()
            h = sys.stdin.readline().strip()
            try:
                msg = bytes.fromhex(h)
            except Exception:
                print("Invalid input."); continue
            if len(msg) > 512:
                print("Invalid input.")
            else:
                notes.append(enc(msg))
        elif ui == "2":
            sys.stdout.write("What index would you like to read? "); sys.stdout.flush()
            try:
                idx = int(sys.stdin.readline().strip())
            except Exception:
                print("Invalid index."); continue
            if 0 <= idx < len(notes):
                print(notes[idx])
            else:
                print("Invalid index.")
        else:
            return

if __name__ == '__main__':
    if sys.argv[1:2] == ['--server']:
        serve()
    elif sys.argv[1:2] == ['selftest']:
        npairs = int(sys.argv[2]) if len(sys.argv) > 2 else 4096
        random.seed(int(os.environ.get('SEED', '1')))
        key = bytes(random.randrange(256) for _ in range(40))
        blocks, pi, ci = build_blocks(npairs)
        cts = [enc_block(b.to_bytes(8, 'big'), key) for b in blocks]
        ks = recover_key(blocks, cts, pi, ci)
        print("selftest ok:", len(ks) > 0 and ks[0] == key)
    elif sys.argv[1:2] == ['local']:
        run_client('local', 0, int(sys.argv[2]) if len(sys.argv) > 2 else 4096)
    else:
        host = sys.argv[1]; port = int(sys.argv[2])
        npairs = int(sys.argv[3]) if len(sys.argv) > 3 else 4096
        run_client(host, port, npairs)
