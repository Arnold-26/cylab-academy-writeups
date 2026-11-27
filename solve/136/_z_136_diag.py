import random, sys
exec(open('/mnt/d/ctf-index/_z_136_solve.py').read().split('# ------------------------------------------------------------------ client')[0])

seed = 1
random.seed(seed)
key = bytes(random.randrange(256) for _ in range(40))
K = [int.from_bytes(key[8 * i:8 * i + 8], 'big') for i in range(5)]
blocks, pi, ci = build_blocks(4096)
cts = [enc_block(b.to_bytes(8, 'big'), key) for b in blocks]
print("true key:", ['%016x' % k for k in K])

ct_pairs = [(cts[i], cts[j]) for i, j in pi]
frontier = [([], ct_pairs)]
beam = 8
for level in (5, 4, 3, 2):
    cand = []
    for keys, pr in frontier:
        b, cnt = best_oi(pr)
        if b is None or cnt < 6:
            continue
        for o in (b | 1, (b | (1 << 63)) | 1):
            inv = pow(o, -1, 1 << 64)
            for k in (o, o ^ 1):
                np_ = [((g((y * inv) & MASK64) ^ k), (g((y2 * inv) & MASK64) ^ k))
                       for y, y2 in pr]
                cand.append(([k] + keys, np_))
    true_tail = [K[level - 1]] + [K[j] for j in range(level, 5)]
    present = any(keys == true_tail for keys, _ in cand)
    scored = []
    for keys, pr in cand:
        bc, c = best_oi(pr)
        scored.append((c, keys, pr))
    scored.sort(key=lambda t: -t[0])
    tsc = [c for c, keys, pr in scored if keys == true_tail]
    if level == 2:
        frontier = cand
    else:
        frontier = [(keys, pr) for c, keys, pr in scored[:beam]]
    print("level %d: cand=%d true_in_cand=%r true_score=%r top=%r frontier=%d" %
          (level, len(cand), present, tsc[:2], [c for c, _, _ in scored[:4]], len(frontier)))

# now the k1 stage over the frontier
found = 0
for keys, pr in frontier:
    k5, k4, k3, k2 = keys
    y1 = []
    for c in cts:
        x = c
        for k in (k5, k4, k3, k2):
            x = g((x * pow(k | 1, -1, 1 << 64)) & MASK64) ^ k
        y1.append(x)
    for i, j in ci[:4]:
        d = (y1[j] - y1[i]) & MASK64
        for o in (d, (-d) & MASK64):
            if not (o & 1):
                continue
            k1 = g((y1[i] * pow(o, -1, 1 << 64)) & MASK64) ^ blocks[i]
            if (k1 | 1) != o:
                continue
            cand = [k1, k2, k3, k4, k5]
            kb = b''.join(k.to_bytes(8, 'big') for k in cand)
            ok = enc_block(blocks[0].to_bytes(8, 'big'), kb) == cts[0]
            if ok:
                found += 1
                print("FOUND", ['%016x' % k for k in cand], "correct:", kb == key)
print("frontier=%d found=%d" % (len(frontier), found))
print("true in frontier (k2..k5):", any(keys == [K[4], K[3], K[2], K[1]] for keys, _ in frontier))
print("true in frontier (k5..k2 rev):", any(keys == [K[1], K[2], K[3], K[4]] for keys, _ in frontier))
for keys, _ in frontier[:4]:
    print("   branch", ['%016x' % k for k in keys])
