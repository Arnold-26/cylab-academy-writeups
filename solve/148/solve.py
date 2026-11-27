# 148 - New Vignere  (Cryptography, picoCTF 2021)
# Flag: academy{468293b06253c715005873e333d98dbc}
# Write-up: ../../../writeups/cryptography/148-new-vignere.md
# Script exact utilise pour produire le flag.
#
import sys, string, itertools
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ALPHABET = string.ascii_lowercase[:16]
ct = "emfakcakmklfajnnlpekfpkndlmildnmnnljenfckbalpglfnknaonebfcnodkpe"
idx = {c: i for i, c in enumerate(ALPHABET)}
nums = [idx[c] for c in ct]

def b16_decode(b16):
    out = bytearray()
    for i in range(0, len(b16) - 1, 2):
        hi = ALPHABET.index(b16[i])
        lo = ALPHABET.index(b16[i + 1])
        out.append(hi * 16 + lo)
    return bytes(out)

for L in range(1, 15):
    classes = []
    total = 1
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
        if not cands:
            ok = False
            break
        classes.append(cands)
        total *= len(cands)
    if not ok or total > 2000000:
        continue
    found = 0
    for combo in itertools.product(*classes):
        b16 = "".join(ALPHABET[(nums[i] - combo[i % L]) % 16] for i in range(len(nums)))
        try:
            txt = b16_decode(b16).decode("ascii")
        except Exception:
            continue
        if all(c in "abcdef0123456789" for c in txt):
            print(f"L={L} cle={''.join(ALPHABET[k] for k in combo)} -> {txt}")
            found += 1
            if found > 3:
                break
