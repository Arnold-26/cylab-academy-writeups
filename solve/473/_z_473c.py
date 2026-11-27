import sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
CT = "OHMLFMWCAI"
res = []
for a in range(1, 26):
    if a % 2 == 0 or a == 13:
        continue  # pas inversible mod 26
    ainv = pow(a, -1, 26)
    for b in range(26):
        pt = ""
        for ch in CT:
            x = (ord(ch) - 65 - b) % 26
            pt += chr((x * ainv) % 26 + 65)
        res.append((pt, a, b))
# afficher les plausibles (mots prononcables)
print("total:", len(res))
for pt, a, b in res:
    vowels = sum(1 for c in pt if c in "AEIOUY")
    if 2 <= vowels <= 5:
        print(f"  a={a:2} b={b:2}  {pt}")
