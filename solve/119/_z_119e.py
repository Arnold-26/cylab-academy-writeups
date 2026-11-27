import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
out = [int(x) for x in open("/mnt/c/Users/arnol/AppData/Local/Temp/cylab_eps/119_output.txt").read().split()]
N = len(out)
randoms = [((i * 327) % 681 + 344) % 313 for i in range(1, N + 1)]
seeds = [(i * 127) % 500 for i in range(1, N + 1)]
funs = []
prev = 0
for i in range(N):
    funs.append(out[i] ^ prev ^ randoms[i])
    prev = out[i]

# compte les paires de 2 bits non conformes (ni 00 ni 11) pour plusieurs decalages
for align in range(0, 4):
    bad = 0
    total = 0
    for f in funs[:20]:
        v = f >> align
        for k in range(30):
            pair = (v >> (2 * k)) & 3
            total += 1
            if pair in (1, 2):
                bad += 1
    print(f"align {align}: paires non conformes {bad}/{total}")
# aussi : verifier que le fun ne depasse pas 60 bits
print("\nbits des funs:", sorted(set(f.bit_length() for f in funs))[:10])
# regarder un fun en binaire
f0 = funs[0]
print("fun0 bin:", format(f0, "060b"))
# paires
pairs = [(f0 >> (2 * k)) & 3 for k in range(30)]
print("paires:", pairs)
print("conformes:", all(p in (0, 3) for p in pairs))
