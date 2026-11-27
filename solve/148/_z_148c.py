import sys, string
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ALPHABET = string.ascii_lowercase[:16]
ct = "emfakcakmklfajnnlpekfpkndlmildnmnnljenfckbalpglfnknaonebfcnodkpe"
idx = {c: i for i, c in enumerate(ALPHABET)}
nums = [idx[c] for c in ct]
print("longueur:", len(nums))

# contraintes : position paire -> 'd'(3) ou 'g'(6) ; position impaire -> 0..9
solutions = []
for L in range(1, 15):
    key = []
    ok = True
    for r in range(L):
        cands = []
        for k in range(16):
            good = True
            for i in range(len(nums)):
                if i % L != r:
                    continue
                p = (nums[i] - k) % 16
                if i % 2 == 0:
                    if p not in (3, 6):
                        good = False
                        break
                else:
                    if not (0 <= p <= 9):
                        good = False
                        break
            if good:
                cands.append(k)
        if len(cands) != 1:
            ok = False
            break
        key.append(cands[0])
    if ok:
        solutions.append((L, key))
        print(f"L={L} cle={''.join(ALPHABET[k] for k in key)}")

for L, key in solutions:
    b16 = "".join(ALPHABET[(nums[i] - key[i % L]) % 16] for i in range(len(nums)))
    # decodage b16 : chaque paire -> octet
    out = bytearray()
    for i in range(0, len(b16) - 1, 2):
        hi = ALPHABET.index(b16[i])
        lo = ALPHABET.index(b16[i + 1])
        out.append(hi * 16 + lo)
    try:
        txt = out.decode("ascii")
    except Exception:
        continue
    print(f"L={L} -> {txt!r}")
    if all(c in "abcdef0123456789" for c in txt):
        print("VALID hex flag:", txt)
